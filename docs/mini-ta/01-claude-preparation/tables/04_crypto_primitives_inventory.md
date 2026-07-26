# Tabel 4 — Inventarisasi Primitif Kriptografi

Konsolidasi 36 entry (`CR-001`..`CR-036`, `02_CRYPTO_IMPLEMENTATION_AUDIT.md`) menjadi 7 komponen inti CORE-1..7 (`03_CRYPTO_INVENTORY_NORMALIZED.md` §4). Tabel penuh 36-entry tetap tersedia di `02_CRYPTO_IMPLEMENTATION_AUDIT.md` — tabel ini adalah ringkasan siap-pakai untuk BAB IV.

| ID | Komponen | Algoritma | Fungsi Utama | Parameter Kunci | Library (versi) | Evidence Utama | Confidence |
|---|---|---|---|---|---|---|---|
| CORE-1 | Noise_IK | Noise Protocol Framework, pola `IK` | Handshake autentikasi + key agreement 2-pesan | 2 pesan (`e,es,s,ss` / `e,ee,se`) | `snow` 0.10.0 | CR-007..011, 026-028 | MEDIUM (orkestrasi HIGH; sub-mekanisme internal LOW) |
| CORE-2 | X25519 | Curve25519 ECDH | Key agreement (DH) dalam Noise_IK | Kunci 256-bit/32 byte | `x25519-dalek` 2.0.1 | CR-007, 016, 022, 032 | HIGH (keygen), MEDIUM (DH internal `snow`) |
| CORE-3 | ChaCha20-Poly1305 | AEAD (RFC 8439) | Enkripsi vault, contact store, transport sesi (3 konteks) | Kunci 256-bit, nonce 96-bit, tag 128-bit | `chacha20poly1305` 0.10.1 | CR-001, 008, 013, 018 | HIGH (vault/contact store), MEDIUM (transport Noise) |
| CORE-4 | BLAKE2s / BLAKE2s-256 | Hash | Fingerprint identitas, KDF contacts-key, hash internal Noise | Output 256-bit/32 byte | `blake2` 0.10.6 | CR-002, 003, 009, 010 | HIGH (fingerprint/KDF), LOW (peran internal Noise) |
| CORE-5 | Argon2id | Password-based KDF (RFC 9106) | Derivasi kunci enkripsi vault dari passphrase | m=19 MiB, t=2, p=1, output 32 byte | `argon2` 0.5.3 | CR-014 | HIGH |
| CORE-6 | Ed25519 | EdDSA (RFC 8032) | Identity keypair jangka panjang (basis fingerprint) — **hanya generate/simpan** | Kunci 256-bit/32 byte, signature 64 byte (belum dipakai) | `ed25519-dalek` 2.2.0 | CR-015, 021, 031 | PARTIAL (keygen HIGH; sign/verify TIDAK ADA evidence) |
| CORE-7 | OsRng | CSPRNG OS (`rand::rngs::OsRng`) | Sumber entropi seluruh key/salt/nonce | — | `rand` 0.8.6 | CR-004, 012, 017, 023, 036 | HIGH |

## Rekapitulasi Kategori (dari 36 Entry Mentah)

| Kategori | Jumlah Entry | Contoh ID |
|---|---|---|
| Algoritma inti | 10 | CR-001, 002, 003, 004, 007, 008, 009, 013, 014, 017 |
| Key material | 2 | CR-015, 016 |
| Parameter | 1 | CR-018 |
| Mekanisme protokol | 2 | CR-010, 019 |
| Kontrol nonkriptografis | 3 | CR-020, 025, 030 |
| Helper (encoding) | 4 | CR-005, 006, 011, 028 |
| Duplikasi (call-site tambahan) | 14 | CR-012, 021-024, 026-027, 029, 031-036 |

## Catatan Kehati-hatian

- **CORE-6 (Ed25519)**: hanya berfungsi sebagai bahan fingerprint di AKSARA saat ini — TIDAK ADA pemanggilan `sign()`/`verify()` di source manapun (CB-084). Jangan menyatakan AKSARA memakai tanda tangan digital aktif.
- **CORE-1/CORE-4 sub-mekanisme internal** (hash transcript, HKDF Noise): confidence LOW, murni inferensi nama pattern `Noise_IK_25519_ChaChaPoly_BLAKE2s`.
- **CORE-3**: TIDAK misuse-resistant (nonce reuse katastropik) — dimitigasi nonce random 96-bit per operasi, bukan properti algoritma itu sendiri.

## Referensi

`02_CRYPTO_IMPLEMENTATION_AUDIT.md`, `03_CRYPTO_INVENTORY_NORMALIZED.md` (TAHAP 3/4).
