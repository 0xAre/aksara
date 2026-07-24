# Desain: UI/UX AKSARA — Mode Light, Cari, Reply, Scroll Wrap-Aware

Status: Disetujui (Opsi A) — 2026-07-24

## Konteks

AKSARA (fork awal dari ALTER v0.1.8) ingin mengejar sebagian perbaikan UI/UX yang sudah
ada di ALTER v0.6.0 (lokal: `E:\Project APP\Alter`), tanpa mengekspos hubungan ke ALTER
dan tanpa menyalin struktur modularnya secara mentah. Empat fitur yang diadopsi:
Mode Light (rebrand dari "mode buram" ALTER), cari pesan, reply, dan perbaikan scroll.
Layar login/auth AKSARA tidak berubah — tetap TUI seperti sekarang, tanpa penyamaran
branding (kebutuhan itu spesifik untuk ALTER yang harus bersembunyi; AKSARA tampil
terang-terangan).

## Pendekatan yang dipilih

**Opsi A — port ke struktur file AKSARA yang sudah ada** (`src/tui/mod.rs`,
`src/tui/ui.rs`, `src/session/mod.rs`), bukan meniru pemecahan modular ALTER
(`app.rs`/`chat.rs`/`theme.rs`/dst — 10+ file) dan bukan mem-port sistem negosiasi
kapabilitas penuh ala ALTER (`PeerCapable`, fallback peer lama). Alasan: AKSARA belum
sebesar itu, dan tidak ada peer versi lama yang perlu dikompatibilitaskan — kedua sisi
koneksi P2P AKSARA selalu menjalankan build yang sama.

## Komponen

### 1. Protokol — hanya untuk Mode Light tersinkron

`session::SessionCmd` baru menggantikan channel `UnboundedReceiver<String>` polos:

```rust
pub enum SessionCmd {
    Text(String),
    Blur(bool),
}
```

Encoding sebelum dienkripsi Noise: `Text(s)` → byte `0x00` + UTF-8 bytes; `Blur(b)` →
byte `0x01` + 1 byte (`0x01`/`0x00`). Setelah didekripsi di sisi penerima, byte pertama
menentukan hasil: `0x00` → `SessionEvent::Message(text)`, `0x01` →
`SessionEvent::PeerBlur(bool)`. Byte tidak dikenal → diabaikan (bukan fatal — beda
dari kegagalan dekripsi yang tetap fail-closed/putus koneksi).

Tidak ada negosiasi kapabilitas (`PeerCapable` dkk. dari ALTER sengaja tidak diport).

### 2. Mode Light (Ctrl+B)

Field baru di `App` (`src/tui/mod.rs`): `blur_enabled: bool`, `blur_synced: bool`,
`blur_prompt_open: bool`. Alur:
- Ctrl+B saat nonaktif → buka prompt `[L] Lokal saja / [B] Berdua / Esc batal`.
- `[L]` → aktif lokal, tidak kirim apa pun ke peer.
- `[B]` → kirim `SessionCmd::Blur(true)`, aktif tersinkron.
- Ctrl+B saat aktif → matikan (kirim `SessionCmd::Blur(false)` jika sedang tersinkron).
- `SessionEvent::PeerBlur(on)` dari peer → update state lokal + system chat line.

Render (`src/tui/ui.rs`, `render_chat_line`): pesan di luar `BLUR_KEEP_RECENT` (3)
pesan terbaru diberi style `DIM` alih-alih warna normal per pengirim.

**Semua string yang tampil ke pengguna memakai istilah "Mode Light"** — tidak pernah
"buram"/"blur" secara literal di UI.

### 3. Scroll wrap-aware

Bug yang ada sekarang: `render_chat_panel` menghitung
`start = messages.len().saturating_sub(inner_h)` — mengasumsikan 1 pesan = 1 baris
terminal, padahal `Paragraph` memakai `Wrap { trim: false }` sehingga pesan panjang
melebar jadi beberapa baris. Akibatnya pesan lama bisa "terdorong" keluar secara salah
hitung saat ada pesan panjang.

