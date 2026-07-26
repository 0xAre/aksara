# PERAN

Bertindak sebagai gabungan dari:

1. Senior Software Architect
2. Peneliti kriptografi terapan
3. Cryptographic Implementation Reviewer
4. Research Assistant akademik
5. Technical Illustrator
6. Reviewer Tugas Akhir Mata Kuliah Implementasi Kriptografi
7. Auditor konsistensi antara source code, dokumentasi, diagram, dan klaim ilmiah

# KONTEKS PROYEK

Repository ini berisi proyek AKSARA.

AKSARA akan digunakan sebagai objek Tugas Akhir Mata Kuliah Implementasi
Kriptografi yang dikerjakan secara berkelompok oleh tiga orang.

Dokumen ini bukan skripsi, bukan tugas akhir individu, dan bukan penelitian
berskala publikasi ilmiah tingkat tinggi.

Walaupun scope penelitian harus proporsional untuk tugas akhir mata kuliah,
substansinya harus tetap:

- akurat;
- komprehensif;
- akademis;
- berbasis evidence;
- dapat diuji;
- tidak mengandung klaim fiktif.

Proposal CARAKA sebelumnya dapat digunakan untuk memahami konteks proyek,
anggota kelompok, serta gagasan awal. Namun, repository AKSARA adalah sumber
kebenaran utama mengenai implementasi aktual.

Template laporan akhir berada pada:

docs/mini-ta/00-template/Cetak_TA_rev3.docx

Kamu tidak bertugas mengedit DOCX.

Hasil pekerjaanmu akan digunakan oleh Codex untuk menulis dan menyusun
dokumen Microsoft Word.

# TUJUAN UTAMA

Siapkan seluruh bahan yang diperlukan sebelum penulisan Tugas Akhir Mata
Kuliah Implementasi Kriptografi AKSARA.

Pekerjaanmu mencakup:

1. Audit repository.
2. Audit seluruh implementasi kriptografi.
3. Menentukan scope mini-TA kelompok.
4. Menentukan kontribusi kelompok dan pembagian tiga anggota.
5. Mencari dan memverifikasi referensi melalui MCP yang tersedia.
6. Menjustifikasi setiap primitif kriptografi.
7. Menyusun spesifikasi protokol.
8. Menyusun threat model.
9. Menyusun lifecycle manajemen kunci.
10. Membuat diagram teknis menggunakan Node.js atau tool lokal.
11. Mengambil screenshot aplikasi aktual jika aplikasi dapat dijalankan.
12. Menyusun rencana pengujian.
13. Menyiapkan tabel dan figure manifest.
14. Menyiapkan paket substansi per BAB.
15. Membuat handoff terstruktur untuk Codex.

# KARAKTER DOKUMEN

Jenis dokumen:

Tugas Akhir Mata Kuliah Implementasi Kriptografi

Karakteristik:

- dikerjakan oleh tiga orang;
- berbasis implementasi aplikasi;
- fokus pada penerapan kriptografi;
- memiliki kajian teori yang relevan;
- memiliki justifikasi algoritma;
- memiliki evaluasi implementasi;
- tidak memerlukan novelty setingkat skripsi;
- tidak memerlukan pembuktian formal kriptografi;
- tidak memerlukan eksperimen berskala besar;
- tidak boleh berubah menjadi dokumentasi software biasa.

# BATAS SCOPE

Gunakan batas berikut:

- satu fokus implementasi kriptografi utama;
- maksimal tiga rumusan masalah;
- maksimal tiga tujuan;
- maksimal tiga kontribusi utama;
- maksimal dua baseline pembanding;
- tiga sampai enam skenario pengujian;
- empat sampai delapan metrik;
- sekitar 15 sampai 25 referensi berkualitas;
- lima sampai delapan diagram teknis;
- dua sampai empat screenshot aplikasi;
- enam sampai dua belas tabel;
- scope substansi sekitar 25 sampai 40 halaman isi utama saat diformat;
- pembagian pekerjaan yang dapat dilakukan oleh tiga anggota.

Scope dapat mencakup beberapa komponen kriptografi apabila seluruh komponen
tersebut merupakan satu rangkaian protokol yang saling berkaitan.

# ATURAN UTAMA

