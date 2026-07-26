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

- TAHAP 1 s.d. 11 berstatus `DONE`; TAHAP 12 berstatus `DONE` partial (build+verifikasi fungsi selesai, capture screenshot TUI aktual `MANUAL_USER_ACTION_REQUIRED`, tidak menghalangi `ready_for_codex`) — seluruhnya SESSION 1-4 selesai.
- Audit codebase menghasilkan 259 klaim final.
- Audit implementasi kriptografi menghasilkan 36 entry, dikonsolidasi ke 7 komponen inti CORE-1..7.
- Spesifikasi protokol (`06_PROTOCOL_SPECIFICATION.md`), key lifecycle (`07_KEY_LIFECYCLE.md`), threat model (`08_THREAT_MODEL.md`), scope & tim (`09_SCOPE_AND_TEAM_PLAN.md`), related work & gap (`10_RELATED_WORK_AND_GAP.md`), dan figure manifest (`11_FIGURE_MANIFEST.md`) sudah tersedia sebagai ground truth untuk sesi berikutnya — jangan diulang tanpa kontradiksi spesifik yang terdokumentasi.
- Referensi terverifikasi total **40 entry** (`references/REFERENCES.bib`) — 33 dari TAHAP 4/9/SESSION 3, 7 tambahan related work TAHAP 10/SESSION 4.
- `cargo build --release` terverifikasi bersih (0 warning/0 error) pada commit `450d484` (2026-07-26) — detail di `01-claude-preparation/screenshots/STATUS.md`. Jangan mengulang klaim ini sebagai "baru diverifikasi" pada sesi mendatang tanpa build ulang.
- Tahap aktif berikutnya adalah TAHAP 13 (rencana pengujian, SESSION 5). Jangan mengulang tahap `DONE` tanpa kontradiksi spesifik yang terdokumentasi.
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

## Workflow Sesi Lanjutan (semula tiga sesi, SESSION 5 dipecah jadi 5A/5B)

- Sisa persiapan mini-TA dibagi menjadi sesi lanjutan berurutan: SESSION 3, SESSION 4, SESSION 5A, SESSION 5B.
- SESSION 3 — Protocol and Security Model: TAHAP 5 (spesifikasi protokol), TAHAP 6 (key lifecycle), TAHAP 7 (threat model). Status: `DONE`.
- SESSION 4 — Scope, Related Work, and Figures: TAHAP 8 (scope & pembagian tim), TAHAP 10 (related work & gap), TAHAP 11 (diagram teknis), TAHAP 12 (status screenshot aplikasi). Status: `DONE` (TAHAP 12 partial, tidak menghalangi lanjut).
- SESSION 5A — Testing Plan and Tables: TAHAP 13 (rencana pengujian), TAHAP 14 (tabel). Status: `READY`.
- SESSION 5B — Chapter Content Pack and Codex Handoff: TAHAP 15 (content pack per BAB — tahap terberat sprint ini), TAHAP 16 (peta klaim-evidence-citation), TAHAP 17 (handoff final Codex). Status: `BLOCKED_BY_SESSION_5A`.
- Pemecahan SESSION 5 diminta user di akhir SESSION 4 (kuota sesi 5-jam tersisa ~50%) — TAHAP 15 tidak digabung dengan tahap lain karena berisiko kepotong kuota di tengah kerja.
- `docs/mini-ta/WORKFLOW_STATE.yaml` adalah state mesin lintas Claude dan Codex untuk workflow ini — baca dan perbarui di setiap sesi berikutnya bersama `PROGRESS.md`.

## Wajib Baca Saat Memulai

1. `docs/mini-ta/PROJECT_MEMORY.md`
2. `docs/mini-ta/01-claude-preparation/PROGRESS.md`
3. `docs/mini-ta/01-claude-preparation/SESSION_4_HANDOFF.md` atau handoff sesi yang lebih baru
4. Deliverable tahap aktif — untuk TAHAP 13 (tahap berikutnya, SESSION 5): `09_SCOPE_AND_TEAM_PLAN.md`, `10_RELATED_WORK_AND_GAP.md`, `11_FIGURE_MANIFEST.md`, `screenshots/STATUS.md` sebagai ground truth, plus `06_PROTOCOL_SPECIFICATION.md`/`07_KEY_LIFECYCLE.md`/`08_THREAT_MODEL.md` bila relevan untuk merancang skenario pengujian
