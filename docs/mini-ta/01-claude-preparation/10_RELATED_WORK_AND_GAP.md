# 10 — Penelitian Terkait dan Research Gap AKSARA

Dokumen ini memposisikan AKSARA terhadap penelitian dan sistem P2P/pesan terenkripsi sejenis. Basis evidence AKSARA: `06_PROTOCOL_SPECIFICATION.md`, `07_KEY_LIFECYCLE.md`, `08_THREAT_MODEL.md` (TAHAP 5-7) dan `02`-`05` (TAHAP 2-4). Basis referensi pembanding: 7 sumber baru yang diverifikasi via `you-search` sesi ini (dicatat lengkap di `references/MCP_RESEARCH_LOG.md` §SESSION 4), ditambahkan ke `references/REFERENCES.bib` (total kini 40 entry) dan `references/REFERENCE_MATRIX.md`.

**Catatan metodologis penting**: 7 sumber ini dipilih lewat pencarian terarah (bukan systematic literature review berskala penuh) — proporsional untuk cakupan tugas mata kuliah sesuai `CLAUDE_PREPARATION_BRIEF.md` §Batas Scope ("lima sampai delapan penelitian terkait"). Klaim gap di §3 dibingkai sebagai **"belum ditemukan pada sumber yang ditinjau"**, bukan **"belum pernah diteliti"** — sesuai larangan eksplisit brief ("Jangan mengklaim 'belum pernah diteliti' tanpa systematic evidence").

---

## 1. Ringkasan Posisi AKSARA

AKSARA adalah aplikasi chat P2P dua-pihak, serverless, berbasis terminal (TUI), memakai Noise_IK (`Noise_IK_25519_ChaChaPoly_BLAKE2s` via crate `snow` 0.10.0) untuk autentikasi+kerahasiaan sesi, dengan dua jalur transport (LAN mDNS, Tor onion service v3) dan penyimpanan identitas terenkripsi lokal (vault Argon2id+ChaCha20-Poly1305). Tidak ada server, broker, atau relay pusat pada arsitektur maupun jalur data manapun (`06_PROTOCOL_SPECIFICATION.md` §1).

Tiga sumbu perbandingan dipakai terhadap tiap related work di §2:
1. **Kerangka kriptografi** — pola handshake/AEAD/KDF yang dipakai, dan apakah ada verifikasi formal terhadap pola tersebut.
2. **Manajemen kunci** — ada/tidaknya rotasi, ratcheting, atau mekanisme pembaruan kunci sesi.
3. **Arsitektur jaringan** — P2P murni vs. federated/hybrid, mekanisme discovery, dan lapisan anonimitas (bila ada).

---

## 2. Tabel Penelitian Terkait

