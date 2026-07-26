# 04 — Justifikasi Kriptografi AKSARA

Dokumen ini menjustifikasi 7 komponen kriptografi inti (`CORE-1`..`CORE-7`) hasil konsolidasi `03_CRYPTO_INVENTORY_NORMALIZED.md` §4, memakai evidence source-level dari `02_CRYPTO_IMPLEMENTATION_AUDIT.md` (ID `CR-xxx`) dan referensi terverifikasi di `references/` (citekey merujuk `references/REFERENCES.bib`).

**Catatan cakupan proposal vs implementasi**: tidak ditemukan dokumen proposal kriptografi terpisah untuk AKSARA di repository ini (pencarian `*proposal*` pada seluruh repo nihil hasil). Sumber kebenaran satu-satunya yang tersedia untuk sesi ini adalah source code aktual (sesuai hierarki `AGENTS.md`). Dengan demikian tidak ada konflik "proposal vs implementasi" yang dapat dilaporkan pada sesi ini — bila dokumen proposal ditemukan di kemudian hari (mis. dari anggota tim), bagian ini WAJIB direvisi.

**Format tiap komponen** mengikuti 15 poin TAHAP 4: (1) masalah yang diselesaikan, (2) properti keamanan, (3) alasan pemilihan, (4) standar/paper utama, (5) dukungan library, (6) kompatibilitas arsitektur, (7) dampak ukuran paket, (8) dampak komputasi, (9) dampak memori, (10) trade-off, (11) alternatif dipertimbangkan, (12) alasan alternatif tidak dipilih, (13) keterbatasan, (14) asumsi penggunaan aman, (15) risiko implementasi. Poin 11-12 dirangkum singkat di sini — perbandingan penuh (>1 kriteria per alternatif) ada di `05_CRYPTO_ALTERNATIVE_COMPARISON.md`.

---

## CORE-1 — Noise_IK (via `snow` 0.10.0)

Evidence: CR-007, CR-008, CR-009, CR-010, CR-011, CR-025, CR-026, CR-027, CR-028.

