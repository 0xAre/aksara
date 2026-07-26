# 05 — Perbandingan Alternatif Kriptografi AKSARA

Untuk setiap fungsi utama, AKSARA (kolom pertama tiap tabel) dibandingkan dengan maksimal dua alternatif relevan, dinilai di banyak kriteria (security level, standardization, library maturity, misuse resistance, interoperability, key/nonce requirements, ciphertext expansion, implementation complexity, ecosystem support, resource consumption) — bukan hanya kecepatan, sesuai instruksi TAHAP 4. Sumber merujuk citekey di `references/REFERENCES.bib`; evidence implementasi lokal merujuk ID `CR-xxx` di `02_CRYPTO_IMPLEMENTATION_AUDIT.md`.

---

## 1. Kerangka Handshake/Protokol: Noise_IK vs. TLS 1.3 vs. Signal X3DH + Double Ratchet

| Kriteria | **Noise_IK** (dipakai AKSARA) | TLS 1.3 (`rfc8446`) | Signal X3DH + Double Ratchet (`x3dh2016`) |
|----------|-------------------------------|----------------------|---------------------------------------------|
| Security level | Setara ~128-bit (mengikuti primitif 25519/ChaChaPoly) | Setara ~128-bit (cipher suite modern) | Setara ~128-bit (X25519 + AES/ChaCha) |
| Standardisasi | Spesifikasi resmi non-IETF, status "official/unstable" (`noise2018`) | RFC IETF penuh, standar internet paling luas dipakai (`rfc8446`) | Spesifikasi resmi Signal, bukan standar IETF/ISO (`x3dh2016`) |
| Maturitas library (Rust) | `snow` — **belum diaudit formal** (self-declared) | `rustls` — sudah diaudit, dipakai luas (termasuk oleh `arti-client` Tor AKSARA sendiri, CR-020) | Tidak ada crate X3DH resmi tunggal yang matang setara `rustls`/`snow`; umumnya diimplementasikan custom per aplikasi |
| Model kepercayaan | Tanpa PKI — static key diverifikasi manual (fingerprint out-of-band) | Berbasis PKI/CA (sertifikat X.509) atau pinning manual | Berbasis server broker (prekey bundle publikasi/distribusi terpusat) |
| Interoperabilitas | Rendah di luar ekosistem yang secara eksplisit mengadopsi Noise (WireGuard, dll.) | Sangat tinggi — protokol web/internet universal | Rendah — spesifik ekosistem Signal-like |
| Kompleksitas implementasi | Rendah-menengah — 2 pesan, tanpa negosiasi cipher suite | Tinggi — negosiasi cipher suite, rantai sertifikat, extension | Tinggi — perlu manajemen prekey bundle, ratcheting state per pesan |
| Overhead handshake | 2 pesan (1-RTT) | Minimal 1-RTT (TLS 1.3), tapi butuh round-trip tambahan untuk validasi sertifikat/OCSP pada praktiknya | Perlu fetch prekey bundle dari server sebelum handshake pertama (tambahan round-trip ke server) |
| Kecocokan skenario AKSARA | **Cocok** — P2P langsung, identitas self-sovereign, tanpa server | Tidak cocok tanpa CA infra tambahan | Tidak cocok — didesain untuk messaging asinkron store-and-forward via server broker, bukan koneksi P2P langsung |

**Sintesis**: AKSARA mempertahankan Noise_IK karena satu-satunya dari ketiganya yang secara native cocok dengan model P2P serverless tanpa PKI dan tanpa broker server. TLS 1.3 lebih matang dan teraudit tapi memaksakan model trust berbasis sertifikat yang bertentangan dengan desain self-sovereign identity AKSARA. X3DH dioptimalkan untuk skenario asinkron (kontak offline menerima prekey bundle dari server) yang tidak relevan untuk AKSARA yang mensyaratkan kedua pihak online untuk terhubung langsung (evidence: tidak ada mekanisme store-and-forward di source yang diaudit). Risiko yang HARUS diterima dari pilihan ini: `snow` belum diaudit formal, berbeda dengan `rustls` yang sudah.

