# 06 — Spesifikasi Protokol AKSARA

Dokumen ini mendeskripsikan protokol **sebagaimana sudah diimplementasikan** (as-built specification), bukan proposal desain baru. Basis evidence: `02_CRYPTO_IMPLEMENTATION_AUDIT.md` (CR-xxx), `evidence/_raw-audit-json/{session,crypto_handshake,transport_lan,transport_tor}.json` (TAHAP 2/3), dan justifikasi kripto di `04_CRYPTOGRAPHIC_JUSTIFICATION.md`/`05_CRYPTO_ALTERNATIVE_COMPARISON.md` (TAHAP 4) yang tidak diulang di sini — hanya dirujuk. Setiap klaim implementasi menyertakan path+baris+ID evidence; klaim teori merujuk citekey di `references/REFERENCES.bib`.

**Batasan wajib dibawa dari `SESSION_2_HANDOFF.md`**: (1) Ed25519 di AKSARA murni fingerprint — TIDAK ada sign()/verify() aktif, jangan dicampur dengan properti EdDSA umum; (2) sub-mekanisme internal Noise_IK (hash/HKDF) confidence LOW, murni inferensi nama pattern; (3) ChaCha20-Poly1305 TIDAK misuse-resistant; (4) klaim timing Argon2id "~100ms" tidak diverifikasi benchmark. Detail lengkap justifikasi kriptografi tidak diulang di sini — lihat `04_CRYPTOGRAPHIC_JUSTIFICATION.md`.

---

## 1. Ruang Lingkup dan Model Komunikasi

AKSARA adalah protokol P2P dua pihak, tanpa server relay atau broker pusat. Satu peer menjalankan satu proses; setiap proses dapat berperan sebagai **Initiator** atau **Responder** dalam satu sesi koneksi. Peran ditentukan **deterministik** dari perbandingan fingerprint, bukan konfigurasi statis client/server:

- `fn role_from_fp(my_fp, target_fp)`: `Role::Initiator` jika `my_fp < target_fp` (operator `<` bawaan `&str`, byte-wise), selain itu `Role::Responder` (`src/transport/mod.rs:101-107`). Tujuannya agar kedua sisi tidak sama-sama mendial (`src/transport/mod.rs:27-33`).
- Perbandingan ini **non-constant-time**, tetapi kedua fingerprint yang dibandingkan adalah data publik yang sudah saling diketahui via pertukaran kontak — risiko timing side-channel dinilai rendah, meski kode tidak mendokumentasikan pertimbangan ini secara eksplisit (evidence: `transport_lan.json`, claim `session_mgmt` baris `mod.rs:101-107`).

Dua jalur transport tersedia, dengan strategi fallback **LAN-first → Tor** (doc-comment `src/transport/mod.rs:1-4`, `DOCUMENTED_ONLY`/HIGH):

| Jalur | Mekanisme | Modul |
|---|---|---|
| LAN | Discovery mDNS + TCP langsung | `src/transport/lan.rs`, orkestrasi di `src/transport/mod.rs` |
| Tor | Onion service v3 via `arti-client`/`tor-hsservice` 0.43.0 | `src/transport/tor.rs` |

Di atas kedua jalur transport, seluruh sesi dibungkus **Noise_IK** (§5) — Tor berperan sebagai lapisan defense-in-depth yang menyembunyikan lokasi jaringan, sementara Noise mengamankan konten dan autentikasi identitas (doc-comment `src/transport/tor.rs:4-7`, dikonfirmasi `transport_tor.json`).

---

## 2. Tahapan Protokol End-to-End

1. **Pembangkitan/unlock identitas** — ringkas di sini, detail penuh di `07_KEY_LIFECYCLE.md`.
2. **Pertukaran kontak (invite code)** out-of-band — §3.
3. **Peer discovery / pembentukan koneksi transport** (LAN mDNS atau Tor connect/accept) — §4.
4. **Handshake Noise_IK** (2 pesan) — §5.
5. **Fase transport terenkripsi** (pesan chat, blur signal, keepalive) — §6.
6. **Penutupan sesi** — §6.5.

---

## 3. Pertukaran Kontak (Invite Code)

Invite code adalah mekanisme *out-of-band* untuk saling mengenal fingerprint sebelum koneksi pertama — bukan bagian dari handshake Noise itu sendiri.

