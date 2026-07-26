# Tabel 9 — Threat Model

Reproduksi model musuh (§3) dan risk register deskriptif T1-T7 (§6) dari `08_THREAT_MODEL.md` sebagai artefak tabel siap-pakai BAB IV/V. Kemungkinan/Dampak dinilai kualitatif, bukan skor kuantitatif (mis. CVSS) — proporsional untuk tugas mata kuliah.

## 9.1 Model Musuh (Adversary Models)

| ID | Kemampuan | Batasan |
|---|---|---|
| A1 | Penyadap pasif di LAN/sirkuit Tor | Tidak dapat mendekripsi lalu lintas terproteksi Noise |
| A2 | Penyerang aktif di LAN (spoofing/injeksi mDNS) | Dapat MITM kontak baru belum diverifikasi; tidak dapat menembus sesi Noise_IK terverifikasi |
| A3 | Penyerang lokal dengan akses baca filesystem | Berhadapan dengan Argon2id + ChaCha20-Poly1305 pada vault |
| A4 | Kontak berbahaya/kompromi dengan fingerprint valid | Berpartisipasi penuh sebagai pihak sah — perilaku desain yang diharapkan |
| A5 | Partisipan mDNS berbahaya di segmen LAN sama | Dapat mengamati broadcast presence/fingerprint plaintext |

## 9.2 Risk Register Deskriptif (T1-T7)

| # | Temuan | Komponen | Kemungkinan | Dampak | Mitigasi yang Sudah Ada |
|---|---|---|---|---|---|
| T1 | Tidak ada pengecekan identitas pada koneksi pertama ke kontak belum dikenal | Handshake | Sedang | Tinggi | Verifikasi fingerprint manual out-of-band |
| T2 | Kebocoran metadata presence/fingerprint di LAN | Discovery mDNS | Tinggi | Rendah-Sedang | X25519 key tidak diiklankan; diakui eksplisit trade-off M1 |
| T3 | Invite code tidak diautentikasi kriptografis | Pertukaran kontak | Sedang | Tinggi | Fingerprint mengikat kedua key; verifikasi manual out-of-band |
| T4 | Tidak ada file-permission hardening pada vault/state Tor | Filesystem lokal | Rendah-Sedang | Sedang-Tinggi | Enkripsi vault (Argon2id+ChaCha20Poly1305) tetap lapisan proteksi utama |
| T5 | UI tidak membedakan penutupan sesi akibat tampering vs. normal | Transport | Rendah | Rendah | Fail-closed tetap terjadi |
| T6 | `FS_MISTRUST_DISABLE_PERMISSIONS_CHECKS` aktif tanpa syarat platform | Tor | Rendah-Sedang | Sedang | Tidak ada |
| T7 | Tidak ada mekanisme rotasi/revokasi kunci apa pun | Key lifecycle | N/A (struktural) | Tinggi jangka panjang | Tidak ada |

## Catatan Anti-Overclaim

Ed25519 tidak dipakai untuk tanda tangan aktif — kategori ancaman "pemalsuan tanda tangan digital" tidak relevan untuk AKSARA saat ini. Ancaman nonce-reuse ChaCha20-Poly1305 dibingkai sebagai batasan desain yang sudah dipertimbangkan, bukan kerentanan yang ditemukan terjadi.

## Referensi

`08_THREAT_MODEL.md` §3, §6, §7 (TAHAP 7).