1. **Masalah**: AKSARA butuh membangun kanal terenkripsi dan saling terautentikasi antara dua pihak P2P tanpa server perantara dan tanpa PKI/CA terpusat (selaras dengan identitas proyek sebagai aplikasi serverless), dengan proses handshake seringkas mungkin (2 pesan) sebelum sesi chat dimulai.
2. **Properti keamanan**: mutual authentication kedua static key di akhir handshake; forward secrecy dari kontribusi ephemeral key pada tiap sesi (kompromi static key jangka-panjang tidak membuka sesi lampau); kerahasiaan static key initiator terhadap penyadap pasif (dikirim terenkripsi pada pesan pertama) — pola `IK` mengasumsikan initiator SUDAH tahu static key responder sebelum handshake dimulai (bukan identity-hiding dua arah penuh).
3. **Alasan pemilihan**: pola IK cocok dengan model AKSARA "kontak sudah bertukar fingerprint/invite out-of-band sebelum terhubung" (mirip prasyarat WireGuard/Signal known-key); menghasilkan 1-RTT handshake ringan untuk aplikasi chat terminal; menghindari kompleksitas stack X.509/TLS penuh yang tidak dibutuhkan untuk model trust P2P AKSARA.
4. **Standar/paper utama**: `noise2018` (spesifikasi resmi Noise Protocol Framework, Trevor Perrin, Revisi 34).
5. **Dukungan library**: `snowcrate` (crate `snow` 0.10.0, tracking Noise spec revisi 34). Catatan penting: dokumentasi resmi crate secara eksplisit menyatakan **belum menerima audit keamanan formal**.
6. **Kompatibilitas arsitektur**: selaras dengan model role AKSARA yang ditentukan dinamis dari perbandingan fingerprint (bukan role tetap client/server) dan tidak membutuhkan infrastruktur PKI eksternal apa pun.
7. **Dampak ukuran paket**: dependency internal `snow` (chacha20poly1305, blake2, x25519-dalek) sebagian besar TUMPANG TINDIH dengan dependency yang sudah dipakai AKSARA di modul lain (bukan penambahan murni terhadap ukuran binary).
8. **Dampak komputasi**: 3-4 operasi scalar multiplication X25519 (token `es, ss, ee, se`) plus beberapa operasi ChaChaPoly kecil — seluruhnya hanya terjadi SEKALI di awal sesi, bukan per pesan chat, sehingga overhead diabaikan relatif terhadap durasi sesi.
9. **Dampak memori**: `HandshakeState`/`TransportState` berukuran kecil (kunci 32-byte × beberapa + cipher state) — negligible untuk aplikasi TUI single-pengguna.
10. **Trade-off**: kesederhanaan dan latensi rendah (1-RTT) ditukar dengan ketiadaan fitur PKI (tidak ada revocation/expiry sertifikat), tidak ada identity-hiding dua arah penuh, dan tidak ada mekanisme resumption 0-RTT bawaan seperti TLS 1.3.
11. **Alternatif dipertimbangkan**: TLS 1.3 (`rfc8446`); Signal X3DH + Double Ratchet (`x3dh2016`).
12. **Alasan tidak dipilih (ringkas)**: TLS 1.3 membutuhkan stack X.509/CA yang tidak natural untuk identitas self-sovereign P2P; X3DH dirancang untuk messaging asinkron store-and-forward dengan broker server dan banyak one-time prekey — tidak cocok dengan model AKSARA yang koneksi langsung sinkron. Detail lengkap di `05_CRYPTO_ALTERNATIVE_COMPARISON.md` §1.
13. **Keterbatasan**: sub-mekanisme internal (hash transcript Noise, HKDF) TIDAK terverifikasi langsung dari source aplikasi — murni inferensi dari string nama pattern `Noise_IK_25519_ChaChaPoly_BLAKE2s` (CR-009/CR-010, confidence LOW); tidak ada pengecekan eksplisit terhadap public key peer yang all-zero/low-order point di `handshake.rs`; tidak ada test yang mengirim payload aplikasi non-kosong pada pesan handshake (payload 0-RTT tidak teruji).
14. **Asumsi penggunaan aman**: initiator HARUS sudah memiliki static key responder yang valid (fingerprint terverifikasi out-of-band) SEBELUM handshake dimulai — bila fingerprint palsu diterima/diverifikasi keliru oleh pengguna, Noise_IK tidak melindungi dari MITM karena root-of-trust berada di luar protokol Noise itu sendiri (pada proses verifikasi fingerprint manusia).
15. **Risiko implementasi**: crate `snow` belum diaudit formal (self-declared pada dokumentasi resminya); error dari `write_message`/`read_message`/`into_transport_mode` dipetakan seragam ke `Error::Noise` tanpa diferensiasi jenis kegagalan (CR-025) — mengurangi granularitas debugging namun juga mengurangi permukaan oracle leak.

---

## CORE-2 — X25519 (Curve25519 ECDH)

Evidence: CR-007, CR-016, CR-022, CR-032.

