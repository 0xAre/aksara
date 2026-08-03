# Generation Log — AKSARA Laporan Final

## Identitas keluaran

- Dokumen: `docs/mini-ta/04-output/AKSARA_LAPORAN_FINAL.docx`
- Tanggal penyelesaian: 2026-07-30
- Base commit saat generasi: `861a022`
- Ukuran akhir: 2.147.970 byte
- SHA-256: `EB413B431F0FFE5F20D8B81521F383E15E3B83D1FC4833C32CA9AAD5038F4ED3`
- Jumlah halaman menurut Microsoft Word: 71
- Jumlah kata menurut Microsoft Word: 8.788
- Status marker `[PERLU KONFIRMASI]`: tidak ada

## Sumber dan metode

Dokumen dibangun dari working copy template
`docs/mini-ta/03-codex-work/template-distill/Cetak_TA_rev3_working.docx`.
Template sumber asli tetap berada di
`docs/mini-ta/00-template/Cetak TA_rev3.docx` dengan SHA-256
`947B3FAE76EF0E934A25AE85F33842182953761D565838034838D1E68E33F2F`.
Isi laporan diambil dari content pack, peta klaim–evidence–sitasi, manifest,
tabel, diagram, screenshot, hasil eksperimen, dan 40 entri bibliografi yang
sudah disiapkan di `docs/mini-ta/01-claude-preparation/`.

Microsoft Word digunakan untuk memperbarui daftar isi, daftar gambar, daftar
tabel, `PAGEREF`, dan nomor halaman; hasil pembaruan kemudian disimpan di
dokumen. Pengaturan pembaruan otomatis saat membuka dokumen dinonaktifkan
setelah field selesai diperbarui agar pembukaan ulang tidak mengubah layout
tanpa sengaja.

## Komposisi

### Gambar

- Sampul: 1 logo institusi.
- BAB IV: 17 gambar.
- BAB V: 1 gambar.
- Total gambar isi: 18.
- Total objek gambar inline termasuk logo: 19.

### Tabel

- BAB I: 1 tabel.
- BAB II: 4 tabel.
- BAB III: 1 tabel.
- BAB IV: 5 tabel.
- BAB V: 2 tabel.
- Total: 13 tabel.

### Referensi

- Daftar pustaka: 40 entri bernomor `[1]`–`[40]`.
- Seluruh 40 nomor muncul sebagai sitasi pada tubuh laporan.

## QA struktur dan semantik

- Heading: 7 `Heading 1` dan 34 `Heading 2`.
- Bagian dokumen: 29 section; A4 portrait dan landscape diterapkan sesuai
  kebutuhan tabel.
- Margin seluruh section: kiri 4 cm; kanan, atas, dan bawah 3 cm.
- Penomoran halaman hanya di-restart pada awal bagian Romawi dan awal BAB I;
  section berikutnya meneruskan nomor Arab.
- Seluruh gambar bersifat inline; tidak ada objek floating.
- Footer memuat nomor halaman dan teks `Politeknik Siber dan Sandi Negara`.
- Tidak ditemukan placeholder sitasi, marker konfirmasi, istilah proyek
  CARAKA/CLAMP, atau klaim terlarang yang diaudit.
- Audit semantik akhir: **PASS**.

## QA render

Seluruh halaman render acuan Word diperiksa. Setelah perbaikan akhir, dokumen
dirender kembali menjadi 71 halaman dan dibandingkan dengan render acuan:
68 halaman mempertahankan isi yang identik; tiga halaman depan berubah hanya
karena pembaruan nomor pada daftar isi, daftar gambar, dan daftar tabel.
Halaman yang terkena perubahan penomoran daftar, pemenggalan Tabel 4.1, serta
transisi setelah tabel diperiksa ulang secara individual.

Masalah yang ditemukan dan diselesaikan:

1. Nomor halaman sempat restart pada section tabel landscape — marker restart
   turunan dihapus.
2. Penomoran perincian sempat berlanjut lintas subbab — diubah menjadi daftar
   huruf yang restart per kelompok.
3. Sel evidence terakhir pada Tabel 4.1 sempat terpisah sebagai fragmen satu
   baris — bobot kolom disesuaikan.
4. Setelah perbaikan Tabel 4.1 sempat tersisa satu halaman landscape kosong —
   paragraf kosong sebelum section break dihapus; jumlah halaman turun dari
   72 menjadi 71.
5. Ekspor PDF final melalui otomasi Word bersifat intermittent/hang pada
   lingkungan ini. Pemeriksaan akhir diselesaikan dengan render Word acuan,
   statistik pagination Word 71 halaman, render alternatif 71 halaman, dan
   perbandingan piksel terarah. Tidak ada masalah dokumen yang tersisa.

## Catatan penggunaan

Field di dokumen akhir sudah diperbarui. Jika isi, heading, caption, section,
atau pagination diubah lagi, buka dokumen di Microsoft Word lalu tekan
`Ctrl+A`, kemudian `F9`, dan periksa kembali daftar isi/gambar/tabel serta
nomor halaman sebelum menyerahkan dokumen.
