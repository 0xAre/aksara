# Plan: Timestamp per Pesan (Jam Lokal, Bukan dari Peer)

Status: Belum dieksekusi — untuk dilanjutkan sesi lain (mis. Antigravity).

## Keputusan

- Timestamp **selalu dicatat lokal saat pesan di-push ke `messages`** (baik pesan
  sendiri maupun pesan peer), BUKAN dikirim lewat wire protocol Noise. Peer tidak
  bisa dipercaya untuk klaim jam sendiri — kalau perlu jam peer, itu berarti
  menambah trust boundary baru tanpa manfaat nyata untuk chat 1:1.
- Tidak ada perubahan protokol (`SessionCmd`/`SessionEvent`/`TYPE_TEXT`) sama sekali.
  Ini murni fitur tampilan TUI.
- Tambah dependency `chrono` (fitur default saja, tanpa `serde`) untuk format
  `HH:MM` lokal — `std::time::SystemTime` tidak bisa breakdown kalender/lokal
  tanpa crate tambahan.

## Perubahan

### 1. `Cargo.toml`
Tambah `chrono = "0.4"`.

### 2. `src/tui/mod.rs`
- `ChatLine` (baris ~92): tambah field `pub time: chrono::DateTime<chrono::Local>`.
- `ChatLine::me/peer/system` (baris ~97-107): isi `time: chrono::Local::now()` di
  ketiganya.
- Semua call site `ChatLine::me(...)` / `ChatLine::peer(...)` / `ChatLine::system(...)`
  tidak perlu berubah (constructor yang urus, bukan caller) — cek baris 738, 746,
  749, 768, 987, 1022, 1030, 1035, 1039, 1044, 1049.

### 3. `src/tui/ui.rs` — jam rata kanan di ujung baris yang sama

Pesan tetap rata kiri (`  → `/`  ← `/`  ·  ` + teks seperti sekarang), jam
ditambahkan sebagai span terpisah di ujung kanan baris yang sama, dipisah spasi
padding — bukan prefix di depan.

- `render_chat_line` (baris ~682) perlu tambah parameter `width: usize` (dari
  `inner_w` yang sudah dihitung di baris ~579). Signature jadi
  `fn render_chat_line(line: &ChatLine, dim: bool, highlight: bool, width: usize) -> Line<'_>`.
- Call site baris ~608: `render_chat_line(msg, dim, highlight, inner_w)`.
- Di dalam fungsi, untuk tiap varian (Me/Peer/System/dim/highlight): hitung
  `time_str = line.time.format("%H:%M").to_string()`, lalu
  `pad = width.saturating_sub(prefix_len + text_len + time_len).max(1)` (pakai
  `.chars().count()` untuk panjang — ponytail: tidak unicode-width-aware untuk
  karakter lebar-ganda/CJK, upgrade ke crate `unicode-width` kalau kelak jadi
  masalah nyata), lalu tambahkan span spasi sepanjang `pad` + span jam
  (`Style::default().fg(DIM)`) di akhir vector span tiap varian.
- **Batasan yang harus didokumentasikan di kode (komentar 1 baris)**: kalau
  `text` sendiri lebih panjang dari `width` (pesan bakal wrap ke beberapa baris
  oleh `Paragraph::wrap`), jam tetap nempel tepat setelah teks (pad minimal 1),
  BUKAN pindah ke ujung kanan baris visual terakhir — karena `Line` di ratatui
  cuma satu unit teks, wrap terjadi di layer render setelahnya dan tidak bisa
  dikontrol per-baris-visual dari sini. Ini simplification yang disengaja,
  bukan bug.
- `estimate_wrapped_lines` (baris ~587) tetap dihitung dari `line.text` polos
  (tanpa jam) — jam hanya menambah lebar pada baris pertama, tidak mengubah
  jumlah baris wrap secara signifikan untuk kasus umum, jadi tidak perlu ubah.

### 4. Test
- Test manual/unit di `tui/mod.rs` (sekitar baris 1132-1134, test yang sudah bikin
  `ChatLine::me/peer/system`) — tinggal assert `time` ada (non-panic), tidak perlu
  assert nilai eksak karena `Local::now()` tidak deterministik.
- Tidak ada test protokol baru diperlukan — tidak ada perubahan di `session/mod.rs`
  atau `crypto/handshake.rs`.

## Verifikasi

```
cargo check
cargo test
```

## Di luar scope (jangan dikerjakan kecuali diminta)

- Timestamp presisi detik atau tanggal penuh.
- Sinkronisasi jam antar peer / NTP.
- Menampilkan fingerprint kontak untuk verifikasi manual anti-MITM (dibahas
  terpisah, fitur lain).
