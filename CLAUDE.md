# AKSARA

Chat P2P terminal serverless — dua orang chat end-to-end terenkripsi tanpa server perantara sama sekali. Noise_IK handshake, transport LAN (mDNS) + Tor onion service, vault identitas Argon2id/ChaCha20-Poly1305. Rust, single binary, ratatui TUI.

Nama AKSARA = backronym "Authenticated Key-based Secure Autonomous Relay Architecture". Arah pengembangan: komersial.

**Bukan proyek yang sama dengan:**
- `CARAKA-APP` (Android, Kotlin, mesh/emergency chat) — tidak terkait sama sekali.
- `Caraka` (Rust/Tauri, sibling folder) — proyek TERPISAH (Tor-only, GUI desktop, sudah M0-M2). Jangan disatukan atau dianggap sama.

**Status:** v0.2.0 disiapkan (belum di-tag). Build + `cargo test` hijau (45 test),
`cargo clippy -- -D warnings` bersih — keduanya ditegakkan CI di setiap push/PR,
jadi perubahan harus lolos keduanya. Lisensi: proprietary (all rights reserved).

## Build & test
```bash
cargo check
cargo test
cargo build --release
```

## Struktur
Single crate, `src/main.rs` sebagai entry point. Modul: `identity` (keypair + vault), `crypto` (Noise_IK handshake), `transport` (LAN mDNS + Tor onion service), `contacts`, `tui` (ratatui).
