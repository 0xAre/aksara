# TUGAS UTAMA

Susun DOKUMEN AKHIR mini-TA AKSARA (mata kuliah Implementasi Kriptografi) sebagai file DOCX baru:

docs/mini-ta/04-output/AKSARA_LAPORAN_FINAL.docx

**Entry point WAJIB dibaca lebih dulu, dalam urutan ini:**

1. `docs/mini-ta/01-claude-preparation/HANDOFF_TO_CODEX.yaml` — dirancang khusus sebagai ringkasan siap pakai untuk tugas ini, baca seluruhnya.
2. `docs/mini-ta/01-claude-preparation/16_DOCUMENT_FORMAT_SPEC.md` — aturan format WAJIB, sudah final dan terverifikasi terhadap Peraturan Direktur Poltek SSN Pedoman Pelaksanaan Tugas Akhir (2024) + pengukuran XML template.
3. `docs/mini-ta/01-claude-preparation/14_CHAPTER_CONTENT_PACK.md` — isi/narasi tiap subbab BAB I-VI, sudah lengkap.
4. `docs/mini-ta/01-claude-preparation/15_CLAIM_EVIDENCE_CITATION_MAP.md` — WAJIB baca bagian "Klaim Kritis Anti-Overclaim" sebelum menulis satu paragraf pun.

**Ini BUKAN proposal singkat, dan BUKAN dokumen yang formatnya diambil dari CARAKA.** Ini laporan akhir 6-BAB yang sudah `ready_for_codex: YES` — pekerjaan riset/audit/analisis SUDAH selesai di seluruh sesi sebelumnya. Tugas Anda murni menyusunnya jadi DOCX yang rapi mengikuti format resmi, BUKAN meneliti ulang atau mengarang isi baru.

# TEMPLATE FORMAT — MANA YANG DIPAKAI, MANA YANG TIDAK

| File | Dipakai untuk | Catatan |
|---|---|---|
| `docs/mini-ta/00-template/Cetak TA_rev3.docx` | **Template format fisik** — style Word, margin, font, heading, penomoran, tata letak sampul, header/footer | Punya orang lain (topik QRNG, Poltek SSN 2025). Sudah dikonfirmasi seluruh nilai XML-nya cocok dengan pedoman resmi. **Jangan ambil satu pun isi/fakta dari dalamnya.** |
| `docs/mini-ta/01-claude-preparation/16_DOCUMENT_FORMAT_SPEC.md` | **Aturan format yang mengikat** — sudah didistilasi dari pedoman resmi + template di atas | Kalau ada perbedaan antara file ini dan apa yang terlihat di Cetak TA_rev3.docx, **dokumen ini yang menang** (sudah memasukkan koreksi dari pedoman resmi). |
| `docs/mini-ta/00-template/PROPOSAL CARAKA (2).docx` | **TIDAK DIPAKAI SAMA SEKALI untuk tugas ini.** | Proyek lain (mesh offline, Ascon, CLAMP). Fungsinya (identitas anggota + preseden struktur ringkas) sudah selesai dipakai sesi sebelumnya dan hasilnya sudah ada permanen di `16_DOCUMENT_FORMAT_SPEC.md` §1 dan §3.2. **Jangan membuka file ini untuk tugas ini** — tidak ada alasan untuk membukanya lagi, dan membukanya hanya menambah risiko istilah/fakta CARAKA ikut tercampur. |

# FAKTA YANG SUDAH CONFIRMED (pakai langsung)

```yaml
title: >
  AKSARA (Authenticated Key-based Secure Autonomous Relay Architecture):
  Chat Terminal Tanpa Server — Implementasi dan Evaluasi Keamanan Protokol
  Noise_IK, Siklus Hidup Kunci, dan Threat Model
title_banned_phrases: ["Tanpa Jejak", "Anti-Sadap", "Sepenuhnya Anonim", "Terbukti Aman"]
document_type: Tugas Mata Kuliah Implementasi Kriptografi (BUKAN Tugas Akhir formal — tidak ada sidang/penguji)
work_type: Kelompok, 3 anggota
study_program: Rekayasa Sistem Kriptografi
institution: Politeknik Siber dan Sandi Negara
year: 2026
members:
  - {name: "Andika Aryansyach Fauzan", nim: "2322101878", role: "Core developer — fullstack"}
  - {name: "Mahendra Nur Hidayat", nim: "2322101937", role: "Dokumentasi akhir"}
  - {name: "Rafi Putra Fadlurrahman", nim: "2322101963", role: "User testing"}
version: "v0.2.1"
```

# STRUKTUR DOKUMEN — IKUTI `16_DOCUMENT_FORMAT_SPEC.md` §3.1 PERSIS

Bagian awal: Sampul → Abstrak (Indonesia, 200-300 kata, spasi tunggal, TANPA sitasi, maks 7 kata kunci) → Daftar Isi → Daftar Gambar → Daftar Tabel.

