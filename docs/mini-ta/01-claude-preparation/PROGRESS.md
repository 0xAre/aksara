# PROGRESS — Persiapan Mini-TA AKSARA

Baca file ini DULU sebelum melanjutkan sesi. Sumber instruksi lengkap:
`docs/mini-ta/CLAUDE_PREPARATION_BRIEF.md` (17 TAHAP, aturan anti-fabrikasi, quality gate).
Update terakhir: TAHAP 8, 10, 11, 12 (SESSION 4 — Scope, Related Work, and Figures) selesai (TAHAP 12 partial — lihat baris tabel). Sesi berikutnya (SESSION 5) mulai TAHAP 13 (rencana pengujian).

## Status per TAHAP

| # | TAHAP | Status | Output |
|---|-------|--------|--------|
| 1 | Tool & MCP inventory | ✅ DONE | `00_TOOL_AND_MCP_INVENTORY.md` |
| 2 | Audit codebase | ✅ DONE | `01_CODEBASE_AUDIT.md` + `evidence/CODE_EVIDENCE_MATRIX.md` selesai. Matrix berisi 259 klaim final; verdict `CORRECTED` dipakai sebagai klaim final, verdict `REFUTED` di-drop. |
| 3 | Audit kriptografi | ✅ DONE | `02_CRYPTO_IMPLEMENTATION_AUDIT.md` selesai. Inventaris berisi 36 primitif/entry kripto dari field `primitives` raw JSON. |
| 4 | Justifikasi kriptografi | ✅ DONE | `03_CRYPTO_INVENTORY_NORMALIZED.md` (36 entry dikategorikan → 7 komponen inti CORE-1..7), `04_CRYPTOGRAPHIC_JUSTIFICATION.md` (15 poin/komponen), `05_CRYPTO_ALTERNATIVE_COMPARISON.md` (7 fungsi utama × maks 2 alternatif, multi-kriteria). |
| 5 | Spesifikasi protokol | ✅ DONE | `06_PROTOCOL_SPECIFICATION.md` selesai — alur invite/discovery/handshake Noise_IK (CR-007..011, CR-026/027)/transport session/framing, berbasis evidence TAHAP 2/3 (`session.json`, `crypto_handshake.json`, `transport_lan.json`, `transport_tor.json`) + justifikasi TAHAP 4. 2 referensi baru (`rfc6762`, `rfc6763`) ditambahkan untuk konteks mDNS. |
| 6 | Key lifecycle | ✅ DONE | `07_KEY_LIFECYCLE.md` selesai — generation/storage/usage/rotation/zeroization seluruh material kunci (identity, noise, vault, contacts-store), berbasis evidence `identity.json`/`contacts.json`/`main_and_error.json` TAHAP 2/3. Tidak ada referensi baru dibutuhkan. |
| 7 | Threat model | ✅ DONE | `08_THREAT_MODEL.md` selesai — trust boundary, aset, 5 model musuh (A1-A5), ancaman per komponen (invite/discovery/handshake/transport/vault/passphrase/Tor), risk register deskriptif T1-T7. Referensi `rfc6762`/`rfc6763` dipakai ulang dari TAHAP 5, tidak ada entry baru. |
| 8 | Scope & tim | ✅ DONE | `09_SCOPE_AND_TEAM_PLAN.md` selesai — fokus utama (Noise_IK + key lifecycle + threat model sebagai satu rangkaian protokol), 3 rumusan masalah/tujuan/kontribusi, batasan penelitian, 3 alternatif judul (rekomendasi #3), pembagian 3 anggota berbasis struktur modul aktual (identity+crypto/transport+session/contacts+tui+integrasi). Placeholder Anggota 1/2/3 dipakai, tidak ada pertanyaan baru ke user. |
| 9 | Riset referensi MCP | ✅ DONE | Digabung ke sesi TAHAP 4. 31 referensi terverifikasi (25 standar/primer, 6 dok. library) — lihat `references/REFERENCES.bib`, `REFERENCE_MATRIX.md`, `ANNOTATED_BIBLIOGRAPHY.md`, `MCP_RESEARCH_LOG.md`. `semantic-scholar` rate-limited setelah 1 query sukses; `tavily` gagal total (HTTP 432, kuota habis) — riset dialihkan penuh ke `ydc-server`(you-search) dengan domain filter resmi. Detail kendala di `MCP_RESEARCH_LOG.md`. |
| 10 | Related work & gap | ✅ DONE | `10_RELATED_WORK_AND_GAP.md` selesai — 7 referensi related work baru terverifikasi via `you-search` (Noise Explorer, Signal formal analysis, WireGuard, OTR, Matrix formal analysis, Briar spec, Tox spec), ditambahkan ke `references/REFERENCES.bib` (total 40), `REFERENCE_MATRIX.md`, `ANNOTATED_BIBLIOGRAPHY.md`, `MCP_RESEARCH_LOG.md`. 5 gap (G1-G5) diidentifikasi berbasis perbandingan langsung, dibingkai "belum ditemukan pada sumber ditinjau" (bukan "belum pernah diteliti"). |
| 11 | Diagram Mermaid | ✅ DONE | `11_FIGURE_MANIFEST.md` selesai — 7 diagram (`diagrams/src/*.mmd`, dirender ke `diagrams/rendered/{svg,png}/` via `mmdc -b white -s 2`): context, arsitektur komponen, arsitektur kriptografi (CORE-1..7), sequence proses utama, sequence handshake Noise_IK (basis §5.1 ASCII), state siklus hidup kunci (basis §8 ASCII), format paket/pesan. Diagram topologi pengujian sengaja tidak dibuat (menunggu `12_TEST_PLAN.md` SESSION 5). |
| 12 | Screenshot aplikasi | 🟡 PARTIAL — build+fungsi ✅ DONE, capture gambar 🔴 BLOCKED | Output: `screenshots/STATUS.md`. `cargo build --release` sukses (0 warning/error, commit `450d484`, aksara v0.2.1, binary 8,77MB). Verifikasi fungsi non-interaktif via `aksara id --offline`: generate identitas, unseal deterministik (invite/fingerprint identik), reject passphrase salah ("vault could not be opened") — seluruhnya cocok dokumentasi TAHAP 6/7. Screenshot TUI aktual tetap perlu tindakan manual user (tidak ada tool capture OS/terminal di environment agent). TIDAK memblokir `ready_for_codex`. |
| 13 | Rencana pengujian | ⬜ PENDING | Output: `12_TEST_PLAN.md` |
| 14 | Tabel | ⬜ PENDING | Output: `13_TABLE_MANIFEST.md` |
| 15 | Content pack per BAB | ⬜ PENDING | Output: `14_CHAPTER_CONTENT_PACK.md` |
| 16 | Peta klaim | ⬜ PENDING | Output: `15_CLAIM_EVIDENCE_CITATION_MAP.md` |
| 17 | Handoff Codex | ⬜ PENDING | Output: `HANDOFF_TO_CODEX.yaml` (tidak bernomor) |

## Sprint Tiga Sesi Berikutnya

State mesin lintas-agen untuk sprint ini: `docs/mini-ta/WORKFLOW_STATE.yaml`. Baca file itu di awal setiap sesi berikutnya bersama file ini.

| Session | Tahap | Fokus | Status | Handoff |
|---------|-------|-------|--------|---------|
| 3 | 5, 6, 7 | Protocol and Security Model (spesifikasi protokol, key lifecycle, threat model) | ✅ DONE | `SESSION_3_HANDOFF.md` |
| 4 | 8, 10, 11, 12 | Scope, Related Work, and Figures (scope & tim, related work/gap, diagram, screenshot) | ✅ DONE (TAHAP 12 partial, tidak menghalangi lanjut) | `SESSION_4_HANDOFF.md` |
| 5 | 13, 14, 15, 16, 17 | Testing and Codex Handoff (rencana pengujian, tabel, content pack, peta klaim, handoff Codex) | READY | `SESSION_5_HANDOFF.md` |

## Keputusan penting (jangan diulang tanya ke user)

0. **Penomoran file TAHAP 5+ digeser +2** — brief asli (`CLAUDE_PREPARATION_BRIEF.md`) menomori TAHAP 4 sebagai 1 file tunggal (`03_CRYPTOGRAPHIC_JUSTIFICATION.md`), tapi sesi TAHAP 4 aktual memakai 3 file (`03_CRYPTO_INVENTORY_NORMALIZED.md`, `04_CRYPTOGRAPHIC_JUSTIFICATION.md`, `05_CRYPTO_ALTERNATIVE_COMPARISON.md`) sesuai instruksi eksplisit pengguna. Untuk menghindari tabrakan nomor, SELURUH file TAHAP 5 s.d. TAHAP 16 digeser +2 dari nomor di brief. Pemetaan final:
   | TAHAP | Nama file di brief | Nama file final (dipakai) |
   |-------|---------------------|------------------------------|
   | 5 — Spesifikasi protokol | `04_PROTOCOL_SPECIFICATION.md` | **`06_PROTOCOL_SPECIFICATION.md`** |
   | 6 — Manajemen kunci | `05_KEY_LIFECYCLE.md` | **`07_KEY_LIFECYCLE.md`** |
   | 7 — Threat model | `06_THREAT_MODEL.md` | **`08_THREAT_MODEL.md`** |
   | 8 — Scope & tim | `07_SCOPE_AND_TEAM_PLAN.md` | **`09_SCOPE_AND_TEAM_PLAN.md`** |
   | 9 — Riset referensi | `references/*` (subfolder, tidak bernomor) | tidak berubah — sudah `DONE` |
   | 10 — Related work & gap | `08_RELATED_WORK_AND_GAP.md` | **`10_RELATED_WORK_AND_GAP.md`** |
   | 11 — Diagram | `09_FIGURE_MANIFEST.md` | **`11_FIGURE_MANIFEST.md`** |
   | 13 — Rencana pengujian | `10_TEST_PLAN.md` | **`12_TEST_PLAN.md`** |
   | 14 — Tabel | `11_TABLE_MANIFEST.md` | **`13_TABLE_MANIFEST.md`** |
   | 15 — Content pack per BAB | `12_CHAPTER_CONTENT_PACK.md` | **`14_CHAPTER_CONTENT_PACK.md`** |
   | 16 — Peta klaim | `13_CLAIM_EVIDENCE_CITATION_MAP.md` | **`15_CLAIM_EVIDENCE_CITATION_MAP.md`** |
   | 17 — Handoff Codex | `HANDOFF_TO_CODEX.yaml` | tidak berubah (tidak bernomor) |
1. **mmdc diperbaiki** — instalasi global `@mermaid-js/mermaid-cli` awalnya korup (node_modules kosong). User sudah **mengizinkan** `npm install -g @mermaid-js/mermaid-cli`. Sudah dijalankan dengan `PUPPETEER_SKIP_DOWNLOAD=true` (download Chromium bawaan gagal), lalu diarahkan ke Chrome sistem via config `docs/mini-ta/puppeteer-config.json` (`executablePath: C:\Program Files\Google\Chrome\Application\chrome.exe`). Diverifikasi render SVG+PNG sukses (exit 0). **Cara pakai untuk TAHAP 11:** `mmdc -i <file>.mmd -o <out>.svg -p "docs/mini-ta/puppeteer-config.json" -b white` (jalankan dari root repo, sesuaikan path relatif).
2. **Nama anggota kelompok** — tidak ada nama asli di manapun (proposal CARAKA lama semua placeholder). Sudah diputuskan pakai placeholder Anggota 1/2/3 di TAHAP 8, ditandai `NEEDS_CONFIRMATION` di handoff akhir. Jangan tanya user lagi soal ini.
3. **Screenshot TAHAP 12** — build+verifikasi fungsi SUDAH selesai SESSION 4 (`cargo build --release` bersih, `aksara id --offline` diverifikasi generate/unseal/reject-passphrase-salah — detail `screenshots/STATUS.md`). Capture gambar TUI aktual TETAP perlu tindakan manual user (tidak ada tool capture OS/terminal di environment agent). Tidak menghalangi `ready_for_codex`. Dokumentasikan status ini juga di `14_OPEN_QUESTIONS.md` bila dibuat TAHAP 15/17.
4. **Versi crate ground-truth** (dari `Cargo.lock`, dipakai konsisten di semua TAHAP kripto): `ed25519-dalek 2.2.0`, `x25519-dalek 2.0.1`, `snow 0.10.0`, `argon2 0.5.3`, `chacha20poly1305 0.10.1` (chacha20 0.10.0, poly1305 0.8.0, aead 0.5.2), `zeroize 1.9.0`, `rand 0.8.6`, `blake2 0.10.6`, `mdns-sd 0.20.0`, `arti-client/tor-hsservice/tor-cell 0.43.0`, `rustls 0.23.40`, `ring 0.17.14`, `tokio 1.52.3`, `ratatui 0.29.0`, `crossterm 0.29.0`.
5. **`cargo build --release` diverifikasi SESSION 4** (commit `450d484`, 2026-07-26) — bersih 0 warning/0 error, binary `target/release/aksara.exe` 8,77MB, waktu build 9 menit (dependency Tor berat pada build pertama). Subcommand `aksara id --vault <path> --offline` (tidak butuh TUI interaktif) dipakai untuk verifikasi fungsi generate/unseal/reject-passphrase-salah — cocok `07_KEY_LIFECYCLE.md` §3.2/§3.4. Kalau perlu verifikasi ulang cepat di sesi depan, pakai subcommand ini dulu sebelum mencoba menjalankan TUI penuh (yang tidak bisa di-capture agent).
6. **Referensi total sekarang 40 entry** (33 dari TAHAP 4/9/SESSION 3 + 7 related work TAHAP 10 SESSION 4) — `references/REFERENCES.bib`/`REFERENCE_MATRIX.md`/`ANNOTATED_BIBLIOGRAPHY.md` sudah sinkron. Jangan hitung ulang dari 33 di sesi berikutnya.

## Data mentah TAHAP 2+3 (audit codebase + kripto)

Dihasilkan via Workflow (`wf_949a0769-7ab`, 16 agent: 8 ekstraksi + 8 verifikasi independen per modul, semua sukses, 0 error). Disalin permanen ke:

```
docs/mini-ta/01-claude-preparation/evidence/_raw-audit-json/
├── identity.json          (35 claims, 7 primitif)
├── crypto_handshake.json  (24 claims, 6 primitif)
├── transport_lan.json     (42 claims, 1 primitif)
├── transport_tor.json     (20 claims, 1 primitif)
├── session.json           (33 claims, 3 primitif)
├── contacts.json          (31 claims, 6 primitif)
├── tui.json                (40 claims, 6 primitif)
└── main_and_error.json    (30 claims, 6 primitif)
```

Tiap file berisi `{module, extracted: {claims[], primitives[]}, verified: {verified_claims[], verified_primitives[]}}`.
**Ini bukan deliverable final** — tapi sumber evidence yang sudah diverifikasi untuk menulis `01_CODEBASE_AUDIT.md`, `evidence/CODE_EVIDENCE_MATRIX.md`, `02_CRYPTO_IMPLEMENTATION_AUDIT.md`. Aman dibaca ulang kapan saja (masing-masing 23-47KB, di bawah limit baca file).

Transcript lengkap workflow (kalau perlu re-cek reasoning agent): `C:\Users\LENOVO\.claude\projects\E--Project-APP-AKSARA\9a01efa0-903c-4657-954e-0983b77c6759\subagents\workflows\wf_949a0769-7ab\journal.jsonl`

## Memory Bersama dan Housekeeping Root

- Root repository telah diaudit pada 2026-07-26.
- Lima artefak abnormal telah dikarantina secara non-destruktif; tidak ada item `NEEDS_REVIEW` tersisa pada root saat validasi. Detail: `docs/mini-ta/ROOT_CLEANUP_AUDIT.md`.
- `AGENTS.md` telah dibuat sebagai instruksi dan memory bersama kanonis untuk Codex dan Claude Code.
- `CLAUDE.md` sekarang mengimpor `AGENTS.md` sebagai adapter Claude Code.
- `docs/mini-ta/PROJECT_MEMORY.md` telah dibuat sebagai ringkasan fakta stabil lintas-agen.
- Aturan filesystem lintas-agen telah aktif: output mini-TA berada di bawah `docs/mini-ta/`, path harus pendek dan deterministik, serta artefak root wajib dikarantina.
- TAHAP 1, 2, dan 3 tetap `DONE`. Tahap berikutnya tetap TAHAP 4 dan riset referensi yang diperlukan; tidak ada status tahap lain yang diubah oleh housekeeping ini.

## Next action kalau lanjut sesi baru

1. Baca `docs/mini-ta/PROJECT_MEMORY.md`, lalu `SESSION_4_HANDOFF.md` (atau handoff sesi lebih baru), `09_SCOPE_AND_TEAM_PLAN.md`, `10_RELATED_WORK_AND_GAP.md`, `11_FIGURE_MANIFEST.md`, `screenshots/STATUS.md` sebagai ground truth SESSION 4.
2. Jangan mengulang audit codebase/kripto/normalisasi/justifikasi/riset referensi/spesifikasi protokol/key lifecycle/threat model/scope-tim/related-work/diagram kecuali ada klaim yang secara eksplisit perlu dikonfirmasi ulang.
3. Lanjut TAHAP 13 (rencana pengujian, `12_TEST_PLAN.md` — 3-6 kelompok eksperimen, JANGAN membuat hasil, hanya rencana + template CSV `docs/mini-ta/02-experiment-data/EXPERIMENT_RESULT_TEMPLATE.csv`), lalu TAHAP 14 (`13_TABLE_MANIFEST.md`), TAHAP 15 (`14_CHAPTER_CONTENT_PACK.md`, BAB I-VI), TAHAP 16 (`15_CLAIM_EVIDENCE_CITATION_MAP.md`), TAHAP 17 (`HANDOFF_TO_CODEX.yaml`). Penomoran file SUDAH FINAL, lihat §0 Keputusan Penting.
4. Subcommand `aksara id --vault <path> --offline` (binary hasil build SESSION 4 masih valid di `target/release/aksara.exe` bila belum dibersihkan) bisa dipakai lagi untuk verifikasi cepat tanpa build ulang, bila TAHAP 13 butuh contoh output nyata sebagai evidence tambahan (bukan pengganti eksperimen terencana).
5. Jika TAHAP 13+ membutuhkan referensi eksternal baru, tambahkan ke `references/REFERENCES.bib` yang sudah ada (40 entry per akhir SESSION 4, JANGAN membuat ulang dari nol).
6. `semantic-scholar` dan `tavily` bermasalah sejak sesi-sesi sebelumnya (rate-limit/kuota habis) — `ydc-server`(you-search) dengan `include_domains`/query spesifik terarah adalah fallback yang terbukti bekerja baik di SESSION 3 dan SESSION 4.
7. Update file ini setiap TAHAP selesai — jangan tunggu sampai akhir sesi.
