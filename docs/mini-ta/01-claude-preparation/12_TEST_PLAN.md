# 12 — Rencana Pengujian AKSARA

Dokumen ini adalah **rencana** pengujian (TAHAP 13) — bukan laporan hasil. Sesuai mandat `AGENTS.md`/`CLAUDE_PREPARATION_BRIEF.md`: **tidak ada data eksperimen yang dibuat di sini**; setiap sel hasil ditandai `WAITING_FOR_EXPERIMENT` sampai eksperimen benar-benar dijalankan (kemungkinan pada SESSION 5B atau sesi terpisah, di luar cakupan SESSION 5A).

Basis objek uji: `02_CRYPTO_IMPLEMENTATION_AUDIT.md` (ID `CR-xxx`), `03_CRYPTO_INVENTORY_NORMALIZED.md` (CORE-1..7), `06_PROTOCOL_SPECIFICATION.md` §8 (tabel bukti empiris test suite yang **sudah ada** di codebase), `07_KEY_LIFECYCLE.md`, `08_THREAT_MODEL.md`. Nama fungsi test yang dirujuk di bawah adalah test **yang sudah ada** di source (`cargo test`), dikonfirmasi lewat audit TAHAP 2/3/5/6 — bukan test baru yang diklaim sudah ditulis untuk sesi ini.

## 0. Cakupan dan Pemetaan 15 Kandidat Brief

`CLAUDE_PREPARATION_BRIEF.md` TAHAP 13 mendaftar 15 kandidat jenis pengujian. Sesuai batas scope (3-6 kelompok eksperimen realistis), 15 kandidat dipetakan ke **5 kelompok eksperimen** (EXP-01 s.d. EXP-05) di bawah — beberapa kandidat digabung dalam satu kelompok karena menguji objek/primitif yang sama, dan dua kandidat ditandai tidak berlaku (N/A) dengan alasan eksplisit.

| # | Kandidat brief | Kelompok eksperimen | Catatan cakupan |
|---|---|---|---|
| 1 | Correctness test | EXP-01, EXP-02, EXP-03, EXP-04 | Tersebar di seluruh kelompok fungsional |
| 2 | Known-answer test (KAT) | **N/A** | Tidak ditemukan test vector standar (mis. dari RFC 8439/RFC 9106) yang dipakai di test suite AKSARA — seluruh test bersifat roundtrip/property-based, bukan KAT terhadap vector resmi. Ditandai `NOT_FOUND`, bukan diasumsikan tersedia. |
| 3 | Encryption-decryption consistency | EXP-01 (vault), EXP-03 (transport), EXP-04 (contacts) | Tiga instance ChaCha20-Poly1305 (CORE-3) diuji terpisah sesuai konteks |
| 4 | Authentication failure test | EXP-02 (peer key salah), EXP-01 (passphrase salah) | |
| 5 | Modified ciphertext rejection | EXP-01 (vault, via ukuran/byte korup) | Untuk transport sesi (EXP-03), lihat catatan keterbatasan §EXP-03 poin 15 — tidak ada test siap pakai di source saat ini, test baru memerlukan modifikasi `tests`/`src` yang di luar wewenang sesi dokumentasi ini |
| 6 | Modified associated-data rejection | **N/A** | AKSARA tidak memakai AAD pada ketiga instance ChaCha20-Poly1305 manapun (dikonfirmasi `04_CRYPTOGRAPHIC_JUSTIFICATION.md` CORE-3 poin 13, `08_THREAT_MODEL.md` §4.4) — tidak ada AD untuk dimodifikasi, sehingga kelas pengujian ini tidak berlaku pada implementasi saat ini |
| 7 | Wrong-key rejection | EXP-01 (`wrong_key_fails` vault/contacts), EXP-02 (`wrong_peer_key_fails_handshake`) | |
| 8 | Replay rejection | **Dicatat sebagai keterbatasan**, bukan kelompok tersendiri | `08_THREAT_MODEL.md` tidak mencantumkan mekanisme replay-protection eksplisit (no sequence number/timestamp check terverifikasi) — dicatat di §EXP-03 poin 15 sebagai `NOT_FOUND`, bukan diasumsikan ada |
| 9 | Nonce handling test | EXP-01 (`vault_looks_random`), EXP-04 (nonce contact-store) | |
| 10 | Key agreement consistency | EXP-02 (`handshake_ik_roundtrip`) | |
| 11 | KDF consistency | EXP-01 (Argon2id determinism dari salt sama), EXP-04 (BLAKE2s contacts-key deterministik) | |
| 12 | Serialization-deserialization consistency | EXP-01 (vault byte layout), EXP-04 (`invite_roundtrip_*`) | |
| 13 | Performance benchmark | EXP-05 | |
| 14 | Ciphertext expansion | EXP-05 (diukur sebagai metrik sekunder — overhead tag 16 byte, deterministik dari spesifikasi bukan perlu diukur berulang) | |
| 15 | Memory usage | EXP-05 (opsional, sekunder — puncak RSS proses saat Argon2id berjalan, 19 MiB per parameter `CR-014`) | Diberi status opsional karena membutuhkan tooling profiling tambahan yang belum dikonfirmasi tersedia di lingkungan ini |

