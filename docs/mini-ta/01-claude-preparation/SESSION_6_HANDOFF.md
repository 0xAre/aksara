# SESSION 6 HANDOFF

Status sesi: **SELESAI**. Dua pekerjaan: (A) validasi output SESSION 5B, (B) eksekusi sisa `12_TEST_PLAN.md` lalu mengisi BAB V dan BAB VI §6.1. Bukan TAHAP baru dalam skema 17-tahap `CLAUDE_PREPARATION_BRIEF.md` — sprint persiapan sudah selesai sejak SESSION 5B.

Commit basis pengukuran: `75d17fd`. Tanggal eksekusi: 2026-07-27.

## A. Hasil Validasi SESSION 5B

Metode: spot-check langsung ke source code (bukan membaca ulang dokumen ke dokumen), plus pengecekan silang antar-dokumen state.

**Yang diverifikasi cocok (tidak ada temuan):**

| Yang dicek | Hasil |
|---|---|
| CM-071 — tidak ada `sign()`/`verify()` Ed25519 | Grep menyeluruh `src/` nihil. **Akurat.** |
| CM-061 — komentar "~100ms" ada di `vault.rs` | Ada, pada blok doc-comment `argon2_params()`. **Akurat.** |
| Layout vault 108 byte | `SALT_LEN 16 + NONCE_LEN 12 + PLAINTEXT_LEN 64 + TAG_LEN 16`. **Cocok.** |
| Parameter Argon2id 19 MiB / t=2 / p=1 | `Params::new(19*1024, 2, 1, Some(32))`. **Cocok.** |
| Konstanta protokol di content pack §4.3/§4.5 | `MAX_FRAME_LEN=65535`, `LAN_AUTO_TIMEOUT=3s`, `TOR_DIAL_TOTAL_TIMEOUT=120s` — **ketiganya cocok** dengan source. |
| Nama pattern Noise | `NOISE_PATTERN = "Noise_IK_25519_ChaChaPoly_BLAKE2s"` literal di source. **Cocok.** |
| Bagian "Klaim Kritis Anti-Overclaim" (5 item) | Kelimanya akurat terhadap kode/dokumen pada saat ditulis. |
| `readiness.quality_gate_17_items` | 17/17 `met: true` tetap valid; tidak ada kontradiksi baru yang memaksa `ready_for_codex: NO`. |

**Dua temuan nyata — keduanya sudah diperbaiki sesi ini:**