1. **Masalah**: dibutuhkan mekanisme key-agreement agar dua pihak dapat menyepakati shared secret melalui kanal publik tanpa pra-share rahasia, sebagai basis derivasi kunci sesi dalam handshake Noise_IK.
2. **Properti keamanan**: keamanan bertumpu pada computational Diffie-Hellman pada Curve25519 (~128-bit security level); desain kurva menjamin keamanan "twist" (semua titik pada twist kurva juga tahan serangan invalid-curve) sehingga validasi titik eksplisit tidak wajib seperti pada kurva Weierstrass; operasi scalar multiplication constant-time by design, mengurangi risiko timing side-channel.
3. **Alasan pemilihan**: performa tinggi dan permukaan kesalahan implementasi yang lebih kecil dibanding kurva Weierstrass NIST (tidak perlu validasi titik/subgroup check manual); merupakan pilihan default token `25519` pada nama pattern Noise yang dipilih project; ekosistem Rust (`x25519-dalek`) matang dan sudah dipakai bersama untuk key material identitas.
4. **Standar/paper utama**: `rfc7748` (standar IETF), `bernstein2006curve25519` (paper asli, PKC 2006).
5. **Dukungan library**: `x25519dalekcrate` (`x25519-dalek` 2.0.1).
6. **Kompatibilitas arsitektur**: representasi kunci 32-byte cocok langsung dengan boundary fungsi berbasis `[u8;32]` mentah yang dipakai konsisten di seluruh AKSARA (CR-011, CR-028) tanpa parsing ASN.1/PEM.
7. **Dampak ukuran paket**: kecil — `x25519-dalek` berbagi dependency `curve25519-dalek` dengan `ed25519-dalek` (CORE-6), tidak ada duplikasi implementasi kurva.
8. **Dampak komputasi**: satu scalar multiplication berkisar puluhan-ratusan mikrodetik pada CPU modern, jauh lebih cepat dari RSA dan kompetitif dengan/lebih cepat dari P-256 non-hardware-accelerated; dipakai 3-4 kali per handshake sesuai token pola IK.
9. **Dampak memori**: kunci 32 byte, state minimal, tidak ada precomputed table besar.
10. **Trade-off**: X25519 tidak menyediakan operasi tanda tangan native (mengharuskan keypair Ed25519 terpisah untuk fungsi identitas — lihat CORE-6); cofactor 8 (bukan prime-order murni) memerlukan penanganan hati-hati pada protokol non-Noise, meski sudah ditangani aman secara internal oleh desain fungsi X25519/`snow`.
11. **Alternatif dipertimbangkan**: NIST P-256 (`sp800-186`/`fips186-5`); Curve448/X448 (`rfc7748`).
12. **Alasan tidak dipilih (ringkas)**: P-256 memiliki riwayat kekhawatiran atas opasitas asal-usul parameter kurva dan risiko implementasi non-constant-time yang secara historis lebih tinggi; Curve448 menawarkan margin keamanan lebih tinggi (~224-bit) dengan overhead komputasi lebih besar yang tidak dibutuhkan pada skala ancaman AKSARA (aplikasi chat personal). Detail di `05_CRYPTO_ALTERNATIVE_COMPARISON.md` §2.
13. **Keterbatasan**: operasi DH aktual terjadi sepenuhnya di dalam `snow` — tidak dapat diverifikasi langsung dari source aplikasi (CR-007, confidence MEDIUM); tidak ada pengecekan eksplisit all-zero/low-order public key di `handshake.rs` (kepercayaan penuh pada `snow`+`x25519-dalek`).
14. **Asumsi penggunaan aman**: private key dibangkitkan dari CSPRNG berkualitas (CORE-7) dan dilindungi `ZeroizeOnDrop` — bila sumber randomness lemah, keamanan X25519 runtuh total tanpa terdeteksi dari level protokol.
15. **Risiko implementasi**: pada beberapa titik akses (mis. parameter `local_noise_sk` di `run_session`, CR-028), kunci privat diteruskan sebagai `[u8;32]` polos tanpa tipe zeroizing eksplisit di level parameter fungsi — berbeda dengan penyimpanan aslinya di `KeyBundle` yang sudah `ZeroizeOnDrop` (CB-070).

---

## CORE-3 — ChaCha20-Poly1305 (AEAD, 3 konteks pemakaian)

Evidence: CR-001 (contact store), CR-008 (transport Noise), CR-013/CR-018 (vault), plus duplikasi CR-024, CR-026, CR-033.

