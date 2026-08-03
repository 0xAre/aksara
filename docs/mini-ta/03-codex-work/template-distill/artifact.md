# Kontrak Eksekusi Template — AKSARA

## Referensi

- Referensi otoritatif: `E:\Project APP\AKSARA\docs\mini-ta\00-template\Cetak TA_rev3.docx`
- SHA-256 referensi: `947B3FAECD4899E9EA32F8402A26D3517D1D4931887324590725686705E33F2F`
- Ukuran referensi: 2.046.100 byte
- Hasil repaginasi Word: 44 halaman
- Jumlah section: 19
- Bukti audit: `section-audit.txt`, `style-evidence.json`, `heading-audit.txt`, `images-audit.txt`, dan `fields-report.txt`
- Bukti visual terbatas: `render-word/page-001.png` s.d. halaman yang berhasil diraster; ekspor seluruh referensi berhenti pada objek lama di halaman tertentu. Spesifikasi format terverifikasi `16_DOCUMENT_FORMAT_SPEC.md` menjadi otoritas bila ada perbedaan.

## Sistem Halaman

- A4 potret: 8,27 × 11,69 inci.
- Margin: kiri 4 cm; kanan, atas, dan bawah 3 cm.
- Jarak header/footer sumber: 1,25 cm; nomor halaman bagian awal ditempatkan 2,5 cm dari tepi bawah sesuai spesifikasi resmi.
- Referensi memiliki 19 section, termasuk satu section lanskap yang hanya relevan bagi tabel proyek contoh. Dokumen AKSARA menggunakan section potret, kecuali tabel yang benar-benar tidak dapat dibuat terbaca dalam potret.
- Sampul tidak bernomor. Bagian awal memakai angka Romawi kecil. BAB I hingga Daftar Pustaka memakai angka Arab mulai dari 1.

## Tipografi dan Peran Paragraf

- Body/Normal: Times New Roman 12 pt, justify, tanpa indentasi baris pertama, spasi baris multiple 1,15, dan satu baris kosong antarparagraf.
- Judul bab: Times New Roman 12 pt, tebal, kapital semua, rata tengah; `BAB <Romawi>` dan judul bab ditulis pada dua baris.
- Subbab: Times New Roman 12 pt, tebal, kapital semua, rata kiri; nomor Romawi.Arab.
- Anak subbab: Times New Roman 12 pt, tebal, Title Case, rata kiri; nomor Romawi.Arab.Arab.
- Caption: Times New Roman 12 pt, Title Case; caption tabel di atas dan caption gambar di bawah. Caption lebih dari satu baris memakai spasi tunggal.
- Abstrak, daftar isi/gambar/tabel, dan daftar pustaka memakai spasi tunggal.
- Footer institusi: Arial 10 pt, tebal, rata kanan, dari Abstrak sampai Daftar Pustaka.
- Istilah asing dicetak miring saat merupakan istilah, bukan nama protokol/produk.

## Gaya Word

- Sumber memuat `Normal`, `Head1`, `Head3`, `Heading 1`, `Heading 2`, `Heading 3`, `Caption`, dan `List Paragraph`.
- Sumber banyak memakai direct formatting dan heading semu. Dokumen AKSARA harus memperbaikinya dengan style Word riil:
  - `Heading 1` untuk judul bab dan bagian awal/akhir yang harus masuk navigasi.
  - `Heading 2` untuk subbab dan sebagai level terakhir Daftar Isi.
  - `Heading 3` untuk anak subbab; tidak dimasukkan ke Daftar Isi.
  - `Caption` untuk semua caption gambar/tabel.
- Nilai tipografi style di atas diselaraskan dengan `16_DOCUMENT_FORMAT_SPEC.md`; spesifikasi resmi menimpa default bawaan template (misalnya Caption 9 pt miring pada sumber tidak dipakai).

## Tabel dan Daftar

- Tabel memakai lebar eksplisit yang tidak melebihi 14 cm area teks potret, grid kolom eksplisit, header berulang, padding sel konsisten, dan tinggi baris otomatis.
- Tabel yang sangat lebar boleh memakai halaman lanskap A4 dengan margin resmi, tetapi preferensi pertama adalah memperpendek header, membungkus teks, dan menyesuaikan lebar kolom.
- Perincian memakai penomoran Word nyata dengan urutan `a.` → `a)` → `(a)` bila diperlukan; tidak memakai bullet/nomor palsu sebagai teks.

## Komponen

- Sampul: blok simetris di tengah, logo institusi dari `template-package/word/media/image2.png`, jenis dokumen, judul, tiga nama/NIM, program studi, institusi, dan tahun.
- Footer: teks institusi dan field nomor halaman sesuai section.
- Daftar Isi, Daftar Gambar, dan Daftar Tabel: field Word otomatis. `w:updateFields=true` wajib diaktifkan.
- Gambar: selalu inline, rata tengah, maksimal selebar area teks, dan caption tepat setelah gambar.
- Tabel: caption tepat sebelum tabel.
- Sitasi: IEEE numerik sebelum tanda baca; urutan Daftar Pustaka sama dengan kemunculan pertama.

## Alur Konten dan Slot

- Seluruh body substansi proyek QRNG pada referensi berstatus `REMOVE`.
- Bagian formal sidang, kata pengantar, abstract Inggris, notasi, lampiran, dan riwayat hidup berstatus `REMOVE`.
- Bagian yang dibangun ulang: Sampul; Abstrak Indonesia; Daftar Isi; Daftar Gambar; Daftar Tabel; BAB I–VI; Daftar Pustaka.
- Styles, theme, logo, dan pola geometri halaman berstatus `PRESERVE/REUSE`.
- Header/footer lama boleh diganti karena struktur section dan penomoran AKSARA berbeda secara eksplisit dari referensi.

## Package Preservation

- Referensi asli tidak boleh dimodifikasi.
- Salinan kerja boleh membersihkan seluruh isi `word/document.xml` selain `sectPr`, lalu membangun ulang body.
- `word/styles.xml`, `word/theme/*`, dan aset logo institusi dipertahankan sebagai sumber style/visual.
- Relasi gambar dan field lama yang tidak lagi dirujuk boleh menjadi orphan sementara, tetapi final harus lolos audit paket, field, gambar, section, dan heading.

## Fidelity Gates

- Geometri A4 dan margin harus cocok spesifikasi.
- Semua heading memakai style Word yang benar.
- Footer institusi konsisten dari Abstrak sampai Daftar Pustaka.
- Gambar/tabel tidak keluar margin dan seluruh caption berpasangan dengan objeknya.
- Tidak ada substansi proyek contoh maupun istilah terlarang CARAKA.
- Field Word diperbarui melalui Word bila tersedia; bila pembaruan tidak dapat disimpan secara deterministik, `w:updateFields=true` dan instruksi `Ctrl+A` lalu `F9` dicatat.
- Final DOCX wajib dirender dari Microsoft Word ke PDF dan setiap halaman diperiksa.
