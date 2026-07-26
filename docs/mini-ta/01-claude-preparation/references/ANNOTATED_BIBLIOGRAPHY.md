# Annotated Bibliography — AKSARA Mini-TA

Anotasi singkat (1-2 paragraf) per sumber, dikelompokkan sesuai kategori di `REFERENCES.bib`. Citekey mengacu ke `REFERENCES.bib`.

## Kerangka Protokol dan Key Agreement (CORE-1, CORE-2)

**`noise2018`** — Perrin, *The Noise Protocol Framework*, Rev. 34 (2018). Spesifikasi resmi yang mendefinisikan bahasa pola handshake Noise, termasuk pola `IK` yang dipakai AKSARA (`Noise_IK_25519_ChaChaPoly_BLAKE2s`, dikonfirmasi di `src/crypto/handshake.rs:3`). Berstatus "official/unstable" — bukan RFC IETF, sehingga tidak melalui proses standardisasi formal, namun menjadi rujukan de facto industri (dipakai WireGuard, Lightning Network, dsb.). Dipakai untuk menjustifikasi properti keamanan pola IK (mutual authentication dua-pesan, identity hiding parsial untuk initiator) yang diklaim AKSARA.

**`rfc7748`** — Langley, Hamburg, Turner, RFC 7748 (2016). Standar IETF yang mendefinisikan fungsi X25519/X448 secara implementer-oriented dengan test vector resmi. Menjadi rujukan normatif untuk operasi Diffie-Hellman token `es/ss/ee/se` pada handshake Noise_IK AKSARA (CR-007) dan untuk parameter ukuran kunci 32-byte yang dipakai `x25519-dalek`.

**`bernstein2006curve25519`** — Bernstein, *Curve25519: New Diffie-Hellman Speed Records*, PKC 2006. Paper asli yang memperkenalkan kurva Curve25519 dan fungsi X25519, termasuk argumen desain di balik pemilihan parameter kurva (Montgomery form, cofactor kecil, constant-time scalar multiplication). Sumber primer untuk menjustifikasi alasan pemilihan X25519 dibanding kurva NIST pada `05_CRYPTO_ALTERNATIVE_COMPARISON.md`.

## AEAD — ChaCha20-Poly1305 (CORE-3)

**`rfc8439`** — Nir, Langley, RFC 8439 (2018). Standar IETF yang mengkombinasikan ChaCha20 dan Poly1305 menjadi satu AEAD (`AEAD_CHACHA20_POLY1305`) dengan nonce 96-bit dan tag 128-bit — parameter ini persis dengan yang diobservasi di ketiga lokasi pemakaian AEAD AKSARA (contact store CR-001, Noise transport CR-008, vault CR-013). Menggantikan RFC 7539 (versi awal, konstruksi identik, hanya perbaikan editorial).

**`bernstein2008chacha`** — Bernstein, *ChaCha, a variant of Salsa20* (2008). Technical report asli penulis stream cipher ChaCha, menjelaskan modifikasi dari Salsa20 untuk meningkatkan difusi per putaran. Dicatat sebagai sumber MEDIUM-HIGH (bukan MEDIUM-HIGH bukan HIGH murni) karena dokumen ini tidak melalui peer-review formal — statusnya sebagai technical report pribadi penulis, baru mendapat validasi luas lewat adopsi di RFC 8439 dan analisis kriptanalisis independen pihak ketiga.

**`bernstein2005poly1305`** — Bernstein, *The Poly1305-AES Message-Authentication Code*, FSE 2005. Paper peer-reviewed asli MAC Poly1305 (varian AES pada publikasi asli; RFC 8439 menggantikan komponen AES dengan ChaCha20 block function untuk keystream kunci one-time). Sumber untuk argumen keamanan bukti Poly1305 sebagai universal hash MAC dengan batas kegagalan pemalsuan yang ketat.

## Password-Based Key Derivation — Argon2id (CORE-5)