1. **Masalah**: dibutuhkan enkripsi simetris terautentikasi (confidentiality + integrity + deteksi tamper) untuk data-at-rest (vault identitas, contact store) dan data-in-transit (pesan sesi pasca-handshake).
2. **Properti keamanan**: AEAD — menggabungkan IND-CPA (confidentiality) dan INT-CTXT (integritas ciphertext); tag Poly1305 128-bit mendeteksi modifikasi ciphertext; ChaCha20 sebagai stream cipher tidak memakai S-box tabel sehingga secara inheren resisten terhadap serangan cache-timing yang menghantui implementasi AES software non-AES-NI.
3. **Alasan pemilihan**: satu primitif AEAD dipakai konsisten di tiga konteks berbeda — mengurangi permukaan kesalahan implementasi dibanding memakai AEAD berbeda per konteks; performa tinggi tanpa akselerasi hardware khusus (relevan karena AKSARA mendistribusikan binary lintas Windows/Linux/macOS Apple Silicon yang tidak seragam dukungan AES-NI-nya); merupakan standar IETF dengan test vector jelas.
4. **Standar/paper utama**: `rfc8439` (standar IETF gabungan), `bernstein2008chacha` (ChaCha), `bernstein2005poly1305` (Poly1305).
5. **Dukungan library**: `chacha20poly1305crate` (0.10.1, RustCrypto) — ekosistem matang, dipakai luas di industri Rust.
6. **Kompatibilitas arsitektur**: nonce 96-bit + tag 128-bit cocok persis dengan layout fixed-offset vault (16B salt + 12B nonce + 64B ciphertext + 16B tag = 108 byte, CR-019) dan format contact store (`[12B nonce][ciphertext+tag]` tanpa header, CB-012).
7. **Dampak ukuran paket**: kecil, pure-Rust, tanpa dependency C/hardware-specific wajib (akselerasi bersifat opsional).
8. **Dampak komputasi**: ChaCha20 murni software-friendly (throughput tinggi pada CPU modern tanpa AES-NI) — untuk ukuran pesan chat/vault AKSARA yang kecil, overhead per operasi diabaikan.
9. **Dampak memori**: state kecil (kunci 32B + counter + nonce), tanpa precomputed table besar seperti implementasi AES table-based klasik.
10. **Trade-off**: ChaCha20-Poly1305 TIDAK misuse-resistant — nonce reuse pada kunci yang sama fatal (membocorkan XOR plaintext dan membuka forgery). AKSARA memitigasi dengan nonce RANDOM 96-bit per operasi (bukan counter, CR-004/CR-018) — memadai untuk volume pemakaian personal, namun secara teori memiliki batas birthday-bound pada volume sangat tinggi dengan kunci sama (tidak relevan untuk skala pemakaian AKSARA saat ini).
11. **Alternatif dipertimbangkan**: AES-256-GCM (`sp800-38d`); AES-GCM-SIV (`rfc8452`).
12. **Alasan tidak dipilih (ringkas)**: AES-GCM software non-accelerated lebih lambat dan rawan cache-timing tanpa AES-NI; AES-GCM-SIV menawarkan nonce-misuse resistance tapi menambah kompleksitas 2-pass dan bukan token AEAD resmi pada spesifikasi Noise (`ChaChaPoly`), sementara skala AKSARA (aplikasi personal, bukan sistem high-volume) belum membutuhkan proteksi misuse-resistance tambahan. Detail di `05_CRYPTO_ALTERNATIVE_COMPARISON.md` §3.
13. **Keterbatasan**: TIDAK ada Associated Data (AAD) dipakai di ketiga konteks pemakaian — ciphertext tidak terikat ke konteks eksternal seperti path file atau versi format (CR-001, CR-013); manajemen nonce pada transport Noise (CR-008) sepenuhnya internal `snow`, tidak dapat diverifikasi dari source aplikasi.
14. **Asumsi penggunaan aman**: nonce TIDAK PERNAH diulang untuk kunci yang sama — bergantung pada kualitas CSPRNG (CORE-7) dan volume pemakaian yang relatif rendah (chat personal, bukan server high-throughput).
15. **Risiko implementasi**: sanity-check panjang ciphertext pada `vault.rs` memakai `debug_assert_eq!` yang DIKOMPILASI HILANG pada release build — tidak ada proteksi runtime di produksi (CB-086); kegagalan dekripsi dipetakan ambigu secara sengaja untuk mencegah oracle attack (CB-079) — trade-off yang tepat untuk keamanan tapi mengurangi kemudahan diagnosis kegagalan legitimate.

---

## CORE-4 — BLAKE2s / BLAKE2s-256

Evidence: CR-002 (fingerprint), CR-003 (KDF contacts), CR-009/CR-010 (internal Noise, inferensi), plus duplikasi CR-029, CR-034, CR-035.

