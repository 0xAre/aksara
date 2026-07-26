# Tabel 12 — Parameter Evaluasi

7 metrik unik lintas 5 kelompok eksperimen `12_TEST_PLAN.md` — memenuhi rentang 4-8 metrik yang disyaratkan `CLAUDE_PREPARATION_BRIEF.md` §Batas Scope. Seluruh nilai `WAITING_FOR_EXPERIMENT` sampai eksperimen dijalankan.

| # | Metrik | Satuan | Dipakai pada | Metode Analisis | Baseline/Ekspektasi |
|---|---|---|---|---|---|
| 1 | Proporsi roundtrip sukses | % | EXP-01 | Deskriptif (persentase) | 100% |
| 2 | Proporsi rejection benar | % | EXP-01 | Deskriptif (persentase) | 100% |
| 3 | Pass/fail unit test | biner | EXP-01, 02, 03, 04 | Tabulasi | Seluruh test pass |
| 4 | Latensi handshake Noise_IK | ms | EXP-02 | Deskriptif (mean, median, stdev) | Tidak diklaim sebelum diukur |
| 5 | Overhead ciphertext (tag AEAD) | byte | EXP-03 | Perbandingan langsung terhadap spesifikasi | +16 byte (tag Poly1305) |
| 6 | Panjang string invite code | karakter | EXP-04 | Deskriptif, pengecekan konsistensi | ~86 karakter (64 byte base64url tanpa padding, tanpa suffix onion) |
| 7 | Waktu unlock vault (Argon2id) | ms | EXP-05 | Deskriptif (mean, median, stdev, min/max) | Dibandingkan terhadap klaim komentar kode "~100ms" (`DOCUMENTED_ONLY`) |

## Metrik Sekunder/Opsional

| Metrik | Satuan | Status |
|---|---|---|
| Ukuran ciphertext vault | byte | Deterministik dari spesifikasi (108 byte), diverifikasi ulang saat eksekusi EXP-05 |
| Memory usage puncak (RSS) saat Argon2id berjalan | MiB | Opsional — butuh tooling profiling tambahan yang belum dikonfirmasi tersedia |

## Referensi

`12_TEST_PLAN.md` §Ringkasan 5 Kelompok Eksperimen (TAHAP 13).
