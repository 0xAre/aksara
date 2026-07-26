# 07 — Key Lifecycle AKSARA

Dokumen ini mendeskripsikan siklus hidup seluruh material kunci di AKSARA: pembangkitan, penyimpanan, pemakaian, rotasi, dan zeroization. Basis evidence: `02_CRYPTO_IMPLEMENTATION_AUDIT.md` (CR-xxx), `evidence/_raw-audit-json/{identity,contacts,main_and_error,session,crypto_handshake}.json` (TAHAP 2/3), dan `04_CRYPTOGRAPHIC_JUSTIFICATION.md` (justifikasi algoritma, tidak diulang di sini).

**Batasan wajib dibawa dari `SESSION_2_HANDOFF.md`**: Ed25519 di AKSARA murni fingerprint (TIDAK ada sign()/verify() aktif — lihat §5.1); klaim timing Argon2id "~100ms" TIDAK diverifikasi benchmark (lihat §3.3); ChaCha20-Poly1305 TIDAK misuse-resistant (relevan pada §3 dan §4).

---

## 1. Ringkasan Material Kunci

| Kunci/Material | Algoritma | Ukuran | Umur | Dipersist? |
|---|---|---|---|---|
| Identity secret key (`IdentityKey`) | Ed25519 | 256 bit / 32 byte | Jangka panjang (per identitas) | Ya — di dalam vault, terenkripsi |
| Identity public key | Ed25519 | 256 bit / 32 byte | Jangka panjang | Ya — plaintext (dalam invite/fingerprint), bukan rahasia |
| Noise secret key (`NoiseKey`) | X25519 | 256 bit / 32 byte | Jangka panjang (statis, per identitas) | Ya — di dalam vault, terenkripsi |
| Noise public key | X25519 | 256 bit / 32 byte | Jangka panjang | Ya — plaintext (dalam invite/fingerprint), bukan rahasia |
| Vault encryption key | Argon2id output | 256 bit / 32 byte | Sekali per operasi `seal()`/`unseal()` | **Tidak** — hanya salt yang dipersist |
| Vault salt | acak (`OsRng`) | 128 bit / 16 byte | Sekali per `seal()` (baru tiap re-seal) | Ya — 16 byte pertama file vault |
| Vault nonce | acak (`OsRng`) | 96 bit / 12 byte | Sekali per `seal()` | Ya — byte ke-17..28 file vault |
| Contacts-store key | BLAKE2s (derivasi dari identity secret) | 256 bit / 32 byte | Dihitung ulang tiap panggilan, deterministik selama identity tidak berubah | **Tidak** — dihitung ulang dari identity secret yang sudah ter-unlock |
| Contacts-store nonce | acak (`OsRng`) | 96 bit / 12 byte | Sekali per `save_contacts()` | Ya — 12 byte pertama file kontak |
| Noise ephemeral key (`e`) | X25519 | 256 bit / 32 byte | Sekali per handshake | Tidak — internal `snow`, tidak diobservasi dari source aplikasi |
| Noise transport session key | (diasumsikan ChaCha20-Poly1305, lihat `06_PROTOCOL_SPECIFICATION.md` §6.4) | — | Sekali per sesi (dari handshake selesai s.d. sesi drop) | Tidak — opak di dalam `EncryptedSession`/`TransportState` |

---

## 2. Pembangkitan (Generation)

Seluruh pembangkitan kunci di AKSARA memakai **satu** sumber entropi seragam: `rand::rngs::OsRng` (CSPRNG OS) — CORE-7 di `04_CRYPTOGRAPHIC_JUSTIFICATION.md`, tidak diulang justifikasinya di sini.