---

## 2. Key Agreement: X25519 vs. NIST P-256 vs. Curve448/X448

| Kriteria | **X25519** (dipakai AKSARA, CR-007/CR-016) | NIST P-256 (`sp800-186`, `fips186-5`) | Curve448/X448 (`rfc7748`) |
|----------|----------------------------------------------|------------------------------------------|------------------------------|
| Security level | ~128-bit | ~128-bit | ~224-bit (margin lebih tinggi) |
| Standardisasi | RFC 7748 (IETF) + kini juga diadopsi NIST SP 800-186 (2023) | FIPS 186-5 / SP 800-186 (NIST, sejak generasi awal) | RFC 7748 (IETF), belum diadopsi eksplisit di FIPS 186-5/SP 800-186 |
| Maturitas library (Rust) | `x25519-dalek` — matang, dipakai luas (`x25519dalekcrate`) | Tersedia (`p256` crate, RustCrypto) — matang tapi tidak dipakai AKSARA | Tersedia (`ed448-goldilocks` dll.) — kurang matang/kurang populer dibanding X25519 |
| Misuse resistance | Desain "twist-secure" — validasi titik eksplisit tidak wajib | Butuh validasi titik/subgroup check manual — riwayat bug implementasi (mis. kesalahan validasi kurva pada beberapa library lama) | Sama seperti X25519 (desain Montgomery serupa) — twist-secure |
| Interoperabilitas | Tinggi di ekosistem modern (TLS 1.3, WireGuard, Signal, SSH) | Sangat tinggi (legacy web PKI, banyak sistem pemerintah) | Rendah — jarang dipakai di luar niche high-security |
| Ukuran kunci | 32 byte | 32 byte (uncompressed 65 byte tanpa compression) | 56 byte |
| Kompleksitas implementasi constant-time | Rendah — desain aritmetika kurva secara alami mendukung constant-time sederhana | Menengah-tinggi — historis banyak implementasi non-constant-time bermasalah | Rendah, serupa X25519 tapi field aritmetika lebih besar |
| Konsumsi resource | Cepat (~puluhan mikrodetik/operasi) | Sebanding tanpa akselerasi hardware, kadang lebih lambat pada implementasi non-optimized | Lebih lambat dari X25519 (field 448-bit lebih besar) untuk margin keamanan tambahan yang tidak dibutuhkan |

**Sintesis**: X25519 dipertahankan karena kombinasi performa tinggi, kesederhanaan implementasi constant-time, dan kesesuaian langsung dengan token pola Noise `25519` yang dipakai `snow`. P-256 ditolak karena riwayat kerawanan implementasi non-constant-time dan opasitas asal-usul parameter kurva NIST generasi awal (kekhawatiran yang mendorong komunitas kriptografi mengadopsi Curve25519 secara luas). Curve448 ditolak murni atas dasar proporsionalitas: margin keamanan 224-bit tidak dibutuhkan untuk ancaman realistis terhadap aplikasi chat personal, dengan biaya performa dan ukuran kunci lebih besar tanpa manfaat sepadan pada skala AKSARA.

---

## 3. AEAD: ChaCha20-Poly1305 vs. AES-256-GCM vs. AES-256-GCM-SIV

