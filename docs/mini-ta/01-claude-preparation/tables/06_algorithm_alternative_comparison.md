# Tabel 6 — Perbandingan Alternatif Algoritma

Sintesis dari `05_CRYPTO_ALTERNATIVE_COMPARISON.md` (perbandingan penuh multi-kriteria per fungsi tersedia di dokumen sumber, 10 kriteria: security level, standardization, library maturity, misuse resistance, interoperability, key/nonce requirements, ciphertext expansion, implementation complexity, ecosystem support, resource consumption).

| Fungsi | Dipakai AKSARA | Alternatif 1 | Alternatif 2 | Alasan Utama Penolakan Alternatif |
|---|---|---|---|---|
| Kerangka handshake/protokol | Noise_IK (`snow`) | TLS 1.3 (`rfc8446`) | Signal X3DH + Double Ratchet (`x3dh2016`) | TLS 1.3 butuh PKI/CA yang tidak natural untuk identitas self-sovereign P2P; X3DH didesain untuk messaging asinkron via broker server, tidak cocok koneksi P2P langsung sinkron AKSARA |
| Key agreement | X25519 | NIST P-256 (`sp800-186`/`fips186-5`) | Curve448/X448 (`rfc7748`) | P-256: riwayat kerawanan implementasi non-constant-time, opasitas asal-usul parameter kurva; Curve448: margin keamanan 224-bit tidak dibutuhkan untuk skala ancaman aplikasi chat personal |
| AEAD | ChaCha20-Poly1305 | AES-256-GCM (`sp800-38d`) | AES-256-GCM-SIV (`rfc8452`) | AES-GCM: risiko implementasi non-constant-time lebih tinggi tanpa AES-NI seragam lintas-platform; AES-GCM-SIV: kompleksitas 2-pass tambahan, adopsi ekosistem lebih rendah |
| Fungsi hash | BLAKE2s | SHA-256 (`fips180-4`) | SHA3-256 (`fips202`) | SHA-256: tidak memberi manfaat tambahan signifikan sambil menambah 1 dependency hash baru; SHA3-256: performa software CPU umum secara historis lebih lambat tanpa akselerasi Keccak khusus |
| Password-based KDF | Argon2id | scrypt (`rfc7914`) | PBKDF2 (`rfc8018`) | scrypt: Argon2id adalah evolusi lebih baru dengan analisis kriptanalisis lebih matang; PBKDF2: BUKAN memory-hard, jauh lebih rentan hardware paralel ASIC/GPU |
| Identitas kriptografis | Ed25519 | ECDSA P-256 (`fips186-5`) | RSA-2048/RSA-PSS | ECDSA: risiko implementasi nonce lebih tinggi tanpa RFC 6979 tambahan; RSA: ukuran kunci/signature jauh lebih besar, level keamanan efektif lebih rendah pada ukuran setara (~112-bit) |
| Sumber entropi (CSPRNG) | OsRng | ChaCha20Rng (`rand_chacha`) | ThreadRng | Keduanya unggul pada volume RNG tinggi (server) — tidak relevan untuk AKSARA (volume RNG rendah, aplikasi chat personal single-pengguna) |

## Catatan Metodologis

Penolakan alternatif **bukan berarti "tidak aman"** — seluruhnya pilihan valid dengan trade-off berbeda; penolakan didasarkan kesesuaian kontekstual dengan arsitektur AKSARA (binary kecil lintas-platform tanpa akselerasi hardware seragam, model P2P serverless tanpa PKI, skala pemakaian personal).

## Referensi

`05_CRYPTO_ALTERNATIVE_COMPARISON.md` (TAHAP 4) — tabel perbandingan penuh 10-kriteria per fungsi tersedia di dokumen sumber, tidak diulang di sini.
