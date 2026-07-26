# Tabel 10 — Penelitian Terkait

Reproduksi tabel `10_RELATED_WORK_AND_GAP.md` §2 (7 entry) sebagai artefak tabel siap-pakai BAB II. Gap G1-G5 dibingkai "belum ditemukan pada sumber yang ditinjau", bukan "belum pernah diteliti".

| No | Penelitian | Primitif | Sistem | Perbedaan dengan AKSARA |
|---|---|---|---|---|
| 1 | `kobeissi2019noiseexplorer` — Noise Explorer (IEEE EuroS&P 2019) | Noise Protocol Framework (semua pola termasuk `IK`) | Tool verifikasi formal | AKSARA memakai pola `IK` tanpa verifikasi formal terhadap instansiasi spesifiknya (G1) |
| 2 | `cohngordon2020signal` — Formal Security Analysis of Signal (J. Cryptology 2020) | X3DH + Double Ratchet | Signal Protocol | AKSARA memakai satu kunci transport statis tanpa ratchet — tidak ada post-compromise security (G2) |
| 3 | `donenfeld2017wireguard` — WireGuard (NDSS 2017) | Noise `IK` + cookie anti-DoS, ChaCha20-Poly1305, BLAKE2s, X25519 | WireGuard VPN kernel-level | Stack primitif nyaris identik, tapi AKSARA tidak punya cookie anti-DoS maupun rekey berkala (G3 evaluasi overhead belum dijalankan) |
| 4 | `borisov2004otr` — Off-the-Record Communication (WPES 2004) | DH + AES + SHA-1 HMAC | OTR Messaging | AKSARA tidak dirancang untuk deniability; forward secrecy AKSARA `DOCUMENTED_ONLY`, bukan diverifikasi eksplisit seperti OTR |
| 5 | `albrecht2024matrix` — Formal Cryptographic Analysis of Matrix (IEEE S&P 2024) | Olm/Megolm (Double Ratchet + rotasi sesi grup) | Matrix (federated multi-device) | AKSARA tidak punya mekanisme rotasi/revokasi apa pun (G2); P2P murni satu-identitas-satu-perangkat, bukan federated |
| 6 | `briarspec` — Bramble Protocol Suite | Curve25519 + AEAD (BTP), transport ganda Tor/Bluetooth/Wi-Fi | Briar (P2P serverless, target aktivis) | Arsitektur paling dekat dengan AKSARA; beda utama: Briar punya jalur offline (G5) dan handshake kontak terstruktur (G4) yang tidak dimiliki AKSARA |
| 7 | `toxspec` — Spesifikasi protokol Tox | NaCl (`crypto_box`, Curve25519 + XSalsa20-Poly1305) | Tox (P2P murni via DHT) | Memakai NaCl (bukan Noise) dan DHT (bukan mDNS); status "belum diaudit formal" paralel dengan `snow` AKSARA |

## Ringkasan Gap

| Gap | Deskripsi Singkat |
|---|---|
| G1 | Ketiadaan verifikasi formal terhadap instansiasi Noise_IK spesifik AKSARA |
| G2 | Ketiadaan mekanisme rotasi/ratcheting kunci sesi |
| G3 | Belum ada evaluasi overhead protokol pada konteks jaringan lokal/Tor AKSARA (`NEEDS_EXPERIMENT` — lihat `12_TEST_PLAN.md`) |
| G4 | Invite code AKSARA tidak memiliki proses handshake kontak terstruktur seperti Briar |
| G5 | Ketiadaan mekanisme fallback offline (bukan gap keamanan, perbedaan cakupan fitur) |

## Referensi

`10_RELATED_WORK_AND_GAP.md` (TAHAP 10), `references/REFERENCES.bib` (7 entry terkait).
