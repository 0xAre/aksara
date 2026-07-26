# Tabel 5 — Justifikasi Algoritma

Ringkasan siap-pakai dari `04_CRYPTOGRAPHIC_JUSTIFICATION.md` (15 poin penuh per komponen tersedia di dokumen sumber, tidak diulang di sini). Kolom "Alasan Pemilihan" dan "Keterbatasan Utama" adalah kompresi poin 3 dan 13 masing-masing komponen.

| Komponen | Masalah yang Diselesaikan | Alasan Pemilihan (ringkas) | Standar/Paper Utama | Keterbatasan Utama |
|---|---|---|---|---|
| CORE-1 Noise_IK | Kanal terenkripsi + saling terautentikasi P2P tanpa PKI/CA | Pola `IK` cocok model "kontak sudah bertukar fingerprint out-of-band"; 1-RTT ringan; hindari kompleksitas X.509 | `noise2018` | Sub-mekanisme internal (hash/HKDF) confidence LOW; `snow` belum diaudit formal |
| CORE-2 X25519 | Key agreement tanpa pra-share rahasia | Performa tinggi, permukaan kesalahan implementasi kecil (twist-secure), default token `25519` pada pola Noise dipilih | `rfc7748`, `bernstein2006curve25519` | Operasi DH internal `snow`, tidak dapat diverifikasi langsung dari source aplikasi |
| CORE-3 ChaCha20-Poly1305 | Enkripsi terautentikasi (confidentiality+integrity) at-rest dan in-transit | Software-friendly tanpa AES-NI (binary lintas-platform tak seragam akselerasi AES), token AEAD resmi Noise `ChaChaPoly` | `rfc8439`, `bernstein2008chacha`, `bernstein2005poly1305` | TIDAK misuse-resistant — nonce reuse pada kunci sama katastropik |
| CORE-4 BLAKE2s | Hash cepat untuk fingerprint, KDF ad hoc, hash internal Noise | Konsistensi dengan hash default pola Noise `_BLAKE2s`; optimal 32-bit/binary kecil lintas-platform | `rfc7693`, `aumasson2013blake2` | Pemakaian sebagai KDF (CR-003) bukan HKDF standar; peran internal Noise confidence LOW |
| CORE-5 Argon2id | KDF memory-hard untuk passphrase manusia berentropi rendah | Pemenang Password Hashing Competition 2015, direkomendasikan RFC 9106 WAJIB didukung; cocok vault lokal single-pengguna | `rfc9106`, `biryukov2016argon2` | Klaim timing "~100ms" belum diverifikasi benchmark (`NEEDS_EXPERIMENT`, lihat EXP-05 `12_TEST_PLAN.md`) |
| CORE-6 Ed25519 | Identitas jangka-panjang ringkas, dapat diverifikasi manusia | Signature deterministic (jika diaktifkan), ukuran kunci/signature ringkas untuk fingerprint/invite compact | `rfc8032`, `bernstein2012ed25519`, `fips186-5` | TIDAK ADA bukti pemakaian aktif `sign()`/`verify()` — hanya generate/simpan |
| CORE-7 OsRng | Sumber entropi tak terprediksi untuk seluruh kebutuhan acak | Sumber paling langsung/tepercaya lintas-platform Rust, tanpa CSPRNG custom berisiko salah desain | `sp800-90a` (konteks kriteria) | Bergantung penuh kualitas CSPRNG OS, di luar kendali audit AKSARA |

## Referensi

`04_CRYPTOGRAPHIC_JUSTIFICATION.md` (TAHAP 4) — detail 15 poin penuh per komponen (properti keamanan, dampak paket/komputasi/memori, trade-off, asumsi penggunaan aman, risiko implementasi) tidak diulang di tabel ringkas ini.