- Format: `base64url_no_pad(ed25519_pub[32] || noise_pub[32])`, opsional suffix `@<onion-address>` (`src/contacts/mod.rs:56-68`, CR-005). Tidak ada magic prefix yang disengaja — dikonfirmasi test `invite_has_no_obvious_prefix` (`contacts/mod.rs:316-323`).
- `decode_invite`: split di karakter `@` pertama, decode base64, wajib hasil persis 64 byte — gagal salah satu menghasilkan `Error::InvalidInvite` (`contacts/mod.rs:74-92`).
- **Invite code TIDAK ditandatangani/diautentikasi secara kriptografis** — dinyatakan eksplisit di komentar kode (`contacts/mod.rs:42-47`, CR-005). Keaslian invite bergantung sepenuhnya pada verifikasi fingerprint out-of-band oleh pengguna (mis. dibacakan lewat kanal komunikasi lain), bukan pada mekanisme dalam kode.
- Fingerprint pengikat: `fingerprint() = hex(BLAKE2s256(ed25519_pub || noise_pub || "aksara-fingerprint-v1"))`, 64 karakter hex (`contacts/mod.rs:39-54`, CR-002). Kedua public key **wajib** diserap bersama untuk mencegah serangan *invite susun-ulang* (attacker mengambil `ed25519_pub` korban dan menggabungkannya dengan `noise_pub` miliknya sendiri) — dikonfirmasi test `fingerprint_binds_both_keys` (`contacts/mod.rs:303-314`).
- Alamat onion diperlakukan sebagai string opaque tanpa validasi format (tidak ada pengecekan suffix `.onion`/panjang/karakter) baik di invite maupun contacts store (`contacts/mod.rs:59-163`, MEDIUM confidence).

---

## 4. Pembentukan Koneksi Transport

### 4.1 Orkestrasi (`fn establish`, `src/transport/mod.rs:118-172`)

1. Peran (`Role`) ditentukan dari `LanMode` eksplisit atau perbandingan fingerprint (§1).
2. `tor_available = tor.is_some() && onion.is_some()`.
3. LAN dicoba lebih dulu (kecuali `LanMode::Off`): timeout `LAN_AUTO_TIMEOUT = 3 detik` **hanya** diterapkan jika `LanMode::Auto` **dan** Tor tersedia (`mod.rs:118-155`); pada mode LAN-only (Tor tidak tersedia), koneksi menunggu **tanpa batas waktu** sampai pengguna membatalkan (Esc, menurut komentar kode).
4. Jika LAN gagal dan Tor tidak tersedia → error LAN asli dikembalikan langsung (bukan fallback dipaksakan). Jika Tor tersedia → lanjut ke jalur Tor dengan peran yang sama: `Initiator` memanggil `tor_dial_with_retry`, `Responder` memanggil `tor.accept_timeout(TOR_ACCEPT_TIMEOUT)` (mengembalikan `Error::ConnectionClosed` bila tidak ada koneksi masuk) (`mod.rs:148-171`).

`enum LanMode { Auto, Listen(u16), Dial(SocketAddr), Off }` — `Auto` memakai discovery mDNS + perbandingan fingerprint; `Listen`/`Dial` memaksa peran untuk pengujian; `Off` melewati LAN sepenuhnya (untuk kontak onion-only), ditandai `#[allow(dead_code)]` dengan catatan "belum di-wire ke UI" — aplikasi default memakai `Auto` (`mod.rs:35-48`).

`enum Conn { Tcp(TcpStream), Tor(DataStream) }` membungkus kedua jenis koneksi dan mendelegasikan `AsyncRead`/`AsyncWrite` ke varian aktif (`mod.rs:50-99`) — sehingga `session::run_session` (§6) generik terhadap jalur transport yang dipakai.

### 4.2 Jalur LAN (`src/transport/lan.rs`)