| Kriteria | **ChaCha20-Poly1305** (dipakai AKSARA, CR-001/008/013) | AES-256-GCM (`sp800-38d`) | AES-256-GCM-SIV (`rfc8452`) |
|----------|------------------------------------------------------------|-------------------------------|----------------------------------|
| Security level | ~256-bit key, ~128-bit tag | ~256-bit key, ~128-bit tag | ~256-bit key, ~128-bit tag |
| Standardisasi | RFC 8439 (IETF) | NIST SP 800-38D (2007), FIPS-approved | RFC 8452 (IETF, CFRG) |
| Maturitas library (Rust) | `chacha20poly1305` (RustCrypto) — matang, sudah dipakai AKSARA | `aes-gcm` (RustCrypto) — sama-sama matang | `aes-gcm-siv` (RustCrypto) — tersedia tapi adopsi lebih rendah |
| Misuse resistance (nonce reuse) | **Rendah** — nonce reuse pada kunci sama membocorkan XOR plaintext + membuka forgery | **Rendah** — sama seperti ChaCha20-Poly1305, katastropik pada nonce reuse | **Tinggi** — didesain eksplisit agar nonce reuse hanya membocorkan kesamaan pesan, tidak katastropik |
| Interoperabilitas | Tinggi (TLS 1.3, Noise, SSH, WireGuard) | Sangat tinggi (TLS legacy & 1.3, IPsec, hampir semua stack kripto modern) | Rendah — adopsi masih terbatas |
| Nonce/tag | Nonce 96-bit, tag 128-bit | Nonce 96-bit (direkomendasikan), tag 128-bit | Nonce 96-bit, tag 128-bit |
| Ekspansi ciphertext | +16 byte (tag) | +16 byte (tag) | +16 byte (tag) |
| Kompleksitas implementasi tanpa akselerasi hardware | Rendah — didesain software-friendly sejak awal, tanpa S-box tabel | Tinggi — implementasi software AES table-based rawan cache-timing; butuh implementasi constant-time yang lebih hati-hati tanpa AES-NI | Sama seperti AES-GCM (berbasis AES) + overhead 2-pass tambahan |
| Dukungan ekosistem | Luas di software modern (terutama non-x86/tanpa AES-NI) | Sangat luas, terutama di hardware dengan AES-NI/ARMv8 Crypto Extensions | Terbatas, niche use-case misuse-resistance |
| Konsumsi resource | Cepat pada CPU modern tanpa hardware acceleration khusus | Sangat cepat DENGAN AES-NI; jauh lebih lambat tanpa AES-NI (mis. beberapa target ARM low-end) | Sebanding AES-GCM + overhead pass kedua (~30% lebih lambat menurut spesifikasi RFC 8452) |

**Sintesis**: ChaCha20-Poly1305 dipertahankan karena performa software-friendly tanpa bergantung pada AES-NI (penting karena AKSARA mendistribusikan binary lintas Windows/Linux/macOS Apple Silicon dengan dukungan akselerasi AES yang tidak seragam) dan karena merupakan token AEAD resmi (`ChaChaPoly`) pada pola Noise yang dipilih. AES-256-GCM ditolak bukan karena kurang aman, tapi karena risiko implementasi non-constant-time lebih tinggi tanpa hardware acceleration. AES-GCM-SIV — meski menawarkan misuse-resistance yang secara teoretis lebih unggul — ditolak karena kompleksitas 2-pass tambahan dan adopsi ekosistem yang lebih rendah, sementara mitigasi AKSARA saat ini (nonce random 96-bit per operasi, volume pemakaian rendah) dinilai memadai untuk skala ancaman aplikasi chat personal. **Catatan risiko yang harus diterima secara sadar**: bila di masa depan AKSARA berkembang ke skenario volume tinggi/multi-device dengan kunci sama, migrasi ke AEAD misuse-resistant seperti AES-GCM-SIV patut dipertimbangkan ulang.

---

## 4. Fungsi Hash: BLAKE2s vs. SHA-256 vs. SHA3-256

