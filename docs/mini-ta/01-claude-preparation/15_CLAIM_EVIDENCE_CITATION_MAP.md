# 15 — Peta Klaim, Evidence, dan Sitasi AKSARA

Peta traceability (TAHAP 16) yang menghubungkan setiap klaim substansial di `14_CHAPTER_CONTENT_PACK.md` (BAB I-IV) ke evidence source-level, referensi teori, data eksperimen (bila relevan), bab tujuan, dan status. Format kolom sesuai brief: `Claim ID | Klaim | Evidence Code | Referensi | Data Eksperimen | Bab | Status`.

**Aturan yang diikuti** (`CLAUDE_PREPARATION_BRIEF.md` TAHAP 16): klaim implementasi didukung source code; klaim teori didukung referensi; klaim keamanan didukung model+referensi; klaim performa didukung eksperimen; klaim hasil didukung data; klaim kontribusi didukung perbandingan.

**Skop**: peta ini beroperasi pada level "claim family" (proposisi yang benar-benar dituliskan di content pack), bukan mendaftar ulang seluruh 36 entry `CR-xxx`/152 entry `CB-xxx` mentah satu-per-satu (itu sudah tersedia utuh di `02_CRYPTO_IMPLEMENTATION_AUDIT.md`/`evidence/CODE_EVIDENCE_MATRIX.md`) — kolom "Evidence Code" merujuk ID mentah yang relevan per klaim.

Prefix ID baru pada peta ini: `CM-xxx` (Claim Map).

---

## 1. Identitas Proyek dan Arsitektur Umum

| Claim ID | Klaim | Evidence Code | Referensi | Data Eksperimen | Bab | Status |
|---|---|---|---|---|---|---|
| CM-001 | AKSARA adalah aplikasi chat P2P terminal terenkripsi, serverless, dua pihak, tanpa server perantara | CB-001 | — | — | BAB I §1.1 | DOCUMENTED_ONLY |
| CM-002 | AKSARA didistribusikan untuk Windows, Linux, macOS Apple Silicon | CB-002 | — | — | BAB I §1.1, BAB III §3.4 | DOCUMENTED_ONLY |
| CM-003 | AKSARA dibangun Rust edition 2021, `rust-version` 1.89 | CB-003 | — | — | BAB III §3.2 | IMPLEMENTED |
| CM-004 | Arsitektur AKSARA terdiri 4 lapisan berkaitan: vault → identity/fingerprint → handshake → transport | `06_PROTOCOL_SPECIFICATION.md` §1-2 | — | — | BAB IV §4.1 | IMPLEMENTED |
| CM-005 | Role (Initiator/Responder) ditentukan dinamis dari perbandingan fingerprint (`role_from_fp`), bukan konfigurasi statis client/server | `transport/mod.rs:101-107` | — | — | BAB IV §4.1 | IMPLEMENTED |
| CM-006 | Strategi transport LAN-first dengan fallback Tor kondisional | `transport/mod.rs:118-172` | — | — | BAB IV §4.1, §4.3 | IMPLEMENTED |
| CM-007 | Versi implementasi terdokumentasi v0.2.1, commit `450d484`, `cargo build --release` bersih (0 warning/error) | `PROJECT_MEMORY.md` §Status Stabil | — | — | BAB III §3.2 | DOCUMENTED_ONLY (jangan diklaim "baru diverifikasi" tanpa rerun) |

---

## 2. CORE-1 — Noise_IK

