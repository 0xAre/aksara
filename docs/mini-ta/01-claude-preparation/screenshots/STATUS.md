# TAHAP 12 — Status Screenshot Aplikasi AKSARA

Status: **PARTIAL** — verifikasi fungsi build+run **selesai** dan **berhasil**; pengambilan screenshot TUI aktual **BLOCKED** (perlu tindakan manual pengguna). Status ini **tidak menghalangi** `ready_for_codex` (screenshot bukan bagian dari 17 syarat quality gate `CLAUDE_PREPARATION_BRIEF.md`).

---

## 1. Verifikasi Build (Selesai, Berhasil)

```
cargo build --release
```

Dijalankan dari root repository pada commit `450d484` (2026-07-26), tanpa perubahan apapun pada `src/`/`Cargo.toml`/`Cargo.lock` (sesuai `AGENTS.md` §Source-Code Protection — hanya `cargo build` dijalankan, bukan editing).

| Item | Hasil |
|---|---|
| Exit code | `0` |
| Warnings | 0 |
| Errors | 0 |
| Waktu build | 9 menit 0 detik (build pertama, termasuk seluruh dependency `arti-client`/`tor-hsservice` 0.43.0) |
| Binary dihasilkan | `target/release/aksara.exe` (8.772.608 byte) |
| Versi package | `aksara v0.2.1` (dikonfirmasi dari baris `Compiling aksara v0.2.1 (E:\Project APP\AKSARA)`) — cocok dengan status v0.2.1 di `AGENTS.md` |

**Kesimpulan**: source code AKSARA pada commit ini **terbukti dapat dikompilasi bersih** tanpa warning/error — verifikasi fresh sesi ini, bukan diklaim ulang dari catatan lama tanpa rerun (sesuai `AGENTS.md` "jangan mempresentasikan sebagai baru terverifikasi kecuali dijalankan ulang").

---

## 2. Verifikasi Fungsi via CLI Non-Interaktif (Selesai, Berhasil)

TUI penuh (`ratatui`/`crossterm`) memerlukan terminal interaktif yang tidak dapat ditangkap tool di lingkungan ini (§3). Sebagai gantinya, subcommand `aksara id` (mencetak invite code lalu keluar, tidak memerlukan TUI — lihat `src/main.rs` fungsi `help_text()`) dipakai untuk memverifikasi fungsi identity/vault end-to-end secara non-interaktif. Dijalankan dengan passphrase dummy (`demo-mini-ta-verification-only`, BUKAN passphrase produksi apapun) pada vault sementara di direktori scratch (dihapus setelah verifikasi, tidak disimpan ke repository).

| Skenario | Perintah (bentuk umum) | Hasil |
|---|---|---|
| Buat identitas baru | `aksara id --vault <path> --offline` (vault belum ada) | `Vault tidak ditemukan... Membuat identitas baru... Identitas dibuat dan disimpan.` — mencetak invite code (base64url 87 karakter) dan fingerprint (64 hex, dikelompokkan 8×8) sesuai format yang didokumentasikan `06_PROTOCOL_SPECIFICATION.md` §3 dan `07_KEY_LIFECYCLE.md` §2 |
| Unlock identitas yang sama (passphrase benar) | `aksara id --vault <path> --offline` (vault sudah ada, passphrase identik) | Mencetak **invite code dan fingerprint yang persis sama** dengan langkah sebelumnya — membuktikan `seal()`/`unseal()` deterministik terhadap identitas yang sama (`07_KEY_LIFECYCLE.md` §3.2) |
| Unlock dengan passphrase salah | `aksara id --vault <path> --offline` (passphrase berbeda) | `Error: vault could not be opened`, exit code `1` — mengonfirmasi langsung pesan error ambigu yang disengaja (anti-oracle attack) yang didokumentasikan `07_KEY_LIFECYCLE.md` §3.4 |

**Kesimpulan**: fungsi inti manajemen identitas (generate → seal → unseal → reject salah passphrase) **terverifikasi berjalan sesuai dokumentasi TAHAP 6/7** pada binary hasil build sesi ini — bukan hanya klaim dari pembacaan kode statis.