| Kriteria | **BLAKE2s** (dipakai AKSARA, CR-002/003) | SHA-256 (`fips180-4`) | SHA3-256 (`fips202`) |
|----------|---------------------------------------------|----------------------------|----------------------------|
| Security level (output) | 256-bit, collision-resistance penuh | 256-bit, collision-resistance penuh | 256-bit, collision-resistance penuh |
| Standardisasi | RFC 7693 (IETF) | FIPS 180-4 (NIST) — standar hash paling luas dipakai global | FIPS 202 (NIST) — pemenang kompetisi SHA-3 |
| Maturitas library (Rust) | `blake2` (RustCrypto) — matang, sekaligus dependency internal `snow` | `sha2` (RustCrypto) — sangat matang | `sha3` (RustCrypto) — matang |
| Interoperabilitas | Menengah — dipakai di ekosistem Noise/WireGuard/argon2, kurang universal dibanding SHA-2 | Sangat tinggi — hampir universal (TLS, Bitcoin, Git, dst.) | Menengah — adopsi tumbuh tapi belum sepopuler SHA-2 |
| Kompleksitas implementasi | Rendah | Rendah (desain Merkle-Damgard klasik, sangat matang) | Menengah (sponge construction Keccak, struktur berbeda dari SHA-2) |
| Dukungan ekosistem | Baik untuk kripto modern (Argon2 internal juga memakai BLAKE2b, Noise memakai BLAKE2s) | Terbaik/paling universal di seluruh industri | Baik, terutama untuk kebutuhan yang secara eksplisit menghindari struktur Merkle-Damgard SHA-2 |
| Konsumsi resource (software, tanpa akselerasi hash khusus) | **Cepat** — didesain eksplisit "fast as MD5" (`aumasson2013blake2`) | Cepat, kompetitif dengan BLAKE2 pada CPU modern (apalagi dengan SHA extensions Intel/ARM) | Lebih lambat dari SHA-2/BLAKE2 pada CPU umum tanpa akselerasi hardware Keccak khusus |

**Sintesis**: BLAKE2s dipertahankan terutama karena KONSISTENSI dengan pola Noise yang sudah dipilih (`_BLAKE2s` adalah bagian dari nama pattern `Noise_IK_25519_ChaChaPoly_BLAKE2s`) — memakai hash berbeda untuk fingerprint/KDF aplikasi vs. hash internal Noise akan menambah satu dependency lagi tanpa manfaat keamanan tambahan yang jelas. SHA-256 adalah alternatif yang sangat valid dan lebih universal, ditolak murni karena tidak memberi manfaat tambahan yang signifikan pada konteks AKSARA sambil menambah satu primitif hash lagi. SHA3-256 ditolak karena performa software CPU umum yang secara historis lebih lambat tanpa akselerasi hardware Keccak khusus, tanpa keunggulan properti keamanan yang relevan untuk kasus pakai AKSARA saat ini (bukan aplikasi yang secara spesifik butuh menghindari kerentanan struktural Merkle-Damgard SHA-2, karena BLAKE2 sendiri sudah bukan Merkle-Damgard murni).

---

## 5. Password-Based Key Derivation: Argon2id vs. scrypt vs. PBKDF2