| Claim ID | Klaim | Evidence Code | Referensi | Data Eksperimen | Bab | Status |
|---|---|---|---|---|---|---|
| CM-010 | AKSARA memakai pola `Noise_IK_25519_ChaChaPoly_BLAKE2s` via crate `snow` 0.10.0 | CR-007, CR-008, CR-009, CR-010, CR-011 | `noise2018`, `snowcrate` | — | BAB II §2.9, BAB IV §4.4, §4.6 | IMPLEMENTED (orkestrasi HIGH) |
| CM-011 | Handshake berlangsung 2 pesan: `-> e, es, s, ss` lalu `<- e, ee, se` | `crypto/handshake.rs:109-129` | `noise2018` | EXP-02 (`handshake_ik_roundtrip`) | BAB IV §4.4 | IMPLEMENTED (HIGH — diverifikasi test+kode) |
| CM-012 | Initiator wajib sudah tahu `peer_noise_pk` sebelum handshake — bila `None`, `run_session` gagal sebelum handshake dimulai | `session/mod.rs:119` (CR-027) | `noise2018` | EXP-02 | BAB IV §4.4 | IMPLEMENTED (HIGH) |
| CM-013 | Responder fail-closed pada ketidakcocokan static key untuk kontak **dikenal** (`Err(IdentityMismatch)`) | `session/mod.rs:145-151` (CR-027), test `responder_rejects_unknown_peer` | — | EXP-02 | BAB IV §4.4, §4.7 (T1) | IMPLEMENTED (HIGH) |
| CM-014 | **Tidak ada** pengecekan identitas sama sekali untuk kontak **belum dikenal** (`peer_noise_pk=None`) — trust-on-first-use implisit | `session/mod.rs:145-151` | — | — | BAB IV §4.4, §4.7 (T1) | IMPLEMENTED (HIGH untuk ketiadaannya); interpretasi "disengaja" = NEEDS_CONFIRMATION |
| CM-015 | Sub-mekanisme internal Noise (transcript hash `mix_hash`, HKDF `mix_key`, berbasis BLAKE2s) — murni inferensi nama pattern, tidak ada pemanggilan langsung di source aplikasi | CR-009, CR-010 | `noise2018` (properti umum) | — | BAB II §2.9, BAB IV §4.4, §4.6 | NEEDS_CONFIRMATION (LOW confidence) |
| CM-016 | Mutual authentication kedua static key di akhir handshake — hanya sisi Responder yang diuji memanggil `remote_static()`; tidak ada test yang memanggil di sisi Initiator | `crypto/handshake.rs:174-191` (CB-045) | `noise2018` | — | BAB IV §4.4 | PARTIAL (MEDIUM) |
| CM-017 | Forward secrecy (ephemeral key per sesi) — properti umum Noise_IK, **tidak diverifikasi** test AKSARA sendiri | `crypto/handshake.rs:14-17` (CB-046) | `noise2018` | — | BAB II §2.8, BAB IV §4.4 | DOCUMENTED_ONLY — **jangan overclaim "terverifikasi"** |
| CM-018 | Kerahasiaan static key Initiator terhadap penyadap pasif — properti umum pola `IK`, tidak diverifikasi test AKSARA | `crypto/handshake.rs:14-17` | `noise2018` | — | BAB IV §4.4 | DOCUMENTED_ONLY |
| CM-019 | Autentikasi implisit via kegagalan DH (`es`) saat peer key salah — dikonfirmasi test `wrong_peer_key_fails_handshake` | `crypto/handshake.rs:193-217` (CB-044) | — | EXP-02 | BAB IV §4.4 | IMPLEMENTED (CONFIRMED, dengan catatan presisi: mengautentikasi initiator menghubungi responder yang benar, bukan static key initiator) |
| CM-020 | Payload handshake 0-RTT (data aplikasi bersamaan pesan handshake) **tidak diuji** — seluruh test memakai payload kosong | `crypto/handshake.rs:115-122,210` (CB-059) | — | — | BAB IV §4.4 | NOT_FOUND (tidak diuji) |
| CM-021 | Crate `snow` **belum diaudit keamanan formal** (self-declared dokumentasi resmi) | Dokumentasi resmi `snow` | `snowcrate` | — | BAB II §2.9, BAB IV §4.6 | DOCUMENTED_ONLY |

---

## 3. CORE-2 — X25519

| Claim ID | Klaim | Evidence Code | Referensi | Data Eksperimen | Bab | Status |
|---|---|---|---|---|---|---|
| CM-030 | X25519 dipakai sebagai static+ephemeral key dalam 4 token DH (`es, ss, ee, se`) pola `IK` | CR-007, CR-016, CR-022, CR-032 | `rfc7748`, `bernstein2006curve25519` | EXP-02 (key agreement consistency) | BAB II §2.4, BAB IV §4.6 | IMPLEMENTED (HIGH keygen, MEDIUM DH internal `snow`) |
| CM-031 | Operasi DH aktual terjadi sepenuhnya internal `snow`, tidak dapat diverifikasi langsung dari source aplikasi | `crypto/handshake.rs:21-47` (CR-007) | — | — | BAB IV §4.6 | NEEDS_CONFIRMATION (MEDIUM) |
| CM-032 | Tidak ada pengecekan eksplisit public key peer all-zero/low-order point di `handshake.rs` — kepercayaan penuh pada `snow`+`x25519-dalek` | `crypto/handshake.rs` (audit TAHAP 2) | — | — | BAB IV §4.4, §4.7 | NOT_FOUND |

---

## 4. CORE-3 — ChaCha20-Poly1305 (3 Konteks)