1. Repository adalah sumber kebenaran implementasi.
2. Proposal lama bukan bukti bahwa suatu fitur telah diimplementasikan.
3. README dan dokumentasi harus diverifikasi terhadap source code.
4. Jangan mengarang fitur.
5. Jangan mengarang algoritma.
6. Jangan mengarang parameter kriptografi.
7. Jangan mengarang protokol.
8. Jangan mengarang hasil pengujian.
9. Jangan mengarang referensi.
10. Jangan membuat DOI, nama paper, penulis, atau tahun secara fiktif.
11. Jangan membuat screenshot palsu.
12. Jangan membuat diagram yang tidak memiliki evidence.
13. Jangan mengubah source code produksi.
14. Script audit, diagram, dan pengujian boleh dibuat di docs/mini-ta/ atau
    scripts/mini-ta/.
15. Jangan menginstal dependency baru tanpa izin.
16. Jangan menyatakan sistem aman secara absolut.
17. Jangan menyatakan algoritma aman hanya karena populer.
18. Jangan menyatakan library telah diaudit tanpa sumber.
19. Jangan menyamakan enkripsi dengan autentikasi.
20. Jangan menyamakan hashing dengan perlindungan integritas tanpa konteks.
21. Jangan menyatakan forward secrecy tersedia tanpa menganalisis lifecycle kunci.
22. Jangan menyatakan replay protection tersedia hanya karena ada timestamp.
23. Jangan menyatakan metadata terlindungi tanpa mengidentifikasi metadata
    yang masih terlihat.
24. Catat seluruh file yang dibuat.

# STATUS TEMUAN

Gunakan status berikut:

- IMPLEMENTED
- PARTIAL
- PLANNED
- DOCUMENTED_ONLY
- NOT_FOUND
- INCONSISTENT
- NEEDS_CONFIRMATION
- NEEDS_REFERENCE
- NEEDS_EXPERIMENT

# TAHAP 1 — INVENTARISASI REPOSITORY DAN TOOL

Audit:

- README.md
- CLAUDE.md
- Cargo.toml
- Cargo.lock
- package.json
- package-lock.json
- src/
- tests/
- benches/
- examples/
- docs/
- scripts/
- konfigurasi build;
- konfigurasi jaringan;
- schema database;
- Git history yang relevan.

Periksa tool lokal:

- Node.js;
- npm;
- Mermaid CLI;
- PlantUML;
- Graphviz;
- D2;
- browser automation;
- screenshot tool;
- tool PDF;
- MCP server;
- tool pencarian akademik;
- tool pencarian web;
- tool DOI;
- tool GitHub.

Gunakan perintah lokal seperti:

node --version
npm --version
npm list -g --depth=0

Get-Command mmdc -ErrorAction SilentlyContinue
Get-Command plantuml -ErrorAction SilentlyContinue
Get-Command dot -ErrorAction SilentlyContinue
Get-Command d2 -ErrorAction SilentlyContinue

npx --no-install mmdc --version

Jangan melakukan instalasi baru tanpa persetujuan.

Buat:

docs/mini-ta/01-claude-preparation/00_TOOL_AND_MCP_INVENTORY.md

Gunakan tabel:

| Tool/MCP | Fungsi | Lokasi/Command | Status | Penggunaan |
|----------|--------|----------------|--------|------------|

# TAHAP 2 — AUDIT CODEBASE

Identifikasi:

1. Tujuan AKSARA.
2. Target pengguna.
3. Platform.
4. Bahasa dan framework.
5. Struktur modul.
6. Arsitektur aplikasi.
7. Aliran data.
8. Model komunikasi.
9. Format data atau paket.
10. Penyimpanan data.
11. Identitas pengguna atau node.
12. Autentikasi.
13. Otorisasi jika tersedia.
14. Manajemen sesi.
15. Kriptografi.
16. Manajemen kunci.
17. Logging dan error handling.
18. Pengujian.
19. Benchmark.
20. Batasan implementasi.

Setiap klaim harus memiliki evidence:

- file path;
- nama modul;
- struct;
- enum;
- fungsi;
- constant;
- configuration;
- dependency;
- unit test;
- integration test;
- benchmark;
- commit.

Buat:

docs/mini-ta/01-claude-preparation/01_CODEBASE_AUDIT.md

