# Tabel 13 — Pembagian Tugas Anggota

Reproduksi tabel `09_SCOPE_AND_TEAM_PLAN.md` §8 sebagai artefak tabel siap-pakai BAB I/lampiran. Nama anggota **CONFIRMED** 2026-07-27 (sumber: `00-template/PROPOSAL CARAKA (2).docx`, ditunjuk pengguna). Pemetaan nama ke peran mengikuti urutan pada proposal dan **boleh ditukar** kelompok — cakupan modul yang menentukan, bukan urutannya — belum ada nama asli yang dapat diverifikasi.

| Anggota | Modul | Tugas Teknis | Eksperimen (rencana TAHAP 13) | Bagian Laporan |
|---|---|---|---|---|
| **Andika Aryansyach Fauzan** (2322101878) | `src/identity/` (`keypair.rs`, `vault.rs`), `src/crypto/handshake.rs` (primitif) | Audit/verifikasi ulang inventarisasi primitif CORE-1..7; jelaskan generation kunci, layout vault, alur `seal()`/`unseal()`, parameter Argon2id | EXP-01 (correctness/rejection vault), EXP-05 (benchmark Argon2id) | BAB II (primitif kriptografi), BAB IV bagian identity/vault |
| **Mahendra Nur Hidayat** (2322101937) | `src/transport/` (`mod.rs`, `lan.rs`, `tor.rs`, `frame.rs`), `src/session/mod.rs` | Dokumentasikan alur protokol end-to-end; jelaskan orkestrasi `run_session`, model konkurensi/cancel-safety, framing | EXP-02 (handshake Noise_IK), EXP-03 (transport sesi) | BAB IV (inti — protokol komunikasi), BAB III (metodologi pengujian protokol) |
| **Rafi Putra Fadlurrahman** (2322101963) | `src/contacts/mod.rs`, `src/tui/` (titik integrasi kripto), `src/main.rs`/`src/error.rs`; lintas-modul: testing, benchmarking, analisis, dokumentasi | Jelaskan invite/fingerprint binding, integrasi kripto TUI/main; agregasi hasil pengujian; susun threat model dan risk register; koordinasi referensi/diagram/tabel/content pack | EXP-04 (invite/fingerprint/contact store); agregasi lintas-eksperimen | BAB I (pendahuluan), BAB V (pengujian dan analisis, gabungan hasil), BAB VI (penutup) |

## Catatan Keseimbangan

Anggota kedua mendapat lebih banyak file karena modul transport secara alami lebih terpecah (LAN/Tor/framing terpisah); kompleksitas konseptual tetap seimbang dengan Anggota 1. Anggota 3 memikul beban integrasi/dokumentasi lebih besar sebagai kompensasi cakupan modul teknis yang lebih kecil.

## Referensi

`09_SCOPE_AND_TEAM_PLAN.md` §8 (TAHAP 8), `12_TEST_PLAN.md` (TAHAP 13, kolom eksperimen diperbarui sesuai 5 kelompok final).
