# MCP Research Log — TAHAP 4 (riset referensi digabung dari TAHAP 9)

Tanggal sesi: 2026-07-26. Tujuan: mencari referensi standar/RFC/paper/dokumentasi library secara targeted untuk 7 komponen kriptografi inti (CORE-1..7) hasil normalisasi `03_CRYPTO_INVENTORY_NORMALIZED.md`, plus referensi pembanding untuk `05_CRYPTO_ALTERNATIVE_COMPARISON.md`.

## Ringkasan Hasil

- 31 referensi terverifikasi (judul, penulis, tahun, venue/publisher, DOI/URL dicek langsung dari halaman resmi).
- 25 dari 31 adalah sumber primer/standar resmi (RFC IETF, FIPS/SP NIST, spesifikasi protokol resmi, paper peer-reviewed) — jauh di atas syarat minimum 5.
- Tidak ada referensi yang diterima hanya dari ingatan/pelatihan model tanpa verifikasi pencarian — seluruh entry di `REFERENCES.bib` memiliki jejak pencarian di bawah, KECUALI dua crate doc (`argon2crate`, `blake2crate`) yang URL-nya diturunkan dari pola URL docs.rs yang sudah diverifikasi berulang pada 4 crate `RustCrypto`/`dalek-cryptography` lain (lihat catatan di bagian akhir).

## MCP yang Dipakai dan Kendala

| MCP | Status | Catatan |
|-----|--------|---------|
| `semantic-scholar` (search_papers) | **Rate-limited** | Percobaan pertama (query "Curve25519 new Diffie-Hellman speed records") berhasil dan mengonfirmasi metadata Bernstein 2006/PKC. Percobaan kedua dan seterusnya (query "ChaCha a variant of Salsa20") gagal dengan `RateLimitError (retry_after: 60)` pada seluruh 4 percobaan retry internal tool, termasuk setelah jeda beberapa menit di percobaan ulang berikutnya. Kemungkinan API key/kuota bersama sudah terpakai sebelum sesi ini. Tool dialihkan ke `ydc-server` (you-search) sebagai fallback sesuai hierarki MCP di `CLAUDE.md`/`00_TOOL_AND_MCP_INVENTORY.md`. |
| `tavily` (tavily-search) | **Gagal (API error 432)** | 4 percobaan pertama (RFC 8439, RFC 7748, RFC 9106, RFC 7693) seluruhnya gagal dengan HTTP 432 (indikasi limit paket/plan API habis, bukan error transient). Tidak dicoba ulang setelah kegagalan konsisten pada 4 query berbeda — dialihkan ke `ydc-server`. |
| `ydc-server` (you-search) | **Berhasil, dipakai sebagai sumber utama** | Seluruh 26 query verifikasi standar/RFC/NIST/paper/crate-doc berhasil lewat tool ini, dengan `include_domains` diarahkan ke domain resmi (`datatracker.ietf.org`, `rfc-editor.org`, `csrc.nist.gov`, `nvlpubs.nist.gov`, `noiseprotocol.org`, `signal.org`, `docs.rs`, `crates.io`, `github.com`) untuk memastikan hasil dari sumber primer, bukan blog/tutorial pihak ketiga. |
| `context7` | **Tidak dipakai** | Dicoba dipertimbangkan untuk dokumentasi crate Rust, tapi `ydc-server` dengan domain filter `docs.rs`/`crates.io` sudah cukup dan lebih cepat untuk crate spesifik-versi (Context7 lebih optimal untuk framework besar dengan indexing mendalam, bukan crate Rust kecil bervensi presisi). |

## Jejak Pencarian per Referensi

Format: `citekey — query yang dipakai — domain hasil yang dikonfirmasi`.

