# Panduan Pengambilan Screenshot AKSARA

**Untuk**: Rafi Putra Fadlurrahman (user testing) dan Mahendra Nur Hidayat (dokumentasi akhir).
**Target**: 6 file PNG wajib + 1 opsional.
**Tidak perlu install Rust atau clone repo** — cukup unduh satu binary dari GitHub.

Hasilnya dipakai sebagai Gambar di BAB IV dan BAB V laporan. Setelah selesai, kabari Andika untuk didaftarkan ke `11_FIGURE_MANIFEST.md`.

## Dua sesi

| Sesi | Butuh | Screenshot | Perkiraan waktu |
|---|---|---|---|
| **A** — dasar | 1 laptop, **tanpa** internet | 01, 02, 03 | 15 menit |
| **B** — Tor | **2 laptop**, internet, **jaringan berbeda** | 04, 05, 06 | 30-45 menit |

Sesi A dikerjakan sendiri-sendiri kapan saja. Sesi B perlu Rafi dan Mahendra bersamaan.

---

## Aturan yang TIDAK BOLEH dilanggar

Melanggarnya membuat gambar tidak bisa dipakai sama sekali di laporan:

1. **Screenshot layar asli.** Jangan bikin mockup, jangan edit gambar, jangan tempel teks.
2. **Jangan ubah tampilan aplikasi** demi foto yang lebih bagus.
3. **Passphrase dummy saja.** Pakai `demo-mini-ta-2026` di seluruh langkah.
4. **Jangan ada rahasia terlihat**: private key, token, password, isi chat pribadi.
5. **Nickname dan pesan chat pakai data dummy.**
6. Sebelum memotret, **tutup jendela lain** yang mungkin memuat data pribadi.
7. **Alamat `.onion` boleh dipotret** — itu alamat layanan, bukan kunci rahasia. Tapi jangan disebar di luar laporan.

---

## Langkah 0 — Unduh binary

Halaman rilis: **https://github.com/0xAre/aksara/releases/tag/v0.2.1**

| OS | File | Ukuran |
|---|---|---|
| **Windows** | `aksara-x86_64-pc-windows-msvc.exe` | 8,9 MB |
| Linux | `aksara-x86_64-unknown-linux-gnu` | 8,4 MB |
| macOS (Apple Silicon) | `aksara-aarch64-apple-darwin` | 6,1 MB |

Buat folder kerja `D:\aksara-demo`, taruh file di situ, **ganti nama jadi `aksara.exe`** (Windows) atau `aksara` (Linux/macOS).

### Verifikasi file (disarankan)

```bash
Get-FileHash aksara.exe -Algorithm SHA256
```

Harus persis: `C04D8A35D03064E31527C8793ACC03C5EB30975EDF3710042F2E8D4AF1A59066`

Linux/macOS pakai `shasum -a 256 aksara` — Linux `6f4c865c...124ed`, macOS `49c2fd34...5de1d2`.

### Windows: izinkan berjalan

Binary tidak ditandatangani digital. Klik kanan `aksara.exe` → **Properties** → centang **Unblock** → OK. Kalau muncul layar biru SmartScreen: **More info** → **Run anyway**.

### Linux/macOS

```bash
chmod +x aksara
```

macOS juga perlu klik kanan → Open → Open, sekali saja.

---

## Persiapan

1. **Perbesar terminal** minimal 100 kolom × 30 baris. Terminal kecil membuat TUI terpotong — penyebab paling sering screenshot tidak terpakai.
2. Semua perintah dijalankan dari dalam folder kerja.
3. Memotret: Windows `Win + Shift + S`, macOS `Cmd + Shift + 4`, Linux tool bawaan.

**Tentang `--offline`**: mematikan Tor supaya aplikasi langsung jalan. Dipakai di Sesi A. **Tidak dipakai di Sesi B**, karena justru Tor yang mau dibuktikan.

---

# SESI A — Dasar (1 laptop, tanpa internet)

