# 16 — Spesifikasi Format Dokumen AKSARA

Dokumen ini adalah **aturan format yang harus diikuti Codex** saat menyusun DOCX. Disusun 2026-07-27 dengan mengekstrak aturan nyata dari dua file di `docs/mini-ta/00-template/`, lalu **menyederhanakannya** sesuai instruksi eksplisit pengguna: dokumen ini adalah tugas mata kuliah, bukan Tugas Akhir/skripsi dengan sidang.

## 1. Sumber dan Status Setiap Aturan

| Sumber | Isi sebenarnya | Dipakai untuk |
|---|---|---|
| `00-template/Cetak TA_rev3.docx` | **TA orang lain yang sudah dicetak** (topik QRNG, penulis Naval Indra Waskita, Poltek SSN 2025) — contoh terisi, bukan template kosong | Aturan tipografi, margin, penomoran, caption, gaya sitasi. Diukur langsung dari XML dokumen, bukan diperkirakan |
| `00-template/PROPOSAL CARAKA (2).docx` | Proposal kelompok yang sama untuk **mata kuliah yang sama** ("PROPOSAL TUGAS IMPLEMENTASI KRIPTOGRAFI") | Identitas anggota, dan **preseden struktur** — proposal ini sudah menghilangkan seluruh lembar formal, sehingga penyederhanaan di §3 punya dasar nyata, bukan asumsi |

**Batas penting**: `PROPOSAL CARAKA` adalah proyek berbeda (mesh offline, Ascon, protokol CLAMP). `AGENTS.md` melarang mencampur faktanya dengan AKSARA. Dari file itu **hanya identitas anggota dan struktur dokumen** yang diambil — tidak satu pun fakta teknis, algoritma, tabel, atau referensinya boleh masuk ke dokumen AKSARA.

## 2. Identitas Dokumen

| Field | Nilai | Status |
|---|---|---|
| Jenis dokumen | Tugas Mata Kuliah Implementasi Kriptografi | CONFIRMED |
| Judul | **AKSARA (*Authenticated Key-based Secure Autonomous Relay Architecture*): Implementasi dan Evaluasi Keamanan Protokol Noise_IK, Manajemen Kunci, dan Threat Model pada Aplikasi Chat Terminal P2P Serverless** | **NEEDS_CONFIRMATION — lihat catatan di bawah** |
| Penulis 1 | Andika Aryansyach Fauzan (2322101878) | CONFIRMED |
| Penulis 2 | Mahendra Nur Hidayat (2322101937) | CONFIRMED |
| Penulis 3 | Rafi Putra Fadlurrahman (2322101963) | CONFIRMED |
| Program studi | Rekayasa Sistem Kriptografi | CONFIRMED |
| Institusi | Politeknik Siber dan Sandi Negara | CONFIRMED |
| Tahun | 2026 | CONFIRMED |

**Catatan judul**: pengguna menginstruksikan nama panjang AKSARA masuk ke judul. Ini **menimpa** `09_SCOPE_AND_TEAM_PLAN.md` §7 yang semula menyatakan nama panjang hanya dipakai sebagai konteks di BAB I. Bentuk di atas menggabungkan instruksi tersebut dengan isi Judul #3 (rekomendasi §7) dan mengikuti pola judul proposal CARAKA (`<NAMA> (<kepanjangan>): <deskripsi>`). Bagian setelah tanda titik dua masih bisa dipendekkan bila dirasa terlalu panjang.

## 3. Struktur Dokumen (Disederhanakan)

### 3.1 Yang DIPAKAI

| # | Bagian | Catatan |
|---|---|---|
| 1 | **Sampul** | Judul, 3 nama + NIM, program studi, institusi, tahun. Tanpa logo kecuali diminta |
| 2 | **Daftar Isi** | Otomatis dari heading Word |
| 3 | **Daftar Gambar** | 7 diagram (`11_FIGURE_MANIFEST.md`) |
| 4 | **Daftar Tabel** | 13 tabel (`13_TABLE_MANIFEST.md`) |
| 5 | **BAB I — PENDAHULUAN** | 6 subbab |
| 6 | **BAB II — KAJIAN PUSTAKA** | 10 subbab |
| 7 | **BAB III — METODOLOGI PENELITIAN** | 5 subbab |
| 8 | **BAB IV — PERANCANGAN DAN IMPLEMENTASI** | 7 subbab |
| 9 | **BAB V — PENGUJIAN DAN ANALISIS** | 3 subbab |
| 10 | **BAB VI — PENUTUP** | 3 subbab |
| 11 | **Daftar Pustaka** | 40 entry (`references/REFERENCES.bib`) |

