export function LoadingState() {
  return (
    <div className="flex flex-col items-center justify-center gap-3 px-6 py-16 text-sm text-slate-500">
      <span className="h-6 w-6 animate-spin rounded-full border-2 border-slate-200 border-t-indigo-600" />
      Memuat data kunjungan...
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