---

## EXP-01 — Correctness dan Rejection Vault Identitas (Argon2id + ChaCha20-Poly1305)

**Objek**: `identity::vault::seal()`/`unseal()` (CORE-3 instance vault CR-013/018, CORE-5 CR-014), diuji lewat (a) test suite `cargo test` yang sudah ada di `src/identity/vault.rs`, dan (b) CLI `aksara id --vault <path> --offline` (binary `target/release/aksara.exe`, terverifikasi berjalan SESSION 4) sebagai jalur verifikasi end-to-end tambahan.

1. **Tujuan**: Memverifikasi bahwa vault identitas mengenkripsi dan mendekripsi key material secara konsisten (roundtrip benar), dan menolak passphrase salah/vault korup secara aman (fail-closed, pesan error ambigu).
2. **Pertanyaan**: Apakah `seal(bundle, passphrase)` diikuti `unseal(vault, passphrase)` yang sama selalu menghasilkan `KeyBundle` identik? Apakah `unseal` dengan passphrase salah atau ciphertext yang dimodifikasi selalu gagal (tidak pernah menghasilkan key material salah yang lolos tanpa error)?
3. **Objek**: Fungsi `seal`/`unseal` di `src/identity/vault.rs`; test yang sudah ada: `seal_unseal_roundtrip`, `vault_looks_random` (keduanya dirujuk `07_KEY_LIFECYCLE.md` §3.2/§9); subcommand CLI `aksara id --vault <path> --offline`.
4. **Input**: (a) `KeyBundle` hasil `KeyBundle::generate()` (Ed25519+X25519 acak); (b) passphrase uji non-kosong (mis. string dummy, TIDAK boleh passphrase nyata pengguna — sesuai aturan data dummy aman `CLAUDE_PREPARATION_BRIEF.md` TAHAP 12); (c) untuk kasus rejection: passphrase salah (string berbeda) dan byte vault yang sengaja dimodifikasi (flip 1 byte pada region ciphertext).
5. **Baseline**: Tidak ada baseline eksternal (tidak ada implementasi vault AKSARA versi lain untuk dibandingkan) — baseline adalah **spesifikasi internal** yang sudah didokumentasikan (`07_KEY_LIFECYCLE.md` §3: layout 108 byte, parameter Argon2id 19 MiB/t=2/p=1).
6. **Variabel**: Variabel bebas — kondisi input (passphrase benar/salah, ciphertext utuh/dimodifikasi). Variabel terikat — hasil operasi (`Ok(KeyBundle)` identik vs `Err(Error::Decryption)`).
7. **Lingkungan**: Rust stable (versi ter-pin `rust-version 1.89` per `Cargo.toml`), build `--release` (commit `450d484` atau commit terbaru saat eksperimen dijalankan — WAJIB dicatat ulang), OS dan spesifikasi hardware **WAJIB dicatat saat eksperimen dijalankan** (belum ditentukan di sesi ini).
8. **Prosedur**:
   1. Jalankan `cargo test --release -p aksara vault::tests -- --nocapture` (nama modul path indikatif, sesuaikan dengan struktur test aktual saat eksekusi) dan catat pass/fail tiap test.
   2. Jalankan `aksara id --vault <path_dummy> --offline` dua kali berurutan dengan passphrase yang sama pada vault yang sama — bandingkan fingerprint/invite yang dicetak (harus identik, selaras verifikasi SESSION 4).
   3. Ulangi langkah 2 dengan passphrase salah — catat pesan error yang muncul (harus generik "vault could not be opened", tanpa membedakan penyebab).
   4. (Opsional, butuh script tambahan) Modifikasi 1 byte pada region ciphertext file vault dummy, jalankan ulang unseal, catat hasil (harus gagal).