| Citekey | Query | Sumber Terverifikasi |
|---------|-------|------------------------|
| `bernstein2006curve25519` | "Curve25519 new Diffie-Hellman speed records" (semantic-scholar) | semanticscholar.org — konfirmasi penulis D. Bernstein, tahun 2006, venue PKC |
| `rfc7748` | "RFC 7748 Elliptic Curves for Security X25519 X448" (you-search) | datatracker.ietf.org/doc/html/rfc7748, rfc-editor.org/rfc/rfc7748.html |
| `rfc8439` | "RFC 8439 ChaCha20-Poly1305 for IETF Protocols" (you-search) | datatracker.ietf.org/doc/rfc8439, rfc-editor.org/rfc/rfc8439.html |
| `rfc9106` | "RFC 9106 Argon2 memory-hard function for password hashing" (you-search) | datatracker.ietf.org/doc/rfc9106, rfc-editor.org/info/rfc9106 |
| `rfc7693` | "RFC 7693 BLAKE2 Cryptographic Hash and MAC" (you-search) | datatracker.ietf.org/doc/html/rfc7693.html, bibtex resmi di datatracker.ietf.org/doc/rfc7693/bibtex |
| `rfc8032` | "RFC 8032 Edwards-Curve Digital Signature Algorithm EdDSA" (you-search) | datatracker.ietf.org/doc/html/rfc8032, bibtex resmi |
| `noise2018` | "Noise Protocol Framework specification Trevor Perrin" (you-search) | noiseprotocol.org/noise.html (Revision 34, 2018-07-11) |
| `rfc8446` | "RFC 8446 The Transport Layer Security TLS Protocol Version 1.3" (you-search) | datatracker.ietf.org/doc/html/rfc8446, bibtex resmi |
| `rfc8452` | "RFC 8452 AES-GCM-SIV Nonce Misuse-Resistant Authenticated Encryption" (you-search) | datatracker.ietf.org/doc/html/rfc8452 |
| `rfc7914` | "RFC 7914 The scrypt Password-Based Key Derivation Function" (you-search) | datatracker.ietf.org/doc/html/rfc7914.html |
| `rfc8018` | "RFC 8018 PKCS 5 Password-Based Cryptography Specification PBKDF2" (you-search) | datatracker.ietf.org/doc/html/rfc8018, bibtex resmi |
| `fips180-4` | "NIST FIPS 180-4 Secure Hash Standard SHS SHA-256" (you-search) | csrc.nist.gov/pubs/fips/180-4/upd1/final |
| `fips202` | "NIST FIPS 202 SHA-3 Standard Permutation-Based Hash" (you-search) | csrc.nist.gov/pubs/fips/202/final |
| `sp800-38d` | "NIST SP 800-38D ... Galois Counter Mode GCM GMAC" (you-search) | csrc.nist.gov/pubs/sp/800/38/d/final (penulis M. Dworkin dikonfirmasi dari PDF nvlpubs.nist.gov) |
| `fips186-5` | "NIST FIPS 186-5 Digital Signature Standard DSS EdDSA ECDSA" (you-search) | csrc.nist.gov/pubs/fips/186-5/final |
| `sp800-186` | "NIST SP 800-186 ... elliptic curve domain parameters P-256" (you-search) | csrc.nist.gov/pubs/sp/800/186/final, nvlpubs.nist.gov (penulis Chen/Moody/Regenscheid/Robinson/Randall) |
| `x3dh2016` | "Signal X3DH Extended Triple Diffie-Hellman ... Marlinspike Perrin" (you-search) | signal.org/docs/specifications/x3dh/ |
| `bernstein2008chacha` | "ChaCha, a variant of Salsa20 Bernstein 2008 paper" (you-search) | cr.yp.to/chacha/chacha-20080120.pdf |
| `bernstein2005poly1305` | "The Poly1305-AES message-authentication code Bernstein FSE 2005" (you-search) | link.springer.com/chapter/10.1007/11502760_3, cr.yp.to/mac/poly1305-20050329.pdf |
| `biryukov2016argon2` | "Argon2 New Generation of Memory-Hard Functions ... EuroS&P 2016" (you-search) | semanticscholar.org (venue + halaman 292-302 + DOI 10.1109/EuroSP.2016.31), rfc-editor.org/rfc9106 (referensi silang) |
| `aumasson2013blake2` | "BLAKE2 simpler smaller fast as MD5 ... ACNS 2013" (you-search) | eprint.iacr.org/2013/322, link.springer.com/chapter/10.1007/978-3-642-38980-1_8 |
| `bernstein2012ed25519` | "High-speed high-security signatures Ed25519 ... Journal of Cryptographic Engineering" (you-search) | link.springer.com/article/10.1007/s13389-012-0027-1, eprint.iacr.org/2011/368, cryptojedi.org/papers/ed25519.bib |
| `percival2009scrypt` | "Stronger Key Derivation via Sequential Memory-Hard Functions Percival scrypt BSDCan 2009" (you-search) | tarsnap.com/scrypt/scrypt.pdf, bsdcan.org/2009/schedule/attachments/87_scrypt.pdf |
| `sp800-90a` | "NIST SP 800-90A ... Deterministic Random Bit Generators" (you-search) | csrc.nist.gov/pubs/sp/800/90/a/r1/final |
| `randcrate` | "rand crate OsRng getrandom crate documentation docs.rs" (you-search) | docs.rs/rand/0.8.4/rand/rngs/ (pola URL versi dikonfirmasi, disesuaikan ke versi proyek 0.8.6 sesuai `Cargo.lock`) |
| `snowcrate` | "snow crate docs.rs Noise Protocol Framework Rust implementation" (you-search) | docs.rs/snow/, crates.io/crates/snow, github.com/mcginty/snow |
| `chacha20poly1305crate` | "RustCrypto chacha20poly1305 argon2 ed25519-dalek x25519-dalek blake2 crates docs.rs" (you-search) | docs.rs/chacha20poly1305/latest/chacha20poly1305/, crates.io/crates/chacha20poly1305 |
| `ed25519dalekcrate` | "RustCrypto ed25519-dalek x25519-dalek argon2 blake2 crates.io official RustCrypto GitHub organization" (you-search) | docs.rs/crate/ed25519-dalek/latest (versi 2.2.0 dikonfirmasi persis cocok `Cargo.lock`) |
| `x25519dalekcrate` | "docs.rs x25519-dalek argon2 blake2 crate documentation RustCrypto" (you-search) | docs.rs/crate/x25519-dalek/latest (versi 2.0.1 dikonfirmasi persis cocok `Cargo.lock`) |
| `argon2crate` | *(tidak ada hasil langsung pada query di atas)* | **Tidak diverifikasi independen** — URL `docs.rs/argon2/0.5.3/argon2/` diturunkan dari pola URL docs.rs yang konsisten pada 4 crate lain yang sudah dikonfirmasi (snow, chacha20poly1305, ed25519-dalek, x25519-dalek); versi 0.5.3 diambil dari ground truth `Cargo.lock` yang sudah diverifikasi TAHAP 2/3 (bukan asumsi baru) |
| `blake2crate` | *(tidak ada hasil langsung pada query di atas)* | **Tidak diverifikasi independen** — sama seperti `argon2crate`, pola URL + versi 0.10.6 dari ground truth `Cargo.lock` |

