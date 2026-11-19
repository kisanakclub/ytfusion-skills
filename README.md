# YtFusion Skills

Skill opsional untuk agen AI yang mengoperasikan YtFusion. Paket ini terpisah
dari aplikasi dan dapat diperbarui sendiri.

The workflow instructions use the Agent Skills format. The agent should answer
in the user's language and use the tools available in its own environment.

## YtFusion Operations

Menyiapkan instalasi baru dan menjalankan tugas upload video final dari Drive,
Regular Studio, serta Live dengan API atau tanpa API. Agen membaca alur aplikasi
yang sesuai tugasnya dan menyimpan penugasan pribadi tiap instance agar setup
dasar tidak diulang. Lihat [instruksi skill](skills/ytfusion-operations/SKILL.md)
dan [setup serta profil penugasan](skills/ytfusion-operations/references/setup.md).

## Mulai di Muse

Copas perintah berikut ke Muse baru. Perintah ini meminta agen **memasang aplikasi
YtFusion dan mengambil skill**, lalu menyiapkan tugas awal. Ini bukan script
installer yang langsung dijalankan oleh repo skill.

```text
Siapkan instance ini untuk mengoperasikan YtFusion.

1. Periksa instalasi dan profil penugasan yang sudah ada. Kalau belum ada,
   ambil https://github.com/kisanakclub/ytfusion-skills dan baca
   skills/ytfusion-operations/SKILL.md beserta references/setup.md.
   Kalau sudah ada, gunakan checkout itu dan baca panduan yang sama.
2. Kalau YtFusion belum terpasang, clone dan install aplikasi dari
   https://github.com/kisanakclub/Yt_FusionX sesuai AGENTS.md dan panduan
   platform di repo aplikasi. Periksa dulu kecocokan lingkungan Muse dan
   kebutuhan tugas. Kalau sudah terpasang, pertahankan data dan konfigurasinya.
3. Pasang/daftarkan skill melalui mekanisme yang benar-benar didukung agen ini
   jika tersedia. Simpan petunjuk untuk menemukan skill dan profil pada tugas
   berikutnya; jangan anggap clone saja sudah mengaktifkan skill otomatis.
4. Tugas awal instance ini: YT Upload untuk video final dari Google Drive,
   tanpa generate atau render HDS. Pelajari alur YT Upload yang terpasang,
   format paket/metadata, antrean, jadwal, riwayat, dan pemulihannya.
5. Gunakan koneksi yang sudah ada. Tanyakan hanya akses atau pilihan yang
   masih kurang: akun/channel, sumber Drive, jadwal/zona waktu, privasi,
   serta izin kerja berkelanjutan. Arahkan login dan isian rahasia lewat UI
   yang sesuai. Jangan minta token atau password ditempel ke chat.
6. Simpan profil penugasan pribadi di luar kedua repo agar nanti cukup
   dilanjutkan. Untuk profil baru, mulai satu upload bersamaan dan simpan
   sumber video. Pertahankan pengaturan aplikasi yang sudah ada.
7. Selesaikan pemasangan dan setup yang sudah bisa dilakukan. Laporkan
   kesiapan dan kebutuhan yang benar-benar belum tersedia. Jalankan upload
   atau Live setelah ada tugas/penugasan yang mengizinkannya.
```

Repo aplikasi Private memerlukan akses GitHub. Jika belum tersedia, agen
mengarahkan login akun yang punya akses; repo skill tidak memberikan akses
aplikasi atau akun Google. Ganti tugas pada poin 4 untuk instance Regular/Live,
atau beri tugas tambahan setelah setup. Contoh perubahan penugasan:

```text
Instance ini khusus Live tanpa API dari video final di Drive. Gunakan profil
penugasan yang sudah ada dan panduan Live. Siapkan sumber serta stream-nya;
jangan mulai siaran dulu. Tanyakan hanya data yang masih kurang.
```

Untuk melanjutkan, cukup beri tugas seperti “Lanjutkan tugas YtFusion sesuai
profil instance ini; cek antrean yang sudah ada sebelum memulai pekerjaan baru.”
Agen tetap memerlukan akses ke profil dan aplikasi pada sesi tersebut.