| Fungsi | Mekanisme | Evidence |
|---|---|---|
| `IdentityKey::generate()` | `SigningKey::generate(&mut OsRng)` | `src/identity/keypair.rs:18-22` |
| `NoiseKey::generate()` | `X25519Secret::random_from_rng(OsRng)` | `src/identity/keypair.rs:51-56` |
| `KeyBundle::generate()` | Memanggil `IdentityKey::generate()` + `NoiseKey::generate()` | `src/identity/keypair.rs:74-89` |
| Salt Argon2id (vault) | `OsRng.fill_bytes()` | `src/identity/vault.rs:68-69` |
| Nonce ChaCha20Poly1305 (vault) | `ChaCha20Poly1305::generate_nonce(&mut OsRng)` | `src/identity/vault.rs:75` |
| Nonce ChaCha20Poly1305 (contacts) | `ChaCha20Poly1305::generate_nonce(&mut OsRng)` | `src/contacts/mod.rs:173-176` |

`KeyBundle::generate()` dipanggil **hanya** saat file vault belum ada di disk, di dalam `load_or_create_vault()` (`src/main.rs:167-185`), **setelah** passphrase non-kosong divalidasi (passphrase kosong → `Error::KeyDerivation` sebelum `generate()` dipanggil, `main.rs:175-178`).

Verifikasi round-trip: test `identity_key_roundtrip` dan `noise_key_roundtrip` (`keypair.rs:95-109`) memastikan `secret_bytes() -> from_secret_bytes()` menghasilkan public key yang identik; test `keybundle_keys_are_independent` (`keypair.rs:111-118`) memastikan public key Ed25519 dan X25519 dalam satu `KeyBundle` berbeda satu sama lain.

---

## 3. Penyimpanan At-Rest (Vault Identitas)

### 3.1 Layout Biner

Format fixed-offset **108 byte** (`VAULT_SIZE`), **tanpa header, magic bytes, versi, atau string identifikasi aplikasi**, by design (`src/identity/vault.rs:1-31`, CR-019):

```
[ 16 byte salt Argon2id ][ 12 byte nonce ChaCha20 ][ 64 byte ciphertext ][ 16 byte tag Poly1305 ]
                                                     (32B Ed25519 sk || 32B X25519 sk)
```

Ketiadaan header/magic/versi dijustifikasi komentar kode sebagai kepatuhan terhadap requirement internal berlabel **"SEC-05"** (definisi lengkapnya tidak ada di ketiga file yang diaudit) — kemungkinan besar terkait *plausible deniability* (`vault.rs:1-14`). Konsekuensi: **tidak ada jalur migrasi** bila `PLAINTEXT_LEN` atau urutan field berubah di masa depan — perubahan semacam itu akan menjadi breaking change senyap yang tidak terdeteksi kode.

### 3.2 Alur `seal()` / `unseal()`

**`seal(bundle, passphrase)`** (`vault.rs:58-93`):
1. Susun plaintext 64 byte: `Ed25519 sk (32B) || X25519 sk (32B)`.
2. Bangkitkan salt 16-byte acak baru.
3. Turunkan kunci 256-bit via Argon2id (§3.3).
4. Bangkitkan nonce 96-bit acak baru.
5. Enkripsi via ChaCha20-Poly1305 → `Error::Encryption` bila gagal (`vault.rs:78-81`).
6. Gabungkan `salt || nonce || ciphertext+tag` menjadi array `VAULT_SIZE`.

**`unseal(vault, passphrase)`** (`vault.rs:95-128`):
1. Pisahkan salt/nonce/ciphertext dari offset tetap.
2. Turunkan ulang kunci via Argon2id memakai salt yang tersimpan.
3. Dekripsi + verifikasi tag ChaCha20-Poly1305.
4. Validasi panjang plaintext hasil dekripsi persis 64 byte.
5. Pisah kembali menjadi 32-byte Ed25519 secret dan 32-byte X25519 secret, rekonstruksi `KeyBundle`.

**Setiap panggilan `seal()` menurunkan kunci baru dari salt acak baru** — sehingga kunci AEAD vault **berbeda pada setiap re-seal**, bahkan dengan passphrase yang sama (dikonfirmasi test `vault_looks_random`, `vault.rs:169-177`: dua `seal()` dengan bundle+passphrase sama menghasilkan byte vault yang berbeda).

