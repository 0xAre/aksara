# AKSARA Project Memory

Dokumen ini memuat fakta stabil lintas-agen, bukan log sesi.

## Identitas dan Konteks

- AKSARA adalah aplikasi chat P2P terminal serverless untuk komunikasi terenkripsi dua pihak tanpa server perantara.
- Implementasi utama menggunakan Rust 2021, Tokio, ratatui/crossterm, LAN dengan mDNS/TCP, dan Tor onion service.
- AKSARA bukan `CARAKA-APP` (proyek Android/Kotlin) dan bukan proyek terpisah `Caraka` (Rust/Tauri). Fakta ketiganya tidak boleh dicampur.
- Dokumen yang disusun adalah Tugas Akhir Mata Kuliah Implementasi Kriptografi, bukan skripsi atau TA individu.
- Pekerjaan dilakukan oleh tiga anggota, identitas **CONFIRMED** 2026-07-27 dari `docs/mini-ta/00-template/PROPOSAL CARAKA (2).docx` (mata kuliah dan kelompok yang sama): Andika Aryansyach Fauzan (2322101878), Mahendra Nur Hidayat (2322101937), Rafi Putra Fadlurrahman (2322101963). Program studi Rekayasa Sistem Kriptografi, Politeknik Siber dan Sandi Negara, tahun 2026. Placeholder `Anggota 1/2/3` sudah tidak dipakai; yang masih `NEEDS_CONFIRMATION` hanya pemetaan nama ke pembagian modul.
- Fokus akademik: menjelaskan implementasi dan memberikan justifikasi kriptografi yang faktual dengan scope proporsional untuk tugas mata kuliah.

## Status Stabil