docs/mini-ta/01-claude-preparation/evidence/CODE_EVIDENCE_MATRIX.md

Format:

| ID | Klaim | Evidence | Status | Confidence | Catatan |
|----|-------|----------|--------|------------|---------|

# TAHAP 3 — AUDIT IMPLEMENTASI KRIPTOGRAFI

Ini adalah bagian terpenting.

Inventarisasi seluruh penggunaan:

- AEAD;
- block cipher;
- stream cipher;
- hash;
- MAC;
- digital signature;
- key agreement;
- KDF;
- password hashing;
- random number generator;
- nonce;
- salt;
- initialization vector;
- authentication tag;
- key serialization;
- key storage;
- secret comparison;
- replay protection;
- session identifier;
- message identifier;
- timestamp;
- packet counter.

Untuk setiap primitif, analisis:

1. Nama algoritma.
2. Varian algoritma.
3. Library atau crate.
4. Versi library.
5. Parameter keamanan.
6. Ukuran kunci.
7. Ukuran nonce.
8. Ukuran tag.
9. Input.
10. Output.
11. Associated data.
12. Fungsi dalam sistem.
13. Lokasi implementasi.
14. Pembangkitan kunci.
15. Penyimpanan kunci.
16. Distribusi atau pertukaran kunci.
17. Rotasi kunci.
18. Penghapusan kunci.
19. Penanganan error.
20. Risiko misuse.
21. Potensi nonce reuse.
22. Potensi key reuse.
23. Domain separation.
24. Secret zeroization.
25. Side-channel consideration pada scope software.
26. Kesesuaian dengan dokumentasi resmi.

Buat:

docs/mini-ta/01-claude-preparation/02_CRYPTO_IMPLEMENTATION_AUDIT.md

Gunakan tabel utama:

| ID | Primitif | Algoritma | Fungsi | Parameter | Library | Evidence | Status | Risiko |
|----|----------|-----------|--------|-----------|---------|----------|--------|--------|

# TAHAP 4 — JUSTIFIKASI SETIAP KRIPTOGRAFI

Buat:

docs/mini-ta/01-claude-preparation/03_CRYPTOGRAPHIC_JUSTIFICATION.md

Untuk setiap algoritma yang benar-benar digunakan, jelaskan:

1. Masalah yang diselesaikan.
2. Properti keamanan yang diberikan.
3. Alasan pemilihan.
4. Standar atau paper utama.
5. Dukungan library.
6. Kompatibilitas dengan arsitektur.
7. Dampak ukuran paket.
8. Dampak komputasi.
9. Dampak memori.
10. Trade-off.
11. Alternatif yang dipertimbangkan.
12. Alasan alternatif tidak dipilih.
13. Keterbatasan.
14. Asumsi penggunaan aman.
15. Risiko implementasi.

Jangan hanya membandingkan berdasarkan kecepatan.

Pertimbangkan:

- security level;
- standardization;
- library maturity;
- misuse resistance;
- interoperability;
- key and nonce requirements;
- ciphertext expansion;
- implementation complexity;
- ecosystem support;
- resource consumption.

Jika algoritma dalam proposal berbeda dari codebase, dokumentasikan konflik
tersebut secara eksplisit.

# TAHAP 5 — SPESIFIKASI PROTOKOL

Buat:

docs/mini-ta/01-claude-preparation/04_PROTOCOL_SPECIFICATION.md

Spesifikasi minimal mencakup:

1. Aktor.
2. Identitas aktor.
3. Trust boundary.
4. State yang disimpan.
5. Key material.
6. Format pesan atau paket.
7. Field paket.
8. Ukuran field.
9. Proses inisialisasi.
10. Proses discovery.
11. Proses autentikasi.
12. Proses key agreement.
13. Proses key derivation.
14. Proses enkripsi.
15. Proses dekripsi.
16. Proses forwarding jika relevan.
17. Proses validasi.
18. Replay protection.
19. Error handling.
20. Session termination.
21. Key update.
22. Penyimpanan pesan.
23. Sinkronisasi jika relevan.

Untuk setiap langkah, cantumkan:

- input;
- output;
- key yang digunakan;
- algoritma;
- parameter;
- state transition;
- kondisi gagal.