**`rfc9106`** — Biryukov, Dinu, Khovratovich, Josefsson, RFC 9106 (2021). Standar IETF (produk CFRG) yang mendefinisikan Argon2 versi 1.3, termasuk parameter default dan rekomendasi Argon2id sebagai varian yang WAJIB didukung. Cocok dengan versi Argon2 (0x13/19) yang diverifikasi di `src/identity/vault.rs` (CR-014).

**`biryukov2016argon2`** — Biryukov, Dinu, Khovratovich, EuroS&P 2016. Paper pemenang Password Hashing Competition (PHC) 2015 yang memperkenalkan Argon2, termasuk justifikasi desain hybrid Argon2id (data-independent untuk separuh pertama pass, data-dependent untuk sisanya) sebagai kompromi antara resistansi side-channel dan resistansi trade-off attack. Sumber utama untuk menjustifikasi pemilihan Argon2id dibanding Argon2i/Argon2d murni.

## Hash — BLAKE2s (CORE-4)

**`rfc7693`** — Saarinen, Aumasson, RFC 7693 (2015). Standar IETF untuk BLAKE2b dan BLAKE2s, termasuk test vector resmi. Rujukan untuk parameter output BLAKE2s-256 (32 byte) yang dipakai pada fingerprint identitas AKSARA (CR-002) dan derivasi kunci contact-store (CR-003).

**`aumasson2013blake2`** — Aumasson, Neves, Wilcox-O'Hearn, Winnerlein, ACNS 2013. Paper asli BLAKE2, penerus finalis SHA-3 BLAKE, dioptimalkan untuk kecepatan software. Sumber untuk argumen keamanan (BLAKE2 mewarisi bukti keamanan BLAKE/SHA-3 finalist) dan argumen performa dibanding SHA-2/SHA-3 yang dipakai pada `05_CRYPTO_ALTERNATIVE_COMPARISON.md`.

## Identitas — Ed25519 (CORE-6)

**`rfc8032`** — Josefsson, Liusvaara, RFC 8032 (2017). Standar IETF EdDSA yang mendefinisikan parameter Ed25519 (kurva edwards25519, hash SHA-512). AKSARA hanya mengimplementasikan generate/simpan kunci Ed25519 (CR-015) tanpa operasi sign/verify yang teraudit — RFC ini tetap relevan sebagai rujukan format kunci 32-byte yang dipakai.

**`bernstein2012ed25519`** — Bernstein, Duif, Lange, Schwabe, Yang, J. Cryptogr. Eng. 2012 (versi ringkas di CHES 2011). Paper asli Ed25519, menunjukkan throughput signing/verifying tinggi pada hardware komoditas serta argumen keamanan (deterministic nonce menghindari kegagalan seperti kasus Sony PS3 ECDSA). Relevan untuk BAB pembahasan meski AKSARA belum memanfaatkan sisi tanda tangan Ed25519 secara aktif di source yang diaudit — dicatat eksplisit sebagai keterbatasan di `03_CRYPTO_INVENTORY_NORMALIZED.md` §6.

**`fips186-5`** dan **`sp800-186`** — NIST (2023). Standar resmi AS yang mengadopsi Ed25519/X25519 ke dalam FIPS 186-5 dan SP 800-186 setelah sebelumnya hanya mengakui kurva Weierstrass NIST (P-256, dst). Dipakai sebagai bukti bahwa Ed25519/X25519 kini berstatus disetujui pemerintah AS, bukan hanya standar IETF/CFRG — memperkuat argumen maturitas standar pada justifikasi.

## Sumber Entropi — CSPRNG (CORE-7)

**`sp800-90a`** — NIST SP 800-90A Rev. 1 (2015). Standar rekomendasi desain DRBG (deterministic random bit generator) yang menjadi rujukan umum industri untuk apa yang dianggap CSPRNG yang aman. AKSARA sendiri tidak mengimplementasikan DRBG sendiri — ia mendelegasikan seluruhnya ke `OsRng` milik OS (CR-004, CR-017) — sehingga standar ini dipakai sebagai konteks kriteria keamanan CSPRNG secara umum, bukan sebagai bukti implementasi langsung.