- Discovery via mDNS: Responder mengiklankan service `_aksara._tcp.local.` (`SERVICE_TYPE`) dengan TXT record `fp=<hex fingerprint 64 karakter>`; Initiator browse service yang sama dan mencocokkan fingerprint dengan kontak dikenal sebelum dial (`lan.rs:1-21`, CR-029).
- **Hanya fingerprint Ed25519 yang diiklankan** — X25519 Noise key **tidak** diiklankan via mDNS, sehingga discovery tidak membocorkan material handshake (`lan.rs:9-11`). Lihat `08_THREAT_MODEL.md` §4.2 untuk analisis kebocoran metadata yang **diakui secara eksplisit oleh komentar kode sendiri** sebagai trade-off yang diterima untuk M1 (`lan.rs:9-12`).
- `MAX_LABEL_LEN = 32` byte (margin aman terhadap batas 63 byte label DNS); `fn safe_label` memendekkan string per-karakter agar tidak memotong UTF-8 multi-byte di tengah (`lan.rs:23-42`).
- `fn is_lan_dialable` menolak alamat loopback, unspecified (`0.0.0.0`), dan link-local (`169.254.x`/APIPA) IPv4; seluruh IPv6 di-skip karena discovery difokuskan IPv4 (`lan.rs:50-55`). Filter yang sama diterapkan ulang (*defense-in-depth*) terhadap alamat yang diiklankan peer sebelum dial, untuk mengantisipasi peer versi lama yang mungkin masih menyiarkan alamat non-dialable (`lan.rs:133-149`).
- `advertise()` memilih IP LAN nyata hasil `local_lan_ips()` daripada `enable_addr_auto()` (yang menyiarkan semua interface termasuk adapter virtual WSL/Hyper-V/Bluetooth link-local); fallback ke `enable_addr_auto()` hanya bila enumerasi IP kosong/gagal (`lan.rs:92-110`).
- Peer tanpa properti TXT `fp` dilewati tanpa dikirim ke konsumer (`lan.rs:126-132`).

### 4.3 Jalur Tor (`src/transport/tor.rs`)

- `TorContext` menyatukan client `arti-client` yang sudah bootstrap, handle onion service berjalan, alamat `.onion` sendiri, dan channel penerima stream masuk (`tor.rs:32-40`).
- `TOR_VIRTUAL_PORT = 9999` — port virtual protokol saat initiator connect ke onion peer, bukan port OS nyata yang di-bind (`tor.rs:27-29`).
- `TorClient::create_bootstrapped(config).await` dipanggil **tanpa timeout eksplisit**; komentar modul hanya menyebut proses ini lambat (~30-60 detik) — bila bootstrap menggantung, `launch()` berpotensi menggantung tanpa batas dari sisi caller (`tor.rs:9-60`).
- Constants retry: `TOR_DIAL_TOTAL_TIMEOUT`, `TOR_DIAL_RETRY_DELAY`, `TOR_ACCEPT_TIMEOUT` (`mod.rs:109-116`). `fn tor_dial_with_retry` (`mod.rs:174-197`, deklarasi 180, retry-loop 186-196) melakukan retry dial ke onion address peer dengan delay tetap `TOR_DIAL_RETRY_DELAY = 8 detik` antar percobaan, sampai total timeout `TOR_DIAL_TOTAL_TIMEOUT = 120 detik` — mengakomodasi keterlambatan propagasi onion descriptor (~1-3 menit setelah bootstrap Tor, menurut komentar kode).
- `accept_timeout()` mengunci `Mutex` pada receiver `incoming`, membungkus `rx.recv()` dengan `tokio::time::timeout`; hasil di-flatten via `.ok().flatten()` sehingga caller **tidak bisa membedakan** "waktu habis" dari "channel sudah tertutup" — keduanya sama-sama `None` (`tor.rs:117-120`).
- State/cache Tor diturunkan dari nama file vault dengan pola `<stem>-tcache`/`<stem>-tstate` di folder induk vault, supaya instance dengan vault berbeda tidak berbagi state Tor (`main.rs:135-151`).
- Seluruh error di modul ini dikonversi ke satu varian `Error::Tor(String)` via `.to_string()`/`format!()` — tipe/struktur error asli dari `arti-client`/`tor-hsservice` hilang di titik ini (`tor.rs:56,60,66,69,73,74,78,111`).

### 4.4 Framing (`src/transport/frame.rs`)

Format frame di atas kabel: **`[2-byte big-endian length][payload]`**. `MAX_FRAME_LEN = 65535` (`frame.rs:16`), persis batas atas `u16` — kebetulan sama dengan batas maksimum satu pesan Noise (spec Noise = 65535 byte), sehingga 1 frame = 1 pesan Noise tanpa fragmentasi di layer ini (`frame.rs:1-9`, verifikasi kode langsung untuk `MAX_FRAME_LEN` HIGH; korespondensi "1 frame = 1 pesan Noise" adalah asersi komentar, MEDIUM — tidak diverifikasi silang langsung terhadap modul session/crypto dalam audit file ini).