| Claim ID | Klaim | Evidence Code | Referensi | Data Eksperimen | Bab | Status |
|---|---|---|---|---|---|---|
| CM-040 | ChaCha20-Poly1305 dipakai konsisten pada 3 konteks: vault (CR-013), contact store (CR-001), transport Noise (CR-008) | CR-001, CR-008, CR-013, CR-018 | `rfc8439`, `bernstein2008chacha`, `bernstein2005poly1305` | EXP-01, EXP-03, EXP-04 | BAB II §2.2, BAB IV §4.2, §4.5, §4.6 | IMPLEMENTED (HIGH vault/contact store, MEDIUM transport) |
| CM-041 | ChaCha20-Poly1305 **TIDAK misuse-resistant** — nonce reuse pada kunci sama katastropik | `04_CRYPTOGRAPHIC_JUSTIFICATION.md` CORE-3 poin 10 | `rfc8439` | — | BAB II §2.2, BAB IV §4.6, §4.7 (T-terkait) | DOCUMENTED_ONLY (properti algoritma, bukan bug ditemukan) |
| CM-042 | Nonce dibangkitkan RANDOM 96-bit per operasi (bukan counter) pada vault dan contact store | CR-004, CR-018 | `rfc8439` | EXP-01 (`vault_looks_random`) | BAB II §2.7, BAB IV §4.2 | IMPLEMENTED (HIGH) |
| CM-043 | Manajemen nonce pada transport Noise sepenuhnya internal `snow`, tidak dapat diverifikasi dari source aplikasi | `crypto/handshake.rs:21-98` (CR-008) | — | — | BAB IV §4.5, §4.6 | NEEDS_CONFIRMATION (MEDIUM) |
| CM-044 | **Tidak ada AAD** dipakai pada ketiga konteks — ciphertext tidak terikat konteks eksternal | CR-001, CR-013 | `rfc8439` | — | BAB II §2.2, BAB IV §4.6 | IMPLEMENTED (HIGH, temuan keterbatasan desain) |
| CM-045 | Overhead ciphertext +16 byte (tag Poly1305) per pesan/blok terenkripsi | `06_PROTOCOL_SPECIFICATION.md` §6.4 (spesifikasi) | `rfc8439` | EXP-03, EXP-05 (verifikasi ulang aktual) | BAB IV §4.5 | DOCUMENTED_ONLY sampai EXP-03/05 dijalankan — **NEEDS_EXPERIMENT** untuk angka terverifikasi |
| CM-046 | Algoritma AEAD transport sesi **diasumsikan** ChaCha20-Poly1305 (default `snow`), TIDAK disebut literal di `session/mod.rs` | `session/mod.rs:212,233` | — | — | BAB IV §4.5 | NEEDS_CONFIRMATION (MEDIUM, jangan dinyatakan "dikonfirmasi") |

---

## 5. CORE-4 — BLAKE2s

| Claim ID | Klaim | Evidence Code | Referensi | Data Eksperimen | Bab | Status |
|---|---|---|---|---|---|---|
| CM-050 | BLAKE2s dipakai 3 peran: fingerprint identitas (CR-002), KDF ad hoc contacts-key (CR-003), hash internal Noise (CR-009/010) | CR-002, CR-003, CR-009, CR-010 | `rfc7693`, `aumasson2013blake2` | EXP-04 (fingerprint binding) | BAB II §2.3, BAB IV §4.6 | IMPLEMENTED (HIGH fingerprint/KDF, LOW peran internal Noise) |
| CM-051 | Fingerprint mengikat KEDUA public key (Ed25519+X25519) sekaligus, mencegah serangan invite susun-ulang | `contacts/mod.rs:39-54` (CR-002), test `fingerprint_binds_both_keys` | `rfc7693` | EXP-04 | BAB II §2.3, BAB IV §4.3 | IMPLEMENTED (HIGH) |
| CM-052 | Domain-separation via context string berbeda (`aksara-fingerprint-v1` vs `aksara-contacts-key-v1`) mencegah cross-protocol attack | CR-002, CR-003 | `rfc7693` | — | BAB IV §4.6 | IMPLEMENTED (HIGH) |
| CM-053 | Pemakaian BLAKE2s sebagai KDF contacts-key adalah hash single-shot, BUKAN konstruksi HKDF standar | CR-003 | `rfc7693` | EXP-04 (KDF consistency) | BAB II §2.5, BAB IV §4.6 | IMPLEMENTED (MEDIUM, keterbatasan desain diterima) |

---

## 6. CORE-5 — Argon2id

