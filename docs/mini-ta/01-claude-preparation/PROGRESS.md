# PROGRESS — Persiapan Mini-TA AKSARA

Baca file ini DULU sebelum melanjutkan sesi. Sumber instruksi lengkap:
`docs/mini-ta/CLAUDE_PREPARATION_BRIEF.md` (17 TAHAP, aturan anti-fabrikasi, quality gate).
Update terakhir: TAHAP 15 (partial, BAB I-IV), 16, 17 (SESSION 5B, menyambung SESSION 5A dalam sesi yang sama) selesai. Seluruh sprint persiapan mini-TA (TAHAP 1-17) kini selesai kecuali BAB V/VI content pack yang sengaja menunggu eksekusi eksperimen — lihat `SESSION_5B_HANDOFF.md` dan `HANDOFF_TO_CODEX.yaml`.

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
| 13 | Rencana pengujian | ✅ DONE | `12_TEST_PLAN.md` selesai — 5 kelompok eksperimen (EXP-01..05: vault correctness/rejection, handshake Noise_IK, transport sesi, invite/fingerprint/contact store, benchmark Argon2id+ciphertext expansion), memetakan 15 kandidat brief (2 ditandai N/A: KAT tidak ada test vector, modified-AD tidak berlaku karena AKSARA tidak memakai AAD). Seluruh 15 field wajib per eksperimen diisi. TIDAK ada hasil eksperimen dibuat — seluruh status `WAITING_FOR_EXPERIMENT`. Template: `docs/mini-ta/02-experiment-data/EXPERIMENT_RESULT_TEMPLATE.csv`. |
| 14 | Tabel | ✅ DONE | `13_TABLE_MANIFEST.md` selesai — 13 kategori tabel (fungsional, non-fungsional, stack teknologi, primitif kriptografi, justifikasi algoritma, perbandingan alternatif, format paket, lifecycle kunci, threat model, penelitian terkait, skenario pengujian, parameter evaluasi, pembagian tugas) di `tables/01`..`13_*.md`. Format Markdown (bukan CSV) karena isi sel didominasi kalimat panjang. Seluruh isi kompresi/reproduksi dari TAHAP 1-13 yang sudah diverifikasi, tidak ada klaim baru. |
| 15 | Content pack per BAB | 🟡 PARTIAL — BAB I-IV ✅ DONE, BAB V-VI 🔵 BLOCKED (sengaja, sesuai izin brief) | `14_CHAPTER_CONTENT_PACK.md`. BAB I (6 subbab), II (10 subbab), III (5 subbab), IV (7 subbab) selesai penuh — 13 field wajib per subbab, memenuhi Quality Gate poin 15 brief. BAB V distub (struktur rencana 3 subbab, status `WAITING_FOR_EXPERIMENT`) menunggu `12_TEST_PLAN.md` dieksekusi. BAB VI distub — 6.1 (kesimpulan) `WAITING_FOR_EXPERIMENT`, TAPI 6.2 (keterbatasan) dan 6.3 (saran) ditandai `READY_FOR_DRAFTING` (tidak bergantung eksperimen, bisa disusun penuh sesi berikutnya). |
| 16 | Peta klaim | ✅ DONE | `15_CLAIM_EVIDENCE_CITATION_MAP.md` — 81 Claim ID (CM-001..154) dikelompokkan 15 kategori (identitas/arsitektur, CORE-1..7, invite/discovery, transport sesi, key lifecycle, threat model T1-T7, related work gap G1-G5, FR/NFR, klaim performa). Format `Claim ID \| Klaim \| Evidence Code \| Referensi \| Data Eksperimen \| Bab \| Status` sesuai brief. Bagian "Klaim Kritis Anti-Overclaim" (5 item) ditambahkan sebagai pengingat prioritas untuk Codex. |
| 17 | Handoff Codex | ✅ DONE | `HANDOFF_TO_CODEX.yaml` — `ready_for_codex: YES_PARTIAL` (BAB I-IV siap, BAB V/VI menunggu eksperimen sesuai izin eksplisit brief). 17 syarat quality gate seluruhnya `met: true` (termasuk poin 17 — tidak ada kontradiksi kritis algoritma/nonce/key-management/format-protokol). 5 blocking issue dicatat non-blocking (BAB V/VI, screenshot, nama anggota, tabel 13/12). |

## Sprint Sesi Lanjutan (semula 3 sesi, SESSION 5 dipecah jadi 5A/5B)

State mesin lintas-agen untuk sprint ini: `docs/mini-ta/WORKFLOW_STATE.yaml`. Baca file itu di awal setiap sesi berikutnya bersama file ini.

