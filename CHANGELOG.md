# Changelog

Format mengikuti [Keep a Changelog](https://keepachangelog.com/id/1.1.0/).
Versi mengikuti [SemVer](https://semver.org/lang/id/) — selama masih `0.x`,
perubahan yang memutus kompatibilitas menaikkan angka minor.

## [0.2.1] — 2026-07-26

### Diperbaiki

- **Sesi bisa putus sendiri di tengah percakapan.** Pembacaan frame ditaruh
  langsung sebagai cabang `tokio::select!`, padahal operasinya membaca panjang
  dan isi dalam dua tahap. Ketika cabang lain menang tepat saat sebuah frame
  baru masuk separuh, tahap yang sudah berjalan dibatalkan dan byte yang
  terlanjur terbaca hilang — frame berikutnya jadi salah tafsir, dekripsi
  gagal, dan room tertutup tanpa sebab yang terlihat.

  Peluangnya paling besar pada frame yang datang terpotong-potong, jadi jalur
  Tor dan pesan panjang paling terdampak. Cacat ini sebenarnya sudah ada sejak
  v0.1.0 (terpicu bila kamu mengirim pesan tepat saat pesan masuk sedang
  separuh), hanya jarang; keepalive di v0.2.0 membuatnya sering.

  Pembacaan kini berjalan di jalur sendiri sehingga tidak pernah dibatalkan di
  tengah. **Semua pengguna v0.2.0 dianjurkan update.** Tidak ada perubahan
  protokol — v0.2.0 dan v0.2.1 tetap bisa saling terhubung.

## [0.2.0] — 2026-07-25

### ⚠ Wajib dibaca sebelum update

**Kedua pihak harus update bersamaan.** Fingerprint identitas berubah di rilis
ini, dan tidak ada jalur kompatibilitas mundur. Peer v0.1.0 dan v0.2.0 **tidak
akan saling menemukan** di LAN, dan bila dipaksa lewat `--dial`/`--listen`
keduanya bisa mengambil peran yang sama sehingga handshake tidak pernah jadi.
Gejalanya hanya "peer tidak ketemu" — tidak ada pesan error yang menjelaskan.

Invite code lama juga perlu ditukar ulang: fingerprint yang tercetak dari
`aksara id` sekarang berbeda, jadi hasil verifikasi lama tidak lagi cocok.

### Keamanan

- **Fingerprint kini mengikat kedua kunci**: `BLAKE2s(ed25519_pub || noise_pub)`,
  sebelumnya hanya `hex(ed25519_pub)`. Invite code tidak ditandatangani, jadi
  dengan fingerprint lama seseorang yang memegang invite orang lain bisa
  menyusunnya ulang dengan kunci Noise miliknya sendiri: fingerprint yang
  tampil tetap milik korban dan lolos pencocokan lewat telepon, padahal
  handshake berjalan ke penyusup. Mengganti kunci Noise kini mengubah
  fingerprint, jadi verifikasi out-of-band kembali bermakna.
- Panel kontak di TUI ikut diperbaiki — panel itu menghitung fingerprint
  sendiri dari `ed25519_pub` alih-alih memakai fungsi bersama, padahal justru
  di layar itulah user melakukan pencocokan.

### Ditambahkan

- Keepalive tiap 30 detik pada sesi aktif. Sebelumnya koneksi yang sudah mati
  baru ketahuan saat user mengetik — umum di Tor, karena circuit putus tanpa
  menutup koneksi secara bersih.
- Jam lokal pada tiap baris chat, dirender rata kanan. Waktu diambil dari jam
  penerima dan tidak pernah dikirim lewat kabel, jadi tidak ada metadata baru
  yang bocor ke lawan bicara.
- Workflow CI: `cargo test` + `cargo clippy -D warnings` di setiap push dan PR.
  Sebelumnya hanya ada workflow rilis yang berjalan saat tag.

### Diperbaiki

- Pesan yang melebihi batas Noise (65535 byte) tidak lagi menutup seluruh room.
  Kini dilaporkan sebagai peringatan non-fatal dan sesi berjalan terus.

### Dihapus

- `Error::RoleNegotiationFailed` dan `TorContext::accept()` — keduanya tidak
  pernah terpakai.

## [0.1.0] — 2026-07-24

Rilis pertama. Chat P2P terminal tanpa server perantara.

- Handshake Noise_IK (`Noise_IK_25519_ChaChaPoly_BLAKE2s`) dengan mutual
  authentication dan forward secrecy.
- Transport LAN via mDNS discovery, dan Tor onion service via arti-client,
  dengan fallback otomatis LAN-first → Tor.
- Vault identitas terenkripsi Argon2id + ChaCha20-Poly1305, tanpa magic bytes.
- Contact store terenkripsi; invite code tanpa prefix yang mengidentifikasi.
- TUI ratatui: Mode Light tersinkron, cari pesan, reply, scroll wrap-aware.
- Binary siap-pakai untuk Windows, Linux, dan macOS.

[0.2.1]: https://github.com/0xAre/aksara/releases/tag/v0.2.1
[0.2.0]: https://github.com/0xAre/aksara/releases/tag/v0.2.0
[0.1.0]: https://github.com/0xAre/aksara/releases/tag/v0.1.0