1. **`HANDOFF_TO_CODEX.yaml` tertinggal satu commit.** Field `experiments.result_status` masih `WAITING_FOR_EXPERIMENT` dengan catatan "TIDAK ADA eksperimen yang sudah dijalankan", padahal commit `75d17fd` (2026-07-26) sudah menjalankan 46/46 test. `PROGRESS.md` dan `WORKFLOW_STATE.yaml` sudah diperbarui saat itu, handoff Codex tidak ikut. **Pelajaran**: bila status eksperimen berubah, ketiga file harus diperbarui bersamaan, bukan dua dari tiga.
2. **`HANDOFF_TO_CODEX.yaml` BI-05 salah menyebut nama file** — tertulis `16_TABLE_MANIFEST.md`, seharusnya `13_TABLE_MANIFEST.md` (kemungkinan sisa dari pergeseran penomoran +2 yang dicatat `PROGRESS.md` keputusan #0). Kosmetik, sudah dikoreksi.

`14_CHAPTER_CONTENT_PACK.md` BAB I-IV dan `15_CLAIM_EVIDENCE_CITATION_MAP.md` **tidak ditulis ulang** — tidak ditemukan pertentangan dengan `06_PROTOCOL_SPECIFICATION.md`/`07_KEY_LIFECYCLE.md`/`08_THREAT_MODEL.md`/`04_CRYPTOGRAPHIC_JUSTIFICATION.md`. Perubahan pada peta klaim murni akibat data eksperimen baru, bukan koreksi kesalahan.

## B. Hasil Eksekusi Pengujian

Data lengkap: `docs/mini-ta/02-experiment-data/EXPERIMENT_RESULTS_2026-07-27.csv` (123 baris data + blok ringkasan). File `EXPERIMENT_RESULTS_2026-07-26.csv` **tidak ditimpa**.

**Lingkungan** (wajib ikut dikutip setiap kali angka di bawah dipakai): Windows 11 Home 10.0.26200 build 26200; Intel Core i7-1165G7 4C/8T @2,80 GHz; RAM 11,79 GB (bebas ~0,93 GB saat uji); bare-metal LENOVO 82FG; `rustc 1.97.0 (2d8144b78 2026-07-07)` / `cargo 1.97.0`; profil `--release`, dibuild ulang sebelum pengukuran (1 menit 5 detik).

### EXP-05 — Benchmark Argon2id (prioritas tertinggi, SELESAI)

Prosedur: 30 cold-start `aksara id --vault <path> --offline` (proses baru per run, passphrase lewat env `AKSARA_PASSPHRASE`, data dummy), diukur `Measure-Command`. Ditambah **30 run kontrol** `aksara -h` untuk mengisolasi biaya Argon2id dari overhead spawn proses — kontrol ini tidak diminta rencana asli, tapi tanpanya angka end-to-end akan melebih-lebihkan biaya KDF.

| Ukuran | Hasil |
|---|---|
| End-to-end proses (n=30) | mean 68,47 ms · median 64,15 · sd 12,47 · min 54,53 · max 106,86 |
| Kontrol tanpa Argon2id (n=30) | mean 20,48 ms · median 19,10 · sd 4,73 |
| **`unseal` neto** (selisih berpasangan) | **mean 47,99 ms** · median 45,08 · sd 11,41 · min 26,99 · max 86,30 |
| Ukuran vault | tepat **108 byte** pada 5 vault independen |

**Kesimpulan EXP-05**: klaim komentar kode "~100 ms" **TERKOREKSI**, bukan dikonfirmasi — pada hardware uji nilainya sekitar separuh. Bahkan angka end-to-end (68 ms) masih di bawah 100 ms. CM-061 berubah dari `DOCUMENTED_ONLY`/LOW menjadi `CORRECTED`.

### Metrik lain

| Metrik | Status | Hasil |
|---|---|---|
| EXP-04 panjang invite | `EXECUTED` | 86 karakter konsisten pada 5 keypair acak; fingerprint 64 karakter hex |
| EXP-01 determinisme + rejection CLI | `EXECUTED` | 10/10 unseal sukses, invite identik seluruh run (string unik = 1); passphrase salah → exit 1, pesan generik `Error: vault could not be opened` |
| EXP-03 overhead tag AEAD | `PARTIAL` | Tepat 16 byte terukur pada instance **vault**. Instance Noise transport **tidak** diukur |
| EXP-02 latensi handshake | `PARTIAL` | Selisih berpasangan −0,15 ms (sd 1,91; n=19) = tidak terdeteksi di atas noise. Dilaporkan **batas atas < 0,86 ms (95% CI)**, bukan nilai titik |
| EXP-05 memory usage puncak (RSS) | `WAITING_FOR_EXPERIMENT` | Tidak diukur; hanya parameter statis 19 MiB yang diketahui |

Metode latensi handshake: perbandingan waktu proses test-binary yang menjalankan `handshake_ik_roundtrip --exact` versus yang menjalankan 0 test. `--report-time` cargo hanya tersedia di nightly, sehingga timing per-test tidak bisa diambil langsung. Hasilnya bermakna secara kualitatif — biaya kriptografi per sesi didominasi Argon2id (~48 ms), bukan handshake (< 1 ms).

## B2. Pekerjaan Lanjutan Sesi yang Sama (#5-#7)

Setelah commit `1653531`, pengguna meminta tiga kekurangan yang teridentifikasi dari analisis kesiapan dituntaskan:

1. **TBL-11 dan TBL-12 diisi hasil aktual.** Keduanya sebelumnya masih seluruhnya `WAITING_FOR_EXPERIMENT` padahal BAB V §5.2/§5.3 sudah menunjuk ke sana. `tables/11_test_scenarios.md` mendapat kolom "Hasil Aktual" + status per EXP; `tables/12_evaluation_parameters.md` mendapat kolom "Hasil Terukur" + status per metrik, plus catatan metode kontrol baseline.
2. **Kontradiksi 87 vs 86 karakter diperbaiki.** `screenshots/STATUS.md` (SESSION 4) mencatat panjang invite **87 karakter**; pengukuran EXP-04 pada 5 keypair memberi **86**, dan aritmetikanya membenarkan 86 (⌈64 × 4 ÷ 3⌉ = 86). Angka 87 adalah kesalahan hitung SESSION 4, bukan perubahan perilaku kode. Sudah dikoreksi beserta catatan penjelasnya. **Pelajaran**: angka yang dicatat dari pengamatan sekilas tanpa verifikasi aritmetika sempat bertahan tiga sesi.
3. **BAB VI §6.2/§6.3 dinaikkan ke content pack 13 field.** Sebelumnya hanya baris tabel rencana berstatus `READY_FOR_DRAFTING` — Codex punya arah tapi bukan bahan, dan risikonya dua subbab penutup ditulis dengan kedalaman berbeda dari 28 subbab lain. §6.2 disusun 3 lapis (batas cakupan / batas metode / batas melekat objek); §6.3 berisi 9 butir saran yang seluruhnya tertaut eksplisit ke G1-G5 atau T1-T7.

Akibatnya **BAB VI kini READY penuh**, bukan lagi campuran READY + READY_FOR_DRAFTING.

## B3. Identitas Anggota dan Spesifikasi Format Dokumen

Pengguna menunjuk `00-template/PROPOSAL CARAKA (2).docx` sebagai sumber identitas anggota, dan mengonfirmasi `00-template/Cetak TA_rev3.docx` sebagai acuan format dari dosen dengan instruksi menyederhanakannya untuk konteks tugas mata kuliah.

**Identitas — CONFIRMED, placeholder `Anggota 1/2/3` pensiun:**

| Nama | NIM |
|---|---|
| Andika Aryansyach Fauzan | 2322101878 |
| Mahendra Nur Hidayat | 2322101937 |
| Rafi Putra Fadlurrahman | 2322101963 |

Program studi Rekayasa Sistem Kriptografi, Politeknik Siber dan Sandi Negara, tahun 2026. Disebar ke `AGENTS.md`, `PROJECT_MEMORY.md`, `WORKFLOW_STATE.yaml`, `09_SCOPE_AND_TEAM_PLAN.md`, `tables/13_team_assignment.md`, dan `HANDOFF_TO_CODEX.yaml`. BI-04 → `resolved`.

**Koreksi catatan lama**: `PROGRESS.md` keputusan #2 dan `09_SCOPE_AND_TEAM_PLAN.md` menyatakan sejak SESSION 2 bahwa "proposal CARAKA seluruhnya placeholder `[Nama X — TBD]`". Itu **keliru** — file tersebut memuat nama asli lengkap dengan NIM. Kesimpulan itu bertahan lima sesi dan menyebabkan placeholder dipakai lebih lama dari perlunya.

**Batas yang dijaga**: dari `PROPOSAL CARAKA` hanya identitas anggota dan struktur dokumen yang diambil. Seluruh fakta teknisnya (mesh offline, Ascon, protokol CLAMP, tabel evaluasi, 24 referensinya) **tidak** masuk ke dokumen AKSARA — `AGENTS.md` melarang mencampur kedua proyek.

**Judul — FINAL, CONFIRMED**: pengguna menginstruksikan kepanjangan AKSARA masuk ke judul, lalu memilih bentuk ringkas dari tiga alternatif. Ini **membatalkan** catatan `09_SCOPE_AND_TEAM_PLAN.md` §7 yang sebelumnya menyatakan kepanjangan hanya dipakai sebagai konteks di BAB I.

> **AKSARA (*Authenticated Key-based Secure Autonomous Relay Architecture*): Chat Terminal Tanpa Server — Implementasi dan Evaluasi Keamanan Protokol Noise_IK, Siklus Hidup Kunci, dan Threat Model**

Dua konsekuensi yang **wajib dikompensasi Codex**, bukan diabaikan: kata "P2P" tidak muncul di judul, sehingga sifat peer-to-peer harus ditegaskan di kalimat pembuka Abstrak dan BAB I §1.1; dan sisi evaluasi empiris juga tidak muncul, sehingga koreksi klaim "~100 ms" → ~48 ms serta hasil 46/46 pengujian harus tampil eksplisit di Abstrak dan BAB VI §6.1.

**Larangan frasa judul** (dicatat di `16_DOCUMENT_FORMAT_SPEC.md` §2): "Tanpa Jejak", "Anti-Sadap", "Sepenuhnya Anonim", "Terbukti Aman", atau variasi yang menyiratkan jaminan absolut. T2 mencatat fingerprint dan presence masih bocor lewat mDNS plaintext — judul yang menjanjikan lebih dari yang dibuktikan dokumen sendiri akan runtuh saat ditanya penguji. "Tanpa Server" lolos karena akurat secara harfiah.

**Format — `16_DOCUMENT_FORMAT_SPEC.md` dibuat.** Aturan tipografi diukur langsung dari XML `Cetak TA_rev3.docx`, bukan diperkirakan: A4, margin kiri 4 cm dan atas/kanan/bawah 3 cm, Times New Roman 12 pt, rata kiri-kanan, spasi baris 1,15, sitasi IEEE numerik, caption bernomor per BAB.

Struktur disederhanakan sesuai instruksi. **Dihapus**: lembar judul duplikat, lembar pernyataan orisinalitas, lembar persetujuan, lembar pengesahan, lembar persetujuan publikasi, kata pengantar, abstract bahasa Inggris, daftar notasi, daftar lampiran, daftar riwayat hidup. Alasannya konsisten: seluruhnya artefak sidang TA resmi yang menuntut tanda tangan pembimbing/penguji, sementara tugas ini tidak melalui sidang. **Dipakai**: sampul, daftar isi/gambar/tabel, BAB I-VI, daftar pustaka; abstrak Indonesia opsional.

Penyederhanaan ini punya **dasar preseden**, bukan asumsi: proposal CARAKA — untuk mata kuliah yang persis sama — sudah memakai struktur ringkas tanpa satu pun lembar formal tersebut.

**Peringatan untuk Codex**: angka spasi baris 1,15 berasal dari pengukuran **satu contoh TA**, bukan kutipan peraturan tertulis. Banyak panduan Indonesia mensyaratkan 1,5. Bila ada panduan tertulis dari dosen, panduan itu menang.

## B4. Pedoman Resmi Institusi dan Peran Anggota

Pengguna menyediakan **`Peraturan Direktur Poltek SSN tentang Pedoman Pelaksanaan Tugas Akhir` (2024, 149 halaman)** — file di luar repo, `E:\Kuliah\TA\FINAL PERDIR PEDOMAN TA\`. Aturan tata tulis diekstrak dari halaman 58-68 dan `16_DOCUMENT_FORMAT_SPEC.md` **ditulis ulang** dengan pedoman ini sebagai sumber otoritatif, bukan lagi hasil ukur contoh docx.

**Yang terkonfirmasi benar** (hasil ukur XML sesi sebelumnya cocok dengan pedoman): A4, margin kiri 4 cm dan kanan/atas/bawah 3 cm, Times New Roman 12 pt, rata kiri-kanan, sitasi IEEE, caption tabel di atas dan gambar di bawah, penomoran per bab.

**Spasi 1,15 — pertanyaan terbuka kini TERTUTUP.** Sesi sebelumnya saya menandai 1,15 sebagai hasil ukur satu contoh yang mungkin kalah oleh panduan tertulis, dan menyarankan cek ke dosen. Pedoman hlm. 59 butir d menyebutnya eksplisit: *"Pengetikan dilakukan dengan spasi 1,15 (line spacing = multiple at 1,15)"*. Angka itu resmi. Jangan diganti 1,5.

**Satu aturan yang saya SALAH sebelumnya**: penomoran subbab. Versi lama spec menyarankan angka Arab (`2.1.1`) demi konsistensi dengan content pack. Pedoman hlm. 62-63 mewajibkan **Romawi.Arab** — `IV.1` untuk subbab (kapital semua) dan `IV.1.1` untuk anak subbab (Title Case, kata sambung/depan huruf kecil). Sudah dikoreksi dengan catatan eksplisit di §6 spec.

**Aturan baru yang sebelumnya tidak diketahui sama sekali**: paragraf **tanpa indentasi** (mulai dari batas kiri, dipisah satu baris kosong); footer wajib auto text "Politeknik Siber dan Sandi Negara" Arial 10 pt tebal rata kanan dari Abstrak sampai Daftar Pustaka; nomor halaman bagian awal Romawi kecil di tengah 2,5 cm dari tepi bawah; larangan menulis judul bab → subbab → anak subbab berturut-turut tanpa kalimat penyisip; perincian `a.` → `a)` → `(a)`; sumber gambar/tabel Times New Roman 10 pt bila bukan olahan sendiri; sitasi IEEE dengan nomor **sebelum tanda baca** dan spasi sebelum kurung siku.

**Abstrak naik dari opsional menjadi wajib** — pedoman mengaturnya rinci (200-300 kata, spasi tunggal, tanpa rujukan referensi, maksimal 7 kata kunci), dan ia menjadi satu-satunya tempat pembaca menangkap koreksi klaim performa dengan cepat karena judul final tidak lagi menyinggung sisi empiris.

**Penyederhanaan tetap berlaku** dan daftarnya bertambah dengan item yang baru terlihat dari pedoman: spesifikasi sampul hardcover linen berwarna, tinta emas, logo 5 cm, jilid lem, cetak bolak-balik, serta aturan "setiap bab mulai di halaman ganjil". Semuanya spesifikasi percetakan TA fisik yang tidak relevan untuk tugas mata kuliah.

**Deviasi jumlah bab dicatat eksplisit**: pedoman hlm. 64 menyebut Bagian Utama 5 bab; dokumen ini memakai 6 bab. Bukan pelanggaran — contoh TA yang lolos sidang juga 6 bab dengan pemisahan yang sama, dan isi AKSARA menuntutnya karena implementasi sudah ada sebelum penelitian dimulai.

### Peran anggota — CONFIRMED

| Anggota | Peran | Bab |
|---|---|---|
| Andika Aryansyach Fauzan | Core developer — fullstack | BAB IV; verifikasi teknis BAB II/III |
| Mahendra Nur Hidayat | Dokumentasi akhir | BAB I, II, VI, Abstrak, bagian awal/akhir |
| Rafi Putra Fadlurrahman | User testing | BAB V; metodologi pengujian BAB III |

Pembagian **berbasis peran fungsional, bukan kepemilikan modul kode**. Pembagian lama di `09_SCOPE_AND_TEAM_PLAN.md` §8 (`identity+crypto` / `transport+session` / `contacts+tui`) adalah asumsi perencanaan SESSION 2 dan kini **SUPERSEDED**, dengan blok penjelasan supersession ditinggalkan di tempatnya.

**Alasan pembagian tidak dipecah per modul**: AKSARA sudah terimplementasi utuh oleh satu core developer sebelum penelitian dimulai. Mengarang pembagian kepemilikan kode menjadi tiga agar terlihat seimbang akan menjadi klaim yang tidak benar — melanggar `AGENTS.md` sekaligus Pasal 5 huruf a Perdir Pedoman TA tentang kejujuran akademik. Keseimbangan tetap terjaga lewat luaran yang sebanding: artefak, dokumen, dan data.

## B5. Screenshot Sesi A Diterima

**2026-07-29**: pengguna mengirim `ss-aksara.zip` berisi 5 berkas PNG hasil pengambilan anggota kelompok. Seluruhnya sudah diperiksa satu per satu sebagai gambar, bukan hanya dicek nama berkasnya, lalu disimpan ke `screenshots/`.

| Berkas | Isi | Bab |
|---|---|---|
| `01-antarmuka-utama.png` | TUI berjalan, badge `⌂ LOCAL`, fingerprint `64809f`, kontak kosong | BAB IV.1 |
| `02-identitas-invite.png` | Invite 86 karakter, fingerprint 64 hex (8×8) | BAB IV.3 |
| `03-komunikasi-loopback-a.png` | Sesi aktif sisi inisiator, 3 pesan | BAB IV.5 |
| `03-komunikasi-loopback-b.png` | Sisi responder sesi yang sama | BAB IV.5 |
| `04-verifikasi-vault.png` | Dua `unseal` identik + tolak passphrase salah | BAB V.2 |

Dua berkas komunikasi diberi akhiran `-loopback` agar jalur transportnya tidak ambigu.

**Temuan dari pemeriksaan gambar:**

1. **Panjang invite terkonfirmasi 86 karakter secara visual.** Ini bukti ketiga yang saling menguatkan setelah pengukuran CLI dan perhitungan aritmetika — memperkuat koreksi 87→86 di §B2.
2. **`04-verifikasi-vault.png` menampilkan passphrase terbaca** (`demo-mini-ta-2026`, `12345678`). Bukan kebocoran karena keduanya dummy, dan justru memperkuat demonstrasi. Lebih penting: gambar itu menjadi **bukti visual atas keterbatasan yang sudah terdokumentasi** — input passphrase stdin masih ter-echo ke layar (`08_THREAT_MODEL.md` §4.6, `07_KEY_LIFECYCLE.md`, status `PLANNED` M4). Sebelumnya keterbatasan itu hanya dibaca dari komentar kode.
3. **Jalur transport pada `03-*` adalah TCP loopback**, bukan LAN fisik atau Tor. Aplikasi tidak mencetak jalur transport di layar, jadi keterangan gambar wajib menyebutnya eksplisit.

**Dua koreksi pada panduan** yang ditemukan saat mencocokkan gambar dengan source:

- **Badge transport bukan `LAN`/`TOR`.** Sesuai `src/tui/ui.rs:311-317`, nilainya `⌂ LOCAL` (abu-abu) bila Tor mati, `LINKING` dengan spinner saat bootstrap, dan `◉ ONLINE` (aksen) saat Tor aktif. Revisi sebelumnya sempat menyatakan "tidak ada badge yang berubah" — itu juga keliru: badge memang berpindah status, hanya saja tanpa tulisan "TOR". Instruksi Screenshot 6 diperbaiki agar mereka memotret badge `◉ ONLINE`.
- **`Ctrl+B` bernama "Mode Light"** di aplikasi (blur pesan lama), bukan sekadar "blur". Ditambahkan juga `Ctrl+S` (cari) dan `Ctrl+R` (balas) yang terlihat di bilah bantuan tapi belum tercatat.

**Status akhir**: Sesi A ✅ selesai, Sesi B ⬜ belum (butuh 2 laptop jaringan berbeda). BI-03 turun dari `non_blocking` menjadi `partially_resolved`. Panduan direnumerasi: Sesi B kini Screenshot 5, 6, 7a/b/c, dan opsional 8.

## C. Dokumen yang Diperbarui

- `14_CHAPTER_CONTENT_PACK.md` — **BAB V terisi penuh** (5.1 lingkungan, 5.2 hasil, 5.3 analisis; format 13 field per subbab sama seperti BAB I-IV) dan **BAB VI §6.1 terisi**. §6.2/§6.3 **tidak diubah** (tetap `READY_FOR_DRAFTING`), hanya ditambahi daftar bahan dari hasil BAB V. Tabel ringkasan status per BAB diperbarui.
- `15_CLAIM_EVIDENCE_CITATION_MAP.md` — CM-061 → `CORRECTED`; §15 klaim performa ditulis ulang dengan hasil nyata; CM-155 (vault 108 byte) dan CM-156 (invite 86 karakter) baru; total **81 → 83** Claim ID; anti-overclaim item #3 diperbarui.
- `HANDOFF_TO_CODEX.yaml` — `ready_for_codex` **`YES_PARTIAL` → `YES`**; `bab_3`/`bab_5`/`bab_6` → `READY`; `experiments.result_status` → `EXECUTED` + blok `environment`; BI-01/BI-02 → `resolved`; **BI-06 baru**; BI-05 nama file dikoreksi.
- `12_TEST_PLAN.md` — bagian "Status Eksekusi" diperbarui dengan tabel hasil per metrik.
- `PROGRESS.md`, `WORKFLOW_STATE.yaml` (`session_6` baru, `ready_for_codex: YES`), `PROJECT_MEMORY.md`.

## D. Aturan Anti-Overclaim yang Wajib Dibawa Codex

Status `ready_for_codex: YES` **tidak** berarti semua terukur. Tiga hedge tidak boleh dihapus saat menulis prosa:

1. **Latensi handshake** — tulis sebagai batas atas (< 0,86 ms), jangan pernah sebagai nilai titik, dan jangan tulis "handshake tidak memakan waktu".
2. **Overhead ciphertext 16 byte** — yang terukur instance **vault**; untuk transport sesi nilainya deterministik dari spesifikasi, bukan hasil pengukuran.
3. **Angka performa apa pun** — selalu bersama n, sebaran, dan spesifikasi hardware §5.1. Jangan generalisasi ke "hardware modern".

Ditambah: jangan menulis komentar kode "salah" secara umum — yang terukur hanya satu unit hardware. Empat item lain di "Klaim Kritis Anti-Overclaim" (Ed25519 tanpa sign/verify, forward secrecy `DOCUMENTED_ONLY`, ChaCha20-Poly1305 tanpa AAD/misuse-resistance, trust-on-first-use) **tidak berubah** dan tetap berlaku penuh.

## E. Next Action

**Jalur B (Codex menyusun DOCX)** — kini dari BAB I s.d. BAB VI, tidak ada lagi yang perlu ditunggu. Entry point tetap `HANDOFF_TO_CODEX.yaml`, wajib baca "Klaim Kritis Anti-Overclaim" dan bagian D di atas sebelum menulis prosa.

**Opsional, butuh izin eksplisit pengguna untuk memodifikasi `src/`:**

1. Tambah harness `criterion` (`benches/`) untuk mengukur latensi handshake dan overhead ciphertext transport secara presisi — akan menaikkan CM-151/CM-152 dari `PARTIAL` menjadi `MEASURED`.
2. Tambah test rejection untuk frame/ciphertext transport sesi yang dimodifikasi — satu-satunya kelas rejection yang belum punya test (`12_TEST_PLAN.md` §EXP-03 poin 15).
3. Ukur RSS puncak saat Argon2id berjalan (CM-154) — butuh tooling profiling, bukan modifikasi source.

Ketiganya **tidak menghalangi** penyusunan DOCX.

**Yang masih `NEEDS_CONFIRMATION` dan hanya bisa diisi kelompok**: nama asli 3 anggota, `study_program`, `institution`, serta capture screenshot TUI aktual (BI-03/BI-04).