| Claim ID | Klaim | Evidence Code | Referensi | Data Eksperimen | Bab | Status |
|---|---|---|---|---|---|---|
| CM-060 | Argon2id dipakai satu-satunya password-based KDF, parameter `m=19 MiB, t=2, p=1`, output 32 byte, dipakai langsung sebagai kunci AEAD vault | CR-014 | `rfc9106`, `biryukov2016argon2` | EXP-01, EXP-05 | BAB II §2.5, BAB IV §4.2, §4.6 | IMPLEMENTED (HIGH parameter, jelas dari kode) |
| CM-061 | Klaim komentar kode "~100ms pada hardware modern" **TERKOREKSI** oleh EXP-05 (2026-07-27): terukur ~48 ms neto (median 45,08 ms, n=30) pada hardware uji | `identity/vault.rs:33-38` (CB-087) | `rfc9106` | **EXP-05 (EXECUTED — `EXPERIMENT_RESULTS_2026-07-27.csv`)** | BAB II §2.5, BAB IV §4.2, BAB V §5.3 | CORRECTED — **jangan kutip "~100ms" sebagai fakta; kutip angka terukur dan selalu sertakan lingkungan ujinya** |
| CM-062 | Output Argon2id dipakai LANGSUNG sebagai kunci AEAD tanpa HKDF perantara | CR-014 | `rfc9106` | — | BAB IV §4.2, §4.6 | IMPLEMENTED (dinilai dapat diterima untuk kasus tunggal saat ini) |

---

## 7. CORE-6 — Ed25519 (Identitas)

| Claim ID | Klaim | Evidence Code | Referensi | Data Eksperimen | Bab | Status |
|---|---|---|---|---|---|---|
| CM-070 | Ed25519 dipakai untuk identity keypair jangka panjang — HANYA generate/simpan/ekspor byte | CR-015 | `rfc8032`, `bernstein2012ed25519`, `fips186-5` | EXP-04 (fingerprint yang memakai public key) | BAB II §2.6, BAB IV §4.6 | PARTIAL (keygen HIGH) |
| CM-071 | **TIDAK ADA** pemanggilan `sign()`/`verify()`/`Signature` di manapun dalam source yang diaudit (grep menyeluruh nihil) | CB-084 | — | — | BAB II §2.6, BAB IV §4.6 | NOT_FOUND (HIGH confidence untuk ketiadaannya) — **KLAIM KRITIS, wajib ditegaskan ulang di setiap bagian yang membahas Ed25519** |
| CM-072 | Ed25519 dan X25519 sengaja dipisah menjadi 2 keypair berbeda meski berbagi kurva dasar (hindari cross-purpose key reuse) | `identity/keypair.rs` (CB-062) | `rfc8032`, `rfc7748` | — | BAB IV §4.6 | IMPLEMENTED (HIGH) |

---

## 8. CORE-7 — OsRng

| Claim ID | Klaim | Evidence Code | Referensi | Data Eksperimen | Bab | Status |
|---|---|---|---|---|---|---|
| CM-080 | `OsRng` dipakai seragam di 4 titik: keygen Ed25519, keygen X25519, salt Argon2id, nonce ChaCha20Poly1305 | CR-004, CR-012, CR-017, CR-023, CR-036 | `sp800-90a` | — | BAB II, BAB IV §4.2, §4.6 | IMPLEMENTED (HIGH) |
| CM-081 | Kebenaran implementasi CSPRNG level-OS yang mendasari `OsRng` **tidak dinilai** — di luar cakupan audit AKSARA | — | `sp800-90a` (konteks) | — | BAB I §1.5 (batasan), BAB IV §4.6 | Batasan eksplisit, bukan klaim IMPLEMENTED/NOT_FOUND |

---

## 9. Invite Code, Discovery, dan Pembentukan Koneksi

| Claim ID | Klaim | Evidence Code | Referensi | Data Eksperimen | Bab | Status |
|---|---|---|---|---|---|---|
| CM-090 | Invite code = `base64url_no_pad(ed25519_pub[32] \|\| noise_pub[32])`, opsional suffix `@<onion>` | `contacts/mod.rs:56-68` (CR-005) | — | EXP-04 (invite roundtrip, panjang string) | BAB IV §4.3 | IMPLEMENTED (HIGH) |
| CM-091 | Invite code **TIDAK ditandatangani/diautentikasi secara kriptografis** — dinyatakan eksplisit di komentar kode | `contacts/mod.rs:42-47` (CR-005) | — | — | BAB IV §4.3, §4.7 (T3) | IMPLEMENTED (HIGH, keterbatasan desain diakui) |
| CM-092 | Discovery LAN via mDNS mengiklankan HANYA fingerprint Ed25519 hex (bukan X25519 Noise key) | `transport/lan.rs:1-21,9-11` (CR-029) | `rfc6762`, `rfc6763` | — | BAB IV §4.3, §4.7 (T2) | IMPLEMENTED (HIGH) |
| CM-093 | Perbandingan fingerprint (`role_from_fp`) memakai operator `<` bawaan `&str` — non-constant-time, risiko dinilai rendah karena data publik | `transport/mod.rs:101-107` (CR-029) | — | — | BAB IV §4.1, §4.3 | IMPLEMENTED (HIGH untuk fakta non-constant-time) |
| CM-094 | Strategi LAN-first: timeout 3 detik hanya pada mode `Auto` DAN Tor tersedia; LAN-only tanpa batas waktu | `transport/mod.rs:118-155` | — | — | BAB IV §4.3 | IMPLEMENTED (HIGH) |
| CM-095 | Jalur Tor: retry dial `TOR_DIAL_RETRY_DELAY=8 detik` sampai `TOR_DIAL_TOTAL_TIMEOUT=120 detik`; bootstrap tanpa timeout eksplisit | `transport/mod.rs:109-116,174-197`, `transport/tor.rs:9-60` | — | — | BAB IV §4.3, §4.7 (Tor availability risk) | IMPLEMENTED (HIGH) |