| Kriteria | **Argon2id** (dipakai AKSARA, CR-014) | scrypt (`rfc7914`, `percival2009scrypt`) | PBKDF2 (`rfc8018`) |
|----------|--------------------------------------------|------------------------------------------------|---------------------------|
| Security level (resistensi brute-force hardware khusus) | **Tinggi** — memory-hard, tuning `id` side-channel-aware | Tinggi — memory-hard (pendahulu Argon2) | **Rendah** — hanya time-hard (iterasi HMAC), TIDAK memory-hard |
| Standardisasi | RFC 9106 (IETF/CFRG, 2021) — lebih baru | RFC 7914 (IETF, 2016) | RFC 8018/PKCS#5 (IETF, 2017; asal PKCS#5 1999) |
| Maturitas library (Rust) | `argon2` (RustCrypto) — matang | `scrypt` (RustCrypto) — matang | `pbkdf2` (RustCrypto) — sangat matang, paling lama dipakai |
| Misuse/side-channel resistance | Hybrid — separuh pertama data-independent (anti-timing), separuh kedua data-dependent (anti-trade-off) | Data-dependent murni (mirip Argon2d) — TIDAK ada varian side-channel-aware bawaan | Tidak relevan (bukan memory-hard, kerentanan utamanya justru pada resistensi ASIC/GPU, bukan side-channel timing) |
| Interoperabilitas | Tumbuh pesat (pemenang PHC, standar terbaru), dipakai luas software modern (banyak password manager) | Mapan lama (dipakai Litecoin dkk.), tapi mulai digantikan Argon2 pada aplikasi baru | Sangat luas secara historis (WPA2, banyak sistem legacy) — masih default di beberapa framework lama |
| Kompleksitas tuning parameter | Menengah (3 parameter: memory, iterations, parallelism) | Menengah (3 parameter: N, r, p — interaksi antar-parameter kurang intuitif) | Rendah (1 parameter: iteration count) — tapi kesederhanaan ini juga kelemahannya |
| Konsumsi resource | Memory tinggi (AKSARA: 19 MiB) + waktu sedang (~100ms diklaim, belum diverifikasi) | Memory tinggi juga, biasanya dikonfigurasi lebih besar (mis. 16-128 MiB umum) | Memory NEGLIGIBLE (kelemahan utamanya) — hanya CPU time |
| Dukungan ekosistem | Terbaik untuk password hashing modern (rekomendasi OWASP 2024 terbaru, sesuai komentar kode AKSARA) | Baik, tapi rekomendasi keamanan modern (OWASP) kini condong ke Argon2id | Masih diterima untuk kompatibilitas legacy, TAPI tidak lagi direkomendasikan sebagai pilihan utama aplikasi baru |

**Sintesis**: Argon2id dipertahankan sebagai pilihan paling sesuai rekomendasi keamanan terkini (RFC terbaru 2021, pemenang PHC, dan secara eksplisit disebut mengikuti "OWASP 2024" pada komentar kode AKSARA — meski klaim timing spesifik belum diverifikasi benchmark, lihat `04_CRYPTOGRAPHIC_JUSTIFICATION.md` CORE-5 poin 8/13). scrypt ditolak bukan karena lemah — scrypt tetap memory-hard dan aman — melainkan karena Argon2id adalah evolusi yang secara eksplisit dirancang mengatasi keterbatasan analitis scrypt (analisis kriptanalisis Argon2 lebih matang dan terbaru). PBKDF2 ditolak tegas karena BUKAN memory-hard — jauh lebih rentan terhadap serangan hardware paralel (ASIC/GPU/FPGA) yang justru menjadi ancaman utama terhadap KDF berbasis passphrase pada era saat ini.

---

## 6. Identitas Kriptografis: Ed25519 vs. ECDSA P-256 vs. RSA-2048/RSA-PSS

> Catatan: AKSARA saat ini HANYA men-generate/menyimpan keypair Ed25519 (CR-015) — TIDAK ada operasi sign/verify aktif yang teraudit (lihat `04_CRYPTOGRAPHIC_JUSTIFICATION.md` CORE-6 poin 2/13). Perbandingan berikut membahas properti algoritmis Ed25519 sebagai pilihan desain identitas jangka-panjang, bukan evaluasi atas pemakaian tanda tangan yang sudah terbukti aktif di source.