| No | Penelitian | Primitif | Sistem | Metode | Metrik | Hasil | Perbedaan dengan AKSARA |
|----|------------|----------|--------|--------|--------|-------|------------|
| 1 | `kobeissi2019noiseexplorer` — Kobeissi, Nicolas, Bhargavan, *Noise Explorer* (IEEE EuroS&P 2019) | Noise Protocol Framework (seluruh pola handshake, termasuk `IK`) | Noise Explorer (tool verifikasi formal, bukan aplikasi chat) | Model-checking otomatis via ProVerif; menghasilkan laporan formal per pola handshake | Properti keamanan formal per pesan (confidentiality, authentication, identity-hiding) yang terverifikasi/tidak per pola | Memformalkan dan memverifikasi properti keamanan pola-pola Noise (termasuk `IK`) secara otomatis dan dapat diulang | AKSARA memakai pola `IK` **tanpa** verifikasi formal terhadap instansiasi spesifiknya sendiri (`Noise_IK_25519_ChaChaPoly_BLAKE2s`); klaim properti keamanan AKSARA (`06_PROTOCOL_SPECIFICATION.md` §5.3) diwarisi dari analisis umum pola `IK` di `noise2018`, bukan hasil tool verifikasi formal seperti ini |
| 2 | `cohngordon2020signal` — Cohn-Gordon, Cremers, Dowling, Garratt, Stebila, *Formal Security Analysis of Signal* (J. Cryptology 2020) | X3DH + Double Ratchet (key agreement awal + ratcheting per pesan) | Signal Protocol (dipakai WhatsApp, Signal, dll., >1 miliar pengguna) | Model keamanan formal multi-stage untuk menangkap struktur ratchet sebagai "pohon" tahapan kunci | Properti formal: forward secrecy, post-compromise security ("future secrecy") | Membuktikan Signal mencapai post-compromise security lewat pembaruan kunci sesi berkelanjutan (ratchet) | AKSARA memakai **satu** kunci transport statis sepanjang masa hidup sesi tanpa ratchet apapun (`07_KEY_LIFECYCLE.md` §6) — tidak ada post-compromise security: kompromi kunci sesi/identity AKSARA tidak dapat dipulihkan tanpa membuat identitas baru |
| 3 | `donenfeld2017wireguard` — Donenfeld, *WireGuard* (NDSS 2017) | Noise Protocol (varian `IK` dengan cookie anti-DoS), ChaCha20-Poly1305, BLAKE2s, Curve25519 | WireGuard (VPN kernel-level Linux) | Desain protokol + implementasi kernel; evaluasi performa throughput/latensi | Baris kode (< 4000 LOC), throughput vs IPsec/OpenVPN | Protokol berbasis Noise dengan stack primitif nyaris identik AKSARA (X25519/ChaCha20-Poly1305/BLAKE2s) terbukti lebih ringkas dan performan dibanding VPN klasik | AKSARA memakai kombinasi primitif yang sama tapi untuk kanal chat P2P (bukan tunnel IP); WireGuard menambahkan **cookie anti-DoS** dan **rekey berkala berbasis waktu/volume data** — dua mekanisme yang **tidak ditemukan** pada implementasi AKSARA (`06_PROTOCOL_SPECIFICATION.md` tidak menyebutkan rekey/cookie apapun) |
| 4 | `borisov2004otr` — Borisov, Goldberg, Brewer, *Off-the-Record Communication* (WPES 2004) | Diffie-Hellman + AES + SHA-1 HMAC (desain OTR generasi awal) | Off-the-Record Messaging (plugin IM) | Desain protokol baru sebagai kontras eksplisit terhadap PGP/S-MIME (non-repudiation permanen) | Properti kualitatif: deniability, perfect forward secrecy, tanpa non-repudiation permanen | Memperkenalkan "deniability" dan forward secrecy sebagai syarat desain pesan instan yang berorientasi percakapan santai (bukan dokumen resmi seperti email PGP) | AKSARA tidak dirancang untuk deniability (Ed25519 hanya fingerprint — `07_KEY_LIFECYCLE.md` §5.1, bukan skema signing-dapat-disangkal); forward secrecy AKSARA berstatus `DOCUMENTED_ONLY` (properti umum Noise_IK yang diwarisi, bukan diverifikasi test AKSARA sendiri), bukan properti yang secara eksplisit dirancang seperti OTR |
| 5 | `albrecht2024matrix` — Albrecht, Dowling, Jones, *Formal Cryptographic Analysis of Matrix' Core* (IEEE S&P 2024) | Olm (Double Ratchet 1-ke-1) + Megolm (ratchet grup dengan rotasi sesi) | Matrix (protokol pesan terfederasi multi-device, non-P2P murni) | Model formal "Device-Oriented Group Messaging" untuk menangkap relasi user-device-group | Properti formal keamanan Megolm/Olm pada konteks multi-device | Memformalkan dan menganalisis keamanan rotasi sesi Megolm pada arsitektur federated | AKSARA **tidak memiliki mekanisme rotasi/revokasi apapun** untuk kunci manapun (vault, identity, Noise, session — T7 `08_THREAT_MODEL.md` §6), kontras langsung dengan rotasi sesi eksplisit Megolm; AKSARA juga P2P murni satu-identitas-satu-perangkat, bukan federated multi-device |
| 6 | `briarspec` — Briar Project, spesifikasi Bramble Protocol Suite | Curve25519 (key agreement) + AEAD (BTP — Bramble Transport Protocol), transport ganda Tor/Bluetooth/Wi-Fi | Briar (aplikasi pesan P2P serverless, target aktivis/jurnalis) | Sinkronisasi P2P langsung antar perangkat tanpa server; jalur online via Tor, jalur offline via Bluetooth/Wi-Fi/USB | Tidak ada metrik kuantitatif terpublikasi dalam spesifikasi (dokumentasi arsitektur, bukan paper evaluasi) | Sistem produksi P2P serverless yang berjalan dengan Tor sebagai salah satu jalur transport, mirip strategi AKSARA | Arsitektur **paling dekat** dengan AKSARA (P2P dua pihak, Tor sebagai transport) — beda utama: Briar punya jalur offline (Bluetooth/Wi-Fi/USB) yang tidak dimiliki AKSARA, dan kontak Briar ditukar via link/QR dengan proses handshake kontak (BHP) yang lebih terstruktur dibanding invite code AKSARA yang eksplisit **tidak** diautentikasi kriptografis (`06_PROTOCOL_SPECIFICATION.md` §3) |
| 7 | `toxspec` — TokTok/Tox Project, spesifikasi protokol Tox | NaCl (`crypto_box`, Curve25519 + XSalsa20-Poly1305) | Tox (pesan instan P2P murni, tanpa server) | Discovery peer via DHT (Kademlia-like), koneksi langsung P2P setelah ditemukan | Tidak ada metrik kuantitatif terpublikasi dalam spesifikasi | Sistem P2P murni tanpa server yang beroperasi hingga saat ini, secara eksplisit menyatakan **belum diaudit keamanan independen** | Arsitektur P2P serverless serupa AKSARA, tapi memakai NaCl (bukan Noise Protocol Framework) dan DHT untuk discovery (bukan mDNS); status "belum diaudit formal" pada Tox paralel dengan status crate `snow` yang dipakai AKSARA (`04_CRYPTOGRAPHIC_JUSTIFICATION.md` CORE-1 poin 5) — keduanya berbagi risiko implementasi yang sama secara kualitatif |

