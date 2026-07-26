# Tabel 1 — Kebutuhan Fungsional

Diturunkan dari kapabilitas yang **sudah terimplementasi dan terverifikasi** pada `01_CODEBASE_AUDIT.md` dan `06_PROTOCOL_SPECIFICATION.md` — bukan daftar kebutuhan yang diusulkan baru. Setiap baris merujuk evidence source-level, bukan dokumentasi/proposal.

| ID | Kebutuhan Fungsional | Deskripsi | Evidence | Status |
|---|---|---|---|---|
| FR-01 | Pembangkitan identitas kriptografis | Sistem dapat membangkitkan pasangan kunci identitas baru (Ed25519 + X25519) memakai CSPRNG OS | `src/identity/keypair.rs:18-22,51-56` (CR-015/016), `02_CRYPTO_IMPLEMENTATION_AUDIT.md` | IMPLEMENTED |
| FR-02 | Penyimpanan identitas terenkripsi (vault) | Sistem menyimpan key material identitas dalam vault 108-byte terenkripsi passphrase (Argon2id + ChaCha20-Poly1305) | `src/identity/vault.rs:58-93` (CR-013/014), `07_KEY_LIFECYCLE.md` §3 | IMPLEMENTED |
| FR-03 | Pembukaan vault dan penolakan passphrase salah | Sistem dapat membuka vault dengan passphrase benar dan menolak (fail-closed, pesan generik) passphrase salah/vault korup | `src/identity/vault.rs:95-128` (CR-013/014), `07_KEY_LIFECYCLE.md` §3.4 | IMPLEMENTED |
| FR-04 | Pembuatan dan penguraian invite code | Sistem dapat membuat invite code (base64url dari 2 public key) dan menguraikannya kembali, opsional menyertakan alamat onion | `src/contacts/mod.rs:56-92` (CR-005), `06_PROTOCOL_SPECIFICATION.md` §3 | IMPLEMENTED |
| FR-05 | Fingerprint identitas yang mengikat dua kunci publik | Sistem menghasilkan fingerprint (BLAKE2s256, hex 64 karakter) yang mengikat public key Ed25519 dan X25519 sekaligus | `src/contacts/mod.rs:39-54` (CR-002), `07_KEY_LIFECYCLE.md` §5.1 | IMPLEMENTED |
| FR-06 | Discovery peer di jaringan lokal | Sistem dapat mengiklankan dan menemukan peer lain di LAN yang sama via mDNS (`_aksara._tcp.local.`) | `src/transport/lan.rs:1-21` (CR-029), `06_PROTOCOL_SPECIFICATION.md` §4.2 | IMPLEMENTED |
| FR-07 | Koneksi P2P via Tor onion service (fallback) | Sistem dapat membentuk koneksi P2P via Tor onion service v3 bila LAN gagal/tidak tersedia | `src/transport/tor.rs:1-122`, `06_PROTOCOL_SPECIFICATION.md` §4.3 | IMPLEMENTED |
| FR-08 | Handshake Noise_IK dua-pesan | Sistem melakukan handshake Noise_IK (2 pesan) untuk autentikasi identitas dan pembentukan kunci sesi | `src/crypto/handshake.rs:109-129` (CR-007..011), `06_PROTOCOL_SPECIFICATION.md` §5 | IMPLEMENTED |
| FR-09 | Enkripsi/dekripsi pesan sesi | Sistem mengenkripsi/mendekripsi pesan chat, sinyal blur, dan keepalive pada sesi transport aktif | `src/session/mod.rs:164-279` (CR-026), `06_PROTOCOL_SPECIFICATION.md` §6 | IMPLEMENTED |
| FR-10 | Penyimpanan daftar kontak terenkripsi | Sistem menyimpan nickname, fingerprint, dan alamat kontak dalam file terenkripsi ChaCha20-Poly1305 | `src/contacts/mod.rs:170-198` (CR-001), `07_KEY_LIFECYCLE.md` §4 | IMPLEMENTED |
| FR-11 | Penolakan koneksi peer tak dikenal (fail-closed) | Sistem menolak koneksi bila static key peer yang sudah dikenal tidak cocok dengan yang diharapkan | `src/session/mod.rs:145-151`, `06_PROTOCOL_SPECIFICATION.md` §5.2 | IMPLEMENTED |
| FR-12 | Antarmuka terminal (TUI) untuk interaksi pengguna | Sistem menyediakan antarmuka TUI (ratatui/crossterm) untuk manajemen identitas, kontak, dan sesi chat | `src/tui/` (evidence `tui.json`), `01_CODEBASE_AUDIT.md` §5 | IMPLEMENTED |

## Referensi

Seluruh evidence merujuk `01_CODEBASE_AUDIT.md`, `02_CRYPTO_IMPLEMENTATION_AUDIT.md`, `06_PROTOCOL_SPECIFICATION.md`, `07_KEY_LIFECYCLE.md` (TAHAP 2/5/6) — tidak ada klaim baru yang diperkenalkan pada tabel ini.
