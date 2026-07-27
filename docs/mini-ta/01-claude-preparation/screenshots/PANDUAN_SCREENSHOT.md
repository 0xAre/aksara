# Panduan Pengambilan Screenshot AKSARA

**Untuk**: Rafi Putra Fadlurrahman (user testing) dan Mahendra Nur Hidayat (dokumentasi akhir).
**Target**: 4 file PNG. Waktu perkiraan 20-30 menit, sekali duduk.
**Tidak perlu install Rust atau clone repo** — cukup unduh satu file binary dari GitHub.

Hasilnya dipakai sebagai Gambar di BAB IV dan BAB V laporan. Setelah selesai, kabari Andika untuk didaftarkan ke `11_FIGURE_MANIFEST.md`.

---

## Aturan yang TIDAK BOLEH dilanggar

Ini bukan formalitas — melanggarnya membuat gambar tidak bisa dipakai sama sekali di laporan:

1. **Screenshot layar asli.** Jangan bikin mockup, jangan edit gambar, jangan tempel teks.
2. **Jangan ubah tampilan aplikasi** demi foto yang lebih bagus.
3. **Passphrase dummy saja.** Pakai `demo-mini-ta-2026` di seluruh langkah. Jangan pakai passphrase asli milik siapa pun.
4. **Jangan ada rahasia terlihat** di layar: private key, token, password, isi chat pribadi.
5. **Nickname dan pesan chat pakai data dummy.** Jangan nama/nomor/alamat asli.
6. Sebelum memotret, **tutup jendela lain** yang mungkin memuat data pribadi (WhatsApp Web, email, dsb.).

---

## Langkah 0 — Unduh binary

Buka halaman rilis: **https://github.com/0xAre/aksara/releases/tag/v0.2.1**

Unduh satu file sesuai sistem operasi:

| OS | File | Ukuran |
|---|---|---|
| **Windows** | `aksara-x86_64-pc-windows-msvc.exe` | 8,9 MB |
| Linux | `aksara-x86_64-unknown-linux-gnu` | 8,4 MB |
| macOS (Apple Silicon) | `aksara-aarch64-apple-darwin` | 6,1 MB |

Buat folder kerja, misalnya `D:\aksara-demo`, lalu taruh file di situ dan **ganti namanya jadi `aksara.exe`** (Windows) atau `aksara` (Linux/macOS).

### Verifikasi file (disarankan, 10 detik)

Windows PowerShell:

```bash
Get-FileHash aksara.exe -Algorithm SHA256
```

Hasilnya harus persis: `C04D8A35D03064E31527C8793ACC03C5EB30975EDF3710042F2E8D4AF1A59066`

Linux/macOS:

```bash
shasum -a 256 aksara
```

Linux harus `6f4c865c...124ed`, macOS `49c2fd34...5de1d2`.

### Windows: izinkan file berjalan

Binary ini tidak ditandatangani digital, jadi SmartScreen akan menahan. Klik kanan `aksara.exe` → **Properties** → centang **Unblock** → OK. Kalau muncul layar biru "Windows protected your PC", klik **More info** → **Run anyway**.

### Linux/macOS: beri izin eksekusi

```bash
chmod +x aksara
```

macOS juga perlu: klik kanan → Open → Open, sekali saja.

---

## Persiapan sebelum memotret

1. **Perbesar jendela terminal** minimal 100 kolom × 30 baris. TUI akan terlihat sempit dan terpotong kalau terminalnya kecil — ini penyebab paling sering screenshot jadi tidak terpakai.
2. Semua perintah dijalankan **dari dalam folder kerja** (`D:\aksara-demo`).
3. Opsi `--offline` dipakai di semua langkah supaya tidak menunggu Tor bootstrap (30-60 detik) dan tidak butuh internet.
4. Cara memotret: Windows tekan `Win + Shift + S` (Snipping Tool), pilih area jendela terminal. macOS `Cmd + Shift + 4`. Linux pakai tool bawaan desktop.

---

## Screenshot 1 — Antarmuka utama

**Masuk ke BAB IV.1.** Ini bukti visual bahwa aplikasinya nyata dan berjalan.

