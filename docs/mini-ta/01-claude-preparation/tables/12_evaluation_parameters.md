# Tabel 12 — Parameter Evaluasi

7 metrik unik lintas 5 kelompok eksperimen `12_TEST_PLAN.md` — memenuhi rentang 4-8 metrik yang disyaratkan `CLAUDE_PREPARATION_BRIEF.md` §Batas Scope.

**Diperbarui 2026-07-27 dengan nilai terukur.** Seluruh angka performa berlaku **hanya** untuk lingkungan uji di `14_CHAPTER_CONTENT_PACK.md` BAB V §5.1 (Intel Core i7-1165G7 4C/8T, RAM 11,79 GB, Windows 11 10.0.26200, `rustc 1.97.0`, profil release) — tidak digeneralisasi ke kelas hardware lain.

| # | Metrik | Satuan | Dipakai pada | Metode Analisis | Baseline/Ekspektasi | Hasil Terukur | Status |
|---|---|---|---|---|---|---|---|
| 1 | Proporsi roundtrip sukses | % | EXP-01 | Deskriptif (persentase) | 100% | **100%** (10/10 run CLI, invite identik seluruh run) | MEASURED |
| 2 | Proporsi rejection benar | % | EXP-01 | Deskriptif (persentase) | 100% | **100%** (passphrase salah → exit 1, pesan generik) | MEASURED |
| 3 | Pass/fail unit test | biner | EXP-01, 02, 03, 04 | Tabulasi | Seluruh test pass | **46/46 pass**, 0 fail, 0 ignored | MEASURED |
| 4 | Latensi handshake Noise_IK | ms | EXP-02 | Deskriptif (mean, median, stdev) | Tidak diklaim sebelum diukur | **Batas atas < 0,86 ms** (95% CI). Selisih berpasangan −0,15 ms (sd 1,91; n=19) — di bawah resolusi metode eksternal, **bukan nilai titik** | PARTIAL |
| 5 | Overhead ciphertext (tag AEAD) | byte | EXP-03 | Perbandingan langsung terhadap spesifikasi | +16 byte (tag Poly1305) | **+16 byte** terukur pada instance vault (108 − 16 salt − 12 nonce − 64 plaintext). Instance Noise transport tidak diukur | PARTIAL |
| 6 | Panjang string invite code | karakter | EXP-04 | Deskriptif, pengecekan konsistensi | 86 karakter (64 byte base64url tanpa padding, tanpa suffix onion) | **86 karakter** konsisten pada 5 keypair acak | MEASURED |
| 7 | Waktu unlock vault (Argon2id) | ms | EXP-05 | Deskriptif (mean, median, stdev, min/max) | Dibandingkan terhadap klaim komentar kode "~100ms" (`DOCUMENTED_ONLY`) | Neto **mean 47,99** · median 45,08 · sd 11,41 · min 26,99 · max 86,30 (n=30). End-to-end mean 68,47 · median 64,15 · sd 12,47. **Klaim "~100 ms" TERKOREKSI** | MEASURED |

**Catatan metode metrik 7**: pengukuran memakai jam dinding dari luar proses (`Measure-Command`), sehingga 30 run kontrol tanpa Argon2id (mean 20,48 ms) dijalankan untuk memisahkan biaya derivasi kunci dari overhead spawn proses. Angka "neto" adalah selisih berpasangan kedua deret.

## Metrik Sekunder/Opsional

| Metrik | Satuan | Hasil | Status |
|---|---|---|---|
| Ukuran ciphertext vault | byte | **Tepat 108 byte** pada 5 vault independen — terverifikasi lewat pengukuran ukuran file, bukan hanya dikutip dari spesifikasi | MEASURED |
| Memory usage puncak (RSS) saat Argon2id berjalan | MiB | Tidak diukur. Hanya parameter statis **19 MiB** yang diketahui dari `argon2_params()` | WAITING_FOR_EXPERIMENT (opsional) |

## Referensi

`12_TEST_PLAN.md` §Ringkasan 5 Kelompok Eksperimen (TAHAP 13).
