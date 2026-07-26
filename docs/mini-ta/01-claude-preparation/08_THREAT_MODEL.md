# 08 — Threat Model AKSARA

Dokumen ini menganalisis ancaman keamanan AKSARA berdasarkan evidence source-level dari TAHAP 2/3 (`02_CRYPTO_IMPLEMENTATION_AUDIT.md`, `evidence/_raw-audit-json/*.json`), justifikasi kriptografi TAHAP 4 (`04_CRYPTOGRAPHIC_JUSTIFICATION.md`, `05_CRYPTO_ALTERNATIVE_COMPARISON.md`), dan spesifikasi protokol/key lifecycle yang disusun di sesi ini (`06_PROTOCOL_SPECIFICATION.md`, `07_KEY_LIFECYCLE.md`). Metodologi: kategorisasi ancaman per-komponen ringan terinspirasi STRIDE, diskalakan proporsional untuk tugas mata kuliah — **bukan** model formal lengkap dengan skoring kuantitatif (mis. CVSS).

**Batasan wajib dibawa dari `SESSION_2_HANDOFF.md`**: Ed25519 murni fingerprint (§3, §5.1 — jangan bahas ancaman "pemalsuan tanda tangan" karena tidak ada tanda tangan aktif untuk dipalsukan); sub-mekanisme internal Noise_IK confidence LOW (§5.3); ChaCha20-Poly1305 bukan misuse-resistant, dibahas sebagai batasan desain sadar bukan bug (§5.4); klaim "~100ms" Argon2id tidak dipakai sebagai basis kuantitatif ketahanan brute-force (§5.5).

---

## 1. Ruang Lingkup dan Batas Kepercayaan (Trust Boundaries)

```
[Pengguna A] --passphrase--> [Proses AKSARA A] <--Noise_IK atas LAN/Tor--> [Proses AKSARA B] <--passphrase-- [Pengguna B]
                                    |                                            |
                              [Vault + contacts       [Vault + contacts
                               store lokal, disk]      store lokal, disk]
                                    |                                            |
                              [OS CSPRNG, filesystem]                    [OS CSPRNG, filesystem]
```

Batas kepercayaan yang relevan:
1. **Jaringan** antar dua proses AKSARA (LAN atau sirkuit Tor) — diasumsikan sepenuhnya tidak tepercaya (kanal publik).
2. **Filesystem lokal** tempat vault identitas dan contact store disimpan — diasumsikan dapat diakses pihak lain pada mesin yang sama (multi-user/shared machine), tapi bukan mesin yang sepenuhnya dikuasai penyerang (di luar cakupan: kompromi OS/root/kernel).
3. **Manusia** — verifikasi fingerprint out-of-band adalah bagian dari model kepercayaan (root-of-trust berada di proses verifikasi manusia, bukan di dalam protokol Noise itu sendiri, lihat `06_PROTOCOL_SPECIFICATION.md` §5.1 poin 14 pada `04_CRYPTOGRAPHIC_JUSTIFICATION.md` CORE-1).
4. **Dependency eksternal** (`snow`, `arti-client`/`tor-hsservice`, `mdns-sd`) — internal cryptography/keamanan crate-crate ini **di luar cakupan** audit source-level AKSARA sendiri (§6).

---

## 2. Aset yang Dilindungi

| Aset | Deskripsi |
|---|---|
| Identity secret key (Ed25519) | Basis fingerprint jangka panjang; kompromi memungkinkan penyamaran identitas dalam pertukaran invite baru |
| Noise secret key (X25519) | Basis autentikasi/kerahasiaan handshake; kompromi memungkinkan dekripsi retroaktif bila juga ada rekaman lalu lintas (tergantung properti forward secrecy Noise_IK yang berstatus DOCUMENTED_ONLY, lihat §5.3) |
| Passphrase vault | Satu-satunya penghalang offline brute-force terhadap kedua secret key di atas |
| Daftar kontak (nickname, fingerprint, alamat) | Metadata sosial; kebocoran memetakan jaringan relasi pengguna |
| Plaintext sesi (isi chat, sinyal blur) | Konten komunikasi — nilai kerahasiaan utama aplikasi |
| Metadata kehadiran (presence) di LAN | Siapa yang online, kapan, fingerprint publiknya — bukan konten, tapi tetap sensitif untuk analisis lalu lintas |