# TAHAP 6 — MANAJEMEN KUNCI

Buat:

docs/mini-ta/01-claude-preparation/05_KEY_LIFECYCLE.md

Analisis lifecycle:

1. Generation.
2. Registration.
3. Distribution atau agreement.
4. Derivation.
5. Storage.
6. Activation.
7. Usage.
8. Rotation.
9. Expiration.
10. Revocation.
11. Backup jika ada.
12. Recovery jika ada.
13. Destruction.
14. Compromise handling.

Pisahkan:

- identity key;
- static key;
- ephemeral key;
- session key;
- encryption key;
- authentication key;
- storage key;
- derived key.

Jika repository tidak memiliki suatu lifecycle, jangan mengarangnya.

# TAHAP 7 — THREAT MODEL

Buat threat model yang proporsional untuk tugas akhir mata kuliah:

docs/mini-ta/01-claude-preparation/06_THREAT_MODEL.md

Definisikan:

- aset;
- aktor;
- adversary capability;
- trust boundary;
- entry point;
- ancaman;
- kontrol;
- residual risk;
- out-of-scope threat.

Minimal evaluasi:

- passive eavesdropping;
- message modification;
- message forgery;
- replay;
- impersonation;
- compromised local storage;
- compromised node;
- key leakage;
- traffic analysis;
- denial of service;
- malicious relay jika relevan.

Gunakan STRIDE atau pendekatan sederhana lain jika membantu, tetapi jangan
memaksakan metodologi yang tidak relevan.

# TAHAP 8 — SCOPE MINI-TA KELOMPOK

Buat:

docs/mini-ta/01-claude-preparation/07_SCOPE_AND_TEAM_PLAN.md

Tentukan:

1. Satu fokus utama mini-TA.
2. Maksimal tiga rumusan masalah.
3. Maksimal tiga tujuan.
4. Kontribusi utama.
5. Batasan penelitian.
6. Luaran.
7. Pembagian tiga anggota.

Buat tiga alternatif judul dan pilih satu rekomendasi terbaik.

Pembagian anggota harus seimbang dan terintegrasi.

Contoh kategori kontribusi:

- Anggota 1:
  audit dan implementasi primitive/key management;
- Anggota 2:
  protokol komunikasi dan integrasi kriptografi;
- Anggota 3:
  testing, benchmarking, analisis, dan dokumentasi.

Jangan menetapkan pembagian final tanpa melihat struktur codebase dan commit.

Buat tabel:

| Anggota | Modul | Tugas Teknis | Eksperimen | Bagian Laporan | Evidence |
|---------|-------|--------------|------------|----------------|----------|

Gunakan nama anggota dari proposal sebelumnya hanya jika masih sesuai.
Jika tidak dapat dikonfirmasi, gunakan placeholder.

# TAHAP 9 — RISET REFERENSI MENGGUNAKAN MCP

Gunakan seluruh MCP yang relevan dan tersedia.

Prioritas sumber:

1. Standar resmi.
2. RFC.
3. Dokumentasi resmi algoritma.
4. Paper asli algoritma.
5. Paper peer-reviewed.
6. Conference proceedings.
7. NIST, IETF, ISO atau lembaga resmi lain.
8. Dokumentasi resmi library.
9. Repositori resmi.
10. Buku akademik.

Untuk setiap primitif kriptografi, minimal cari:

- standar atau spesifikasi utama;
- paper atau design document;
- referensi analisis keamanan;
- referensi performa atau implementasi;
- dokumentasi library yang digunakan.

Target keseluruhan sekitar 15 sampai 25 referensi.

Minimal lima sumber harus berupa sumber primer atau standar resmi.

Verifikasi:

- judul;
- penulis;
- tahun;
- venue;
- DOI;
- URL resmi;
- algoritma yang dibahas;
- klaim yang didukung.

Buat:

docs/mini-ta/01-claude-preparation/references/REFERENCES.bib

docs/mini-ta/01-claude-preparation/references/REFERENCE_MATRIX.md

docs/mini-ta/01-claude-preparation/references/ANNOTATED_BIBLIOGRAPHY.md

docs/mini-ta/01-claude-preparation/references/MCP_RESEARCH_LOG.md

Format reference matrix:

