# Tabel 7 — Format Paket dan Data

Seluruh layout diambil langsung dari `06_PROTOCOL_SPECIFICATION.md`/`07_KEY_LIFECYCLE.md` (TAHAP 5/6) — tidak ada format baru diperkenalkan.

## 7.1 Invite Code

| Field | Ukuran | Deskripsi |
|---|---|---|
| Ed25519 public key | 32 byte | Bagian pertama payload sebelum encoding |
| X25519 (Noise) public key | 32 byte | Bagian kedua payload sebelum encoding |
| Encoding | — | `base64url_no_pad(ed25519_pub \|\| noise_pub)`, ~86 karakter untuk 64 byte |
| Suffix onion (opsional) | variabel | `@<onion-address>`, diperlakukan string opaque tanpa validasi format |

Evidence: `src/contacts/mod.rs:56-92` (CR-005), `06_PROTOCOL_SPECIFICATION.md` §3.

## 7.2 Vault Identitas (108 byte, fixed-offset, tanpa header/magic/versi)

| Offset | Ukuran | Isi |
|---|---|---|
| 0-15 | 16 byte | Salt Argon2id (acak per `seal()`) |
| 16-27 | 12 byte | Nonce ChaCha20-Poly1305 (acak per `seal()`) |
| 28-91 | 64 byte | Ciphertext (32B Ed25519 sk \|\| 32B X25519 sk) |
| 92-107 | 16 byte | Tag Poly1305 |

Evidence: `src/identity/vault.rs:1-31` (CR-019), `07_KEY_LIFECYCLE.md` §3.1.

## 7.3 Frame Transport (Wire Format)

| Field | Ukuran | Deskripsi |
|---|---|---|
| Length prefix | 2 byte (big-endian) | Panjang payload yang mengikuti |
| Payload | ≤ `MAX_FRAME_LEN` = 65535 byte | Muatan terenkripsi Noise (1 frame = 1 pesan Noise) |

Evidence: `src/transport/frame.rs:16` (`MAX_FRAME_LEN`), `06_PROTOCOL_SPECIFICATION.md` §4.4.

## 7.4 Payload Plaintext Sesi (Sebelum Enkripsi)

| Tag (1 byte) | Nilai | Body |
|---|---|---|
| `TYPE_TEXT` | `0x00` | Byte UTF-8 teks pesan |
| `TYPE_BLUR` | `0x01` | 1 byte tambahan: `on as u8` |
| `TYPE_PING` | `0x02` | Tidak ada body (payload total 1 byte, keepalive) |

Overhead AEAD: +16 byte tag per pesan terenkripsi (asumsi ChaCha20-Poly1305 via `snow`, MEDIUM confidence — tidak disebut literal di `session/mod.rs`).

Evidence: `src/session/mod.rs:36-41,169-182`, `06_PROTOCOL_SPECIFICATION.md` §6.3-6.4.

## 7.5 Contact Store (File Kontak Terenkripsi)

| Field | Ukuran | Isi |
|---|---|---|
| Nonce | 12 byte | Nonce ChaCha20-Poly1305 (acak per `save_contacts()`) |
| Ciphertext + tag | variabel | Data kontak (nickname, fingerprint, alamat) terenkripsi, tanpa magic bytes header |

Evidence: `src/contacts/mod.rs:94-100,170-198` (CR-001), `07_KEY_LIFECYCLE.md` §4.

## Referensi

`06_PROTOCOL_SPECIFICATION.md`, `07_KEY_LIFECYCLE.md` (TAHAP 5-6).
