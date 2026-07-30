# 11 — Figure Manifest AKSARA

Dokumen ini mendaftar seluruh diagram teknis mini-TA. Sumber diagram (`.mmd`) dirender dengan Mermaid CLI (`mmdc`) via Node.js (`docs/mini-ta/puppeteer-config.json`, Chrome sistem) — bukan AI image generator, sesuai `CLAUDE_PREPARATION_BRIEF.md` §TAHAP 11. Dua diagram (03 dan 06) langsung diformalkan dari versi ASCII yang sudah ada di `06_PROTOCOL_SPECIFICATION.md` §5.1 dan `07_KEY_LIFECYCLE.md` §8 sesuai instruksi sesi ini — bukan dirancang baru dari nol.

Perintah render yang dipakai (dari root repo):

```
mmdc -i <file>.mmd -o <out>.svg -p "docs/mini-ta/puppeteer-config.json" -b white -s 2
mmdc -i <file>.mmd -o <out>.png -p "docs/mini-ta/puppeteer-config.json" -b white -s 2
```

`-b white` memenuhi ketentuan latar putih; `-s 2` (scale 2×) dipakai untuk resolusi cetak yang lebih tinggi setelah verifikasi awal pada `06-key-lifecycle-state` menunjukkan teks terlalu rapat pada resolusi default. Seluruh diagram memakai palet default Mermaid (ungu muda/kuning muda/abu-abu, tanpa gradient/efek 3D/glow), font default Mermaid (terbaca), dan garis solid konsisten — tidak ada elemen dekoratif tambahan.

Lokasi:
- Source: `docs/mini-ta/01-claude-preparation/diagrams/src/*.mmd`
- Rendered SVG: `docs/mini-ta/01-claude-preparation/diagrams/rendered/svg/*.svg`
- Rendered PNG: `docs/mini-ta/01-claude-preparation/diagrams/rendered/png/*.png`

---

## Daftar Diagram

| ID | File | Judul | Tujuan | Evidence | Bab | Caption |
|----|------|-------|--------|----------|-----|---------|
| FIG-01 | `01-context` | Diagram Konteks AKSARA | Menunjukkan batas kepercayaan level tertinggi: dua pengguna, dua proses AKSARA, jaringan (LAN/Tor), dan penyimpanan lokal masing-masing | `08_THREAT_MODEL.md` §1 (diagram ASCII trust boundary), `06_PROTOCOL_SPECIFICATION.md` §1 | BAB IV | Gambar X.1. Diagram konteks AKSARA: dua proses P2P dihubungkan Noise_IK atas LAN mDNS/TCP atau Tor onion service, masing-masing menyimpan vault dan contacts store terenkripsi secara lokal. |
| FIG-02 | `02-component-architecture` | Diagram Arsitektur Komponen | Memetakan modul source (`identity`, `crypto`, `transport`, `session`, `contacts`, `tui`, `main`/`error`) dan relasi orkestrasinya | `AGENTS.md` (daftar modul), `06_PROTOCOL_SPECIFICATION.md`, `07_KEY_LIFECYCLE.md`, struktur `src/` | BAB IV | Gambar X.2. Arsitektur komponen AKSARA: `main.rs` mengorkestrasi `identity`, `contacts`, `transport`, dan `tui`; `transport` dan `crypto` bermuara ke `session::run_session`. |
| FIG-03 | `03-crypto-architecture` | Diagram Arsitektur Kriptografi | Memvisualisasikan CORE-1..7 sebagai satu rangkaian: entropi → penyimpanan at-rest → identitas → handshake → transport terenkripsi | `03_CRYPTO_INVENTORY_NORMALIZED.md`, `04_CRYPTOGRAPHIC_JUSTIFICATION.md`, `07_KEY_LIFECYCLE.md` | BAB IV | Gambar X.3. Arsitektur kriptografi AKSARA: seluruh kunci dibangkitkan via `OsRng` (CORE-7), dilindungi Argon2id+ChaCha20-Poly1305 saat disimpan (CORE-5/3), mengikat identitas via BLAKE2s (CORE-4), dan bermuara pada handshake Noise_IK (CORE-1) yang menghasilkan kunci sesi transport. |
| FIG-04 | `04-sequence-main-flow` | Sequence Diagram Proses Utama | Alur end-to-end: unlock vault → pertukaran invite out-of-band → discovery → handshake → sesi chat terenkripsi | `06_PROTOCOL_SPECIFICATION.md` §2-6 | BAB IV | Gambar X.4. Alur proses utama AKSARA dari unlock identitas hingga sesi chat aktif. |
| FIG-05 | `05-sequence-handshake-noise-ik` | Sequence Diagram Handshake Noise_IK | Formalisasi alur 2-pesan Noise_IK, termasuk percabangan kontak dikenal vs. belum dikenal (temuan trust-on-first-use) | `06_PROTOCOL_SPECIFICATION.md` §5.1-5.2 (versi ASCII sebagai basis langsung) | BAB IV | Gambar X.5. Handshake Noise_IK 2-pesan (`Noise_IK_25519_ChaChaPoly_BLAKE2s`); Responder memverifikasi `remote_static()` hanya bila kontak sudah dikenal — pada kontak baru, tidak ada pengecekan identitas sama sekali. |
| FIG-06 | `06-key-lifecycle-state` | Diagram Siklus Hidup Kunci | Formalisasi status kunci: belum ada vault → KeyBundle di memori → vault tersimpan → handshake aktif → sesi berakhir | `07_KEY_LIFECYCLE.md` §8 (versi ASCII sebagai basis langsung), §2-7 | BAB IV | Gambar X.6. Siklus hidup kunci AKSARA — tidak ada transisi rotasi/revokasi pada diagram ini karena mekanisme tersebut tidak ditemukan di source AKSARA (T7). |
| FIG-07 | `07-packet-format` | Diagram Format Paket/Pesan | Empat layout biner AKSARA: frame wire format, vault 108-byte, invite code, payload plaintext bertag | `06_PROTOCOL_SPECIFICATION.md` §3, §4.4, §6.3; `07_KEY_LIFECYCLE.md` §3.1 | BAB IV | Gambar X.7. Format paket dan pesan AKSARA: frame `[2-byte length][payload]`, vault `[salt‖nonce‖ciphertext‖tag]`, invite code `base64url(Ed25519 pub‖X25519 pub)`, dan payload plaintext `[1-byte tag][body]`. |