1. **Masalah**: dibutuhkan fungsi hash cepat untuk tiga tujuan berbeda — fingerprint identitas publik (mengikat dua public key jadi satu identifier ringkas untuk diverifikasi manusia), derivasi kunci simetris single-shot dari secret identitas, dan (secara internal pada `snow`) transcript hash serta HKDF handshake Noise.
2. **Properti keamanan**: collision-resistance dan preimage-resistance setara warisan BLAKE sebagai finalis kompetisi SHA-3; output 256-bit (varian BLAKE2s, dioptimalkan 32-bit) cukup untuk fingerprint yang sulit ditabrakkan; domain-separation via context string berbeda (`aksara-fingerprint-v1` vs `aksara-contacts-key-v1`) mencegah cross-protocol attack antar dua pemakaian berbeda dalam codebase yang sama.
3. **Alasan pemilihan**: BLAKE2s (bukan BLAKE2b) dipilih karena dioptimalkan untuk platform 32-bit/arsitektur kecil, selaras dengan target binary kecil lintas-platform AKSARA; juga merupakan hash default pada pola Noise `_BLAKE2s` yang dipilih project, sehingga satu primitif hash dipakai konsisten di seluruh codebase.
4. **Standar/paper utama**: `rfc7693` (standar IETF), `aumasson2013blake2` (paper asli, ACNS 2013).
5. **Dukungan library**: `blake2crate` (0.10.6, RustCrypto) — sekaligus menjadi dependency internal `snow` untuk hash Noise, tanpa duplikasi implementasi.
6. **Kompatibilitas arsitektur**: output 32-byte cocok langsung untuk representasi hex 64-karakter (CR-006) dan sebagai kunci ChaCha20Poly1305 tanpa transformasi tambahan (CR-003).
7. **Dampak ukuran paket**: kecil; sudah menjadi dependency wajib `snow` secara internal, sehingga pemakaian langsung oleh aplikasi tidak menambah dependency baru.
8. **Dampak komputasi**: BLAKE2 didesain lebih cepat dari MD5 pada software modern dan umumnya lebih cepat dari SHA-2 pada kebanyakan platform tanpa akselerasi hardware SHA khusus.
9. **Dampak memori**: state kecil, cocok untuk hashing single-shot pendek (dua public key 32+32 byte) tanpa kebutuhan streaming besar.
10. **Trade-off**: pemakaian sebagai KDF ad hoc (CR-003 — satu pemanggilan BLAKE2s, bukan konstruksi HKDF resmi extract-then-expand) lebih sederhana tapi secara teoretis kurang fleksibel dibanding HKDF standar; dinilai dapat diterima karena input (secret identitas) sudah berentropi tinggi dan hanya satu context string per tujuan.
11. **Alternatif dipertimbangkan**: SHA-256 (`fips180-4`); SHA3-256 (`fips202`).
12. **Alasan tidak dipilih (ringkas)**: performa software BLAKE2 umumnya lebih unggul dari SHA-2 pada CPU tanpa akselerasi khusus, dan BLAKE2 sudah terintegrasi bawaan sebagai hash pada pola Noise yang dipilih; SHA-3/Keccak dirancang untuk ketahanan struktural berbeda (sponge construction) dengan performa software CPU umum yang secara historis kalah dari BLAKE2 tanpa akselerasi hardware SHA-3 khusus. Detail di `05_CRYPTO_ALTERNATIVE_COMPARISON.md` §4.
13. **Keterbatasan**: pemakaian sebagai hash internal Noise (transcript hash + HKDF, CR-009/CR-010) TIDAK terverifikasi langsung dari source aplikasi — murni inferensi dari nama pattern (confidence LOW); perbandingan fingerprint pada `transport/lan.rs` memakai operator `<` bawaan `&str` yang byte-wise dan non-constant-time (CR-029) — risiko dinilai rendah karena kedua fingerprint adalah data publik, namun bukan best practice ideal.
14. **Asumsi penggunaan aman**: context string domain-separation harus tetap unik dan tidak pernah dipakai ulang untuk tujuan lain — bila pengembangan mendatang menambah pemakaian BLAKE2s baru tanpa context string baru, risiko cross-protocol collision antar-turunan meningkat.
15. **Risiko implementasi**: tidak ada risiko implementasi signifikan tambahan di luar poin 13; ketergantungan pada `snow` untuk peran hash-internal Noise berarti kelemahan di sana (bila ada) tidak terdeteksi dari audit source AKSARA sendiri.

---

## CORE-5 — Argon2id

Evidence: CR-014, plus duplikasi CR-024, CR-033.