Opsional, boleh ditambahkan bila diminta dosen:

- **Abstrak** (1 halaman, bahasa Indonesia saja) — tidak ada di proposal CARAKA, tapi murah dibuat dan menambah bobot akademik. **Abstract bahasa Inggris tidak perlu.**
- **Lampiran** — kode sumber tidak perlu dilampirkan karena repositori sudah menjadi luaran; cukup dirujuk.

### 3.2 Yang DIHAPUS dan alasannya

| Bagian di `Cetak TA_rev3.docx` | Alasan dihapus |
|---|---|
| Lembar Judul (duplikat sampul) | Redundan dengan sampul |
| Lembar Pernyataan Orisinalitas | Butuh tanda tangan elektronik bersertifikat — artefak sidang TA, bukan tugas mata kuliah |
| Lembar Persetujuan | Butuh tanda tangan Pembimbing Materi |
| Lembar Pengesahan | Butuh tanda tangan Ketua Penguji + Penguji I + Penguji II. **Tidak ada sidang** untuk tugas mata kuliah |
| Lembar Pernyataan Persetujuan Publikasi | Penyerahan Hak Bebas Royalti ke institusi — hanya berlaku untuk TA resmi |
| Kata Pengantar | Ucapan terima kasih personal; tidak relevan untuk tugas kelompok satu mata kuliah |
| Abstract (Inggris) | Persyaratan TA resmi, berlebihan untuk tugas mata kuliah |
| Daftar Notasi | AKSARA tidak memakai notasi matematis formal yang perlu didaftar |
| Daftar Lampiran | Tidak ada lampiran (lihat §3.1) |
| Daftar Riwayat Hidup | Artefak TA resmi |

**Dasar penyederhanaan**: proposal kelompok ini untuk mata kuliah yang sama sudah memakai struktur ringkas — hanya sampul, daftar isi/gambar/tabel, isi, dan daftar pustaka. Jadi penghapusan di atas mengikuti preseden yang sudah diterima, bukan keputusan sepihak.

## 4. Format Halaman dan Tipografi

Seluruh nilai berikut **diukur langsung** dari `word/document.xml` dan `word/styles.xml` milik `Cetak TA_rev3.docx`, bukan diperkirakan.

| Aspek | Nilai | Bukti |
|---|---|---|
| Ukuran kertas | **A4** (210 × 297 mm) | `<w:pgSz w:w="11906" w:h="16838">` |
| Margin kiri | **4 cm** | `w:left="2268"` twips ÷ 567 |
| Margin atas, kanan, bawah | **3 cm** | `w:top/right/bottom="1701"` twips ÷ 567 |
| Font | **Times New Roman** | 935 kemunculan, dominan mutlak |
| Ukuran badan teks | **12 pt** | `<w:sz w:val="24">` (half-point), 1886 kemunculan |
| Ukuran judul sampul | 16 pt | `w:val="32"`, 24 kemunculan |
| Ukuran heading besar | 14 pt | `w:val="28"`, 64 kemunculan |
| Ukuran caption / isi tabel | 9–10 pt | style `Caption` `w:sz="18"`; sebagian isi tabel `w:val="20"` |
| Perataan badan teks | **Rata kiri-kanan (justify)** | `<w:jc w:val="both">` dominan (360 vs 65 rata kiri) |
| Spasi baris badan teks | **1,15** | `w:line="276"` dengan `lineRule="auto"` (276 ÷ 240) |
| Font kode sumber | Courier New | 45 kemunculan |

**Peringatan spasi baris**: nilai 1,15 adalah apa yang benar-benar dipakai contoh TA tersebut. Banyak panduan penulisan Indonesia mensyaratkan **1,5**. Bila dosen punya panduan tertulis yang menyebut 1,5, **panduan tertulis menang** — angka di sini adalah hasil pengukuran satu contoh, bukan kutipan dari peraturan resmi.

## 5. Penomoran Heading

Pola yang dipakai contoh TA:

| Level | Bentuk | Contoh |
|---|---|---|
| BAB | `BAB <romawi>` pada baris pertama, judul BAB pada baris kedua, keduanya kapital dan rata tengah | `BAB I` / `PENDAHULUAN` |
| Subbab (level 2) | **KAPITAL SEMUA**, bernomor otomatis | `LATAR BELAKANG`, `RUMUSAN MASALAH` |
| Sub-subbab (level 3) | Kapital di awal kata, bernomor `<romawi-bab>.<n>.<n>` | `II.1.1 Quantum Random Number Generator` |

