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

[![Release](https://img.shields.io/badge/release-v0.2.1-5dd4d4?style=flat-square)](https://github.com/0xAre/aksara/releases)
[![Rust](https://img.shields.io/badge/Rust-1.89+-orange?style=flat-square&logo=rust)](https://www.rust-lang.org)
[![License](https://img.shields.io/badge/License-Proprietary-lightgrey?style=flat-square)](LICENSE)
[![CI](https://img.shields.io/github/actions/workflow/status/0xAre/aksara/ci.yml?branch=main&style=flat-square&label=CI)](https://github.com/0xAre/aksara/actions/workflows/ci.yml)

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

Pilih satu — yang pertama tidak butuh Rust sama sekali.

### 1. Download binary (paling mudah)

Ambil file untuk OS-mu dari **[halaman Releases](https://github.com/0xAre/aksara/releases)**, lalu jalankan. Tidak ada yang perlu dipasang.

| OS | File | Menjalankan |
|---|---|---|
| Windows | `aksara-x86_64-pc-windows-msvc.exe` | Rename jadi `aksara.exe`, taruh di folder mana saja, dobel-klik atau panggil dari terminal. Sudah static — tanpa Visual C++ Redistributable. |
| Linux | `aksara-x86_64-unknown-linux-gnu` | `chmod +x aksara-* && ./aksara-*` |
| macOS (Apple Silicon) | `aksara-aarch64-apple-darwin` | `chmod +x aksara-* && ./aksara-*` |

Di Windows ada jalur satu baris yang sekalian menambahkan ke PATH:

```powershell
irm https://raw.githubusercontent.com/0xAre/aksara/main/install.ps1 | iex
```

Tutup dan buka ulang terminal, lalu ketik `aksara`.

### 2. Pasang via Cargo

```bash
cargo install --git https://github.com/0xAre/aksara
```

`aksara` langsung tersedia lewat `~/.cargo/bin`.

### 3. Build dari source

```bash
git clone https://github.com/0xAre/aksara
cd aksara
cargo install --path .
```

Butuh Rust stable (rustc ≥ 1.89) dari <https://rustup.rs>, plus toolchain C bawaan platform — MSVC Build Tools di Windows (sudah ikut kalau Rust dipasang via rustup dengan host MSVC), `build-essential` di Linux, Xcode CLT di macOS.

Tidak butuh OpenSSL, dan tidak perlu menjalankan daemon Tor terpisah — semuanya terbungkus di dalam binary.

> **Upgrade dari v0.1.0?** Kalian berdua harus update bersamaan. Fingerprint identitas berubah di v0.2.0, jadi peer v0.1.0 dan v0.2.0 tidak akan saling menemukan — dan satu-satunya gejala yang terlihat hanyalah "peer tidak ketemu". Tukar ulang invite code setelah update. Detailnya di [CHANGELOG](CHANGELOG.md).

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

### Verifikasi kontak

Invite code ditukar di luar aplikasi, jadi AKSARA tidak bisa tahu apakah yang kamu tempel benar-benar dari orang yang kamu maksud. Yang memastikannya adalah **fingerprint**, dan itu tugas kamu:

1. Tekan `i` untuk melihat fingerprint-mu (juga tercetak oleh `aksara id`).
2. Buka fingerprint kontak di panel kontak.
3. Bacakan lewat jalur **berbeda** dari tempat kamu menukar invite — telepon, tatap muka, aplikasi lain. Kalau invite dikirim lewat WhatsApp, jangan verifikasi lewat WhatsApp juga.

Cocok → aman. **Berbeda walau satu karakter → jangan masuk room.** Artinya invite yang kamu terima sudah diubah di tengah jalan.

Fingerprint diturunkan dari kunci identitas *dan* kunci enkripsi sekaligus, jadi invite yang dimodifikasi selalu mengubah fingerprint — tidak bisa dipalsukan agar tetap terlihat sama.

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

Tiap baris chat menampilkan jam lokal di sisi kanan. Waktunya diambil dari jam perangkatmu sendiri dan tidak pernah dikirim ke lawan bicara.

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
- **Fingerprint mengikat dua kunci** (`BLAKE2s(ed25519 ‖ noise)`) — invite yang diubah di tengah jalan selalu mengubah fingerprint, sehingga [verifikasi manual](#verifikasi-kontak) benar-benar mendeteksinya.
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

Riwayat perubahan per versi ada di **[CHANGELOG.md](CHANGELOG.md)**.

## Lisensi

Proprietary — All rights reserved. © 2026 Andika Aryansyach.