```bash
.\aksara.exe --offline --vault demo-a.key
```

1. Vault belum ada, jadi aplikasi meminta membuat identitas baru. Ketik passphrase `demo-mini-ta-2026`, tekan **Enter**.
2. Ikuti layar inisialisasi sampai selesai (tekan **Enter** bila diminta).
3. Setelah masuk layar utama (daftar kontak + badge status), **potret sekarang**.

Simpan sebagai: **`01-antarmuka-utama.png`**

Pastikan terlihat: judul AKSARA, badge status koneksi (`LAN`), dan panel daftar kontak.

---

## Screenshot 2 — Identitas dan invite code

**Masuk ke BAB IV.3** (pertukaran invite dan fingerprint).

Masih di layar yang sama, tekan tombol **`i`** untuk menampilkan invite code dan fingerprint milik sendiri.

**Potret** saat invite code dan fingerprint terlihat.

Simpan sebagai: **`02-identitas-invite.png`**

> Aman dipotret: invite code hanya berisi **public key**, bukan rahasia. Yang tidak boleh terlihat adalah passphrase — dan passphrase memang tidak pernah ditampilkan di layar ini.

Sebelum lanjut, **salin invite code ini** (tekan **`c`** untuk copy, atau catat manual). Dibutuhkan di Screenshot 3. Sebut saja ini **INVITE-A**.

Lalu tekan **`q`** untuk keluar.

---

## Screenshot 3 — Dua aplikasi saling chat

**Masuk ke BAB IV.5** (transport sesi terenkripsi). Ini screenshot terpenting — membuktikan komunikasi end-to-end benar-benar jalan, bukan sekadar unit test lulus.

Butuh **dua jendela terminal** berdampingan, keduanya di folder kerja yang sama.

**Terminal kiri** (penerima) — jalankan lebih dulu:

```bash
.\aksara.exe --offline --vault demo-a.key --listen 9000
```

Masukkan passphrase `demo-mini-ta-2026`.

**Terminal kanan** (pemanggil) — ganti `INVITE-A` dengan invite yang tadi disalin:

```bash
.\aksara.exe --offline --vault demo-b.key --name demo-a --dial 127.0.0.1:9000 --add INVITE-A
```

1. Vault B belum ada → buat identitas baru, passphrase `demo-mini-ta-2026`.
2. Di layar kontak terminal kanan, kontak `demo-a` sudah ada. Pilih dengan **↑/↓**, lalu tekan **Enter** untuk memulai koneksi.
3. Tunggu status berubah menjadi terhubung/aktif.
4. Ketik pesan dummy, tekan **Enter**. Contoh aman: `halo, ini uji coba mini-TA` dan dibalas `pesan diterima, sesi aktif`.
5. Kirim 2-3 pesan bolak-balik supaya percakapannya terlihat hidup.
6. **Potret kedua terminal sekaligus** dalam satu gambar (atur berdampingan). Kalau sulit, potret masing-masing dan beri nama `03-komunikasi-a.png` dan `03-komunikasi-b.png`.

Simpan sebagai: **`03-komunikasi-dua-instance.png`**

> **Kalau gagal terhubung**: penyebab paling umum adalah invite code tersalin tidak utuh. Panjangnya harus tepat **86 karakter**. Ulangi Screenshot 2, salin ulang dengan tombol `c`.
>
> Sisi pemanggil **wajib** punya kontak tujuan — itu sebabnya `--add` dipakai. Tanpa itu koneksi ditolak, karena protokol Noise_IK mensyaratkan pemanggil sudah mengetahui kunci publik lawan sebelum handshake dimulai. Ini perilaku desain, bukan bug.

Setelah selesai, tekan **Esc** lalu **`q`** di kedua terminal.

---

## Screenshot 4 — Verifikasi vault: deterministik dan menolak passphrase salah

**Masuk ke BAB V.2** (hasil EXP-01). BAB V saat ini seluruhnya berisi angka tanpa satu pun gambar — screenshot ini yang menutupinya.

