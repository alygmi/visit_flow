# Visit Flow

Prototype aplikasi manajemen kunjungan sales: daftar kunjungan dengan filter, ringkasan status, pencarian entitas, tambah kunjungan, dan perubahan status khusus pemilik kunjungan.

Aplikasi terdiri dari backend FastAPI + PostgreSQL dan frontend React (Vite + Tailwind). Semua data, nama, dan kredensial di repo ini fiktif dan hanya untuk demo.

## Stack dan alasan

| Bagian | Teknologi | Alasan |
| --- | --- | --- |
| Backend | Python 3.12, FastAPI | Ringkas, validasi Pydantic bawaan, dokumentasi OpenAPI otomatis. |
| Database | PostgreSQL 16, SQLAlchemy 2.x, Alembic | Filter dan pencarian dikerjakan di SQL; migrasi eksplisit dan reproducible. |
| Auth | JWT (PyJWT), passlib + bcrypt | Stateless, cukup untuk prototype; password tidak disimpan plaintext. |
| Validasi | Pydantic v2 | Schema request/response dan pesan validasi yang konsisten. |
| Frontend | React 18, Vite, Tailwind CSS, React Router | Build cepat, styling tanpa library berat, rute login/protected sederhana. |
| Data fetching | `fetch` wrapper tipis | Tanpa state library tambahan; cukup untuk satu halaman utama. |
| Tes | pytest, httpx/TestClient | Tes API end-to-end terhadap database PostgreSQL terpisah. |

## Struktur repo

```text
visit_flow/
├── backend/
│   ├── alembic/                 # konfigurasi dan migrasi
│   ├── app/
│   │   ├── routers/             # auth, entities, activities
│   │   ├── config.py            # pembacaan environment
│   │   ├── models.py            # User, Entity, Activity
│   │   ├── schemas.py           # schema Pydantic
│   │   ├── seed.py              # data demo idempotent
│   │   └── main.py              # aplikasi FastAPI
│   ├── tests/                   # 25 tes API
│   └── requirements.txt
├── db/init/                     # pembuatan database tes saat container pertama kali dibuat
├── frontend/
│   └── src/                     # halaman login, tabel kunjungan, komponen
├── docker-compose.yml           # PostgreSQL 16
├── .env.example
├── AI_USAGE.md
└── README.md
```

## Prasyarat

- Docker dan Docker Compose
- Python 3.12
- Node.js 20+ dan npm

## Menjalankan aplikasi

### 1. Siapkan environment

Dari root repo:

```bash
cp .env.example .env
```

Di Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Nilai di `.env.example` adalah nilai pengembangan, bukan kredensial nyata. Ganti `JWT_SECRET` bila aplikasi dipakai di luar lingkungan lokal.

### 2. Jalankan database

```bash
docker compose up -d
```

Compose menjalankan PostgreSQL 16 pada port host **5433** (agar tidak bentrok dengan PostgreSQL lokal di 5432). Script `db/init/01-create-test-db.sh` membuat database terpisah `visitflow_test` saat container pertama kali dibuat.

Cek status:

```bash
docker compose ps
```

### 3. Jalankan backend

```bash
cd backend
python -m venv .venv
```

Aktifkan virtual environment:

```bash
# Linux/macOS
source .venv/bin/activate

# Windows PowerShell
.\.venv\Scripts\Activate.ps1
```

Install dependensi, jalankan migrasi, lalu seed data demo:

```bash
pip install -r requirements.txt
alembic upgrade head
python -m app.seed
uvicorn app.main:app --reload --port 8000
```

- API: <http://localhost:8000>
- Dokumentasi OpenAPI: <http://localhost:8000/docs>
- Health check: <http://localhost:8000/health>

Seed bersifat idempotent: aman dijalankan ulang dan tidak menduplikasi data.

### 4. Jalankan frontend

Di terminal lain:

```bash
cd frontend
npm install
npm run dev
```

Buka <http://localhost:5173>. Vite mem-proxy `/api` ke `http://localhost:8000`.

### Akun demo

| Username | Password | Nama |
| --- | --- | --- |
| `sales1` | `password123` | Adit Pratama |
| `sales2` | `password123` | Rina Kurnia |
| `sales3` | `password123` | Bayu Santoso |

Semua akun dapat melihat seluruh kunjungan, tetapi hanya dapat mengubah status kunjungan miliknya sendiri.

