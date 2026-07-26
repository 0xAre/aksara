# PROGRESS — Persiapan Mini-TA AKSARA

Baca file ini DULU sebelum melanjutkan sesi. Sumber instruksi lengkap:
`docs/mini-ta/CLAUDE_PREPARATION_BRIEF.md` (17 TAHAP, aturan anti-fabrikasi, quality gate).
Update terakhir: TAHAP 4 dan TAHAP 9 (riset referensi, digabung) selesai. Sesi berikutnya mulai TAHAP 5 (spesifikasi protokol).

## Status per TAHAP

| # | TAHAP | Status | Output |
|---|-------|--------|--------|
| 1 | Tool & MCP inventory | ✅ DONE | `00_TOOL_AND_MCP_INVENTORY.md` |
| 2 | Audit codebase | ✅ DONE | `01_CODEBASE_AUDIT.md` + `evidence/CODE_EVIDENCE_MATRIX.md` selesai. Matrix berisi 259 klaim final; verdict `CORRECTED` dipakai sebagai klaim final, verdict `REFUTED` di-drop. |
| 3 | Audit kriptografi | ✅ DONE | `02_CRYPTO_IMPLEMENTATION_AUDIT.md` selesai. Inventaris berisi 36 primitif/entry kripto dari field `primitives` raw JSON. |
| 4 | Justifikasi kriptografi | ✅ DONE | `03_CRYPTO_INVENTORY_NORMALIZED.md` (36 entry dikategorikan → 7 komponen inti CORE-1..7), `04_CRYPTOGRAPHIC_JUSTIFICATION.md` (15 poin/komponen), `05_CRYPTO_ALTERNATIVE_COMPARISON.md` (7 fungsi utama × maks 2 alternatif, multi-kriteria). |
| 5 | Spesifikasi protokol | ⬜ PENDING | Butuh #2+#3 |
| 6 | Key lifecycle | ⬜ PENDING | Butuh #2+#3 |
| 7 | Threat model | ⬜ PENDING | Butuh #2+#3 |
| 8 | Scope & tim | ⬜ PENDING | Nama anggota: TIDAK ADA sumber terkonfirmasi (cek 3 proposal CARAKA sibling folder, semua placeholder `[Nama X — TBD]`) → **pakai placeholder Anggota 1/2/3**, tidak perlu tanya user lagi soal ini |
| 9 | Riset referensi MCP | ✅ DONE | Digabung ke sesi TAHAP 4. 31 referensi terverifikasi (25 standar/primer, 6 dok. library) — lihat `references/REFERENCES.bib`, `REFERENCE_MATRIX.md`, `ANNOTATED_BIBLIOGRAPHY.md`, `MCP_RESEARCH_LOG.md`. `semantic-scholar` rate-limited setelah 1 query sukses; `tavily` gagal total (HTTP 432, kuota habis) — riset dialihkan penuh ke `ydc-server`(you-search) dengan domain filter resmi. Detail kendala di `MCP_RESEARCH_LOG.md`. |
| 10 | Related work & gap | ⬜ PENDING | |
| 11 | Diagram Mermaid | ⬜ PENDING | `mmdc` SUDAH DIPERBAIKI sesi ini (lihat Keputusan Penting) — render pipeline teruji OK |
| 12 | Screenshot aplikasi | 🔴 BLOCKED (bagian render), verifikasi fungsi bisa jalan | Tidak ada tool screenshot OS/terminal di environment ini. Build+run untuk verifikasi fungsi masih bisa. Pengambilan gambar aktual perlu user manual. TIDAK memblokir `ready_for_codex` (screenshot tak masuk 17 syarat quality gate) |
| 13 | Rencana pengujian | ⬜ PENDING | |
| 14 | Tabel | ⬜ PENDING | |
| 15 | Content pack per BAB | ⬜ PENDING | |
| 16 | Peta klaim | ⬜ PENDING | |
| 17 | Handoff Codex | ⬜ PENDING | |

## Keputusan penting (jangan diulang tanya ke user)

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

1. Baca `docs/mini-ta/PROJECT_MEMORY.md`, lalu `SESSION_2_HANDOFF.md` (atau handoff sesi lebih baru), `03_CRYPTO_INVENTORY_NORMALIZED.md`, `04_CRYPTOGRAPHIC_JUSTIFICATION.md`, `05_CRYPTO_ALTERNATIVE_COMPARISON.md`.
2. Jangan mengulang audit codebase/kripto/normalisasi/justifikasi/riset referensi kecuali ada klaim yang secara eksplisit perlu dikonfirmasi ulang.
3. Lanjut TAHAP 5: spesifikasi protokol (`docs/mini-ta/01-claude-preparation/04_PROTOCOL_SPECIFICATION.md` per penomoran brief asli — cek penomoran final terhadap file yang sudah ada di folder ini sebelum menulis, karena TAHAP 4 sesi ini memakai 3 file `03/04/05` sehingga penomoran brief asli untuk TAHAP 5 dst. kemungkinan perlu digeser +1 atau disesuaikan; putuskan penomoran definitif di awal sesi TAHAP 5 dan catat keputusannya di sini).
4. Jika TAHAP 5+ membutuhkan referensi eksternal baru, tambahkan ke `references/` yang sudah ada (JANGAN membuat ulang dari nol) — 31 referensi TAHAP 4/9 sudah mencakup 7 komponen kripto inti; TAHAP 5 (protokol) dan TAHAP 6/7 (key lifecycle/threat model) kemungkinan besar cukup memakai ulang referensi yang sama.
5. `semantic-scholar` dan `tavily` sempat bermasalah (rate-limit/kuota habis) sesi ini — coba lagi di sesi baru (kuota mungkin sudah reset), tapi jangan blocking: `ydc-server`(you-search) dengan `include_domains` terarah adalah fallback yang terbukti bekerja baik.
6. Update file ini setiap TAHAP selesai — jangan tunggu sampai akhir sesi.
