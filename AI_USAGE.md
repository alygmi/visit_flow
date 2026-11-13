# AI Usage Log

Dokumen ini dicatat sejak awal pengerjaan. Setiap tahap mencatat file/fungsi yang dibuat atau dibantu AI, serta bagian yang ditulis atau diubah manual oleh Adit. Persentase akhir dihitung dari catatan ini, bukan diperkirakan di akhir.

## Legenda

- **AI**: dibuat atau diubah dengan bantuan AI.
- **Manual**: ditulis atau diubah sendiri oleh Adit tanpa AI.

## Catatan per tahap

| Tahap | Tanggal | File / fungsi | AI | Manual | Catatan |
| --- | --- | --- | --- | --- | --- |
| 1 | 2026-11-13 | `docker-compose.yml`, `db/init/01-create-test-db.sh`, `.env.example`, `.gitignore`, `.gitattributes` | Ya | Belum ada | Setup PostgreSQL 16 dan konfigurasi lingkungan. |
| 1 | 2026-11-13 | `backend/requirements.txt`, `backend/app/config.py`, `backend/app/database.py`, `backend/app/main.py` | Ya | Belum ada | Kerangka FastAPI, konfigurasi, dan koneksi database. |
| 1 | 2026-11-13 | `frontend/package.json`, `vite.config.js`, `tailwind.config.js`, `postcss.config.js`, `index.html`, `src/main.jsx`, `src/App.jsx`, `src/index.css` | Ya | Belum ada | Kerangka React + Vite + Tailwind dan proxy `/api`. |
| 2 | 2026-11-13 | `backend/app/models.py` (`User`, `Entity`, `Activity`), `backend/app/security.py` (`hash_password`, `verify_password`) | Ya | Belum ada | Model SQLAlchemy 2.x, snapshot entitas, CHECK constraint segmen/status, dan hashing password. |
| 2 | 2026-11-13 | `backend/alembic.ini`, `backend/alembic/env.py`, `backend/alembic/versions/0001_initial_schema.py` | Ya | Belum ada | Migrasi awal tabel users, entities, activities beserta index dan foreign key. |
| 2 | 2026-11-13 | `backend/app/seed.py` | Ya | Belum ada | Seed idempotent: 3 sales, 14 entitas, 20 kunjungan master, 4 kunjungan riwayat. |
| 3 | 2026-11-13 | `backend/app/security.py` (`create_access_token`, `decode_access_token`), `backend/app/deps.py` (`get_current_user`) | Ya | Belum ada | JWT PyJWT, masa berlaku token, dan dependency identitas dari token. |
| 3 | 2026-11-13 | `backend/app/routers/auth.py`, `backend/app/schemas.py` (`LoginRequest`, `LoginResponse`), `backend/app/errors.py`, `backend/app/main.py` | Ya | Belum ada | Endpoint login, format error `{message, errors}`, dan handler validasi berbahasa Indonesia. |

## Rekap manual Adit

Bagian ini diisi saat Adit meninjau atau mengubah kode. Jika belum ada perubahan manual, kolom Manual tetap "Belum ada" agar persentase tidak dilebih-lebihkan.

| File / fungsi | Perubahan manual | Tanggal |
| --- | --- | --- |
| - | - | - |