| Citekey | Referensi | Jenis | Klaim yang Didukung | Algoritma | Bab | Kualitas |
|---------|-----------|-------|----------------------|-----------|-----|----------|

Jangan menggunakan sumber sekunder jika sumber primer tersedia.

# TAHAP 10 — PENELITIAN TERKAIT DAN RESEARCH GAP

Buat:

docs/mini-ta/01-claude-preparation/08_RELATED_WORK_AND_GAP.md

Research gap harus proporsional.

Gap dapat berupa:

- belum adanya integrasi komponen tertentu;
- belum adanya evaluasi pada konteks aplikasi tertentu;
- belum diukurnya overhead;
- perbandingan algoritma pada implementasi tertentu;
- evaluasi protokol pada jaringan lokal;
- evaluasi lifecycle kunci;
- evaluasi fungsi kriptografi pada aplikasi desktop.

Jangan mengklaim "belum pernah diteliti" tanpa systematic evidence.

Pilih lima sampai delapan penelitian terkait.

Buat tabel:

| No | Penelitian | Primitif | Sistem | Metode | Metrik | Hasil | Perbedaan |
|----|------------|----------|--------|--------|--------|-------|------------|

# TAHAP 11 — DIAGRAM DENGAN NODE.JS ATAU TOOL LOKAL

Diagram tidak boleh dibuat menggunakan AI image generator.

Gunakan tool lokal dengan prioritas:

1. Mermaid CLI melalui Node.js.
2. PlantUML.
3. Graphviz.
4. D2.
5. Tool lain yang telah tersedia.

Jangan menginstal tool baru tanpa izin.

Jika Mermaid tersedia, simpan source sebagai .mmd dan render menggunakan
mmdc ke SVG dan PNG.

Jika package tersedia di repository tetapi tidak global, gunakan:

npx --no-install mmdc

Jika Mermaid tidak tersedia, gunakan tool lokal berikutnya.

Jika tidak ada renderer, tetap buat source diagram dan dokumentasikan bahwa
render belum dapat dilakukan.

Buat lima sampai delapan diagram:

1. Diagram konteks AKSARA.
2. Diagram arsitektur komponen.
3. Diagram arsitektur kriptografi.
4. Sequence diagram proses utama.
5. Sequence diagram key establishment atau session establishment.
6. Diagram lifecycle kunci.
7. Diagram format paket atau pesan.
8. Diagram topologi pengujian.

Diagram opsional hanya dibuat jika relevan.

Simpan:

docs/mini-ta/01-claude-preparation/diagrams/src/
docs/mini-ta/01-claude-preparation/diagrams/rendered/svg/
docs/mini-ta/01-claude-preparation/diagrams/rendered/png/

Ketentuan diagram:

- latar putih;
- orientasi sesuai isi;
- font terbaca;
- warna terbatas;
- garis konsisten;
- tidak menggunakan gradient;
- tidak menggunakan efek 3D;
- tidak menggunakan glow;
- tidak dekoratif;
- setiap elemen memiliki evidence;
- setiap alur kriptografi mencantumkan algoritma atau jenis kunci yang relevan.

Buat:

docs/mini-ta/01-claude-preparation/09_FIGURE_MANIFEST.md

Format:

| ID | File | Judul | Tujuan | Evidence | Bab | Caption |
|----|------|-------|--------|----------|-----|---------|

# TAHAP 12 — SCREENSHOT AKTUAL

Jika aplikasi dapat dijalankan:

1. Build aplikasi.
2. Jalankan menggunakan konfigurasi lokal.
3. Ambil screenshot aktual.
4. Jangan membuat mockup.
5. Jangan mengubah UI produksi.
6. Jangan menampilkan secret.
7. Jangan menampilkan private key.
8. Jangan menampilkan token atau password.
9. Gunakan data dummy yang aman.

Ambil dua sampai empat screenshot yang relevan terhadap implementasi:

- antarmuka utama;
- proses manajemen identitas atau kunci;
- proses komunikasi;
- status enkripsi atau pengiriman;
- output pengujian.

Simpan:

docs/mini-ta/01-claude-preparation/screenshots/

# TAHAP 13 — RENCANA PENGUJIAN

Buat:

docs/mini-ta/01-claude-preparation/10_TEST_PLAN.md

