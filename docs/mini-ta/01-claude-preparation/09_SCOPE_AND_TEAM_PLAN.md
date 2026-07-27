# 09 — Scope dan Pembagian Tim Mini-TA AKSARA

Dokumen ini menentukan scope mini-TA kelompok (Tugas Akhir Mata Kuliah Implementasi Kriptografi, 3 anggota) berdasarkan implementasi AKSARA **sebagaimana sudah diaudit** pada TAHAP 1-7 (`01_CODEBASE_AUDIT.md`, `02_CRYPTO_IMPLEMENTATION_AUDIT.md`, `03_CRYPTO_INVENTORY_NORMALIZED.md`, `04_CRYPTOGRAPHIC_JUSTIFICATION.md`, `05_CRYPTO_ALTERNATIVE_COMPARISON.md`, `06_PROTOCOL_SPECIFICATION.md`, `07_KEY_LIFECYCLE.md`, `08_THREAT_MODEL.md`). Tidak ada scope baru yang diusulkan di sini — dokumen ini **memilih dan membingkai** dari apa yang sudah terbukti terimplementasi, bukan merancang fitur baru.

**Diperbarui 2026-07-27**: identitas anggota kini **CONFIRMED** — Andika Aryansyach Fauzan (2322101878), Mahendra Nur Hidayat (2322101937), Rafi Putra Fadlurrahman (2322101963), program studi Rekayasa Sistem Kriptografi, Politeknik Siber dan Sandi Negara. Sumber: `docs/mini-ta/00-template/PROPOSAL CARAKA (2).docx` (mata kuliah dan kelompok yang sama), ditunjuk langsung oleh pengguna. Catatan SESSION 2 yang menyatakan "tidak ada nama asli yang dapat diverifikasi" sudah tidak berlaku. Label **Anggota 1/2/3** di §8 dipertahankan sebagai penanda peran; pemetaan nama ke peran memakai urutan pada proposal dan **boleh ditukar** kelompok.

---

## 1. Fokus Utama

**Implementasi dan evaluasi protokol keamanan end-to-end AKSARA**: pembentukan kanal aman dua-pihak via handshake Noise_IK (`Noise_IK_25519_ChaChaPoly_BLAKE2s`, CORE-1), bertumpu pada siklus hidup kunci kriptografi yang melindunginya (identity key Ed25519, Noise key X25519, vault Argon2id+ChaCha20-Poly1305), dievaluasi terhadap threat model yang proporsional untuk tugas mata kuliah.

Ini **satu rangkaian protokol yang saling berkaitan** (bukan kumpulan primitif lepas), memenuhi ketentuan `CLAUDE_PREPARATION_BRIEF.md` §Batas Scope: vault (Argon2id+ChaCha20Poly1305) melindungi secret key jangka panjang yang dipakai sebagai static key Noise_IK; fingerprint BLAKE2s mengikat kedua public key (Ed25519+X25519) yang sama menjadi identitas dalam invite code; hasil akhirnya adalah sesi transport terenkripsi (ChaCha20-Poly1305, diasumsikan dari `snow`) yang membawa payload chat. Empat komponen ini (vault → identity/fingerprint → handshake → transport) adalah satu jalur data yang berurutan, bukan topik terpisah.

**Tidak termasuk fokus utama** (dibahas sebagai konteks/lapisan pendukung, bukan objek analisis kripto primer): transport LAN mDNS dan Tor onion service — keduanya adalah *carrier* di bawah lapisan Noise_IK, bukan mekanisme kriptografi AKSARA sendiri (lihat `06_PROTOCOL_SPECIFICATION.md` §1). TUI (`src/tui/`) dibahas hanya sejauh menjadi titik integrasi kripto (mis. alur invite/verifikasi fingerprint), bukan sebagai objek evaluasi UI/UX.

---

## 2. Rumusan Masalah (maks. 3)