1. **Masalah**: passphrase manusia memiliki entropi rendah — dibutuhkan KDF yang mahal secara komputasi DAN memori agar brute-force offline (khususnya dengan hardware paralel khusus ASIC/GPU/FPGA) menjadi tidak ekonomis untuk melindungi vault identitas AKSARA di disk.
2. **Properti keamanan**: memory-hardness — setiap upaya tebak membutuhkan RAM besar, bukan hanya waktu CPU, sehingga menghilangkan keunggulan ekonomis hardware paralel khusus dibanding CPU umum; varian `id` (hybrid Argon2i+Argon2d) memberi resistansi side-channel timing pada paruh pertama pass SEKALIGUS resistansi trade-off attack pada paruh kedua.
3. **Alasan pemilihan**: Argon2id adalah pemenang Password Hashing Competition (2015) dan direkomendasikan RFC 9106 sebagai varian yang WAJIB didukung setiap implementasi; cocok untuk kasus AKSARA (vault lokal single-pengguna, bukan server multi-tenant) di mana resistansi terhadap offline attack lebih krusial dibanding kecepatan verifikasi berulang.
4. **Standar/paper utama**: `rfc9106` (standar IETF), `biryukov2016argon2` (paper asli, EuroS&P 2016).
5. **Dukungan library**: `argon2crate` (0.5.3, RustCrypto).
6. **Kompatibilitas arsitektur**: output 32-byte langsung dipakai sebagai kunci ChaCha20Poly1305 vault (CR-014, CR-013) tanpa transformasi tambahan.
7. **Dampak ukuran paket**: kecil, pure-Rust.
8. **Dampak komputasi**: parameter AKSARA (19 MiB, t=2, p=1 — CR-014) didesain agar unlock vault memakan waktu klaim "~100 ms" pada hardware modern (komentar kode); klaim timing ini **TIDAK diverifikasi** via benchmark aktual dalam source yang diaudit (CB-087, `DOCUMENTED_ONLY`).
9. **Dampak memori**: 19 MiB RAM per operasi seal/unseal — signifikan dibanding primitif lain di codebase, namun proporsional karena hanya terjadi saat buka/simpan vault (jarang), bukan per pesan chat.
10. **Trade-off**: memory-hardness memberi keamanan lebih baik dengan konsekuensi waktu startup lebih lambat dan lonjakan RAM sesaat lebih tinggi — dinilai wajar untuk operasi non-frequent (unlock aplikasi sekali per sesi penggunaan).
11. **Alternatif dipertimbangkan**: scrypt (`rfc7914`/`percival2009scrypt`); PBKDF2 (`rfc8018`).
12. **Alasan tidak dipilih (ringkas)**: Argon2id adalah generasi lebih baru dengan analisis kriptanalisis lebih matang dan tuning side-channel-aware yang tidak dimiliki scrypt murni; PBKDF2 BUKAN memory-hard (murni iterasi HMAC berulang), jauh lebih rentan terhadap serangan paralel ASIC/GPU massal. Detail di `05_CRYPTO_ALTERNATIVE_COMPARISON.md` §5.
13. **Keterbatasan**: output Argon2id dipakai LANGSUNG sebagai kunci AEAD tanpa HKDF perantara — tidak masalah untuk kasus tunggal saat ini, tapi bukan praktik yang scalable bila di masa depan dibutuhkan multi-purpose key derivation dari passphrase yang sama; klaim performa "~100 ms" belum diverifikasi benchmark.
14. **Asumsi penggunaan aman**: salt 16-byte dibangkitkan RANDOM (OsRng, CORE-7) dan unik per pemanggilan `seal()` — bila salt tidak acak atau dipakai ulang lintas vault, resistansi terhadap precomputed/rainbow-table-style attack berkurang drastis.
15. **Risiko implementasi**: parameter Argon2id (19 MiB/t=2/p=1) adalah nilai TETAP dalam source — tidak ada mekanisme versioning/upgrade parameter untuk vault lama jika rekomendasi standar berubah di masa depan (selaras dengan tidak adanya header/versi pada layout vault, CR-019).

---

## CORE-6 — Ed25519 (identity keypair)

Evidence: CR-015, plus duplikasi CR-021, CR-031.

