# SESSION 4 HANDOFF

Status sesi: TAHAP 8, 10, 11 selesai penuh. TAHAP 12 selesai **partial** (build+verifikasi fungsi selesai; capture screenshot TUI aktual tetap `MANUAL_USER_ACTION_REQUIRED`, tidak menghalangi `ready_for_codex`). TAHAP 1-7 dan 9 tidak diulang.

## Output Selesai

- `docs/mini-ta/01-claude-preparation/09_SCOPE_AND_TEAM_PLAN.md` — fokus utama mini-TA (Noise_IK + key lifecycle + threat model sebagai satu rangkaian protokol), 3 rumusan masalah, 3 tujuan, 3 kontribusi utama, batasan penelitian, luaran, 3 alternatif judul (rekomendasi judul #3), pembagian 3 anggota berbasis struktur modul aktual (bukan kategori generik brief).
- `docs/mini-ta/01-claude-preparation/10_RELATED_WORK_AND_GAP.md` — 7 penelitian/sistem terkait (Noise Explorer, Signal formal analysis, WireGuard, OTR, Matrix formal analysis, Briar spec, Tox spec), tabel perbandingan lengkap, 5 gap (G1-G5) dibingkai sebagai "belum ditemukan pada sumber ditinjau" (bukan klaim novelty absolut).
- `docs/mini-ta/01-claude-preparation/11_FIGURE_MANIFEST.md` + `diagrams/src/*.mmd` (7 file) + `diagrams/rendered/{svg,png}/*` (7×2 file) — diagram konteks, arsitektur komponen, arsitektur kriptografi (CORE-1..7), sequence proses utama, sequence handshake Noise_IK (formalisasi §5.1 ASCII), state siklus hidup kunci (formalisasi §8 ASCII), format paket/pesan. Seluruh render sukses (`mmdc -b white -s 2`, exit 0), diverifikasi visual untuk 4 dari 7 diagram (detail di manifest §Ringkasan Confidence).
- `docs/mini-ta/01-claude-preparation/screenshots/STATUS.md` — dokumentasi verifikasi `cargo build --release` (bersih, 0 warning/error, commit `450d484`) dan verifikasi fungsi non-interaktif via `aksara id --offline` (generate/unseal-deterministik/reject-passphrase-salah, seluruhnya cocok `07_KEY_LIFECYCLE.md` §3.2/§3.4). Instruksi lengkap capture manual untuk pengguna (2-4 screenshot, aturan keamanan data dummy).
- `references/REFERENCES.bib` — ditambah 7 entry baru (`kobeissi2019noiseexplorer`, `cohngordon2020signal`, `donenfeld2017wireguard`, `borisov2004otr`, `albrecht2024matrix`, `briarspec`, `toxspec`), total sekarang **40 entry**.
- `references/REFERENCE_MATRIX.md`, `references/ANNOTATED_BIBLIOGRAPHY.md`, `references/MCP_RESEARCH_LOG.md` — seluruhnya disinkronkan dengan 7 entry baru (baris tabel, anotasi, dan jejak pencarian §SESSION 4).
- `PROGRESS.md` — diperbarui 4 kali (checkpoint tiap TAHAP: 8, 10, 11, 12) plus sinkronisasi akhir sesi (tabel sprint, keputusan penting baru poin 5-6, next action).
- `docs/mini-ta/WORKFLOW_STATE.yaml` — `current_session: 5`, `latest_completed_stage: 12`, `latest_handoff` → file ini, `session_4.status: DONE`, `session_5.status: READY`, `next_action: testing_and_codex_handoff`.
- `docs/mini-ta/PROJECT_MEMORY.md` — akan diperbarui HANYA jika ada fakta stabil baru (lihat bagian bawah handoff ini, dilakukan setelah handoff ini ditulis).

## Scope yang Dipakai

- Ground truth utama sesi ini: `06_PROTOCOL_SPECIFICATION.md`, `07_KEY_LIFECYCLE.md`, `08_THREAT_MODEL.md` (TAHAP 5-7, dibaca ulang penuh sesuai instruksi user — bukan hanya ringkasan `PROJECT_MEMORY.md`), plus `CLAUDE_PREPARATION_BRIEF.md` penuh (17 TAHAP) untuk memastikan format tabel/struktur setiap TAHAP sesuai spesifikasi asli.
- Tidak ada pembacaan ulang source code `.rs` untuk TAHAP 8/10/11 — seluruh klaim bersumber dari dokumen TAHAP 2-7 yang sudah diverifikasi. TAHAP 12 **mengecualikan** aturan ini secara sengaja: binary hasil `cargo build --release` dijalankan langsung (`aksara id --offline`) untuk mendapatkan verifikasi fungsi empiris segar, bukan hanya klaim dari pembacaan kode — dipilih karena TAHAP 12 secara eksplisit meminta "build+jalankan untuk verifikasi fungsi", bukan audit kode.
- MCP dipakai: 11 panggilan `you-search` (2 untuk klarifikasi Briar/Matrix tambahan, 9 untuk 7 kandidat related work TAHAP 10). Tidak ada MCP lain dipakai sesi ini, sesuai batasan CLAUDE.md ("gunakan MCP hanya untuk kebutuhan tahap aktif").

## Temuan yang Perlu Dibawa ke Tahap Berikutnya

1. **Referensi total sekarang 40 entry** (33 lama + 7 baru TAHAP 10) — TAHAP 13-17 (SESSION 5) harus memakai angka ini, jangan menghitung ulang dari 33.
2. **Build AKSARA (commit `450d484`) terverifikasi bersih** — `cargo build --release` 0 warning/0 error, binary `target/release/aksara.exe` masih ada di working tree bila belum dibersihkan. Fungsi generate/unseal/reject-passphrase-salah pada `aksara id --offline` sudah diverifikasi cocok dengan `07_KEY_LIFECYCLE.md`. Bila TAHAP 13 (rencana pengujian) SESSION 5 butuh contoh output nyata sebagai ilustrasi (bukan pengganti eksperimen terencana), subcommand ini bisa dipakai lagi tanpa build ulang.
3. **Screenshot TUI aktual TETAP belum ada** — `screenshots/STATUS.md` berisi instruksi lengkap capture manual untuk user (2-4 gambar, aturan keamanan). SESSION 5/TAHAP 17 (handoff Codex) harus mencantumkan status ini sebagai `blocking_issues` non-blocking di `HANDOFF_TO_CODEX.yaml`, BUKAN dianggap selesai.
4. **5 gap (G1-G5) di `10_RELATED_WORK_AND_GAP.md`** relevan langsung untuk TAHAP 15 (content pack BAB II kajian pustaka, BAB VI penutup/keterbatasan) — terutama G2 (ketiadaan rotasi kunci, sudah beririsan dengan T7 di threat model) dan G1 (ketiadaan verifikasi formal Noise_IK spesifik AKSARA).
5. **Judul rekomendasi TAHAP 8**: "Implementasi dan Evaluasi Keamanan Protokol Noise_IK, Manajemen Kunci, dan Threat Model pada Aplikasi Chat Terminal P2P Serverless AKSARA" (alternatif #3 di `09_SCOPE_AND_TEAM_PLAN.md` §7) — dipakai sebagai `recommended_title` acuan bila TAHAP 17 (`HANDOFF_TO_CODEX.yaml`) SESSION 5 membutuhkannya, kecuali kelompok/dosen pembimbing mengubahnya.
6. **Pembagian 3 anggota** (`09_SCOPE_AND_TEAM_PLAN.md` §8) sudah dipetakan ke modul konkret — dipakai sebagai basis `team.contribution_matrix` di TAHAP 17 tanpa perlu dirancang ulang.
7. **7 diagram** (`11_FIGURE_MANIFEST.md`) siap dipakai BAB IV pada TAHAP 15 — 4 dari 7 sudah diverifikasi visual penuh (FIG-03, 05, 06, 07), 3 lainnya (FIG-01, 02, 04) hanya dicek dimensi piksel (lihat confidence table manifest). Bila ada waktu di SESSION 5, verifikasi visual 3 diagram sisanya sebelum dipakai di dokumen final.
8. **Diagram topologi pengujian sengaja tidak dibuat** sesi ini (menunggu `12_TEST_PLAN.md`) — TAHAP 13 SESSION 5 sebaiknya mempertimbangkan menambah diagram ke-8 setelah skenario pengujian final, atau eksplisit memutuskan tidak perlu (tetap dalam rentang 5-8 diagram yang disyaratkan brief).

## Instruksi Sesi Berikutnya (SESSION 5 — TAHAP 13, 14, 15, 16, 17)

1. Mulai dari `PROGRESS.md`, lalu file ini, lalu `09_SCOPE_AND_TEAM_PLAN.md`/`10_RELATED_WORK_AND_GAP.md`/`11_FIGURE_MANIFEST.md`/`screenshots/STATUS.md` sebagai ground truth baru.
2. Jangan mengulang TAHAP 1-12 (audit, normalisasi, justifikasi, riset referensi, protokol, key lifecycle, threat model, scope/tim, related work, diagram, build/screenshot) kecuali ada kontradiksi terdokumentasi.
3. **TAHAP 13 (rencana pengujian)** → `12_TEST_PLAN.md`. 3-6 kelompok eksperimen realistis, JANGAN membuat hasil eksperimen (rencana saja). Buat juga `docs/mini-ta/02-experiment-data/EXPERIMENT_RESULT_TEMPLATE.csv`.
4. **TAHAP 14 (tabel)** → `13_TABLE_MANIFEST.md` + data di `tables/` (CSV/Markdown).
5. **TAHAP 15 (content pack per BAB)** → `14_CHAPTER_CONTENT_PACK.md`. BAB V hanya boleh diisi setelah data eksperimen tersedia (kemungkinan besar tetap `WAITING_FOR_EXPERIMENT` pada sesi ini kecuali eksperimen TAHAP 13 sempat dijalankan). BAB VI tidak boleh berisi kesimpulan hasil sebelum BAB V selesai.
6. **TAHAP 16 (peta klaim)** → `15_CLAIM_EVIDENCE_CITATION_MAP.md`.
7. **TAHAP 17 (handoff Codex)** → `HANDOFF_TO_CODEX.yaml` — set `ready_for_codex` sesuai 17 syarat quality gate `CLAUDE_PREPARATION_BRIEF.md`, cantumkan screenshot capture sebagai `blocking_issues` non-blocking.
8. Referensi baru (bila dibutuhkan TAHAP 13+): tambahkan ke `references/REFERENCES.bib` yang sudah ada (40 entry) dan `references/REFERENCE_MATRIX.md` — **jangan** membuat file bibliografi terpisah.
9. Update `PROGRESS.md` di checkpoint tengah (tiap TAHAP selesai), jangan tunggu akhir sesi.