9. **Jumlah pengulangan**: Minimum 10 kali untuk langkah roundtrip (2), guna menangkap kemungkinan non-determinisme tersembunyi; langkah 1 dan 3 cukup 1 kali jalan penuh test suite (hasil deterministik pass/fail, bukan diulang statistik).
10. **Metrik**: (a) proporsi roundtrip sukses (%); (b) proporsi rejection benar pada passphrase salah/ciphertext dimodifikasi (%); (c) hasil pass/fail tiap unit test.
11. **Satuan**: Persentase (%) untuk metrik (a)/(b); biner pass/fail untuk (c).
12. **Expected behavior**: Roundtrip 100% identik; rejection 100% pada seluruh kasus passphrase salah/ciphertext dimodifikasi/panjang file salah (selaras `07_KEY_LIFECYCLE.md` §3.4); tidak ada kasus di mana passphrase salah menghasilkan `Ok` dengan key material yang berbeda dari harapan.
13. **Data yang dicatat**: Output stdout test suite, output CLI per run, hash/fingerprint yang dicetak per run, pesan error persis per kasus rejection, versi commit dan environment.
14. **Metode analisis**: Perhitungan proporsi sukses/gagal sederhana (deskriptif) — tidak memerlukan uji statistik inferensial karena sifatnya deterministik/biner, bukan pengukuran kontinu bervariasi.
15. **Keterbatasan**: Tidak menguji klaim timing "~100ms" (dipisah ke EXP-05); tidak menguji ketahanan brute-force kuantitatif (di luar scope, `09_SCOPE_AND_TEAM_PLAN.md` §5); langkah 4 (modifikasi byte ciphertext) membutuhkan script kecil tambahan di luar `cargo test` bawaan — jika waktu terbatas, boleh dilewati dan ditandai `NEEDS_EXPERIMENT` pada laporan hasil tanpa membatalkan kelompok eksperimen ini.

---

## EXP-02 — Correctness dan Rejection Handshake Noise_IK (CORE-1, CORE-2)

**Objek**: `crypto::handshake::HandshakeSession` (CR-007/008/009/010/011) dan orkestrasi `session::run_session` (CR-026/027), diuji lewat test suite yang sudah ada.

