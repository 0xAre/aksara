# 03 — Normalisasi Inventaris Kriptografi AKSARA

Sumber tunggal: 36 entry `CR-001`..`CR-036` di `02_CRYPTO_IMPLEMENTATION_AUDIT.md` (evidence lengkap per entry — path, baris, versi library, confidence, risiko — tidak diulang di sini, hanya dirujuk via ID). Dokumen ini menambahkan lapisan kategorisasi dan konsolidasi, bukan audit ulang. Tidak ada source code baru dibaca untuk menyusun dokumen ini kecuali disebutkan eksplisit sebagai verifikasi targeted.

## 1. Skema Kategori

| Kategori | Definisi | Konsekuensi untuk TAHAP 4 |
|----------|----------|----------------------------|
| **Algoritma inti** | Pemanggilan/konfigurasi langsung sebuah algoritma kriptografi standar (AEAD, hash, KDF, key agreement, CSPRNG) di titik kode tersebut. | Kandidat utama dibahas di `04_CRYPTOGRAPHIC_JUSTIFICATION.md` dan `05_CRYPTO_ALTERNATIVE_COMPARISON.md`. |
| **Key material** | Deskripsi objek kunci (generate/simpan/serialize) tanpa memanggil algoritma baru — kunci itu sendiri, bukan operasi kriptografi baru. | Dilebur ke narasi algoritma induknya (tidak dapat justifikasi/perbandingan terpisah). |
| **Parameter** | Nilai konfigurasi (ukuran nonce, tag, key, cost parameter) yang melekat pada suatu algoritma inti. | Dikutip sebagai parameter di dalam justifikasi algoritma induk. |
| **Mekanisme protokol** | Konstruksi struktural yang dibangun DI ATAS satu/lebih algoritma inti (format handshake, layout file, binding fingerprint) — bukan primitif itu sendiri. | Dibahas singkat sebagai konteks pemakaian, bukan entri justifikasi/perbandingan tersendiri. |
| **Kontrol nonkriptografis** | Mekanisme keamanan yang bukan algoritma kriptografi (desain pesan error ambigu, instalasi crypto-provider dependency, orkestrasi tanpa primitif langsung). | Dicatat sebagai batasan/konteks, di luar cakupan perbandingan algoritma. |
| **Helper** | Encoding/serialisasi murni (base64, hex, raw byte array) tanpa properti keamanan kriptografis sendiri. | Disebut sebagai detail implementasi, tidak dibahas sebagai "algoritma". |
| **Duplikasi** | Titik pemanggilan/akses tambahan atas primitif yang telah dicatat entry lain (modul berbeda, fungsi yang sama). | Diarahkan ke entry induk lewat kolom "Primitif Induk"; tidak menambah cakupan baru. |

## 2. Tabel Normalisasi (36 entry)