---

## 3. Model Musuh (Adversary Models)

| ID | Kemampuan | Batasan |
|---|---|---|
| **A1** | Penyadap pasif di LAN atau sirkuit Tor | Dapat mengamati ciphertext, broadcast mDNS, metadata TCP; **tidak** dapat mendekripsi lalu lintas terproteksi Noise (dengan asumsi X25519/ChaCha20-Poly1305 tidak dibobol) |
| **A2** | Penyerang aktif di LAN (spoofing/injeksi mDNS) | Dapat mencoba MITM terhadap kontak **baru** yang belum diverifikasi; **tidak dapat** menembus sesi Noise_IK terverifikasi karena responder fail-closed pada ketidakcocokan static key (§5.2) — **KECUALI** pada koneksi pertama ke kontak yang belum dikenal (`peer_noise_pk=None`, §5.2) |
| **A3** | Penyerang lokal dengan akses baca filesystem (bukan root, tanpa passphrase) | Berhadapan dengan Argon2id + ChaCha20-Poly1305 pada vault; dapat mencoba brute-force offline terhadap passphrase lemah, dibatasi *cost* Argon2id (kuantitas waktu **tidak** diketahui pasti — lihat §5.5) |
| **A4** | Kontak berbahaya/kompromi yang memegang fingerprint valid | Karena invite code tidak diautentikasi kriptografis dan Noise_IK tidak memberi non-repudiation konten di luar sesi, kontak semacam ini berpartisipasi penuh sebagai pihak sah — ini **perilaku desain yang diharapkan**, bukan celah |
| **A5** | Partisipan mDNS berbahaya di segmen LAN yang sama | Dapat mengamati broadcast presence/fingerprint plaintext (§4.2); mDNS/DNS-SD (`rfc6762`, `rfc6763`) secara struktural tidak menyediakan kerahasiaan/otentikasi pada broadcast-nya — eksposur ini melekat pada mekanisme discovery yang dipilih, bukan murni bug spesifik AKSARA |

---

## 4. Ancaman per Komponen (Dipetakan ke Fase Protokol)

### 4.1 Pertukaran Kontak (Invite Code)

- **Invite code tidak ditandatangani/diautentikasi** (`contacts/mod.rs:42-47`, CR-005) — bila invite dikirim lewat kanal out-of-band yang dapat dimanipulasi penyerang, invite palsu dapat mengikat korban ke kunci milik penyerang. Mitigasi **satu-satunya** adalah verifikasi fingerprint manual oleh manusia (out-of-band); kode aplikasi **tidak memaksa atau mengingatkan** langkah verifikasi ini secara eksplisit — status alur UX verifikasi pada TUI `NEEDS_CONFIRMATION` (di luar cakupan file yang diaudit sesi ini).
- Kedua public key **wajib** diserap bersama via BLAKE2s fingerprint dengan domain-separation (`contacts/mod.rs:39-54`) — mencegah *serangan invite susun-ulang* (attacker menggabungkan `ed25519_pub` korban dengan `noise_pub` miliknya sendiri), dikonfirmasi test `fingerprint_binds_both_keys`. Ini mitigasi struktural yang **sudah efektif**.
- Alamat onion diperlakukan sebagai string opaque tanpa validasi format — risiko rendah karena hanya berperan sebagai *routing hint*, bukan batas keamanan kriptografis.

### 4.2 Discovery LAN (mDNS)