1. **Tujuan**: Memverifikasi bahwa handshake Noise_IK 2-pesan menghasilkan sesi transport yang identik/konsisten di kedua sisi saat peer key benar, dan gagal secara aman saat peer key salah atau kontak tidak dikenal.
2. **Pertanyaan**: Apakah `do_handshake()` selalu menghasilkan `EncryptedSession` yang dapat saling berkomunikasi (enkripsi satu sisi terbaca sisi lain)? Apakah handshake dengan `peer_noise_pk` yang salah selalu gagal pada tahap DH (`es`)? Apakah responder menolak (fail-closed) peer dikenal dengan static key yang tidak cocok?
3. **Objek**: Test yang sudah ada — `handshake_ik_roundtrip`, `transport_encrypt_decrypt_roundtrip`, `responder_verifies_initiator_identity`, `wrong_peer_key_fails_handshake` (`src/crypto/handshake.rs`); `responder_rejects_unknown_peer` (`src/session/mod.rs`).
4. **Input**: Dua pasang `KeyBundle` uji (Initiator, Responder) hasil `generate()`; untuk kasus rejection, satu keypair pihak ketiga ("Eve") sebagai peer key salah.
5. **Baseline**: Properti umum pola Noise `IK` sebagaimana dispesifikasikan `noise2018` — dipakai sebagai kerangka acuan ekspektasi (bukan implementasi pembanding langsung, karena tidak ada implementasi Noise_IK AKSARA versi lain).
6. **Variabel**: Variabel bebas — kombinasi key (benar/salah/tidak dikenal). Variabel terikat — hasil handshake (`Ok`/`Err`, jenis `Error` yang dikembalikan).
7. **Lingkungan**: Sama seperti EXP-01 (Rust stable, build release, environment WAJIB dicatat saat eksekusi).
8. **Prosedur**:
   1. Jalankan `cargo test --release handshake -- --nocapture` dan `cargo test --release session -- --nocapture`, catat pass/fail per test.
   2. Untuk metrik latensi tambahan (bukan pass/fail semata): ukur waktu wall-clock `do_handshake()` end-to-end per pengulangan (butuh instrumentasi timer di sekitar pemanggilan test, atau microbenchmark terpisah jika `cargo bench` tersedia — dicatat `NEEDS_CONFIRMATION` apakah `benches/` ada di repo, tidak diverifikasi ulang di sesi ini).
9. **Jumlah pengulangan**: Minimum 30 kali untuk pengukuran latensi (langkah 2) agar layak dianalisis statistik dasar (rata-rata, median, standar deviasi); langkah 1 cukup 1 kali jalan penuh test suite.
10. **Metrik**: (a) pass/fail tiap test; (b) latensi handshake end-to-end (ms) bila diinstrumentasi.
11. **Satuan**: Biner pass/fail untuk (a); milidetik (ms) untuk (b).
12. **Expected behavior**: Seluruh test pass sesuai `06_PROTOCOL_SPECIFICATION.md` §8 (sudah terverifikasi ada di source, tapi status pass/fail aktual saat run harus dicatat ulang, bukan diasumsikan dari audit statis); latensi handshake berorde milidetik rendah (operasi X25519+ChaChaPoly ringan per `04_CRYPTOGRAPHIC_JUSTIFICATION.md` CORE-1 poin 8) — **tidak ada angka pasti yang diklaim di sini** sampai diukur.
13. **Data yang dicatat**: Output test suite, daftar waktu per pengulangan (bila diukur), versi commit, environment.
14. **Metode analisis**: Deskriptif (rata-rata, median, standar deviasi, min/max) untuk latensi; tabulasi pass/fail untuk correctness/rejection.
15. **Keterbatasan**: Sub-mekanisme internal Noise (hash/HKDF BLAKE2s) tidak dapat diuji terpisah dari source aplikasi (confidence LOW, `06_PROTOCOL_SPECIFICATION.md` §5.4) — pengujian ini hanya memverifikasi perilaku observable di boundary aplikasi, bukan internal `snow`; payload handshake 0-RTT tidak diuji (seluruh test existing memakai payload kosong).

---

## EXP-03 — Consistency dan Non-Fatal/Fatal Handling Transport Sesi Terenkripsi (CORE-3 via Noise transport)

**Objek**: `session::run_session` fase transport (`session.encrypt`/`session.decrypt`, CR-026), diuji lewat test suite yang sudah ada.