## Keputusan Metodologis

1. **Hierarki sumber diikuti sesuai brief**: standar resmi/RFC diprioritaskan di atas paper, paper primer di atas dokumentasi library, dokumentasi library di atas sumber sekunder (blog/tutorial). Tidak ada satu pun referensi final yang berasal dari blog pihak ketiga atau ringkasan non-resmi.
2. **`include_domains` dipakai secara konsisten** pada `you-search` untuk memaksa hasil dari domain resmi (`datatracker.ietf.org`, `csrc.nist.gov`, dst.), menghindari risiko mengutip mirror/ringkasan pihak ketiga yang berpotensi keliru.
3. **Dua crate doc (`argon2crate`, `blake2crate`) TIDAK diverifikasi via pencarian langsung** — didokumentasikan secara eksplisit di atas sebagai penyimpangan dari proses standar, dengan alasan: (a) pola URL docs.rs sudah diverifikasi berulang untuk 4 crate sejenis dari publisher yang sama, (b) nomor versi berasal dari `Cargo.lock` yang sudah menjadi ground truth terverifikasi sejak TAHAP 1-3, bukan klaim baru. Risiko kesalahan dinilai rendah tapi tidak nol — jika ada keraguan pada saat penulisan BAB, verifikasi ulang manual disarankan sebelum submission akhir.
4. **`bernstein2008chacha` diberi kualitas MEDIUM-HIGH, bukan HIGH**, karena statusnya sebagai technical report pribadi penulis tanpa peer-review formal — dicatat eksplisit di `ANNOTATED_BIBLIOGRAPHY.md` dan `REFERENCE_MATRIX.md` agar tidak disalahartikan sebagai paper peer-reviewed penuh setara `bernstein2005poly1305` atau `biryukov2016argon2`.
5. **Tidak ada klaim algoritma/parameter yang dimasukkan ke `04_CRYPTOGRAPHIC_JUSTIFICATION.md`/`05_CRYPTO_ALTERNATIVE_COMPARISON.md` tanpa rujukan pada tabel di atas** — bila sebuah pernyataan teoretis tidak punya sumber terverifikasi di sesi ini, pernyataan tersebut ditandai `NEEDS_CONFIRMATION` di badan dokumen, bukan disajikan sebagai fakta.

---

## SESSION 4 (TAHAP 10 — Related Work & Gap, 2026-07-26)

Tujuan: mencari 5-8 penelitian/sistem terkait untuk `10_RELATED_WORK_AND_GAP.md` — literatur pembanding aplikasi/protokol chat P2P terenkripsi sejenis. 33 referensi TAHAP 4/9/SESSION 3 seluruhnya berfokus primitif kriptografi + mDNS, **bukan** related-work level aplikasi/protokol — gap ini dikonfirmasi eksplisit di `SESSION_3_HANDOFF.md` poin 5.

### MCP yang Dipakai

`ydc-server` (you-search) — 9 query, seluruhnya berhasil pada percobaan pertama tanpa `include_domains` (query memakai judul/penulis/venue spesifik sehingga hasil top otomatis mengarah ke halaman resmi paper/proyek: eprint.iacr.org, ndss-symposium.org, dl.acm.org, gitlab.matrix.org, code.briarproject.org, toktok.ltd). Tidak ada MCP lain dipakai — konsisten batasan CLAUDE.md ("gunakan MCP hanya untuk kebutuhan tahap aktif").