Bisa dikerjakan Rafi dan Mahendra masing-masing di laptop sendiri.

## Screenshot 1 — Antarmuka utama

**BAB IV.1.** Bukti visual aplikasinya nyata dan berjalan.

```bash
.\aksara.exe --offline --vault demo-a.key
```

1. Vault belum ada → aplikasi minta buat identitas baru. Passphrase `demo-mini-ta-2026`, **Enter**.
2. Ikuti layar inisialisasi sampai selesai.
3. Setelah masuk layar utama (daftar kontak + header), **potret**.

Simpan: **`01-antarmuka-utama.png`**

## Screenshot 2 — Identitas dan invite code

**BAB IV.3.** Masih di layar yang sama, tekan **`i`** untuk menampilkan invite code dan fingerprint sendiri. **Potret.**

Simpan: **`02-identitas-invite.png`**

> Aman dipotret: invite code hanya berisi **public key**.

Panjang invite di sini harus tepat **86 karakter** (mode offline, tanpa onion). Tekan **`q`** untuk keluar.

## Screenshot 3 — Verifikasi vault

**BAB V.2** (hasil EXP-01). BAB V saat ini seluruhnya angka tanpa satu pun gambar.

Tiga perintah berurutan **di satu terminal, jangan dibersihkan layarnya**:

```bash
.\aksara.exe id --vault demo-a.key --offline
```

Passphrase `demo-mini-ta-2026`. Catat invite dan fingerprint.

```bash
.\aksara.exe id --vault demo-a.key --offline
```

Passphrase sama. **Hasilnya harus persis identik.**

```bash
.\aksara.exe id --vault demo-a.key --offline
```

Passphrase **salah**, misalnya `passphrase-salah`. Harus muncul `Error: vault could not be opened`.

**Potret** seluruh terminal sehingga ketiga hasil terlihat.

Simpan: **`03-verifikasi-vault.png`**

Membuktikan `unseal` deterministik sekaligus penolakan passphrase salah dengan pesan generik.

---

# SESI B — Tor (2 laptop, jaringan berbeda)

Ini bagian terpenting. Tor saat ini komponen dengan **bukti paling minim** di seluruh dokumen: `src/transport/tor.rs` tidak punya satu pun unit test.

## ⚠ Syarat mutlak: kedua laptop HARUS di jaringan yang BERBEDA

Ini bukan saran, tapi keharusan teknis. Aplikasi **selalu mencoba LAN lebih dulu** dan hanya memberi jatah **3 detik** sebelum jatuh ke Tor (`LAN_AUTO_TIMEOUT` di `src/transport/mod.rs`). Kalau kedua laptop berada di WiFi yang sama, LAN akan langsung menang dan **sesi tidak pernah lewat Tor** — screenshot-nya jadi tidak membuktikan apa pun tentang Tor.

**Cara paling mudah memisahkan jaringan:**

- **Laptop 1**: tetap di WiFi rumah/kampus.
- **Laptop 2**: matikan WiFi, lalu *tethering* ke **data seluler HP** (bukan hotspot dari HP yang tersambung WiFi yang sama).

Dengan begitu tidak ada jalur LAN yang mungkin, sehingga satu-satunya cara keduanya bisa tersambung adalah lewat Tor. Ini sekaligus demo terkuat untuk laporan: dua mesin di jaringan yang sama sekali berbeda, tanpa server perantara, tanpa *port forwarding*, tetap bisa berkomunikasi.

## ⚠ Kesabaran: onion descriptor butuh 1-3 menit

Setelah notifikasi "Tor siap" muncul, alamat onion **belum langsung bisa dihubungi**. Descriptor-nya perlu waktu terpublikasi ke jaringan Tor — biasanya 1 sampai 3 menit. Aplikasi sudah menangani ini dengan mencoba ulang tiap 8 detik selama maksimal 2 menit, tapi **jangan menekan Enter terlalu cepat**. Tunggu dulu beberapa menit setelah "Tor siap" di kedua laptop.