1. **Tujuan**: Memverifikasi konsistensi enkripsi-dekripsi pesan sesi end-to-end pada topologi LAN loopback, dan memverifikasi penanganan pesan oversize/keepalive sesuai spesifikasi (non-fatal untuk oversize, keepalive tidak bocor sebagai pesan).
2. **Pertanyaan**: Apakah pesan teks yang dikirim satu sisi selalu diterima identik di sisi lain? Apakah pesan yang melebihi `MAX_FRAME_LEN` (65535 byte) ditangani non-fatal (sesi tetap hidup)? Apakah keepalive ping tidak pernah muncul sebagai `SessionEvent::Message` di sisi penerima?
3. **Objek**: Test yang sudah ada — `lan_session_message_roundtrip`, `blur_toggle_roundtrip`, `oversized_message_does_not_kill_session`, `keepalive_ping_is_not_delivered_as_message` (`src/session/mod.rs`); `frame_roundtrip`, `multiple_frames_in_order`, `oversized_payload_rejected` (`src/transport/frame.rs`).
4. **Input**: Dua task `run_session` di atas TCP loopback (topologi uji sudah dipakai test existing); payload teks bervariasi ukuran (kecil, mendekati batas, melebihi batas 65535 byte — mengikuti test existing 70.000 byte).
5. **Baseline**: Spesifikasi internal `06_PROTOCOL_SPECIFICATION.md` §6.3-6.4 (format tag payload, batas ukuran pesan).
6. **Variabel**: Variabel bebas — ukuran payload, jenis pesan (teks/blur/ping). Variabel terikat — hasil pengiriman (diterima identik / `Notice` non-fatal / diabaikan).
7. **Lingkungan**: Sama seperti EXP-01/02, dengan tambahan: topologi loopback TCP lokal (127.0.0.1), tidak melibatkan jaringan LAN fisik maupun Tor pada eksperimen ini (dipisahkan sebagai potensi eksperimen lanjutan bila waktu mengizinkan, ditandai `NEEDS_EXPERIMENT` bila tidak dijalankan).
8. **Prosedur**:
   1. Jalankan `cargo test --release session:: -- --nocapture` dan `cargo test --release transport::frame -- --nocapture`, catat pass/fail per test.
   2. Untuk metrik overhead: hitung selisih ukuran ciphertext vs plaintext per pesan (harus tepat +16 byte tag, per `06_PROTOCOL_SPECIFICATION.md` §6.4) — dikonfirmasi dari kode/spesifikasi, verifikasi ulang via nilai aktual saat test dijalankan (bukan hanya dikutip dari dokumen ini).
9. **Jumlah pengulangan**: 1 kali jalan penuh test suite (deterministik); untuk overhead ciphertext, cukup 1 sampel per ukuran payload uji karena nilainya deterministik (bukan bervariasi acak).
10. **Metrik**: (a) pass/fail tiap test; (b) overhead ciphertext (byte) per ukuran payload.
11. **Satuan**: Biner pass/fail untuk (a); byte untuk (b).
12. **Expected behavior**: Seluruh test existing pass; overhead ciphertext konsisten +16 byte pada seluruh ukuran payload yang diuji (sesuai desain tag Poly1305 128-bit).
13. **Data yang dicatat**: Output test suite, tabel ukuran plaintext vs ciphertext per sampel, versi commit, environment.
14. **Metode analisis**: Tabulasi pass/fail; perhitungan selisih byte sederhana (deskriptif, bukan statistik inferensial karena deterministik).
15. **Keterbatasan**: **Tidak ada test rejection untuk ciphertext/frame yang dimodifikasi secara sengaja pada level transport sesi** (berbeda dengan vault EXP-01) yang ditemukan di source teraudit — menulis test baru untuk skenario ini akan memerlukan modifikasi `src/`/`tests/` yang berada di luar wewenang sesi dokumentasi (`AGENTS.md` §Source-Code Protection: "Source changes require an explicit user request"). Kelompok ini ditandai `NEEDS_EXPERIMENT` untuk sub-skenario modified-ciphertext-rejection transport sesi — dapat dieksekusi pada sesi terpisah setelah persetujuan eksplisit pengguna untuk menambah test. Replay rejection dan modified-AD rejection juga **tidak berlaku/tidak ditemukan** (lihat §0 tabel pemetaan).

---

## EXP-04 — Correctness Invite Code, Fingerprint Binding, dan Contact Store (CORE-4 BLAKE2s, helper encoding)