Panduan ini belum membuktikan pemasangan atau Studio/Live berjalan di Muse.
Kemampuan runtime, alamat dashboard/OAuth, penyimpanan, dan jaringan harus
diperiksa pada instance sebenarnya. Menyalin skill bukan proses melatih model
atau jaminan akses lintas chat; gunakan dukungan skill/memori agen yang tersedia.

## HDS Home Production

Membantu membuat Master baru, menyiapkan channel dan stok, mengkurasi referensi,
membagi koleksi, serta menjalankan atau melanjutkan produksi melalui HDS.
Lihat [kemampuan dan contoh perintah](skills/hds-home-production/references/capabilities.md).

## YtFusion Domain and VPS

Memeriksa domain dan koneksi VPS, memasang HTTPS, serta memindahkan alamat
dashboard melalui **YouTube API Setup** dan **Server Transfer** di instalasi
YtFusion. Lihat [instruksi skill](skills/ytfusion-domain-vps/SKILL.md).

    Pakai $ytfusion-domain-vps untuk cek HTTPS dan koneksi Server Transfer VPS saya.
    Cek status saja.

## Pasang

Untuk Codex yang menyediakan skill-installer, gunakan permintaan:

    Gunakan skill-installer untuk memasang skill dari
    https://github.com/kisanakclub/ytfusion-skills/tree/main/skills/hds-home-production

    Gunakan skill-installer untuk memasang skill dari
    https://github.com/kisanakclub/ytfusion-skills/tree/main/skills/ytfusion-domain-vps

    Gunakan skill-installer untuk memasang skill dari
    https://github.com/kisanakclub/ytfusion-skills/tree/main/skills/ytfusion-operations

Untuk agen lain yang mendukung Agent Skills, pasang folder
skill yang ingin dipakai pada lokasi yang didukung agen tersebut.
Cara pemasangan dan akses alat mengikuti dokumentasi agen masing-masing.
Menyalin folder sumber ke lokasi biasa belum membuatnya otomatis aktif.

Paket ini berisi instruksi dan satu helper Python read-only. Mengambil paket ini
saja tidak memasang YtFusion. Perintah **Mulai di Muse** meminta agen melakukan
pemasangan aplikasi sesuai panduannya. Paket skill tidak membuat koneksi agen ke
komputer dan tidak menambahkan provider ke edisi yang tidak menyediakannya.

## Mulai

    Pakai HDS Home Production. Jelaskan kemampuan yang tersedia pada device ini.

Atau langsung beri tugas:

    Buat Master baru untuk 12 channel berbahasa Spanyol, masing-masing 50 judul.
    Siapkan sampai setup saja. Gunakan referensi yang cocok jika tersedia.

    Lanjutkan koleksi yang saya pilih sampai gambar dan thumbnail selesai.
    Pertahankan hasil yang sudah valid.

Agen memerlukan akses yang sesuai ke instalasi HDS dan koleksi yang dikerjakan.
HDS Master tidak wajib tersedia pada device pelaksana: koleksi produksi yang
mandiri dapat dikerjakan tanpa membawa seluruh bank Master.

## Private dan Shared

Prosedur skill dapat dipakai dengan kedua edisi, sesuai fitur yang tersedia.
Provider, preset dan target produksi mengikuti instalasi serta pilihan pengguna.
Skill tidak membawa engine Private dan tidak mengganti provider diam-diam.

## Data pengguna

Master pribadi, stok judul, gambar referensi, Batch, hasil produksi, profil
penugasan instance, catatan channel/Drive, dan kredensial disimpan terpisah dari
repo ini. Master starter dapat menjadi paket pendamping opsional; versi awal ini
tidak menyertakan starter atau media pihak ketiga.

## Verifikasi pengembangan

    python3 -m unittest discover -s tests -v

Helper menggunakan pustaka standar Python 3.9 atau lebih baru. Pemeriksaan
diagnostik tidak membuktikan readiness native atau kualitas hasil produksi.
Pengujian lintas agen, lintas edisi dan antar-device dicatat terpisah di
[catatan kompatibilitas](skills/hds-home-production/references/compatibility.md).