| ID | Ringkasan Lokasi | Kategori | Primitif Induk | Catatan Normalisasi |
|----|-------------------|----------|-----------------|----------------------|
| CR-001 | contacts/mod.rs:170-198 — ChaCha20-Poly1305 contact-store | Algoritma inti | **CORE-3** ChaCha20-Poly1305 | Instance ke-2 (dari 3) pemakaian AEAD ini di codebase. |
| CR-002 | contacts/mod.rs:48-54 — BLAKE2s256 fingerprint | Algoritma inti | **CORE-4** BLAKE2s | Juga berfungsi sebagai mekanisme binding fingerprint (lihat CR-029, CR-035). |
| CR-003 | contacts/mod.rs:104-112 — BLAKE2s256 contacts-key KDF | Algoritma inti | **CORE-4** BLAKE2s | Pemakaian BLAKE2s sebagai KDF single-shot, BUKAN HKDF terstandar — dicatat sebagai keterbatasan desain di justifikasi. |
| CR-004 | contacts/mod.rs:173-176 — OsRng nonce contact-store | Algoritma inti | **CORE-7** OsRng | Instance CSPRNG untuk nonce AEAD contact-store. |
| CR-005 | contacts/mod.rs:59-92 — Base64 URL-safe invite | Helper | — | Encoding transport murni, tanpa proteksi integritas/kerahasiaan sendiri (invite tidak ditandatangani, dicatat eksplisit di kode). |
| CR-006 | contacts/mod.rs:114-138 — Hex encoding | Helper | — | Representasi teks reversibel penuh, tanpa properti keamanan. |
| CR-007 | crypto/handshake.rs:21-47 — X25519 DH token es/ss/ee/se | Algoritma inti | **CORE-2** X25519 | Dijalankan internal oleh `snow`; bagian dari mekanisme Noise_IK (CORE-1). |
| CR-008 | crypto/handshake.rs:21-98 — ChaCha20-Poly1305 (Noise ChaChaPoly) | Algoritma inti | **CORE-3** ChaCha20-Poly1305 | Instance ke-1 (dari 3); enkripsi payload handshake dan pesan transport pasca-handshake. |
| CR-009 | crypto/handshake.rs:21 — BLAKE2s sebagai hash Noise (inferensi) | Algoritma inti | **CORE-4** BLAKE2s | LOW confidence — tidak ada pemanggilan eksplisit di file; inferensi murni dari nama pattern `Noise_IK_25519_ChaChaPoly_BLAKE2s`. |
| CR-010 | crypto/handshake.rs:21 — Noise HKDF berbasis BLAKE2s (inferensi) | Mekanisme protokol | **CORE-4** BLAKE2s (KDF internal Noise) | LOW confidence, sama seperti CR-009 — konstruksi HKDF-Noise sepenuhnya internal `snow`, tidak diverifikasi dari source aplikasi. |
| CR-011 | crypto/handshake.rs:32-46 — key Noise sebagai `[u8;32]` mentah | Helper | — | Representasi byte, bukan operasi kriptografi. |
| CR-012 | crypto/handshake.rs:18 — CSPRNG ephemeral/static key (NOT_FOUND di file ini) | Duplikasi | **CORE-7** OsRng | Temuan negatif file-lokal; evidence aktual CSPRNG ada di CR-004/CR-017. |
| CR-013 | identity/vault.rs:60-128 — ChaCha20-Poly1305 AEAD vault | Algoritma inti | **CORE-3** ChaCha20-Poly1305 | Instance ke-3; melindungi 64 byte secret key material saat disimpan di disk. |
| CR-014 | identity/vault.rs:39-56 — Argon2id KDF | Algoritma inti | **CORE-5** Argon2id | Satu-satunya pemakaian Argon2id di codebase; parameter 19 MiB/t=2/p=1/output 32 byte. |
| CR-015 | identity/keypair.rs:6-38 — Ed25519 identity keypair | Key material | **CORE-6** Ed25519 | Hanya generate/simpan; TIDAK ada pemanggilan sign()/verify() ditemukan di file manapun yang diaudit. |
| CR-016 | identity/keypair.rs:40-72 — X25519 Noise keypair | Key material | **CORE-2** X25519 | Generate/simpan static key untuk Noise_IK. |
| CR-017 | identity/keypair.rs:2, vault.rs:20 — OsRng key/salt/nonce | Algoritma inti | **CORE-7** OsRng | Evidence paling lengkap untuk OsRng: dipakai di 4 titik (key Ed25519, key X25519, salt Argon2id, nonce ChaCha20Poly1305). |
| CR-018 | identity/vault.rs:74-75 — nonce 96-bit ChaCha20Poly1305 | Parameter | **CORE-3** ChaCha20-Poly1305 | Parameter nonce untuk instance vault (CR-013); dibangkitkan acak, bukan counter. |
| CR-019 | identity/vault.rs:1-31 — layout biner vault | Mekanisme protokol | **CORE-3 + CORE-5** (gabungan) | Format fixed-offset tanpa header/magic/versi — desain disengaja (plausible deniability / "SEC-05"), bukan primitif tersendiri. |
| CR-020 | main.rs:213-215 — rustls default CryptoProvider (ring) | Kontrol nonkriptografis | — | Inisialisasi backend TLS untuk `arti-client` (Tor), BUKAN bagian dari protokol P2P AKSARA sendiri; di luar cakupan justifikasi/perbandingan algoritma inti. |
| CR-021 | main.rs:187-188 — akses Ed25519 pubkey | Duplikasi | **CORE-6** Ed25519 | Call-site tambahan atas CR-015, di layer main.rs. |
| CR-022 | main.rs:189-190 — akses X25519 key material | Duplikasi | **CORE-2** X25519 | Call-site tambahan atas CR-016, di layer main.rs. |
| CR-023 | main.rs:179 — `KeyBundle::generate()` | Duplikasi | **CORE-6 + CORE-2 + CORE-7** | Orkestrasi call-site yang menggabungkan CR-015+CR-016+CR-017; bukan primitif baru. |
| CR-024 | main.rs:167-185 — vault seal/unseal call-site | Duplikasi | **CORE-3 + CORE-5** | Orkestrasi call-site atas CR-013+CR-014 di layer main.rs. |
| CR-025 | error.rs:16-17 — Noise error passthrough | Kontrol nonkriptografis | — | Plumbing tipe error (`snow::Error` → `Error::Noise`), bukan operasi kriptografi. |
| CR-026 | session/mod.rs:164-279 — wrapper encrypt/decrypt sesi | Duplikasi | **CORE-3** ChaCha20-Poly1305 (via Noise transport) | Call-site tambahan atas CR-008, di layer session. |
| CR-027 | session/mod.rs:117-159 — orkestrasi handshake Noise_IK | Duplikasi | **CORE-1** Noise_IK (CR-007/008/009/010/011) | Call-site tambahan yang menjalankan role Initiator/Responder; bukan primitif baru. |
| CR-028 | session/mod.rs:96-97 — key Noise sebagai byte mentah (boundary fungsi) | Helper | — | Duplikat konsep dari CR-011 di file berbeda. |
| CR-029 | transport/lan.rs:5-90 — fingerprint Ed25519 hex, perbandingan non-constant-time | Duplikasi | **CORE-4** BLAKE2s (fingerprint, CR-002) | Catatan tambahan: `role_from_fp` membandingkan fingerprint dengan operator `<` bawaan `&str` (byte-wise, non-constant-time) — risiko dinilai rendah karena kedua fingerprint publik, tapi dicatat sebagai keterbatasan kontrol nonkriptografis. |
| CR-030 | transport/tor.rs:1-122 — tidak ada primitif kripto langsung | Kontrol nonkriptografis | — | Temuan negatif eksplisit — kripto onion-service Tor v3 didelegasikan penuh ke dependency `arti-client`/`tor-hsservice`, di luar source AKSARA yang diaudit. |
| CR-031 | tui/mod.rs:281-292 — ekstraksi Ed25519 pubkey | Duplikasi | **CORE-6** Ed25519 | Call-site tambahan atas CR-015/CR-021, di layer TUI. |
| CR-032 | tui/mod.rs:32-38 — static keypair Noise/X25519 | Duplikasi | **CORE-2** X25519 | Call-site tambahan atas CR-016/CR-022, di layer TUI. |
| CR-033 | tui/mod.rs:559-592 — vault seal/unseal (TUI) | Duplikasi | **CORE-3 + CORE-5** | Call-site tambahan atas CR-013/CR-014/CR-024, di layer TUI. |
| CR-034 | tui/mod.rs:182 — `derive_contacts_key` call-site | Duplikasi | **CORE-4** BLAKE2s | Call-site tambahan atas CR-003, di layer TUI. |
| CR-035 | tui/mod.rs:286 — `contacts::fingerprint` call-site | Duplikasi | **CORE-4** BLAKE2s | Call-site tambahan atas CR-002/CR-029, di layer TUI. |
| CR-036 | tui/mod.rs:584 — `KeyBundle::generate()` (TUI) | Duplikasi | **CORE-7** OsRng | Call-site tambahan atas CR-017/CR-023, di layer TUI. |

