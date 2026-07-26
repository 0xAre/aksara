# Reference Matrix — AKSARA Mini-TA

Kolom "Bab" adalah proyeksi provisional untuk TAHAP 15 (content pack per BAB) yang BELUM dikerjakan sesi ini — bukan penempatan final. Kolom "Algoritma" merujuk ke komponen inti `CORE-1`..`CORE-7` dari `03_CRYPTO_INVENTORY_NORMALIZED.md`. Kolom "Klaim yang Didukung" merujuk ke ID `CR-xxx` (audit kripto, `02_CRYPTO_IMPLEMENTATION_AUDIT.md`) yang relevan.

| Citekey | Referensi | Jenis | Klaim yang Didukung | Algoritma | Bab | Kualitas |
|---------|-----------|-------|----------------------|-----------|-----|----------|
| `noise2018` | Perrin, "The Noise Protocol Framework", Rev. 34 (2018) | Spesifikasi resmi (primer) | CR-007, CR-008, CR-009, CR-010, CR-011, CR-027 | CORE-1 (Noise_IK) | BAB II | HIGH |
| `rfc7748` | Langley, Hamburg, Turner, RFC 7748 (2016) | Standar IETF | CR-007, CR-016, CR-022, CR-032 | CORE-2 (X25519) | BAB II | HIGH |
| `bernstein2006curve25519` | Bernstein, "Curve25519: New Diffie-Hellman Speed Records", PKC 2006 | Paper primer | CR-007, CR-016 | CORE-2 (X25519) | BAB II | HIGH |
| `rfc8439` | Nir, Langley, RFC 8439 (2018) | Standar IETF | CR-001, CR-008, CR-013, CR-018, CR-024, CR-026, CR-033 | CORE-3 (ChaCha20-Poly1305) | BAB II | HIGH |
| `bernstein2008chacha` | Bernstein, "ChaCha, a variant of Salsa20" (2008) | Technical report primer (non-peer-review) | CR-001, CR-008, CR-013 | CORE-3 (ChaCha20-Poly1305) | BAB II | MEDIUM-HIGH |
| `bernstein2005poly1305` | Bernstein, "The Poly1305-AES Message-Authentication Code", FSE 2005 | Paper primer (peer-reviewed) | CR-001, CR-008, CR-013 | CORE-3 (ChaCha20-Poly1305) | BAB II | HIGH |
| `rfc9106` | Biryukov, Dinu, Khovratovich, Josefsson, RFC 9106 (2021) | Standar IETF | CR-014, CR-024, CR-033 | CORE-5 (Argon2id) | BAB II | HIGH |
| `biryukov2016argon2` | Biryukov, Dinu, Khovratovich, EuroS&P 2016 | Paper primer (peer-reviewed) | CR-014 | CORE-5 (Argon2id) | BAB II | HIGH |
| `rfc7693` | Saarinen, Aumasson, RFC 7693 (2015) | Standar IETF | CR-002, CR-003, CR-009, CR-010, CR-029, CR-034, CR-035 | CORE-4 (BLAKE2s) | BAB II | HIGH |
| `aumasson2013blake2` | Aumasson, Neves, Wilcox-O'Hearn, Winnerlein, ACNS 2013 | Paper primer (peer-reviewed) | CR-002, CR-003 | CORE-4 (BLAKE2s) | BAB II | HIGH |
| `rfc8032` | Josefsson, Liusvaara, RFC 8032 (2017) | Standar IETF | CR-015, CR-021, CR-031 | CORE-6 (Ed25519) | BAB II | HIGH |
| `bernstein2012ed25519` | Bernstein, Duif, Lange, Schwabe, Yang, J. Cryptogr. Eng. 2012 | Paper primer (peer-reviewed) | CR-015, CR-021, CR-031 | CORE-6 (Ed25519) | BAB II | HIGH |
| `fips186-5` | NIST, FIPS 186-5 (2023) | Standar resmi (NIST) | CR-015 (konteks standardisasi Ed25519 oleh NIST) | CORE-6 (Ed25519) | BAB II | HIGH |
| `sp800-186` | Chen, Moody, Regenscheid, Robinson, Randall, NIST SP 800-186 (2023) | Standar resmi (NIST) | CR-007, CR-015 (parameter kurva Ed25519/X25519 versi NIST) | CORE-2, CORE-6 | BAB II | HIGH |
| `sp800-90a` | NIST, SP 800-90A Rev.1 (2015) | Standar resmi (NIST) | CR-004, CR-012, CR-017, CR-023, CR-036 | CORE-7 (OsRng) | BAB II | HIGH |
| `randcrate` | rust-random, `rand::rngs::OsRng` docs | Dokumentasi library | CR-004, CR-012, CR-017, CR-023, CR-036 | CORE-7 (OsRng) | BAB III | MEDIUM |
| `sp800-38d` | Dworkin, NIST SP 800-38D (2007) | Standar resmi (NIST) | — (pembanding AES-GCM di `05_CRYPTO_ALTERNATIVE_COMPARISON.md`) | CORE-3 pembanding | BAB II/V | HIGH |
| `rfc8452` | Gueron, Langley, Lindell, RFC 8452 (2019) | Standar IETF | — (pembanding AES-GCM-SIV) | CORE-3 pembanding | BAB II/V | HIGH |
| `rfc7914` | Percival, Josefsson, RFC 7914 (2016) | Standar IETF | — (pembanding scrypt) | CORE-5 pembanding | BAB II/V | HIGH |
| `percival2009scrypt` | Percival, BSDCan 2009 | Paper/design document primer | — (pembanding scrypt) | CORE-5 pembanding | BAB II/V | HIGH |
| `rfc8018` | Moriarty, Kaliski, Rusch, RFC 8018 (2017) | Standar IETF | — (pembanding PBKDF2) | CORE-5 pembanding | BAB II/V | HIGH |
| `fips180-4` | NIST, FIPS 180-4 (2015) | Standar resmi (NIST) | — (pembanding SHA-256) | CORE-4 pembanding | BAB II/V | HIGH |
| `fips202` | NIST, FIPS 202 (2015) | Standar resmi (NIST) | — (pembanding SHA3-256) | CORE-4 pembanding | BAB II/V | HIGH |
| `rfc8446` | Rescorla, RFC 8446 (2018) | Standar IETF | — (pembanding kerangka TLS 1.3) | CORE-1 pembanding | BAB II/V | HIGH |
| `x3dh2016` | Marlinspike, Perrin, X3DH (2016) | Spesifikasi resmi (Signal) | — (pembanding kerangka X3DH/Signal) | CORE-1 pembanding | BAB II/V | HIGH |
| `snowcrate` | McGinty et al., crate `snow` v0.10.0 | Dokumentasi library | CR-007, CR-008, CR-009, CR-010, CR-011, CR-025, CR-026, CR-027 | CORE-1 (Noise_IK) | BAB III | MEDIUM |
| `chacha20poly1305crate` | RustCrypto, crate `chacha20poly1305` v0.10.1 | Dokumentasi library | CR-001, CR-008, CR-013, CR-018 | CORE-3 (ChaCha20-Poly1305) | BAB III | MEDIUM |
| `ed25519dalekcrate` | dalek-cryptography, crate `ed25519-dalek` v2.2.0 | Dokumentasi library | CR-015, CR-021, CR-031 | CORE-6 (Ed25519) | BAB III | MEDIUM |
| `x25519dalekcrate` | dalek-cryptography, crate `x25519-dalek` v2.0.1 | Dokumentasi library | CR-016, CR-022, CR-032 | CORE-2 (X25519) | BAB III | MEDIUM |
| `argon2crate` | RustCrypto, crate `argon2` v0.5.3 | Dokumentasi library | CR-014 | CORE-5 (Argon2id) | BAB III | MEDIUM |
| `blake2crate` | RustCrypto, crate `blake2` v0.10.6 | Dokumentasi library | CR-002, CR-003 | CORE-4 (BLAKE2s) | BAB III | MEDIUM |

## Rekap Kualitas Sumber

| Kualitas | Jumlah | Keterangan |
|----------|--------|------------|
| HIGH | 24 | Standar resmi (RFC/FIPS/NIST/spesifikasi protokol) dan paper primer peer-reviewed |
| MEDIUM-HIGH | 1 | `bernstein2008chacha` — technical report asli penulis algoritma, tapi tidak melalui proses peer-review formal (baru distandardisasi belakangan lewat RFC 8439) |
| MEDIUM | 6 | Dokumentasi resmi library/crate — otoritatif untuk klaim implementasi, bukan untuk klaim keamanan teoretis |
| **Total** | **31** | Melebihi target 15–25 karena TAHAP 9 digabung ke TAHAP 4 dan mencakup referensi pembanding untuk `05_CRYPTO_ALTERNATIVE_COMPARISON.md` (bukan hanya justifikasi primitif terpakai) |

Sumber primer/standar resmi (bukan dokumentasi library): **25 dari 31** — jauh di atas syarat minimum 5.