- TAHAP 1 s.d. 11 berstatus `DONE`; TAHAP 12 berstatus `DONE` partial (build+verifikasi fungsi selesai, capture screenshot TUI aktual `MANUAL_USER_ACTION_REQUIRED`, tidak menghalangi `ready_for_codex`) — seluruhnya SESSION 1-4 selesai.
- TAHAP 13 (rencana pengujian) dan TAHAP 14 (tabel) berstatus `DONE` — SESSION 5A selesai. Output: `12_TEST_PLAN.md` (5 kelompok eksperimen EXP-01..05, seluruh status `WAITING_FOR_EXPERIMENT`, TIDAK ada hasil dibuat), `02-experiment-data/EXPERIMENT_RESULT_TEMPLATE.csv`, `13_TABLE_MANIFEST.md` + `tables/01`..`13_*.md` (13 kategori tabel, format Markdown). Detail lengkap di `SESSION_5A_HANDOFF.md`.
- **SPRINT PERSIAPAN MINI-TA (TAHAP 1-17) SELESAI** — SESSION 5B menyambung SESSION 5A dalam satu percakapan (bukan sesi terpisah). TAHAP 15 (`14_CHAPTER_CONTENT_PACK.md`) `PARTIAL` by design: BAB I-IV selesai penuh (28 subbab, memenuhi Quality Gate #15 brief); BAB V dan BAB VI subbab 6.1 sengaja distub `WAITING_FOR_EXPERIMENT` (diizinkan eksplisit brief), TAPI BAB VI subbab 6.2 (keterbatasan) dan 6.3 (saran) berstatus `READY_FOR_DRAFTING` — TIDAK bergantung eksperimen. TAHAP 16 `DONE`: `15_CLAIM_EVIDENCE_CITATION_MAP.md`, 81 Claim ID (`CM-001`..`154`) plus bagian "Klaim Kritis Anti-Overclaim" (5 item prioritas tertinggi, WAJIB dicek Codex sebelum menulis prosa). TAHAP 17 `DONE`: `HANDOFF_TO_CODEX.yaml`, `ready_for_codex: YES_PARTIAL`, 17/17 syarat quality gate `met: true` (termasuk poin 17 — tidak ada kontradiksi kritis algoritma/nonce/key-management/format-protokol). Detail lengkap di `SESSION_5B_HANDOFF.md`.
- **Langkah selanjutnya BUKAN TAHAP baru** dalam skema 17-tahap brief — dua jalur independen: (a) menjalankan `12_TEST_PLAN.md` untuk melengkapi BAB V/VI, atau (b) Codex mulai menyusun DOCX dari BAB I-IV yang sudah `YES_PARTIAL`. Keduanya boleh berjalan tanpa saling menunggu.
- **Jalur A (eksperimen) SELESAI** — dua tahap. (a) 2026-07-26, commit `3d22494`: `cargo test --release` = 46/46 PASS, mencakup penuh correctness+rejection EXP-01..04. (b) 2026-07-27, commit `75d17fd` (SESSION 6): EXP-05 dan 3 metrik sisa dijalankan. Hasil: `02-experiment-data/EXPERIMENT_RESULTS_2026-07-26.csv` dan `EXPERIMENT_RESULTS_2026-07-27.csv`. Jangan jalankan ulang apa pun dari nol tanpa alasan spesifik.
- **Hasil kuantitatif kunci (SESSION 6, hardware uji spesifik — JANGAN digeneralisasi)**: waktu `unseal` vault neto **mean 47,99 ms** (median 45,08; sd 11,41; n=30 cold-start), end-to-end **68,47 ms**. Ini **MENGOREKSI** klaim komentar kode `src/identity/vault.rs` "~100 ms" (CB-087/CM-061) — satu-satunya klaim performa eksplisit dalam source, kini berstatus `CORRECTED`, bukan lagi `DOCUMENTED_ONLY`. Terverifikasi juga: vault tepat 108 byte (5 sampel), invite 86 karakter (5 sampel), fingerprint 64 hex, overhead tag AEAD 16 byte (instance vault), determinisme `unseal` 10/10, rejection passphrase salah 100%. Lingkungan uji: Windows 11 10.0.26200, Intel Core i7-1165G7 4C/8T, RAM 11,79 GB, bare-metal, `rustc 1.97.0`, profil release.
- **Tiga metrik TETAP tidak terukur presisi dan hedge-nya wajib dipertahankan**: latensi handshake Noise_IK (hanya batas atas **< 0,86 ms**, 95% CI — di bawah resolusi pengukuran eksternal), overhead ciphertext instance Noise transport (tidak observable dari luar proses), memory usage puncak/RSS (CM-154). Ketiganya butuh instrumentasi `src/` (mis. `criterion`) yang memerlukan permintaan eksplisit pengguna per `AGENTS.md` §Source-Code Protection.
- **BAB I s.d. BAB VI seluruhnya READY** di `14_CHAPTER_CONTENT_PACK.md` (SESSION 6) — 31 subbab dengan format 13 field. `ready_for_codex` di `HANDOFF_TO_CODEX.yaml` kini **`YES`** penuh, naik dari `YES_PARTIAL`. Peta klaim naik dari 81 menjadi 83 Claim ID (CM-155/CM-156 baru untuk metrik deterministik terverifikasi). TBL-11 dan TBL-12 sudah berisi hasil aktual, bukan lagi `WAITING_FOR_EXPERIMENT`.
- **Panjang invite = 86 karakter, bukan 87.** `screenshots/STATUS.md` sempat mencatat 87 sejak SESSION 4; terukur 86 pada 5 keypair dan aritmetika membenarkannya (base64url tanpa padding atas 64 byte = ⌈64×4÷3⌉ = 86). Sudah dikoreksi 2026-07-27. Jangan pakai angka 87 dari dokumen/ingatan lama.
- **Aturan format ada di `01-claude-preparation/16_DOCUMENT_FORMAT_SPEC.md`** (direvisi 2026-07-27 dari pedoman resmi). **Sumber otoritatif**: `Peraturan Direktur Poltek SSN tentang Pedoman Pelaksanaan Tugas Akhir` (2024), halaman 58-68 — file berada DI LUAR repo di `E:\Kuliah\TA\FINAL PERDIR PEDOMAN TA\`. Pedoman menimpa contoh docx mana pun. Inti: A4, margin kiri 4 cm dan sisi lain 3 cm, Times New Roman 12 pt, justify, **spasi 1,15** (resmi, bukan terka — pertanyaan 1,15 vs 1,5 sudah TERTUTUP), paragraf tanpa indentasi, footer institusi Arial 10 pt tebal rata kanan, penomoran subbab **Romawi.Arab (`IV.1.1`)** bukan angka Arab, sitasi IEEE dengan nomor sebelum tanda baca.
- **Struktur DISEDERHANAKAN atas instruksi pengguna** (tata tulis tetap diikuti penuh): seluruh lembar formal, kata pengantar, abstract Inggris, daftar notasi/lampiran/riwayat hidup, dan spesifikasi sampul hardcover DIHAPUS karena tugas mata kuliah tidak melalui sidang. **Abstrak Indonesia justru NAIK jadi wajib.** Preseden penghapusan: proposal CARAKA untuk mata kuliah yang sama.
- **Judul FINAL (CONFIRMED 2026-07-27)**: `AKSARA (Authenticated Key-based Secure Autonomous Relay Architecture): Chat Terminal Tanpa Server — Implementasi dan Evaluasi Keamanan Protokol Noise_IK, Siklus Hidup Kunci, dan Threat Model`. Membatalkan catatan `09_SCOPE_AND_TEAM_PLAN.md` §7 yang lama. Kata "P2P" dan sisi evaluasi empiris sengaja tidak ada di judul — WAJIB dikompensasi di Abstrak/BAB I §1.1/BAB VI §6.1. DILARANG menambah frasa "Tanpa Jejak"/"Anti-Sadap"/"Terbukti Aman" (T2: metadata masih bocor via mDNS).
- **Peran anggota CONFIRMED 2026-07-27**: Andika = core developer fullstack (BAB IV), Mahendra = dokumentasi akhir (BAB I/II/VI + Abstrak + bagian awal-akhir), Rafi = user testing (BAB V + metodologi pengujian BAB III). Pembagian **berbasis peran fungsional, bukan kepemilikan modul kode** — AKSARA sudah terimplementasi utuh oleh satu core developer sebelum penelitian dimulai. Pembagian berbasis modul di versi lama `09_SCOPE_AND_TEAM_PLAN.md` §8 adalah asumsi SESSION 2 dan sudah SUPERSEDED. Jangan mengarang pembagian modul per orang agar terlihat seimbang.
- **Yang tersisa sebelum penyusunan DOCX**: capture screenshot TUI, plus dua pertanyaan kosmetik (apakah footer institusi dan Abstrak dua bahasa tetap diminta untuk tugas mata kuliah).
- Audit codebase menghasilkan 259 klaim final.
- Audit implementasi kriptografi menghasilkan 36 entry, dikonsolidasi ke 7 komponen inti CORE-1..7.
- Spesifikasi protokol (`06_PROTOCOL_SPECIFICATION.md`), key lifecycle (`07_KEY_LIFECYCLE.md`), threat model (`08_THREAT_MODEL.md`), scope & tim (`09_SCOPE_AND_TEAM_PLAN.md`), related work & gap (`10_RELATED_WORK_AND_GAP.md`), dan figure manifest (`11_FIGURE_MANIFEST.md`) sudah tersedia sebagai ground truth untuk sesi berikutnya — jangan diulang tanpa kontradiksi spesifik yang terdokumentasi.
- Referensi terverifikasi total **40 entry** (`references/REFERENCES.bib`) — 33 dari TAHAP 4/9/SESSION 3, 7 tambahan related work TAHAP 10/SESSION 4.
- `cargo build --release` terverifikasi bersih (0 warning/0 error) pada commit `450d484` (2026-07-26) — detail di `01-claude-preparation/screenshots/STATUS.md`. Jangan mengulang klaim ini sebagai "baru diverifikasi" pada sesi mendatang tanpa build ulang.
- Tidak ada lagi "tahap aktif berikutnya" dalam skema TAHAP 1-17 — seluruhnya `DONE`/`PARTIAL by design`. Jangan mengulang tahap `DONE` tanpa kontradiksi spesifik yang terdokumentasi.
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

## Workflow Sprint Persiapan (SELESAI — SESSION 1 s.d. 5B)

- Sprint persiapan mini-TA sudah selesai penuh: SESSION 1, 2, 3, 4, 5A, 5B — seluruhnya `DONE`.
- SESSION 3 — Protocol and Security Model: TAHAP 5-7. Status: `DONE`.
- SESSION 4 — Scope, Related Work, and Figures: TAHAP 8, 10, 11, 12. Status: `DONE` (TAHAP 12 partial, tidak menghalangi lanjut).
- SESSION 5A — Testing Plan and Tables: TAHAP 13, 14. Status: `DONE`.
- SESSION 5B — Chapter Content Pack and Codex Handoff: TAHAP 15 (partial by design), 16, 17. Status: `DONE`. Dijalankan menyambung SESSION 5A dalam satu percakapan (user memilih lanjut bertahap-hati-hati alih-alih sesi baru terpisah, berbeda dari pemecahan SESSION 4→5A/5B sebelumnya).
- `docs/mini-ta/WORKFLOW_STATE.yaml` (`sprint_status: PREPARATION_COMPLETE`) adalah state mesin lintas Claude dan Codex — baca dan perbarui bila ada pekerjaan lanjutan (eksekusi eksperimen, penyusunan DOCX oleh Codex).

## Wajib Baca Saat Memulai (Pekerjaan Lanjutan Pasca-Sprint)

1. `docs/mini-ta/PROJECT_MEMORY.md`
2. `docs/mini-ta/01-claude-preparation/PROGRESS.md`
3. `docs/mini-ta/01-claude-preparation/SESSION_6_HANDOFF.md` (handoff terbaru)
4. `docs/mini-ta/01-claude-preparation/HANDOFF_TO_CODEX.yaml` sebagai entry point — Jalur A (eksperimen) sudah selesai, sehingga jalur aktif tinggal (b): Codex menyusun DOCX dari `14_CHAPTER_CONTENT_PACK.md` BAB I s.d. VI + `15_CLAIM_EVIDENCE_CITATION_MAP.md` (cek "Klaim Kritis Anti-Overclaim" dulu — item #3 sudah berubah, klaim "~100 ms" kini terkoreksi, bukan lagi "belum diverifikasi")
