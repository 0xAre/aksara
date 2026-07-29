# Panduan Pengambilan Screenshot AKSARA

**Untuk**: Rafi Putra Fadlurrahman (user testing) dan Mahendra Nur Hidayat (dokumentasi akhir).
**Target**: 6 file PNG wajib + 1 opsional.
**Tidak perlu install Rust atau clone repo** — cukup unduh satu file binary dari GitHub.

Hasilnya dipakai sebagai Gambar di BAB IV dan BAB V laporan. Setelah selesai, kabari Andika untuk didaftarkan ke `11_FIGURE_MANIFEST.md`.

## Pembagian kerja

| Bagian | Butuh apa | Siapa |
|---|---|---|
| **Sesi A** — Screenshot 1, 2, 3 | 1 laptop, tanpa internet | Bisa dikerjakan sendiri |
| **Sesi B** — Screenshot 4 | **2 laptop di WiFi yang sama** | Rafi + Mahendra bersamaan |
| **Sesi C** — Screenshot 5, 6 | 1 laptop, **butuh internet** | Bisa dikerjakan sendiri |

Sesi A dan C bisa dikerjakan siapa saja sendirian. Hanya Sesi B yang perlu janjian berdua.

---

## Aturan yang TIDAK BOLEH dilanggar

Ini bukan formalitas — melanggarnya membuat gambar tidak bisa dipakai sama sekali di laporan:

1. **Screenshot layar asli.** Jangan bikin mockup, jangan edit gambar, jangan tempel teks.
2. **Jangan ubah tampilan aplikasi** demi foto yang lebih bagus.
3. **Passphrase dummy saja.** Pakai `demo-mini-ta-2026` di seluruh langkah. Jangan pakai passphrase asli milik siapa pun.
4. **Jangan ada rahasia terlihat** di layar: private key, token, password, isi chat pribadi.
5. **Nickname dan pesan chat pakai data dummy.** Jangan nama/nomor/alamat asli.
6. Sebelum memotret, **tutup jendela lain** yang mungkin memuat data pribadi.
7. **Alamat `.onion` boleh dipotret** — itu alamat layanan publik, bukan kunci rahasia. Tapi jangan dibagikan di luar laporan.

---

## Langkah 0 — Unduh binary

Buka halaman rilis: **https://github.com/0xAre/aksara/releases/tag/v0.2.1**

Unduh satu file sesuai sistem operasi:

| OS | File | Ukuran |
|---|---|---|
| **Windows** | `aksara-x86_64-pc-windows-msvc.exe` | 8,9 MB |
| Linux | `aksara-x86_64-unknown-linux-gnu` | 8,4 MB |
| macOS (Apple Silicon) | `aksara-aarch64-apple-darwin` | 6,1 MB |

Buat folder kerja, misalnya `D:\aksara-demo`, taruh file di situ dan **ganti namanya jadi `aksara.exe`** (Windows) atau `aksara` (Linux/macOS).

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
3. Cara memotret: Windows `Win + Shift + S`, macOS `Cmd + Shift + 4`, Linux pakai tool bawaan desktop.

**Tentang opsi `--offline`**: mematikan Tor sehingga aplikasi langsung jalan tanpa menunggu bootstrap. Dipakai di Sesi A dan B. **Tidak dipakai** di Sesi C, karena justru Tor yang mau dibuktikan.

---

# SESI A — Satu laptop, tanpa internet

## Screenshot 1 — Antarmuka utama

**Masuk ke BAB IV.1.** Bukti visual bahwa aplikasinya nyata dan berjalan.

```bash
.\aksara.exe --offline --vault demo-a.key
```

1. Vault belum ada, jadi aplikasi meminta membuat identitas baru. Ketik passphrase `demo-mini-ta-2026`, tekan **Enter**.
2. Ikuti layar inisialisasi sampai selesai (tekan **Enter** bila diminta).
3. Setelah masuk layar utama (daftar kontak + badge status), **potret sekarang**.

Simpan sebagai: **`01-antarmuka-utama.png`**

Pastikan terlihat: judul AKSARA, badge status koneksi (`LAN`), dan panel daftar kontak.