| Kriteria | **Ed25519** (dipakai AKSARA, CR-015) | ECDSA P-256 (`fips186-5`) | RSA-2048/RSA-PSS |
|----------|------------------------------------------|-------------------------------|---------------------|
| Security level | ~128-bit | ~128-bit | ~112-bit (RSA-2048, di bawah 128-bit) |
| Standardisasi | RFC 8032 (IETF) + kini FIPS 186-5/SP 800-186 (NIST, 2023) | FIPS 186-5 (NIST) — standar lama dan mapan | FIPS 186-5 (NIST) — standar sangat lama dan mapan |
| Maturitas library (Rust) | `ed25519-dalek` — matang | `p256`/`ecdsa` (RustCrypto) — matang, tidak dipakai AKSARA | `rsa` (RustCrypto) — matang, tidak dipakai AKSARA |
| Misuse resistance | **Tinggi** — signature deterministic, tidak butuh RNG saat signing (aman dari kegagalan RNG signing) | **Rendah tanpa RFC 6979** — nonce per-signature harus RANDOM dan UNIK; kebocoran/reuse nonce membuka ekstraksi private key total (preseden nyata: Sony PS3, beberapa dompet Bitcoin/Android) | Tidak butuh nonce per-signature (deterministic secara struktural untuk RSA-PSS dengan catatan), tapi rentan pada implementasi padding yang salah (preseden: Bleichenbacher) |
| Interoperabilitas | Tinggi dan terus tumbuh (SSH, TLS 1.3, banyak sistem modern) | Sangat tinggi (web PKI legacy, banyak sistem pemerintah) | Sangat tinggi historis (masih dominan di beberapa sistem legacy/PKI lama) |
| Ukuran kunci/signature | Public key 32 byte, signature 64 byte — sangat ringkas | Public key ~64 byte (uncompressed), signature ~64-72 byte (DER-encoded variable) | Public key 256 byte (2048-bit), signature 256 byte — jauh lebih besar |
| Kompleksitas implementasi | Rendah — tidak ada encoding DER variable-length, tidak ada isu malleability signature | Menengah-tinggi — encoding DER, isu signature malleability historis, butuh RFC 6979 tambahan untuk determinism | Tinggi — padding scheme (PSS) harus benar, ukuran modulus besar |
| Konsumsi resource | Signing/verifying sangat cepat (ratusan ribu operasi/detik pada hardware komoditas, `bernstein2012ed25519`) | Cepat, sebanding tanpa hardware acceleration | Jauh lebih lambat, terutama untuk operasi private-key (signing) |

**Sintesis**: Ed25519 adalah pilihan yang tepat untuk identitas AKSARA — ukuran kunci/signature ringkas krusial untuk fingerprint yang harus mudah diverifikasi manusia dan invite code yang ringkas, dan sifat deterministic signature menghilangkan seluruh kelas kerentanan "nonce reuse ECDSA" yang punya preseden insiden nyata. ECDSA P-256 ditolak terutama karena risiko implementasi nonce yang lebih tinggi (kecuali memakai varian deterministic RFC 6979 tambahan, yang berarti kompleksitas ekstra). RSA ditolak karena ukuran kunci/signature yang jauh lebih besar (tidak sesuai kebutuhan fingerprint/invite ringkas) dan level keamanan efektif yang lebih rendah pada ukuran kunci setara (2048-bit RSA ≈ 112-bit, di bawah 128-bit Ed25519/ECDSA). **Catatan kejujuran evidence**: karena AKSARA belum memakai sisi signing Ed25519 secara aktif, keunggulan misuse-resistance ini bersifat POTENSIAL (berlaku bila fitur signing diaktifkan), bukan keunggulan yang sudah terbukti dimanfaatkan pada implementasi saat ini.

---

## 7. Sumber Entropi (CSPRNG): OsRng vs. ChaCha20Rng vs. ThreadRng