**`randcrate`** — dokumentasi crate `rand` (`OsRng`). Menjelaskan bahwa `OsRng` membaca langsung dari sumber entropi OS (`getrandom(2)` di Linux, `RtlGenRandom`/`BCryptGenRandom` di Windows, dsb.) tanpa PRNG userspace tambahan — relevan untuk klaim bahwa AKSARA tidak melakukan seeding manual/custom.

## Pembanding untuk `05_CRYPTO_ALTERNATIVE_COMPARISON.md`

**`sp800-38d`** (Dworkin, NIST, 2007) dan **`rfc8452`** (Gueron, Langley, Lindell, 2019) — rujukan AES-GCM dan AES-GCM-SIV sebagai dua alternatif AEAD yang dibandingkan dengan ChaCha20-Poly1305: AES-GCM mewakili "standar dominan berbasis hardware AES-NI", AES-GCM-SIV mewakili "AEAD misuse-resistant" yang tidak fatal pada nonce reuse.

**`rfc7914`** (Percival, Josefsson, 2016) dan **`percival2009scrypt`** (Percival, BSDCan 2009) — rujukan scrypt sebagai alternatif memory-hard KDF pra-Argon2, dipakai untuk membandingkan Argon2id vs scrypt (keduanya memory-hard, beda skema tuning parameter dan riwayat kriptanalisis).

**`rfc8018`** (Moriarty, Kaliski, Rusch, 2017) — rujukan PBKDF2 sebagai alternatif KDF non-memory-hard (murni iterasi HMAC), dipakai sebagai kontras terhadap Argon2id/scrypt untuk menunjukkan kerentanan terhadap serangan hardware khusus (ASIC/GPU/FPGA).

**`fips180-4`** (NIST, 2015) dan **`fips202`** (NIST, 2015) — rujukan SHA-256 (SHA-2) dan SHA3-256 sebagai dua alternatif hash function yang dibandingkan dengan BLAKE2s.

**`rfc8446`** (Rescorla, 2018) dan **`x3dh2016`** (Marlinspike, Perrin, 2016) — rujukan TLS 1.3 dan X3DH (Signal) sebagai dua kerangka key-agreement/handshake alternatif yang dibandingkan dengan Noise_IK pada level desain protokol (bukan level primitif tunggal).

## Dokumentasi Library (Crate Rust)

**`snowcrate`**, **`chacha20poly1305crate`**, **`ed25519dalekcrate`**, **`x25519dalekcrate`**, **`argon2crate`**, **`blake2crate`**, **`randcrate`** — dokumentasi resmi tujuh crate Rust yang menjadi dependency langsung implementasi kripto AKSARA (versi persis sesuai `Cargo.lock`, dikonfirmasi ulang di TAHAP 2/3). Dipakai sebagai bukti dukungan library/maturitas ekosistem pada justifikasi, BUKAN sebagai sumber klaim keamanan teoretis — untuk itu tetap dirujuk ke standar/paper primer di atas. Catatan penting dari dokumentasi `snow`: crate ini secara eksplisit menyatakan **belum menerima audit keamanan formal** ("this library has not received any formal audit") — dicatat sebagai risiko implementasi di `04_CRYPTOGRAPHIC_JUSTIFICATION.md`.

## Related Work — Aplikasi/Protokol Chat P2P Terenkripsi Sejenis (TAHAP 10, SESSION 4)

Detail perbandingan lengkap ada di `10_RELATED_WORK_AND_GAP.md` — anotasi berikut hanya ringkasan sumber, bukan analisis gap.

**`kobeissi2019noiseexplorer`** — Kobeissi, Nicolas, Bhargavan, *Noise Explorer*, IEEE EuroS&P 2019 (eprint 2018/766). Tool dan metodologi verifikasi formal otomatis untuk pola handshake Noise Protocol Framework, termasuk pola `IK` yang dipakai AKSARA. Relevan sebagai pembanding: AKSARA memakai Noise_IK via crate `snow` tanpa verifikasi formal apapun terhadap instansiasi spesifiknya sendiri (`Noise_IK_25519_ChaChaPoly_BLAKE2s`) — properti keamanan yang diklaim AKSARA (§5.3 `06_PROTOCOL_SPECIFICATION.md`) diwarisi dari analisis umum pola Noise_IK di `noise2018`, bukan hasil verifikasi formal khusus AKSARA seperti yang dilakukan paper ini terhadap pola-pola Noise lain.

