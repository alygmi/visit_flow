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
| 4 | 2026-11-13 | `backend/app/routers/entities.py`, `backend/app/entity_utils.py` | Ya | Ya (rekap #1) | Daftar entitas master, fallback snapshot riwayat, ID sintetis `hist:`, label tipe, dan anti-duplikat. |
| 4 | 2026-11-13 | `backend/app/routers/activities.py`, `backend/app/schemas.py` (`ActivityCreate`, `ActivityItem`, `ActivitySummary`) | Ya | Ya (rekap #1, #2) | GET dengan filter SQL + ringkasan, POST dari master/riwayat, PATCH status dengan aturan kepemilikan. |
| 5 | 2026-11-13 | `backend/pytest.ini`, `backend/tests/conftest.py`, `backend/tests/test_auth.py`, `backend/tests/test_activities.py`, `backend/tests/test_entities.py` | Ya | Ya (rekap #2) | 25 tes: auth, filter inklusif/kombinasi, validasi POST, kepemilikan PATCH, fallback entitas, dedup/label, ringkasan. Database test terpisah `visitflow_test`. |
| 6 | 2026-11-13 | `frontend/src/api/client.js`, `frontend/src/auth/AuthContext.jsx`, `frontend/src/components/ProtectedRoute.jsx`, `frontend/src/pages/LoginPage.jsx` | Ya | Belum ada | Fetch wrapper tipis, token di localStorage, proteksi rute, dan logout saat 401/token kedaluwarsa. |
| 6 | 2026-11-13 | `frontend/src/pages/VisitFlowPage.jsx`, `frontend/src/components/FilterBar.jsx`, `SummaryCards.jsx`, `ActivityTable.jsx`, `Badges.jsx`, `States.jsx`, `frontend/src/App.jsx` | Ya | Ya (rekap #2) | Tabel kunjungan, filter server-side dengan debounce, ringkasan, loading/error/empty state. |
| 7 | 2026-11-13 | `frontend/src/components/AddActivityModal.jsx`, `frontend/src/pages/VisitFlowPage.jsx`, `frontend/src/components/ActivityTable.jsx` | Ya | Belum ada | Form tambah kunjungan dengan dropdown entitas per segmen, validasi frontend/backend, tombol status hanya untuk `canEdit`, refresh tabel dan ringkasan dari API. |
| 8 | 2026-11-13 | `README.md` | Ya | Ya (rekap #2) | Dokumentasi cara menjalankan database/backend/frontend, akun demo, ringkasan API, aturan bisnis, tes, keputusan desain, keterbatasan, dan disclosure AI. |
| 8 | 2026-11-13 | `AI_USAGE.md` | Ya | Belum ada | Penambahan catatan tahap 8 dan rekap persentase akhir berdasarkan log. |
| Tambahan | 2026-11-13 | `frontend/src/components/States.jsx` (`TableSkeleton`), `frontend/src/components/SummaryCards.jsx`, `frontend/src/pages/VisitFlowPage.jsx` | Ya | Belum ada | Skeleton loading tabel dan ringkasan saat initial load maupun perubahan filter, dengan `aria-busy` dan teks status untuk screen reader. |
| Tambahan | 2026-11-13 | `README.md`, `AI_USAGE.md` | Ya | Belum ada | Penyesuaian dokumentasi setelah rename filter: catatan keputusan desain `start`/`end`, tabel rekap manual, dan disclosure AI. |

Kolom **Manual** di tabel ini menandai baris yang kemudian diubah manual, dengan rujukan ke nomor di *Rekap manual Adit*. Nilainya bukan tambahan entri: jumlah entri manual dihitung dari tabel rekap di bawah, supaya tidak terhitung dua kali.

## Rekap manual Adit

Bagian ini diisi saat Adit meninjau atau mengubah kode. Nomor `#` dipakai sebagai rujukan dari kolom Manual di tabel per tahap. Jika belum ada perubahan manual, kolom Manual tetap "Belum ada" agar persentase tidak dilebih-lebihkan.

| # | File / fungsi | Perubahan manual | Tanggal |
| --- | --- | --- | --- |
| 1 | `backend/app/routers/activities.py`, `backend/app/routers/entities.py` | Merapikan penulisan query (trailing comma, spasi) tanpa mengubah perilaku; sempat menambahkan query alternatif sebagai komentar lalu menghapusnya. | 2026-11-13 |
| 2 | `backend/app/routers/activities.py` (`alias`, pesan error), `backend/app/errors.py` (`FIELD_LABELS`), `frontend/src/pages/VisitFlowPage.jsx`, `frontend/src/components/FilterBar.jsx`, `backend/tests/test_activities.py`, `README.md` | Mengganti parameter filter `from`/`to` menjadi `start`/`end` secara menyeluruh: query param, state frontend, input tanggal, tes, dan dokumentasi. | 2026-11-13 |

## Rekap akhir

Jumlah entri AI dihitung dari baris ber-AI "Ya" pada catatan per tahap. Jumlah entri manual dihitung dari tabel *Rekap manual Adit*; kolom Manual di tabel per tahap hanya rujukan, bukan entri tambahan.

| Kategori | Jumlah entri | Persentase |
| --- | --- | --- |
| Dibuat/diubah dengan AI | 18 | 90% |
| Ditulis/diubah manual oleh Adit | 2 | 10% |
| **Total** | **20** | **100%** |

Persentase dihitung **per entri perubahan**, bukan per baris kode: 18 entri AI dibanding 2 entri manual. Secara jumlah baris, perubahan manual saat ini sekitar **1%** dari total baris kode, karena rename parameter hanya menyentuh sebagian kecil baris. Dua angka itu ditulis apa adanya supaya tidak melebih-lebihkan: 10% berasal dari metode per entri, bukan klaim porsi baris. Bila Adit mengubah bagian lain, tambahkan barisnya ke tabel rekap manual dan hitung ulang persentase dari total entri yang baru. Jangan mengisi kolom manual tanpa perubahan yang benar-benar dilakukan.