- `write_frame`: menolak `payload.len() > MAX_FRAME_LEN` dengan `Error::FrameTooLarge`; jika lolos, tulis 2-byte BE length lalu payload, lalu `flush()` (`frame.rs:19-31`).
- `read_frame`: `UnexpectedEof` saat membaca header length ditafsirkan sebagai **koneksi ditutup bersih**, mengembalikan `Ok(0)` (bukan error) — dikonsumsi caller sebagai "peer keluar dari room"; error IO lain dibungkus `Error::Io`; panjang yang dideklarasikan melebihi kapasitas buffer → `Error::FrameTooLarge` sebelum membaca payload (`frame.rs:37-56`).
- **`read_frame` TIDAK cancel-safe**: dua `read_exact` berurutan (header lalu payload) berarti bila future-nya dibatalkan (mis. kalah dalam `tokio::select!`) di tengah pembacaan payload, byte yang sudah terkonsumsi hilang bersama future, dan pembacaan berikutnya menafsirkan sisa payload lama sebagai header panjang baru — stream desync (dibuktikan langsung oleh test `read_frame_yang_dibatalkan_merusak_sinkronisasi_stream`, `frame.rs:105-141`, bukan sekadar klaim komentar). Ini alasan langsung mengapa `session::run_session` memindahkan pembacaan frame ke task terpisah (§6.2).

---

## 5. Handshake Noise_IK (CORE-1)

Nama pattern lengkap: **`Noise_IK_25519_ChaChaPoly_BLAKE2s`**, via crate `snow` 0.10.0 (`crypto/handshake.rs:3-21`, CR-007..CR-011). Justifikasi pemilihan pola/algoritma sudah dibahas penuh di `04_CRYPTOGRAPHIC_JUSTIFICATION.md` CORE-1/CORE-2/CORE-3/CORE-4 dan tidak diulang di sini — bagian ini fokus pada **alur pesan dan orkestrasinya**.

### 5.1 Alur 2 Pesan

```
Initiator                                          Responder
(sudah tahu static-key Responder, dari kontak)      (belum tahu static-key Initiator)

  --- Pesan 1: e, es, s, ss --->
      (ephemeral pub, DH(e_i, s_r), static pub terenkripsi, DH(s_i, s_r))

                                                     verifikasi opsional: remote_static()
                                                     dibandingkan peer_noise_pk yang
                                                     diharapkan (jika kontak dikenal)

  <--- Pesan 2: e, ee, se ---
      (ephemeral pub, DH(e_i, e_r), DH(e_i, s_r))

      [kedua sisi -> into_transport() -> EncryptedSession]
```

Dikonfirmasi empiris oleh `do_handshake()` yang memanggil `write_message`/`read_message` tepat 2 kali per sisi (`crypto/handshake.rs:109-129`, dipakai 3 dari 4 test — `wrong_peer_key_fails_handshake` sengaja hanya menjalankan pesan 1 secara manual untuk menguji kegagalan sebelum pesan 2 terkirim, `handshake.rs:193-217`).

- `HandshakeSession::new_initiator` menerima `local_noise_privkey` **dan** `peer_noise_pubkey` (masing-masing `&[u8;32]`) — pola `IK` mensyaratkan initiator **sudah tahu** static key responder sebelum handshake dimulai (`handshake.rs:32-38`).
- `HandshakeSession::new_responder` hanya menerima `local_noise_privkey`; peer's public key **belum diketahui** di awal, baru diverifikasi setelah membaca pesan pertama — khas pola `IK` (`handshake.rs:40-48`).
- `write_message()`/`read_message()` adalah wrapper tipis ke `snow::HandshakeState`, error dipetakan seragam ke `Error::Noise` (`handshake.rs:52-60`).
- `into_transport()` mengonsumsi `HandshakeSession` (by value), memanggil `into_transport_mode()` snow, menghasilkan `EncryptedSession` baru; memanggil ini sebelum handshake selesai menghasilkan error (komentar kode, `handshake.rs:68-73`).

### 5.2 Orkestrasi di `session::run_session` (CR-026/CR-027, `src/session/mod.rs:117-159`)

- `run_session` menerima `local_noise_sk: [u8; 32]` dan `peer_noise_pk: Option<[u8; 32]>` (`session/mod.rs:96-97`).
- **Initiator**: `peer_noise_pk` **wajib** `Some` — jika `None`, `run_session` mengembalikan `Err(Error::InvalidKey)` **sebelum** handshake dimulai (`mod.rs:119`). Blok initiator mengirim pesan 1 (`-> e, es, s, ss`, `mod.rs:122`) lalu membaca pesan 2 (`<- e, ee, se`, `mod.rs:127-131`); EOF saat membaca (n==0) → `Error::ConnectionClosed`.
- **Responder**: membaca pesan 1 (`<- e, es, s, ss`, `mod.rs:138-143`), lalu **jika** `peer_noise_pk` berisi nilai (kontak sudah dikenal), dibandingkan dengan `hs.remote_static()` — ketidakcocokan **atau** remote static key tidak ada → `Err(Error::IdentityMismatch)`, komentar kode secara eksplisit menyebut ini **"fail closed"** untuk mencegah impersonation (`mod.rs:145-151`, dikonfirmasi test `responder_rejects_unknown_peer`, `mod.rs:502-553`). Lalu mengirim pesan 2 (`-> e, ee, se`, `mod.rs:153-155`).