- **Kebocoran metadata kehadiran diakui secara eksplisit oleh komentar kode sendiri** sebagai trade-off yang diterima untuk M1 (`transport/lan.rs:9-12`): siapa pun di segmen LAN yang sama dapat mengamati siapa yang menjalankan AKSARA beserta fingerprint hex-nya, memungkinkan analisis lalu lintas/social engineering terarah **tanpa perlu membobol kriptografi apa pun**. Mekanisme mDNS/DNS-SD (`rfc6762`/`rfc6763`) yang dipakai `mdns-sd` 0.20.0 secara struktural memang broadcast tanpa proteksi kerahasiaan/otentikasi bawaan — ini bukan kelemahan implementasi AKSARA per se, melainkan properti bawaan dari kelas mekanisme discovery yang dipilih.
- **X25519 Noise key TIDAK diiklankan** via mDNS (`lan.rs:9-11`) — jadi material handshake sendiri tidak bocor pra-koneksi, hanya identitas/presence.
- Filter `is_lan_dialable` + re-filter *defense-in-depth* pada alamat yang diiklankan peer (`lan.rs:50-55,133-149`) mengurangi (bukan menghilangkan) risiko peer berbahaya menyiarkan alamat spoofed/non-dialable.
- Perbandingan fingerprint non-constant-time (`role_from_fp`, operator `<` bawaan `&str`) dinilai risiko rendah karena kedua fingerprint adalah data publik yang sudah saling diketahui, bukan rahasia (`transport/mod.rs:101-107`).

### 4.3 Handshake Noise_IK

- **Tidak ada pengecekan identitas sama sekali** ketika Responder menerima koneksi dari kontak yang **belum dikenal** (`peer_noise_pk = None`, `session/mod.rs:145-151`) — model *trust-on-first-use* implisit. Serangan MITM aktif pada **koneksi pertama** ke kontak yang belum diverifikasi **tidak dapat dibedakan** oleh protokol dari koneksi asli; mitigasi sepenuhnya berada di luar layer Noise, pada langkah verifikasi fingerprint manusia (§4.1).
- Untuk kontak yang **sudah** dikenal, ketidakcocokan static key menghasilkan `Error::IdentityMismatch` dengan perilaku **fail-closed** eksplisit (`session/mod.rs:145-151`, dikonfirmasi test `responder_rejects_unknown_peer`) — proteksi kuat terhadap *impersonation* pada re-koneksi ke kontak yang telah diverifikasi.
- Tidak ada pengecekan eksplisit terhadap public key peer all-zero/low-order point di `crypto/handshake.rs` — kepercayaan sepenuhnya pada penanganan internal `snow`+`x25519-dalek`, tidak diverifikasi independen dalam audit ini.
- Crate `snow` **belum diaudit keamanan formal** (self-declared) — risiko implementasi yang diterima secara sadar (`04_CRYPTOGRAPHIC_JUSTIFICATION.md` CORE-1 poin 5).
- Properti *forward secrecy* dan kerahasiaan static-key initiator terhadap penyadap pasif hanya dinyatakan pada komentar dokumentasi (`crypto/handshake.rs:14-17`), **tidak diverifikasi** oleh test suite AKSARA sendiri — perlakukan sebagai properti desain yang diwarisi dari spesifikasi Noise_IK (`noise2018`), bukan jaminan teruji secara independen.
- Jalur payload 0-RTT (data aplikasi dikirim bersamaan pesan handshake) **tidak diuji** oleh test suite manapun (seluruh test memakai payload kosong) — bila jalur ini dipakai di produksi, perilakunya tidak terverifikasi.

### 4.4 Fase Transport (Sesi Aktif)

