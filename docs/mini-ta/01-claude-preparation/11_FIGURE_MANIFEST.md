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