> **Temuan kritis (bawa ke `08_THREAT_MODEL.md`)**: bila responder memanggil `run_session` dengan `peer_noise_pk = None` (kontak **belum** dikenal), **tidak ada pengecekan identitas peer sama sekali** pada jalur kode ini — verifikasi identitas sepenuhnya bergantung pada caller yang menyediakan `peer_noise_pk` yang benar. Ini kemungkinan desain *trust-on-first-use* yang disengaja, namun tidak dapat dipastikan tanpa membaca pemanggil (mis. logika contacts/tui) — status `NEEDS_CONFIRMATION`/MEDIUM (`session.json`).

### 5.3 Properti Keamanan yang Diklaim vs. Diverifikasi

| Properti | Sumber klaim | Status verifikasi |
|---|---|---|
| Mutual authentication (di akhir handshake) | Doc-comment `handshake.rs:14-17`; diverifikasi PARSIAL — hanya sisi Responder yang diuji memanggil `remote_static()` (test `responder_verifies_initiator_identity`, `handshake.rs:174-191`); tidak ada test yang memanggil `remote_static()` di sisi Initiator | MEDIUM |
| Forward secrecy (ephemeral key per sesi) | Doc-comment `handshake.rs:14-17` | **DOCUMENTED_ONLY** — tidak ada test yang membandingkan ephemeral key antar sesi (`crypto_handshake.json`) |
| Kerahasiaan static key Initiator terhadap penyadap pasif | Doc-comment `handshake.rs:14-17` | **DOCUMENTED_ONLY** — tidak ada test yang memeriksa ciphertext static-key (`crypto_handshake.json`) |
| Autentikasi implisit via kegagalan DH (`es`) saat peer key salah | Test `wrong_peer_key_fails_handshake` (`handshake.rs:193-217`) | CONFIRMED, dengan catatan: token `es` = DH(initiator ephemeral, **responder** static) — mengautentikasi apakah initiator menghubungi responder yang benar, **bukan** memverifikasi static key initiator sendiri (koreksi presisi dari `crypto_handshake.json`) |

Ketiga properti pertama berasal dari properti umum pola Noise_IK yang terdokumentasi di `noise2018`, **bukan** klaim yang diverifikasi secara independen dari test suite AKSARA sendiri — jangan menyatakan "terverifikasi penuh" di BAB manapun (mandat `SESSION_2_HANDOFF.md`).

### 5.4 Batasan dan Confidence

- **Sub-mekanisme internal Noise (hash transcript `mix_hash`, HKDF `mix_key`, keduanya berbasis BLAKE2s) confidence LOW** — murni inferensi dari token nama pattern `BLAKE2s`; tidak ada satu baris kode pun di `handshake.rs`/`session/mod.rs` yang memanggilnya langsung (CR-009/CR-010). **Jangan overclaim "terverifikasi penuh"** pada bagian ini di BAB manapun.
- Tidak ada pengecekan eksplisit di `handshake.rs` terhadap public key peer yang all-zero/low-order point — kepercayaan sepenuhnya pada implementasi internal `snow`+`x25519-dalek`.
- Seluruh test mengirim payload handshake **kosong** (`&[]`, `handshake.rs:115-122,210`) — pengiriman data aplikasi bersamaan handshake (0-RTT payload) **tidak diuji** dalam file ini.
- Semua error dari `write_message`/`read_message`/`into_transport_mode` dipetakan seragam ke `Error::Noise` tanpa diferensiasi jenis kegagalan (5 titik pemakaian identik, `handshake.rs:53,59,71,92,97`) — mengurangi granularitas debugging namun juga mengurangi permukaan *oracle leak*.
- Crate `snow` **belum diaudit keamanan formal** (self-declared pada dokumentasi resminya) — sudah dicatat di `04_CRYPTOGRAPHIC_JUSTIFICATION.md` CORE-1 poin 5, tidak diulang detailnya di sini.

---

## 6. Fase Transport Terenkripsi (`session::run_session`)

Setelah handshake selesai, `hs.into_transport()` menghasilkan `EncryptedSession` (`handshake.rs:68-73`, dipanggil di `mod.rs:133` untuk Initiator dan `mod.rs:157` untuk Responder).

