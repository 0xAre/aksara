# Tabel 2 — Kebutuhan Non-Fungsional

Diturunkan dari properti keamanan/arsitektur yang **sudah teraudit** pada `04_CRYPTOGRAPHIC_JUSTIFICATION.md`, `07_KEY_LIFECYCLE.md`, `08_THREAT_MODEL.md`. Kolom "Tingkat Pemenuhan" memakai status audit (bukan skor kuantitatif) untuk menghindari overclaim.

| ID | Kebutuhan Non-Fungsional | Deskripsi | Evidence | Tingkat Pemenuhan |
|---|---|---|---|---|
| NFR-01 | Confidentiality (kerahasiaan) | Pesan sesi, vault identitas, dan contact store dienkripsi ChaCha20-Poly1305 (AEAD) | CR-001/008/013, `04_CRYPTOGRAPHIC_JUSTIFICATION.md` CORE-3 | IMPLEMENTED (HIGH untuk vault/contact store, MEDIUM untuk transport Noise — nonce internal `snow`) |
| NFR-02 | Integrity (integritas pesan/data) | Tag Poly1305 128-bit mendeteksi modifikasi ciphertext pada seluruh instance AEAD | CR-001/008/013, `04_CRYPTOGRAPHIC_JUSTIFICATION.md` CORE-3 poin 2 | IMPLEMENTED |
| NFR-03 | Authentication (autentikasi identitas peer) | Verifikasi static key X25519 dalam Noise_IK untuk kontak yang sudah dikenal, fail-closed pada ketidakcocokan | `session/mod.rs:145-151`, `06_PROTOCOL_SPECIFICATION.md` §5.2 | PARTIAL — HIGH untuk kontak dikenal; **TIDAK ADA** verifikasi untuk kontak baru (`peer_noise_pk=None`), lihat T1 `08_THREAT_MODEL.md` |
| NFR-04 | Portabilitas lintas platform | Binary didistribusikan untuk Windows, Linux, macOS Apple Silicon | `README.md:52-54` (CB-002), Rust edition 2021 | DOCUMENTED_ONLY (klaim README, terverifikasi build Windows SESSION 4) |
| NFR-05 | Efisiensi sumber daya (memory-bounded KDF) | Argon2id dibatasi 19 MiB memori per operasi seal/unseal, bukan tak terbatas | CR-014, `04_CRYPTOGRAPHIC_JUSTIFICATION.md` CORE-5 poin 9 | IMPLEMENTED |
| NFR-06 | Ketersediaan/resiliensi transport | Strategi LAN-first dengan fallback Tor otomatis bila LAN gagal dan Tor tersedia | `transport/mod.rs:118-172`, `06_PROTOCOL_SPECIFICATION.md` §4.1 | IMPLEMENTED |
| NFR-07 | Data lokal tanpa server (serverless) | Tidak ada penyimpanan data pengguna di server/pihak ketiga manapun — seluruh state (vault, kontak) lokal di disk pengguna | `README.md:23` (CB-001), arsitektur P2P `06_PROTOCOL_SPECIFICATION.md` §1 | IMPLEMENTED |
| NFR-08 | Higiene rahasia di memori (zeroization) | Key material inti (`IdentityKey`, `NoiseKey`, `KeyBundle`, buffer vault) dibersihkan dari memori via `ZeroizeOnDrop`/`Zeroizing` saat drop | `keypair.rs:10,44,74-89`; `vault.rs:49-56,62,108` | PARTIAL — kuat pada tipe kunci inti, lemah pada boundary `session`/`handshake`/`contacts`/`main.rs` (`07_KEY_LIFECYCLE.md` §7.2) |
| NFR-09 | Ketiadaan mekanisme rotasi kunci | Tidak ada rotasi/revokasi otomatis untuk kunci identitas, Noise, maupun vault | `07_KEY_LIFECYCLE.md` §6, T7 `08_THREAT_MODEL.md` §6 | NOT_FOUND (dicatat sebagai keterbatasan desain M1 yang disengaja, bukan bug) |

## Catatan

NFR-03 dan NFR-09 sengaja dicantumkan sebagai kebutuhan yang **belum/tidak sepenuhnya terpenuhi** — bukan kesalahan penulisan tabel, melainkan bagian dari evaluasi jujur berbasis evidence sesuai aturan anti-overclaim `AGENTS.md`.

## Referensi

`04_CRYPTOGRAPHIC_JUSTIFICATION.md`, `06_PROTOCOL_SPECIFICATION.md`, `07_KEY_LIFECYCLE.md`, `08_THREAT_MODEL.md` (TAHAP 4-7).
