# 00 — Inventarisasi Tool dan MCP

Dibuat: TAHAP 1, sesuai `docs/mini-ta/CLAUDE_PREPARATION_BRIEF.md`.
Lingkungan: Windows 11, PowerShell, repo `E:\Project APP\AKSARA`.

## Tool lokal

| Tool/MCP | Fungsi | Lokasi/Command | Status | Penggunaan |
|----------|--------|----------------|--------|------------|
| Node.js | Runtime untuk Mermaid CLI | `node --version` → v22.16.0 | READY | Menjalankan `mmdc` |
| npm | Package manager Node | `npm --version` → 10.9.2 | READY | Install/repair `mmdc` |
| Mermaid CLI (`mmdc`) | Render diagram `.mmd` → SVG/PNG | `C:\Users\LENOVO\AppData\Roaming\npm\mmdc.ps1` (`@mermaid-js/mermaid-cli`, global) | READY (diperbaiki sesi ini — instalasi awal korup: `node_modules/@mermaid-js/mermaid-cli` kosong tanpa `package.json`). Diinstal ulang dengan `PUPPETEER_SKIP_DOWNLOAD=true` lalu diarahkan ke Chrome sistem via `-p puppeteer-config.json`. Diverifikasi dengan smoke test (SVG dan PNG, exit code 0). | Render seluruh diagram TAHAP 11 |
| `puppeteer-config.json` | Konfigurasi Puppeteer agar `mmdc` memakai Chrome sistem, bukan Chromium bawaan (yang gagal didownload) | `docs/mini-ta/puppeteer-config.json` → `executablePath: C:\Program Files\Google\Chrome\Application\chrome.exe` | READY | Argumen `-p` pada setiap pemanggilan `mmdc` |
| PlantUML | Alternatif diagram (prioritas 2) | `Get-Command plantuml` → tidak ditemukan | NOT_FOUND | Tidak dipakai — Mermaid tersedia (prioritas 1 sudah terpenuhi) |
| Graphviz (`dot`) | Alternatif diagram (prioritas 3) | `Get-Command dot` → tidak ditemukan | NOT_FOUND | Tidak dipakai |
| D2 | Alternatif diagram (prioritas 4) | `Get-Command d2` → tidak ditemukan | NOT_FOUND | Tidak dipakai |
| Pandoc | Konversi dokumen | `Get-Command pandoc` → tidak ditemukan | NOT_FOUND | Tidak dibutuhkan — seluruh output TAHAP ini Markdown/YAML/CSV, bukan DOCX/PDF |
| Cargo / rustc | Build & test AKSARA | `cargo --version` → 1.97.0; `rustc --version` → 1.97.0 | READY | Build aplikasi untuk verifikasi fungsi (TAHAP 12), referensi versi toolchain |
| Git | Riwayat repo | Terpasang, repo aktif di `main` | READY | Audit commit relevan-kripto (TAHAP 2) |
| Browser automation (Claude Browser / Claude in Chrome) | Screenshot & interaksi halaman web | Tersedia sebagai MCP tool | NOT_APPLICABLE | AKSARA adalah TUI terminal (ratatui), bukan aplikasi web — tool ini tidak bisa menangkap jendela terminal |
| Screenshot tool (OS/terminal-level) | Menangkap tangkapan layar aplikasi TUI aktual | Tidak ada tool computer-use/screen-capture native di environment ini | NOT_FOUND | **Blocking** untuk TAHAP 12 — lihat `14_OPEN_QUESTIONS.md` |
| Tool PDF | Ekspor/inspeksi PDF | Tidak diperiksa lebih lanjut — tidak dibutuhkan tahap ini | NOT_APPLICABLE | — |
| Tool DOI dedicated | Resolusi DOI otomatis | Tidak ada tool khusus | NOT_FOUND | Verifikasi DOI dilakukan manual via MCP web search / halaman resmi (lihat `MCP_RESEARCH_LOG.md`) |
| Tool GitHub (`gh` CLI) | Operasi GitHub lokal | Tidak diperiksa — MCP `github` tersedia sebagai gantinya | NOT_APPLICABLE | — |

## MCP server

