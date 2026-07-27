# Tabel 11 — Skenario Pengujian

Ringkasan 5 kelompok eksperimen `12_TEST_PLAN.md` (TAHAP 13) — detail 15 field wajib per eksperimen tersedia di dokumen sumber, tidak diulang di sini.

**Diperbarui 2026-07-27 dengan hasil aktual.** Eksekusi dua tahap: correctness/rejection pada commit `3d22494` (2026-07-26) dan seluruh metrik kuantitatif pada commit `75d17fd` (2026-07-27). Lingkungan lengkap tercatat di `14_CHAPTER_CONTENT_PACK.md` BAB V §5.1. Data mentah: `docs/mini-ta/02-experiment-data/EXPERIMENT_RESULTS_2026-07-26.csv` dan `EXPERIMENT_RESULTS_2026-07-27.csv`.

| ID | Nama Skenario | Objek Utama | Primitif (CORE-x) | Jenis Pengujian | Metrik Utama | Hasil Aktual | Status |
|---|---|---|---|---|---|---|---|
| EXP-01 | Correctness dan rejection vault identitas | `identity::vault` (`seal`/`unseal`) | CORE-3, CORE-5 | Correctness, wrong-key rejection, modified-ciphertext rejection, nonce handling | Proporsi roundtrip sukses (%), proporsi rejection benar (%) | Roundtrip **100%** (5 unit test + 10/10 run CLI dengan invite identik); rejection **100%** (passphrase salah dan ciphertext dimodifikasi) | EXECUTED |
| EXP-02 | Correctness dan rejection handshake Noise_IK | `crypto::handshake`, `session::run_session` (fase handshake) | CORE-1, CORE-2 | Correctness, key agreement consistency, wrong-key/unknown-peer rejection | Pass/fail test, latensi handshake (ms) | 5/5 test **pass**. Latensi: **batas atas < 0,86 ms** (95% CI, n=19) — tidak terdeteksi di atas noise metode eksternal, **bukan nilai titik** | EXECUTED (correctness) / PARTIAL (latensi) |
| EXP-03 | Consistency transport sesi terenkripsi | `session::run_session` (fase transport), `transport::frame` | CORE-3 (transport) | Encryption-decryption consistency, oversize/keepalive handling | Pass/fail test, overhead ciphertext (byte) | 9/9 test **pass**. Overhead tag **16 byte** terukur pada instance vault; instance Noise transport **tidak diukur langsung** | EXECUTED (correctness) / PARTIAL (overhead) |
| EXP-04 | Correctness invite/fingerprint/contact store | `contacts::mod` | CORE-4, helper encoding | Serialization-deserialization consistency, KDF consistency, wrong-key rejection | Pass/fail test, panjang string invite (karakter) | 10/10 test **pass**. Panjang invite **86 karakter** konsisten pada 5 keypair acak; fingerprint 64 hex | EXECUTED |
| EXP-05 | Benchmark Argon2id dan ciphertext expansion | `identity::vault` (performa) | CORE-5, CORE-3 | Performance benchmark, ciphertext expansion | Waktu unlock vault (ms: mean/median/stdev), ukuran vault (byte) | Neto **mean 47,99 ms** (median 45,08; sd 11,41; n=30); end-to-end mean 68,47 ms. **MENGOREKSI** klaim komentar kode "~100 ms". Ukuran vault **tepat 108 byte** (5 sampel) | EXECUTED |

**Agregat test suite**: `cargo test --release` = **46/46 PASS, 0 FAIL, 0 ignored**.

**Yang tetap belum terukur**: memory usage puncak (RSS) saat Argon2id berjalan — opsional, hanya parameter statis 19 MiB yang diketahui dari kode. Bersama latensi handshake presisi dan overhead instance Noise transport, ketiganya memerlukan instrumentasi `src/` yang membutuhkan permintaan eksplisit pengguna (`AGENTS.md` §Source-Code Protection).

## Cakupan Kandidat Brief yang Tidak Berlaku (N/A)

| Kandidat | Alasan |
|---|---|
| Known-answer test (KAT) | Tidak ditemukan test vector standar resmi yang dipakai test suite AKSARA — seluruh test bersifat roundtrip/property-based |
| Modified associated-data rejection | AKSARA tidak memakai AAD pada ketiga instance ChaCha20-Poly1305 manapun |
| Replay rejection | Tidak ditemukan mekanisme replay-protection eksplisit di source yang diaudit |

## Referensi

`12_TEST_PLAN.md` (TAHAP 13).