## 3. Rekapitulasi per Kategori

| Kategori | Jumlah | ID |
|----------|--------|-----|
| Algoritma inti | 10 | CR-001, 002, 003, 004, 007, 008, 009, 013, 014, 017 |
| Key material | 2 | CR-015, 016 |
| Parameter | 1 | CR-018 |
| Mekanisme protokol | 2 | CR-010, 019 |
| Kontrol nonkriptografis | 3 | CR-020, 025, 030 |
| Helper | 4 | CR-005, 006, 011, 028 |
| Duplikasi | 14 | CR-012, 021, 022, 023, 024, 026, 027, 029, 031, 032, 033, 034, 035, 036 |
| **Total** | **36** | |

Catatan silang-kategori: CR-002 (algoritma inti) dan CR-019 (mekanisme protokol) sekaligus menjadi rujukan mekanisme untuk beberapa entry duplikasi (CR-029, CR-035 untuk fingerprint; CR-024, CR-033 untuk vault). Ini disengaja — satu primitif dapat punya banyak titik pakai; kolom "Primitif Induk" menjaga ketertelusuran tanpa menghitung ganda cakupan pembahasan.

## 4. Konsolidasi Komponen Kriptografi Inti (CORE-1 s.d. CORE-7)

Menggabungkan seluruh "algoritma inti" + "key material" + mekanisme protokol yang relevan menjadi 7 komponen yang dibahas di `04_CRYPTOGRAPHIC_JUSTIFICATION.md` dan `05_CRYPTO_ALTERNATIVE_COMPARISON.md`:

| # | Komponen | Fungsi utama | Semua evidence ID (algoritma inti + key material + duplikasi) | Confidence gabungan |
|---|----------|---------------|-----------------------------------------------------------------|----------------------|
| CORE-1 | **Noise_IK** (pola handshake, via `snow` 0.10.0) | Mekanisme protokol autentikasi + key agreement 2-pesan | CR-007, 008, 009, 010, 011, 026, 027, 028 | MEDIUM (orkestrasi terverifikasi; sub-mekanisme internal `snow` seperti hash/HKDF hanya inferensi nama pattern — LOW) |
| CORE-2 | **X25519** (Curve25519 ECDH) | Key agreement (Diffie-Hellman) dalam Noise_IK | CR-007, 016, 022, 032 | HIGH (generate/simpan key terverifikasi HIGH; pemakaian DH dalam handshake MEDIUM karena internal `snow`) |
| CORE-3 | **ChaCha20-Poly1305** (RFC 8439) | AEAD — 3 konteks berbeda: transport sesi (Noise), vault identitas, contact store | CR-001, 008, 013, 018, 024, 026, 033 | HIGH untuk vault & contact store (source langsung terlihat); MEDIUM untuk transport Noise (nonce dikelola internal `snow`, tidak terlihat dari source aplikasi) |
| CORE-4 | **BLAKE2s / BLAKE2s-256** | Hash — 3 peran: fingerprint identitas, KDF ad hoc contact-store key, hash internal Noise (transcript + HKDF) | CR-002, 003, 009, 010, 029, 034, 035 | HIGH untuk fingerprint & contacts-key; LOW untuk peran internal Noise (inferensi nama pattern) |
| CORE-5 | **Argon2id** (RFC 9106) | Password-based key derivation untuk kunci enkripsi vault | CR-014, 024, 033 | HIGH |
| CORE-6 | **Ed25519** | Identity keypair jangka panjang (dasar fingerprint) | CR-015, 021, 031 | PARTIAL — generate/simpan/ekspor HIGH, tapi operasi sign/verify TIDAK ditemukan di source yang diaudit (lihat batasan di §5) |
| CORE-7 | **OsRng** (`rand::rngs::OsRng`, OS CSPRNG) | Sumber entropi untuk seluruh key/salt/nonce generation | CR-004, 012, 017, 023, 036 | HIGH |

## 5. Komponen yang Sengaja Tidak Dibahas Sebagai "Inti"

