# Tabel 11 — Skenario Pengujian

Ringkasan 5 kelompok eksperimen `12_TEST_PLAN.md` (TAHAP 13) — detail 15 field wajib per eksperimen tersedia di dokumen sumber, tidak diulang di sini. Seluruh status `WAITING_FOR_EXPERIMENT` (rencana, belum dijalankan).

| ID | Nama Skenario | Objek Utama | Primitif (CORE-x) | Jenis Pengujian | Metrik Utama | Status |
|---|---|---|---|---|---|---|
| EXP-01 | Correctness dan rejection vault identitas | `identity::vault` (`seal`/`unseal`) | CORE-3, CORE-5 | Correctness, wrong-key rejection, modified-ciphertext rejection, nonce handling | Proporsi roundtrip sukses (%), proporsi rejection benar (%) | WAITING_FOR_EXPERIMENT |
| EXP-02 | Correctness dan rejection handshake Noise_IK | `crypto::handshake`, `session::run_session` (fase handshake) | CORE-1, CORE-2 | Correctness, key agreement consistency, wrong-key/unknown-peer rejection | Pass/fail test, latensi handshake (ms) | WAITING_FOR_EXPERIMENT |
| EXP-03 | Consistency transport sesi terenkripsi | `session::run_session` (fase transport), `transport::frame` | CORE-3 (transport) | Encryption-decryption consistency, oversize/keepalive handling | Pass/fail test, overhead ciphertext (byte) | WAITING_FOR_EXPERIMENT |
| EXP-04 | Correctness invite/fingerprint/contact store | `contacts::mod` | CORE-4, helper encoding | Serialization-deserialization consistency, KDF consistency, wrong-key rejection | Pass/fail test, panjang string invite (karakter) | WAITING_FOR_EXPERIMENT |
| EXP-05 | Benchmark Argon2id dan ciphertext expansion | `identity::vault` (performa) | CORE-5, CORE-3 | Performance benchmark, ciphertext expansion | Waktu unlock vault (ms: mean/median/stdev), ukuran vault (byte) | WAITING_FOR_EXPERIMENT |

## Cakupan Kandidat Brief yang Tidak Berlaku (N/A)

| Kandidat | Alasan |
|---|---|
| Known-answer test (KAT) | Tidak ditemukan test vector standar resmi yang dipakai test suite AKSARA — seluruh test bersifat roundtrip/property-based |
| Modified associated-data rejection | AKSARA tidak memakai AAD pada ketiga instance ChaCha20-Poly1305 manapun |
| Replay rejection | Tidak ditemukan mekanisme replay-protection eksplisit di source yang diaudit |

## Referensi

`12_TEST_PLAN.md` (TAHAP 13).
