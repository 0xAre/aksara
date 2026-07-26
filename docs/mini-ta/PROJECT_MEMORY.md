# AKSARA Project Memory

Dokumen ini memuat fakta stabil lintas-agen, bukan log sesi.

## Identitas dan Konteks

- AKSARA adalah aplikasi chat P2P terminal serverless untuk komunikasi terenkripsi dua pihak tanpa server perantara.
- Implementasi utama menggunakan Rust 2021, Tokio, ratatui/crossterm, LAN dengan mDNS/TCP, dan Tor onion service.
- AKSARA bukan `CARAKA-APP` (proyek Android/Kotlin) dan bukan proyek terpisah `Caraka` (Rust/Tauri). Fakta ketiganya tidak boleh dicampur.
- Dokumen yang disusun adalah Tugas Akhir Mata Kuliah Implementasi Kriptografi, bukan skripsi atau TA individu.
- Pekerjaan dilakukan oleh tiga anggota. Nama tetap `Anggota 1`, `Anggota 2`, dan `Anggota 3` dengan status `NEEDS_CONFIRMATION`.
- Fokus akademik: menjelaskan implementasi dan memberikan justifikasi kriptografi yang faktual dengan scope proporsional untuk tugas mata kuliah.

## Status Stabil

- TAHAP 1, 2, dan 3 berstatus `DONE`.
- Audit codebase menghasilkan 259 klaim final.
- Audit implementasi kriptografi menghasilkan 36 entry.
- Tahap aktif berikutnya tetap TAHAP 4, normalisasi dan justifikasi kriptografi, disertai riset referensi yang diperlukan. Jangan mengulang tahap `DONE` tanpa kontradiksi spesifik yang terdokumentasi.
- Root repository telah diaudit; lima direktori hasil agen telah dikarantina secara non-destruktif. Lihat `ROOT_CLEANUP_AUDIT.md`.

## Versi Ground Truth

Versi yang telah dicatat dari `Cargo.lock`:

| Komponen | Versi |
|----------|-------|
| ed25519-dalek | 2.2.0 |
| x25519-dalek | 2.0.1 |
| snow | 0.10.0 |
| argon2 | 0.5.3 |
| chacha20poly1305 | 0.10.1 |
| chacha20 / poly1305 / aead | 0.10.0 / 0.8.0 / 0.5.2 |
| zeroize / rand / blake2 | 1.9.0 / 0.8.6 / 0.10.6 |
| mdns-sd | 0.20.0 |
| arti-client / tor-hsservice / tor-cell | 0.43.0 |
| rustls / ring | 0.23.40 / 0.17.14 |
| tokio / ratatui / crossterm | 1.52.3 / 0.29.0 / 0.29.0 |

## Tool dan Media

- `mmdc` tercatat sudah berfungsi dengan Chrome sistem dan `docs/mini-ta/puppeteer-config.json`.
- Perintah render: `mmdc -i <file>.mmd -o <out>.svg -p "docs/mini-ta/puppeteer-config.json" -b white`.
- Status screenshot TAHAP 12 yang tercatat: pengambilan gambar aktual belum tersedia dan memerlukan tindakan manual pengguna; verifikasi fungsi aplikasi tetap mungkin. Status ini tidak menghalangi quality gate `ready_for_codex`.

## Sumber Kebenaran dan Aturan Klaim

Urutan sumber kebenaran: source code aktual; `Cargo.toml` dan versi terverifikasi `Cargo.lock`; test/build output; evidence audit terverifikasi; dokumentasi proyek; proposal lama sebagai konteks historis; referensi eksternal hanya untuk teori.

- Klaim implementasi wajib memiliki path dan symbol.
- Klaim teori wajib memiliki sumber.
- Klaim hasil wajib memiliki data eksperimen.
- Jangan menyatakan fitur `IMPLEMENTED` hanya dari dokumentasi.
- Gunakan `NEEDS_CONFIRMATION` jika data tidak tersedia, dan bedakan status `IMPLEMENTED`, `PARTIAL`, `PLANNED`, `DOCUMENTED_ONLY`, `NOT_FOUND`, `INCONSISTENT`, serta `NEEDS_EXPERIMENT`.

## Wajib Baca Saat Memulai

1. `docs/mini-ta/PROJECT_MEMORY.md`
2. `docs/mini-ta/01-claude-preparation/PROGRESS.md`
3. `docs/mini-ta/01-claude-preparation/SESSION_1_HANDOFF.md` atau handoff sesi yang lebih baru
4. Deliverable tahap aktif, untuk tahap berikutnya `01_CODEBASE_AUDIT.md`, `02_CRYPTO_IMPLEMENTATION_AUDIT.md`, dan evidence matrix yang relevan