1. Bagaimana AKSARA mengimplementasikan protokol Noise_IK (`snow` 0.10.0) untuk mencapai autentikasi identitas dan kerahasiaan sesi pada komunikasi P2P dua pihak, dan properti keamanan mana dari yang diklaim dokumentasi kode yang benar-benar dapat diverifikasi dari evidence source-level (bukan sekadar didokumentasikan)?
2. Bagaimana siklus hidup kunci kriptografi AKSARA (identity key Ed25519, Noise key X25519, vault key turunan Argon2id, contacts-store key turunan BLAKE2s) dikelola end-to-end — generation, storage, usage, dan zeroization — dan sejauh mana pengelolaan tersebut konsisten dengan praktik yang direkomendasikan standar terkait (RFC 9106, RFC 8439, dst.)?
3. Sejauh mana desain protokol dan manajemen kunci AKSARA memberikan ketahanan terhadap kelas ancaman yang relevan (penyadapan pasif, impersonasi, tampering pesan, kompromi penyimpanan lokal), dan apa batasan/celah residual yang teridentifikasi dari analisis source-level (mis. ketiadaan rotasi kunci, trust-on-first-use pada kontak baru)?

## 3. Tujuan (maks. 3, berkorespondensi 1:1 dengan rumusan masalah)

1. Mendokumentasikan dan menganalisis spesifikasi protokol Noise_IK AKSARA sebagai *as-built specification* — alur pesan, orkestrasi kode (`crypto/handshake.rs`, `session/mod.rs`), dan pemetaan eksplisit klaim `HIGH`/`MEDIUM`/`DOCUMENTED_ONLY` per properti keamanan.
2. Menganalisis siklus hidup seluruh material kunci AKSARA (generation seragam via `OsRng`, storage vault 108-byte, usage per konteks, ketiadaan rotasi/revokasi, kesenjangan zeroization di boundary fungsi) dan membandingkannya dengan rekomendasi standar yang relevan.
3. Menyusun threat model deskriptif AKSARA (trust boundary, aset, 5 model musuh A1-A5, ancaman per 7 komponen protokol, risk register T1-T7 kualitatif) dan merancang serta — sejauh waktu mengizinkan pada SESSION 5 — menjalankan pengujian correctness/security dasar pada primitif kripto kunci untuk memverifikasi sebagian klaim di atas secara empiris.

## 4. Kontribusi Utama (maks. 3)

1. **Spesifikasi protokol as-built** Noise_IK AKSARA berbasis evidence source-level (path+baris+ID evidence per klaim) — bukan proposal desain baru, melainkan dokumentasi presisi dari apa yang benar-benar berjalan di kode, termasuk kesenjangan antara klaim dokumentasi kode dan bukti test (mis. forward secrecy `DOCUMENTED_ONLY`, bukan `CONFIRMED`).
2. **Analisis siklus hidup dan zeroization kunci kriptografi end-to-end** pada implementasi Rust nyata (bukan skema teoretis) — memetakan secara eksplisit tipe kunci mana yang sudah dilindungi `ZeroizeOnDrop` dan boundary fungsi mana yang belum (`session::run_session`, `crypto::handshake`, `contacts::mod`, `main.rs`).
3. **Threat model deskriptif dan rencana pengujian primitif kriptografi** yang proporsional untuk tugas mata kuliah — risk register kualitatif berbasis kontrol yang sudah ada di kode (bukan rekomendasi remediasi baru di luar cakupan), dilengkapi rencana pengujian correctness (roundtrip, rejection test, KAT bila tersedia) untuk memverifikasi sebagian klaim keamanan secara empiris pada SESSION 5.

## 5. Batasan Penelitian (Limitations)

Diwarisi langsung dari batasan cakupan eksplisit `08_THREAT_MODEL.md` §5, ditambah batasan umum tugas mata kuliah:

1. **Tidak menilai keamanan internal dependency crate** (`snow`, `arti-client`/`tor-hsservice`, `mdns-sd`, `x25519-dalek`, `ed25519-dalek`) — analisis terbatas pada cara AKSARA memakainya, bukan audit kriptografi crate itu sendiri.
2. **Tidak menilai kebenaran implementasi CSPRNG level-OS** yang mendasari `OsRng` — didelegasikan penuh ke OS.
3. **Tidak melakukan pembuktian formal kriptografi** (mis. bukti keamanan berbasis game/simulasi) — analisis bersifat deskriptif berbasis evidence source-level dan referensi standar, sesuai proporsi tugas mata kuliah (bukan skripsi/publikasi).
4. **Tidak melakukan analisis side-channel fisik/hardware** (power analysis, emisi elektromagnetik, timing attack presisi-tinggi) — di luar cakupan scope software-level.
5. **Tidak mengevaluasi ketahanan denial-of-service** terhadap kondisi jaringan adversarial skala luas — tidak ada analisis rate-limiting kuantitatif.
6. **Tidak mencakup skenario multi-device/sinkronisasi kunci** — desain AKSARA saat ini adalah satu identitas per satu perangkat.
7. **Bukan proyek remediasi/redesign** — risk register T1-T7 dan kesenjangan zeroization dilaporkan **deskriptif** (apa yang ada di kode), bukan diimplementasikan ulang sebagai perbaikan dalam scope mini-TA ini, kecuali disepakati eksplisit sebagai kontribusi tambahan di luar 3 kontribusi utama di atas.
8. **Transport LAN (mDNS) dan Tor** dibahas sebagai konteks pendukung (lapisan defense-in-depth dan sumber kebocoran metadata di §4.2/§4.7 threat model), bukan sebagai objek evaluasi kriptografi primer — tidak ada analisis mendalam terhadap keamanan protokol Tor/mDNS itu sendiri.
9. **Klaim performa/timing (mis. "~100ms" Argon2id) tidak dikutip sebagai fakta terukur** kecuali diverifikasi lewat benchmark aktual pada TAHAP 13 (SESSION 5) — bila eksperimen tidak sempat dijalankan, klaim tetap ditandai `DOCUMENTED_ONLY`/`NEEDS_EXPERIMENT`.

## 6. Luaran (Outputs)

1. Dokumen Tugas Akhir Mata Kuliah Implementasi Kriptografi (BAB I-VI, format `docs/mini-ta/00-template/Cetak_TA_rev3.docx`, disusun Codex dari content pack TAHAP 15).
2. Spesifikasi protokol, key lifecycle, dan threat model as-built (`06_PROTOCOL_SPECIFICATION.md`, `07_KEY_LIFECYCLE.md`, `08_THREAT_MODEL.md` — sudah `DONE`).
3. Rencana pengujian dan (bila sempat dijalankan pada SESSION 5) data eksperimen dasar correctness/performance primitif kripto kunci (Argon2id, ChaCha20-Poly1305, Noise_IK handshake).
4. Diagram teknis (5-8 diagram Mermaid, TAHAP 11) dan screenshot aplikasi (2-4 gambar bila memungkinkan, TAHAP 12).
5. Daftar referensi terverifikasi (33 entry TAHAP 4/9/SESSION 3 + tambahan TAHAP 10 untuk related work) dan peta klaim-evidence-citation (TAHAP 16).
6. Handoff terstruktur untuk Codex (`HANDOFF_TO_CODEX.yaml`, TAHAP 17) — bukan dokumen DOCX itu sendiri.

## 7. Judul yang Dipertimbangkan

| # | Judul | Cakupan | Catatan |
|---|---|---|---|
| 1 | Implementasi dan Analisis Protokol Noise_IK untuk Autentikasi dan Kerahasiaan Sesi pada Aplikasi Chat P2P Terenkripsi AKSARA | Fokus sempit: hanya handshake+transport (§5-6 `06_PROTOCOL_SPECIFICATION.md`) | Tidak eksplisit mencakup key lifecycle/threat model — berisiko dibaca sebagai scope lebih sempit dari yang sudah dikerjakan TAHAP 5-7 |
| 2 | Analisis Siklus Hidup Kunci dan Protokol Keamanan pada Aplikasi Komunikasi Peer-to-Peer Berbasis Noise Protocol Framework: Studi Kasus AKSARA | Fokus seimbang: key lifecycle + protokol, "studi kasus" menegaskan sifat implementasi | Judul cukup panjang tapi akurat; "studi kasus" tepat untuk level tugas mata kuliah (bukan klaim novelty skripsi) |
| 3 | Implementasi dan Evaluasi Keamanan Protokol Noise_IK, Manajemen Kunci, dan Threat Model pada Aplikasi Chat Terminal P2P Serverless AKSARA | Cakupan penuh: 3 pilar TAHAP 5-7 sekaligus (protokol, key lifecycle, threat model) | Paling representatif terhadap fokus utama §1 di atas, tapi paling panjang dari ketiganya |

