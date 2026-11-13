const inputClass =
  "mt-1 w-full rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm text-slate-900 shadow-sm outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100";

export default function FilterBar({ filters, onChange, onReset }) {
  function update(event) {
    onChange(event.target.name, event.target.value);
  }

  return (
    <form
      className="mt-6 rounded-xl border border-slate-200 bg-white p-4 shadow-sm sm:p-5"
      onSubmit={(event) => event.preventDefault()}
    >
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-6">
        <div className="sm:col-span-2">
          <label
            htmlFor="filter-search"
            className="text-sm font-medium text-slate-700"
          >
            Cari entitas
          </label>
          <input
            id="filter-search"
            name="search"
            type="search"
            value={filters.search}
            onChange={update}
            placeholder="Cari nama entitas..."
            className={inputClass}
          />
        </div>

        <div>
          <label
            htmlFor="filter-segment"
            className="text-sm font-medium text-slate-700"
          >
            Segmen
          </label>
          <select
            id="filter-segment"
            name="segment"
            value={filters.segment}
            onChange={update}
            className={inputClass}
          >
            <option value="">Semua segmen</option>
            <option value="B2G">B2G</option>
            <option value="B2B">B2B</option>
          </select>
        </div>

        <div>
          <label
            htmlFor="filter-status"
            className="text-sm font-medium text-slate-700"
          >
            Status
          </label>
          <select
            id="filter-status"
            name="status"
            value={filters.status}
            onChange={update}
            className={inputClass}
          >
            <option value="">Semua status</option>
            <option value="VISITED">Visited</option>
            <option value="NOT_VISITED">Not Visited</option>
          </select>
        </div>

        <div>
          <label
            htmlFor="filter-from"
            className="text-sm font-medium text-slate-700"
          >
            Tanggal mulai
          </label>
          <input
            id="filter-from"
            name="from"
            type="date"
            value={filters.from}
            onChange={update}
            className={inputClass}
          />
        </div>

        <div>
          <label
            htmlFor="filter-to"
            className="text-sm font-medium text-slate-700"
          >
            Tanggal akhir
          </label>
          <input
            id="filter-to"
            name="to"
            type="date"
            value={filters.to}
            onChange={update}
            className={inputClass}
          />
        </div>
      </div>

      <div className="mt-4 flex justify-end">
        <button
          type="button"
          onClick={onReset}
          className="rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm font-medium text-slate-700 shadow-sm hover:bg-slate-50"
        >
          Reset filter
        </button>
      </div>
    </form>
  );
}