> **Kalau Tor gagal bootstrap**: sebagian jaringan kampus/kantor memblokir Tor. Pakai data seluler di kedua sisi. Kalau tetap gagal, lewati Sesi B dan **beri tahu Andika** — statusnya akan ditulis apa adanya sebagai belum terverifikasi, bukan dikarang.

---

## Screenshot 4 — Onion address di dalam invite

**Dikerjakan di masing-masing laptop.** Sama seperti Sesi A tapi **tanpa `--offline`**:

Laptop 1:

```bash
.\aksara.exe id --vault demo-a.key
```

Laptop 2:

```bash
.\aksara.exe id --vault demo-b.key
```

1. Muncul `Bootstrap Tor untuk ambil onion address (~30-60 dtk)…`. Tunggu.
2. Passphrase `demo-mini-ta-2026`.
3. Invite yang tercetak sekarang **jauh lebih panjang**, berakhiran `@xxxxx.onion`, dan baris `Transport:` ikut berubah.
4. **Potret** salah satu laptop saja (cukup satu gambar).

Simpan: **`04-onion-invite.png`**

Bukti bahwa onion service v3 benar-benar terbentuk dan alamatnya tertanam ke dalam invite.

> Pembanding untuk laporan: invite LAN-only **86 karakter**, invite dengan onion sekitar **149 karakter**. Selisihnya adalah alamat `.onion`.

**Sekarang tukar invite**: kirim invite Laptop 1 (**INVITE-A**) ke Laptop 2, dan invite Laptop 2 (**INVITE-B**) ke Laptop 1, lewat WhatsApp atau chat apa pun. Pastikan tersalin **utuh** — panjangnya sekitar 149 karakter.

## Screenshot 5 — Notifikasi "Tor siap" di TUI

**Cukup di salah satu laptop.**

```bash
.\aksara.exe --vault demo-a.key
```

1. Passphrase `demo-mini-ta-2026`.
2. TUI **langsung tampil** tanpa menunggu Tor — di header muncul indikator `tor·…` yang menandakan bootstrap berjalan di latar belakang.
3. **Tunggu 30-60 detik.** Saat siap, muncul notifikasi hijau: **"Tor siap — sekarang online (LAN + Tor)."**
4. **Potret** saat notifikasi itu tampil.

Simpan: **`05-tor-siap.png`**

Memperlihatkan perilaku yang dijelaskan di BAB IV: TUI tidak diblokir menunggu Tor, melainkan tetap responsif sementara bootstrap berjalan di latar belakang, lalu invite diperbarui sendiri begitu onion tersedia.

Tekan **`q`** untuk keluar.

## Screenshot 6 — Komunikasi dua laptop lewat Tor

**BAB IV.5.** Screenshot paling berharga dari seluruh daftar.

Pastikan syarat jaringan berbeda di atas sudah dipenuhi. Lalu **kedua laptop** menjalankan — perhatikan: **tanpa `--offline`, tanpa `--listen`, tanpa `--dial`**:

Laptop 1:

```bash
.\aksara.exe --vault demo-a.key --name demo-b --add INVITE-B
```

Laptop 2:

```bash
.\aksara.exe --vault demo-b.key --name demo-a --add INVITE-A
```

1. Passphrase `demo-mini-ta-2026` di keduanya.
2. **Tunggu notifikasi hijau "Tor siap" muncul di KEDUA laptop.**
3. **Tunggu 2-3 menit lagi** supaya onion descriptor sempat terpublikasi. Ini langkah yang paling sering dilewati dan jadi penyebab utama kegagalan.
4. Di layar kontak, pilih kontak lawan dengan **↑/↓**, tekan **Enter** di kedua laptop.
5. LAN akan gagal dalam 3 detik (tidak ada jalur antar-jaringan), lalu aplikasi otomatis beralih ke Tor. **Sabar** — dial lewat Tor mencoba ulang tiap 8 detik hingga total 2 menit.
6. Setelah sesi aktif, kirim 2-3 pesan bolak-balik. Contoh aman: `halo, uji coba lewat tor` dan `diterima, sesi aktif`.
7. **Potret layar kedua laptop.** Simpan terpisah:

**`06a-komunikasi-tor-laptop1.png`** dan **`06b-komunikasi-tor-laptop2.png`**

### Tambahan yang membuat bukti jauh lebih kuat

Screenshot chat **tidak menampilkan jalur transport yang dipakai** — aplikasi tidak mencetak "via Tor" atau "via LAN" di layar. Jadi yang membuktikan sesi itu lewat Tor adalah **fakta bahwa kedua laptop berada di jaringan berbeda**, dan fakta itu harus terlihat atau tercatat.

Karena itu, potret juga kondisi jaringan masing-masing laptop, misalnya nama WiFi/koneksi aktif di taskbar atau hasil perintah berikut:

```bash
ipconfig
```

Simpan sebagai **`06c-bukti-jaringan-berbeda.png`** (boleh gabungan kedua laptop dalam satu gambar). Ini yang akan dirujuk di keterangan gambar laporan untuk menjelaskan mengapa jalur LAN mustahil.

### Kalau gagal terhubung

1. **Invite tersalin tidak utuh** — penyebab paling sering. Invite ber-onion sekitar 149 karakter, pastikan tidak terpotong saat dikirim lewat chat.
2. **Terlalu cepat menekan Enter** — descriptor belum terpublikasi. Tunggu 3 menit penuh setelah "Tor siap", lalu coba lagi.
3. **Salah satu sisi Tor-nya gagal** — cek notifikasi; kalau muncul "Tor gagal", jaringan itu memblokir Tor. Ganti ke data seluler.
4. Coba ulang **maksimal tiga kali**. Setiap percobaan beri jeda 2 menit.

Kalau tetap gagal, **jangan dipaksakan dan jangan dikarang**. Ambil pengganti lewat jalur LAN loopback di **satu laptop**:

```bash
.\aksara.exe --offline --vault demo-a.key --listen 9000
```

```bash
.\aksara.exe --offline --vault demo-b.key --name demo-a --dial 127.0.0.1:9000 --add INVITE-A-OFFLINE
```

(`INVITE-A-OFFLINE` = invite 86 karakter dari Screenshot 2, bukan yang ber-onion.)

Simpan sebagai **`06-komunikasi-loopback.png`** dan **beri tahu Andika bahwa yang berhasil hanya jalur LAN loopback** — status di laporan akan berbeda dan itu harus ditulis apa adanya.

---

# Opsional — Screenshot 7: hasil `cargo test`

Hanya untuk yang punya source dan toolchain Rust (**Andika**). Dari root repositori:

```bash
cargo test --release
```

Potret bagian `test result: ok. 46 passed; 0 failed`. Simpan sebagai `07-hasil-pengujian.png`.

---

## Setelah selesai

1. Kumpulkan file:

   ```
   01-antarmuka-utama.png
   02-identitas-invite.png
   03-verifikasi-vault.png
   04-onion-invite.png
   05-tor-siap.png
   06a-komunikasi-tor-laptop1.png      (atau 06-komunikasi-loopback.png)
   06b-komunikasi-tor-laptop2.png
   06c-bukti-jaringan-berbeda.png
   07-hasil-pengujian.png              (opsional)
   ```

2. **Periksa ulang tiap gambar**: tidak ada passphrase terlihat, tidak ada data pribadi dari jendela lain, teks terbaca jelas dan tidak terpotong.

3. **Catat kondisi jaringan** yang dipakai saat Sesi B: laptop mana pakai apa (mis. "Laptop 1: WiFi kos, Laptop 2: tethering data seluler"). Informasi ini masuk ke keterangan gambar di laporan.

4. **Laporkan yang gagal, jangan diam-diam dilewati.** Catat: nomor berapa, gagal di langkah mana, pesan error apa. Kegagalan yang dicatat jujur tetap berguna; kegagalan yang disembunyikan membuat klaim di BAB IV tidak bisa dipertanggungjawabkan.