- ChaCha20-Poly1305 (diasumsikan, lihat `06_PROTOCOL_SPECIFICATION.md` §6.4) **bukan** konstruksi *misuse-resistant* — nonce reuse pada kunci sama bersifat katastropik. Manajemen nonce sepenuhnya internal `snow`, tidak dapat diverifikasi independen dari source aplikasi. Ini **batasan desain yang diterima secara sadar** (dibahas penuh di `04_CRYPTOGRAPHIC_JUSTIFICATION.md` CORE-3 poin 10/12 dan `05_CRYPTO_ALTERNATIVE_COMPARISON.md` §3) — **bukan** bukti adanya bug nonce-reuse aktual yang ditemukan dalam audit ini.
- Tidak ada AAD yang mengikat domain pesan (`TYPE_TEXT`/`TYPE_BLUR`/`TYPE_PING`) pada level AEAD — pemisahan jenis pesan terjadi struktural (byte tag dicek pasca-dekripsi), bukan terikat kriptografis. Risiko praktis rendah (tidak ada skenario type-confusion yang teridentifikasi), tapi dicatat sebagai kelonggaran desain.
- **Kegagalan dekripsi frame masuk menghentikan sesi secara fail-closed** (`session/mod.rs:253-268`) — perilaku default yang baik, namun **UI tidak dapat membedakan** "sesi ditutup karena kecurigaan tampering" dari penutupan biasa lainnya (kecuali event `PeerLeft` yang khusus untuk EOF bersih). Penyerang yang berulang kali mencoba merusak frame secara aktif hanya akan tampak bagi pengguna sebagai "koneksi terputus", tanpa sinyal keamanan yang berbeda.
- `read_frame` tidak cancel-safe (`transport/frame.rs:97-104`) — sudah dimitigasi arsitektural via task pembaca terpisah (`session/mod.rs:166-190`); risiko regresi bila perubahan kode di masa depan mengembalikan `read_frame` ke dalam arm `tokio::select!` (bukan kerentanan aktif saat ini, melainkan catatan untuk pengembangan lanjutan — lihat memori proyek terkait ini yang dicatat lintas-sesi).
- Deteksi keterputusan koneksi sepenuhnya bergantung pada kegagalan `write_frame`, bukan ping tak terbalas (`session/mod.rs:54-58`) — peer yang diam-diam berhenti merespons namun mempertahankan koneksi TCP/Tor tetap "half-open" mungkin tidak terdeteksi segera. Sudah didokumentasikan sebagai keterbatasan M1 yang disengaja.

### 4.5 Vault Identitas dan Contacts Store (At-Rest)

- Vault dilindungi Argon2id + ChaCha20-Poly1305 dengan pesan error yang sengaja ambigu (mitigasi *oracle attack*, `identity/vault.rs:96-97`, `error.rs:1-14`) — detail penuh di `07_KEY_LIFECYCLE.md` §3. Implikasi ancaman: penyerang dengan akses **baca** vault dibatasi pada brute-force offline terhadap passphrase (dibatasi *cost* Argon2id, namun **kuantitas** ketahanannya tidak diketahui pasti — §5.5); penyerang dengan akses **tulis** dapat merusak/mengganti file vault, namun ini hanya akan terdeteksi sebagai kegagalan dekripsi generik saat unlock berikutnya, **tanpa sinyal tamper-evidence** terpisah di luar tag AEAD itu sendiri.
- **Tidak ada file-permission hardening eksplisit** pada penulisan/pembacaan vault (`vault.rs:132-142`) — pada sistem multi-pengguna, perlindungan bergantung sepenuhnya pada permission filesystem default OS, bukan pengerasan aktif dari AKSARA sendiri.
- Contacts store memakai kunci yang diturunkan **deterministik** dari identity secret (bukan passphrase terpisah) — akibatnya kompromi identity secret yang sudah ter-unlock otomatis membuka seluruh daftar kontak; tidak ada kompartementalisasi (`07_KEY_LIFECYCLE.md` §4).
- `deserialize_contacts` diam-diam melewati baris rusak/tidak lengkap tanpa melaporkan ke caller (`contacts/mod.rs:140-167`) — potensi kehilangan data kontak secara senyap pasca-korupsi parsial, tanpa peringatan ke pengguna.

### 4.6 Penanganan Passphrase (`main.rs`)

- `AKSARA_PASSPHRASE` (env var): nilainya hidup di environment proses selama proses berjalan, **tanpa mekanisme pembersihan** setelah dibaca (`main.rs:156-158`) — pada sistem multi-pengguna, visibilitas environment variabel antar-proses bergantung OS dan tidak diverifikasi lebih jauh dalam audit ini.
- Input passphrase interaktif dari stdin **masih ter-echo ke layar** pada versi ini (`main.rs:153-154`, status `PLANNED` untuk M4, **belum diimplementasikan**) — risiko *shoulder-surfing*/perekaman layar saat pembuatan/unlock identitas.
- Passphrase kosong ditolak (`main.rs:175-178`) — hanya validasi dasar, **tidak ada** persyaratan kompleksitas/kekuatan passphrase yang ditegakkan aplikasi.

### 4.7 Jalur Tor (Lapisan Defense-in-Depth)