1. **Masalah**: AKSARA butuh identitas jangka-panjang publik yang stabil dan ringkas, direpresentasikan sebagai fingerprint yang dapat diverifikasi manusia out-of-band (mis. dibacakan lewat kanal komunikasi lain).
2. **Properti keamanan (properti algoritma Ed25519/EdDSA secara umum)**: signature deterministic (tidak membutuhkan RNG saat proses signing → aman dari kegagalan RNG saat signing, berbeda dengan insiden historis pada skema ECDSA nondeterministic); ketahanan tinggi terhadap kesalahan implementasi dibanding ECDSA klasik; verifikasi cepat dan mendukung batch verification. **Catatan penting**: properti ini adalah properti algoritma Ed25519 secara umum — grep menyeluruh pada `src/identity/*.rs` menunjukkan TIDAK ADA pemanggilan `sign()`/`verify()`/`Signature` (CB-084) — AKSARA saat ini hanya men-generate dan menyimpan keypair Ed25519 (CR-015), belum memanfaatkan operasi tanda tangannya.
3. **Alasan pemilihan**: Ed25519 dipilih sebagai identity key yang SENGAJA DIPISAHKAN dari X25519 (kunci DH Noise, CORE-2) karena keduanya memakai ruang skalar berbeda meski berbagi kurva dasar (komentar kode, CB-062) — pemisahan ini selaras dengan praktik yang direkomendasikan (hindari satu keypair untuk dua tujuan berbeda: signing dan key-agreement).
4. **Standar/paper utama**: `rfc8032` (standar IETF EdDSA), `bernstein2012ed25519` (paper asli), `fips186-5`/`sp800-186` (adopsi resmi NIST atas Ed25519).
5. **Dukungan library**: `ed25519dalekcrate` (2.2.0).
6. **Kompatibilitas arsitektur**: public key 32-byte dipakai langsung sebagai komponen fingerprint (bersama `noise_pub`, CR-002) dan invite code base64 (CR-005).
7-9. **Dampak paket/komputasi/memori**: pola identik dengan CORE-2 (berbagi dependency `curve25519-dalek`) — minimal, karena hanya dipakai generate + simpan + ekspor byte, TANPA operasi sign/verify berulang yang teraudit.
10. **Trade-off**: memakai dua keypair terpisah (Ed25519 + X25519) menggandakan key material yang harus dilindungi dibanding skema hipotetis satu-keypair-untuk-semua — trade-off ini sengaja diambil untuk menghindari risiko cross-purpose key reuse yang secara kriptografis lebih berbahaya.
11. **Alternatif dipertimbangkan**: ECDSA P-256 (`fips186-5`); RSA-2048/RSA-PSS.
12. **Alasan tidak dipilih (ringkas)**: EdDSA/Ed25519 lebih resisten terhadap kesalahan implementasi RNG (deterministic nonce) dibanding ECDSA, dan lebih cepat verifikasi; RSA memiliki ukuran kunci dan signature jauh lebih besar, tidak cocok untuk representasi fingerprint ringkas dan invite code compact yang menjadi kebutuhan UX AKSARA. Detail di `05_CRYPTO_ALTERNATIVE_COMPARISON.md` §6.
13. **Keterbatasan (paling penting untuk komponen ini)**: TIDAK ADA bukti pemakaian aktif `sign()`/`verify()` Ed25519 di manapun dalam source yang diaudit — saat ini Ed25519 di AKSARA berfungsi murni sebagai bahan fingerprint/identifier publik, BUKAN mekanisme otentikasi tanda tangan yang aktif dipakai. Ini harus dinyatakan eksplisit pada BAB pembahasan agar tidak overclaim kapabilitas keamanan yang belum diverifikasi terpakai.
14. **Asumsi penggunaan aman**: jika di masa depan sign/verify diaktifkan, asumsi standar EdDSA berlaku — keamanan bergantung pada private key tidak bocor (nonce reuse otomatis dihindari oleh desain deterministic Ed25519 selama private key tetap rahasia).
15. **Risiko implementasi**: karena fitur signing belum dipakai, tidak ada risiko implementasi sign/verify untuk dinilai saat ini; risiko yang ada murni pada sisi penyimpanan kunci, yang sudah tertangani lewat `ZeroizeOnDrop` (CB-070).

---

## CORE-7 — OsRng (`rand::rngs::OsRng`, sumber entropi OS)

Evidence: CR-004, CR-017, plus duplikasi CR-012, CR-023, CR-036.