**Objek**: `contacts::mod` — `fingerprint()`, `encode_invite()`/`decode_invite()`, `derive_contacts_key()`, `save_contacts()`/`load_contacts()` (CR-001..006), diuji lewat test suite yang sudah ada.

1. **Tujuan**: Memverifikasi bahwa fingerprint mengikat kedua public key secara konsisten, invite code dapat di-roundtrip tanpa kehilangan informasi, dan contact store terenkripsi konsisten dapat disimpan/dibaca kembali dengan kunci yang benar sekaligus menolak kunci yang salah.
2. **Pertanyaan**: Apakah `fingerprint(ed_pub, noise_pub)` selalu menghasilkan output yang sama untuk input yang sama (deterministik), dan berbeda bila salah satu key ditukar (binding kedua key, anti-invite-susun-ulang)? Apakah `encode_invite`/`decode_invite` roundtrip lossless? Apakah `load_contacts` dengan kunci salah selalu gagal, bukan menghasilkan data salah yang lolos?
3. **Objek**: Test yang sudah ada — `fingerprint_binds_both_keys`, `fingerprint_is_64_hex_chars`, `invite_has_no_obvious_prefix`, `invite_roundtrip_lan_only`, `invite_roundtrip_with_onion`, `invite_rejects_garbage`, `invite_rejects_wrong_length`, `contacts_save_load_roundtrip`, `contacts_load_missing_file_is_empty`, `contacts_wrong_key_fails` (seluruhnya `src/contacts/mod.rs`).
4. **Input**: Pasangan public key Ed25519/X25519 uji; invite string valid dan invalid (panjang salah, karakter sampah); daftar kontak dummy (nickname + fingerprint + alamat dummy, TANPA data pengguna nyata).
5. **Baseline**: Spesifikasi internal `06_PROTOCOL_SPECIFICATION.md` §3 (format invite, binding fingerprint).
6. **Variabel**: Variabel bebas — validitas input (key/invite/kunci contact-store benar vs salah). Variabel terikat — hasil operasi (`Ok` dengan nilai identik vs `Err`).
7. **Lingkungan**: Sama seperti kelompok sebelumnya.
8. **Prosedur**:
   1. Jalankan `cargo test --release contacts:: -- --nocapture`, catat pass/fail per test.
   2. Untuk metrik tambahan: catat panjang string invite yang dihasilkan (harus konsisten dengan format `base64url_no_pad(64 byte)` ± suffix onion, per `06_PROTOCOL_SPECIFICATION.md` §3).
9. **Jumlah pengulangan**: 1 kali jalan penuh test suite (deterministik); untuk panjang string invite, cukup beberapa sampel key acak berbeda (mis. 5 sampel) untuk konfirmasi konsistensi format.
10. **Metrik**: (a) pass/fail tiap test; (b) panjang string invite (karakter) per sampel key.
11. **Satuan**: Biner pass/fail untuk (a); jumlah karakter untuk (b).
12. **Expected behavior**: Seluruh test existing pass; panjang invite konsisten (~86 karakter untuk 64 byte base64url tanpa padding, tanpa suffix onion) di seluruh sampel.
13. **Data yang dicatat**: Output test suite, tabel panjang invite per sampel, versi commit, environment.
14. **Metode analisis**: Tabulasi pass/fail; pengecekan konsistensi panjang string (deskriptif).
15. **Keterbatasan**: Tidak menguji keamanan verifikasi fingerprint out-of-band oleh manusia (di luar scope pengujian otomatis — ini adalah kontrol prosedural, bukan kontrol kode, per `08_THREAT_MODEL.md` §4.1); tidak menguji alamat onion tidak-valid secara format (kode memperlakukan onion sebagai string opaque tanpa validasi, sesuai `06_PROTOCOL_SPECIFICATION.md` §3 — sehingga tidak ada perilaku rejection untuk diuji pada aspek ini).

---

## EXP-05 — Benchmark Kinerja Argon2id (Waktu Unlock Vault) dan Ciphertext Expansion

