# 16 — Spesifikasi Format Dokumen AKSARA

Aturan format yang **wajib diikuti Codex** saat menyusun DOCX. Direvisi 2026-07-27 setelah pengguna menyediakan pedoman resmi institusi.

## 1. Sumber dan Hierarki Aturan

| Prioritas | Sumber | Status | Dipakai untuk |
|---|---|---|---|
| **1** | **`Peraturan Direktur Poltek SSN tentang Pedoman Pelaksanaan Tugas Akhir` (2024, 149 hlm.)** — di luar repo: `E:\Kuliah\TA\FINAL PERDIR PEDOMAN TA\` | **Peraturan resmi** | **Sumber utama seluruh aturan tata tulis.** Menimpa dua sumber di bawah bila berbeda |
| 2 | `00-template/Cetak TA_rev3.docx` | Contoh TA orang lain (topik QRNG, Poltek SSN 2025) | Konfirmasi silang: seluruh nilai yang diukur dari XML-nya **cocok** dengan pedoman |
| 3 | `00-template/PROPOSAL CARAKA (2).docx` | Proposal kelompok yang sama, mata kuliah yang sama | Identitas anggota dan preseden struktur ringkas |

**Catatan penting tentang cakupan pedoman**: Perdir ini mengatur **Tugas Akhir** — karya tingkat IV, 2 semester, 4 SKS, dengan sidang dan penguji (Pasal 2-6). Dokumen kita adalah **tugas mata kuliah Implementasi Kriptografi**, bukan TA tersebut. Karena itu aturannya diterapkan **terpisah**:

- **Tata tulis (§4-§8 dokumen ini) → diikuti penuh.** Ini yang dimaksud pengguna dengan "aturan dari dosen".
- **Struktur dokumen (§3) → disederhanakan** atas instruksi eksplisit pengguna. Bagian yang dihapus beserta alasannya didaftar lengkap di §3.2 supaya keputusan ini dapat dipertanggungjawabkan bila ditanya.

**Batas `PROPOSAL CARAKA`**: proyek berbeda (mesh offline, Ascon, protokol CLAMP). `AGENTS.md` melarang mencampur faktanya. Dari file itu **hanya identitas anggota dan struktur dokumen** yang diambil.

## 2. Identitas Dokumen

| Field | Nilai | Status |
|---|---|---|
| Jenis dokumen | Tugas Mata Kuliah Implementasi Kriptografi | CONFIRMED |
| Judul | **AKSARA (*Authenticated Key-based Secure Autonomous Relay Architecture*): Chat Terminal Tanpa Server — Implementasi dan Evaluasi Keamanan Protokol Noise_IK, Siklus Hidup Kunci, dan Threat Model** | CONFIRMED (2026-07-27) |
| Penulis 1 | Andika Aryansyach Fauzan (2322101878) | CONFIRMED |
| Penulis 2 | Mahendra Nur Hidayat (2322101937) | CONFIRMED |
| Penulis 3 | Rafi Putra Fadlurrahman (2322101963) | CONFIRMED |
| Program studi | Rekayasa Sistem Kriptografi | CONFIRMED |
| Institusi | Politeknik Siber dan Sandi Negara | CONFIRMED |
| Tahun | 2026 | CONFIRMED |

**Judul sudah diperiksa terhadap pedoman** (hlm. 60 butir 3): judul tidak memakai singkatan kecuali nama/istilah — `AKSARA` adalah nama proyek dan `Noise_IK` adalah nama protokol, keduanya diizinkan; judul bukan kalimat tanya; judul tidak ditutup tanda baca. **Aman.**

Dua konsekuensi pilihan judul yang **wajib dikompensasi Codex**:

1. Kata "P2P" tidak muncul di judul → sifat *peer-to-peer* ditegaskan di kalimat pembuka Abstrak dan BAB I.1.
2. Sisi evaluasi empiris tidak muncul → koreksi klaim "~100 ms" menjadi ~48 ms dan hasil 46/46 pengujian harus tampil eksplisit di Abstrak dan BAB VI.

**Frasa DILARANG** di judul/subjudul meski terdengar menjual: "Tanpa Jejak", "Anti-Sadap", "Sepenuhnya Anonim", "Terbukti Aman". `08_THREAT_MODEL.md` T2 mencatat fingerprint dan presence masih bocor lewat mDNS plaintext. "Tanpa Server" lolos karena akurat secara harfiah.

## 3. Struktur Dokumen

### 3.1 Yang DIPAKAI

| # | Bagian | Catatan |
|---|---|---|
| 1 | **Sampul** | Judul, 3 nama + NIM, program studi, institusi, tahun. Simetris di tengah. Tanpa hardcover/linen/tinta emas (§3.2) |
| 2 | **Abstrak** (Indonesia) | **200-300 kata**, spasi tunggal, **tanpa rujukan referensi apa pun**, diakhiri maksimal 7 kata kunci urut abjad. Memuat judul, kata "Oleh", nama + NIM, nama program studi |
| 3 | **Daftar Isi** | Dibangkitkan otomatis Word, spasi tunggal |
| 4 | **Daftar Gambar** | 7 diagram (`11_FIGURE_MANIFEST.md`), otomatis, spasi tunggal |
| 5 | **Daftar Tabel** | 13 tabel (`13_TABLE_MANIFEST.md`), otomatis, spasi tunggal |
| 6 | **BAB I — PENDAHULUAN** | 6 subbab |
| 7 | **BAB II — KAJIAN PUSTAKA** | 10 subbab |
| 8 | **BAB III — METODOLOGI PENELITIAN** | 5 subbab |
| 9 | **BAB IV — PERANCANGAN DAN IMPLEMENTASI** | 7 subbab |
| 10 | **BAB V — PENGUJIAN DAN ANALISIS** | 3 subbab |
| 11 | **BAB VI — PENUTUP** | 3 subbab |
| 12 | **Daftar Pustaka** | 40 entry (`references/REFERENCES.bib`), format IEEE, spasi tunggal |

**Abstrak naik status dari opsional menjadi dipakai** — pedoman mengatur Abstrak secara rinci (hlm. 61) dan ia menjadi satu-satunya tempat pembaca menangkap koreksi klaim performa secara cepat, mengingat judul final tidak lagi menyinggung sisi empiris.

**Catatan jumlah bab**: pedoman (hlm. 64) menyebut Bagian Utama terdiri atas Pendahuluan, Telaah Kepustakaan, Metodologi Penelitian, Hasil Penelitian dan Pembahasan, serta Simpulan dan Saran — 5 bab. Dokumen ini memakai **6 bab** dengan memisahkan Perancangan/Implementasi (BAB IV) dari Pengujian/Analisis (BAB V). Ini **bukan pelanggaran**: contoh `Cetak TA_rev3.docx` yang sudah dicetak dan lolos sidang juga memakai 6 bab dengan pemisahan yang sama, dan pemisahan ini justru dituntut oleh isi AKSARA — implementasinya sudah ada sebelum penelitian dimulai, pengujiannya yang baru dikerjakan.

### 3.2 Yang DIHAPUS dan alasannya

| Bagian di pedoman | Alasan dihapus |
|---|---|
| Lembar Judul (duplikat sampul) | Redundan dengan sampul |
| Lembar Pernyataan Orisinalitas | Butuh tanda tangan elektronik bersertifikat — artefak sidang TA |
| Lembar Persetujuan | Butuh tanda tangan Pembimbing Materi; tugas mata kuliah tidak punya pembimbing TA |
| Lembar Pengesahan Penguji | Butuh tanda tangan Ketua Penguji + Penguji I + II. **Tidak ada sidang** |
| Halaman Pernyataan Persetujuan Publikasi | Penyerahan Hak Bebas Royalti ke institusi — hanya untuk TA resmi |
| Kata Pengantar / Ucapan Terima Kasih | Ucapan terima kasih personal; tidak relevan untuk tugas satu mata kuliah |
| Abstract (bahasa Inggris) | Pedoman mensyaratkan dua bahasa untuk TA; berlebihan untuk tugas mata kuliah |
| Daftar Notasi | AKSARA tidak memakai notasi matematis formal yang perlu didaftar |
| Daftar Lampiran + Lampiran | Kode sumber tidak dilampirkan — repositori sudah menjadi luaran, cukup dirujuk |
| Daftar Riwayat Hidup | Artefak TA resmi |
| Sampul hardcover linen berwarna, tinta emas, logo 5 cm, jilid lem, cetak bolak-balik | Spesifikasi fisik percetakan TA (hlm. 58, 60). Tugas mata kuliah tidak dijilid hardcover |
| Aturan "setiap bab dimulai di halaman ganjil" | Konsekuensi cetak bolak-balik yang tidak dipakai |

**Dasar penyederhanaan**: proposal kelompok ini untuk mata kuliah yang sama sudah memakai struktur ringkas — hanya sampul, daftar isi/gambar/tabel, isi, dan daftar pustaka. Penghapusan di atas mengikuti preseden yang sudah diterima, bukan keputusan sepihak.

## 4. Halaman dan Tipografi

Seluruh nilai berasal dari pedoman (hlm. 58-59) dan **terkonfirmasi cocok** dengan hasil pengukuran XML `Cetak TA_rev3.docx`.

| Aspek | Ketentuan | Sumber |
|---|---|---|
| Kertas | A4, HVS 80 gram, putih polos | Pedoman hlm. 58 |
| Margin kiri | **4 cm** | Pedoman hlm. 58 · cocok dengan XML (`w:left="2268"` twips) |
| Margin kanan, atas, bawah | **3 cm** | Pedoman hlm. 58 · cocok dengan XML (`1701` twips) |
| Font | **Times New Roman 12 pt** | Pedoman hlm. 58 · cocok dengan XML |
| Perataan | **Rata kiri-kanan (justify)** | Pedoman hlm. 58 · cocok dengan XML |
| Spasi baris | **1,15** (`line spacing = multiple at 1,15`) | Pedoman hlm. 59 · cocok dengan XML (`w:line="276"`) |
| Indentasi paragraf | **TIDAK ADA.** Huruf pertama paragraf baru mulai dari batas tepi kiri | Pedoman hlm. 65 butir 7 |
| Jarak antarparagraf | Satu baris kosong (spasi 1,15, ukuran 12) | Pedoman hlm. 65 butir 8 |
| Footer | Auto text **"Politeknik Siber dan Sandi Negara"**, **Arial 10 pt tebal, rata kanan**, dari Abstrak sampai Daftar Pustaka | Pedoman hlm. 58 butir b |

**Catatan spasi 1,15 — pertanyaan terbuka sebelumnya kini TERTUTUP.** Revisi dokumen ini sebelumnya menandai 1,15 sebagai hasil ukur satu contoh yang mungkin kalah oleh panduan tertulis. Pedoman hlm. 59 butir d menyebut angka itu eksplisit: *"Pengetikan dilakukan dengan spasi 1,15 (line spacing = multiple at 1,15)"*. **1,15 adalah aturan resmi, bukan kebetulan.** Jangan diganti 1,5.

Spasi **tunggal** (bukan 1,15) khusus untuk: kutipan langsung, keterangan notasi setelah persamaan, judul tabel/gambar yang lebih dari satu baris, daftar pustaka, Abstrak, dan seluruh daftar (isi/gambar/tabel).

Jarak antarblok (pedoman hlm. 59 butir h): penunjuk bab → judul bab = 1 spasi; judul bab → teks pertama = 3 spasi; teks → judul subbab berikutnya = 2 spasi; judul subbab → baris pertama teks = 1 spasi; teks ↔ tabel/gambar = 2 spasi.

## 5. Penomoran Halaman

| Bagian | Penomoran |
|---|---|
| Lembar Sampul | Tidak diberi nomor |
| Bagian awal (Abstrak, Daftar Isi/Gambar/Tabel) | **Angka Romawi kecil**, posisi **tengah, 2,5 cm dari tepi bawah** |
| BAB I sampai Daftar Pustaka | **Angka Arab** |

Sumber: pedoman hlm. 59 butir g.

## 6. Penomoran dan Penulisan Judul Bab

> **KOREKSI terhadap revisi dokumen ini sebelumnya.** Versi lama menyarankan penomoran subbab memakai angka Arab (`2.1.1`) demi konsistensi dengan `14_CHAPTER_CONTENT_PACK.md`. **Itu salah.** Pedoman hlm. 62-63 mewajibkan kombinasi **angka Romawi (bab) + angka Arab (subbab)**. Pedoman menang; content pack hanya alat kerja internal, bukan dokumen cetak.

| Level | Bentuk | Contoh |
|---|---|---|
| Bab | `BAB` + angka Romawi pada satu baris, judul bab pada baris berikutnya. **Kapital semua, tebal, simetris tengah**, tanpa garis bawah, tanpa titik | `BAB IV` / `PERANCANGAN DAN IMPLEMENTASI` |
| Subbab | **Romawi.Arab**, judul **kapital semua** | `IV.1 ARSITEKTUR SISTEM` |
| Anak subbab | **Romawi.Arab.Arab**, judul **Title Case** | `IV.1.1 Struktur Modul Kriptografi` |

Pada Title Case anak subbab, kata sambung dan kata depan di tengah judul **tidak** dikapitalkan: *yang, karena, dan, untuk, sebagai, atau, tetapi, dengan, jika, maka, oleh, serta, bagi, dari, daripada, terhadap, di, ke, pada, kepada* (pedoman hlm. 63 butir 5).

Aturan lain yang mudah terlewat:

- **Nomor dan judul anak subbab tidak dimuat di Daftar Isi** — hanya bab dan subbab (hlm. 62 butir 4).
- **Dilarang menulis judul bab → judul subbab → judul anak subbab berturut-turut tanpa kalimat penyisip.** Wajib ada minimal satu paragraf di antaranya (hlm. 65 butir 13).
- Perincian yang bukan subordinat judul memakai huruf, bukan angka: `a.` → `a)` → `(a)` (hlm. 65 butir 6).
- Setiap bab dimulai pada halaman baru (hlm. 64 butir 1).
- Istilah asing dicetak **miring**, kecuali nama (hlm. 62 butir 10). Relevan untuk dokumen ini: *handshake*, *forward secrecy*, *trust-on-first-use*, *serverless*, *peer-to-peer*.

## 7. Gambar dan Tabel

Sumber: pedoman hlm. 66.

| Aturan | Ketentuan |
|---|---|
| Penomoran | Menyertakan nomor bab: `Tabel 4.1` = tabel pertama di BAB IV. Berlaku sama untuk gambar |
| Judul tabel | **Di atas** tabel, rata kiri atau simetris tengah, jarak 1,15 spasi, langsung mengikuti nomornya |
| Judul gambar | **Di bawah** gambar, simetris tengah, jarak 1,15 spasi |
| Judul lebih dari satu baris | Simetris tengah, **spasi tunggal** |
| Penulisan nama | **Title Case** |
| Posisi | Simetris tengah terhadap halaman, diletakkan di antara bagian teks yang paling banyak membahasnya |
| Wajib dirujuk | Setiap gambar/tabel harus dirujuk dalam teks bagian utama |
| Harus mandiri | Dapat dimengerti tanpa membaca teks — judul harus deskriptif |
| Sumber | Bila bukan olahan sendiri, tulis sumber di bawah tabel / di bawah judul gambar, **Times New Roman 10 pt tegak**, jarak 1,15 spasi. Bila diolah lebih lanjut beri catatan "telah diolah kembali" |

**Untuk AKSARA**: ketujuh diagram adalah olahan sendiri (dirender dari `diagrams/src/*.mmd`), sehingga **tidak perlu baris sumber**. Sisipkan dari `diagrams/rendered/png/`. Seluruh tabel juga olahan sendiri dari audit source code.

## 8. Sitasi dan Daftar Pustaka

Sumber: pedoman hlm. 68.

- **Gaya IEEE**, dibangkitkan dengan *Reference Manager Tools* (Mendeley/Zotero/fitur Word), bukan diketik manual.
- Rujukan dalam teks memakai **nomor urut dalam kurung siku**, ditempatkan **sebelum tanda baca**, dengan **spasi sebelum kurung siku pembuka**. Contoh: `… dispesifikasikan pada Noise Protocol Framework [1].`
- Nomor diberikan **sesuai urutan kemunculan pertama**; sumber yang sama memakai nomor yang sama di seluruh dokumen.
- Urutan entri Daftar Pustaka **harus sama persis** dengan urutan numerik dalam teks.
- Nama depan penulis ditulis sebagai inisial, nama belakang lengkap.
- Daftar Pustaka diketik **spasi tunggal**.

**Sumber referensi AKSARA**: `references/REFERENCES.bib` (**40 entry terverifikasi**). Dilarang menambah referensi baru tanpa verifikasi — `AGENTS.md` melarang mengarang DOI/penulis/tahun/venue.

Aturan `AGENTS.md` **lebih ketat** dan tetap berlaku di atas aturan format: setiap klaim teori wajib bersitasi; setiap klaim implementasi wajib menunjuk path + symbol source code, bukan sitasi.

## 9. Yang Masih Perlu Dikonfirmasi

| # | Item | Dampak bila salah |
|---|---|---|
| 1 | Apakah dosen mata kuliah menghendaki struktur lebih ringkas atau lebih lengkap dari §3 | Menambah atau menghapus bagian |
| 2 | Apakah footer "Politeknik Siber dan Sandi Negara" tetap diminta untuk tugas mata kuliah | Kosmetik, mudah ditambah/dihapus |
| 3 | Apakah Abstrak wajib dua bahasa seperti TA, atau cukup Indonesia | Menambah satu halaman |

Ketiganya kosmetik dan tidak menghalangi penyusunan dimulai.

## Referensi

Tidak ada referensi teori baru. Isi dokumen ini berasal dari `Peraturan Direktur Poltek SSN tentang Pedoman Pelaksanaan Tugas Akhir` (2024) halaman 58-68, dengan konfirmasi silang terhadap `00-template/Cetak TA_rev3.docx` (pengukuran XML) dan `00-template/PROPOSAL CARAKA (2).docx` (identitas dan preseden struktur).