---

## 3. Research Gap

Gap berikut diidentifikasi dari **perbandingan langsung** antara evidence AKSARA (TAHAP 2-7) dan 7 sumber di §2 — bukan klaim generalisasi terhadap seluruh literatur pesan terenkripsi.

### G1 — Ketiadaan verifikasi formal terhadap instansiasi Noise_IK spesifik AKSARA

`kobeissi2019noiseexplorer` menunjukkan bahwa pola Noise (termasuk `IK`) dapat diverifikasi formal secara otomatis per instansiasi. AKSARA memakai `Noise_IK_25519_ChaChaPoly_BLAKE2s` (CORE-1) tanpa verifikasi formal khusus terhadap kombinasi primitif ini — seluruh klaim properti keamanan (`06_PROTOCOL_SPECIFICATION.md` §5.3) bersumber dari analisis generik pola `IK` di `noise2018`, dikombinasikan dengan bukti test empiris terbatas (roundtrip handshake, penolakan peer key salah). **Gap ini bersifat evaluatif** (dapat diukur pada TAHAP 13/SESSION 5 sejauh menjalankan tool eksternal seperti Noise Explorer di luar cakupan sesi ini), bukan celah implementasi yang sudah terbukti salah.

### G2 — Ketiadaan mekanisme rotasi/ratcheting kunci sesi

`cohngordon2020signal` (Double Ratchet) dan `albrecht2024matrix` (Megolm) menunjukkan dua pendekatan matang untuk rotasi kunci sesi pada protokol pesan terenkripsi produksi. AKSARA **tidak memiliki mekanisme serupa apapun** — dikonfirmasi eksplisit tidak ditemukan di seluruh source yang diaudit (T7, `08_THREAT_MODEL.md` §6; `07_KEY_LIFECYCLE.md` §6). Ini adalah gap desain yang **sudah terdokumentasi sebagai keterbatasan sadar** pada level implementasi AKSARA saat ini (M1), bukan temuan baru sesi ini — TAHAP 10 hanya memposisikannya secara eksplisit terhadap dua pendekatan matang yang ada di literatur.

### G3 — Belum ada evaluasi overhead protokol pada konteks jaringan lokal/Tor spesifik AKSARA

