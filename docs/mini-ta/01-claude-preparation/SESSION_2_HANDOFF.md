# SESSION 2 HANDOFF

Status sesi: TAHAP 4 (justifikasi kriptografi) selesai penuh, digabung dengan TAHAP 9 (riset referensi MCP) sesuai instruksi eksplisit sesi ini. TAHAP 1-3 tidak diulang.

## Output Selesai

- `docs/mini-ta/01-claude-preparation/03_CRYPTO_INVENTORY_NORMALIZED.md` — normalisasi 36 entry `CR-001`..`CR-036` ke 7 kategori (algoritma inti, key material, parameter, mekanisme protokol, kontrol nonkriptografis, helper, duplikasi), dikonsolidasi jadi 7 komponen inti `CORE-1`..`CORE-7`.
- `docs/mini-ta/01-claude-preparation/04_CRYPTOGRAPHIC_JUSTIFICATION.md` — justifikasi 15-poin per komponen inti (Noise_IK, X25519, ChaCha20-Poly1305, BLAKE2s, Argon2id, Ed25519, OsRng).
- `docs/mini-ta/01-claude-preparation/05_CRYPTO_ALTERNATIVE_COMPARISON.md` — perbandingan multi-kriteria (bukan hanya kecepatan) maksimal 2 alternatif per 7 fungsi utama.
- `docs/mini-ta/01-claude-preparation/references/REFERENCES.bib` — 31 entry BibTeX terverifikasi.
- `docs/mini-ta/01-claude-preparation/references/REFERENCE_MATRIX.md` — matrix Citekey/Referensi/Jenis/Klaim/Algoritma/Bab/Kualitas.
- `docs/mini-ta/01-claude-preparation/references/ANNOTATED_BIBLIOGRAPHY.md` — anotasi per sumber, dikelompokkan per komponen.
- `docs/mini-ta/01-claude-preparation/references/MCP_RESEARCH_LOG.md` — jejak pencarian lengkap + dokumentasi kendala MCP.
- `PROGRESS.md` — diperbarui dua kali (segera setelah normalisasi, dan di akhir sesi).

## Scope Yang Dipakai

- Ground truth implementasi: 36 entry `02_CRYPTO_IMPLEMENTATION_AUDIT.md` (TAHAP 3, sudah `DONE`). TIDAK ada audit ulang source code — hanya 2 verifikasi silang targeted terhadap `evidence/CODE_EVIDENCE_MATRIX.md` (CB-084 untuk konfirmasi ketiadaan sign/verify Ed25519; pengecekan `*proposal*` untuk konfirmasi tidak ada dokumen proposal kripto terpisah).
- Referensi eksternal: 31 sumber (25 standar/RFC/NIST/spesifikasi resmi/paper primer peer-reviewed, 6 dokumentasi library Rust) — jauh melebihi target 15-25 karena TAHAP 9 digabung dan mencakup referensi pembanding untuk TAHAP 5 nanti (bukan hanya untuk primitif yang benar-benar dipakai).
- MCP dipakai: `semantic-scholar` (1 query sukses lalu rate-limited seterusnya), `ydc-server`/you-search (sumber utama, 26 query sukses dengan `include_domains` diarahkan ke domain resmi), `tavily` (gagal total, HTTP 432/kuota habis, tidak dipakai). Detail lengkap di `references/MCP_RESEARCH_LOG.md`.

## Temuan Yang Perlu Dibawa Ke Tahap Berikutnya