---

## 10. Transport Sesi Terenkripsi

| Claim ID | Klaim | Evidence Code | Referensi | Data Eksperimen | Bab | Status |
|---|---|---|---|---|---|---|
| CM-100 | Payload plaintext memakai tag 1-byte: `TYPE_TEXT(0x00)`, `TYPE_BLUR(0x01)`, `TYPE_PING(0x02)` | `session/mod.rs:36-41` | — | EXP-03 | BAB IV §4.5 | IMPLEMENTED (HIGH) |
| CM-101 | Batas pesan 65535 byte (`MAX_FRAME_LEN`); pesan oversize ditangani NON-FATAL (`Notice`, sesi tetap hidup) | `transport/frame.rs:16`, `session/mod.rs:212-224`, test `oversized_message_does_not_kill_session` | — | EXP-03 | BAB IV §4.5 | IMPLEMENTED (HIGH) |
| CM-102 | Kegagalan dekripsi frame masuk FATAL — loop `break` segera, fail-closed eksplisit | `session/mod.rs:253-268` | — | EXP-03 (belum ada test rejection ciphertext dimodifikasi, lihat keterbatasan `12_TEST_PLAN.md` EXP-03 poin 15) | BAB IV §4.5, §4.7 (T5) | IMPLEMENTED (HIGH, tapi belum diuji langsung dengan ciphertext dimodifikasi sengaja) |
| CM-103 | UI TIDAK dapat membedakan penutupan sesi akibat kegagalan dekripsi (potensi tampering) vs penutupan normal lainnya | `session/mod.rs:246-249,253-268` | — | — | BAB IV §4.5, §4.7 (T5) | IMPLEMENTED (HIGH) |
| CM-104 | `read_frame` TIDAK cancel-safe — dimitigasi via task pembaca terpisah; risiko regresi bila dikembalikan ke dalam `tokio::select!` | `transport/frame.rs:97-104`, `session/mod.rs:166-190`, test `read_frame_yang_dibatalkan_merusak_sinkronisasi_stream` | — | — | BAB IV §4.5 | IMPLEMENTED (HIGH) — **catatan lintas-sesi**: jangan pernah kembalikan `read_frame` ke dalam `select!` |
| CM-105 | Deteksi koneksi mati sepenuhnya bergantung kegagalan `write_frame`, BUKAN ping tak terbalas | `session/mod.rs:54-58` | — | — | BAB IV §4.5 | IMPLEMENTED (HIGH, keterbatasan M1 disengaja) |

---

## 11. Key Lifecycle — Rotasi, Revokasi, Zeroization