Untuk AKSARA, penomoran level 3 disarankan memakai angka Arab (`2.1.1`) agar konsisten dengan penomoran subbab di `14_CHAPTER_CONTENT_PACK.md` yang sudah dipakai lintas seluruh dokumen persiapan. **Konsistensi internal lebih penting daripada meniru persis contoh** — yang penting satu pola dipakai dari BAB I sampai BAB VI.

## 6. Gambar dan Tabel

| Aturan | Ketentuan |
|---|---|
| Penomoran | Per BAB: `Gambar <bab>.<urut>`, `Tabel <bab>.<urut>` — contoh `Gambar 4.1`, `Tabel 5.2` |
| Posisi caption gambar | **Di bawah** gambar |
| Posisi caption tabel | **Di atas** tabel |
| Gaya caption | Times New Roman 10 pt, rata tengah |
| Wajib dirujuk di teks | Setiap gambar/tabel harus disebut dalam kalimat sebelum kemunculannya (mis. "Gambar 4.1 menunjukkan…") — tidak boleh muncul tanpa rujukan |
| Sumber gambar AKSARA | `diagrams/rendered/png/` (7 diagram, resolusi 2×) untuk disisipkan ke DOCX; versi SVG tersedia bila perlu kualitas cetak lebih tinggi |

**Konsistensi penomoran**: contoh TA memakai bentuk tidak konsisten (`Gambar 1. 1` dengan spasi vs `Gambar 2.1` tanpa spasi). Untuk AKSARA pakai **`Gambar 4.1`** (tanpa spasi setelah titik) secara seragam.

## 7. Sitasi dan Daftar Pustaka

- **Gaya: IEEE numerik.** Kedua dokumen sumber memakainya secara konsisten — rujukan dalam teks berbentuk `[1]`, `[5]`, `[7][8][9]`, dan daftar pustaka diurutkan berdasarkan urutan kemunculan pertama.
- Sumber referensi AKSARA: `references/REFERENCES.bib` (**40 entry terverifikasi**). Jangan menambah referensi baru tanpa verifikasi — `AGENTS.md` melarang mengarang DOI/penulis/tahun/venue.
- Format entry mengikuti pola pada contoh: penulis, judul (dalam tanda kutip untuk artikel, miring untuk buku), venue/penerbit, kota, tahun; untuk sumber daring tambahkan `[Online]. Available: <URL>`.
- Setiap klaim teori wajib bersitasi; setiap klaim implementasi wajib menunjuk path+symbol source code, bukan sitasi. Aturan ini berasal dari `AGENTS.md` dan **lebih ketat** daripada aturan format mana pun di sini.

## 8. Penomoran Halaman

| Bagian | Penomoran |
|---|---|
| Sampul | Tidak diberi nomor |
| Daftar isi/gambar/tabel | Angka romawi kecil (`i`, `ii`, `iii`) |
| BAB I sampai Daftar Pustaka | Angka Arab (`1`, `2`, `3`) mulai dari BAB I |

Posisi nomor halaman mengikuti contoh: bawah-tengah atau kanan-atas — belum dapat dipastikan dari ekstraksi XML, **NEEDS_CONFIRMATION**, dan tidak berdampak besar bila salah pilih.

## 9. Yang Masih Perlu Dikonfirmasi

| # | Item | Dampak bila salah |
|---|---|---|
| 1 | Bentuk final judul (§2) | Perlu diganti di sampul dan daftar isi — murah diperbaiki |
| 2 | Spasi baris 1,15 vs 1,5 (§4) | Mengubah jumlah halaman; perlu satu kali set ulang |
| 3 | Perlu/tidaknya Abstrak (§3.1) | Menambah satu halaman |
| 4 | Posisi nomor halaman (§8) | Kosmetik |
| 5 | Apakah dosen mensyaratkan bagian lain yang tidak ada di kedua dokumen sumber | Bisa berarti bagian baru harus ditulis |

## Referensi

Tidak ada referensi teori baru. Seluruh isi dokumen ini adalah hasil ekstraksi dari `00-template/Cetak TA_rev3.docx` (aturan format, diukur dari XML) dan `00-template/PROPOSAL CARAKA (2).docx` (identitas anggota dan preseden struktur untuk mata kuliah yang sama).