### 6.1 State dan Event

- `enum SessionState { Connecting, Handshaking, Active, Closed }` (`mod.rs:19-25`). Catatan: varian `Connecting` dideklarasikan tapi **tidak pernah dikirim** sebagai event dari dalam `run_session` — hanya `Handshaking` (`mod.rs:107`), `Active` (`mod.rs:161`), dan `Closed` (`mod.rs:277`) yang benar-benar dikirim; kemungkinan `Connecting` diset caller sebelum memanggil `run_session` (tidak diverifikasi, di luar cakupan file ini).
- `enum SessionEvent { StateChanged, Message, PeerBlur, PeerLeft, Notice, Error }` adalah **satu-satunya** antarmuka keluar dari `run_session` ke lapisan UI, lewat `UnboundedSender<SessionEvent>` (`mod.rs:70-84`). Catatan: varian `SessionEvent::Error` dideklarasikan untuk "error fatal" tapi **tidak pernah dikonstruksi/dikirim** di dalam `run_session` — kegagalan handshake/sesi dikembalikan lewat `Result<(), Error>` fungsi (`Error::InvalidKey`, `Error::ConnectionClosed`, `Error::IdentityMismatch`), bukan lewat channel events.

### 6.2 Model Konkurensi dan Cancel-Safety

- `tokio::io::split(stream)` memberi handle baca (`rd`)/tulis (`wr`) independen, bekerja generik untuk `TcpStream` (LAN) maupun `arti::DataStream` (Tor) lewat bound generic `S` (`mod.rs:111`).
- Pembacaan frame dipindahkan ke **task `tokio::spawn` terpisah**, dikomunikasikan lewat channel internal `RxFrame` — secara eksplisit **karena** `read_frame` tidak cancel-safe di dalam `tokio::select!` (§4.4) (`mod.rs:166-190`).
- Loop aktif sesi memakai `tokio::select!` dengan **3 cabang**: penerimaan `SessionCmd` dari UI, tick keepalive, dan penerimaan `RxFrame` dari task pembaca — ketiganya adalah primitif cancel-safe (`recv()`, `tick()`) (`mod.rs:198-271`).
- `reader.abort()` dipanggil eksplisit setelah loop `select` selesai, karena men-drop channel saja tidak akan membangunkan task pembaca yang sedang menunggu I/O dari peer yang diam (`mod.rs:273-275`).

### 6.3 Format Payload Plaintext

1 byte tag jenis di depan, lalu body sesuai jenis (`mod.rs:36-41`):

| Tag | Nilai | Body |
|---|---|---|
| `TYPE_TEXT` | `0x00` | byte UTF-8 teks pesan |
| `TYPE_BLUR` | `0x01` | tepat 1 byte tambahan: `on as u8` |
| `TYPE_PING` | `0x02` | tidak ada body (payload total 1 byte) |

- `SessionCmd::Text` → `[TYPE_TEXT][utf8 bytes]` sebelum dienkripsi (`mod.rs:203-209`).
- `SessionCmd::Blur(on)` → persis 2 byte `[TYPE_BLUR, on as u8]` (`mod.rs:210`).
- Keepalive ping: payload plaintext 1 byte `[TYPE_PING]`, dienkripsi dan dikirim tiap tick interval; penerima mencocokkan `TYPE_PING` dan **mengabaikannya** (tanpa balasan otomatis, tidak diteruskan ke UI) (`mod.rs:232-264`, dikonfirmasi test `keepalive_ping_is_not_delivered_as_message`, `mod.rs:462-498`).
- Setelah dekripsi berhasil, dispatch berdasarkan byte pertama plaintext: `TYPE_TEXT` → `SessionEvent::Message` via `String::from_utf8_lossy`; `TYPE_BLUR` hanya diproses jika panjang payload ≥ 2 byte → `SessionEvent::PeerBlur(pt[1]==0x01)`; byte tipe tak dikenal **diabaikan** tanpa dianggap fatal (`mod.rs:256-266`).
- `KEEPALIVE_INTERVAL` = 30 detik pada build non-test, 5 milidetik pada build `#[cfg(test)]` (`mod.rs:59-68`).
- **Tidak ada Associated Data (AAD)** yang memisahkan domain `TYPE_TEXT`/`TYPE_BLUR`/`TYPE_PING` pada level AEAD — pemisahan jenis pesan terjadi **setelah** dekripsi lewat byte tag pertama, bukan bagian dari proses autentikasi AEAD itu sendiri (`session.json`, misuse_risk_notes).

### 6.4 Batas Ukuran Pesan

