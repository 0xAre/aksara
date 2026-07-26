# Tabel 8 — Lifecycle Kunci

Reproduksi tabel ringkasan `07_KEY_LIFECYCLE.md` §1 sebagai artefak tabel siap-pakai BAB IV, ditambah tabel status rotasi/zeroization (§6-7 dokumen sumber). Tidak ada klaim baru — seluruhnya rujukan.

## 8.1 Ringkasan Material Kunci

| Kunci/Material | Algoritma | Ukuran | Umur | Dipersist? |
|---|---|---|---|---|
| Identity secret key | Ed25519 | 256 bit / 32 byte | Jangka panjang (per identitas) | Ya — dalam vault, terenkripsi |
| Identity public key | Ed25519 | 256 bit / 32 byte | Jangka panjang | Ya — plaintext (invite/fingerprint) |
| Noise secret key | X25519 | 256 bit / 32 byte | Jangka panjang (statis) | Ya — dalam vault, terenkripsi |
| Noise public key | X25519 | 256 bit / 32 byte | Jangka panjang | Ya — plaintext (invite/fingerprint) |
| Vault encryption key | Argon2id output | 256 bit / 32 byte | Sekali per `seal()`/`unseal()` | Tidak — hanya salt dipersist |
| Vault salt | Acak (`OsRng`) | 128 bit / 16 byte | Sekali per `seal()` | Ya |
| Vault nonce | Acak (`OsRng`) | 96 bit / 12 byte | Sekali per `seal()` | Ya |
| Contacts-store key | BLAKE2s (derivasi dari identity secret) | 256 bit / 32 byte | Dihitung ulang tiap panggilan | Tidak |
| Contacts-store nonce | Acak (`OsRng`) | 96 bit / 12 byte | Sekali per `save_contacts()` | Ya |
| Noise ephemeral key (`e`) | X25519 | 256 bit / 32 byte | Sekali per handshake | Tidak — internal `snow` |
| Noise transport session key | (diasumsikan ChaCha20-Poly1305) | — | Sekali per sesi | Tidak — opak di `EncryptedSession` |

## 8.2 Status Rotasi/Revokasi

| Material | Status Rotasi | Status Revokasi |
|---|---|---|
| Kunci enkripsi vault | Tidak ada kebijakan rotasi terjadwal (kunci baru hanya karena salt baru per `seal()`) | N/A |
| Identity key (Ed25519) jangka panjang | Tidak ada | Tidak ada mekanisme in-band |
| Noise key (X25519) jangka panjang | Tidak ada | Tidak ada mekanisme in-band |
| Parameter Argon2id (m,t,p) | Tidak ada versioning | N/A |
| Noise session transport key | Tidak ada — satu kunci per sesi | N/A (berakhir saat sesi drop) |

## 8.3 Status Zeroization

| Tipe/Boundary | Status |
|---|---|
| `IdentityKey`, `NoiseKey`, `KeyBundle` | `ZeroizeOnDrop` diterapkan konsisten |
| Buffer vault (plaintext, kunci turunan, hasil dekripsi) | `Zeroizing<[u8;N]>`/`Zeroizing<Vec<u8>>` diterapkan |
| `session::run_session` (parameter `local_noise_sk`/`peer_noise_pk`, buffer plaintext pesan) | **Tidak** ada wrapper zeroizing |
| `crypto::handshake` (`HandshakeSession`/`EncryptedSession`) | **Tidak** ada `Zeroize`/`ZeroizeOnDrop` eksplisit |
| `contacts::mod` (`derive_contacts_key()`, plaintext `String` hasil dekripsi) | **Tidak** ada wrapper zeroizing |
| `main.rs` (`AKSARA_PASSPHRASE` env var, passphrase stdin echo) | **Tidak** ada pembersihan; echo stdin belum diimplementasikan (`PLANNED` M4) |

## Referensi

`07_KEY_LIFECYCLE.md` §1, §6, §7 (TAHAP 6).
