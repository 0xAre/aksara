# 14 — Content Pack per BAB AKSARA

Dokumen ini menyiapkan bahan substansi per BAB (TAHAP 15) untuk dipakai Codex menyusun dokumen Tugas Akhir Mata Kuliah Implementasi Kriptografi (`docs/mini-ta/00-template/Cetak_TA_rev3.docx`). Setiap subbab diisi 13 field wajib brief: (1) Tujuan, (2) Outline paragraf, (3) Kalimat topik, (4) Fakta codebase, (5) Evidence, (6) Referensi, (7) Claim ID, (8) Diagram, (9) Tabel, (10) Eksperimen, (11) Klaim yang boleh ditulis, (12) Klaim yang dilarang, (13) Status kesiapan.

**Prinsip penyusunan**: seluruh isi adalah kompresi/rujukan dari dokumen TAHAP 1-14 yang sudah diverifikasi (`01`-`13`, `references/`) — bukan penulisan naratif baru dengan klaim yang belum diaudit. Codex WAJIB memperluas menjadi prosa akademik penuh berdasarkan field ini, bukan mengarang fakta tambahan.

**Status penyelesaian sesi ini**: BAB I-IV disusun penuh (memenuhi Quality Gate poin 15 brief: "BAB I sampai BAB IV memiliki content pack"). BAB V dan BAB VI **sengaja di-stub/blocked** sesuai izin eksplisit brief ("BAB V dan BAB VI boleh menunggu data pengujian") — lihat §BAB V dan §BAB VI di bagian akhir dokumen ini.

---

## BAB I — PENDAHULUAN

### 1.1 Latar Belakang

1. **Tujuan**: Menjelaskan konteks kebutuhan komunikasi terenkripsi P2P tanpa pihak ketiga tepercaya, dan memposisikan AKSARA sebagai objek studi yang sudah terimplementasi.
2. **Outline paragraf**: (a) kebutuhan umum kerahasiaan+keaslian komunikasi digital tanpa server perantara; (b) AKSARA sebagai aplikasi chat P2P terminal serverless (Rust, Noise_IK, dua jalur transport LAN/Tor) yang sudah berjalan; (c) motivasi akademik — tugas ini menganalisis/mengevaluasi implementasi yang sudah ada, bukan merancang protokol baru.
3. **Kalimat topik**: "Komunikasi digital yang aman memerlukan jaminan kerahasiaan dan keaslian tanpa bergantung pada pihak ketiga yang tepercaya — kebutuhan yang mendasari desain protokol peer-to-peer seperti yang diimplementasikan pada AKSARA."
4. **Fakta codebase**: AKSARA — chat P2P terminal dua pihak, serverless, Rust edition 2021, Noise_IK (`snow` 0.10.0), transport LAN (mDNS+TCP) dan Tor onion service v3, vault identitas Argon2id+ChaCha20-Poly1305.
5. **Evidence**: CB-001 (`README.md:23`), CB-002 (`README.md:52-54`), CB-003/CB-004 (`Cargo.toml`).
6. **Referensi**: `noise2018` (kerangka protokol yang dipakai), `rfc8439` (AEAD yang dipakai).
7. **Claim ID**: CB-001, CB-002, CB-003, CB-004.
8. **Diagram**: FIG-01 (diagram konteks AKSARA, `11_FIGURE_MANIFEST.md`).
9. **Tabel**: TBL-03 (stack teknologi, `tables/03_tech_stack.md`).
10. **Eksperimen**: Tidak relevan pada subbab ini.
11. **Klaim yang boleh ditulis**: AKSARA adalah aplikasi chat P2P terminal terenkripsi, serverless, dua pihak, dibangun Rust, memakai Noise_IK sebagai kerangka handshake.
12. **Klaim yang dilarang**: "AKSARA 100% aman"/"tidak dapat diretas"; klaim originalitas riset setingkat skripsi/publikasi; menyamakan enkripsi dengan keamanan mutlak.
13. **Status kesiapan**: READY.

### 1.2 Rumusan Masalah

1. **Tujuan**: Menyajikan 3 rumusan masalah penelitian sesuai `09_SCOPE_AND_TEAM_PLAN.md` §2.
2. **Outline paragraf**: Satu paragraf pembuka transisi dari latar belakang, diikuti 3 poin rumusan masalah bernomor (protokol Noise_IK & verifikasi klaim keamanan; siklus hidup kunci & konsistensi dengan standar; ketahanan terhadap kelas ancaman & batasan residual).
3. **Kalimat topik**: "Berdasarkan latar belakang tersebut, penelitian ini merumuskan tiga permasalahan utama terkait implementasi protokol, manajemen kunci, dan ketahanan keamanan AKSARA."
4. **Fakta codebase**: Rumusan masalah bersumber langsung dari cakupan yang sudah diaudit (handshake Noise_IK `crypto/handshake.rs`+`session/mod.rs`; key lifecycle `identity/keypair.rs`+`vault.rs`+`contacts/mod.rs`; threat model 5 model musuh A1-A5).
5. **Evidence**: Tidak ada evidence source-level baru — rumusan masalah adalah sintesis TAHAP 8, bukan klaim implementasi baru.
6. **Referensi**: Tidak ada referensi teori baru diperlukan di subbab ini.
7. **Claim ID**: Tidak berlaku (rumusan masalah, bukan klaim faktual).
8. **Diagram**: Tidak berlaku.
9. **Tabel**: Tidak berlaku.
10. **Eksperimen**: Rumusan masalah #1 dan #3 berkorespondensi dengan EXP-02 (handshake) dan EXP-01/03/04 (ketahanan/rejection) `12_TEST_PLAN.md`.
11. **Klaim yang boleh ditulis**: 3 rumusan masalah persis seperti `09_SCOPE_AND_TEAM_PLAN.md` §2 (dapat diparafrase redaksional, substansi tidak diubah).
12. **Klaim yang dilarang**: Menambah rumusan masalah ke-4 tanpa persetujuan (brief membatasi maksimal 3).
13. **Status kesiapan**: READY.

### 1.3 Tujuan Penelitian