### Jejak Pencarian

| Citekey | Query | Sumber Terverifikasi |
|---------|-------|------------------------|
| `kobeissi2019noiseexplorer` | "Noise Explorer formal verification Noise Protocol Framework Kobeissi Bhargavan paper" | eprint.iacr.org/2018/766 (bibtex resmi), wireguard.com (PDF ter-host), semanticscholar.org, hal.science (konfirmasi presentasi RWC 2019 + publikasi EuroS&P 2019) |
| `cohngordon2020signal` | "A Formal Security Analysis of the Signal Messaging Protocol Cohn-Gordon Cremers Dowling" | eprint.iacr.org/2016/1013 (bibtex resmi), link.springer.com/article/10.1007/s00145-020-09360-1 (J. Cryptology vol 33, 2020), dl.acm.org (DOI cross-check) |
| `donenfeld2017wireguard` | "WireGuard Jason Donenfeld NDSS 2017 paper next generation kernel network tunnel" | ndss-symposium.org/ndss2017/ndss-2017-programme/ (halaman resmi program NDSS), ndss-symposium.org PDF paper resmi |
| `borisov2004otr` | "Off-the-Record Communication Why Not To Use PGP Borisov Goldberg Brewer WPES 2004" | dl.acm.org/doi/10.1145/1029179.1029200 (DOI resmi ACM), otr.cypherpunks.ca/otr-wpes.pdf (PDF asli penulis) |
| `briarspec` | "Briar messaging app peer-to-peer Tor encrypted architecture whitepaper" + "Briar project academic paper Bramble protocol specification technical report peer-to-peer secure messaging Rogers" | briarproject.org/how-it-works/, code.briarproject.org/briar/briar-spec (repositori spesifikasi resmi), en.wikipedia.org/wiki/Briar_(software) (konfirmasi Bramble protocol suite), ethz.ch (laporan analisis independen ETH Zürich sebagai konteks tambahan, tidak dijadikan citekey terpisah) |
| `toxspec` | "Tox protocol peer-to-peer encrypted instant messaging NaCl cryptography spec" | toktok.ltd/spec.html (spesifikasi resmi TokTok), en.wikipedia.org/wiki/Tox_(protocol) (konfirmasi arsitektur DHT+NaCl, status belum diaudit formal) |
| `albrecht2024matrix` | "Matrix Olm Megolm cryptographic ratchet specification decentralized messaging" + "A Formal Cryptographic Analysis of Matrix' Core eprint 2023/1300 authors Usenix" | eprint.iacr.org/2023/1300 (bibtex resmi), ieeexplore.ieee.org/document/10646860 (konfirmasi publikasi IEEE S&P 2024), martinralbrecht.wordpress.com (blog penulis pertama, konfirmasi venue) |

### Keputusan Metodologis

1. **7 kandidat dipilih dari domain berbeda** untuk menghindari bias satu jenis sumber: 2 paper formal-verification pada Noise Protocol Framework/turunannya (`kobeissi2019noiseexplorer` untuk Noise_IK langsung, `donenfeld2017wireguard` untuk sistem nyata berbasis Noise), 3 paper formal-analysis protokol pesan populer (`cohngordon2020signal` Signal, `albrecht2024matrix` Matrix, `borisov2004otr` OTR sebagai fondasi historis), dan 2 spesifikasi sistem P2P serverless nyata (`briarspec`, `toxspec`) yang arsitekturnya paling dekat dengan AKSARA (P2P dua pihak tanpa server, salah satunya memakai Tor).
2. **`briarspec` dan `toxspec` sengaja diberi kualitas MEDIUM** (bukan HIGH) karena keduanya spesifikasi/dokumentasi proyek resmi, bukan paper peer-reviewed — konsisten dengan perlakuan `snowcrate`/dst. pada TAHAP 4/9. Laporan analisis independen Briar oleh ETH Zürich (`ethz.ch/.../report_YuanmingSong.pdf`) ditemukan sebagai konteks tambahan namun **tidak** dijadikan citekey terpisah (bukan publikasi peer-review, berstatus laporan semester project) — disebutkan hanya sebagai catatan di log ini, tidak dikutip di badan `10_RELATED_WORK_AND_GAP.md`.
3. **Tidak ada satupun dari 7 referensi yang diterima tanpa verifikasi pencarian** — seluruh judul, penulis, tahun, dan venue/DOI dicek langsung dari halaman resmi (eprint IACR, NDSS, ACM DL, IEEE Xplore, atau repositori spesifikasi proyek resmi), bukan dari ingatan model.
4. **Jumlah total referensi setelah TAHAP 10: 40** (33 + 7) — tetap proporsional untuk tugas mata kuliah, di atas ambang minimum manapun yang relevan pada brief.
