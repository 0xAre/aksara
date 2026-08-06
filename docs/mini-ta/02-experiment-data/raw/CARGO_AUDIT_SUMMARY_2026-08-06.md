# Cargo Audit — Ringkasan Hasil (2026-08-06)

Pengujian kerentanan dependency AKSARA menggunakan `cargo audit`, yang mencocokkan
seluruh crate di `Cargo.lock` terhadap RustSec Advisory Database (basis data CVE
resmi ekosistem Rust, https://rustsec.org).

## Lingkungan Pengujian

| Item | Nilai |
|---|---|
| Tool | `cargo-audit` 0.22.2 |
| Cargo / rustc | 1.97.0 |
| Advisory DB | 1189 advisory (snapshot lokal `~/.cargo/advisory-db`, di-fetch saat run) |
| Commit | `e1eb104` (branch `main`) |
| Crate discan | 566 dependency (`Cargo.lock`) |
| Perintah | `cargo audit` dan `cargo audit --json` |
| Raw output | `cargo_audit_2026-08-06.txt`, `cargo_audit_2026-08-06.json` (folder ini) |

Catatan: sejumlah pengecekan status "yanked" gagal karena timeout jaringan ke
registry crates.io (`request could not be completed in the allotted timeframe`).
Ini tidak mempengaruhi pencocokan terhadap advisory database (yang berjalan dari
salinan lokal), hanya melewatkan sebagian pengecekan yanked real-time.

## Hasil

**1 vulnerability, 6 warning.**

| # | Crate | Versi | ID | Severity | Jenis | Status |
|---|---|---|---|---|---|---|
| 1 | `rsa` | 0.9.10 | RUSTSEC-2023-0071 | 5.9 (medium) | Vulnerability — Marvin Attack (timing side-channel pada key recovery RSA) | Tidak ada versi perbaikan tersedia dari upstream |
| 2 | `bincode` | 2.0.1 | RUSTSEC-2025-0141 | — | Warning — unmaintained | — |
| 3 | `paste` | 1.0.15 | RUSTSEC-2024-0436 | — | Warning — unmaintained | — |
| 4 | `event-listener` | 5.4.1 | RUSTSEC-2026-0221 | — | Warning — unsound (`!Send` lolos batas thread via `StackSlot`) | — |
| 5 | `lru` | 0.12.5 | RUSTSEC-2026-0002 | — | Warning — unsound (`IterMut` melanggar Stacked Borrows) | — |
| 6 | `memmap2` | 0.9.10 | RUSTSEC-2026-0186 | — | Warning — unsound (unchecked pointer offset) | — |
| 7 | `spin` | 0.9.8 | — | — | Warning — yanked | — |

## Analisis untuk Laporan

- **Temuan #1 (`rsa`, medium) bukan bagian dari kode kripto AKSARA sendiri.**
  `cargo tree -i rsa` (`cargo_tree_rsa_2026-08-06.txt`) membuktikan `rsa` masuk
  sebagai dependency transitif lewat rantai Tor: `arti-client` /
  `tor-hsservice` / `tor-cell` → `tor-key-forge` → `ssh-key-fork-arti` → `rsa`.
  Primitif kriptografi milik AKSARA sendiri (identity/session/handshake) tetap
  `ed25519-dalek`, `x25519-dalek`, `snow`, `argon2`, `chacha20poly1305`,
  `blake2` — sudah tercatat di `PROJECT_MEMORY.md` §Versi Ground Truth, tidak
  ada `rsa` di daftar itu.
- Marvin Attack (RUSTSEC-2023-0071) adalah side-channel timing pada operasi
  RSA decrypt/sign (PKCS#1 v1.5). Crate `rsa` di sini dipakai `arti-client`
  untuk sebagian operasi kunci Tor (bukan untuk Noise_IK/handshake AKSARA),
  dan upstream belum merilis versi perbaikan — status `NEEDS_CONFIRMATION`
  untuk dampak nyata terhadap AKSARA, karena bergantung path pemakaian
  internal `arti-client` yang berada di luar `src/` AKSARA.
- 6 warning lainnya seluruhnya dependency transitif (bukan dependency
  langsung AKSARA di `Cargo.toml`), tidak ada exploit/CVE resmi terkait —
  kategori "unmaintained"/"unsound"/"yanked" adalah peringatan kualitas,
  bukan vulnerability bernomor CVE/RUSTSEC vulnerability.
- Hasil ini cocok dijadikan entri baru di `08_THREAT_MODEL.md` (risk register)
  dan/atau `15_CLAIM_EVIDENCE_CITATION_MAP.md` sebagai Claim ID baru dengan
  Evidence Code menunjuk ke `cargo_audit_2026-08-06.json` — **belum
  ditambahkan ke dokumen manapun**, ini murni hasil mentah sesuai permintaan
  pengguna.

## Cara Reproduksi

```powershell
cargo install cargo-audit   # sekali saja, tidak mengubah Cargo.lock proyek
cargo audit                 # human-readable
cargo audit --json          # machine-readable
cargo tree -i rsa           # bukti rantai dependency untuk temuan #1
```
