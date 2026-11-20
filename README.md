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
tugas. Untuk halaman branding Muse baru, pilihan utama adalah **Firebase Hosting
Spark**, mengikuti pilot. Website yang sudah ditugaskan tetap dipakai; hosting
lain menjadi cadangan bila Firebase tidak memenuhi kebutuhan nyata. Hasil
publikasi Audience, branding dan verifikasi dicatat terpisah dari hosting.

Untuk tugas Muse yang mengambil video final tanpa dashboard, tersedia
[panduan executor Muse](skills/ytfusion-operations/references/muse-executor.md):
konektor Drive atau API, uploader YouTube resumable, catatan job privat, dan
scheduler bawaan. Pilot 20 November 2026 membuktikan unduh Drive tervalidasi,
upload private dari VM, baca Analytics, serta perbaikan pengaturan, thumbnail
dan playlist. Sinkronisasi riwayat Drive, cleanup pasca-upload, penjadwalan
berulang dan sustained Live belum terbukti dalam pilot itu. Ini paket instruksi,
bukan uploader/scheduler siap jalan. Baca
[onboarding Muse](skills/ytfusion-operations/references/muse-onboarding.md) dan
[kontrak upload lengkap](skills/ytfusion-operations/references/upload-workflow.md).

## YtFusion Channel Analytics

Membaca channel yang sudah terhubung dan menyiapkan dashboard privat di Muse,
mengikuti tabel, filter dan grafik **channel-stats**. Dashboard disimpan di
**Library** agar mudah dibuka lagi, dengan kartu UI di main chat. Side chat khusus
bisa digunakan bila diminta pengguna.
Memakai koneksi instance yang ada; tidak perlu mengulang setup
GCP atau menyalakan Mac untuk executor VM yang sudah terhubung.
Lihat [instruksi skill](skills/ytfusion-channel-analytics/SKILL.md).

```text
Pasang skill skills/ytfusion-channel-analytics dari repo ini dan verifikasi
discovery. Pakai skill itu untuk membuat dashboard privat Analytics channel
yang ditugaskan pada instance ini, mirip UI channel-stats. Simpan di Library
dan tampilkan kartu UI-nya di main chat agar mudah kubuka lagi. Pakai data nyata dan
koneksi yang ada, tunjukkan periode/cakupan dan waktu update, serta uji refresh.
Jangan mempublikasikan datanya atau membuat jadwal berulang.
```

Skill mencakup views, watch time, subscriber dan pendapatan yang memang dapat
diakses. Statistik total, data harian, data realtime dan angka yang belum tersedia
dibedakan. Ini panduan membangun dashboard dengan kemampuan host; memasang skill
saja belum berarti artifact dan refresh API-nya sudah berjalan.

## Mulai di Muse

Copas perintah berikut ke Muse baru. Ganti tugas awal bila instance ditujukan
untuk Regular/Live. Akun, project, channel, sumber dan jadwal ditentukan dari
penugasan instance itu; tidak ada data pilot yang perlu disalin.

```text
Siapkan instance Muse ini untuk workflow YtFusion.

Ambil atau gunakan checkout https://github.com/kisanakclub/ytfusion-skills.
Baca skills/ytfusion-operations/SKILL.md, references/muse-onboarding.md,
dan references/setup.md. Pasang/daftarkan skill lewat mekanisme host yang
tersedia, verifikasi ditemukan, dan simpan referensi versi terpasangnya.
Ambil atau gunakan source https://github.com/kisanakclub/Yt_FusionX dan baca
AGENTS.md. Pilih cara eksekusi dari kemampuan nyata host; pelajari logic
workflow dan pasang dependency yang diperlukan, tanpa mewajibkan server
aplikasi atau seluruh provider HDS untuk tugas upload final.

Tugas awal: siapkan upload video final dari Google Drive ke YouTube, tanpa
generate/render HDS. Selesaikan setup yang diizinkan; upload pertama menunggu
penugasan video/channel dan izin upload. Buat project GCP baru untuk instance
baru kecuali aku menunjuk project yang sudah ada. Pelihara profil privat agar
akun/project/channel dan keputusan tidak perlu dijelaskan ulang.

Riset dan kerjakan solusi yang didukung dengan sedikit langkah manual dan
login tambahan. Tanyakan hanya data/persetujuan yang memang masih diperlukan.
Bila perlu project sendiri, siapkan API Data/Analytics/Drive sesuai tugas,
branding publik (utamakan Firebase Hosting Spark untuk situs baru), status
In production dan client sesuai jalur login yang valid.
Simpan credential lewat jalur privat; jangan minta password/token/kode di chat.

Sebelum upload, ikuti references/upload-workflow.md: metadata dan default
aplikasi, AI/audience/category, thumbnail, playlist, lalu verifikasi hasil,
receipt/penanda pernah upload di Drive dan cleanup. Setelan awal yang kuinginkan
untuk job nanti: satu upload bersamaan, hapus hanya salinan staging milik job
di VM setelah hasil serta riwayat Drive tercatat dan terverifikasi; simpan
video asli, metadata dan thumbnail di Drive. Pertahankan pilihan eksplisit yang
sudah ada dan minta penjelasan bila bertentangan. Jangan menghapus file sekarang.

Lanjutkan langkah yang sudah diizinkan sampai selesai atau blocker nyata.
Ikuti aturan host untuk terms, credential/grant baru dan tindakan sensitif.
Jangan aktifkan billing, mulai publikasi/Live atau membuat jadwal berulang
sebelum ditugaskan. Pilih pendekatan sendiri; jangan berhenti pada rencana
atau mengunci satu provider. Laporkan hasil yang benar-benar terbukti dan
hal yang masih perlu tindakan pengguna.
```

Repo aplikasi Private memerlukan akses GitHub yang sesuai; skill tidak memberikan
akses akun atau repo tersebut. Login/2FA dilakukan melalui UI yang didukung.
Untuk instance yang sudah disiapkan cukup beri tugas, misalnya:

```text
Lanjutkan sesuai profil instance ini. Ambil paket yang kutugaskan dari Drive,
upload ke channel tujuan sebagai Private tanpa jadwal, dan selesaikan seluruh
workflow termasuk riwayat Drive serta cleanup lokal yang sudah disepakati.
```

Untuk penugasan lain:

```text
Instance ini khusus Live tanpa API dari video final di Drive. Gunakan profil
yang sudah ada, baca referensi Live, dan siapkan sumber/encoder. Jangan mulai
siaran sebelum kutugaskan. Tanyakan hanya informasi yang belum tersedia.
```

Menyalin skill bukan pelatihan model dan clone saja tidak mengaktifkan discovery.
Gunakan dukungan skill/memori host, simpan assignment privat, serta verifikasi
hasil pada instance yang sebenarnya. Pemasangan seluruh aplikasi, Regular Studio,
render dan Live belum dibuktikan hanya oleh pilot upload.

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

    Gunakan skill-installer untuk memasang skill dari
    https://github.com/kisanakclub/ytfusion-skills/tree/main/skills/ytfusion-channel-analytics

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