Komentar kode dan test menyatakan batas ukuran pesan Noise transport adalah **65535 byte** (selaras batas `MAX_FRAME_LEN`, §4.4); payload yang melebihi batas ini membuat `session.encrypt` gagal, dan kegagalan itu ditangani sebagai `SessionEvent::Notice` **non-fatal** — sesi tetap hidup, bukan mati (`mod.rs:212-224`, dikonfirmasi test `oversized_message_does_not_kill_session` dengan payload 70.000 byte, `mod.rs:409-457`).

Overhead AEAD 16 byte (tag) terlihat konsisten pada alokasi buffer ciphertext (`payload.len()+16` untuk pesan chat, `1+16` untuk ping, `mod.rs:212,233`) — **algoritma AEAD konkret tidak disebutkan literal** di `session/mod.rs` sendiri; diasumsikan ChaCha20-Poly1305 (default `snow` untuk pola Noise ini, selaras `04_CRYPTOGRAPHIC_JUSTIFICATION.md` CORE-3), namun tidak diverifikasi langsung dari file ini (confidence MEDIUM).

### 6.5 Error Handling dan Penutupan Sesi

| Kejadian | Penanganan | Evidence |
|---|---|---|
| `encrypt()` gagal untuk pesan chat keluar (mis. terlalu besar) | Non-fatal: `SessionEvent::Notice`, loop `continue`, sesi tetap hidup | `mod.rs:212-227` |
| `encrypt()` gagal untuk ping keepalive | Fatal: loop `break` | `mod.rs:233-241` |
| `decrypt()` gagal pada frame masuk | Fatal: loop `break` **segera**, komentar eksplisit "fail closed" | `mod.rs:253-268` |
| Kegagalan I/O pada `write_frame` (kirim/ping) | Fatal: loop `break` | `mod.rs:212-241` |

Setelah `decrypt()` gagal, fungsi tetap mengirim `SessionEvent::StateChanged(Closed)` dan mengembalikan `Ok(())` — **bukan** `Err`, dan **tanpa** mengirim `SessionEvent::Error` yang berbeda dari penutupan normal. Akibatnya, **UI tidak dapat membedakan** "sesi ditutup karena dekripsi gagal (potensi tampering)" dari penutupan normal lainnya, kecuali event `PeerLeft` yang khusus menandai EOF bersih dari `read_frame` (`mod.rs:246-249`). Deteksi koneksi mati selama sesi aktif sepenuhnya bergantung pada kegagalan `write_frame`, **bukan** pada ping yang tak terbalas — dinyatakan eksplisit dalam komentar kode sebagai keterbatasan yang disengaja untuk M1, dengan upgrade path "batas tak-ada-frame-masuk-selama-N-detik" yang belum diimplementasikan (`mod.rs:54-58`).

Tidak ada mekanisme rotasi kunci: satu kunci transport dipakai sepanjang masa hidup sesi (dari selesainya handshake sampai `session` di-drop di akhir fungsi). Zeroization kunci transport saat sesi ditutup **tidak dapat diverifikasi** dari `session/mod.rs` (bergantung pada perilaku internal `snow`/`crypto::handshake` yang tidak diaudit di titik ini) — detail lengkap kunci dan zeroization dibahas di `07_KEY_LIFECYCLE.md`.

Tidak ditemukan pemanggilan crate logging (`log::`/`tracing::`) di `session/mod.rs` maupun `crypto/handshake.rs` — seluruh pelaporan status/diagnostik ke UI dilakukan lewat channel `SessionEvent`.

---

## 7. Ringkasan Confidence (Level Protokol)

| Klaim | Confidence | Catatan anti-overclaim |
|---|---|---|
| Orkestrasi handshake 2-pesan (`run_session`, `do_handshake`) | HIGH | Diverifikasi empiris via test + pembacaan kode langsung |
| Sub-mekanisme internal Noise (hash/HKDF berbasis BLAKE2s) | **LOW** | Murni inferensi nama pattern string, tidak ada pemanggilan langsung di source aplikasi |
| Fail-closed identity check untuk kontak dikenal (Responder) | HIGH | Diverifikasi test `responder_rejects_unknown_peer` |
| (Ketiadaan) identity check untuk kontak belum dikenal (`peer_noise_pk=None`) | HIGH (untuk fakta ketiadaannya) | Interpretasi "trust-on-first-use yang disengaja" bersifat `NEEDS_CONFIRMATION` |
| Forward secrecy, identity-hiding parsial, mutual-auth penuh | MEDIUM/DOCUMENTED_ONLY | Properti umum Noise_IK (`noise2018`), tidak diverifikasi test AKSARA sendiri |
| Algoritma AEAD konkret pada transport sesi (`session.encrypt/decrypt`) | MEDIUM | Tidak disebut literal di `session/mod.rs`, diasumsikan ChaCha20-Poly1305 dari default `snow` |
| Batas pesan 65535 byte, non-fatal pada oversize | HIGH | Diverifikasi test `oversized_message_does_not_kill_session` |
| `read_frame` tidak cancel-safe, dimitigasi via task terpisah | HIGH | Diverifikasi test `read_frame_yang_dibatalkan_merusak_sinkronisasi_stream` |