**`cohngordon2020signal`** — Cohn-Gordon, Cremers, Dowling, Garratt, Stebila, *A Formal Security Analysis of the Signal Messaging Protocol*, J. Cryptology 2020. Analisis formal protokol Signal dengan properti "future secrecy"/post-compromise security via ratcheting (kunci sesi diperbarui tiap pesan). Pembanding penting untuk gap AKSARA: AKSARA memakai **satu** kunci transport statis sepanjang masa hidup sesi tanpa ratchet apapun (`07_KEY_LIFECYCLE.md` §6) — tidak ada post-compromise security setelah kompromi kunci sesi.

**`donenfeld2017wireguard`** — Donenfeld, *WireGuard: Next Generation Kernel Network Tunnel*, NDSS 2017. VPN kernel-level yang memakai Noise Protocol Framework dengan kombinasi primitif serupa AKSARA (Curve25519/X25519, ChaCha20-Poly1305, BLAKE2s). Pembanding arsitektural: WireGuard beroperasi di layer jaringan (tunnel IP) dengan static-key konfigurasi out-of-band mirip invite code AKSARA, tapi WireGuard memakai varian pola `Noise_IK` dengan cookie anti-DoS dan rekey berkala berbasis waktu/volume — dua mekanisme yang **tidak ada** pada AKSARA.

**`borisov2004otr`** — Borisov, Goldberg, Brewer, *Off-the-Record Communication, or, Why Not To Use PGP*, WPES 2004. Paper fondasi yang memperkenalkan properti "deniability" dan "perfect forward secrecy" sebagai syarat pesan instan yang aman, kontras dengan PGP (non-repudiation permanen, tanpa forward secrecy). Relevan sebagai kerangka evaluasi historis: AKSARA tidak dirancang untuk deniability (Ed25519 dipakai murni fingerprint, bukan signing — lihat `07_KEY_LIFECYCLE.md` §5.1) dan forward secrecy AKSARA berstatus `DOCUMENTED_ONLY`, bukan properti yang diverifikasi seperti OTR generasi berikutnya.

**`albrecht2024matrix`** — Albrecht, Dowling, Jones, *Device-Oriented Group Messaging: A Formal Cryptographic Analysis of Matrix' Core*, IEEE S&P 2024 (eprint 2023/1300). Analisis formal protokol Matrix (Olm/Megolm) untuk pesan terenkripsi terfederasi multi-device dengan rotasi sesi Megolm eksplisit. Pembanding langsung untuk T7 di `08_THREAT_MODEL.md`: Matrix menyediakan mekanisme rotasi kunci sesi yang dianalisis formal, sedangkan AKSARA **tidak memiliki mekanisme rotasi/revokasi apapun** untuk kunci manapun (vault, identity, Noise, session).

**`briarspec`** — Briar Project, spesifikasi teknis Bramble Protocol Suite. Aplikasi pesan P2P serverless dengan transport ganda (Tor untuk online, Bluetooth/Wi-Fi untuk offline) — arsitektur paling dekat dengan AKSARA di antara seluruh related work (P2P murni, memakai Tor sebagai salah satu jalur transport, kontak dipertukarkan out-of-band). Bukan paper peer-review, melainkan spesifikasi proyek resmi — dicatat kualitas MEDIUM.

**`toxspec`** — TokTok/Tox Project, spesifikasi protokol Tox. Pesan instan P2P murni tanpa server sama sekali, kunci publik/privat dipertukarkan langsung, discovery peer via DHT (bukan mDNS seperti AKSARA), dienkripsi NaCl (`crypto_box`, XSalsa20-Poly1305) bukan Noise Protocol Framework. Proyek secara eksplisit menyatakan **belum diaudit keamanan formal oleh pihak independen** — paralel langsung dengan status crate `snow` yang dipakai AKSARA (`snowcrate`, §Dokumentasi Library di atas). Kualitas MEDIUM (spesifikasi proyek, bukan peer-review).