**Objek**: `identity::vault::seal()`/`unseal()` — parameter Argon2id (`m=19*1024 KiB, t=2, p=1`, CR-014); dipilih sebagai satu-satunya eksperimen performa (bukan sekadar correctness) karena mengoreksi/mengonfirmasi klaim komentar kode "~100ms" yang berstatus `DOCUMENTED_ONLY`/LOW confidence (`07_KEY_LIFECYCLE.md` §3.3, CB-087) — satu-satunya klaim performa eksplisit dalam source yang belum diverifikasi benchmark di seluruh audit TAHAP 1-12.

1. **Tujuan**: Mengukur waktu wall-clock aktual `unseal()` (dan `seal()`) pada hardware yang tersedia, untuk mengonfirmasi atau mengoreksi klaim "~100ms" pada komentar kode, serta mendokumentasikan ciphertext expansion vault sebagai metrik sekunder deterministik.
2. **Pertanyaan**: Berapa rata-rata dan sebaran waktu `unseal()`/`seal()` vault pada hardware uji? Apakah nilainya mendekati klaim "~100ms", jauh lebih cepat, atau jauh lebih lambat?
3. **Objek**: `identity::vault::seal`/`unseal` (`src/identity/vault.rs:58-128`); alternatif jalur pengukuran non-invasif: subcommand CLI `aksara id --vault <path> --offline` (tidak butuh modifikasi source, waktu diukur dari sisi luar proses, mis. `Measure-Command` PowerShell atau `time` POSIX pada Bash tool).
4. **Input**: Vault dummy dengan `KeyBundle` dan passphrase uji (sama seperti EXP-01, data dummy aman).
5. **Baseline**: Klaim komentar kode "~100 ms pada hardware modern" (`vault.rs:33-38`, dikutip `07_KEY_LIFECYCLE.md` §3.3) — dipakai sebagai **titik pembanding**, bukan kebenaran yang diasumsikan.
6. **Variabel**: Variabel bebas — tidak ada manipulasi (parameter Argon2id tetap/konstan di source, tidak dapat divariasikan tanpa mengubah kode). Variabel terikat — waktu eksekusi (ms).
7. **Lingkungan**: **WAJIB dicatat lengkap saat eksekusi** — model CPU, jumlah core, RAM tersedia, OS dan versi, apakah dijalankan di VM/container atau bare-metal (kritis untuk Argon2id karena memory-hard, hasil sangat bergantung kecepatan RAM/kontensi memori sistem), build `--release` (bukan debug — signifikan untuk operasi crypto-heavy).
8. **Prosedur**:
   1. Build `cargo build --release` (pastikan versi/commit tercatat).
   2. Jalankan `unseal()` (via `aksara id --vault <path> --offline` atau harness benchmark internal bila `cargo bench`/`criterion` tersedia — `NEEDS_CONFIRMATION` apakah `benches/` dikonfigurasi di `Cargo.toml`, tidak diverifikasi ulang di sesi ini) sejumlah N pengulangan dengan **cold-start proses baru per pengulangan** (bukan loop dalam satu proses) agar representatif terhadap skenario nyata (satu kali unlock per sesi pemakaian aplikasi).
   3. Catat waktu wall-clock per pengulangan dari sisi eksternal proses.
   4. Untuk ciphertext expansion: bandingkan ukuran plaintext (64 byte: 32B Ed25519 sk + 32B X25519 sk) dengan ukuran vault total (108 byte: 16B salt + 12B nonce + 64B ciphertext + 16B tag) — nilai ini deterministik dari spesifikasi (`07_KEY_LIFECYCLE.md` §3.1), verifikasi ulang lewat pengukuran ukuran file aktual saat eksperimen (bukan hanya dikutip).