Total: **7 diagram** — dalam rentang 5-8 yang disyaratkan brief.

---

## Daftar Screenshot Aplikasi

Ditambahkan 2026-07-29, dilengkapi 2026-07-30. Dihitung **terpisah** dari 7 diagram di atas: rentang 5-8 pada brief berlaku untuk diagram, sedangkan screenshot diatur terpisah di TAHAP 12 (2-4 screenshot). Seluruh berkas berada di `screenshots/`, diambil dari **binary rilis v0.2.1** (bukan build lokal) pada Windows 11, terminal PowerShell.

| ID | File | Judul | Apa yang dibuktikan | Bab | Status |
|----|------|-------|---------------------|-----|--------|
| SS-01 | `01-antarmuka-utama.png` | Antarmuka Utama AKSARA | TUI berjalan nyata: header dengan badge transport `⌂ LOCAL`, fingerprint pendek `64809f`, panel kontak kosong, dan bilah bantuan tombol | BAB IV.1 | ✅ ADA |
| SS-02 | `02-identitas-invite.png` | Panel Identitas dan Invite Code | Invite code **86 karakter** dan fingerprint **64 hex** dikelompokkan 8×8, plus keterangan aplikasi sendiri bahwa tanpa `--offline` invite menyertakan onion | BAB IV.3 | ✅ ADA |
| SS-03a | `03-komunikasi-loopback-a.png` | Sesi Terenkripsi — Sisi Inisiator | Sesi aktif dengan peer `peer-4f88ab37`, notifikasi "Sesi aman terbuka", tiga pesan bertukar dengan cap waktu | BAB IV.5 | ✅ ADA |
| SS-03b | `03-komunikasi-loopback-b.png` | Sesi Terenkripsi — Sisi Responder | Sisi lawan dari sesi yang sama, memperlihatkan pesan diterima utuh | BAB IV.5 | ✅ ADA |
| SS-04 | `04-verifikasi-vault.png` | Verifikasi Vault: Determinisme dan Penolakan | Dua `unseal` dengan passphrase benar menghasilkan invite/fingerprint **identik**; passphrase salah menghasilkan `Error: vault could not be opened` | BAB V.2 (EXP-01) | ✅ ADA |
| SS-05 | `05-onion-invite.png` | Invite dengan Onion Address | Onion service v3 terbentuk dan alamatnya tertanam ke invite (~149 karakter, `Transport: LAN + Tor`), sisi laptop 2/demo-b | BAB IV.3 | ✅ ADA |
| SS-06 | `06-tor-online.png` | Badge Transport `◉ ONLINE` | Badge berubah menjadi `◉ ONLINE` (sisi laptop 1), status `idle` sebelum kontak ditambahkan. **Catatan**: notifikasi hijau "Tor siap" yang disebut panduan tidak terekam di gambar ini (sudah hilang saat capture) — badge tetap jadi bukti utama | BAB IV.6 | ✅ ADA (parsial, lihat catatan) |
| SS-07a | `07a-komunikasi-tor-laptop1.png` | Sesi Terenkripsi Lintas Jaringan via Tor — Sisi Laptop 1 | Sesi aktif dengan kontak `demo b`, 2 pesan dummy bertukar (`hallo`/`haii`) | BAB IV.5 | ✅ ADA |
| SS-07b | `07b-komunikasi-tor-laptop2.png` | Sesi Terenkripsi Lintas Jaringan via Tor — Sisi Laptop 2 | Sisi lawan dari sesi yang sama, 4 pesan dummy bertukar (`hallo`/`haii`/`berhasil`/`hore`) | BAB IV.5 | ✅ ADA |
| SS-07c-1 | `07c-bukti-jaringan-berbeda-laptop1.png` | Bukti Jaringan Berbeda — Laptop 1 | Output `ipconfig`: Wi-Fi aktif `192.168.102.128/24`, gateway `192.168.102.1` | BAB IV.5 (keterangan gambar) | ✅ ADA |
| SS-07c-2 | `07c-bukti-jaringan-berbeda-laptop2.png` | Bukti Jaringan Berbeda — Laptop 2 | Output `ipconfig`: Wi-Fi aktif `192.168.93.113/22`, gateway `192.168.92.1` — subnet berbeda dari laptop 1, mendukung klaim jaringan berbeda | BAB IV.5 (keterangan gambar) | ✅ ADA |

