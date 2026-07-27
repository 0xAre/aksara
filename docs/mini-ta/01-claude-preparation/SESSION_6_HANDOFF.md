# SESSION 6 HANDOFF

Status sesi: **SELESAI**. Dua pekerjaan: (A) validasi output SESSION 5B, (B) eksekusi sisa `12_TEST_PLAN.md` lalu mengisi BAB V dan BAB VI §6.1. Bukan TAHAP baru dalam skema 17-tahap `CLAUDE_PREPARATION_BRIEF.md` — sprint persiapan sudah selesai sejak SESSION 5B.

Commit basis pengukuran: `75d17fd`. Tanggal eksekusi: 2026-07-27.

## A. Hasil Validasi SESSION 5B

Metode: spot-check langsung ke source code (bukan membaca ulang dokumen ke dokumen), plus pengecekan silang antar-dokumen state.

**Yang diverifikasi cocok (tidak ada temuan):**

| Yang dicek | Hasil |
|---|---|
| CM-071 — tidak ada `sign()`/`verify()` Ed25519 | Grep menyeluruh `src/` nihil. **Akurat.** |
| CM-061 — komentar "~100ms" ada di `vault.rs` | Ada, pada blok doc-comment `argon2_params()`. **Akurat.** |
| Layout vault 108 byte | `SALT_LEN 16 + NONCE_LEN 12 + PLAINTEXT_LEN 64 + TAG_LEN 16`. **Cocok.** |
| Parameter Argon2id 19 MiB / t=2 / p=1 | `Params::new(19*1024, 2, 1, Some(32))`. **Cocok.** |
| Konstanta protokol di content pack §4.3/§4.5 | `MAX_FRAME_LEN=65535`, `LAN_AUTO_TIMEOUT=3s`, `TOR_DIAL_TOTAL_TIMEOUT=120s` — **ketiganya cocok** dengan source. |
| Nama pattern Noise | `NOISE_PATTERN = "Noise_IK_25519_ChaChaPoly_BLAKE2s"` literal di source. **Cocok.** |
| Bagian "Klaim Kritis Anti-Overclaim" (5 item) | Kelimanya akurat terhadap kode/dokumen pada saat ditulis. |
| `readiness.quality_gate_17_items` | 17/17 `met: true` tetap valid; tidak ada kontradiksi baru yang memaksa `ready_for_codex: NO`. |

**Dua temuan nyata — keduanya sudah diperbaiki sesi ini:**