## Ringkasan API

Semua endpoint data (selain login dan health check) memerlukan header `Authorization: Bearer <token>`.

| Method | Endpoint | Keterangan |
| --- | --- | --- |
| `POST` | `/api/auth/login` | Login, mengembalikan token dan data user. |
| `GET` | `/api/entities` | Opsi entitas, filter `segment` dan `search`. |
| `GET` | `/api/activities` | Daftar kunjungan + ringkasan, filter `segment`, `status`, `from`, `to`, `search`. |
| `POST` | `/api/activities` | Tambah kunjungan baru; `salesId` selalu diambil dari token. |
| `PATCH` | `/api/activities/{id}` | Ubah status; hanya pemilik kunjungan (403 untuk lainnya). |
| `GET` | `/health` | Health check. |

Catatan filter:

- `from` dan `to` inklusif terhadap tanggal batas.
- `search` memakai `ILIKE` pada nama entitas.
- `from` setelah `to` menghasilkan `400`.
- Ringkasan (`total`, `visited`, `notVisited`) dihitung dari hasil filter yang sama dengan daftar item.

Format error konsisten:

```json
{
  "message": "Data yang dikirim tidak valid.",
  "errors": { "visitDate": "Wajib diisi." }
}
```

## Aturan bisnis yang diterapkan

- Login JWT; seluruh endpoint data menolak request tanpa token yang valid.
- Identitas sales untuk kunjungan baru diambil dari token, bukan dari body.
- Status awal kunjungan baru adalah `NOT_VISITED`.
- PATCH status hanya boleh dilakukan pemilik kunjungan; UI hanya menampilkan tombol untuk item dengan `canEdit: true`.
- Filter segmen, status, rentang tanggal, dan pencarian dijalankan di query SQL, bukan difilter di browser.
- Tanggal `from`/`to` inklusif.
- Pencarian nama memakai `ILIKE` (case-insensitive, partial match).
- Ringkasan selalu konsisten dengan item yang dikembalikan.
- Entitas master dan riwayat:
  - Entitas master disimpan di tabel `entities`.
  - Setiap kunjungan menyimpan snapshot nama, tipe, dan wilayah agar riwayat tetap terbaca bila master berubah.
  - Bila pencarian/filter tidak menemukan entitas master, API menyusun opsi dari snapshot riwayat yang unik.
  - Opsi riwayat memakai ID sintetis stabil `hist:<nama>-<tipe>-<wilayah>-<segmen>` dan dapat dipakai untuk membuat kunjungan baru.
  - Label opsi selalu menyertakan tipe, misalnya `Cempaka (Instansi)`, sehingga nama sama dengan tipe berbeda tetap dapat dibedakan.
- Data seed mencakup batas tanggal `2026-03-01` dan `2026-03-31`, campuran segmen/status, serta kunjungan lama tanpa entitas master untuk mendemokan fallback riwayat.

## Tes

Pastikan PostgreSQL berjalan dan database `visitflow_test` tersedia (dibuat otomatis oleh compose). Lalu dari direktori `backend`:

```bash
# Linux/macOS
.venv/bin/python -m pytest

# Windows PowerShell
.\.venv\Scripts\python.exe -m pytest
```

Hasil saat ini: **25 passed**. Cakupan tes:

- login sukses/gagal, token wajib, token tidak valid;
- penolakan `salesId` dari body;
- filter tanggal inklusif, kombinasi filter, dan validasi `from > to`;
- validasi POST (field wajib, tanggal tidak valid, segmen tidak valid, entitas tidak dikenal, segmen tidak cocok);
- identitas sales dari token;
- PATCH oleh pemilik vs non-pemilik, 404, dan status tidak valid;
- ringkasan konsisten dan hasil kosong;
- `canEdit` hanya `true` untuk pemilik;
- opsi entitas master, label tipe, deduplikasi, filter segmen;
- fallback riwayat hanya saat hasil master kosong, termasuk pembuatan kunjungan dari ID `hist:`.

Build frontend:

```bash
cd frontend
npm run build
```

## Keputusan desain