**Total tersedia: 11 berkas** (SS-01 s.d. SS-07c-2). Seluruh Sesi A dan Sesi B selesai, tidak ada lagi item screenshot tertunda.

### Catatan penting untuk penyusun laporan

1. **Jalur transport pada SS-03 adalah TCP loopback**, bukan LAN fisik maupun Tor. Aplikasi tidak mencetak jalur transport yang dipakai di layar, sehingga keterangan gambar **wajib** menyebut "topologi loopback lokal" secara eksplisit. Jangan menuliskannya seolah komunikasi lintas jaringan.

2. **SS-04 menampilkan passphrase dalam bentuk terbaca** (`demo-mini-ta-2026` dan `12345678`). Ini **bukan kebocoran**: keduanya passphrase dummy, dan yang terlihat justru **memperkuat** demonstrasi karena pembaca dapat memastikan percobaan kedua memakai passphrase yang sama sedangkan yang ketiga berbeda.

   Lebih dari itu, gambar ini menjadi **bukti visual atas keterbatasan yang sudah terdokumentasi**: input passphrase dari stdin masih ter-echo ke layar (`08_THREAT_MODEL.md` §4.6, `07_KEY_LIFECYCLE.md` baris `main.rs`, status `PLANNED` untuk M4). Sebelumnya keterbatasan itu hanya dibaca dari komentar kode; kini terlihat langsung. **Manfaatkan** di BAB IV atau BAB VI.2 sebagai contoh konkret, jangan disembunyikan.

3. **Kondisi gambar**: SS-01, SS-02, dan SS-04 beresolusi 1920×1140 dengan area kosong cukup besar di bawah; SS-03a/b beresolusi 1482×762. Untuk cetak, pemangkasan (*crop*) area kosong disarankan agar teks tidak mengecil berlebihan — pemangkasan area kosong **bukan** pengeditan yang dilarang, sepanjang isi layar tidak diubah.