- Bootstrap `TorClient::create_bootstrapped` tanpa timeout/retry eksplisit (`tor.rs:9-60`) — bootstrap yang menggantung dapat membuat `launch()` menggantung tanpa batas dari sisi caller (risiko ketersediaan, bukan kerahasiaan/integritas).
- `accept_timeout()` tidak dapat membedakan "waktu habis" dari "channel tertutup" (`tor.rs:117-120`) — ambiguitas level-caller, risiko operasional minor.
- Manajemen/rotasi key onion service sepenuhnya didelegasikan ke `arti-client`/`tor-hsservice`, **tidak diverifikasi independen** dari source AKSARA sendiri — di luar cakupan audit source-level ini.
- **`FS_MISTRUST_DISABLE_PERMISSIONS_CHECKS=true` diset tanpa syarat platform apa pun** (dikonfirmasi: tidak ada `cfg(windows)`/`target_os` di seluruh `main.rs`) setiap kali mode online aktif (`main.rs:216-219`) — melemahkan pengecekan permission filesystem bawaan `arti` untuk direktori state/cache-nya, **di semua platform** (Linux/macOS/Windows), bukan hanya Windows seperti tersirat dari komentar kode ("dev convenience di Windows"). Pada sistem Linux/macOS multi-pengguna, ini berpotensi membiarkan pengguna lokal lain membaca/mengubah direktori state/cache Tor tanpa terdeteksi oleh pengecekan `fs-mistrust` yang biasanya aktif.

---

## 5. Batasan Cakupan (Explicitly Out of Scope)

Sesuai hierarki sumber kebenaran `AGENTS.md`, hal berikut **tidak dinilai** dalam threat model ini:

1. Keamanan internal dependency crate itu sendiri (`snow`, `arti-client`, `tor-hsservice`, `mdns-sd`, `x25519-dalek`, `ed25519-dalek`, dsb.) — audit source-level ini terbatas pada kode AKSARA sendiri.
2. Kebenaran implementasi CSPRNG level-OS yang mendasari `OsRng` (didelegasikan penuh ke OS; preseden historis seperti insiden Debian OpenSSL 2008 dicatat sebagai konteks umum di `04_CRYPTOGRAPHIC_JUSTIFICATION.md` CORE-7, bukan temuan spesifik AKSARA).
3. Serangan side-channel fisik/hardware (analisis daya, emisi elektromagnetik) — tidak ada evidence yang ditinjau, tidak ada klaim yang dibuat.
4. Ketahanan denial-of-service terhadap kondisi jaringan adversarial di luar yang sudah terdokumentasi (mis. tidak ada analisis rate-limiting yang dilakukan).
5. Skenario multi-device/sinkronisasi kunci — desain AKSARA saat ini (berdasarkan file yang diaudit) adalah satu identitas per satu perangkat; tidak ada permukaan ancaman multi-device untuk dinilai.
6. Rekomendasi perbaikan/roadmap remediasi teknis — **di luar cakupan TAHAP 7** (deskripsi ancaman, bukan rencana perbaikan; TAHAP 8 dan seterusnya berada di luar cakupan sesi ini per instruksi eksplisit).

---

## 6. Ringkasan Temuan (Risk Register Deskriptif)

Tabel ini **mendeskripsikan** temuan dan mitigasi yang **sudah ada** di kode — bukan rekomendasi perbaikan baru (di luar cakupan TAHAP 7).

