<div align="center">

```
 █████╗ ██╗  ██╗███████╗ █████╗ ██████╗   █████╗
 ██╔══██╗██║ ██╔╝██╔════╝██╔══██╗██╔══██╗ ██╔══██╗
 ███████║█████╔╝ ███████╗███████║██████╔╝ ███████║
 ██╔══██║██╔═██╗ ╚════██║██╔══██║██╔══██╗ ██╔══██║
 ██║  ██║██║  ██╗███████║██║  ██║██║  ██║ ██║  ██║
 ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═╝  ╚═╝
```

**Tanpa server. Tanpa perantara. Cuma kamu dan orang yang kamu ajak bicara.**

[![Release](https://img.shields.io/badge/release-v0.1.0-5dd4d4?style=flat-square)](https://github.com/0xAre/aksara/releases)
[![Rust](https://img.shields.io/badge/Rust-1.89+-orange?style=flat-square&logo=rust)](https://www.rust-lang.org)
[![License](https://img.shields.io/badge/License-Proprietary-lightgrey?style=flat-square)](LICENSE)
[![Build](https://img.shields.io/github/actions/workflow/status/0xAre/aksara/release.yml?style=flat-square)](https://github.com/0xAre/aksara/actions)

</div>

---

**Chat P2P terminal terenkripsi, serverless.** Dua orang chat end-to-end terenkripsi **tanpa server perantara** sama sekali — tidak ada perusahaan, tidak ada akun, tidak ada metadata percakapan yang tersimpan di pihak ketiga. Koneksi langsung antar perangkat lewat LAN, atau lintas internet via jaringan Tor.

> Model **Room-Bound Sync**: kedua pihak harus hadir di "room" yang sama secara bersamaan. Begitu salah satu keluar, kunci sesi di-*zeroize* permanen — *forward secrecy* penuh per sesi, bukan janji retensi data dari kebijakan perusahaan. Tidak ada arsip percakapan yang tersimpan untuk disalahgunakan di kemudian hari.

```
 AKSARA   Tor+LAN   Room terbuka.                   id:29a40f43d0
┌──── Kontak ─────┬─────────────────── Room ────────────────────┐
│ › ◈ Bob         │ ● Bob hadir di room                         │
│   ◇ Alice       ├─────────────────── Chat ────────────────────┤
│                 │ » halo Bob                                  │
│                 │ « hai, aman ini?                            │
├─────────────────┴─────────────────── Pesan ───────────────────┤
│ > ketik pesan...                                              │
└───────────────────────────────────────────────────────────────┘
 [Enter] kirim   [Esc] keluar room
```

---

## Instalasi

### Prasyarat
- **Rust** (toolchain stable, rustc ≥ 1.89) — pasang via <https://rustup.rs>
- **Windows**: Visual Studio Build Tools (MSVC) — dibutuhkan untuk mengompilasi SQLite bundled & kripto. Sudah ada jika Rust dipasang via rustup dengan MSVC host.
- **Linux/macOS**: toolchain C standar (`build-essential` / Xcode CLT).

Tidak butuh OpenSSL, tidak butuh menjalankan daemon Tor terpisah — semuanya terbungkus.

### Download siap-pakai — TANPA install Rust (paling mudah)
Untuk laptop yang masih kosong (belum ada Rust sama sekali), ambil binary jadi dari halaman **Releases**:

**<https://github.com/0xAre/aksara/releases>**

| OS | File | Cara pakai |
|---|---|---|
| Windows | `aksara-x86_64-pc-windows-msvc.exe` | Rename jadi `aksara.exe`, taruh di folder mana saja, dobel-klik / jalankan dari terminal. Sudah static — tidak perlu Visual C++ Redistributable. |
| Linux | `aksara-x86_64-unknown-linux-gnu` | `chmod +x aksara-* && ./aksara-*` |
| macOS (Apple Silicon) | `aksara-aarch64-apple-darwin` | `chmod +x aksara-* && ./aksara-*` |

Tidak perlu install apa pun. Tinggal jalankan.

**Windows — installer satu baris** (download + tambah ke PATH otomatis, tanpa Rust; repo harus publik):
```powershell
irm https://raw.githubusercontent.com/0xAre/aksara/main/install.ps1 | iex
```
Tutup & buka ulang terminal, lalu ketik `aksara`.

> Binary dibuat otomatis oleh GitHub Actions setiap rilis (lihat `.github/workflows/release.yml`).

### Pasang via Cargo (kalau sudah ada Rust)
```bash
cargo install --git https://github.com/0xAre/aksara
```
Setelah selesai, `aksara` langsung tersedia di PATH (lewat `~/.cargo/bin`). Tidak perlu setup tambahan.

### Build dari source lokal
```bash
git clone https://github.com/0xAre/aksara
cd aksara
cargo install --path .
```

---

## Pemakaian

Cukup panggil:
```bash
aksara            # ONLINE (LAN + Tor) — default, langsung masuk TUI
aksara --offline  # LAN murni (tanpa Tor, tanpa internet)
```

`aksara` langsung online: TUI muncul seketika (LAN siap pakai), sementara Tor di-bootstrap **di latar belakang**. Badge transport berubah `LAN` → `TOR+LAN` saat Tor siap (muncul notifikasi), dan invite code-mu otomatis menyertakan onion address. Tidak ada mode terpisah — satu binary, satu perintah.

Identitas (vault terenkripsi) disimpan di `~/.aksara/id.key` secara default, jadi `aksara` dari folder mana pun membuka identitas yang sama.

### Pertama kali
1. `aksara` → layar **Buat Identitas Baru** → set passphrase (+ konfirmasi).
2. Tekan `i` untuk melihat **invite code** kamu. Bagikan ke lawan bicara lewat channel aman lain.
3. Tekan `a` untuk menambah kontak (tempel invite code mereka, opsional + spasi + nickname).
4. Pilih kontak (`↑`/`↓`) → `Enter` untuk masuk room.

### Keybinding
| Tombol | Aksi |
|---|---|
| `↑` / `↓` | Pilih kontak |
| `Enter` | Masuk room / kirim pesan |
| `a` | Tambah kontak (otomatis tersimpan, terenkripsi) |
| `c` | Salin invite code-ku ke clipboard |
| `i` | Tampilkan invite code-ku |
| `Esc` | Keluar room |
| `q` | Keluar aplikasi |

**Di dalam room:**

| Tombol | Aksi |
|---|---|
| `Ctrl+B` | Mode Light — redupkan pesan lama di layar (anti-lihat-dari-belakang), pilih lokal saja atau tersinkron ke peer |
| `Ctrl+S` | Cari pesan dalam room |
| `Ctrl+R` | Balas (kutip) pesan tertentu |
| `PageUp` / `PageDown` | Scroll riwayat chat |

### Opsi CLI
```
aksara [opsi]            Jalankan TUI
aksara id [opsi]         Cetak invite code lalu keluar

  --vault <path>        Lokasi vault (default: ~/.aksara/id.key)
  --offline             Matikan Tor (LAN murni; tak butuh internet)
  --add <invite>        Pra-muat satu kontak
  --name <nickname>     Nickname untuk --add
  --listen <port>       Paksa mode responder (testing LAN 1 mesin)
  --dial <ip:port>      Paksa mode initiator (testing LAN 1 mesin)
```

Passphrase saat `aksara id` dibaca dari env `AKSARA_PASSPHRASE` bila diset (otomasi), selain itu dari stdin.

---

## Keamanan (ringkas)

- **Noise_IK** (`Noise_IK_25519_ChaChaPoly_BLAKE2s`) — mutual auth + forward secrecy + identity hiding.
- **Vault**: Argon2id (OWASP 2024: m=19 MiB, t=2, p=1) + ChaCha20-Poly1305. File 108 byte, **tanpa magic bytes** — tak bisa dibedakan dari data acak tanpa passphrase.
- **Zero-trace**: pesan hanya di RAM; kunci sesi di-`ZeroizeOnDrop` saat room ditutup.
- **Kontak tersimpan terenkripsi**: daftar kontak di-enkripsi ChaCha20-Poly1305 (key diturunkan dari identity via BLAKE2s) — social graph tidak plaintext di disk.
- **Tor**: onion service persisten untuk jalur internet; fallback otomatis LAN-first (3 dtk) → Tor.

> ⚠️ **Status: pre-rilis (M0–M2).** Belum diaudit pihak ketiga secara independen. Gunakan dengan pemahaman risiko untuk komunikasi sensitif hingga audit M4 selesai. Hardening tambahan (obfs4, padding) ada di milestone M3.

---

## Status pengembangan

- [x] **M0** — Fondasi: identity, vault, handshake Noise_IK
- [x] **M1** — LAN MVP: mDNS + TCP, TUI, chat 1-on-1
- [x] **M2** — Jalur internet: Tor onion service + fallback
- [ ] **M3** — Hardening: obfs4 (anti-DPI/pemblokiran ISP), traffic padding
- [ ] **M4** — Polish & audit internal

## Lisensi

Proprietary — All rights reserved. © 2026 Andika Aryansyach.
