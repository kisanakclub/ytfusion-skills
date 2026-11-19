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
Instalasi kosong mengikuti [panduan tambah channel dan koneksi Drive](skills/ytfusion-operations/references/accounts.md),
termasuk pemilihan metode login, impor koneksi, serta pemeriksaan hasilnya.
Jika perlu project sendiri, ikuti [panduan GCP, branding, dan publish](skills/ytfusion-operations/references/google-project.md).
Agen menyiapkan project/API, halaman publik, client, dan pemasangannya sesuai
tugas. Hosting dipilih dari yang bisa dipakai: website yang sudah ada,
Cloudflare Pages, atau GitHub Pages; hasil publish/verifikasi dicatat terpisah.

Untuk tugas Muse yang mengambil video final tanpa dashboard, tersedia
[panduan executor Muse](skills/ytfusion-operations/references/muse-executor.md):
konektor Drive atau API, uploader YouTube resumable, catatan job privat, dan
scheduler bawaan. Pemeriksaan satu instance menemukan fasilitas pendukungnya,
tetapi unduh/upload nyata belum diuji. Panduan ini belum menyertakan helper
uploader mandiri atau membuat jadwal otomatis.

## Mulai di Muse

Copas perintah berikut ke Muse baru. Perintah ini meminta agen **mengambil source
YtFusion dan skill**, memeriksa jalur eksekusi, lalu menyiapkan tugas awal beserta
instalasi yang diperlukan. Ini bukan script installer otomatis dari repo skill.

```text
Siapkan instance ini untuk mengoperasikan YtFusion.

1. Periksa instalasi dan profil penugasan yang sudah ada. Kalau belum ada,
   ambil https://github.com/kisanakclub/ytfusion-skills dan baca
   skills/ytfusion-operations/SKILL.md beserta references/setup.md.
   Kalau sudah ada, gunakan checkout itu dan baca panduan yang sama.
2. Untuk tugas upload final di Muse, baca references/muse-executor.md dan
   periksa konektor/API serta scheduler yang tersedia. Ambil source dari
   https://github.com/kisanakclub/Yt_FusionX untuk mempelajari logic dan
   gunakan dependency yang diperlukan. Jika memilih alur aplikasi native,
   install sesuai AGENTS.md dan panduan platform setelah memeriksa kecocokan
   host. Pertahankan instalasi, data, dan konfigurasi yang sudah ada.
3. Pasang/daftarkan skill melalui mekanisme yang benar-benar didukung agen ini
   jika tersedia. Simpan petunjuk untuk menemukan skill dan profil pada tugas
   berikutnya; jangan anggap clone saja sudah mengaktifkan skill otomatis.
4. Tugas awal instance ini: persiapan upload video final dari Google Drive,
   tanpa generate atau render HDS. Evaluasi jalur executor Muse terlebih
   dahulu. Pelajari logic metadata, mapping channel, jadwal, riwayat, dan
   pemulihan YtFusion yang relevan. Jangan anggap uploader mandiri sudah ada.
5. Jika jalur terpilih memerlukan client Google sendiri dan belum ada project
   yang ditugaskan, ikuti
   references/google-project.md untuk menyiapkan project sendiri: aktifkan API
   yang diperlukan, siapkan branding dan halaman publik di hosting yang bisa
   dipakai, lakukan publish In production serta verifikasi yang diperlukan,
   lalu buat dan pasang client Web/Desktop sesuai jalur login yang tersedia.
   Periksa hasilnya; jangan berhenti pada memberikan link panduan.
   Untuk aplikasi native, ikuti references/accounts.md. Untuk executor Muse,
   gunakan koneksi yang benar-benar didukung konektor/uploader terpilih.
   Pelajari UI dan handler login yang terpasang, pilih
   metode yang cocok, lalu siapkan dan periksa koneksinya. Gunakan koneksi yang
   sudah ada. Tanyakan hanya akses atau pilihan yang masih kurang: akun pemilik
   GCP, channel, sumber Drive, jadwal/zona waktu, privasi, serta izin kerja
   berkelanjutan. Arahkan login dan isian rahasia lewat UI yang sesuai.
   Jangan minta token atau password ditempel ke chat.
6. Simpan profil penugasan pribadi di luar kedua repo agar nanti cukup
   dilanjutkan. Untuk profil baru, mulai satu upload bersamaan dan simpan
   sumber video. Pertahankan pengaturan aplikasi yang sudah ada.
7. Selesaikan pemasangan dan setup yang sudah bisa dilakukan. Laporkan
   kesiapan dan kebutuhan yang benar-benar belum tersedia. Jalankan upload
   atau Live setelah ada tugas/penugasan yang mengizinkannya.
   Tugas berulang baru dibuat setelah diminta, sumber/tujuan jelas, dan jalur
   transfer terbukti. Jadwal persisten tidak menjamin proses upload tahan putus.
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
penyiapan sesuai jalur eksekusi yang dipilih. Paket skill tidak membuat koneksi agen ke
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