`donenfeld2017wireguard` mempublikasikan metrik throughput/latensi kuantitatif untuk sistem berbasis Noise sejenis. AKSARA belum memiliki data eksperimen serupa (overhead framing, latensi handshake pada LAN vs Tor, dsb.) — TAHAP 13 (SESSION 5) merencanakan pengujian ini, namun **belum dijalankan** pada sesi manapun hingga saat ini. Gap ini murni `NEEDS_EXPERIMENT`, bukan gap desain.

### G4 — Invite code AKSARA tidak memiliki proses handshake kontak terstruktur seperti Briar

Briar (`briarspec`) memiliki protokol handshake kontak eksplisit (Bramble Handshake Protocol) yang melibatkan pembuktian kepemilikan kunci sebelum kontak ditambahkan. Invite code AKSARA **secara eksplisit tidak diautentikasi kriptografis** (`06_PROTOCOL_SPECIFICATION.md` §3, `08_THREAT_MODEL.md` §4.1, T3) — keaslian bergantung sepenuhnya pada verifikasi fingerprint manual di luar protokol. Gap ini sudah tercatat di threat model TAHAP 7 sebagai T3; TAHAP 10 menambahkan pembanding konkret (Briar) yang menunjukkan pendekatan alternatif yang lebih terstruktur pernah diimplementasikan pada sistem serupa.

### G5 — Ketiadaan mekanisme fallback offline (dibandingkan Briar)

Briar mendukung sinkronisasi Bluetooth/Wi-Fi/USB saat internet tidak tersedia. AKSARA hanya mendukung dua jalur (LAN langsung atau Tor via internet) — tidak ada jalur delay-tolerant/offline. Ini **bukan kekurangan** dalam scope AKSARA saat ini (di luar tujuan desain M1, tidak disebutkan di dokumentasi manapun sebagai target), melainkan perbedaan cakupan fitur yang relevan dicatat sebagai konteks perbandingan arsitektur, bukan gap keamanan.

### Batasan Penilaian Gap

Sesuai batasan cakupan `08_THREAT_MODEL.md` §5 dan larangan brief terhadap klaim novelty setingkat skripsi: gap di atas **tidak diklaim sebagai kontribusi orisinal berskala publikasi ilmiah**. G1-G5 adalah observasi perbandingan terstruktur yang proporsional untuk tugas mata kuliah, ditujukan untuk memperkaya BAB II (kajian pustaka) dan BAB VI (penutup, keterbatasan/saran) pada TAHAP 15.

---

## 4. Ringkasan Confidence

| Klaim | Confidence | Catatan |
|---|---|---|
| 7 referensi related work terverifikasi (judul/penulis/tahun/venue/DOI/URL) | HIGH | Seluruhnya dicek langsung ke halaman resmi, dicatat di `MCP_RESEARCH_LOG.md` §SESSION 4 |
| AKSARA tidak punya rotasi/ratcheting kunci sesi (G2) | HIGH | Sudah diverifikasi source-level penuh di TAHAP 6/7, bukan klaim baru sesi ini |
| AKSARA tidak punya verifikasi formal Noise_IK spesifik (G1) | HIGH (untuk fakta ketiadaannya) | Tidak ditemukan artefak verifikasi formal apapun di repository AKSARA |
| Briar adalah sistem "paling dekat" secara arsitektural dengan AKSARA di antara 7 pembanding | Penilaian kualitatif tim penulis | Berdasarkan kombinasi P2P-murni + pemakaian Tor; bukan hasil scoring sistematis |

---

## Referensi

7 referensi baru sesi ini: `kobeissi2019noiseexplorer`, `cohngordon2020signal`, `donenfeld2017wireguard`, `borisov2004otr`, `albrecht2024matrix`, `briarspec`, `toxspec` — ditambahkan ke `references/REFERENCES.bib` (total 40 entry), `references/REFERENCE_MATRIX.md`, dan `references/ANNOTATED_BIBLIOGRAPHY.md`. Jejak pencarian lengkap: `references/MCP_RESEARCH_LOG.md` §SESSION 4. Referensi CORE-1..7 yang dirujuk pada tabel §2 sudah ada sejak TAHAP 4/9 (`noise2018`, `rfc8439`, `rfc7693`, dst.), tidak diulang di sini.