### 3.3 Argon2id (Key Derivation)

Parameter: `m = 19*1024 KiB (19 MiB)`, `t = 2`, `p = 1`, output 32 byte (`Params::new(19*1024, 2, 1, Some(32))`, `vault.rs:40-45`) — nilai **tetap** (constant), tidak ada mekanisme versioning parameter.

> **Klaim yang harus dihindari**: komentar kode menyatakan parameter ini menghasilkan waktu unlock **"~100 ms"** pada "hardware modern" (`vault.rs:33-38`). **Tidak ada benchmark, timing test, atau pengukuran apa pun** dalam source yang diaudit untuk membuktikan angka ini. Jangan mengutip angka ini sebagai fakta terukur di BAB manapun (termasuk BAB Hasil/Pengujian, TAHAP 13) tanpa benchmark aktual — status `DOCUMENTED_ONLY`, confidence LOW.

Output Argon2id dipakai **langsung** sebagai kunci AEAD tanpa HKDF perantara — dapat diterima untuk kasus tunggal saat ini (dibahas di `04_CRYPTOGRAPHIC_JUSTIFICATION.md` CORE-5 poin 13), tidak diulang di sini.

### 3.4 Error Handling (Vault)

| Kegagalan | Penanganan | Evidence |
|---|---|---|
| Argon2 `hash_password_into` gagal | `Error::KeyDerivation` | `vault.rs:49-56` |
| Enkripsi ChaCha20Poly1305 gagal | `Error::Encryption` | `vault.rs:78-81` |
| Dekripsi/verifikasi tag gagal (passphrase salah **atau** vault corrupt) | `Error::Decryption` — **sengaja ambigu** | `vault.rs:95-112` |
| Panjang plaintext hasil dekripsi ≠ 64 byte | `Error::Decryption` (sama seperti di atas) | `vault.rs:114-116` |
| File vault salah ukuran (`try_into::<[u8;VAULT_SIZE]>()` gagal) | `Error::Decryption` (bukan error format terpisah) | `vault.rs:137-142` |
| Kegagalan I/O filesystem | `Error::Io` | `vault.rs:132-139` |

Ambiguitas `Error::Decryption` (passphrase salah vs. vault korup vs. file salah ukuran, ketiganya dipetakan ke pesan yang sama, "vault could not be opened") **disengaja** — komentar kode eksplisit menyatakan ini mitigasi terhadap *oracle attack* melalui isi pesan error (`vault.rs:96-97`, dikonfirmasi `src/error.rs:1-14`). Ini mitigasi yang tepat untuk kerahasiaan pesan error, namun **tidak mencakup potensi side-channel lain** (mis. perbedaan waktu proses Argon2id vs. pembacaan file) — tidak dinilai dari file yang diaudit.

`write_vault()`/`read_vault()` memakai `std::fs::write`/`std::fs::read` polos — **tidak ada file-permission hardening eksplisit** (mis. pembatasan mode akses) yang ditemukan di file ini (`vault.rs:132-142`).

Sanity-check panjang ciphertext pasca-enkripsi memakai `debug_assert_eq!` — **dikompilasi hilang pada release build**, sehingga tidak memberi proteksi runtime apa pun di produksi (`vault.rs:83-84`).

---

## 4. Contacts-Store Key (Bukan Passphrase-Derived)

`derive_contacts_key(bundle)` menurunkan kunci ChaCha20Poly1305 32-byte untuk enkripsi contact store dari `bundle.identity.secret_bytes()` (secret identitas yang **sudah ter-unlock**), via BLAKE2s256 dengan domain string `"aksara-contacts-key-v1"` (`src/contacts/mod.rs:104-112`, CR-003).

