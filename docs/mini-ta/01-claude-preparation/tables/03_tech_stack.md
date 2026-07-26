# Tabel 3 — Stack Teknologi

Versi ground-truth diambil langsung dari `Cargo.lock`/`Cargo.toml`, dicatat pertama kali `PROGRESS.md`/`PROJECT_MEMORY.md` (TAHAP 1-3), tidak diverifikasi ulang pada sesi ini.

| Kategori | Komponen | Versi | Fungsi dalam AKSARA |
|---|---|---|---|
| Bahasa | Rust | edition 2021, `rust-version` 1.89 | Bahasa implementasi utama |
| Runtime async | tokio | 1.52.3 | Runtime asinkron untuk I/O jaringan, task, channel |
| TUI | ratatui | 0.29.0 | Rendering antarmuka terminal |
| TUI | crossterm | 0.29.0 | Backend terminal cross-platform (input/output) |
| Discovery LAN | mdns-sd | 0.20.0 | Implementasi mDNS/DNS-SD untuk discovery peer LAN |
| Transport anonim | arti-client / tor-hsservice / tor-cell | 0.43.0 | Klien Tor dan onion service v3 (Rust-native Tor) |
| TLS backend (Tor) | rustls / ring | 0.23.40 / 0.17.14 | CryptoProvider TLS untuk `arti-client` |
| Handshake kripto | snow | 0.10.0 | Implementasi Noise Protocol Framework (pola `Noise_IK_25519_ChaChaPoly_BLAKE2s`) |
| Key agreement | x25519-dalek | 2.0.1 | X25519 (Curve25519 ECDH) — Noise static/ephemeral key |
| Identity signing lib | ed25519-dalek | 2.2.0 | Ed25519 — identity keypair (generate/simpan, belum dipakai sign/verify aktif) |
| AEAD | chacha20poly1305 (+ chacha20, poly1305, aead) | 0.10.1 (0.10.0 / 0.8.0 / 0.5.2) | Enkripsi vault, contact store, transport sesi |
| KDF password-based | argon2 | 0.5.3 | Derivasi kunci vault dari passphrase |
| Hash | blake2 | 0.10.6 | Fingerprint identitas, KDF contacts-key, hash internal Noise |
| CSPRNG | rand (`OsRng`) | 0.8.6 | Sumber entropi seluruh key/salt/nonce generation |
| Zeroization | zeroize | 1.9.0 | Pembersihan key material dari memori saat drop |
| Build target | Windows, Linux, macOS Apple Silicon | — | Platform distribusi binary (README) |

## Referensi

`PROJECT_MEMORY.md` §Versi Ground Truth, `Cargo.lock` (TAHAP 1-3) — tidak ada dependency baru ditambahkan pada sesi ini.