1. **Ed25519 di AKSARA saat ini murni bahan fingerprint, BUKAN mekanisme tanda tangan aktif** — grep menyeluruh (CB-084) tidak menemukan pemanggilan `sign()`/`verify()`/`Signature` di `src/identity/*.rs`. Setiap pembahasan Ed25519 di BAB berikutnya (spesifikasi protokol, threat model) HARUS membedakan tegas properti algoritma EdDSA secara umum vs. apa yang benar-benar dipakai AKSARA saat ini.
2. **Noise_IK sub-mekanisme internal (hash transcript, HKDF) berconfidence LOW** — murni inferensi dari nama pattern string `Noise_IK_25519_ChaChaPoly_BLAKE2s`, tidak ada pemanggilan langsung di source aplikasi yang teraudit. Jangan overclaim "terverifikasi penuh" pada BAB manapun untuk bagian ini.
3. **ChaCha20-Poly1305 TIDAK misuse-resistant** — AKSARA mengandalkan nonce random 96-bit per operasi (bukan konstruksi misuse-resistant seperti AES-GCM-SIV). Ini sudah cukup untuk skala pemakaian personal tapi harus dicatat sebagai batasan desain yang sadar, bukan disembunyikan.
4. **Klaim timing Argon2id "~100ms" pada komentar kode TIDAK diverifikasi benchmark** dalam source yang diaudit — jangan kutip angka ini sebagai fakta terukur di BAB hasil/pengujian (TAHAP 13) tanpa benchmark aktual.
5. **Tidak ditemukan dokumen proposal kriptografi terpisah** untuk AKSARA di repository — sehingga tidak ada "konflik proposal vs implementasi" yang bisa dilaporkan pada `04_CRYPTOGRAPHIC_JUSTIFICATION.md`. Bila proposal ditemukan nanti (mis. dari anggota tim), bagian pembuka `04_CRYPTOGRAPHIC_JUSTIFICATION.md` WAJIB direvisi.
6. **31 referensi di `references/` sudah mencakup seluruh 7 komponen inti DAN alternatif pembandingnya** — TAHAP 5 (spesifikasi protokol), TAHAP 6 (key lifecycle), TAHAP 7 (threat model) kemungkinan besar bisa memakai ulang referensi yang sama tanpa riset MCP tambahan, KECUALI muncul kebutuhan spesifik baru (mis. referensi tentang mDNS security untuk membahas metadata leak LAN discovery, yang belum dicari sesi ini).
7. **Kendala MCP dicatat untuk sesi berikutnya**: `semantic-scholar` rate-limited (`retry_after: 60` konsisten gagal meski sudah menunggu beberapa menit — kemungkinan API key/kuota bersama terpakai penuh), `tavily` gagal total (HTTP 432). `ydc-server` (you-search) terbukti sebagai fallback yang andal dengan `include_domains` terarah ke domain resmi (`datatracker.ietf.org`, `csrc.nist.gov`, `docs.rs`, dst.) — pakai ini dulu jika `semantic-scholar`/`tavily` bermasalah lagi.

## Instruksi Sesi Berikutnya

1. Mulai dari `PROGRESS.md`, lalu file ini, lalu `03_CRYPTO_INVENTORY_NORMALIZED.md`, `04_CRYPTOGRAPHIC_JUSTIFICATION.md`, `05_CRYPTO_ALTERNATIVE_COMPARISON.md`.
2. Lanjutkan TAHAP 5 (spesifikasi protokol) — evidence dasar sudah tersedia lengkap di TAHAP 2/3/4, terutama untuk komponen handshake Noise_IK (CORE-1) dan alur `session/mod.rs::run_session` (CR-026/CR-027).
3. **Putuskan penomoran file di awal sesi**: brief asli (`CLAUDE_PREPARATION_BRIEF.md`) menomori TAHAP 5 sebagai `04_PROTOCOL_SPECIFICATION.md`, tapi sesi ini sudah memakai `03/04/05` untuk TAHAP 4 (normalisasi/justifikasi/perbandingan) sesuai instruksi eksplisit pengguna. Cek daftar file yang sudah ada di `01-claude-preparation/` sebelum menulis file baru, dan sesuaikan penomoran TAHAP 5 dst. secara konsisten (kemungkinan besar mulai dari `06_...`) — dokumentasikan keputusan ini di `PROGRESS.md` begitu diputuskan.
4. Jangan mengulang normalisasi/justifikasi/riset referensi kecuali ada klaim yang secara eksplisit perlu dikonfirmasi ulang.
5. Untuk referensi baru (bila dibutuhkan), tambahkan ke `references/REFERENCES.bib` yang sudah ada — jangan membuat file bibliografi baru terpisah.