## Screenshot 2 — Identitas dan invite code

**Masuk ke BAB IV.3** (pertukaran invite dan fingerprint).

Masih di layar yang sama, tekan tombol **`i`** untuk menampilkan invite code dan fingerprint sendiri. **Potret.**

Simpan sebagai: **`02-identitas-invite.png`**

> Aman dipotret: invite code hanya berisi **public key**, bukan rahasia.

Sebelum lanjut, **salin invite code ini** (tekan **`c`**, atau catat manual). Panjangnya harus tepat **86 karakter**. Sebut saja **INVITE-A** — dibutuhkan di Sesi B.

Tekan **`q`** untuk keluar.

## Screenshot 3 — Verifikasi vault: deterministik dan menolak passphrase salah

**Masuk ke BAB V.2** (hasil EXP-01). BAB V saat ini seluruhnya angka tanpa satu pun gambar.

Jalankan tiga perintah berurutan **di satu terminal, jangan dibersihkan layarnya**:

```bash
.\aksara.exe id --vault demo-a.key --offline
```

Passphrase `demo-mini-ta-2026`. Catat invite dan fingerprint yang tercetak.

```bash
.\aksara.exe id --vault demo-a.key --offline
```

Passphrase sama lagi. **Hasilnya harus persis identik** dengan perintah pertama.

```bash
.\aksara.exe id --vault demo-a.key --offline
```

Kali ini ketik passphrase **salah**, misalnya `passphrase-salah`. Harus muncul `Error: vault could not be opened`.

**Potret** seluruh terminal sehingga ketiga hasil terlihat dalam satu gambar.

Simpan sebagai: **`03-verifikasi-vault.png`**

Membuktikan dua hal sekaligus: `unseal` deterministik, dan penolakan passphrase salah memakai pesan generik yang tidak membocorkan penyebab kegagalan.

---

# SESI B — Dua laptop di WiFi yang sama

**Masuk ke BAB IV.3 dan IV.5.** Ini screenshot paling berharga dari seluruh daftar, karena satu-satunya yang membuktikan **penemuan peer otomatis lewat mDNS** benar-benar bekerja.

**Kenapa harus dua laptop**: kode sengaja menolak alamat loopback sebagai target discovery (`is_lan_dialable()` di `src/transport/lan.rs` menolak `127.0.0.1`). Jadi penemuan otomatis **secara desain tidak akan pernah jalan di satu mesin**. Ini bukan keterbatasan pengujian, melainkan perilaku yang memang dirancang begitu.

### Persiapan

1. Kedua laptop **tersambung ke WiFi yang sama**. Hotspot HP juga bisa.
2. **Matikan sementara** VPN dan firewall yang memblokir mDNS (UDP port 5353). Di Windows, saat pertama kali dijalankan biasanya muncul dialog Windows Defender Firewall — pilih **Allow access** untuk jaringan Private.
3. Salin binary `aksara.exe` ke kedua laptop.

### Langkah

**Laptop 1** — buat identitas dan ambil invite:

```bash
.\aksara.exe id --vault demo-a.key --offline
```

Salin invite yang tercetak (**INVITE-A**), kirim ke Laptop 2 lewat chat.

**Laptop 2** — buat identitas dan ambil invite:

```bash
.\aksara.exe id --vault demo-b.key --offline
```

Salin invite yang tercetak (**INVITE-B**), kirim balik ke Laptop 1.

Sekarang **kedua laptop** menjalankan perintah berikut — perhatikan: **tidak ada `--listen` maupun `--dial`**. Itu intinya, biar aplikasi mencari sendiri.

Laptop 1:

```bash
.\aksara.exe --offline --vault demo-a.key --name demo-b --add INVITE-B
```

Laptop 2:

```bash
.\aksara.exe --offline --vault demo-b.key --name demo-a --add INVITE-A
```

1. Masukkan passphrase `demo-mini-ta-2026` di keduanya.
2. Di layar kontak, pilih kontak lawan dengan **↑/↓**, tekan **Enter**.
3. Tunggu keduanya saling menemukan lewat mDNS dan sesi menjadi aktif.
4. Kirim 2-3 pesan bolak-balik. Contoh aman: `halo dari laptop 1`, dibalas `diterima di laptop 2`.
5. **Potret layar kedua laptop.** Simpan terpisah:

**`04a-lan-discovery-laptop1.png`** dan **`04b-lan-discovery-laptop2.png`**

### Kalau gagal terhubung

Coba berurutan:

1. **Invite tersalin tidak utuh** — penyebab paling sering. Panjangnya harus tepat 86 karakter.
2. **Firewall memblokir** — pastikan dialog Windows Firewall sudah di-*allow* untuk jaringan Private di kedua laptop.
3. **WiFi mengisolasi klien** — banyak WiFi kampus dan publik mengaktifkan *AP isolation* yang memblokir komunikasi antarperangkat. Pindah ke hotspot HP salah satu anggota.

**Kalau tetap gagal setelah tiga langkah di atas**, jangan dipaksakan dan jangan dikarang. Jatuhkan ke mode manual di **satu laptop** sebagai pengganti:

```bash
.\aksara.exe --offline --vault demo-a.key --listen 9000
```

```bash
.\aksara.exe --offline --vault demo-b.key --name demo-a --dial 127.0.0.1:9000 --add INVITE-A
```

Simpan sebagai **`04-komunikasi-loopback.png`** dan **beri tahu Andika bahwa yang berhasil hanya mode manual** — statusnya di laporan akan berbeda, dan itu harus ditulis apa adanya.

---

# SESI C — Satu laptop, butuh internet

Membuktikan lapisan Tor benar-benar hidup. Saat ini Tor adalah bagian yang **paling minim bukti** di seluruh dokumen — `src/transport/tor.rs` tidak punya satu pun unit test, jadi dua screenshot ini yang menutupinya.

> **Catatan**: bootstrap Tor butuh 30-60 detik dan koneksi internet. Sebagian jaringan kampus/kantor memblokir Tor — kalau gagal, pakai hotspot HP. Kalau tetap gagal, lewati Sesi C dan beri tahu Andika; statusnya akan tetap ditulis sebagai belum terverifikasi.

## Screenshot 5 — Onion address di dalam invite

Perintahnya sama seperti sebelumnya **tanpa `--offline`**:

```bash
.\aksara.exe id --vault demo-a.key
```

1. Muncul pesan `Bootstrap Tor untuk ambil onion address (~30-60 dtk)…`. Tunggu.
2. Passphrase `demo-mini-ta-2026`.
3. Invite yang tercetak sekarang **jauh lebih panjang** dan berakhiran `@xxxxx.onion`, serta baris `Transport:` berubah dari `LAN` menjadi menyertakan Tor.
4. **Potret** seluruh terminal.

Simpan sebagai: **`05-onion-invite.png`**

Ini bukti bahwa onion service versi 3 benar-benar terbentuk dan alamatnya tertanam ke dalam invite — bukan sekadar ada di kode.

> Pembanding untuk laporan: invite LAN-only 86 karakter, invite dengan onion sekitar 149 karakter. Selisihnya adalah alamat `.onion` yang di-*append*.

## Screenshot 6 — Badge TOR aktif di TUI

```bash
.\aksara.exe --vault demo-a.key
```

1. Passphrase `demo-mini-ta-2026`.
2. TUI langsung tampil dengan badge `LAN` — Tor masih bootstrap di latar belakang.
3. **Tunggu 30-60 detik** sampai badge berubah menyertakan `TOR`.
4. **Potret** saat badge sudah menampilkan status Tor aktif.

Simpan sebagai: **`06-badge-tor-aktif.png`**

Ini memperlihatkan perilaku yang dijelaskan di BAB IV: TUI tidak diblokir menunggu Tor, melainkan tetap responsif sementara bootstrap berjalan di latar belakang.

---

# Opsional — Screenshot 7: hasil `cargo test`

Hanya bisa diambil oleh yang punya source code dan toolchain Rust (**Andika**). Dari root repositori:

```bash
cargo test --release
```

