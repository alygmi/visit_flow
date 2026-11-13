const TABLE_HEADERS = [
  "Entitas",
  "Segmen",
  "Wilayah",
  "Tanggal Kunjungan",
  "Status",
  "Sales",
  "Aksi",
];

const SKELETON_CELLS = [
  { width: "w-40", height: "h-4", subWidth: "w-20" },
  { width: "w-12", height: "h-5", pill: true },
  { width: "w-20", height: "h-4" },
  { width: "w-24", height: "h-4" },
  { width: "w-16", height: "h-5", pill: true },
  { width: "w-24", height: "h-4" },
  { width: "w-20", height: "h-4" },
];

export function TableSkeleton({ rows = 6 }) {
  return (
    <div
      role="status"
      aria-live="polite"
      className="overflow-hidden rounded-xl border border-slate-200 bg-white shadow-sm"
    >
      <span className="sr-only">Memuat data kunjungan...</span>
      <div className="overflow-x-auto">
        <table
          className="min-w-full divide-y divide-slate-200"
          aria-hidden="true"
        >
          <thead className="bg-slate-50">
            <tr>
              {TABLE_HEADERS.map((header, index) => (
                <th
                  key={header}
                  scope="col"
                  className={`px-4 py-3 text-xs font-semibold uppercase tracking-wide text-slate-500 ${
                    index === TABLE_HEADERS.length - 1
                      ? "text-right"
                      : "text-left"
                  }`}
                >
                  {header}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {Array.from({ length: rows }, (_, rowIndex) => (
              <tr key={rowIndex} className="animate-pulse">
                {SKELETON_CELLS.map((cell, cellIndex) => (
                  <td
                    key={cellIndex}
                    className={`px-4 py-4 ${
                      cellIndex === SKELETON_CELLS.length - 1
                        ? "text-right"
                        : ""
                    }`}
                  >
                    <div
                      className={`${cell.height} ${cell.width} ${
                        cell.pill ? "rounded-full" : "rounded"
                      } bg-slate-200 ${
                        cellIndex === SKELETON_CELLS.length - 1 ? "ml-auto" : ""
                      }`}
                    />
                    {cell.subWidth && (
                      <div
                        className={`mt-2 h-3 ${cell.subWidth} rounded bg-slate-100`}
                      />
                    )}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export function ErrorState({ message, onRetry }) {
  return (
    <div className="rounded-xl border border-red-200 bg-red-50 px-6 py-10 text-center">
      <h2 className="text-base font-semibold text-red-800">
        Gagal memuat data
      </h2>
      <p className="mt-1 text-sm text-red-700">
        {message || "Terjadi kesalahan yang tidak diketahui."}
      </p>
      <button
        type="button"
        onClick={onRetry}
        className="mt-4 rounded-lg bg-red-600 px-3 py-2 text-sm font-semibold text-white hover:bg-red-700"
      >
        Coba lagi
      </button>
    </div>
  );
}

export function EmptyState() {
  return (
    <div className="px-6 py-16 text-center">
      <p className="text-base font-semibold text-slate-700">
        Tidak ada kunjungan yang cocok dengan filter
      </p>
      <p className="mt-1 text-sm text-slate-500">
        Coba ubah kata kunci, segmen, status, atau rentang tanggal.
      </p>
    </div>
  );
}