| Claim ID | Klaim | Evidence Code | Referensi | Data Eksperimen | Bab | Status |
|---|---|---|---|---|---|---|
| CM-110 | Vault layout fixed-offset 108 byte, TANPA header/magic/versi (disengaja, "SEC-05") | `identity/vault.rs:1-31` (CR-019) | — | EXP-05 (verifikasi ukuran) | BAB IV §4.2, §4.6 (TBL-07) | IMPLEMENTED (HIGH) |
| CM-111 | Setiap `seal()` menurunkan kunci baru dari salt acak baru — kunci vault berbeda tiap re-seal walau passphrase sama | `identity/vault.rs:169-177` (test `vault_looks_random`) | — | EXP-01 | BAB IV §4.2 | IMPLEMENTED (HIGH) |
| CM-112 | Ambiguitas `Error::Decryption` (passphrase salah/vault korup/ukuran salah → pesan sama) DISENGAJA — mitigasi oracle attack | `identity/vault.rs:96-97`, `error.rs:1-14` | — | EXP-01 | BAB IV §4.2, §4.7 | IMPLEMENTED (HIGH) |
| CM-113 | **TIDAK DITEMUKAN mekanisme rotasi** untuk kunci manapun (vault, identity, Noise, session) | CB-083, `07_KEY_LIFECYCLE.md` §6 | — | — | BAB II §2.8, BAB IV §4.2, §4.7 (T7) | NOT_FOUND (HIGH untuk ketiadaannya) |
| CM-114 | **TIDAK DITEMUKAN mekanisme revokasi** kontak/kunci in-band | `07_KEY_LIFECYCLE.md` §6 | — | — | BAB IV §4.2, §4.7 (T7) | NOT_FOUND (HIGH) |
| CM-115 | `ZeroizeOnDrop`/`Zeroizing` diterapkan KONSISTEN pada tipe kunci inti (`IdentityKey`, `NoiseKey`, `KeyBundle`, buffer vault) | `identity/keypair.rs:10,44,74-89`, `identity/vault.rs:49-56,62,108` | — | — | BAB IV §4.2, §4.6 (TBL-08) | IMPLEMENTED (HIGH) |
| CM-116 | Zeroization **TIDAK konsisten** di 5 boundary: `session::run_session`, `crypto::handshake`, `contacts::mod`, `main.rs` (2 titik) | `07_KEY_LIFECYCLE.md` §7.2 | — | — | BAB IV §4.2, §4.7 | PARTIAL (HIGH untuk fakta kesenjangan) |
| CM-117 | Passphrase interaktif stdin MASIH TER-ECHO ke layar; input tersembunyi `PLANNED` M4, belum diimplementasikan | `main.rs:153-154` | — | — | BAB IV §4.2, §4.7 | PLANNED |

---

## 12. Threat Model — Risk Register T1-T7

| Claim ID | Klaim | Evidence Code | Referensi | Data Eksperimen | Bab | Status |
|---|---|---|---|---|---|---|
| CM-120 | T1 — Tidak ada pengecekan identitas pada koneksi pertama ke kontak belum dikenal (Sedang/Tinggi) | `08_THREAT_MODEL.md` §6 = CM-014 | — | EXP-02 (perilaku observable) | BAB IV §4.7 (TBL-09) | IMPLEMENTED (temuan HIGH confidence, deskriptif) |
| CM-121 | T2 — Kebocoran metadata presence/fingerprint di LAN via mDNS (Tinggi/Rendah-Sedang) | `08_THREAT_MODEL.md` §6 = CM-092 | `rfc6762`, `rfc6763` | — | BAB IV §4.7 | IMPLEMENTED |
| CM-122 | T3 — Invite code tidak diautentikasi kriptografis (Sedang/Tinggi) | `08_THREAT_MODEL.md` §6 = CM-091 | — | EXP-04 | BAB IV §4.7 | IMPLEMENTED |
| CM-123 | T4 — Tidak ada file-permission hardening pada vault/state Tor (Rendah-Sedang/Sedang-Tinggi) | `identity/vault.rs:132-142` (CB-074) | — | — | BAB IV §4.7 | NOT_FOUND |
| CM-124 | T5 — UI tidak membedakan penutupan sesi akibat tampering vs normal (Rendah/Rendah) | `08_THREAT_MODEL.md` §6 = CM-103 | — | — | BAB IV §4.7 | IMPLEMENTED |
| CM-125 | T6 — `FS_MISTRUST_DISABLE_PERMISSIONS_CHECKS` aktif tanpa syarat platform apa pun (Rendah-Sedang/Sedang) | `main.rs:216-219` | — | — | BAB IV §4.7 | IMPLEMENTED (HIGH — dikonfirmasi tidak ada `cfg(windows)` di seluruh `main.rs`) |
| CM-126 | T7 — Tidak ada mekanisme rotasi/revokasi kunci apa pun (N/A struktural/Tinggi jangka panjang) | `08_THREAT_MODEL.md` §6 = CM-113/CM-114 | — | — | BAB IV §4.7, BAB II §2.8 | NOT_FOUND |

---

## 13. Related Work — Gap G1-G5