Potret bagian akhir yang menampilkan `test result: ok. 46 passed; 0 failed`. Simpan sebagai `07-hasil-pengujian.png`.

---

## Setelah selesai

1. Kumpulkan file PNG:

   ```
   01-antarmuka-utama.png
   02-identitas-invite.png
   03-verifikasi-vault.png
   04a-lan-discovery-laptop1.png     (atau 04-komunikasi-loopback.png)
   04b-lan-discovery-laptop2.png
   05-onion-invite.png
   06-badge-tor-aktif.png
   07-hasil-pengujian.png            (opsional)
   ```

2. **Periksa ulang setiap gambar** sebelum dikirim:
   - Tidak ada passphrase terketik yang terlihat.
   - Tidak ada data pribadi di jendela lain yang ikut terpotret.
   - Teks terbaca jelas, tidak buram, tidak terpotong.

3. **Laporkan apa yang gagal**, jangan diam-diam dilewati. Untuk setiap screenshot yang tidak berhasil diambil, catat: nomor berapa, gagal di langkah mana, pesan error apa yang muncul. Kegagalan yang dicatat jujur tetap berguna untuk laporan; kegagalan yang disembunyikan membuat klaim di BAB IV tidak bisa dipertanggungjawabkan.

4. Kirim ke Andika beserta catatan tersebut.

5. Hapus file demo di folder kerja: `demo-a.key`, `demo-b.key`, dan folder state Tor bila ada.

---

## Ringkasan perintah

| # | Screenshot | Perintah |
|---|---|---|
| 1 | Antarmuka utama | `.\aksara.exe --offline --vault demo-a.key` |
| 2 | Identitas/invite | (lanjutan #1, tekan `i`) |
| 3 | Verifikasi vault | `.\aksara.exe id --vault demo-a.key --offline` (3×, ketiga passphrase salah) |
| 4 | LAN discovery, laptop 1 | `.\aksara.exe --offline --vault demo-a.key --name demo-b --add INVITE-B` |
| 4 | LAN discovery, laptop 2 | `.\aksara.exe --offline --vault demo-b.key --name demo-a --add INVITE-A` |
| 5 | Onion di invite | `.\aksara.exe id --vault demo-a.key` |
| 6 | Badge TOR | `.\aksara.exe --vault demo-a.key` |
| 7 | Pengujian (opsional) | `cargo test --release` |

## Tombol TUI

| Tombol | Fungsi |
|---|---|
| `i` | Tampilkan/sembunyikan invite code sendiri |
| `c` | Salin invite code |
| `a` | Tambah kontak dari invite code |
| `↑` `↓` | Pilih kontak |
| `Enter` | Mulai koneksi (layar kontak) / kirim pesan (chat) |
| `Esc` | Keluar dari ruang chat |
| `q` | Keluar aplikasi |
| `Ctrl+B` | Sembunyikan isi chat (blur) |
| `Ctrl+C` | Keluar paksa |

---

**Sumber**: rilis `v0.2.1` (2026-07-26). Daftar dan aturan screenshot mengikuti `CLAUDE_PREPARATION_BRIEF.md` TAHAP 12 butir larangan 3-9. Alur `--listen`/`--dial`/`--add`, perilaku penolakan loopback pada discovery, dan daftar tombol diverifikasi langsung terhadap `src/transport/lan.rs`, `src/transport/mod.rs`, `src/session/mod.rs`, dan `src/tui/mod.rs` — bukan diperkirakan.

**Status bukti yang sedang ditutup oleh Sesi B dan C**: `src/transport/tor.rs` tidak memiliki unit test sama sekali, dan empat test di `src/transport/lan.rs` seluruhnya menguji fungsi murni (`safe_label`, `is_lan_dialable`) tanpa pernah menjalankan `advertise()`/`spawn_browse()`. Screenshot dari kedua sesi ini adalah **bukti visual**, bukan pengganti eksperimen terukur — sub-skenario Tor dan LAN fisik pada `12_TEST_PLAN.md` EXP-03 tetap berstatus `NEEDS_EXPERIMENT` sampai dijalankan sebagai run eksperimen dengan pencatatan lingkungan lengkap.