Bagian utama — 6 BAB, 34 subbab total, seluruhnya sudah `READY` di `14_CHAPTER_CONTENT_PACK.md`:

- BAB I PENDAHULUAN (6 subbab)
- BAB II KAJIAN PUSTAKA (10 subbab)
- BAB III METODOLOGI PENELITIAN (5 subbab)
- BAB IV PERANCANGAN DAN IMPLEMENTASI (7 subbab — bab inti, paling rinci)
- BAB V PENGUJIAN DAN ANALISIS (3 subbab — SUDAH berisi data eksperimen nyata, bukan rencana)
- BAB VI PENUTUP (3 subbab)

Bagian akhir: Daftar Pustaka (IEEE, dari `references/REFERENCES.bib`, 40 entry).

**JANGAN** menambahkan lembar pengesahan, lembar pernyataan orisinalitas, lembar persetujuan, kata pengantar, abstract bahasa Inggris, daftar notasi/lampiran/riwayat hidup — semuanya sudah sengaja dihapus (`16_DOCUMENT_FORMAT_SPEC.md` §3.2), jangan dikembalikan.

# CARA MENULIS TIAP SUBBAB

Untuk setiap subbab, `14_CHAPTER_CONTENT_PACK.md` sudah menyediakan 13 field (tujuan, outline paragraf, kalimat topik, fakta codebase, evidence, referensi, Claim ID, diagram, tabel, eksperimen, klaim yang boleh, klaim yang dilarang, status kesiapan). Tugas Anda: **ekspansi field-field ini menjadi prosa akademik penuh** — bukan menyalin field-nya secara literal ke dokumen, dan bukan mengarang fakta baru di luar field yang tersedia.

Ikuti `16_DOCUMENT_FORMAT_SPEC.md` §6 untuk penomoran (`BAB IV` / `IV.1 JUDUL SUBBAB` kapital semua / `IV.1.1 Judul Anak Subbab` Title Case), §7 untuk gambar/tabel (judul tabel di atas, judul gambar di bawah, penomoran `Tabel 4.1`/`Gambar 4.1` per-BAB), §8 untuk sitasi IEEE (nomor sebelum tanda baca, spasi sebelum kurung siku pembuka).

## Klaim yang DILARANG ditulis (dari `15_CLAIM_EVIDENCE_CITATION_MAP.md`)

1. "AKSARA menggunakan tanda tangan digital Ed25519" — HANYA dipakai untuk bahan fingerprint, TIDAK ADA `sign()`/`verify()` aktif.
2. "AKSARA terbukti memiliki forward secrecy" — status `DOCUMENTED_ONLY`, diwarisi dari spesifikasi Noise_IK, tidak diverifikasi test AKSARA sendiri.
3. Mengutip "~100ms" Argon2id sebagai fakta — sudah **dikoreksi** jadi mean 47,99 ms neto (n=30, sd 11,41) pada hardware uji spesifik (BAB V §5.1). Selalu sertakan n, sebaran, dan environment.
4. "ChaCha20-Poly1305 melindungi dari nonce reuse" tanpa hedge — TIDAK misuse-resistant.
5. "AKSARA selalu memverifikasi identitas peer" tanpa kualifikasi "untuk kontak yang sudah dikenal" — trust-on-first-use pada kontak baru.
6. Klaim absolut apa pun ("100% aman", "tidak dapat diretas").
7. Menyatakan latensi handshake sebagai nilai titik — yang ada hanya batas atas < 0,86 ms.
8. Menyatakan 46/46 test lolos berarti sistem "terbukti aman".

# GAMBAR DAN TABEL — SUDAH TERSEDIA, TINGGAL DIPAKAI

**Jangan membuat diagram atau audit kode baru.** Semua sudah siap:

- **Gambar**: `docs/mini-ta/01-claude-preparation/11_FIGURE_MANIFEST.md` mendaftar SELURUH 18 gambar (7 diagram `diagrams/rendered/png/` + 11 screenshot aplikasi `screenshots/*.png`), lengkap dengan judul, keterangan, dan BAB tujuannya. Sisipkan persis sesuai kolom "Bab" di manifest itu, beri caption sesuai kolom "Judul".
  - **Penting untuk SS-06 dan SS-07**: baca catatan §5-6 di manifest sebelum menulis keterangan gambar — screenshot komunikasi via Tor TIDAK membuktikan jalur Tor sendirian, harus dikombinasikan dengan bukti jaringan berbeda + argumen `LAN_AUTO_TIMEOUT` di keterangan gambar.
- **Tabel**: `docs/mini-ta/01-claude-preparation/13_TABLE_MANIFEST.md` + `tables/01`..`13_*.md` — 13 tabel siap pakai, sudah berisi hasil eksperimen aktual (bukan rencana) untuk TBL-11/TBL-12.