1. **Tujuan**: Menyajikan 3 tujuan penelitian yang berkorespondensi 1:1 dengan rumusan masalah.
2. **Outline paragraf**: 3 poin tujuan bernomor, redaksi searah kata kerja aktif ("mendokumentasikan dan menganalisis...", "menganalisis siklus hidup...", "menyusun threat model dan merancang pengujian...").
3. **Kalimat topik**: "Sejalan dengan rumusan masalah, penelitian ini memiliki tiga tujuan yang saling berkaitan sebagai satu rangkaian evaluasi protokol keamanan AKSARA."
4. **Fakta codebase**: Sama seperti 1.2 — tujuan bersumber dari cakupan TAHAP 5-7 yang sudah selesai (spesifikasi protokol, key lifecycle, threat model).
5. **Evidence**: Tidak ada evidence baru.
6. **Referensi**: Tidak ada referensi baru.
7. **Claim ID**: Tidak berlaku.
8. **Diagram**: Tidak berlaku.
9. **Tabel**: Tidak berlaku.
10. **Eksperimen**: Tujuan #3 eksplisit mencakup "merancang serta — sejauh waktu mengizinkan — menjalankan pengujian" → berkorespondensi `12_TEST_PLAN.md` (EXP-01 s.d. EXP-05).
11. **Klaim yang boleh ditulis**: 3 tujuan persis seperti `09_SCOPE_AND_TEAM_PLAN.md` §3.
12. **Klaim yang dilarang**: Menyatakan tujuan sudah "tercapai penuh" sebelum BAB V selesai (khususnya tujuan #3 yang bergantung eksperimen).
13. **Status kesiapan**: READY.

### 1.4 Manfaat Penelitian

1. **Tujuan**: Menjelaskan manfaat akademik dan praktis dari hasil analisis (bukan dari pembuatan aplikasi baru, karena AKSARA sudah ada).
2. **Outline paragraf**: (a) manfaat akademik — model dokumentasi protokol as-built untuk aplikasi P2P Rust nyata, dapat dijadikan referensi pengajaran; (b) manfaat praktis — pemetaan kesenjangan (zeroization, rotasi kunci) berguna sebagai basis pengembangan lanjutan AKSARA (di luar scope mini-TA, tapi manfaat tidak langsung).
3. **Kalimat topik**: "Penelitian ini memberikan manfaat baik dari sisi akademik sebagai studi kasus implementasi kriptografi terapan, maupun dari sisi praktis sebagai peta kesenjangan keamanan yang dapat menjadi rujukan pengembangan AKSARA selanjutnya."
4. **Fakta codebase**: Merujuk temuan kesenjangan yang sudah terdokumentasi (T1-T7 threat model, kesenjangan zeroization `07_KEY_LIFECYCLE.md` §7.2) sebagai basis manfaat praktis — bukan klaim manfaat yang dibesar-besarkan.
5. **Evidence**: T1-T7 (`08_THREAT_MODEL.md` §6), §7.2 (`07_KEY_LIFECYCLE.md`).
6. **Referensi**: Tidak ada referensi baru.
7. **Claim ID**: Tidak berlaku (bagian naratif manfaat, bukan klaim teknis baru).
8. **Diagram**: Tidak berlaku.
9. **Tabel**: TBL-09 (threat model) sebagai rujukan manfaat praktis.
10. **Eksperimen**: Tidak berlaku.
11. **Klaim yang boleh ditulis**: Penelitian memberi peta kesenjangan keamanan deskriptif berbasis evidence source-level, bukan rekomendasi remediasi yang sudah diimplementasikan.
12. **Klaim yang dilarang**: Mengklaim penelitian ini "memperbaiki" kesenjangan yang ditemukan (di luar scope, sifatnya deskriptif per `09_SCOPE_AND_TEAM_PLAN.md` §5 poin 7).
13. **Status kesiapan**: READY.

### 1.5 Batasan Masalah

1. **Tujuan**: Menyajikan batasan penelitian secara eksplisit agar scope tidak overclaim.
2. **Outline paragraf**: Daftar 9 batasan sesuai `09_SCOPE_AND_TEAM_PLAN.md` §5 (tidak menilai keamanan dependency crate, tidak menilai CSPRNG OS, tidak pembuktian formal, tidak side-channel fisik, tidak DoS skala luas, tidak multi-device, bukan proyek remediasi, transport LAN/Tor sebagai konteks bukan objek primer, klaim performa hanya dari benchmark aktual).
3. **Kalimat topik**: "Untuk menjaga penelitian tetap proporsional dengan cakupan tugas mata kuliah, sejumlah batasan eksplisit ditetapkan pada aspek yang tidak dinilai dalam analisis ini."
4. **Fakta codebase**: Batasan diturunkan langsung dari `08_THREAT_MODEL.md` §5 (Batasan Cakupan) yang sudah menjadi bagian evidence terverifikasi.
5. **Evidence**: `08_THREAT_MODEL.md` §5 (poin 1-6).
6. **Referensi**: Tidak ada referensi baru.
7. **Claim ID**: Tidak berlaku.
8. **Diagram**: Tidak berlaku.
9. **Tabel**: Tidak berlaku.
10. **Eksperimen**: Batasan poin 9 (`09_SCOPE_AND_TEAM_PLAN.md` §5) langsung terkait status `WAITING_FOR_EXPERIMENT` seluruh `12_TEST_PLAN.md`.
11. **Klaim yang boleh ditulis**: 9 batasan persis seperti `09_SCOPE_AND_TEAM_PLAN.md` §5.
12. **Klaim yang dilarang**: Mengurangi/menghapus batasan manapun tanpa alasan terdokumentasi — batasan ini adalah kontrol anti-overclaim, bukan formalitas.
13. **Status kesiapan**: READY.

### 1.6 Sistematika Penulisan

1. **Tujuan**: Memberi peta ringkas isi BAB I-VI untuk pembaca.
2. **Outline paragraf**: Satu paragraf naratif singkat merangkum isi tiap BAB (I pendahuluan, II kajian pustaka, III metodologi, IV perancangan+implementasi, V pengujian+analisis, VI penutup).
3. **Kalimat topik**: "Sistematika penulisan laporan ini disusun dalam enam bab yang saling berkaitan, dimulai dari pendahuluan hingga penutup."
4. **Fakta codebase**: Tidak ada — subbab murni struktural/navigasi dokumen.
5. **Evidence**: Tidak berlaku.
6. **Referensi**: Tidak berlaku.
7. **Claim ID**: Tidak berlaku.
8. **Diagram**: Tidak berlaku.
9. **Tabel**: Tidak berlaku.
10. **Eksperimen**: Tidak berlaku.
11. **Klaim yang boleh ditulis**: Deskripsi ringkas isi tiap BAB sesuai struktur dokumen ini.
12. **Klaim yang dilarang**: Tidak ada risiko overclaim pada subbab struktural ini.
13. **Status kesiapan**: READY.

---

## BAB II — KAJIAN PUSTAKA

Brief mewajibkan BAB II menekankan teori: confidentiality, integrity, authenticity, AEAD, MAC, hashing, key agreement, KDF, digital identity, nonce, replay protection, key management, dan primitif yang dipakai AKSARA. Struktur di bawah memetakan seluruh topik wajib tersebut ke subbab konkret, plus subbab related work (TAHAP 10).

### 2.1 Konsep Dasar Keamanan Informasi (Confidentiality, Integrity, Authenticity)

1. **Tujuan**: Menjelaskan tiga properti keamanan dasar (CIA triad relevan-kripto) sebagai kerangka evaluasi seluruh primitif AKSARA.
2. **Outline paragraf**: (a) definisi confidentiality/integrity/authenticity secara teoretis umum (dengan sitasi standar); (b) bagaimana ketiganya dipetakan ke primitif AKSARA (ChaCha20-Poly1305 untuk confidentiality+integrity via AEAD, verifikasi static-key Noise_IK untuk authenticity).
3. **Kalimat topik**: "Tiga properti keamanan mendasar — kerahasiaan, integritas, dan keaslian — menjadi kerangka acuan untuk mengevaluasi setiap primitif kriptografi yang diimplementasikan pada AKSARA."
4. **Fakta codebase**: AEAD (CORE-3) memberi confidentiality+integrity; verifikasi static-key Noise_IK (CR-027, fail-closed) memberi authenticity untuk kontak dikenal.
5. **Evidence**: CR-001/008/013 (AEAD), `session/mod.rs:145-151` (fail-closed identity check).
6. **Referensi**: `rfc8439` (AEAD ChaCha20-Poly1305), `noise2018` (autentikasi Noise_IK).
7. **Claim ID**: CR-001, CR-008, CR-013, CR-027.
8. **Diagram**: Tidak ada diagram khusus — konsep teoretis, dibahas naratif.
9. **Tabel**: TBL-02 (kebutuhan non-fungsional NFR-01/02/03).
10. **Eksperimen**: EXP-01/03 (confidentiality+integrity via correctness/rejection test).
11. **Klaim yang boleh ditulis**: AKSARA memenuhi confidentiality+integrity via AEAD pada 3 konteks; authenticity terpenuhi PARSIAL (hanya kontak dikenal, lihat T1 threat model).
12. **Klaim yang dilarang**: Menyamakan enkripsi dengan autentikasi (larangan eksplisit `AGENTS.md` #19); menyatakan authenticity terpenuhi penuh tanpa catatan trust-on-first-use.
13. **Status kesiapan**: READY.

### 2.2 AEAD (Authenticated Encryption with Associated Data)

1. **Tujuan**: Menjelaskan konsep AEAD secara teoretis dan implementasinya via ChaCha20-Poly1305 di AKSARA.
2. **Outline paragraf**: (a) definisi AEAD, komponen (enkripsi+tag autentikasi, opsional AAD); (b) ChaCha20-Poly1305 sebagai instansiasi AEAD; (c) tiga konteks pemakaian AKSARA (vault, contact store, transport Noise) dan ketiadaan AAD pada seluruhnya.
3. **Kalimat topik**: "Authenticated Encryption with Associated Data (AEAD) menggabungkan kerahasiaan dan integritas dalam satu konstruksi kriptografi, sebagaimana diimplementasikan AKSARA melalui ChaCha20-Poly1305 pada tiga konteks berbeda."
4. **Fakta codebase**: CORE-3, 3 instance (CR-001 contact store, CR-008 transport Noise, CR-013 vault); nonce 96-bit, tag 128-bit; TIDAK memakai AAD di ketiganya.
5. **Evidence**: CR-001, CR-008, CR-013, CR-018.
6. **Referensi**: `rfc8439`, `bernstein2008chacha`, `bernstein2005poly1305`.
7. **Claim ID**: CR-001, CR-008, CR-013, CR-018.
8. **Diagram**: FIG-03 (arsitektur kriptografi CORE-1..7, `11_FIGURE_MANIFEST.md`).
9. **Tabel**: TBL-04 (inventarisasi primitif — baris CORE-3), TBL-05 (justifikasi — baris CORE-3), TBL-06 (perbandingan AES-GCM/GCM-SIV).
10. **Eksperimen**: EXP-01 (vault), EXP-03 (transport), EXP-04 (contact store) — encryption-decryption consistency; EXP-05 (ciphertext expansion).
11. **Klaim yang boleh ditulis**: AKSARA memakai ChaCha20-Poly1305 konsisten pada 3 konteks; TIDAK misuse-resistant; TIDAK memakai AAD.
12. **Klaim yang dilarang**: Menyatakan ChaCha20-Poly1305 "aman terhadap nonce reuse" (bertentangan fakta — TIDAK misuse-resistant).
13. **Status kesiapan**: READY.

### 2.3 MAC dan Fungsi Hash

1. **Tujuan**: Menjelaskan konsep MAC (via tag Poly1305 dalam AEAD) dan fungsi hash (BLAKE2s) secara teoretis, dipetakan ke pemakaian AKSARA.
2. **Outline paragraf**: (a) definisi MAC sebagai autentikasi pesan, Poly1305 sebagai komponen tag dalam AEAD (bukan MAC berdiri sendiri di AKSARA); (b) definisi fungsi hash (collision/preimage resistance), BLAKE2s sebagai keluarga BLAKE2 dioptimalkan 32-bit; (c) 3 peran BLAKE2s di AKSARA (fingerprint, KDF ad hoc, hash internal Noise).
3. **Kalimat topik**: "Selain enkripsi, autentikasi pesan dan fungsi hash berperan penting dalam menjamin integritas data serta membentuk identitas ringkas yang dapat diverifikasi manusia pada AKSARA."
4. **Fakta codebase**: Poly1305 sebagai bagian AEAD (bukan MAC terpisah); BLAKE2s (CORE-4) — fingerprint (CR-002), KDF contacts (CR-003), hash internal Noise (CR-009/010, confidence LOW).
5. **Evidence**: CR-002, CR-003, CR-009, CR-010.
6. **Referensi**: `bernstein2005poly1305` (Poly1305), `rfc7693`/`aumasson2013blake2` (BLAKE2s).
7. **Claim ID**: CR-002, CR-003, CR-009, CR-010.
8. **Diagram**: FIG-03 (arsitektur kriptografi).
9. **Tabel**: TBL-04 (baris CORE-4), TBL-05, TBL-06 (perbandingan SHA-256/SHA3-256).
10. **Eksperimen**: EXP-04 (fingerprint binding, KDF consistency).
11. **Klaim yang boleh ditulis**: BLAKE2s dipakai 3 peran berbeda; peran hash-internal-Noise confidence LOW (inferensi nama pattern, bukan verifikasi langsung).
12. **Klaim yang dilarang**: Menyamakan hashing dengan perlindungan integritas tanpa konteks (larangan `AGENTS.md` #20) — BLAKE2s sebagai fingerprint TIDAK memberi integritas pesan, hanya identifier.
13. **Status kesiapan**: READY.

### 2.4 Key Agreement (Diffie-Hellman / ECDH)

1. **Tujuan**: Menjelaskan konsep key agreement dan X25519 (Curve25519 ECDH) sebagai instansiasi yang dipakai AKSARA dalam Noise_IK.
2. **Outline paragraf**: (a) definisi key agreement, computational Diffie-Hellman problem; (b) X25519 sebagai ECDH atas Curve25519, properti twist-secure; (c) token DH (`es/ss/ee/se`) dalam handshake Noise_IK AKSARA.
3. **Kalimat topik**: "Key agreement memungkinkan dua pihak menyepakati rahasia bersama melalui kanal publik tanpa pra-share kunci, sebagaimana diimplementasikan AKSARA melalui X25519 dalam empat token Diffie-Hellman pola Noise_IK."
4. **Fakta codebase**: CORE-2, X25519 dipakai 4 titik DH dalam handshake (CR-007), key generation/storage terpisah (CR-016).
5. **Evidence**: CR-007, CR-016, CR-022, CR-032.
6. **Referensi**: `rfc7748`, `bernstein2006curve25519`.
7. **Claim ID**: CR-007, CR-016.
8. **Diagram**: FIG-05 (sequence handshake Noise_IK, `11_FIGURE_MANIFEST.md`).
9. **Tabel**: TBL-04 (baris CORE-2), TBL-06 (perbandingan P-256/Curve448).
10. **Eksperimen**: EXP-02 (key agreement consistency).
11. **Klaim yang boleh ditulis**: X25519 dipakai sebagai static+ephemeral key dalam 4 token DH pola `IK`; operasi DH aktual internal `snow` (confidence MEDIUM, bukan diverifikasi langsung dari source aplikasi).
12. **Klaim yang dilarang**: Mengklaim implementasi X25519 sendiri diaudit AKSARA (operasi DH sepenuhnya di dalam crate `snow`, di luar cakupan audit source AKSARA).
13. **Status kesiapan**: READY.

### 2.5 Key Derivation Function (KDF)

1. **Tujuan**: Menjelaskan konsep KDF umum dan dua instansiasi berbeda di AKSARA (Argon2id untuk passphrase, BLAKE2s ad hoc untuk contacts-key).
2. **Outline paragraf**: (a) definisi KDF, perbedaan KDF generik (mis. HKDF) vs password-based KDF (memory-hard); (b) Argon2id sebagai password-based KDF vault; (c) BLAKE2s sebagai KDF ad hoc single-shot untuk contacts-key (bukan HKDF standar) — dibandingkan trade-off keduanya.
3. **Kalimat topik**: "Fungsi derivasi kunci mengubah rahasia berentropi rendah atau tinggi menjadi kunci kriptografi yang sesuai, dengan AKSARA menerapkan dua pendekatan berbeda bergantung sumber entropi input."
4. **Fakta codebase**: Argon2id (CORE-5, CR-014, m=19MiB/t=2/p=1) untuk vault; BLAKE2s single-shot (CR-003) untuk contacts-key dari identity secret (bukan passphrase).
5. **Evidence**: CR-014, CR-003.
6. **Referensi**: `rfc9106`/`biryukov2016argon2` (Argon2id), `rfc7693` (BLAKE2s sebagai basis KDF ad hoc).
7. **Claim ID**: CR-014, CR-003.
8. **Diagram**: FIG-06 (state siklus hidup kunci, `11_FIGURE_MANIFEST.md`).
9. **Tabel**: TBL-04 (baris CORE-5), TBL-05, TBL-06 (perbandingan scrypt/PBKDF2), TBL-08 (lifecycle kunci).
10. **Eksperimen**: EXP-01 (KDF consistency Argon2id), EXP-04 (KDF consistency BLAKE2s), EXP-05 (benchmark timing Argon2id).
11. **Klaim yang boleh ditulis**: Argon2id dipakai untuk passphrase (memory-hard, 19 MiB); BLAKE2s dipakai KDF ad hoc untuk secret berentropi tinggi (bukan HKDF standar, dinilai dapat diterima untuk kasus tunggal ini).
12. **Klaim yang dilarang**: Mengutip klaim timing "~100ms" Argon2id sebagai fakta terukur sebelum EXP-05 benar-benar dijalankan (`DOCUMENTED_ONLY`, CB-087).
13. **Status kesiapan**: READY (naratif teori) — bagian kuantitatif timing tetap `WAITING_FOR_EXPERIMENT`.

### 2.6 Identitas Digital dan Digital Signature

1. **Tujuan**: Menjelaskan konsep identitas kriptografis dan digital signature (EdDSA/Ed25519), sekaligus menegaskan status pemakaian Ed25519 di AKSARA (fingerprint-only).
2. **Outline paragraf**: (a) konsep identitas digital berbasis keypair asimetris; (b) EdDSA/Ed25519 sebagai algoritma signature deterministic; (c) **penegasan eksplisit**: AKSARA hanya men-generate/menyimpan Ed25519, TIDAK ADA sign()/verify() aktif — fungsi identitas sebenarnya dijalankan lewat fingerprint+verifikasi static-key Noise_IK.
3. **Kalimat topik**: "Identitas digital pada sistem P2P umumnya dibangun di atas pasangan kunci asimetris, namun pada AKSARA properti tanda tangan digital Ed25519 belum dimanfaatkan secara aktif — identitas direpresentasikan melalui fingerprint dan diverifikasi melalui handshake Noise_IK."
4. **Fakta codebase**: Ed25519 (CORE-6) — CR-015 hanya generate/simpan; grep `sign()`/`verify()`/`Signature` di `identity/*.rs` nihil (CB-084).
5. **Evidence**: CR-015, CB-084.
6. **Referensi**: `rfc8032`, `bernstein2012ed25519`, `fips186-5`.
7. **Claim ID**: CR-015, CB-084.
8. **Diagram**: FIG-03 (arsitektur kriptografi, CORE-6 ditandai partial).
9. **Tabel**: TBL-04 (baris CORE-6, confidence PARTIAL), TBL-06 (perbandingan ECDSA/RSA).
10. **Eksperimen**: Tidak ada eksperimen langsung menguji sign/verify (fitur tidak dipakai); EXP-04 menguji fingerprint yang memakai public key Ed25519.
11. **Klaim yang boleh ditulis**: AKSARA men-generate dan menyimpan keypair Ed25519; public key dipakai sebagai bahan fingerprint. **WAJIB** dinyatakan eksplisit: TIDAK ADA operasi sign/verify aktif.
12. **Klaim yang dilarang**: **KRITIS** — jangan menyatakan AKSARA "menggunakan Ed25519 untuk tanda tangan digital" atau mengklaim properti keamanan EdDSA (non-repudiation, dsb.) sebagai kapabilitas AKSARA yang aktif dipakai (mandat berulang `SESSION_2_HANDOFF.md`, `04_CRYPTOGRAPHIC_JUSTIFICATION.md` CORE-6).
13. **Status kesiapan**: READY.

### 2.7 Nonce dan Replay Protection

1. **Tujuan**: Menjelaskan konsep nonce dalam AEAD dan konsep replay protection secara teoretis, dipetakan ke kondisi aktual AKSARA (nonce ada, replay protection tidak ditemukan).
2. **Outline paragraf**: (a) definisi nonce dan mengapa keunikan nonce kritis pada AEAD; (b) strategi nonce AKSARA (random 96-bit per operasi, bukan counter); (c) definisi replay protection (mis. sequence number/timestamp check) dan **penegasan**: tidak ditemukan mekanisme replay-protection eksplisit di source AKSARA.
3. **Kalimat topik**: "Keunikan nonce merupakan prasyarat keamanan AEAD, sementara mekanisme replay protection — meskipun umum pada protokol pesan aman — tidak ditemukan diimplementasikan secara eksplisit pada AKSARA."
4. **Fakta codebase**: Nonce random `OsRng` pada vault (CR-018) dan contact store (CR-004); nonce transport Noise dikelola internal `snow` (tidak terlihat dari source aplikasi). Tidak ada sequence number/timestamp check ditemukan pada `session/mod.rs`.
5. **Evidence**: CR-004, CR-018.
6. **Referensi**: `rfc8439` (spesifikasi nonce 96-bit ChaCha20-Poly1305).
7. **Claim ID**: CR-004, CR-018.
8. **Diagram**: Tidak ada diagram khusus.
9. **Tabel**: TBL-04, TBL-07 (format paket — tidak ada field sequence number).
10. **Eksperimen**: EXP-01 (`vault_looks_random`, nonce handling); replay rejection eksplisit **N/A** pada `12_TEST_PLAN.md` §0.
11. **Klaim yang boleh ditulis**: Nonce dibangkitkan acak (bukan counter) pada vault/contact store; TIDAK ditemukan mekanisme replay-protection eksplisit di source yang diaudit.
12. **Klaim yang dilarang**: Menyatakan replay protection tersedia hanya karena ada timestamp (larangan eksplisit `AGENTS.md` #22) — AKSARA bahkan tidak terverifikasi memakai timestamp untuk tujuan ini.
13. **Status kesiapan**: READY.

### 2.8 Manajemen Kunci (Key Management)

1. **Tujuan**: Menjelaskan konsep lifecycle manajemen kunci (generation-storage-usage-rotation-destruction) sebagai kerangka evaluasi, dipetakan ke `07_KEY_LIFECYCLE.md`.
2. **Outline paragraf**: (a) konsep umum lifecycle kunci kriptografi; (b) penerapan tiap fase pada AKSARA (generation via OsRng, storage vault terenkripsi, usage per konteks, TIDAK ADA rotasi/revokasi, zeroization parsial).
3. **Kalimat topik**: "Pengelolaan kunci kriptografi sepanjang siklus hidupnya — mulai dari pembangkitan hingga penghapusan — menentukan ketahanan keseluruhan sistem terhadap kompromi, sebuah aspek yang dievaluasi menyeluruh pada AKSARA."
4. **Fakta codebase**: Seluruh isi `07_KEY_LIFECYCLE.md` — generation seragam OsRng, vault 108-byte, TIDAK ADA rotasi/revokasi, zeroization kuat pada tipe kunci inti tapi lemah pada boundary fungsi.
5. **Evidence**: CR-004, CR-013, CR-014, CR-017, CB-083 (tidak ada rotasi).
6. **Referensi**: `sp800-90a` (CSPRNG), `rfc9106` (Argon2id).
7. **Claim ID**: CR-004, CR-013, CR-014, CR-017, CB-083.
8. **Diagram**: FIG-06 (state siklus hidup kunci).
9. **Tabel**: TBL-08 (lifecycle kunci, lengkap).
10. **Eksperimen**: EXP-01, EXP-05 (vault/Argon2id).
11. **Klaim yang boleh ditulis**: Seluruh klaim `07_KEY_LIFECYCLE.md` yang sudah berstatus HIGH/PARTIAL confidence — termasuk ketiadaan rotasi kunci sebagai temuan HIGH confidence (bukan dugaan).
12. **Klaim yang dilarang**: Menyatakan forward secrecy tersedia tanpa menganalisis lifecycle kunci penuh (larangan `AGENTS.md` #21) — forward secrecy AKSARA `DOCUMENTED_ONLY`, bukan `CONFIRMED`.
13. **Status kesiapan**: READY.

### 2.9 Noise Protocol Framework dan Pola Handshake `IK`

1. **Tujuan**: Menjelaskan Noise Protocol Framework secara umum dan pola `IK` khususnya, sebagai dasar teori CORE-1.
2. **Outline paragraf**: (a) Noise Protocol Framework sebagai kerangka modular untuk membangun protokol handshake AEAD; (b) notasi token (`e, s, es, ss, ee, se`) dan pola `IK` spesifik (initiator tahu static key responder di awal); (c) posisi `Noise_IK_25519_ChaChaPoly_BLAKE2s` sebagai instansiasi konkret AKSARA.
3. **Kalimat topik**: "Noise Protocol Framework menyediakan kerangka modular untuk merancang protokol handshake yang saling terautentikasi dan rahasia, dari mana AKSARA mengadopsi pola `IK` sebagai basis pembentukan sesi amannya."
4. **Fakta codebase**: `Noise_IK_25519_ChaChaPoly_BLAKE2s` via `snow` 0.10.0; alur 2 pesan (`e,es,s,ss` / `e,ee,se`).
5. **Evidence**: CR-007..011, `crypto/handshake.rs:3-21`.
6. **Referensi**: `noise2018`.
7. **Claim ID**: CR-007, CR-008, CR-009, CR-010, CR-011.
8. **Diagram**: FIG-05 (sequence handshake Noise_IK).
9. **Tabel**: TBL-04 (baris CORE-1), TBL-05, TBL-06 (perbandingan TLS 1.3/X3DH).
10. **Eksperimen**: EXP-02.
11. **Klaim yang boleh ditulis**: Deskripsi umum Noise Protocol Framework dan pola `IK` berdasarkan `noise2018`; AKSARA mengadopsi instansiasi `25519_ChaChaPoly_BLAKE2s` via `snow`.
12. **Klaim yang dilarang**: Mengklaim `snow` sudah diaudit keamanan formal (dokumentasi resminya menyatakan sebaliknya, self-declared).
13. **Status kesiapan**: READY.

### 2.10 Penelitian Terkait

1. **Tujuan**: Memposisikan AKSARA terhadap 7 sistem/penelitian sejenis dan menyajikan 5 gap (G1-G5).
2. **Outline paragraf**: (a) pengantar tiga sumbu perbandingan (kerangka kriptografi, manajemen kunci, arsitektur jaringan); (b) 7 subbagian singkat per penelitian terkait (Noise Explorer, Signal, WireGuard, OTR, Matrix, Briar, Tox); (c) penutup gap G1-G5 dengan pembingkaian "belum ditemukan pada sumber ditinjau".
3. **Kalimat topik**: "Untuk memposisikan kontribusi analisis ini, AKSARA dibandingkan dengan tujuh sistem dan penelitian sejenis pada tiga sumbu: kerangka kriptografi, manajemen kunci, dan arsitektur jaringan."
4. **Fakta codebase**: Seluruh isi `10_RELATED_WORK_AND_GAP.md` §2-3 — reproduksi langsung, tidak diubah substansinya.
5. **Evidence**: Seluruh evidence AKSARA yang dirujuk `10_RELATED_WORK_AND_GAP.md` (T7 threat model, `07_KEY_LIFECYCLE.md` §6, dst.).
6. **Referensi**: `kobeissi2019noiseexplorer`, `cohngordon2020signal`, `donenfeld2017wireguard`, `borisov2004otr`, `albrecht2024matrix`, `briarspec`, `toxspec`.
7. **Claim ID**: Merujuk T7 (`08_THREAT_MODEL.md`), tidak ada CR/CB baru.
8. **Diagram**: Tidak ada diagram khusus (tabel perbandingan cukup).
9. **Tabel**: TBL-10 (penelitian terkait, lengkap).
10. **Eksperimen**: G3 (evaluasi overhead) berkorespondensi `12_TEST_PLAN.md` EXP-05.
11. **Klaim yang boleh ditulis**: 5 gap G1-G5 persis seperti `10_RELATED_WORK_AND_GAP.md` §3, dengan pembingkaian "belum ditemukan pada sumber ditinjau".
12. **Klaim yang dilarang**: Mengklaim "belum pernah diteliti" tanpa systematic evidence (larangan eksplisit brief TAHAP 10); mengklaim gap sebagai kontribusi orisinal berskala publikasi ilmiah.
13. **Status kesiapan**: READY.

---

## BAB III — METODOLOGI PENELITIAN

### 3.1 Jenis Penelitian

1. **Tujuan**: Mengklasifikasikan jenis penelitian (deskriptif-evaluatif berbasis audit source-code, bukan eksperimental murni/kuantitatif penuh).
2. **Outline paragraf**: Penelitian bersifat studi kasus (case study) terhadap implementasi nyata, memakai metode audit source-level dan evaluasi deskriptif terhadap threat model, dilengkapi eksperimen correctness/performa terbatas.
3. **Kalimat topik**: "Penelitian ini merupakan studi kasus deskriptif-evaluatif terhadap implementasi kriptografi nyata pada aplikasi AKSARA, dikombinasikan dengan pengujian correctness dan benchmark performa terbatas."
4. **Fakta codebase**: Metode yang benar-benar dipakai TAHAP 1-14: audit source-level (grep+baca kode), sintesis evidence JSON terverifikasi 16-agent, perbandingan literatur (`you-search`), rencana pengujian berbasis test suite existing.
5. **Evidence**: Metodologi TAHAP 1-3 (`PROGRESS.md` §Data mentah TAHAP 2+3).
6. **Referensi**: Tidak ada referensi metodologi penelitian formal dikutip (di luar scope brief).
7. **Claim ID**: Tidak berlaku.
8. **Diagram**: Tidak berlaku.
9. **Tabel**: Tidak berlaku.
10. **Eksperimen**: Tidak berlaku (deskripsi metode, bukan hasil).
11. **Klaim yang boleh ditulis**: Penelitian adalah studi kasus deskriptif-evaluatif berbasis audit source-level dan evidence terverifikasi, bukan penelitian eksperimental murni skala besar.
12. **Klaim yang dilarang**: Mengklaim metodologi setingkat systematic literature review formal (7 sumber dipilih terarah, bukan SLR penuh, sesuai `10_RELATED_WORK_AND_GAP.md`).
13. **Status kesiapan**: READY.

### 3.2 Objek Penelitian

1. **Tujuan**: Mendeskripsikan AKSARA sebagai objek penelitian — versi, struktur modul, cakupan yang dianalisis.
2. **Outline paragraf**: (a) identitas AKSARA (nama, versi v0.2.1, commit `450d484`); (b) struktur modul (`identity`, `crypto`, `transport`, `session`, `contacts`, `tui`); (c) fokus utama penelitian (CORE-1..7, key lifecycle, threat model — bukan seluruh codebase).
3. **Kalimat topik**: "Objek penelitian ini adalah AKSARA, aplikasi chat peer-to-peer terminal serverless versi 0.2.1, dengan fokus analisis pada rangkaian protokol Noise_IK, siklus hidup kunci, dan model ancaman yang menyertainya."
4. **Fakta codebase**: v0.2.1, commit `450d484`, 46 test passing (per `PROJECT_MEMORY.md`, jangan diklaim "baru diverifikasi" tanpa rerun), 7 modul utama.
5. **Evidence**: `PROJECT_MEMORY.md` §Status Stabil, `01_CODEBASE_AUDIT.md` §Cakupan Evidence.
6. **Referensi**: Tidak berlaku.
7. **Claim ID**: Tidak ada ID baru — rujukan ke cakupan modul TAHAP 2.
8. **Diagram**: FIG-02 (arsitektur komponen).
9. **Tabel**: TBL-03 (stack teknologi), TBL-13 (pembagian tugas per modul).
10. **Eksperimen**: Tidak berlaku.
11. **Klaim yang boleh ditulis**: AKSARA v0.2.1, commit `450d484`, cakupan modul persis seperti `01_CODEBASE_AUDIT.md` §Cakupan Evidence.
12. **Klaim yang dilarang**: Mengklaim "46 test passing dan Clippy bersih" sebagai fakta yang baru diverifikasi ulang pada sesi ini (`AGENTS.md`: "jangan mempresentasikan ini sebagai baru diverifikasi kecuali dijalankan ulang").
13. **Status kesiapan**: READY.

### 3.3 Tahapan Penelitian

1. **Tujuan**: Menjelaskan alur kerja penelitian dari audit hingga pengujian sebagai metodologi yang dapat direproduksi.
2. **Outline paragraf**: Alur bernomor — (1) audit codebase & kripto berbasis evidence 16-agent verifikasi silang, (2) normalisasi & justifikasi algoritma, (3) penyusunan spesifikasi protokol/key lifecycle/threat model as-built, (4) perancangan rencana pengujian, (5) (bila sempat) eksekusi pengujian dan analisis.
3. **Kalimat topik**: "Penelitian ini dilaksanakan melalui lima tahapan berurutan, dimulai dari audit source-level hingga — sejauh kuota mengizinkan — eksekusi pengujian empiris."
4. **Fakta codebase**: Alur TAHAP 1-14 aktual yang sudah dijalankan (audit 16-agent workflow `wf_949a0769-7ab`, TAHAP 4 justifikasi 7 komponen, TAHAP 5-7 spesifikasi, TAHAP 13 rencana pengujian 5 kelompok).
5. **Evidence**: `PROGRESS.md` seluruh tabel status TAHAP.
6. **Referensi**: Tidak berlaku.
7. **Claim ID**: Tidak berlaku.
8. **Diagram**: Tidak berlaku (opsional: diagram alur metodologi, tidak wajib per rentang 5-8 diagram brief yang sudah terpenuhi 7 diagram).
9. **Tabel**: Tidak berlaku.
10. **Eksperimen**: Tahapan ke-5 mencakup seluruh `12_TEST_PLAN.md`.
11. **Klaim yang boleh ditulis**: Deskripsi 5 tahapan metodologi sesuai urutan TAHAP 1-17 brief yang benar-benar dijalankan.
12. **Klaim yang dilarang**: Mengklaim tahap ke-5 (eksekusi pengujian) sudah selesai — status tetap `WAITING_FOR_EXPERIMENT` per `12_TEST_PLAN.md`.
13. **Status kesiapan**: READY.

### 3.4 Lingkungan dan Alat

1. **Tujuan**: Mendokumentasikan lingkungan pengembangan/audit dan tool yang dipakai.
2. **Outline paragraf**: (a) bahasa/toolchain (Rust 1.89+, `cargo`); (b) tool audit (grep, LSP, workflow multi-agen); (c) tool diagram (Mermaid CLI via Node.js); (d) rencana lingkungan eksekusi pengujian (dicatat lengkap saat eksperimen benar-benar dijalankan, belum final sesi ini).
3. **Kalimat topik**: "Analisis dan pengujian pada penelitian ini memanfaatkan toolchain Rust standar, perkakas audit berbasis pencarian kode, dan Mermaid CLI untuk visualisasi teknis."
4. **Fakta codebase**: Rust edition 2021/`rust-version` 1.89; `mmdc` (Mermaid CLI) via Chrome sistem; build `cargo build --release` terverifikasi commit `450d484`.
5. **Evidence**: `00_TOOL_AND_MCP_INVENTORY.md`, `PROGRESS.md` §Keputusan Penting poin 1/5.
6. **Referensi**: Tidak berlaku.
7. **Claim ID**: Tidak berlaku.
8. **Diagram**: Tidak berlaku.
9. **Tabel**: TBL-03 (stack teknologi).
10. **Eksperimen**: Lingkungan eksekusi EXP-01..05 (CPU/RAM/OS) **WAJIB dicatat ulang saat eksperimen dijalankan** — belum final di sesi ini (lihat `12_TEST_PLAN.md` poin 7 tiap eksperimen).
11. **Klaim yang boleh ditulis**: Toolchain dan versi yang sudah diverifikasi TAHAP 1/12 (Rust 1.89+, `mmdc`, build commit `450d484`).
12. **Klaim yang dilarang**: Mencantumkan spesifikasi hardware eksekusi pengujian sebelum benar-benar diukur (lihat keterbatasan EXP-05).
13. **Status kesiapan**: PARTIAL — bagian toolchain READY, bagian lingkungan eksekusi pengujian `WAITING_FOR_EXPERIMENT`.

### 3.5 Rencana Pengujian (Ringkasan)

1. **Tujuan**: Menyajikan ringkasan 5 kelompok eksperimen sebagai bagian metodologi (detail penuh di BAB V setelah eksekusi).
2. **Outline paragraf**: Ringkas 5 kelompok (EXP-01 s.d. EXP-05), metrik utama, dan status `WAITING_FOR_EXPERIMENT` seragam.
3. **Kalimat topik**: "Rencana pengujian dirancang dalam lima kelompok eksperimen yang mencakup correctness, rejection, consistency, dan benchmark performa terhadap primitif kriptografi inti AKSARA."
4. **Fakta codebase**: Seluruh isi `12_TEST_PLAN.md`.
5. **Evidence**: Rujuk nama test existing per kelompok (lihat `12_TEST_PLAN.md` §EXP-01..05 poin 3).
6. **Referensi**: Tidak ada referensi baru.
7. **Claim ID**: Tidak berlaku (rencana, bukan hasil).
8. **Diagram**: Opsional — diagram topologi pengujian (belum dibuat, lihat `SESSION_5A_HANDOFF.md` poin 5).
9. **Tabel**: TBL-11 (skenario pengujian), TBL-12 (parameter evaluasi).
10. **Eksperimen**: EXP-01 s.d. EXP-05 (rujukan penuh).
11. **Klaim yang boleh ditulis**: Ringkasan rencana 5 kelompok eksperimen persis seperti `12_TEST_PLAN.md`.
12. **Klaim yang dilarang**: Menyisipkan angka hasil apa pun di subbab ini — ini BAB III (metodologi), bukan BAB V (hasil).
13. **Status kesiapan**: READY (sebagai rencana) — bukan `READY` untuk hasil, karena memang belum ada hasil.

---

## BAB IV — PERANCANGAN DAN IMPLEMENTASI

Brief menandai BAB IV sebagai **bagian inti** — dijelaskan paling rinci dari seluruh BAB.

### 4.1 Gambaran Umum Arsitektur AKSARA

1. **Tujuan**: Memberi peta arsitektur menyeluruh sebelum masuk ke detail per komponen.
2. **Outline paragraf**: (a) model P2P dua-pihak tanpa server/broker; (b) dua jalur transport (LAN-first, fallback Tor); (c) lapisan Noise_IK di atas kedua transport; (d) empat lapisan data utama (vault → identity/fingerprint → handshake → transport) sebagai satu rangkaian.
3. **Kalimat topik**: "Arsitektur AKSARA dibangun di atas empat lapisan yang saling terkait — penyimpanan identitas, pengikatan fingerprint, handshake autentikasi, dan transport terenkripsi — di atas dua kemungkinan jalur jaringan."
4. **Fakta codebase**: Model komunikasi P2P (`transport/mod.rs:1-4`), role dinamis dari perbandingan fingerprint (`role_from_fp`, `mod.rs:101-107`).
5. **Evidence**: `06_PROTOCOL_SPECIFICATION.md` §1-2.
6. **Referensi**: `noise2018`.
7. **Claim ID**: Rujuk seluruh evidence §1-2 `06_PROTOCOL_SPECIFICATION.md`.
8. **Diagram**: FIG-01 (konteks), FIG-02 (arsitektur komponen), FIG-04 (sequence proses utama).
9. **Tabel**: TBL-01 (kebutuhan fungsional), TBL-04 (primitif).
10. **Eksperimen**: Tidak langsung — konteks untuk seluruh EXP-01..05.
11. **Klaim yang boleh ditulis**: Deskripsi arsitektur 4-lapisan dan strategi LAN-first/Tor-fallback sesuai `06_PROTOCOL_SPECIFICATION.md` §1-2.
12. **Klaim yang dilarang**: Menyebut AKSARA punya server/relay pusat manapun (bertentangan fakta — serverless murni).
13. **Status kesiapan**: READY.

### 4.2 Identitas dan Manajemen Kunci

1. **Tujuan**: Menjelaskan rinci pembangkitan, penyimpanan, dan pemakaian seluruh material kunci AKSARA (isi utama BAB IV, paling detail).
2. **Outline paragraf**: (a) pembangkitan seragam via `OsRng` (4 titik); (b) layout vault 108-byte dan alur `seal()`/`unseal()`; (c) parameter Argon2id dan catatan klaim timing belum terverifikasi; (d) contacts-store key (BLAKE2s, bukan Argon2id, dan alasannya); (e) pemakaian per konteks (Ed25519 fingerprint-only vs X25519 static DH); (f) ketiadaan rotasi/revokasi; (g) status zeroization (kuat vs lemah per boundary).
3. **Kalimat topik**: "Pengelolaan kunci pada AKSARA mencakup tujuh jenis material kunci berbeda, masing-masing dengan mekanisme pembangkitan, penyimpanan, dan pembersihan memori yang terverifikasi pada tingkat kode sumber."
4. **Fakta codebase**: Seluruh isi `07_KEY_LIFECYCLE.md` §1-7 — tabel material kunci, alur seal/unseal, parameter Argon2id, contacts-key derivation, zeroization gap.
5. **Evidence**: CR-004, CR-013, CR-014, CR-015, CR-016, CR-017, CB-083, CB-087.
6. **Referensi**: `rfc9106`/`biryukov2016argon2`, `rfc8439`, `rfc7693`, `rfc8032`, `sp800-90a`.
7. **Claim ID**: CR-004, CR-013, CR-014, CR-015, CR-016, CR-017, CB-083, CB-087.
8. **Diagram**: FIG-06 (state siklus hidup kunci).
9. **Tabel**: TBL-08 (lifecycle kunci, lengkap — dipakai langsung).
10. **Eksperimen**: EXP-01 (correctness/rejection vault), EXP-05 (benchmark Argon2id).
11. **Klaim yang boleh ditulis**: Seluruh klaim `07_KEY_LIFECYCLE.md` sesuai status confidence masing-masing (HIGH/PARTIAL/DOCUMENTED_ONLY) — WAJIB mempertahankan pembedaan status ini, tidak diratakan jadi "terverifikasi" semua.
12. **Klaim yang dilarang**: Mengutip "~100ms" Argon2id sebagai fakta terukur; menyatakan zeroization "lengkap" di seluruh codebase (faktanya PARTIAL, lemah di 5 boundary yang terdaftar `07_KEY_LIFECYCLE.md` §7.2).
13. **Status kesiapan**: READY (naratif) — bagian timing tetap `WAITING_FOR_EXPERIMENT`.

### 4.3 Spesifikasi Protokol: Invite, Discovery, dan Pembentukan Koneksi

1. **Tujuan**: Menjelaskan tahap pra-handshake — pertukaran invite code dan pembentukan koneksi transport (LAN/Tor).
2. **Outline paragraf**: (a) format dan alur invite code, ketiadaan autentikasi kriptografis; (b) discovery mDNS (apa yang diiklankan/tidak); (c) orkestrasi `establish()` — strategi LAN-first dengan timeout kondisional, fallback Tor; (d) jalur Tor (onion service v3, retry dial).
3. **Kalimat topik**: "Sebelum handshake kriptografis dimulai, AKSARA melalui tahap pertukaran invite code dan pembentukan koneksi transport yang menentukan jalur mana — LAN atau Tor — akan membawa sesi terenkripsi berikutnya."
4. **Fakta codebase**: Seluruh isi `06_PROTOCOL_SPECIFICATION.md` §3-4 — format invite base64, fingerprint binding, mDNS TXT record `fp=<hex>`, `LAN_AUTO_TIMEOUT=3 detik` kondisional, `TOR_DIAL_TOTAL_TIMEOUT=120 detik`.
5. **Evidence**: CR-002, CR-005, CR-029, `transport/mod.rs:118-172`, `transport/lan.rs:1-90`, `transport/tor.rs:1-122`.
6. **Referensi**: `rfc6762`, `rfc6763` (mDNS/DNS-SD).
7. **Claim ID**: CR-002, CR-005, CR-029.
8. **Diagram**: FIG-01, FIG-02.
9. **Tabel**: TBL-07 (format paket — bagian invite).
10. **Eksperimen**: EXP-04 (invite/fingerprint correctness).
11. **Klaim yang boleh ditulis**: Invite code TIDAK diautentikasi kriptografis (fakta eksplisit dari komentar kode); X25519 key tidak diiklankan mDNS; strategi LAN-first/Tor-fallback sesuai §4.1 `06_PROTOCOL_SPECIFICATION.md`.
12. **Klaim yang dilarang**: Menyatakan metadata presence "terlindungi" tanpa mengidentifikasi metadata yang masih terlihat (larangan `AGENTS.md` #23) — fingerprint dan presence tetap bocor via mDNS plaintext.
13. **Status kesiapan**: READY.

### 4.4 Handshake Noise_IK

1. **Tujuan**: Menjelaskan rinci alur 2-pesan handshake, orkestrasi kode, dan properti keamanan yang terverifikasi vs. hanya didokumentasikan.
2. **Outline paragraf**: (a) nama pattern `Noise_IK_25519_ChaChaPoly_BLAKE2s` dan alur 2 pesan; (b) orkestrasi `run_session` — initiator wajib tahu `peer_noise_pk`, responder fail-closed untuk kontak dikenal; (c) **temuan kritis**: tidak ada pengecekan identitas untuk kontak belum dikenal (trust-on-first-use implisit); (d) tabel properti keamanan diklaim vs diverifikasi.
3. **Kalimat topik**: "Inti autentikasi dan pembentukan kunci sesi AKSARA terjadi pada handshake Noise_IK dua pesan, di mana verifikasi identitas peer bersifat fail-closed untuk kontak yang telah dikenal namun tidak diterapkan sama sekali pada koneksi pertama ke kontak baru."
4. **Fakta codebase**: Seluruh isi `06_PROTOCOL_SPECIFICATION.md` §5 — alur 2 pesan, `session/mod.rs:117-159`, tabel properti §5.3, batasan confidence §5.4.
5. **Evidence**: CR-007..011, CR-026, CR-027.
6. **Referensi**: `noise2018`.
7. **Claim ID**: CR-007, CR-008, CR-009, CR-010, CR-011, CR-026, CR-027.
8. **Diagram**: FIG-05 (sequence handshake Noise_IK — diagram paling kritis BAB ini).
9. **Tabel**: TBL-04 (baris CORE-1), TBL-09 (threat model — T1 langsung terkait).
10. **Eksperimen**: EXP-02 (correctness, key agreement consistency, wrong-key/unknown-peer rejection).
11. **Klaim yang boleh ditulis**: Alur 2 pesan terverifikasi HIGH confidence (test+kode); fail-closed untuk kontak dikenal HIGH confidence; **ketiadaan** pengecekan identitas kontak baru HIGH confidence (untuk fakta ketiadaannya) — interpretasi "trust-on-first-use disengaja" tetap `NEEDS_CONFIRMATION`.
12. **Klaim yang dilarang**: Mengklaim forward secrecy/identity-hiding/mutual-authentication "terverifikasi penuh" — ketiganya `DOCUMENTED_ONLY`/MEDIUM, properti umum Noise_IK yang diwarisi, bukan diverifikasi test AKSARA sendiri (mandat berulang `SESSION_2_HANDOFF.md`).
13. **Status kesiapan**: READY (naratif) — verifikasi empiris tambahan lewat EXP-02 tetap `WAITING_FOR_EXPERIMENT`.

### 4.5 Transport Sesi Terenkripsi

1. **Tujuan**: Menjelaskan fase pasca-handshake — enkripsi pesan, framing, model konkurensi, dan penanganan error/penutupan sesi.
2. **Outline paragraf**: (a) format payload plaintext (tag 1-byte: TEXT/BLUR/PING); (b) model konkurensi `tokio::select!` dan alasan pemisahan task pembaca (cancel-safety `read_frame`); (c) batas ukuran pesan 65535 byte dan penanganan oversize non-fatal; (d) tabel error handling (fail-closed pada dekripsi gagal).
3. **Kalimat topik**: "Setelah handshake selesai, seluruh komunikasi AKSARA berlangsung melalui sesi transport yang mengenkripsi setiap pesan dengan skema tag plaintext sederhana dan penanganan kegagalan yang secara konsisten fail-closed."
4. **Fakta codebase**: Seluruh isi `06_PROTOCOL_SPECIFICATION.md` §6 — `session/mod.rs:164-279`, format tag TYPE_TEXT/BLUR/PING, `KEEPALIVE_INTERVAL`, tabel error handling §6.5.
5. **Evidence**: CR-026, `transport/frame.rs:1-9,16,37-56,97-104`.
6. **Referensi**: `rfc8439` (asumsi AEAD transport).
7. **Claim ID**: CR-026.
8. **Diagram**: FIG-04 (sequence proses utama).
9. **Tabel**: TBL-07 (format paket — frame+payload).
10. **Eksperimen**: EXP-03 (consistency, oversize/keepalive handling, ciphertext overhead).
11. **Klaim yang boleh ditulis**: Format tag 1-byte, batas 65535 byte, penanganan oversize non-fatal (Notice) vs dekripsi gagal fatal (fail-closed) — seluruhnya terverifikasi test existing.
12. **Klaim yang dilarang**: Menyatakan algoritma AEAD transport "dikonfirmasi ChaCha20-Poly1305" tanpa hedge — faktanya diasumsikan (MEDIUM confidence), tidak disebut literal di `session/mod.rs`.
13. **Status kesiapan**: READY.

### 4.6 Implementasi Primitif Kriptografi (CORE-1 s.d. CORE-7)

1. **Tujuan**: Menyajikan rangkuman implementasi 7 komponen kriptografi inti sebagai satu subbab konsolidasi (detail teori sudah di BAB II, di sini fokus pemetaan implementasi).
2. **Outline paragraf**: 7 sub-poin (satu per CORE), masing-masing: algoritma, library+versi, lokasi kode, parameter kunci, confidence.
3. **Kalimat topik**: "Tujuh komponen kriptografi inti — mulai dari kerangka handshake hingga sumber entropi — diimplementasikan secara konsisten menggunakan pustaka Rust matang dengan tingkat keyakinan evidence yang bervariasi per komponen."
4. **Fakta codebase**: Seluruh isi `03_CRYPTO_INVENTORY_NORMALIZED.md` §4 dan `04_CRYPTOGRAPHIC_JUSTIFICATION.md`.
5. **Evidence**: CR-001 s.d. CR-036 (seluruh 36 entry, dikonsolidasi).
6. **Referensi**: Seluruh 14 citekey primitif (`noise2018`, `rfc7748`, `bernstein2006curve25519`, `rfc8439`, `bernstein2008chacha`, `bernstein2005poly1305`, `rfc9106`, `biryukov2016argon2`, `rfc7693`, `aumasson2013blake2`, `rfc8032`, `bernstein2012ed25519`, `fips186-5`, `sp800-186`, `sp800-90a`) + 6 citekey dokumentasi library (`snowcrate`, `chacha20poly1305crate`, `ed25519dalekcrate`, `x25519dalekcrate`, `argon2crate`, `blake2crate`).
7. **Claim ID**: CR-001 s.d. CR-036.
8. **Diagram**: FIG-03 (arsitektur kriptografi CORE-1..7 — diagram utama subbab ini).
9. **Tabel**: TBL-04 (inventarisasi primitif, dipakai langsung sebagai tabel utama subbab).
10. **Eksperimen**: EXP-01 s.d. EXP-05 (seluruhnya relevan, dipetakan per CORE di `12_TEST_PLAN.md` §0).
11. **Klaim yang boleh ditulis**: Seluruh isi TBL-04 dengan confidence masing-masing dipertahankan (jangan diratakan ke HIGH semua).
12. **Klaim yang dilarang**: Menyatakan algoritma "aman" hanya karena populer (larangan `AGENTS.md` #17); menyatakan library "telah diaudit" tanpa sumber (larangan #18) — `snow` eksplisit BELUM diaudit formal.
13. **Status kesiapan**: READY.

### 4.7 Threat Model dan Analisis Risiko

1. **Tujuan**: Menyajikan trust boundary, model musuh, ancaman per komponen, dan risk register deskriptif T1-T7.
2. **Outline paragraf**: (a) trust boundary (jaringan, filesystem lokal, manusia, dependency eksternal); (b) 5 model musuh A1-A5; (c) ancaman per 7 komponen protokol (§4.1-4.7 `08_THREAT_MODEL.md`); (d) risk register T1-T7; (e) batasan cakupan eksplisit.
3. **Kalimat topik**: "Analisis ancaman terhadap AKSARA mengidentifikasi lima model musuh dan tujuh temuan risiko deskriptif, masing-masing dipetakan pada mitigasi yang benar-benar sudah tersedia dalam kode sumber."
4. **Fakta codebase**: Seluruh isi `08_THREAT_MODEL.md` §1-7.
5. **Evidence**: Seluruh evidence yang dirujuk `08_THREAT_MODEL.md` (CR-xxx, CB-xxx lintas modul).
6. **Referensi**: `noise2018`, `rfc6762`, `rfc6763`, `rfc9106`, `rfc8439`.
7. **Claim ID**: T1-T7 (risk register), A1-A5 (model musuh).
8. **Diagram**: Tidak ada diagram formal terpisah (trust boundary sudah tersaji sebagai diagram ASCII di `08_THREAT_MODEL.md` §1 — dapat diformalkan jadi Mermaid tambahan bila kuota SESSION 5B mengizinkan, opsional, di luar 7 diagram wajib yang sudah ada).
9. **Tabel**: TBL-09 (threat model, lengkap — model musuh + risk register).
10. **Eksperimen**: T1 berkorespondensi EXP-02 (unknown-peer rejection tidak diuji karena memang tidak ada mekanismenya — dicatat sebagai batasan, bukan bug pengujian).
11. **Klaim yang boleh ditulis**: Seluruh 7 temuan T1-T7 dan 5 model musuh A1-A5 persis seperti `08_THREAT_MODEL.md` §3, §6.
12. **Klaim yang dilarang**: Menyatakan sistem "aman" secara absolut (larangan `AGENTS.md` #16); memberikan skor kuantitatif (CVSS dsb.) yang tidak pernah dihitung — kemungkinan/dampak T1-T7 murni kualitatif.
13. **Status kesiapan**: READY.

---

## BAB V — PENGUJIAN DAN ANALISIS (BLOCKED — Menunggu Data Eksperimen)

Sesuai brief ("BAB V hanya boleh diisi setelah data eksperimen tersedia") dan Quality Gate ("BAB V dan BAB VI boleh menunggu data pengujian"), BAB V **sengaja tidak diisi** pada sesi ini. Struktur subbab yang direncanakan (untuk diisi setelah `12_TEST_PLAN.md` dieksekusi):

| Subbab (rencana) | Isi yang akan diisi | Sumber data |
|---|---|---|
| 5.1 Lingkungan Pengujian Aktual | Spesifikasi hardware/OS/commit saat eksperimen benar-benar dijalankan | `EXPERIMENT_RESULT_TEMPLATE.csv` kolom `environment`/`commit_hash` |
| 5.2 Hasil EXP-01 s.d. EXP-05 | Data terukur per kelompok eksperimen | `EXPERIMENT_RESULT_TEMPLATE.csv` terisi |
| 5.3 Analisis dan Diskusi | Interpretasi hasil terhadap ekspektasi `12_TEST_PLAN.md` poin 12 tiap eksperimen | Hasil §5.2 + `12_TEST_PLAN.md` |

**Status kesiapan seluruh BAB V**: `WAITING_FOR_EXPERIMENT`. **Claim ID**: Tidak ada — tidak boleh ada klaim hasil sebelum data tersedia. **Klaim yang dilarang secara mutlak**: menulis angka/hasil apa pun di BAB V sebelum eksperimen `12_TEST_PLAN.md` benar-benar dijalankan dan dicatat di `EXPERIMENT_RESULT_TEMPLATE.csv`.

---

## BAB VI — PENUTUP (BLOCKED — Bergantung BAB V)

Sesuai brief ("BAB VI tidak boleh berisi kesimpulan hasil sebelum BAB V selesai"), BAB VI **sengaja tidak diisi substansi hasil** pada sesi ini. Struktur subbab yang direncanakan:

| Subbab (rencana) | Isi yang akan diisi | Ketergantungan |
|---|---|---|
| 6.1 Kesimpulan | Kesimpulan menjawab 3 rumusan masalah — **butuh hasil BAB V** untuk rumusan masalah #1 dan #3 (verifikasi klaim keamanan empiris); rumusan masalah #2 (key lifecycle) SEBAGIAN dapat dijawab dari analisis deskriptif BAB IV tanpa menunggu eksperimen | BAB V (parsial), BAB IV (parsial) |
| 6.2 Keterbatasan Penelitian | Dapat disusun dari `09_SCOPE_AND_TEAM_PLAN.md` §5 + gap G1-G5 (`10_RELATED_WORK_AND_GAP.md`) + T1-T7 (`08_THREAT_MODEL.md`) — **tidak bergantung BAB V**, dapat disiapkan lebih awal pada SESSION 5B | Tidak bergantung eksperimen |
| 6.3 Saran | Saran pengembangan lanjutan (rotasi kunci, verifikasi formal Noise_IK, dst.) berbasis gap yang sudah teridentifikasi — **tidak bergantung BAB V** | Tidak bergantung eksperimen |

**Catatan untuk SESSION 5B**: subbab 6.2 dan 6.3 **dapat disusun lebih awal** (tidak perlu menunggu BAB V) karena bersumber dari analisis deskriptif yang sudah selesai (threat model, related work gap) — bukan dari data eksperimen. Hanya 6.1 (kesimpulan) yang benar-benar terikat penuh pada ketersediaan BAB V.

**Status kesiapan**: 6.1 = `WAITING_FOR_EXPERIMENT`; 6.2 dan 6.3 = `READY_FOR_DRAFTING` (dapat disusun penuh di SESSION 5B tanpa menunggu eksperimen, meski secara formal ditempatkan setelah BAB V dalam struktur dokumen akhir).

---

## Ringkasan Status Kesiapan per BAB

| BAB | Jumlah Subbab | Status Dominan | Catatan |
|---|---|---|---|
| I — Pendahuluan | 6 | READY | Seluruh subbab selesai penuh |
| II — Kajian Pustaka | 10 | READY | Seluruh subbab selesai penuh; bagian kuantitatif (timing Argon2id) tetap `WAITING_FOR_EXPERIMENT` |
| III — Metodologi | 5 | READY (4) / PARTIAL (1) | 3.4 sebagian `WAITING_FOR_EXPERIMENT` (lingkungan eksekusi belum final) |
| IV — Perancangan dan Implementasi | 7 | READY | Seluruh subbab selesai penuh — BAB inti, paling rinci |
| V — Pengujian dan Analisis | 3 (rencana) | `WAITING_FOR_EXPERIMENT` | Sengaja di-block, sesuai izin brief |
| VI — Penutup | 3 (rencana) | `WAITING_FOR_EXPERIMENT` (6.1) / `READY_FOR_DRAFTING` (6.2, 6.3) | 6.2/6.3 dapat disusun penuh di SESSION 5B tanpa menunggu eksperimen |

**Quality Gate poin 15 brief** ("BAB I sampai BAB IV memiliki content pack") **TERPENUHI** pada akhir subbab ini.

## Referensi

Seluruh referensi memakai citekey dari `references/REFERENCES.bib` (40 entry) — tidak ada penambahan baru pada TAHAP 15 bagian BAB I-IV ini.