- **Sengaja bukan Argon2id** — komentar kode eksplisit menyatakan ini karena input sudah berupa secret berentropi tinggi (bukan passphrase berentropi rendah manusia), sehingga tidak perlu memory-hardening tambahan (`contacts/mod.rs:102-103`).
- Kunci ini **tidak dipersist** — dihitung ulang tiap kali `derive_contacts_key` dipanggil, selama identity tidak berubah hasilnya deterministik.
- **Konsekuensi keamanan**: karena kunci diturunkan langsung dari identity secret (bukan passphrase terpisah), **kompromi identity secret otomatis membuka seluruh contact store** — tidak ada kompartementalisasi terpisah antara keduanya.
- Format file kontak di disk: `[12 byte nonce][ciphertext+tag]`, tanpa magic bytes header (`contacts/mod.rs:94-100`), memakai nonce acak baru per `save_contacts()` (`contacts/mod.rs:173-176`).
- Error handling: `load_contacts` memperlakukan **setiap** error dari `std::fs::read` (termasuk kemungkinan *permission denied*, bukan hanya "file belum ada") sebagai kondisi "belum ada kontak" → `Ok(Vec::new())` (`contacts/mod.rs:185-188`); file yang lebih pendek dari nonce+tag minimum juga diperlakukan sebagai daftar kosong, bukan error korupsi (`contacts/mod.rs:189-191`); `deserialize_contacts` diam-diam melewati baris yang tidak lengkap/invalid tanpa melaporkan korupsi ke caller (`contacts/mod.rs:140-167`) — berpotensi kehilangan data kontak secara senyap.

---

## 5. Pemakaian Kunci per Konteks

### 5.1 Identity Key (Ed25519) — HANYA Fingerprint, BUKAN Signing Aktif

**Temuan yang wajib ditegaskan ulang di setiap BAB yang membahas Ed25519** (mandat `SESSION_2_HANDOFF.md`): grep menyeluruh terhadap `sign(`/`verify(`/`Signature` di `src/identity/keypair.rs`, `src/identity/vault.rs`, dan `src/identity/mod.rs` menghasilkan **nihil** (CB-084, dikonfirmasi silang di `identity.json`: "Grep for sign(/verify(/Signature across all three files returned no matches"). Fungsi Ed25519 di AKSARA **saat ini**:

- Generate keypair (`IdentityKey::generate()`).
- Simpan/ekspor secret bytes (`pub(crate) secret_bytes()`, dipakai vault.rs untuk serialisasi).
- Menyediakan public key sebagai bahan `fingerprint()` (bersama X25519 public key, via BLAKE2s — CORE-4) dan invite code.

**Tidak ada** operasi `sign()`/`verify()` di manapun dalam source yang diaudit. Properti keamanan EdDSA umum (signature deterministic, resisten kegagalan RNG saat signing, verifikasi cepat — dibahas di `04_CRYPTOGRAPHIC_JUSTIFICATION.md` CORE-6 poin 2) adalah properti **algoritma Ed25519 secara umum**, bukan kapabilitas yang **dimanfaatkan** AKSARA hari ini. Autentikasi identitas peer yang benar-benar berjalan di AKSARA adalah verifikasi static-key X25519 di dalam handshake Noise_IK (`06_PROTOCOL_SPECIFICATION.md` §5.2), **bukan** tanda tangan digital Ed25519.

### 5.2 Noise Key (X25519) — Static DH Key

Dipakai sebagai static key dalam handshake Noise_IK, dikonsumsi `crypto::handshake.rs` via `session::run_session` (`06_PROTOCOL_SPECIFICATION.md` §5). Secret disimpan di vault bersama secret Ed25519; tidak ada pemakaian lain di luar handshake yang ditemukan dalam audit.

### 5.3 Noise Ephemeral Key dan Transport Session Key

Keduanya dibangkitkan/dikelola **sepenuhnya internal** oleh crate `snow` — tidak ada kode aplikasi yang membangkitkan atau menyimpannya secara eksplisit (`crypto/handshake.rs`, key_storage: opak di dalam `HandshakeState`/`TransportState`, `handshake.rs:25,85`). Confidence LOW-MEDIUM untuk detail internal ini, konsisten dengan catatan §5.4 di `06_PROTOCOL_SPECIFICATION.md`.

---

## 6. Rotasi dan Revokasi