4. **Fingerprint `64809f54…` dan invite pada gambar berasal dari identitas dummy** yang dibuat khusus untuk pengambilan gambar, bukan identitas produksi siapa pun.

5. **Cara mengutip SS-07 (Tor) — WAJIB dibaca sebelum menulis prosa BAB IV.5**: aplikasi TIDAK menampilkan jalur transport yang sedang dipakai di layar manapun — tidak ada teks "via Tor"/"via LAN". Gambar chat (SS-07a/b) **sendirian tidak membuktikan** sesi berjalan lewat Tor. Yang membuktikannya adalah kombinasi tiga hal: (a) SS-07a/b (sesi chat aktif), (b) SS-07c-1/2 (kedua laptop di subnet Wi-Fi berbeda: `192.168.102.x` vs `192.168.93.x`), dan (c) fakta arsitektural bahwa `establish()` di `src/transport/mod.rs` hanya punya dua jalur — LAN dulu dengan `LAN_AUTO_TIMEOUT` 3 detik, baru fallback Tor — sehingga jalur LAN mustahil dipakai antar-jaringan yang berbeda. Keterangan gambar di laporan **wajib** menyebutkan konfigurasi jaringan kedua laptop; tanpa itu klaim "lewat Tor" menjadi overclaim. Rujuk juga `HANDOFF_TO_CODEX.yaml` blocking_issues BI-08.

6. **SS-06 tidak menampilkan notifikasi hijau "Tor siap"** yang disebut `PANDUAN_SCREENSHOT.md` Screenshot 6 — kemungkinan sudah hilang sebelum gambar diambil. Cukup kutip badge `◉ ONLINE` sebagai bukti; jangan menulis seolah notifikasi itu terlihat di gambar.

---

## Diagram yang Dipertimbangkan tapi Tidak Dibuat

**Diagram topologi pengujian** (kategori ke-8 di brief) **sengaja tidak dibuat** sesi ini: TAHAP 13 (rencana pengujian, `12_TEST_PLAN.md`) belum disusun (dijadwalkan SESSION 5) sehingga topologi pengujian konkret (jumlah node, environment, kombinasi LAN/Tor per skenario) belum ditentukan. Membuat diagram ini sekarang berisiko mendahului keputusan TAHAP 13 tanpa evidence rencana pengujian yang sudah final — melanggar aturan "setiap elemen diagram memiliki evidence". FIG-01 (diagram konteks) sudah mencakup topologi jaringan dasar (2 proses, LAN/Tor) yang relevan sebagai referensi sementara. Diagram topologi pengujian spesifik dapat ditambahkan sebagai figure baru pada SESSION 5 setelah `12_TEST_PLAN.md` tersedia.

---

## Ringkasan Confidence

| Klaim | Confidence | Catatan |
|---|---|---|
| Seluruh 7 diagram berhasil dirender (SVG+PNG, exit 0) | HIGH | Diverifikasi langsung — `06-key-lifecycle-state` sempat gagal parse pada percobaan pertama (sintaks label state diagram), diperbaiki dan diverifikasi ulang render sukses |
| FIG-03/FIG-05/FIG-06/FIG-07 dicek visual (tidak ada elemen terpotong/tumpang tindih signifikan) | HIGH | Dibaca langsung sebagai gambar setelah render; FIG-06 sempat mengalami tumpang-tindih label pada layout TB awal, diperbaiki dengan `direction LR` |
| FIG-01/FIG-02/FIG-04 tidak dicek visual granular (hanya dicek dimensi piksel wajar) | MEDIUM | Render sukses tanpa error dan dimensi proporsional (bukan 66px pipih seperti kegagalan awal FIG-07), tapi tidak diperiksa piksel-demi-piksel |

---

## Referensi

Dokumen ini tidak memperkenalkan referensi teori baru — seluruh evidence sudah dirujuk ke `06_PROTOCOL_SPECIFICATION.md`, `07_KEY_LIFECYCLE.md`, dan `03_CRYPTO_INVENTORY_NORMALIZED.md`/`04_CRYPTOGRAPHIC_JUSTIFICATION.md` yang sudah memakai citekey `references/REFERENCES.bib`.