| Session | Tahap | Fokus | Status | Handoff |
|---------|-------|-------|--------|---------|
| 3 | 5, 6, 7 | Protocol and Security Model (spesifikasi protokol, key lifecycle, threat model) | ✅ DONE | `SESSION_3_HANDOFF.md` |
| 4 | 8, 10, 11, 12 | Scope, Related Work, and Figures (scope & tim, related work/gap, diagram, screenshot) | ✅ DONE (TAHAP 12 partial, tidak menghalangi lanjut) | `SESSION_4_HANDOFF.md` |
| 5A | 13, 14 | Testing Plan and Tables (rencana pengujian, tabel) | ✅ DONE | `SESSION_5A_HANDOFF.md` |
| 5B | 15, 16, 17 | Chapter Content Pack and Codex Handoff (content pack per BAB, peta klaim, handoff Codex) | ✅ DONE (TAHAP 15 partial — BAB I-IV, BAB V/VI sengaja diblokir, tidak menghalangi `ready_for_codex`) | `SESSION_5B_HANDOFF.md` |

**Catatan pemecahan SESSION 5**: dipecah jadi 5A/5B atas permintaan user (kuota sesi 5-jam tersisa ~50% saat SESSION 4 selesai). TAHAP 15 (content pack 6 BAB) adalah tahap terberat di seluruh sprint — digabung dengan 13/14/16/17 berisiko kepotong di tengah kuota. 5A (ringan-menengah, mekanis) jadi sesi transisi; 5B (berat, sintesis lintas-dokumen) dapat sesi tersendiri dengan kuota penuh.

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
2. **Nama anggota kelompok** — ~~tidak ada nama asli di manapun~~ **DIPERBARUI 2026-07-27**: pengguna menunjuk `00-template/PROPOSAL CARAKA (2).docx` sebagai sumber identitas. Nama CONFIRMED: **Andika Aryansyach Fauzan (2322101878), Mahendra Nur Hidayat (2322101937), Rafi Putra Fadlurrahman (2322101963)**, program studi Rekayasa Sistem Kriptografi, Politeknik Siber dan Sandi Negara, tahun 2026. Catatan SESSION 2 ("proposal CARAKA semua placeholder") ternyata keliru — file itu memuat nama asli. Yang tersisa hanya pemetaan nama ke peran modul. Jangan tanya user lagi soal nama.
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

## Update Pasca-Sprint (2026-07-26, commit `3d22494`) — Eksekusi Eksperimen Parsial

`cargo test --release` dijalankan: **46/46 PASS, 0 FAIL**, mencakup penuh correctness+rejection EXP-01..04 (`12_TEST_PLAN.md` sudah diupdate, hasil di `02-experiment-data/EXPERIMENT_RESULTS_2026-07-26.csv`). **BELUM dijalankan** (kuota sesi habis): latensi handshake, overhead ciphertext byte, panjang invite, dan **seluruh EXP-05** (benchmark Argon2id — termasuk verifikasi klaim "~100ms" yang paling prioritas). BAB V/VI `14_CHAPTER_CONTENT_PACK.md` **BELUM diupdate** dengan hasil ini — masih perlu EXP-05 dan 3 metrik sisa sebelum BAB V ditulis penuh.

**Next action paling prioritas sesi berikutnya**: jalankan EXP-05 (Argon2id timing, 30 cold-start run) — satu-satunya klaim performa eksplisit yang belum diverifikasi di seluruh sprint. Lalu isi 3 metrik sisa (latensi handshake, overhead ciphertext, panjang invite) — semuanya cepat/murah. Baru setelah itu lengkapi BAB V/VI di `14_CHAPTER_CONTENT_PACK.md` dan update `HANDOFF_TO_CODEX.yaml` (`chapters.bab_5`/`bab_6`, `experiments.result_status`, `readiness.ready_for_codex` → `YES` penuh).

## Update SESSION 6 (2026-07-27, commit `75d17fd`) — Eksperimen SELESAI, BAB V/VI Terisi

Next action di atas **sudah dikerjakan seluruhnya**. Rincian di `SESSION_6_HANDOFF.md`. Ringkasnya:

- **EXP-05 SELESAI** — 30 cold-start `unseal` via CLI + 30 run kontrol. Neto **mean 47,99 ms** (median 45,08; sd 11,41), end-to-end mean 68,47 ms. **Klaim komentar kode "~100 ms" TERKOREKSI** (sekitar separuhnya pada hardware uji). Ukuran vault 108 byte terverifikasi 5 sampel.
- **3 metrik sisa**: panjang invite 86 karakter (5 sampel) `EXECUTED`; overhead tag 16 byte `PARTIAL` (instance vault terukur, instance Noise transport tidak); latensi handshake `PARTIAL` (hanya batas atas < 0,86 ms, di bawah resolusi metode eksternal).
- **Bonus EXP-01**: determinisme `unseal` 10/10 dengan invite identik; rejection passphrase salah 100%.
- Hasil: `02-experiment-data/EXPERIMENT_RESULTS_2026-07-27.csv` (123 baris data). File 2026-07-26 **tidak** ditimpa.
- **BAB V (3 subbab) dan BAB VI §6.1 terisi penuh** di `14_CHAPTER_CONTENT_PACK.md`. §6.2/§6.3 tidak diubah.
- `HANDOFF_TO_CODEX.yaml`: `ready_for_codex` → **`YES`** penuh; `bab_3`/`bab_5`/`bab_6` → READY; `experiments.result_status` → `EXECUTED`; BI-01/BI-02 → `resolved`; BI-06 baru (3 metrik yang tetap hedged).
- `15_CLAIM_EVIDENCE_CITATION_MAP.md`: CM-061 → `CORRECTED`; CM-150..154 diperbarui; CM-155/CM-156 baru; total klaim **81 → 83**.
- **Validasi SESSION 5B**: dilakukan (spot-check kode + konsistensi dokumen). Dua temuan nyata, keduanya sudah diperbaiki — `experiments.result_status` di handoff masih tertulis "TIDAK ADA eksperimen dijalankan" padahal commit `75d17fd` sudah menjalankan 46/46 test, dan BI-05 salah menyebut `16_TABLE_MANIFEST.md` (seharusnya `13_`). Selebihnya konsisten.

**Lanjutan sesi yang sama (setelah commit `1653531`)** — tiga kekurangan dituntaskan:

- **TBL-11/TBL-12 diisi hasil aktual** (`tables/11_test_scenarios.md`, `tables/12_evaluation_parameters.md`) — keduanya sebelumnya masih seluruhnya `WAITING_FOR_EXPERIMENT` padahal BAB V sudah merujuk ke sana.
- **Kontradiksi diperbaiki**: `screenshots/STATUS.md` mencatat panjang invite **87 karakter** (SESSION 4), terukur **86** dan aritmetika membenarkan 86 (⌈64×4÷3⌉). Dikoreksi beserta catatan penjelas.
- **BAB VI §6.2/§6.3 dinaikkan ke content pack 13 field** — sebelumnya hanya baris tabel rencana. **BAB VI kini READY penuh.**

**Next action**: tidak ada pekerjaan data/dokumen tersisa yang bisa dikerjakan agen tanpa izin tambahan. Jalur berikutnya = **Jalur B (Codex menyusun DOCX)** dari BAB I s.d. VI.

**Lanjutan berikutnya (identitas + format dokumen), 2026-07-27:**

- **Identitas anggota CONFIRMED** dan disebar ke `AGENTS.md`, `PROJECT_MEMORY.md`, `WORKFLOW_STATE.yaml`, `09_SCOPE_AND_TEAM_PLAN.md`, `tables/13_team_assignment.md`, `HANDOFF_TO_CODEX.yaml`. BI-04 → `resolved`.
- **`16_DOCUMENT_FORMAT_SPEC.md` dibuat** — aturan format diukur langsung dari XML `Cetak TA_rev3.docx` (A4, margin kiri 4 cm dan sisi lain 3 cm, Times New Roman 12 pt, justify, spasi 1,15, sitasi IEEE numerik, caption per BAB), lalu **struktur disederhanakan** atas instruksi pengguna: seluruh lembar formal + kata pengantar + abstract Inggris + daftar notasi/lampiran/riwayat hidup dihapus. Preseden penghapusan: proposal CARAKA untuk mata kuliah yang sama sudah memakai struktur ringkas.
- **Judul**: kepanjangan AKSARA kini masuk judul atas instruksi pengguna — membatalkan catatan `09_SCOPE_AND_TEAM_PLAN.md` §7 sebelumnya. Bentuk usulan di `16_DOCUMENT_FORMAT_SPEC.md` §2.

Yang masih terbuka, seluruhnya butuh keputusan/tindakan pengguna:

1. Persetujuan bentuk final judul (`16_DOCUMENT_FORMAT_SPEC.md` §2).
2. Pemetaan nama anggota ke peran Anggota 1/2/3 — urutan saat ini default dari proposal, boleh ditukar.
3. Capture screenshot TUI aktual (BI-03).
4. Konfirmasi spasi baris **1,15** (terukur dari contoh) vs **1,5** (lazim di panduan tertulis) — panduan tertulis dosen menang bila ada.
5. Opsional: histogram distribusi 30 run EXP-05 (`02-experiment-data/charts/` masih kosong); diagram topologi pengujian untuk BAB V (sengaja ditunda di TAHAP 11 menunggu test plan — alasan penundaannya kini hilang, BAB V satu-satunya bab tanpa gambar).
6. Opsional, butuh izin modifikasi `src/`: harness `criterion` untuk latensi handshake presisi dan test rejection ciphertext transport.

## Next action kalau lanjut sesi baru

**Sprint persiapan mini-TA (TAHAP 1-17) kini selesai** — `ready_for_codex: YES_PARTIAL` di `HANDOFF_TO_CODEX.yaml`. Sesi berikutnya BUKAN lagi "SESSION 6" dalam skema TAHAP baru, melainkan salah satu dari dua jalur berikut, tergantung permintaan pengguna:

### Jalur A — Menjalankan eksperimen (melengkapi BAB V/VI)

1. Baca `docs/mini-ta/PROJECT_MEMORY.md`, `SESSION_5B_HANDOFF.md`, `12_TEST_PLAN.md` (5 kelompok EXP-01..05), `15_CLAIM_EVIDENCE_CITATION_MAP.md` §15 (klaim performa).
2. Jalankan eksperimen sesuai prosedur `12_TEST_PLAN.md` (rebuild bila perlu, catat environment lengkap — CPU/RAM/OS/commit — WAJIB per setiap eksperimen).
3. Isi `docs/mini-ta/02-experiment-data/EXPERIMENT_RESULT_TEMPLATE.csv` dengan data nyata (JANGAN mengarang angka).
4. Lengkapi BAB V dan BAB VI subbab 6.1 di `14_CHAPTER_CONTENT_PACK.md` berdasarkan hasil nyata.
5. Update `HANDOFF_TO_CODEX.yaml`: `chapters.bab_5`/`bab_6` → READY, `experiments.result_status` → hasil aktual, `readiness.ready_for_codex` → `YES` penuh bila BAB V/VI selesai.

### Jalur B — Codex menyusun DOCX dari bahan yang sudah `YES_PARTIAL`

1. Codex membaca `HANDOFF_TO_CODEX.yaml` sebagai entry point, lalu `14_CHAPTER_CONTENT_PACK.md` (BAB I-IV siap), `15_CLAIM_EVIDENCE_CITATION_MAP.md` (verifikasi tiap klaim sebelum ditulis prosa), `13_TABLE_MANIFEST.md`+`tables/`, `11_FIGURE_MANIFEST.md`+`diagrams/`.
2. BAB V/VI (6.1) disusun belakangan setelah Jalur A selesai; 6.2/6.3 boleh disusun sekarang (`READY_FOR_DRAFTING`, tidak bergantung eksperimen).
3. WAJIB cek bagian "Klaim Kritis Anti-Overclaim" `15_CLAIM_EVIDENCE_CITATION_MAP.md` sebelum finalisasi prosa BAB manapun.

### Catatan Umum (berlaku kedua jalur)

- Jangan mengulang audit codebase/kripto/normalisasi/justifikasi/riset referensi/spesifikasi protokol/key lifecycle/threat model/scope-tim/related-work/diagram/rencana-pengujian/tabel/content-pack-BAB-I-IV/peta-klaim/handoff-Codex kecuali ada kontradiksi terdokumentasi.
- Subcommand `aksara id --vault <path> --offline` (binary `target/release/aksara.exe`, build SESSION 4 commit `450d484`, bila belum dibersihkan) dapat dipakai untuk EXP-01/EXP-05.
- Jika dibutuhkan referensi eksternal baru, tambahkan ke `references/REFERENCES.bib` yang sudah ada (40 entry).
- `semantic-scholar` dan `tavily` bermasalah sejak sesi-sesi sebelumnya — `ydc-server` (you-search) adalah fallback terbukti bekerja.
- Nama asli 3 anggota kelompok, `study_program`, dan `institution` tetap `NEEDS_CONFIRMATION` di `HANDOFF_TO_CODEX.yaml` — perlu diisi kelompok sebelum cetak final.
- Update file ini setiap TAHAP/langkah besar selesai — jangan tunggu sampai akhir sesi.