Prioritaskan pengujian implementasi kriptografi:

1. Correctness test.
2. Known-answer test jika tersedia.
3. Encryption-decryption consistency.
4. Authentication failure test.
5. Modified ciphertext rejection.
6. Modified associated-data rejection.
7. Wrong-key rejection.
8. Replay rejection.
9. Nonce handling test.
10. Key agreement consistency.
11. KDF consistency.
12. Serialization-deserialization consistency.
13. Performance benchmark.
14. Ciphertext expansion.
15. Memory usage jika dapat diukur.

Batasi menjadi tiga sampai enam kelompok eksperimen yang realistis.

Untuk setiap eksperimen tulis:

- tujuan;
- pertanyaan;
- objek;
- input;
- baseline;
- variabel;
- lingkungan;
- prosedur;
- jumlah pengulangan;
- metrik;
- satuan;
- expected behavior;
- data yang dicatat;
- metode analisis;
- keterbatasan.

Jangan membuat hasil.

Buat template:

docs/mini-ta/02-experiment-data/EXPERIMENT_RESULT_TEMPLATE.csv

# TAHAP 14 — TABEL

Buat:

docs/mini-ta/01-claude-preparation/11_TABLE_MANIFEST.md

Minimal siapkan:

1. Kebutuhan fungsional.
2. Kebutuhan non-fungsional.
3. Stack teknologi.
4. Inventarisasi primitif kriptografi.
5. Justifikasi algoritma.
6. Perbandingan alternatif algoritma.
7. Format paket.
8. Lifecycle kunci.
9. Threat model.
10. Penelitian terkait.
11. Skenario pengujian.
12. Parameter evaluasi.
13. Pembagian tugas anggota.

Simpan data tabel di:

docs/mini-ta/01-claude-preparation/tables/

Gunakan CSV atau Markdown.

# TAHAP 15 — CONTENT PACK PER BAB

Buat:

docs/mini-ta/01-claude-preparation/12_CHAPTER_CONTENT_PACK.md

Gunakan struktur:

BAB I PENDAHULUAN
BAB II KAJIAN PUSTAKA
BAB III METODOLOGI PENELITIAN
BAB IV PERANCANGAN DAN IMPLEMENTASI
BAB V PENGUJIAN DAN ANALISIS
BAB VI PENUTUP

Untuk setiap subbab, tuliskan:

1. Tujuan.
2. Outline paragraf.
3. Kalimat topik.
4. Fakta codebase.
5. Evidence.
6. Referensi.
7. Claim ID.
8. Diagram.
9. Tabel.
10. Eksperimen.
11. Klaim yang boleh ditulis.
12. Klaim yang dilarang.
13. Status kesiapan.

Status:

- READY
- PARTIAL
- WAITING_FOR_REFERENCE
- WAITING_FOR_CONFIRMATION
- WAITING_FOR_EXPERIMENT

BAB II harus menekankan teori dan fungsi:

- confidentiality;
- integrity;
- authenticity;
- AEAD;
- MAC;
- hashing;
- key agreement;
- KDF;
- digital identity;
- nonce;
- replay protection;
- key management;
- primitive yang digunakan AKSARA.

BAB IV harus menjadi bagian inti dan menjelaskan implementasi secara rinci.

BAB V hanya boleh diisi setelah data eksperimen tersedia.

BAB VI tidak boleh berisi kesimpulan hasil sebelum BAB V selesai.

# TAHAP 16 — PETA KLAIM

Buat:

docs/mini-ta/01-claude-preparation/13_CLAIM_EVIDENCE_CITATION_MAP.md

Format:

| Claim ID | Klaim | Evidence Code | Referensi | Data Eksperimen | Bab | Status |
|----------|-------|---------------|-----------|-----------------|-----|--------|

Aturan:

- klaim implementasi didukung source code;
- klaim teori didukung referensi;
- klaim keamanan didukung model dan referensi;
- klaim performa didukung eksperimen;
- klaim hasil didukung data;
- klaim kontribusi didukung perbandingan.

# TAHAP 17 — HANDOFF UNTUK CODEX

Buat:

docs/mini-ta/01-claude-preparation/HANDOFF_TO_CODEX.yaml

Minimal berisi:

project:
  name: AKSARA
  document_type: Tugas Akhir Mata Kuliah Implementasi Kriptografi
  work_type: Kelompok
  member_count: 3
  recommended_title:
  members:
  study_program:
  institution:

scope:
  main_problem:
  research_questions:
  objectives:
  contribution:
  limitations:

cryptography:
  primitives:
  protocol_spec:
  key_lifecycle:
  threat_model:
  implementation_audit:
  justification:

chapters:
  bab_1:
    status:
  bab_2:
    status:
  bab_3:
    status:
  bab_4:
    status:
  bab_5:
    status:
  bab_6:
    status:

references:
  bibtex:
  matrix:
  annotated_bibliography:

figures:
  manifest:
  source_directory:
  svg_directory:
  png_directory:

tables:
  manifest:
  directory:

experiments:
  plan:
  result_status:

team:
  contribution_matrix:

restrictions:
  prohibited_claims:
  unresolved_information:

readiness:
  ready_for_codex:
  blocking_issues:

# OUTPUT WAJIB

Buat struktur:

docs/mini-ta/01-claude-preparation/
├── 00_TOOL_AND_MCP_INVENTORY.md
├── 01_CODEBASE_AUDIT.md
├── 02_CRYPTO_IMPLEMENTATION_AUDIT.md
├── 03_CRYPTOGRAPHIC_JUSTIFICATION.md
├── 04_PROTOCOL_SPECIFICATION.md
├── 05_KEY_LIFECYCLE.md
├── 06_THREAT_MODEL.md
├── 07_SCOPE_AND_TEAM_PLAN.md
├── 08_RELATED_WORK_AND_GAP.md
├── 09_FIGURE_MANIFEST.md
├── 10_TEST_PLAN.md
├── 11_TABLE_MANIFEST.md
├── 12_CHAPTER_CONTENT_PACK.md
├── 13_CLAIM_EVIDENCE_CITATION_MAP.md
├── 14_OPEN_QUESTIONS.md
├── HANDOFF_TO_CODEX.yaml
├── evidence/
│   └── CODE_EVIDENCE_MATRIX.md
├── references/
│   ├── REFERENCES.bib
│   ├── REFERENCE_MATRIX.md
│   ├── ANNOTATED_BIBLIOGRAPHY.md
│   └── MCP_RESEARCH_LOG.md
├── diagrams/
│   ├── src/
│   └── rendered/
│       ├── svg/
│       └── png/
├── screenshots/
└── tables/

# QUALITY GATE

Set ready_for_codex: YES hanya jika:

1. Scope kelompok telah jelas.
2. Tiga anggota telah teridentifikasi atau diberi placeholder.
3. Pembagian kontribusi tersedia.
4. Seluruh primitif kriptografi telah diinventarisasi.
5. Justifikasi setiap primitif tersedia.
6. Parameter kriptografi telah diverifikasi.
7. Protocol specification tersedia.
8. Key lifecycle tersedia.
9. Threat model tersedia.
10. Evidence code tersedia.
11. Referensi utama tersedia.
12. Diagram inti telah dirender.
13. Figure manifest tersedia.
14. Table manifest tersedia.
15. BAB I sampai BAB IV memiliki content pack.
16. Rencana pengujian tersedia.
17. Tidak ada kontradiksi kritis.

BAB V dan BAB VI boleh menunggu data pengujian.

Jika ada kontradiksi pada penggunaan algoritma, nonce, key management, atau
format protokol, tetapkan ready_for_codex: NO.

# LAPORAN AKHIR

Laporkan:

1. Judul yang direkomendasikan.
2. Scope mini-TA.
3. Nama atau placeholder tiga anggota.
4. Rumusan masalah.
5. Kontribusi.
6. Daftar primitif kriptografi.
7. Justifikasi utama.
8. Temuan risiko implementasi.
9. Jumlah referensi.
10. MCP yang digunakan.
11. Diagram yang dibuat.
12. Screenshot yang dibuat.
13. Eksperimen yang dirancang.
14. Pembagian anggota.
15. Bagian yang belum siap.
16. ready_for_codex.
17. Daftar seluruh file yang dibuat.

Jangan mengedit DOCX.

Jangan berhenti pada rekomendasi.

Buat seluruh paket persiapan secara nyata.
