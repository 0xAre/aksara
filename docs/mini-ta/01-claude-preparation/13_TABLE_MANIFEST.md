# 13 — Manifest Tabel AKSARA

Dokumen ini mendaftar 13 kategori tabel wajib (`CLAUDE_PREPARATION_BRIEF.md` TAHAP 14). Seluruh isi tabel adalah **kompresi/reproduksi siap-pakai** dari dokumen TAHAP 1-13 yang sudah diaudit/diverifikasi — tidak ada klaim baru diperkenalkan pada TAHAP 14 ini. Data disimpan di `docs/mini-ta/01-claude-preparation/tables/` dalam format Markdown (dipilih atas CSV karena mayoritas sel berisi kalimat/frasa panjang yang lebih terbaca sebagai tabel Markdown daripada CSV ber-quote).

| # | Kategori (brief) | ID Tabel | File | Sumber Utama | Bab Tujuan |
|---|---|---|---|---|---|
| 1 | Kebutuhan fungsional | TBL-01 | `tables/01_functional_requirements.md` | `01_CODEBASE_AUDIT.md`, `06_PROTOCOL_SPECIFICATION.md` | BAB III/IV |
| 2 | Kebutuhan non-fungsional | TBL-02 | `tables/02_nonfunctional_requirements.md` | `04_CRYPTOGRAPHIC_JUSTIFICATION.md`, `07_KEY_LIFECYCLE.md`, `08_THREAT_MODEL.md` | BAB III/IV |
| 3 | Stack teknologi | TBL-03 | `tables/03_tech_stack.md` | `PROJECT_MEMORY.md` §Versi Ground Truth, `Cargo.lock` | BAB III/IV |
| 4 | Inventarisasi primitif kriptografi | TBL-04 | `tables/04_crypto_primitives_inventory.md` | `02_CRYPTO_IMPLEMENTATION_AUDIT.md`, `03_CRYPTO_INVENTORY_NORMALIZED.md` | BAB IV |
| 5 | Justifikasi algoritma | TBL-05 | `tables/05_algorithm_justification.md` | `04_CRYPTOGRAPHIC_JUSTIFICATION.md` | BAB II/IV |
| 6 | Perbandingan alternatif algoritma | TBL-06 | `tables/06_algorithm_alternative_comparison.md` | `05_CRYPTO_ALTERNATIVE_COMPARISON.md` | BAB II/IV |
| 7 | Format paket | TBL-07 | `tables/07_packet_format.md` | `06_PROTOCOL_SPECIFICATION.md`, `07_KEY_LIFECYCLE.md` | BAB IV |
| 8 | Lifecycle kunci | TBL-08 | `tables/08_key_lifecycle.md` | `07_KEY_LIFECYCLE.md` | BAB IV |
| 9 | Threat model | TBL-09 | `tables/09_threat_model.md` | `08_THREAT_MODEL.md` | BAB IV/V |
| 10 | Penelitian terkait | TBL-10 | `tables/10_related_work.md` | `10_RELATED_WORK_AND_GAP.md` | BAB II |
| 11 | Skenario pengujian | TBL-11 | `tables/11_test_scenarios.md` | `12_TEST_PLAN.md` | BAB III/V |
| 12 | Parameter evaluasi | TBL-12 | `tables/12_evaluation_parameters.md` | `12_TEST_PLAN.md` | BAB III/V |
| 13 | Pembagian tugas anggota | TBL-13 | `tables/13_team_assignment.md` | `09_SCOPE_AND_TEAM_PLAN.md` §8 | BAB I |

## Catatan Status Data

- **TBL-01 s.d. TBL-04, TBL-07, TBL-08, TBL-09** bersumber dari klaim yang sudah berstatus `IMPLEMENTED`/`CONFIRMED`/`DOCUMENTED_ONLY` sesuai audit TAHAP 1-7 — tidak memerlukan verifikasi tambahan pada TAHAP 14.
- **TBL-05, TBL-06** bersumber langsung dari `04`/`05` (TAHAP 4) — kompresi 15 poin/10 kriteria penuh, dokumen sumber tetap menjadi rujukan detail.
- **TBL-10** bersumber dari `10_RELATED_WORK_AND_GAP.md` (TAHAP 10) — 7 entry, 40 referensi total tetap konsisten.
- **TBL-11, TBL-12** bersumber dari `12_TEST_PLAN.md` (TAHAP 13, SESSION 5A) — seluruh nilai metrik berstatus `WAITING_FOR_EXPERIMENT`, BUKAN hasil terukur. Jangan mengutip nilai dari tabel ini sebagai data eksperimen final di BAB V sebelum eksperimen benar-benar dijalankan.
- **TBL-13** bersumber dari `09_SCOPE_AND_TEAM_PLAN.md` §8 (TAHAP 8) — nama anggota tetap placeholder `NEEDS_CONFIRMATION`.

## Validasi Silang

Seluruh 13 tabel diperiksa agar konsisten dengan dokumen sumbernya masing-masing (tidak ada angka/istilah yang menyimpang dari `02`-`10`/`12`). Tidak ditemukan kontradiksi antar tabel pada saat penyusunan TAHAP 14 (SESSION 5A).

## Referensi

Seluruh dokumen sumber TAHAP 1-13 (`01`-`10`, `12`) dan `references/REFERENCES.bib` (40 entry, tidak ada penambahan baru pada TAHAP 14).