9. **Jumlah pengulangan**: Minimum 30 cold-start run untuk metrik waktu (agar mean/median/stdev layak dilaporkan); 1 sampel cukup untuk ukuran file (deterministik, kecuali ingin verifikasi konsistensi lintas beberapa vault berbeda — disarankan minimal 3 vault berbeda).
10. **Metrik**: (a) waktu `unseal()` end-to-end (ms) — mean, median, standar deviasi, min, max; (b) ukuran ciphertext vault (byte, harus tepat 108).
11. **Satuan**: Milidetik (ms) untuk (a); byte untuk (b).
12. **Expected behavior**: Waktu unlock berorde puluhan-ratusan milidetik (konsisten dengan parameter memory-hard 19 MiB, t=2), namun **angka pasti TIDAK diklaim sebelum diukur** — hasil dapat mengonfirmasi ATAU mengoreksi klaim "~100ms" tergantung hardware aktual; ukuran vault selalu tepat 108 byte pada seluruh sampel.
13. **Data yang dicatat**: Daftar waktu per run (ms), spesifikasi hardware/OS lengkap, ukuran file vault per sampel, versi commit/build flag.
14. **Metode analisis**: Statistik deskriptif (mean, median, standar deviasi, min, max, mungkin histogram sederhana) untuk waktu; perbandingan langsung ukuran file terukur vs spesifikasi 108 byte untuk ciphertext expansion. Tidak diperlukan uji hipotesis formal (bukan perbandingan dua kelompok berbeda) — cukup deskriptif dan interpretasi kualitatif terhadap klaim "~100ms".
15. **Keterbatasan**: Hasil sangat bergantung hardware spesifik pengujian — **tidak dapat digeneralisasi sebagai klaim performa universal AKSARA** di seluruh kelas hardware; tidak mengukur memory usage puncak (metrik #15 kandidat brief) kecuali tooling profiling tambahan dikonfirmasi tersedia saat eksekusi — bila tidak tersedia, metrik memory usage cukup dilaporkan dari nilai parameter statis (19 MiB, deterministik dari kode) tanpa pengukuran RSS aktual, ditandai `NEEDS_EXPERIMENT` untuk pengukuran runtime-nya.

---

## Ringkasan 5 Kelompok Eksperimen

| ID | Nama | Objek utama | Primitif (CORE-x) | Jenis metrik dominan |
|---|---|---|---|---|
| EXP-01 | Correctness & rejection vault | `identity::vault` | CORE-3, CORE-5 | Biner (pass/fail, %) |
| EXP-02 | Correctness & rejection handshake Noise_IK | `crypto::handshake`, `session::run_session` (fase handshake) | CORE-1, CORE-2 | Biner + latensi (ms) |
| EXP-03 | Consistency transport sesi | `session::run_session` (fase transport), `transport::frame` | CORE-3 (transport) | Biner + overhead (byte) |
| EXP-04 | Correctness invite/fingerprint/contact store | `contacts::mod` | CORE-4, helper encoding | Biner + panjang string |
| EXP-05 | Benchmark Argon2id + ciphertext expansion | `identity::vault` (performa) | CORE-5, CORE-3 | Waktu (ms) + ukuran (byte) |

**Total metrik unik lintas kelompok**: 7 (proporsi sukses roundtrip %, proporsi rejection benar %, pass/fail unit test, latensi handshake ms, overhead ciphertext byte, panjang string invite karakter, waktu unlock vault ms) — memenuhi rentang 4-8 metrik yang disyaratkan `CLAUDE_PREPARATION_BRIEF.md` §Batas Scope.

## Status Eksekusi

Seluruh 5 kelompok berstatus **`WAITING_FOR_EXPERIMENT`** pada akhir SESSION 5A — rencana ini disiapkan untuk dieksekusi pada sesi terpisah (kemungkinan SESSION 5B atau sesi khusus eksperimen, tergantung kuota dan keputusan pengguna). Template pencatatan hasil: `docs/mini-ta/02-experiment-data/EXPERIMENT_RESULT_TEMPLATE.csv`.

## Referensi

Dokumen ini tidak memperkenalkan referensi teori baru — seluruh rujukan primitif menggunakan citekey yang sudah ada di `references/REFERENCES.bib` (`noise2018`, `rfc8439`, `rfc9106`, `rfc7693`, dst., sudah dikutip di `06_PROTOCOL_SPECIFICATION.md`/`07_KEY_LIFECYCLE.md`).