| # | Temuan | Komponen | Kemungkinan* | Dampak* | Mitigasi yang sudah ada di kode |
|---|---|---|---|---|---|
| T1 | Tidak ada pengecekan identitas pada koneksi pertama ke kontak belum dikenal | Handshake (§4.3) | Sedang (butuh MITM aktif tepat saat first-contact) | Tinggi (impersonation penuh bila berhasil) | Verifikasi fingerprint manual out-of-band (di luar layer Noise) |
| T2 | Kebocoran metadata presence/fingerprint di LAN | Discovery mDNS (§4.2) | Tinggi (pasif, siapa pun di LAN yang sama) | Rendah-Sedang (metadata, bukan konten/kunci) | X25519 key tidak diiklankan; diakui eksplisit sebagai trade-off M1 |
| T3 | Invite code tidak diautentikasi kriptografis | Pertukaran kontak (§4.1) | Sedang (butuh kontrol atas kanal out-of-band) | Tinggi (mengikat korban ke kunci penyerang) | Fingerprint mengikat kedua key; verifikasi manual out-of-band |
| T4 | Tidak ada file-permission hardening pada vault/state Tor | Filesystem lokal (§4.5, §4.7) | Rendah-Sedang (butuh akses lokal ke mesin) | Sedang-Tinggi (bergantung permission OS default) | Enkripsi vault (Argon2id+ChaCha20Poly1305) tetap jadi lapisan proteksi utama |
| T5 | UI tidak membedakan penutupan sesi akibat tampering vs. normal | Transport (§4.4) | Rendah (butuh MITM aktif merusak frame berulang) | Rendah (fail-closed tetap terjadi; hanya kurang sinyal ke pengguna) | Fail-closed pada kegagalan dekripsi tetap berjalan |
| T6 | `FS_MISTRUST_DISABLE_PERMISSIONS_CHECKS` aktif tanpa syarat platform | Tor (§4.7) | Rendah-Sedang (butuh akses lokal multi-user) | Sedang (state/cache Tor, bukan vault identitas) | Tidak ada — kesenjangan antara niat komentar kode dan implementasi aktual |
| T7 | Tidak ada mekanisme rotasi/revokasi kunci apa pun | Key lifecycle (`07_KEY_LIFECYCLE.md` §6) | N/A (keterbatasan struktural, bukan probabilitas serangan) | Tinggi jangka panjang (kompromi key = tidak ada pemulihan in-band) | Tidak ada — dicatat sebagai keterbatasan desain M1 |

\* Kemungkinan/Dampak dinilai **kualitatif** berdasarkan evidence source-level yang tersedia, bukan skor kuantitatif terstandardisasi (mis. CVSS) — proporsional untuk cakupan tugas mata kuliah.

---

## 7. Catatan Anti-Overclaim (Ringkasan Kehati-hatian)

1. **Ed25519 tidak dipakai untuk tanda tangan aktif** — kategori ancaman "pemalsuan tanda tangan digital" tidak relevan untuk AKSARA hari ini karena tidak ada mekanisme signing yang berjalan untuk dipalsukan. Mekanisme autentikasi identitas yang benar-benar berlaku adalah verifikasi static-key X25519 dalam Noise_IK (§4.3) dan fingerprint out-of-band (§4.1).
2. Ancaman yang dibingkai terhadap sub-mekanisme internal Noise (hash/HKDF berbasis BLAKE2s) bersifat **hipotetis/confidence LOW**, karena internal ini tidak terverifikasi dari source AKSARA sendiri (`06_PROTOCOL_SPECIFICATION.md` §5.4).
3. Ancaman nonce-reuse ChaCha20-Poly1305 dibingkai sebagai **batasan desain yang sudah dipertimbangkan** (mitigasi: nonce random + rederivasi kunci per `seal()`/`save()`), **bukan** sebagai kerentanan nonce-reuse yang benar-benar ditemukan terjadi dalam audit ini.
4. Ketahanan brute-force Argon2id dinilai **kualitatif** (properti memory-hardness, `rfc9106`) — **tidak** dikuantifikasi dengan estimasi waktu-crack berbasis klaim "~100ms" yang tidak diverifikasi benchmark (`07_KEY_LIFECYCLE.md` §3.3).

---

## Referensi

Seluruh referensi teori pada dokumen ini menggunakan citekey yang **sudah ada** di `references/REFERENCES.bib`, termasuk `rfc6762`/`rfc6763` yang ditambahkan pada TAHAP 5 sesi ini (lihat `06_PROTOCOL_SPECIFICATION.md` §Referensi) — tidak ada entry baru lagi yang dibutuhkan untuk TAHAP 7: `noise2018` (properti desain Noise_IK yang diwarisi, §4.3), `rfc6762`/`rfc6763` (konteks mekanisme mDNS/DNS-SD, §4.2), `rfc9106`/`biryukov2016argon2` (properti memory-hardness Argon2id, §4.5/§4.6), `rfc8439` (properti AEAD ChaCha20-Poly1305, §4.4/§4.5).