Perbaikan: tambah `scroll_offset: usize` di `App`, dan fungsi murni
`estimate_wrapped_lines(text: &str, width: usize) -> usize` (perkiraan
`ceil(char_count / width)`, bukan word-wrap persis dari ratatui — ditandai komentar
`ponytail:` di kode karena ini pendekatan, bukan replikasi wrap engine ratatui;
upgrade path: pakai `ratatui::text::Line` width measurement kalau presisi jadi masalah
nyata). Pilih pesan dari akhir sampai akumulasi estimasi baris ≥ tinggi panel.
Navigasi: `PageUp` mundur, `PageDown` maju (mengikuti konvensi ALTER).

### 4. Cari pesan (Ctrl+S)

Local-only, tidak sentuh protokol. Field baru: `search_active: bool`,
`search_query: String`, `search_matches: Vec<usize>` (indeks ke `app.messages`),
`search_cursor: usize`. Ctrl+S buka mode cari, Enter/panah pindah antar match,
Esc tutup. Match di-highlight beda style saat render.

### 5. Reply (Ctrl+R)

Local-only (dikonfirmasi dari kode ALTER — reply cuma konvensi format teks, bukan
frame protokol baru). Field baru: `replying_to: Option<String>` (kutipan yang sedang
dibalas), `select_reply_idx: Option<usize>` (mode pilih pesan sebelum reply aktif).
Saat mengirim balasan, teks yang dikirim (lewat `SessionCmd::Text`) diformat:
`↩ "kutipan…"\n<isi balasan>`. Penerima menampilkannya apa adanya (baris kutipan bisa
diberi style `DIM+ITALIC` saat parsing prefix `↩ "..."` di awal teks).

### 6. Tema warna

Tidak ada perubahan nilai — palet AKSARA (`ACCENT`/`DIM`/`TEXT`/`SUCCESS`/`WARNING`/
`ERROR` di `src/tui/ui.rs`) sudah identik dengan `theme.rs` ALTER v0.6.0. Item ini
selesai tanpa kerja tambahan.

### 7. Login/auth

Tidak diubah. Tetap TUI seperti sekarang. Fitur "penyamaran branding" ALTER (logo
tanpa wordmark) **tidak diadopsi** — itu kebutuhan spesifik ALTER untuk
menyembunyikan identitas aplikasi; AKSARA tidak butuh itu.

## Error handling

- Byte tipe payload tidak dikenal setelah dekripsi → diabaikan, bukan memutus koneksi.
- Kegagalan dekripsi (sudah ada) tetap fail-closed (putus koneksi) — tidak berubah.
- `SessionCmd::Blur` gagal terkirim (channel closed) → diperlakukan sama seperti
  `SessionCmd::Text` gagal (silent break dari loop existing, konsisten dengan pola
  yang sudah ada di `run_session`).

## Testing

Satu test per cabang baru, menambah ke suite yang sudah ada (target: tetap hijau +
test baru):

1. `session::mod` — roundtrip `SessionCmd::Blur` via TCP loopback (pola sama seperti
   `lan_session_message_roundtrip` yang sudah ada).
2. `tui::mod` — alur prompt Mode Light: `[L]` aktif lokal, `[B]` aktif tersinkron +
   terkirim ke channel, `Esc` batal tanpa aktif.
3. `tui::ui` (atau lokasi fungsi murni) — `estimate_wrapped_lines` untuk beberapa
   panjang teks/width.
4. Fungsi cari — match ditemukan/tidak ditemukan, cursor berpindah benar.
5. Fungsi format reply — quote-prefix terbentuk sesuai format `↩ "..."\n...`.

## Di luar scope (sengaja tidak dikerjakan sekarang)

- Struktur modular ala ALTER (`app.rs`/`chat.rs`/dst.) — file `mod.rs`/`ui.rs` AKSARA
  masih dalam ukuran wajar setelah fitur ini ditambahkan; split ditunda sampai
  benar-benar diperlukan.
- Negosiasi kapabilitas peer (`PeerCapable`) — tidak ada peer versi lama untuk
  dikompatibilitaskan.
- Fitur ALTER lain (private message/`pm.rs`, image, migrate, ruang tunggu halaman 2)
  — tidak diminta, tidak diadopsi.