**Tidak ditemukan mekanisme rotasi** untuk kunci/material manapun di AKSARA:

| Material | Status rotasi |
|---|---|
| Kunci enkripsi vault (passphrase-derived) | Tidak ada — kunci baru **hanya** karena salt baru dibangkitkan tiap `seal()`, bukan kebijakan rotasi terjadwal/dipicu |
| Identity key (Ed25519) jangka panjang | Tidak ada |
| Noise key (X25519) jangka panjang | Tidak ada |
| Parameter Argon2id (`m`,`t`,`p`) | Tidak ada — nilai konstan tetap, tidak ada versioning bila rekomendasi standar berubah |
| Noise session transport key | Tidak ada — satu kunci per sesi, berakhir saat sesi drop |
| Contacts-store key | N/A (deterministik dari identity secret, bukan target rotasi) |

**Tidak ditemukan mekanisme revokasi**: setelah fingerprint/public key kontak dipertukarkan via invite code, tidak ada alur *revoke*/ganti-kunci-kontak di `contacts/mod.rs`. **Implikasi untuk `08_THREAT_MODEL.md`**: bila identity key jangka panjang seorang pengguna kompromi, tidak ada mekanisme in-band untuk membatalkannya — pemulihan memerlukan pembuatan identitas baru dan pertukaran ulang invite sepenuhnya di luar cakupan protokol yang ada.

---

## 7. Zeroization (Penghapusan Kunci dari Memori)

### 7.1 Yang Sudah Diterapkan

- `IdentityKey`, `NoiseKey`, `KeyBundle` seluruhnya derive `#[derive(ZeroizeOnDrop)]`; field public/verifying secara eksplisit dikecualikan via `#[zeroize(skip)]` karena bukan rahasia (`keypair.rs:10,44,74-89`).
- Vault: buffer plaintext `Zeroizing<[u8;64]>` (`vault.rs:62`), kunci turunan `Zeroizing<[u8;32]>` (`vault.rs:49-56`), plaintext hasil dekripsi `Zeroizing<Vec<u8>>` (`vault.rs:108`) — seluruhnya via crate `zeroize` 1.9.0.

### 7.2 Kesenjangan yang Ditemukan (dilaporkan, bukan disembunyikan)

| Lokasi | Kesenjangan | Evidence |
|---|---|---|
| `session::run_session` | Parameter `local_noise_sk`/`peer_noise_pk` diterima sebagai `[u8;32]` polos tanpa wrapper zeroizing di boundary fungsi ini | `session/mod.rs:96-97` |
| `session::run_session` | Buffer plaintext pesan (`payload` keluar, `pt` masuk) adalah `Vec<u8>` biasa tanpa zeroize — sisa plaintext berpotensi tertinggal di heap setelah scope berakhir | `session/mod.rs:205-211,253-266` |
| `crypto::handshake` | Tidak ada `Zeroize`/`ZeroizeOnDrop` pada `HandshakeSession`/`EncryptedSession` atau field state-nya; perilaku zeroization internal `snow` tidak diverifikasi dari file ini | `crypto/handshake.rs:24-86` |
| `contacts::mod` | `derive_contacts_key()` mengembalikan `[u8;32]` polos tanpa zeroizing wrapper; plaintext `String` hasil dekripsi tidak dibersihkan setelah dipakai | `contacts/mod.rs:104-112,197` |
| `main.rs` | `secret_bytes()` mengekstrak private key X25519 mentah ke variabel lokal `noise_sk`, disalin ke struct `SelfKeys` yang diteruskan ke `tui::run()` — apakah `SelfKeys` sendiri menerapkan `ZeroizeOnDrop` **tidak terlihat** dari `main.rs` | `main.rs:189-199` (`NEEDS_CONFIRMATION`) |
| `main.rs` | Passphrase via env var `AKSARA_PASSPHRASE` hidup di environment proses tanpa mekanisme pembersihan setelah dibaca | `main.rs:156-158` |
| `main.rs` | Input passphrase dari stdin **masih ter-echo ke layar** pada versi ini (komentar "Catatan M1"); input tersembunyi via crossterm direncanakan M4, **belum diimplementasikan** | `main.rs:153-154` (status `PLANNED`) |