1. **Masalah**: hampir seluruh primitif kriptografi AKSARA (key generation, salt Argon2id, nonce ChaCha20Poly1305) membutuhkan sumber angka acak yang tidak dapat diprediksi penyerang.
2. **Properti keamanan**: unpredictability berbasis entropi fisik yang dikelola OS — `OsRng` membaca langsung dari CSPRNG kernel (`getrandom(2)` di Linux, `BCryptGenRandom`/`RtlGenRandom` di Windows, dsb.), bukan PRNG deterministik userspace tanpa seeding eksternal.
3. **Alasan pemilihan**: sumber entropi paling langsung dan tepercaya yang tersedia lintas-platform di ekosistem Rust, tanpa perlu implementasi CSPRNG custom yang berisiko salah desain.
4. **Standar/paper utama**: `sp800-90a` (kriteria umum desain DRBG/CSPRNG — konteks pembanding, BUKAN bukti implementasi DRBG kustom AKSARA, karena AKSARA sepenuhnya mendelegasikan ke OS).
5. **Dukungan library**: `randcrate` (`rand` 0.8.6, `rand::rngs::OsRng`).
6. **Kompatibilitas arsitektur**: dipakai seragam pada 4 titik kebutuhan acak aplikasi (keygen Ed25519, keygen X25519, salt Argon2id, nonce ChaCha20Poly1305 — CR-017) — satu primitif RNG untuk seluruh kebutuhan, tanpa RNG custom/campuran.
7-9. **Dampak paket/komputasi/memori**: negligible — `OsRng` adalah wrapper tipis tanpa state internal besar, setiap panggilan langsung ke syscall OS.
10. **Trade-off**: memanggil syscall OS setiap kali sedikit lebih lambat dibanding PRNG userspace ter-seed sekali (mis. `ChaCha20Rng`/`ThreadRng`) — namun volume pemanggilan RNG pada AKSARA sangat rendah (hanya saat keygen/seal/nonce-per-pesan, bukan hot-loop), sehingga trade-off performa ini tidak relevan secara praktis.
11. **Alternatif dipertimbangkan**: `ChaCha20Rng` (CSPRNG userspace ter-seed dari OS sekali); `ThreadRng`.
12. **Alasan tidak dipilih (ringkas)**: `ChaCha20Rng` menambah state yang harus dikelola/di-reseed dengan benar (risiko kesalahan seeding) untuk manfaat performa yang tidak dibutuhkan pada skala AKSARA; `ThreadRng` ditujukan untuk aplikasi multi-thread heavy-RNG, sementara `OsRng` langsung lebih sederhana dan lebih mudah diaudit untuk kebutuhan AKSARA yang jarang memanggil RNG. Detail di `05_CRYPTO_ALTERNATIVE_COMPARISON.md` §7.
13. **Keterbatasan**: bergantung penuh pada kualitas implementasi CSPRNG OS yang mendasarinya — di luar kendali dan cakupan audit source AKSARA sendiri; bila OS memiliki bug CSPRNG (preseden historis: insiden Debian OpenSSL 2008), AKSARA otomatis terdampak tanpa mitigasi tambahan di level aplikasi.
14. **Asumsi penggunaan aman**: OS CSPRNG sudah cukup "seeded" dengan entropi SEBELUM AKSARA memanggil `OsRng` — pada sistem baru boot atau lingkungan virtual machine tertentu, ada risiko teoretis blocking/low-entropy early-boot (dicatat sebagai catatan umum pada dokumentasi `rand` crate sendiri).
15. **Risiko implementasi**: tidak ditemukan risiko implementasi tambahan spesifik AKSARA di luar poin 13-14 — pemakaian konsisten tanpa custom seeding menghindari kelas bug tersendiri yang biasa muncul dari implementasi RNG custom.

---

## Ringkasan Lintas-Komponen

| Komponen | Confidence gabungan (dari `03_CRYPTO_INVENTORY_NORMALIZED.md`) | Catatan overclaim-risk paling kritis |
|----------|-------------------------------------------------------------|----------------------------------------|
| CORE-1 Noise_IK | MEDIUM (orkestrasi HIGH, sub-mekanisme internal LOW) | Jangan klaim identity-hiding dua arah penuh — IK hanya menyembunyikan static key initiator |
| CORE-2 X25519 | HIGH (keygen), MEDIUM (pemakaian DH internal snow) | — |
| CORE-3 ChaCha20-Poly1305 | HIGH (vault, contact store), MEDIUM (transport Noise) | Jangan klaim misuse-resistant — nonce random, bukan deterministic-safe |
| CORE-4 BLAKE2s | HIGH (fingerprint, KDF contacts), LOW (peran internal Noise) | Peran hash/HKDF Noise murni inferensi nama pattern |
| CORE-5 Argon2id | HIGH | Klaim timing "~100ms" belum dibuktikan benchmark |
| CORE-6 Ed25519 | PARTIAL (keygen HIGH, sign/verify TIDAK ADA evidence) | **Jangan klaim AKSARA memakai Ed25519 untuk tanda tangan digital aktif** |
| CORE-7 OsRng | HIGH | — |