---

## 8. Bukti Empiris (Cakupan Test)

| Test | File | Yang diverifikasi |
|---|---|---|
| `handshake_ik_roundtrip` | `crypto/handshake.rs:131-145` | Handshake IK 2-pesan lengkap berhasil, `is_finished()==true` kedua sisi |
| `transport_encrypt_decrypt_roundtrip` | `crypto/handshake.rs:147-172` | Enkripsi/dekripsi transport pasca-handshake byte-per-byte identik |
| `responder_verifies_initiator_identity` | `crypto/handshake.rs:174-191` | `remote_static()` responder cocok dengan public key initiator |
| `wrong_peer_key_fails_handshake` | `crypto/handshake.rs:193-217` | Peer key salah → `read_message` gagal (kegagalan DH `es`) |
| `lan_session_message_roundtrip` | `session/mod.rs:302-358` | 2 task `run_session` nyata di atas TCP loopback, handshake penuh, pesan dua arah |
| `blur_toggle_roundtrip` | `session/mod.rs:363-404` | Byte tag `TYPE_BLUR` roundtrip end-to-end |
| `oversized_message_does_not_kill_session` | `session/mod.rs:409-457` | Payload 70.000 byte → `Notice`, bukan `Error`; sesi tetap hidup |
| `keepalive_ping_is_not_delivered_as_message` | `session/mod.rs:462-498` | `TYPE_PING` difilter, tidak bocor sebagai `SessionEvent::Message` |
| `responder_rejects_unknown_peer` | `session/mod.rs:502-553` | `peer_noise_pk` salah → `Err(Error::IdentityMismatch)` |
| `frame_roundtrip`, `multiple_frames_in_order`, `eof_returns_zero` | `transport/frame.rs:62-95` | Framing dasar benar |
| `read_frame_yang_dibatalkan_merusak_sinkronisasi_stream` | `transport/frame.rs:105-141` | Membuktikan `read_frame` bukan cancel-safe |
| `oversized_payload_rejected` | `transport/frame.rs:143-151` | `write_frame` menolak payload > `MAX_FRAME_LEN` |
| `safe_label_*`, `lan_dialable_*` (4 test) | `transport/lan.rs:161-197` | Truncation label DNS aman-UTF8, filter alamat IPv4 dialable |
| `invite_roundtrip_*`, `invite_rejects_*`, `fingerprint_*` (6 test) | `contacts/mod.rs:204-323` | Invite code dan fingerprint pengikat kedua key |

---

## Referensi

Seluruh referensi teori pada dokumen ini menggunakan citekey yang **sudah ada** di `references/REFERENCES.bib` (TAHAP 4/9): `noise2018` (properti Noise_IK), `rfc7748`/`bernstein2006curve25519` (X25519), `rfc8439` (ChaCha20-Poly1305), `rfc7693`/`aumasson2013blake2` (BLAKE2s). Ditambahkan 2 entry baru pada `references/REFERENCES.bib` (SESSION 3, dicatat di `references/REFERENCE_MATRIX.md`) untuk konteks mekanisme discovery LAN yang belum tercakup TAHAP 4/9:

- `rfc6762` (Cheshire & Krochmal, *Multicast DNS*, RFC 6762, 2013) — spesifikasi mDNS yang diimplementasikan `mdns-sd` 0.20.0 dan dipakai `transport/lan.rs`.
- `rfc6763` (Cheshire & Krochmal, *DNS-Based Service Discovery*, RFC 6763, 2013) — spesifikasi format service-type/TXT-record (`_aksara._tcp.local.`, `fp=<hex>`) yang dipakai `advertise()`/browse.

Kedua RFC ini dikutip sebagai **konteks mekanisme protokol pihak ketiga** (apa yang secara struktural terbuka pada mDNS/DNS-SD), bukan sebagai bukti properti keamanan AKSARA sendiri — analisis ancaman metadata leak-nya ada di `08_THREAT_MODEL.md` §4.2.