Jalankan tiga perintah berikut **berurutan di satu terminal**, jangan dibersihkan layarnya di antara perintah:

```bash
.\aksara.exe id --vault demo-a.key --offline
```

Masukkan passphrase `demo-mini-ta-2026`. Catat invite dan fingerprint yang tercetak.

```bash
.\aksara.exe id --vault demo-a.key --offline
```

Passphrase sama lagi. **Hasilnya harus persis identik** dengan perintah pertama.

```bash
.\aksara.exe id --vault demo-a.key --offline
```

Kali ini ketik passphrase **salah**, misalnya `passphrase-salah`. Harus muncul `Error: vault could not be opened`.

**Potret** seluruh terminal sehingga ketiga hasil terlihat dalam satu gambar.

Simpan sebagai: **`04-verifikasi-vault.png`**

Ini sekaligus membuktikan dua hal untuk laporan: `unseal` bersifat deterministik, dan penolakan passphrase salah memakai pesan generik yang tidak membocorkan penyebab kegagalan.

---

## Opsional — Screenshot 5: hasil `cargo test`

Hanya bisa diambil oleh yang punya source code dan toolchain Rust terpasang (**Andika**). Jalankan dari root repositori:

```bash
cargo test --release
```

Potret bagian akhir yang menampilkan `test result: ok. 46 passed; 0 failed`. Simpan sebagai `05-hasil-pengujian.png`.

Lewati saja kalau merepotkan — Screenshot 4 sudah cukup mewakili BAB V.

---

## Setelah selesai

1. Kumpulkan file PNG:

   ```
   01-antarmuka-utama.png
   02-identitas-invite.png
   03-komunikasi-dua-instance.png
   04-verifikasi-vault.png
   05-hasil-pengujian.png   (opsional)
   ```

2. **Periksa ulang setiap gambar** sebelum dikirim:
   - Tidak ada passphrase terketik yang terlihat.
   - Tidak ada data pribadi di jendela lain yang ikut terpotret.
   - Teks terbaca jelas, tidak buram, tidak terpotong.

3. Kirim ke Andika untuk ditaruh di `docs/mini-ta/01-claude-preparation/screenshots/`.

4. Hapus file demo di folder kerja: `demo-a.key`, `demo-b.key`. Isinya cuma identitas dummy, tapi lebih rapi dibersihkan.

---

## Ringkasan perintah

| Screenshot | Perintah |
|---|---|
| 1 — Antarmuka utama | `.\aksara.exe --offline --vault demo-a.key` |
| 2 — Identitas/invite | (lanjutan #1, tekan `i`) |
| 3 — Komunikasi, terminal kiri | `.\aksara.exe --offline --vault demo-a.key --listen 9000` |
| 3 — Komunikasi, terminal kanan | `.\aksara.exe --offline --vault demo-b.key --name demo-a --dial 127.0.0.1:9000 --add INVITE-A` |
| 4 — Verifikasi vault | `.\aksara.exe id --vault demo-a.key --offline` (3×, yang ketiga passphrase salah) |
| 5 — Pengujian (opsional) | `cargo test --release` |

## Tombol TUI yang dipakai

| Tombol | Fungsi |
|---|---|
| `i` | Tampilkan/sembunyikan invite code sendiri |
| `c` | Salin invite code |
| `a` | Tambah kontak dari invite code |
| `↑` `↓` | Pilih kontak |
| `Enter` | Mulai koneksi (di layar kontak) / kirim pesan (di chat) |
| `Esc` | Keluar dari ruang chat |
| `q` | Keluar aplikasi |
| `Ctrl+B` | Sembunyikan isi chat (blur) |
| `Ctrl+C` | Keluar paksa |

---

**Sumber**: rilis `v0.2.1` (2026-07-26). Daftar dan aturan screenshot mengikuti `CLAUDE_PREPARATION_BRIEF.md` TAHAP 12 (2-4 screenshot, butir larangan 3-9). Alur `--listen`/`--dial`/`--add` dan daftar tombol diverifikasi langsung terhadap `src/session/mod.rs` dan `src/tui/mod.rs`, bukan diperkirakan.