| Tool/MCP | Fungsi | Status | Penggunaan dalam paket ini |
|----------|--------|--------|------------------------------|
| `context7` | Dokumentasi resmi library/crate (versi terkini) | READY | Verifikasi API/parameter crate: `snow`, `chacha20poly1305`, `argon2`, `ed25519-dalek`, `x25519-dalek`, `blake2`, `mdns-sd`, `arti-client`, `ratatui` |
| `github` | Baca repo/commit/release publik | READY | Cross-check repo resmi crate (mis. `snow`, `arti-client`) bila dibutuhkan sebagai referensi sekunder |
| `tavily` | Web search + ekstraksi halaman | **GAGAL TOTAL sejak TAHAP 4** (2026-07-26) — seluruh 4 percobaan pertama gagal HTTP 432 (indikasi kuota/plan API habis, bukan transient). Tidak dicoba ulang. | **JANGAN dipakai sebagai sumber utama** — cadangan opsional terakhir saja, cek dulu apakah kuota sudah reset sebelum mengandalkannya |
| `ydc-server` (you-search/you-research/you-contents) | Discovery web, sintesis multi-sumber, baca URL spesifik | READY — **terbukti andal**, dipakai sebagai sumber utama riset TAHAP 4/9 (26 query sukses) | **Sumber utama/prioritas pertama** untuk web search & riset referensi (standar, RFC, NIST, paper, dokumentasi library) — pakai `include_domains` diarahkan ke domain resmi (`datatracker.ietf.org`, `csrc.nist.gov`, `docs.rs`, dst.) agar hasil tetap otoritatif |
| `academic-core` | Ingest & index paper akademik | READY (opsional) | Tidak dipakai kecuali dibutuhkan indexing paper dalam jumlah besar |
| `semantic-scholar` | Pencarian paper akademik, metadata, sitasi | **RATE-LIMITED sejak TAHAP 4** (2026-07-26) — hanya 1 query pertama sukses, seluruh percobaan berikutnya gagal `RateLimitError (retry_after: 60)` meski sudah menunggu beberapa menit. Kemungkinan API key/kuota bersama sudah terpakai. | **JANGAN diandalkan sebagai sumber utama** — coba paling banyak 1 query untuk cek apakah kuota sudah reset, lalu langsung alihkan ke `ydc-server` bila gagal. Jangan retry berulang. |
| `zotero` | Baca item/metadata dari library referensi pengguna | READY | Dicek bila pengguna sudah punya koleksi referensi tersimpan; tidak wajib |
| `sequential-thinking` | Bantuan penalaran terstruktur | READY (opsional) | Tidak dipakai sebagai sumber evidence, hanya bila dibutuhkan penalaran berlapis |
| `wolfram-alpha` | Komputasi matematis | READY (opsional) | Tidak relevan untuk audit ini |
| `playwright` / Claude Browser / Claude in Chrome | Otomasi browser | READY tapi NOT_APPLICABLE | AKSARA bukan aplikasi web |
| `office-word-mcp` | Edit dokumen Word | READY tapi TIDAK DIPAKAI | Brief melarang eksplisit mengedit DOCX — hasil paket ini dipakai Codex, bukan ditulis langsung ke `Cetak_TA_rev3.docx` |
| `stitch` | Desain UI/mockup web | NOT_APPLICABLE | Tidak relevan (bukan aplikasi web, dan brief melarang diagram dari AI image generator) |
| `cloudflare-api`, `papersflow`, `gitlab`, `vercel` | — | NEEDS_AUTH | Tidak diotorisasi di sesi ini; tidak relevan untuk paket TA ini |

## Ringkasan kesiapan

- Diagram: **siap penuh** — Mermaid CLI prioritas-1 berfungsi (source `.mmd` + render SVG/PNG).
- Riset referensi: **siap, dengan catatan** — `tavily` dan `semantic-scholar` bermasalah sejak TAHAP 4 (lihat baris masing-masing di atas dan detail lengkap di `references/MCP_RESEARCH_LOG.md`). `ydc-server` (you-search) terbukti sebagai sumber utama yang andal (31 referensi berhasil diverifikasi TAHAP 4/9 hampir seluruhnya lewat tool ini) — **prioritaskan `ydc-server` lebih dulu** untuk riset referensi berikutnya, bukan cadangan terakhir.
- Screenshot aplikasi aktual: **terblokir** — tidak ada tool capture layar/terminal di environment ini. Build & run untuk verifikasi fungsi tetap bisa dilakukan; pengambilan gambar aktual perlu dilakukan manual oleh pengguna. Dicatat di `14_OPEN_QUESTIONS.md` dan `HANDOFF_TO_CODEX.yaml`.
- Build project: **siap** — `cargo`/`rustc` 1.97.0 terpasang, `target/debug` menunjukkan build sebelumnya berhasil.