5. Kirim ke Andika beserta catatan itu.

6. Bersihkan folder kerja: `demo-a.key`, `demo-b.key`, dan folder state Tor yang terbentuk.

---

## Ringkasan perintah

| # | Screenshot | Perintah |
|---|---|---|
| 1 | Antarmuka utama | `.\aksara.exe --offline --vault demo-a.key` |
| 2 | Identitas/invite | (lanjutan #1, tekan `i`) |
| 3 | Verifikasi vault | `.\aksara.exe id --vault demo-a.key --offline` (3×, ketiga passphrase salah) |
| 4 | Onion di invite | `.\aksara.exe id --vault demo-a.key` |
| 5 | Notifikasi Tor siap | `.\aksara.exe --vault demo-a.key` |
| 6 | Komunikasi Tor, laptop 1 | `.\aksara.exe --vault demo-a.key --name demo-b --add INVITE-B` |
| 6 | Komunikasi Tor, laptop 2 | `.\aksara.exe --vault demo-b.key --name demo-a --add INVITE-A` |
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

## Catatan untuk penyusun laporan

**Yang TIDAK dicakup panduan ini**: penemuan peer otomatis lewat mDNS (`advertise()`/`spawn_browse()` di `src/transport/lan.rs`). Rencana screenshot dua laptop di WiFi yang sama sengaja **tidak dipakai** karena tidak berguna sebagai bukti — `DiscoveredPeer` tidak pernah sampai ke lapisan TUI, sehingga sesi hasil discovery otomatis dan sesi hasil `--dial` manual tampil **identik** di layar. Screenshot tidak dapat membedakan keduanya.

Konsekuensinya harus ditulis jujur: **mDNS discovery tetap tanpa bukti empiris**, berstatus `IMPLEMENTED` dari pembacaan kode saja. Empat unit test di `src/transport/lan.rs` seluruhnya menguji fungsi murni (`safe_label`, `is_lan_dialable`), bukan alur discovery. Ini sejalan dengan `09_SCOPE_AND_TEAM_PLAN.md` §5 butir 8 yang membatasi mDNS sebagai konteks pendukung.

**Cara mengutip Screenshot 6 dengan benar**: aplikasi tidak menampilkan jalur transport yang sedang dipakai, sehingga gambar chat itu sendiri tidak membuktikan sesi berjalan lewat Tor. Yang membuktikannya adalah **kombinasi** gambar chat + gambar kondisi jaringan (`06c`) + fakta bahwa `establish()` hanya punya dua jalur (LAN lalu Tor) dan jalur LAN mustahil antar-jaringan berbeda. Keterangan gambar di laporan **wajib** menyebutkan konfigurasi jaringan yang dipakai — tanpa itu, klaim "lewat Tor" tidak tertopang.

**Status bukti Tor setelah Sesi B**: screenshot adalah **bukti visual**, bukan pengganti eksperimen terukur. Sub-skenario Tor pada `12_TEST_PLAN.md` EXP-03 tetap `NEEDS_EXPERIMENT` sampai dijalankan sebagai run resmi dengan pencatatan lingkungan lengkap.

---

**Sumber**: rilis `v0.2.1` (2026-07-26). Aturan screenshot mengikuti `CLAUDE_PREPARATION_BRIEF.md` TAHAP 12 butir larangan 3-9. Seluruh alur perintah, urutan LAN-lalu-Tor beserta `LAN_AUTO_TIMEOUT` 3 detik, retry dial Tor 8 detik hingga total 120 detik, catatan publikasi descriptor 1-3 menit, teks notifikasi Tor, dan daftar tombol diverifikasi langsung terhadap `src/transport/mod.rs`, `src/transport/lan.rs`, `src/session/mod.rs`, `src/main.rs`, dan `src/tui/mod.rs` — bukan diperkirakan.