# QUALITY GATE — SUDAH TERPENUHI, JANGAN DIEVALUASI ULANG

`HANDOFF_TO_CODEX.yaml` `readiness.ready_for_codex: YES` — 17/17 syarat quality gate brief sudah terpenuhi, tidak ada kontradiksi kritis. Anda tidak perlu mengevaluasi ulang apakah dokumen "siap" — itu sudah diputuskan. Fokus pada eksekusi penulisan.

# METODE PENGEDITAN DOCX

1. Gunakan Office Word MCP apabila tersedia.
2. Jika tidak tersedia: Python (`python-docx`, `lxml`, `zipfile`, manipulasi OOXML bila perlu).
3. Boleh memakai `docs/mini-ta/03-codex-work/` sebagai folder kerja sementara (draft, style extraction dari template, dll.) — output final tetap harus di `docs/mini-ta/04-output/`.
4. Ambil style Word (Heading 1/2/3, Normal, Caption, dst.) dari `Cetak TA_rev3.docx`, jangan bangun style baru dari nol.
5. Render ke PDF untuk pemeriksaan visual (LibreOffice/Word bila tersedia mekanismenya).

File final WAJIB `.docx`.

# DAFTAR ISI DAN FIELD WORD

Heading pakai style heading Word yang benar (bukan bold manual). Bangkitkan Daftar Isi/Gambar/Tabel otomatis. Jika field TOC tidak bisa diperbarui otomatis lewat library: sisipkan field TOC yang benar via OOXML, aktifkan `updateFields` saat dokumen dibuka, dan dokumentasikan bahwa pengguna perlu Ctrl+A lalu F9 saat pertama membuka file.

# QUALITY ASSURANCE

1. Render `AKSARA_LAPORAN_FINAL.docx` ke PDF, periksa SETIAP halaman (bukan cuma halaman pertama).
2. Pastikan tidak ada: teks terpotong, tabel keluar margin, gambar bertumpuk/pecah, caption terpisah tidak wajar, halaman kosong berlebihan, heading tertinggal di bawah halaman, header/footer rusak (footer "Politeknik Siber dan Sandi Negara" harus konsisten dari Abstrak sampai Daftar Pustaka), nomor halaman salah (Romawi kecil di bagian awal, Arab mulai BAB I), font berubah tanpa alasan, referensi gambar/tabel yang salah, daftar isi tidak sinkron.
3. Perbaiki, render ulang, ulangi sampai bersih.

# VALIDASI AKHIR

Cari di seluruh dokumen istilah: `CARAKA`, `CLAMP`, `Compact Lightweight Authenticated Mesh Protocol`, `Ascon-MAC`, `Ascon-Hash256`, `Epidemic Sync`, `Controlled Flooding`. **Tidak boleh ada satupun** — dokumen ini tidak pernah menggunakan proyek CARAKA sebagai sumber substansi.

Cek juga: judul persis seperti "Fakta yang Sudah CONFIRMED" (tanpa frasa terlarang), 8 klaim terlarang di atas tidak muncul di prosa manapun, seluruh gambar/tabel dirujuk dalam narasi, rumusan masalah (BAB I) konsisten dengan kesimpulan (BAB VI §6.1), tidak ada hasil eksperimen yang diubah/dibulatkan dari yang tertulis di BAB V, tidak ada daftar pustaka fiktif (hanya dari `references/REFERENCES.bib`).

# OUTPUT WAJIB

1. `docs/mini-ta/04-output/AKSARA_LAPORAN_FINAL.docx` — dokumen final.
2. `docs/mini-ta/04-output/GENERATION_LOG.md` — ringkas: keputusan pemilihan gambar/tabel per BAB (kalau ada opsi), masalah render yang ditemukan dan diperbaiki, bagian mana pun yang ditandai `[PERLU KONFIRMASI]` karena field content pack kurang jelas.

Setelah selesai, perbarui (jangan buat file baru):
- `docs/mini-ta/WORKFLOW_STATE.yaml` — `workflow.next_action` dari `codex_menyusun_docx_bab_1_sampai_6` menjadi selesai, catat tanggal dan commit.
- `docs/mini-ta/01-claude-preparation/PROGRESS.md` — tambahkan entri bahwa DOCX final sudah dihasilkan Codex, tanggal, lokasi file.

# LAPORAN AKHIR

Laporkan ke pengguna: jumlah halaman hasil akhir, gambar/tabel apa saja yang disisipkan per BAB, masalah format yang ditemukan+diperbaiki saat render, item yang ditandai `[PERLU KONFIRMASI]` (kalau ada), dan instruksi Ctrl+A → F9 bila field Word perlu diperbarui manual saat pertama dibuka.

Jangan berhenti di analisis/saran saja — hasilkan file DOCX final di `docs/mini-ta/04-output/`.