Tidak ada output di atas yang memuat passphrase asli pengguna, private key mentah, atau data produksi — seluruhnya dummy/sementara dan sudah dibersihkan dari disk pasca-verifikasi (sesuai `CLAUDE_PREPARATION_BRIEF.md` TAHAP 12 aturan #6-9).

---

## 3. Screenshot TUI Aktual — BLOCKED (Perlu Tindakan Manual Pengguna)

**Alasan blocking**: AKSARA adalah aplikasi TUI penuh (`ratatui`+`crossterm`) yang memerlukan terminal interaktif dengan rendering karakter/warna real-time. Lingkungan eksekusi sesi ini hanya menyediakan:
- Bash non-interaktif (tanpa PTY/terminal emulator yang dapat merender TUI ratatui).
- Browser pane (Playwright/Claude Browser) — hanya untuk halaman web, tidak dapat membuka atau menangkap aplikasi terminal native.
- Tidak ada tool screenshot level-OS (mis. capture layar Windows) yang terhubung ke sesi ini.

Ini **bukan** kegagalan aplikasi — AKSARA terbukti berjalan benar (§1-2). Ini murni keterbatasan tooling capture pada environment eksekusi agent, sudah dicatat sejak `PROGRESS.md`/`WORKFLOW_STATE.yaml` SESSION sebelumnya.

### Instruksi Pengambilan Manual (untuk pengguna/anggota kelompok)

Ambil **2-4 screenshot** dari daftar berikut (per `CLAUDE_PREPARATION_BRIEF.md` TAHAP 12), simpan sebagai PNG di folder ini (`docs/mini-ta/01-claude-preparation/screenshots/`) dengan nama deskriptif (mis. `01-antarmuka-utama.png`):

1. **Antarmuka utama** — jalankan `cargo run --release -- --offline` (mode LAN-only, tidak perlu Tor/internet), tunggu TUI tampil.
2. **Manajemen identitas/kunci** — layar saat identitas baru dibuat atau invite code ditampilkan di dalam TUI (bukan hasil CLI `id`, tapi tampilan TUI-nya).
3. **Proses komunikasi** — dua instance AKSARA di dua terminal (satu `--listen <port>`, satu `--dial 127.0.0.1:<port>`, memakai vault berbeda via `--vault`) yang sudah terhubung dan bertukar pesan chat dummy.
4. **Status enkripsi/pengiriman** atau **output pengujian** — badge status koneksi (LAN/TOR) di TUI, atau output `cargo test` di terminal.

**Wajib dipatuhi saat mengambil screenshot** (sesuai brief, jangan dilanggar):
- Jangan menampilkan passphrase asli, private key mentah, token, atau kredensial apapun — pakai passphrase dummy seperti pada §2.
- Jangan mengubah UI produksi demi kebutuhan screenshot.
- Gunakan nickname/invite code/pesan chat dummy yang aman (bukan data pribadi nyata).
- Jangan membuat mockup atau editan gambar yang meniru tampilan aplikasi — hanya screenshot layar aktual dari binary yang benar-benar berjalan.

Setelah screenshot tersedia, update `11_FIGURE_MANIFEST.md` (tambahkan baris baru) dan `HANDOFF_TO_CODEX.yaml` (TAHAP 17, SESSION 5) untuk mereferensikannya.

---

## Ringkasan Confidence

| Klaim | Confidence | Catatan |
|---|---|---|
| Build bersih 0 warning/0 error pada commit `450d484` | HIGH | Dijalankan fresh sesi ini, exit code 0 diverifikasi langsung |
| Fungsi generate/seal/unseal/reject-salah-passphrase berjalan sesuai dokumentasi | HIGH | Diverifikasi via eksekusi CLI nyata (bukan pembacaan kode saja), output dicocokkan langsung ke `07_KEY_LIFECYCLE.md` §3.2/§3.4 |
| Screenshot TUI aktual | `MANUAL_USER_ACTION_REQUIRED` | Tidak ada tool capture OS/terminal di environment agent ini — bukan keterbatasan aplikasi |

---

## Referensi

Tidak ada referensi teori baru — verifikasi ini murni eksekusi binary terhadap klaim yang sudah dirujuk di `06_PROTOCOL_SPECIFICATION.md` dan `07_KEY_LIFECYCLE.md` (citekey sudah ada di `references/REFERENCES.bib`).