Ini bukan klaim bahwa kesenjangan tersebut adalah eksploitasi aktif yang ditemukan — melainkan area di mana jaminan zeroization/hardening yang berlaku pada tipe kunci inti (`IdentityKey`/`NoiseKey`/`KeyBundle`, vault) **tidak** diperpanjang secara konsisten ke seluruh boundary fungsi dan buffer sementara di sekitarnya.

---

## 8. Diagram Siklus Hidup (Tekstual)

Diagram Mermaid resmi adalah cakupan TAHAP 11 (`11_FIGURE_MANIFEST.md`, SESSION 4) — bagian ini hanya ringkasan tekstual urutan status, bukan figur yang dirender.

```
[Belum ada vault]
      |  KeyBundle::generate() (main.rs:179, setelah passphrase non-kosong tervalidasi)
      v
[KeyBundle di memori: IdentityKey(Ed25519) + NoiseKey(X25519), keduanya ZeroizeOnDrop]
      |  vault::seal(bundle, passphrase) -> Argon2id(passphrase, salt acak) -> ChaCha20Poly1305 encrypt
      v
[Vault 108-byte tersimpan di disk: salt || nonce || ciphertext+tag]
      |  (restart aplikasi / kunci ulang)
      |  vault::unseal(vault_bytes, passphrase) -> Argon2id(passphrase, salt tersimpan) -> ChaCha20Poly1305 decrypt
      v
[KeyBundle di memori kembali]
      |  X25519 static key -> dipakai handshake Noise_IK (per sesi, tanpa rotasi)
      |  Ed25519 public key -> dipakai fingerprint/invite (TIDAK pernah untuk sign/verify)
      v
[Sesi berakhir -> EncryptedSession di-drop -> transport key hilang mengikuti drop Rust biasa,
 TIDAK diverifikasi ada zeroize eksplisit di titik ini]
```

---

## 9. Ringkasan Confidence

| Klaim | Confidence | Catatan |
|---|---|---|
| Pembangkitan kunci seragam via `OsRng` | HIGH | Diverifikasi langsung di semua titik generate |
| Layout vault 108-byte, tanpa header/versi | HIGH | Diverifikasi langsung + test `seal_unseal_roundtrip` |
| Ambiguitas error `Decryption` disengaja (anti-oracle) | HIGH | Komentar kode eksplisit + `error.rs` |
| Timing Argon2id "~100ms" | **LOW / DOCUMENTED_ONLY** | Tidak ada benchmark — jangan kutip sebagai fakta terukur |
| Ed25519 hanya fingerprint, tanpa sign/verify aktif | HIGH | Grep menyeluruh nihil hasil (CB-084) |
| Zeroization konsisten di seluruh boundary fungsi | **PARTIAL** | Kuat pada tipe kunci inti (`KeyBundle`/vault), lemah pada boundary `session`/`handshake`/`contacts`/`main` |
| Ketiadaan rotasi/revokasi kunci | HIGH (untuk fakta ketiadaannya) | Tidak ditemukan mekanisme apa pun di seluruh file yang diaudit |

---

## Referensi

Seluruh referensi teori pada dokumen ini menggunakan citekey yang **sudah ada** di `references/REFERENCES.bib` (TAHAP 4/9), tidak ada entry baru yang dibutuhkan untuk TAHAP 6: `rfc9106`/`biryukov2016argon2` (Argon2id), `rfc8439` (ChaCha20-Poly1305 vault/contacts), `rfc7693`/`aumasson2013blake2` (BLAKE2s contacts-key), `rfc8032`/`bernstein2012ed25519`/`fips186-5` (Ed25519 — dikutip sebagai konteks properti algoritma umum, bukan bukti pemakaian sign/verify aktif AKSARA), `sp800-90a` (konteks kriteria CSPRNG untuk `OsRng`).