Agar `04`/`05` proporsional dengan cakupan tugas mata kuliah, komponen berikut TIDAK mendapat entry justifikasi/perbandingan algoritma tersendiri, dengan alasan eksplisit:

- **Base64 URL-safe & Hex encoding** (CR-005, CR-006, CR-011, CR-028) — murni serialisasi/representasi, tanpa properti keamanan kriptografis untuk dijustifikasi atau dibandingkan alternatifnya.
- **rustls/ring CryptoProvider** (CR-020) — dependency inisialisasi untuk stack Tor (`arti-client`), bukan bagian dari desain protokol P2P AKSARA sendiri. Algoritma TLS spesifik tidak dirinci di titik pemanggilan dan di luar cakupan file yang diaudit.
- **Vault binary layout** (CR-019) — keputusan desain format, bukan algoritma; dibahas sebagai konteks pemakaian Argon2id+ChaCha20-Poly1305 (CORE-3/CORE-5), bukan entry berdiri sendiri.
- **Error handling / oracle-attack mitigation** (CR-025, dan pesan error ambigu pada CR-014/CR-024) — kontrol keamanan yang relevan, tapi bukan algoritma kriptografi; dicatat sebagai catatan desain dalam justifikasi Argon2id/vault.
- **Perbandingan fingerprint non-constant-time** (CR-029) — dicatat sebagai keterbatasan dalam justifikasi CORE-4 (fingerprint), bukan topik perbandingan algoritma tersendiri.
- **Tor onion-service crypto** (CR-030) — eksplisit `NOT_FOUND` di source AKSARA; sepenuhnya didelegasikan ke crate `arti-client`/`tor-hsservice` (Tor v3 spec, di luar audit source-level ini). Disebut sebagai batasan cakupan, tidak dijustifikasi sebagai pilihan algoritma AKSARA sendiri.

## 6. Klaim yang Perlu Kehati-hatian Khusus di TAHAP 4

Dibawa dari `SESSION_1_HANDOFF.md`, dikonfirmasi tetap berlaku setelah normalisasi:

1. **CORE-1 (Noise_IK) sub-mekanisme internal** (hash Noise, HKDF) berstatus confidence LOW — murni inferensi dari string nama pattern `Noise_IK_25519_ChaChaPoly_BLAKE2s`, tidak ada pemanggilan langsung di source aplikasi (CR-009, CR-010). Justifikasi TAHAP 4 harus menyatakan ini secara eksplisit, bukan mengklaim terverifikasi penuh.
2. **CORE-6 (Ed25519) hanya PARTIAL** — tidak ada bukti `sign()`/`verify()` di scope audit manapun (CB-084 pada evidence matrix codebase mengonfirmasi silang: grep `sign(`/`verify(`/`Signature` di tiga file identity/*.rs nihil hasil). Kunci Ed25519 di AKSARA saat ini berfungsi sebagai bahan fingerprint/identitas publik, BUKAN sebagai mekanisme tanda tangan aktif yang teraudit.
3. **Invite code tidak diautentikasi secara kriptografis** — base64 (CR-005) murni transport, bergantung pada verifikasi fingerprint out-of-band oleh pengguna.
4. **Tidak ada rotasi key eksplisit** untuk kunci identitas jangka panjang maupun kunci vault (CR-013 s.d. CR-019 tidak menunjukkan mekanisme rotasi).
5. Beberapa boundary buffer (passphrase, plaintext hasil dekripsi) tidak memakai tipe zeroizing eksplisit meski `ZeroizeOnDrop` dipakai konsisten pada tipe key material inti (`IdentityKey`, `NoiseKey`, `KeyBundle`).

## 7. Verifikasi Targeted (jika ada)

Tidak ada pembacaan source code baru yang diperlukan untuk menyusun normalisasi ini — seluruh 36 entry dan cross-check CB-084 sudah tersedia dari `02_CRYPTO_IMPLEMENTATION_AUDIT.md` dan `evidence/CODE_EVIDENCE_MATRIX.md` TAHAP 2/3. Tidak ada klaim ambigu yang memerlukan pembacaan source ulang pada tahap normalisasi ini.