**Rekomendasi: Judul #3.** Alasan: (a) secara langsung merepresentasikan fokus utama §1 (satu rangkaian protokol: handshake + key lifecycle + threat model, bukan topik terpisah), sehingga tidak perlu "menyembunyikan" cakupan key lifecycle/threat model yang sudah dikerjakan penuh di TAHAP 5-7; (b) frasa "Implementasi dan Evaluasi Keamanan" (bukan "Desain" atau "Perancangan") jujur terhadap sifat pekerjaan — AKSARA sudah terimplementasi, tugas mini-TA adalah menganalisis dan mengevaluasi, bukan merancang dari nol; (c) "Aplikasi Chat Terminal P2P Serverless" secara akurat mendeskripsikan AKSARA tanpa mengklaim properti yang belum tentu benar (mis. tidak memakai kata "aman" secara mutlak, sesuai aturan anti-overclaim `CLAUDE_PREPARATION_BRIEF.md` aturan #16).

~~Ketiga judul memakai nama panjang AKSARA hanya sebagai konteks penamaan proyek di BAB I, bukan bagian dari judul TA itu sendiri.~~ **DIBATALKAN 2026-07-27** atas instruksi eksplisit pengguna: kepanjangan AKSARA (*Authenticated Key-based Secure Autonomous Relay Architecture*) **masuk ke judul**. Bentuk final yang diusulkan ada di `16_DOCUMENT_FORMAT_SPEC.md` §2, menggabungkan instruksi tersebut dengan isi Judul #3 dan pola judul proposal CARAKA.

---

## 8. Pembagian Tiga Anggota

Pembagian dibuat berdasarkan struktur modul aktual (`src/identity`, `src/crypto`, `src/transport`, `src/session`, `src/contacts`, `src/tui`, `src/main.rs`/`src/error.rs`) dan file evidence mentah TAHAP 2/3 yang sudah dipetakan per modul (`evidence/_raw-audit-json/*.json`), mengikuti pola kategori contoh di brief (audit primitif/key management; protokol komunikasi/integrasi kripto; testing/benchmarking/analisis/dokumentasi) — **disesuaikan** dengan struktur codebase nyata, bukan disalin mentah dari kategori generik brief.

