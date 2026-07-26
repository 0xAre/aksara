# PROGRESS — Persiapan Mini-TA AKSARA

Baca file ini DULU sebelum melanjutkan sesi. Sumber instruksi lengkap:
`docs/mini-ta/CLAUDE_PREPARATION_BRIEF.md` (17 TAHAP, aturan anti-fabrikasi, quality gate).
Update terakhir: TAHAP 5, 6, 7 (SESSION 3 — Protocol and Security Model) selesai. Sesi berikutnya (SESSION 4) mulai TAHAP 8 (scope & tim).

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
| 8 | Scope & tim | ⬜ PENDING | Output: `09_SCOPE_AND_TEAM_PLAN.md`. Nama anggota: TIDAK ADA sumber terkonfirmasi (cek 3 proposal CARAKA sibling folder, semua placeholder `[Nama X — TBD]`) → **pakai placeholder Anggota 1/2/3**, tidak perlu tanya user lagi soal ini |
| 9 | Riset referensi MCP | ✅ DONE | Digabung ke sesi TAHAP 4. 31 referensi terverifikasi (25 standar/primer, 6 dok. library) — lihat `references/REFERENCES.bib`, `REFERENCE_MATRIX.md`, `ANNOTATED_BIBLIOGRAPHY.md`, `MCP_RESEARCH_LOG.md`. `semantic-scholar` rate-limited setelah 1 query sukses; `tavily` gagal total (HTTP 432, kuota habis) — riset dialihkan penuh ke `ydc-server`(you-search) dengan domain filter resmi. Detail kendala di `MCP_RESEARCH_LOG.md`. |
| 10 | Related work & gap | ⬜ PENDING | Output: `10_RELATED_WORK_AND_GAP.md` |
| 11 | Diagram Mermaid | ⬜ PENDING | Output: `11_FIGURE_MANIFEST.md`. `mmdc` SUDAH DIPERBAIKI sesi ini (lihat Keputusan Penting) — render pipeline teruji OK |
| 12 | Screenshot aplikasi | 🔴 BLOCKED (bagian render), verifikasi fungsi bisa jalan | Tidak ada tool screenshot OS/terminal di environment ini. Build+run untuk verifikasi fungsi masih bisa. Pengambilan gambar aktual perlu user manual. TIDAK memblokir `ready_for_codex` (screenshot tak masuk 17 syarat quality gate) |
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
| 4 | 8, 10, 11, 12 | Scope, Related Work, and Figures (scope & tim, related work/gap, diagram, screenshot) | READY | `SESSION_4_HANDOFF.md` |
| 5 | 13, 14, 15, 16, 17 | Testing and Codex Handoff (rencana pengujian, tabel, content pack, peta klaim, handoff Codex) | BLOCKED_BY_SESSION_4 | `SESSION_5_HANDOFF.md` |

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
3. **Screenshot TAHAP 12** — sudah dilaporkan ke user sebagai blocking issue (tidak ada tool capture). User belum diminta konfirmasi lanjutan soal ini karena tidak menghalangi `ready_for_codex`. Cukup dokumentasikan di `14_OPEN_QUESTIONS.md`.
4. **Versi crate ground-truth** (dari `Cargo.lock`, dipakai konsisten di semua TAHAP kripto): `ed25519-dalek 2.2.0`, `x25519-dalek 2.0.1`, `snow 0.10.0`, `argon2 0.5.3`, `chacha20poly1305 0.10.1` (chacha20 0.10.0, poly1305 0.8.0, aead 0.5.2), `zeroize 1.9.0`, `rand 0.8.6`, `blake2 0.10.6`, `mdns-sd 0.20.0`, `arti-client/tor-hsservice/tor-cell 0.43.0`, `rustls 0.23.40`, `ring 0.17.14`, `tokio 1.52.3`, `ratatui 0.29.0`, `crossterm 0.29.0`.

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

1. Baca `docs/mini-ta/PROJECT_MEMORY.md`, lalu `SESSION_3_HANDOFF.md` (atau handoff sesi lebih baru), `06_PROTOCOL_SPECIFICATION.md`, `07_KEY_LIFECYCLE.md`, `08_THREAT_MODEL.md` sebagai ground truth SESSION 3.
2. Jangan mengulang audit codebase/kripto/normalisasi/justifikasi/riset referensi/spesifikasi protokol/key lifecycle/threat model kecuali ada klaim yang secara eksplisit perlu dikonfirmasi ulang.
3. Lanjut TAHAP 8 (scope & tim, `09_SCOPE_AND_TEAM_PLAN.md` — placeholder Anggota 1/2/3, JANGAN tanya user lagi), lalu TAHAP 10 (`10_RELATED_WORK_AND_GAP.md`), TAHAP 11 (`11_FIGURE_MANIFEST.md`, `mmdc` sudah berfungsi), TAHAP 12 (screenshot, sebagian BLOCKED — verifikasi fungsi build+run tetap bisa jalan). Penomoran file TAHAP 8+ SUDAH FINAL, lihat §0 Keputusan Penting.
4. Jika TAHAP 8+ membutuhkan referensi eksternal baru, tambahkan ke `references/REFERENCES.bib` yang sudah ada (33 entry per akhir SESSION 3, JANGAN membuat ulang dari nol).
5. `semantic-scholar` dan `tavily` sempat bermasalah sesi-sesi sebelumnya (rate-limit/kuota habis) — `ydc-server`(you-search) dengan `include_domains` terarah adalah fallback yang terbukti bekerja baik (dipakai lagi sukses di SESSION 3 untuk verifikasi `rfc6762`).
6. Update file ini setiap TAHAP selesai — jangan tunggu sampai akhir sesi.