| Kriteria | **OsRng** (dipakai AKSARA, CR-004/CR-017) | ChaCha20Rng (`rand_chacha`) | ThreadRng |
|----------|------------------------------------------------|-----------------------------------|--------------|
| Sumber keamanan | Langsung dari CSPRNG kernel OS (entropi fisik + DRBG kernel, selaras kriteria `sp800-90a`) | PRNG userspace deterministic, DI-SEED dari OS sekali di awal | Wrapper thread-local di atas CSPRNG userspace, di-reseed periodik dari `OsRng` |
| Standardisasi | Tidak ada standar formula tunggal (implementasi bergantung OS: `getrandom(2)`, `BCryptGenRandom`, dst.) — tapi kriteria keamanannya selaras `sp800-90a` | Berbasis algoritma ChaCha20 yang terstandardisasi (`rfc8439`), TAPI skema reseed/manajemen state adalah desain crate, bukan standar formal | Sama seperti ChaCha20Rng dari sisi standardisasi algoritma dasar |
| Maturitas library | `rand::rngs::OsRng` — matang, dipakai luas sebagai baseline seluruh ekosistem `rand` | `rand_chacha` — matang, dipakai sebagai default internal `rand::thread_rng()` | Bagian dari crate `rand` inti — matang |
| Misuse resistance (seeding) | **Tinggi** — tidak ada state untuk di-mismanage, setiap panggilan langsung ke OS | Menengah — bila seeding awal keliru/gagal, seluruh output turunan berisiko predictable | Menengah — sama seperti ChaCha20Rng, ditambah kompleksitas thread-local state |
| Portabilitas/interoperabilitas | Tinggi — abstraksi seragam lintas OS oleh crate `rand`/`getrandom` | Tinggi (murni algoritmik, tidak bergantung OS setelah seeding) | Tinggi, tapi didesain untuk konteks multi-thread yang tidak relevan untuk AKSARA (aplikasi TUI single-thread-dominan) |
| Kompleksitas implementasi | Rendah — tidak ada state yang dikelola aplikasi | Rendah-menengah — perlu memastikan seeding awal benar | Rendah dari sisi pemanggil, tapi state internal lebih kompleks (thread-local + reseed logic) |
| Konsumsi resource | Overhead syscall per panggilan (lebih lambat per-call) | Lebih cepat untuk pemanggilan volume tinggi (tidak ada syscall berulang) | Sebanding ChaCha20Rng untuk volume tinggi |

**Sintesis**: `OsRng` dipertahankan karena volume pemanggilan RNG pada AKSARA sangat rendah (hanya saat keygen/seal vault/nonce per pesan — bukan hot-loop volume tinggi), sehingga overhead syscall per panggilan tidak relevan secara praktis, sementara kesederhanaan (tanpa state userspace yang bisa salah dikelola) memberi permukaan audit paling kecil. `ChaCha20Rng`/`ThreadRng` unggul pada skenario volume RNG tinggi (mis. server yang melayani ribuan request/detik) — skenario yang tidak berlaku untuk AKSARA sebagai aplikasi chat P2P personal single-pengguna.

---

## Catatan Metodologis

- Seluruh perbandingan di atas dinilai pada BANYAK kriteria (bukan hanya kecepatan) sesuai instruksi TAHAP 4: security level, standardization, library maturity, misuse resistance, interoperability, key/nonce requirements, ciphertext expansion, implementation complexity, ecosystem support, dan resource consumption — masing-masing dicek relevansinya per fungsi (tidak semua kriteria berlaku sama pada setiap kategori, mis. "ciphertext expansion" tidak relevan untuk perbandingan hash function).
- Alternatif yang TIDAK dipilih AKSARA (AES-GCM/GCM-SIV, P-256, Curve448, SHA-2/SHA-3, scrypt/PBKDF2, ECDSA/RSA, ChaCha20Rng/ThreadRng) bukan berarti "tidak aman" — seluruhnya adalah pilihan valid dengan trade-off berbeda; penolakan didasarkan pada kesesuaian dengan konteks spesifik AKSARA (binary kecil lintas-platform tanpa akselerasi hardware seragam, model P2P serverless tanpa PKI, skala pemakaian personal bukan high-volume server).
- Perbandingan ini TIDAK mengklaim superioritas mutlak satu algoritma atas yang lain secara umum — klaim dibatasi pada kecocokan kontekstual dengan arsitektur dan skenario ancaman AKSARA sebagaimana didokumentasikan di `02_CRYPTO_IMPLEMENTATION_AUDIT.md` dan `03_CRYPTO_INVENTORY_NORMALIZED.md`.