| Claim ID | Klaim | Evidence Code | Referensi | Data Eksperimen | Bab | Status |
|---|---|---|---|---|---|---|
| CM-130 | G1 — Tidak ada verifikasi formal terhadap instansiasi Noise_IK spesifik AKSARA | `10_RELATED_WORK_AND_GAP.md` §3 | `kobeissi2019noiseexplorer`, `noise2018` | — (evaluatif, di luar cakupan tool eksternal sesi ini) | BAB II §2.10 | NOT_FOUND (untuk ketiadaan verifikasi formal AKSARA) |
| CM-131 | G2 — Tidak ada rotasi/ratcheting kunci sesi (kontras Signal Double Ratchet, Matrix Megolm) | `10_RELATED_WORK_AND_GAP.md` §3 = CM-113 | `cohngordon2020signal`, `albrecht2024matrix` | — | BAB II §2.10 | NOT_FOUND |
| CM-132 | G3 — Belum ada evaluasi overhead protokol pada konteks LAN/Tor AKSARA | `10_RELATED_WORK_AND_GAP.md` §3 | `donenfeld2017wireguard` | **EXP-05 (WAITING_FOR_EXPERIMENT)** | BAB II §2.10 | NEEDS_EXPERIMENT |
| CM-133 | G4 — Invite code AKSARA tidak punya handshake kontak terstruktur seperti Briar (BHP) | `10_RELATED_WORK_AND_GAP.md` §3 = CM-091 | `briarspec` | — | BAB II §2.10 | IMPLEMENTED (untuk fakta ketiadaan struktur serupa) |
| CM-134 | G5 — Tidak ada fallback offline (Bluetooth/Wi-Fi/USB) dibanding Briar — perbedaan cakupan fitur, bukan gap keamanan | `10_RELATED_WORK_AND_GAP.md` §3 | `briarspec` | — | BAB II §2.10 | NOT_FOUND (deskriptif, bukan kekurangan) |

---

## 14. Kebutuhan Fungsional/Non-Fungsional (Cross-Cutting)

| Claim ID | Klaim | Evidence Code | Referensi | Data Eksperimen | Bab | Status |
|---|---|---|---|---|---|---|
| CM-140 | 12 kebutuhan fungsional (FR-01..12) — seluruhnya `IMPLEMENTED`, evidence per FR di TBL-01 | `tables/01_functional_requirements.md` | — | — | BAB III, BAB IV | IMPLEMENTED |
| CM-141 | NFR-03 (autentikasi) berstatus PARTIAL — HIGH untuk kontak dikenal, TIDAK ADA untuk kontak baru | `tables/02_nonfunctional_requirements.md` = CM-013/CM-014 | — | EXP-02 | BAB III, BAB IV §4.7 | PARTIAL |
| CM-142 | NFR-09 (ketiadaan rotasi kunci) berstatus NOT_FOUND — keterbatasan desain M1 disengaja, bukan bug | `tables/02_nonfunctional_requirements.md` = CM-113 | — | — | BAB III, BAB IV §4.7 | NOT_FOUND |

---

## 15. Klaim Performa (Diperbarui 2026-07-27 — 4 dari 5 Sudah Terukur)

Aturan "klaim performa didukung eksperimen" tetap berlaku. Empat baris di bawah kini **sudah punya data nyata** (`EXPERIMENT_RESULTS_2026-07-27.csv`, commit `75d17fd`); satu baris tetap belum diukur. Seluruh angka **wajib** ditulis bersama n, sebaran, dan spesifikasi hardware uji — tidak boleh digeneralisasi.

| Claim ID | Klaim | Evidence Code | Referensi | Data Eksperimen | Bab | Status |
|---|---|---|---|---|---|---|
| CM-150 | Waktu unlock vault (Argon2id) pada hardware uji = mean 47,99 ms neto / 68,47 ms end-to-end (n=30, sd 11,41/12,47 ms) | CB-087 = CM-061 | `rfc9106` | EXP-05 (EXECUTED) | BAB V §5.2, §5.3 | MEASURED — berlaku hanya untuk lingkungan di BAB V §5.1 |
| CM-151 | Latensi handshake Noise_IK end-to-end **tidak terdeteksi di atas noise** metode eksternal; batas atas < 0,86 ms (95% CI, n=19) | — | `noise2018` | EXP-02 (EXECUTED, parsial) | BAB V §5.2, §5.3 | PARTIAL — batas atas, **bukan nilai titik**; presisi butuh instrumentasi source |
| CM-152 | Overhead tag AEAD = tepat 16 byte, terukur pada instance vault (108 − 16 salt − 12 nonce − 64 plaintext) | `identity/vault.rs` konstanta layout | `rfc8439` | EXP-03 (EXECUTED, parsial) | BAB V §5.2 | PARTIAL — instance **vault** terukur; instance Noise transport tetap `NEEDS_EXPERIMENT` |
| CM-153 | Proporsi correctness/rejection: 46/46 unit test lolos; 10/10 unseal CLI sukses dan deterministik; 100% rejection passphrase salah | — | — | EXP-01..04 (EXECUTED) | BAB V §5.2 | MEASURED |
| CM-154 | Memory usage puncak (RSS) saat Argon2id berjalan | — | — | EXP-05 (opsional/sekunder) | BAB V §5.3 (dicatat sebagai keterbatasan) | WAITING_FOR_EXPERIMENT (opsional) — hanya parameter statis 19 MiB yang diketahui |
| CM-155 | Ukuran vault = tepat 108 byte, terverifikasi 5 vault independen | `identity/vault.rs` `VAULT_SIZE` | — | EXP-05 (EXECUTED) | BAB V §5.2 | MEASURED |
| CM-156 | Panjang invite LAN-only = 86 karakter, konsisten pada 5 keypair acak | `contacts/mod.rs` `encode_invite` | — | EXP-04 (EXECUTED) | BAB V §5.2 | MEASURED |