1. **`HANDOFF_TO_CODEX.yaml` tertinggal satu commit.** Field `experiments.result_status` masih `WAITING_FOR_EXPERIMENT` dengan catatan "TIDAK ADA eksperimen yang sudah dijalankan", padahal commit `75d17fd` (2026-07-26) sudah menjalankan 46/46 test. `PROGRESS.md` dan `WORKFLOW_STATE.yaml` sudah diperbarui saat itu, handoff Codex tidak ikut. **Pelajaran**: bila status eksperimen berubah, ketiga file harus diperbarui bersamaan, bukan dua dari tiga.
2. **`HANDOFF_TO_CODEX.yaml` BI-05 salah menyebut nama file** — tertulis `16_TABLE_MANIFEST.md`, seharusnya `13_TABLE_MANIFEST.md` (kemungkinan sisa dari pergeseran penomoran +2 yang dicatat `PROGRESS.md` keputusan #0). Kosmetik, sudah dikoreksi.

`14_CHAPTER_CONTENT_PACK.md` BAB I-IV dan `15_CLAIM_EVIDENCE_CITATION_MAP.md` **tidak ditulis ulang** — tidak ditemukan pertentangan dengan `06_PROTOCOL_SPECIFICATION.md`/`07_KEY_LIFECYCLE.md`/`08_THREAT_MODEL.md`/`04_CRYPTOGRAPHIC_JUSTIFICATION.md`. Perubahan pada peta klaim murni akibat data eksperimen baru, bukan koreksi kesalahan.

## B. Hasil Eksekusi Pengujian

Data lengkap: `docs/mini-ta/02-experiment-data/EXPERIMENT_RESULTS_2026-07-27.csv` (123 baris data + blok ringkasan). File `EXPERIMENT_RESULTS_2026-07-26.csv` **tidak ditimpa**.

**Lingkungan** (wajib ikut dikutip setiap kali angka di bawah dipakai): Windows 11 Home 10.0.26200 build 26200; Intel Core i7-1165G7 4C/8T @2,80 GHz; RAM 11,79 GB (bebas ~0,93 GB saat uji); bare-metal LENOVO 82FG; `rustc 1.97.0 (2d8144b78 2026-07-07)` / `cargo 1.97.0`; profil `--release`, dibuild ulang sebelum pengukuran (1 menit 5 detik).

### EXP-05 — Benchmark Argon2id (prioritas tertinggi, SELESAI)

Prosedur: 30 cold-start `aksara id --vault <path> --offline` (proses baru per run, passphrase lewat env `AKSARA_PASSPHRASE`, data dummy), diukur `Measure-Command`. Ditambah **30 run kontrol** `aksara -h` untuk mengisolasi biaya Argon2id dari overhead spawn proses — kontrol ini tidak diminta rencana asli, tapi tanpanya angka end-to-end akan melebih-lebihkan biaya KDF.

| Ukuran | Hasil |
|---|---|
| End-to-end proses (n=30) | mean 68,47 ms · median 64,15 · sd 12,47 · min 54,53 · max 106,86 |
| Kontrol tanpa Argon2id (n=30) | mean 20,48 ms · median 19,10 · sd 4,73 |
| **`unseal` neto** (selisih berpasangan) | **mean 47,99 ms** · median 45,08 · sd 11,41 · min 26,99 · max 86,30 |
| Ukuran vault | tepat **108 byte** pada 5 vault independen |

**Kesimpulan EXP-05**: klaim komentar kode "~100 ms" **TERKOREKSI**, bukan dikonfirmasi — pada hardware uji nilainya sekitar separuh. Bahkan angka end-to-end (68 ms) masih di bawah 100 ms. CM-061 berubah dari `DOCUMENTED_ONLY`/LOW menjadi `CORRECTED`.

### Metrik lain

| Metrik | Status | Hasil |
|---|---|---|
| EXP-04 panjang invite | `EXECUTED` | 86 karakter konsisten pada 5 keypair acak; fingerprint 64 karakter hex |
| EXP-01 determinisme + rejection CLI | `EXECUTED` | 10/10 unseal sukses, invite identik seluruh run (string unik = 1); passphrase salah → exit 1, pesan generik `Error: vault could not be opened` |
| EXP-03 overhead tag AEAD | `PARTIAL` | Tepat 16 byte terukur pada instance **vault**. Instance Noise transport **tidak** diukur |
| EXP-02 latensi handshake | `PARTIAL` | Selisih berpasangan −0,15 ms (sd 1,91; n=19) = tidak terdeteksi di atas noise. Dilaporkan **batas atas < 0,86 ms (95% CI)**, bukan nilai titik |
| EXP-05 memory usage puncak (RSS) | `WAITING_FOR_EXPERIMENT` | Tidak diukur; hanya parameter statis 19 MiB yang diketahui |

Metode latensi handshake: perbandingan waktu proses test-binary yang menjalankan `handshake_ik_roundtrip --exact` versus yang menjalankan 0 test. `--report-time` cargo hanya tersedia di nightly, sehingga timing per-test tidak bisa diambil langsung. Hasilnya bermakna secara kualitatif — biaya kriptografi per sesi didominasi Argon2id (~48 ms), bukan handshake (< 1 ms).

## B2. Pekerjaan Lanjutan Sesi yang Sama (#5-#7)

Setelah commit `1653531`, pengguna meminta tiga kekurangan yang teridentifikasi dari analisis kesiapan dituntaskan:

1. **TBL-11 dan TBL-12 diisi hasil aktual.** Keduanya sebelumnya masih seluruhnya `WAITING_FOR_EXPERIMENT` padahal BAB V §5.2/§5.3 sudah menunjuk ke sana. `tables/11_test_scenarios.md` mendapat kolom "Hasil Aktual" + status per EXP; `tables/12_evaluation_parameters.md` mendapat kolom "Hasil Terukur" + status per metrik, plus catatan metode kontrol baseline.
2. **Kontradiksi 87 vs 86 karakter diperbaiki.** `screenshots/STATUS.md` (SESSION 4) mencatat panjang invite **87 karakter**; pengukuran EXP-04 pada 5 keypair memberi **86**, dan aritmetikanya membenarkan 86 (⌈64 × 4 ÷ 3⌉ = 86). Angka 87 adalah kesalahan hitung SESSION 4, bukan perubahan perilaku kode. Sudah dikoreksi beserta catatan penjelasnya. **Pelajaran**: angka yang dicatat dari pengamatan sekilas tanpa verifikasi aritmetika sempat bertahan tiga sesi.
3. **BAB VI §6.2/§6.3 dinaikkan ke content pack 13 field.** Sebelumnya hanya baris tabel rencana berstatus `READY_FOR_DRAFTING` — Codex punya arah tapi bukan bahan, dan risikonya dua subbab penutup ditulis dengan kedalaman berbeda dari 28 subbab lain. §6.2 disusun 3 lapis (batas cakupan / batas metode / batas melekat objek); §6.3 berisi 9 butir saran yang seluruhnya tertaut eksplisit ke G1-G5 atau T1-T7.

Akibatnya **BAB VI kini READY penuh**, bukan lagi campuran READY + READY_FOR_DRAFTING.

## C. Dokumen yang Diperbarui

- `14_CHAPTER_CONTENT_PACK.md` — **BAB V terisi penuh** (5.1 lingkungan, 5.2 hasil, 5.3 analisis; format 13 field per subbab sama seperti BAB I-IV) dan **BAB VI §6.1 terisi**. §6.2/§6.3 **tidak diubah** (tetap `READY_FOR_DRAFTING`), hanya ditambahi daftar bahan dari hasil BAB V. Tabel ringkasan status per BAB diperbarui.
- `15_CLAIM_EVIDENCE_CITATION_MAP.md` — CM-061 → `CORRECTED`; §15 klaim performa ditulis ulang dengan hasil nyata; CM-155 (vault 108 byte) dan CM-156 (invite 86 karakter) baru; total **81 → 83** Claim ID; anti-overclaim item #3 diperbarui.
- `HANDOFF_TO_CODEX.yaml` — `ready_for_codex` **`YES_PARTIAL` → `YES`**; `bab_3`/`bab_5`/`bab_6` → `READY`; `experiments.result_status` → `EXECUTED` + blok `environment`; BI-01/BI-02 → `resolved`; **BI-06 baru**; BI-05 nama file dikoreksi.
- `12_TEST_PLAN.md` — bagian "Status Eksekusi" diperbarui dengan tabel hasil per metrik.
- `PROGRESS.md`, `WORKFLOW_STATE.yaml` (`session_6` baru, `ready_for_codex: YES`), `PROJECT_MEMORY.md`.

## D. Aturan Anti-Overclaim yang Wajib Dibawa Codex

Status `ready_for_codex: YES` **tidak** berarti semua terukur. Tiga hedge tidak boleh dihapus saat menulis prosa:

1. **Latensi handshake** — tulis sebagai batas atas (< 0,86 ms), jangan pernah sebagai nilai titik, dan jangan tulis "handshake tidak memakan waktu".
2. **Overhead ciphertext 16 byte** — yang terukur instance **vault**; untuk transport sesi nilainya deterministik dari spesifikasi, bukan hasil pengukuran.
3. **Angka performa apa pun** — selalu bersama n, sebaran, dan spesifikasi hardware §5.1. Jangan generalisasi ke "hardware modern".

Ditambah: jangan menulis komentar kode "salah" secara umum — yang terukur hanya satu unit hardware. Empat item lain di "Klaim Kritis Anti-Overclaim" (Ed25519 tanpa sign/verify, forward secrecy `DOCUMENTED_ONLY`, ChaCha20-Poly1305 tanpa AAD/misuse-resistance, trust-on-first-use) **tidak berubah** dan tetap berlaku penuh.

## E. Next Action

**Jalur B (Codex menyusun DOCX)** — kini dari BAB I s.d. BAB VI, tidak ada lagi yang perlu ditunggu. Entry point tetap `HANDOFF_TO_CODEX.yaml`, wajib baca "Klaim Kritis Anti-Overclaim" dan bagian D di atas sebelum menulis prosa.

**Opsional, butuh izin eksplisit pengguna untuk memodifikasi `src/`:**

1. Tambah harness `criterion` (`benches/`) untuk mengukur latensi handshake dan overhead ciphertext transport secara presisi — akan menaikkan CM-151/CM-152 dari `PARTIAL` menjadi `MEASURED`.
2. Tambah test rejection untuk frame/ciphertext transport sesi yang dimodifikasi — satu-satunya kelas rejection yang belum punya test (`12_TEST_PLAN.md` §EXP-03 poin 15).
3. Ukur RSS puncak saat Argon2id berjalan (CM-154) — butuh tooling profiling, bukan modifikasi source.

Ketiganya **tidak menghalangi** penyusunan DOCX.

**Yang masih `NEEDS_CONFIRMATION` dan hanya bisa diisi kelompok**: nama asli 3 anggota, `study_program`, `institution`, serta capture screenshot TUI aktual (BI-03/BI-04).