| Anggota | Modul | Tugas Teknis | Eksperimen (rencana TAHAP 13) | Bagian Laporan | Evidence |
|---|---|---|---|---|---|
| **Anggota 1 — Andika Aryansyach Fauzan** (2322101878) | `src/identity/` (`keypair.rs`, `vault.rs`), `src/crypto/handshake.rs` (primitif) | Audit dan verifikasi ulang inventarisasi primitif CORE-1..7 (`02`/`03`); jelaskan generation kunci (`OsRng`), layout vault 108-byte, alur `seal()`/`unseal()`, parameter Argon2id; dukung penulisan BAB II (kajian teori primitif) dan bagian primitif BAB IV | Correctness roundtrip vault (`seal`→`unseal`), verifikasi ukuran salt/nonce/tag sesuai spesifikasi, timing kasar Argon2id (mengoreksi/mengonfirmasi klaim "~100ms" yang saat ini `DOCUMENTED_ONLY`) | BAB II (primitif kriptografi), BAB IV bagian identity/vault | `identity.json`, `02_CRYPTO_IMPLEMENTATION_AUDIT.md`, `04_CRYPTOGRAPHIC_JUSTIFICATION.md`, `07_KEY_LIFECYCLE.md` §2-3 |
| **Anggota 2 — Mahendra Nur Hidayat** (2322101937) | `src/transport/` (`mod.rs`, `lan.rs`, `tor.rs`, `frame.rs`), `src/session/mod.rs` | Dokumentasikan alur protokol end-to-end (discovery → handshake → transport, `06_PROTOCOL_SPECIFICATION.md` §4-6); jelaskan orkestrasi `run_session`, model konkurensi/cancel-safety, framing; dukung penulisan BAB IV inti (perancangan dan implementasi protokol) | Pengujian handshake roundtrip end-to-end (LAN loopback, mengacu test `lan_session_message_roundtrip`), pengujian rejection (wrong-key, oversized payload, replay bila relevan), pengukuran overhead framing/AEAD (16-byte tag) | BAB IV (inti — protokol komunikasi), BAB III (metodologi pengujian protokol) | `session.json`, `crypto_handshake.json`, `transport_lan.json`, `transport_tor.json`, `06_PROTOCOL_SPECIFICATION.md` |
| **Anggota 3 — Rafi Putra Fadlurrahman** (2322101963) | `src/contacts/mod.rs`, `src/tui/` (titik integrasi kripto saja), `src/main.rs`/`src/error.rs`; lintas-modul: testing, benchmarking, analisis, dokumentasi | Jelaskan invite code/fingerprint binding (`contacts/mod.rs`), integrasi kripto di TUI/main (passphrase handling, error mapping); agregasi hasil pengujian Anggota 1 & 2; susun threat model (`08_THREAT_MODEL.md`) dan risk register; koordinasi referensi, diagram, tabel, dan content pack BAB I/V/VI | Pengujian invite/fingerprint binding (`fingerprint_binds_both_keys`), agregasi metrik lintas eksperimen, analisis risk register T1-T7 vs hasil pengujian aktual | BAB I (pendahuluan), BAB V (pengujian dan analisis, digabung hasil Anggota 1+2), BAB VI (penutup) | `contacts.json`, `main_and_error.json`, `08_THREAT_MODEL.md`, seluruh dokumen TAHAP 8-17 |

**Catatan keseimbangan**: ketiga anggota memiliki cakupan modul yang sebanding (Anggota 1: 2 file inti; Anggota 2: 4 file inti; Anggota 3: 2 file inti + peran integratif lintas-tim) — Anggota 2 mendapat lebih banyak file karena modul transport secara alami lebih terpecah (LAN/Tor/framing terpisah), namun kompleksitas konseptual (jumlah primitif kriptografi unik yang harus dijustifikasi) tetap seimbang dengan Anggota 1. Anggota 3 memikul beban integrasi/dokumentasi lebih besar sebagai kompensasi cakupan modul teknis yang lebih kecil — pola ini konsisten dengan contoh kategori di brief ("testing, benchmarking, analisis, dan dokumentasi").

---

## 9. Ringkasan Confidence

| Klaim di dokumen ini | Confidence | Catatan |
|---|---|---|
| Fokus utama = satu rangkaian protokol berkaitan (vault→identity→handshake→transport) | HIGH | Diverifikasi langsung dari alur data di `06_PROTOCOL_SPECIFICATION.md`/`07_KEY_LIFECYCLE.md`, bukan asumsi baru |
| Pemetaan modul ke anggota sesuai struktur codebase nyata | HIGH | Berdasarkan `evidence/_raw-audit-json/*.json` per modul (TAHAP 2/3), bukan kategori generik brief yang disalin mentah |
| Nama anggota kelompok | `CONFIRMED` (2026-07-27) | Andika Aryansyach Fauzan (2322101878), Mahendra Nur Hidayat (2322101937), Rafi Putra Fadlurrahman (2322101963). Sumber: `00-template/PROPOSAL CARAKA (2).docx`, ditunjuk pengguna. Yang tersisa hanya pemetaan nama ke peran modul |
| Judul rekomendasi #3 | Rekomendasi tim penulis, bukan fakta terverifikasi | Keputusan editorial berbasis kesesuaian scope, dapat diubah oleh anggota kelompok/dosen pembimbing |

---

## Referensi

Dokumen ini tidak memperkenalkan referensi teori baru — seluruh klaim teknis merujuk ke `06_PROTOCOL_SPECIFICATION.md`, `07_KEY_LIFECYCLE.md`, `08_THREAT_MODEL.md`, dan `02`-`05` yang sudah memakai citekey dari `references/REFERENCES.bib` (TAHAP 4/9/SESSION 3, 33 entry).