---

## Ringkasan Rekapitulasi

| Kategori | Jumlah Claim ID | Rentang |
|---|---|---|
| Identitas & arsitektur umum | 7 | CM-001..007 |
| CORE-1 Noise_IK | 12 | CM-010..021 |
| CORE-2 X25519 | 3 | CM-030..032 |
| CORE-3 ChaCha20-Poly1305 | 7 | CM-040..046 |
| CORE-4 BLAKE2s | 4 | CM-050..053 |
| CORE-5 Argon2id | 3 | CM-060..062 |
| CORE-6 Ed25519 | 3 | CM-070..072 |
| CORE-7 OsRng | 2 | CM-080..081 |
| Invite/discovery/koneksi | 6 | CM-090..095 |
| Transport sesi | 6 | CM-100..105 |
| Key lifecycle (rotasi/revokasi/zeroization) | 8 | CM-110..117 |
| Threat model T1-T7 | 7 | CM-120..126 |
| Related work gap G1-G5 | 5 | CM-130..134 |
| FR/NFR cross-cutting | 3 | CM-140..142 |
| Klaim performa | 7 | CM-150..156 |
| **Total** | **83** | CM-001..156 (non-kontinu per kategori) |

**Distribusi status**: mayoritas `IMPLEMENTED`/`NOT_FOUND` dengan evidence HIGH confidence (audit source-level langsung); sejumlah kecil `DOCUMENTED_ONLY`/`NEEDS_CONFIRMATION`/LOW-MEDIUM confidence yang **wajib dipertahankan hedge-nya** (terutama CM-015, CM-017, CM-018 — larangan overclaim eksplisit). Klaim performa **diperbarui 2026-07-27**: 4 `MEASURED` (CM-150, CM-153, CM-155, CM-156), 2 `PARTIAL` (CM-151 batas atas, CM-152 hanya instance vault), 1 tetap `WAITING_FOR_EXPERIMENT` (CM-154 RSS). CM-061 berubah dari `DOCUMENTED_ONLY` menjadi `CORRECTED`. Dua Claim ID baru (CM-155, CM-156) ditambahkan untuk metrik deterministik yang kini terverifikasi empiris — total naik dari 81 menjadi 83.

## Klaim Kritis Anti-Overclaim (Prioritas Tertinggi)

Daftar ini mengulang (bukan menduplikasi baru) klaim yang paling berisiko di-overclaim Codex saat menulis prosa BAB — WAJIB dicek ulang sebelum finalisasi dokumen:

1. **CM-071** — Ed25519 TIDAK dipakai sign/verify aktif. Jangan pernah menulis "AKSARA menggunakan tanda tangan digital Ed25519".
2. **CM-017/CM-018** — Forward secrecy dan kerahasiaan static-key initiator `DOCUMENTED_ONLY`. Jangan menulis "AKSARA terbukti memiliki forward secrecy".
3. **CM-061** — Klaim "~100ms" Argon2id sudah diuji (EXP-05, 2026-07-27) dan **TERKOREKSI menjadi ~48 ms neto** pada hardware uji. Jangan mengutip "~100ms" sebagai fakta; kutip angka terukur, selalu bersama n, sebaran, dan spesifikasi hardware — dan jangan generalisasi ke hardware lain.
4. **CM-041/CM-044** — ChaCha20-Poly1305 TIDAK misuse-resistant dan TIDAK memakai AAD. Jangan menulis "AKSARA melindungi terhadap nonce reuse" tanpa hedge.
5. **CM-014** — Trust-on-first-use pada kontak baru. Jangan menulis "AKSARA selalu memverifikasi identitas peer" tanpa kualifikasi "untuk kontak yang sudah dikenal".

## Referensi

Seluruh evidence code (`CB-xxx`, `CR-xxx`, `T1-T7`, `G1-G5`) merujuk `01_CODEBASE_AUDIT.md`, `02_CRYPTO_IMPLEMENTATION_AUDIT.md`, `08_THREAT_MODEL.md`, `10_RELATED_WORK_AND_GAP.md` (TAHAP 2/3/7/10). Seluruh citekey merujuk `references/REFERENCES.bib` (40 entry, tidak ada penambahan baru pada TAHAP 16).