- **Snapshot pada aktivitas.** Nama, tipe, dan wilayah entitas disalin ke setiap kunjungan. Ini menjaga data historis tetap utuh dan membuat fallback riwayat memungkinkan tanpa tabel histori terpisah.
- **ID aktivitas dibuat aplikasi** (`act-<uuid4hex>`) agar tidak bergantung pada sequence database dan aman dipakai di URL.
- **Filter di SQL.** Semua filter dan pencarian dijalankan sebelum data diambil sehingga ringkasan dan daftar selalu berasal dari kumpulan data yang sama.
- **Fallback riwayat berbasis pencarian.** Master tetap menjadi sumber utama; snapshot riwayat hanya muncul bila hasil master untuk filter tersebut kosong, sehingga opsi master dan riwayat tidak tercampur.
- **Error dalam bahasa Indonesia** dengan bentuk `{message, errors}` agar frontend dapat menampilkan pesan per field.
- **Tanpa pagination.** Belum diminta pada spesifikasi; volume data prototype masih kecil.
- **Token di `localStorage`.** Sederhana untuk prototype; frontend memeriksa masa berlaku token dan logout otomatis saat menerima `401`. Tidak ada data kunjungan yang disimpan di browser; `localStorage` hanya menyimpan sesi, sedangkan seluruh data kunjungan dan entitas berasal dari API/PostgreSQL.

## Keterbatasan

- Belum ada registrasi, manajemen user, atau role selain aturan kepemilikan kunjungan.
- Belum ada CRUD entitas master; entitas hanya berasal dari seed dan snapshot riwayat.
- Belum ada pagination, sorting kolom, atau ekspor.
- `npm audit` melaporkan 2 kerentanan moderate pada `react-router`/`react-router-dom` 6.x. Perbaikan memerlukan upgrade breaking ke react-router-dom 7 dan belum diterapkan agar perubahan tetap sesuai spesifikasi.
- Token disimpan di `localStorage`; untuk produksi perlu pertimbangan cookie `HttpOnly`, rotasi token, dan hardening tambahan.
- Lingkungan pengembangan saat pengerjaan tidak mendukung Docker (WSL2/Hyper-V tidak tersedia), sehingga verifikasi lokal memakai PostgreSQL 18 pada port 5433. `docker-compose.yml` tetap menjadi cara menjalankan database sesuai spesifikasi dan memakai PostgreSQL 16.

## Reset data demo

Untuk mengembalikan data ke kondisi seed:

```bash
docker compose down -v
docker compose up -d
cd backend
alembic upgrade head
python -m app.seed
```

Perintah di atas menghapus volume database. Alternatif tanpa menghapus volume: kosongkan tabel `activities` lalu jalankan ulang seed.

## Penggunaan AI

Seluruh kode dan dokumentasi prototype ini dibuat dengan bantuan AI: **100% berdasarkan 17 entri log (17 dibuat AI, 0 manual)**. Belum ada perubahan manual yang tercatat.

| Area | File/fungsi yang menggunakan AI |
| --- | --- |
| Setup | `docker-compose.yml`, `db/init/01-create-test-db.sh`, `.env.example`, `.gitignore` |
| Konfigurasi & database | `backend/app/config.py`, `database.py`, `models.py` (`User`, `Entity`, `Activity`), `security.py`, migrasi `0001_initial_schema.py` |
| Seed | `backend/app/seed.py` (3 sales, 14 entitas master, 20 kunjungan, 4 kunjungan riwayat) |
| Auth & error | `backend/app/routers/auth.py`, `deps.py` (`get_current_user`), `errors.py`, `schemas.py` |
| API aktivitas | `backend/app/routers/activities.py` (`list_activities`, `create_activity`, `update_activity_status`, `_resolve_entity`) |
| API entitas | `backend/app/routers/entities.py`, `entity_utils.py` (`history_entity_id`, `find_history_snapshot`, `entity_label`) |
| Tes | `backend/tests/conftest.py`, `test_auth.py`, `test_activities.py`, `test_entities.py` (25 tes) |
| Frontend auth | `frontend/src/api/client.js`, `auth/AuthContext.jsx`, `components/ProtectedRoute.jsx`, `pages/LoginPage.jsx` |
| Frontend kunjungan | `pages/VisitFlowPage.jsx`, `components/ActivityTable.jsx`, `FilterBar.jsx`, `SummaryCards.jsx`, `Badges.jsx`, `States.jsx`, `AddActivityModal.jsx` |
| Dokumentasi | `README.md`, `AI_USAGE.md` |

Rincian per tahap dan rekap manual ada di [`AI_USAGE.md`](./AI_USAGE.md).
