import { useEffect, useState } from "react";

import { api } from "../api/client";
import { useAuth } from "../auth/AuthContext";
import ActivityTable from "../components/ActivityTable";
import AddActivityModal from "../components/AddActivityModal";
import FilterBar from "../components/FilterBar";
import { EmptyState, ErrorState, TableSkeleton } from "../components/States";
import SummaryCards from "../components/SummaryCards";

const INITIAL_FILTERS = {
  search: "",
  segment: "",
  status: "",
  from: "",
  to: "",
};

const EMPTY_SUMMARY = { total: 0, visited: 0, notVisited: 0 };

export default function VisitFlowPage() {
  const { user, logout } = useAuth();
  const [filters, setFilters] = useState(INITIAL_FILTERS);
  const [debouncedSearch, setDebouncedSearch] = useState("");
  const [data, setData] = useState({ items: [], summary: EMPTY_SUMMARY });
  const [loadState, setLoadState] = useState("loading");
  const [errorMessage, setErrorMessage] = useState("");
  const [reloadToken, setReloadToken] = useState(0);
  const [isModalOpen, setModalOpen] = useState(false);
  const [pendingId, setPendingId] = useState(null);
  const [actionError, setActionError] = useState("");

  useEffect(() => {
    const timer = window.setTimeout(
      () => setDebouncedSearch(filters.search.trim()),
      350,
    );
    return () => window.clearTimeout(timer);
  }, [filters.search]);

  useEffect(() => {
    const controller = new AbortController();

    async function loadActivities() {
      setLoadState("loading");
      setErrorMessage("");

      const params = new URLSearchParams();
      if (debouncedSearch) params.set("search", debouncedSearch);
      if (filters.segment) params.set("segment", filters.segment);
      if (filters.status) params.set("status", filters.status);
      if (filters.from) params.set("from", filters.from);
      if (filters.to) params.set("to", filters.to);
      const query = params.toString();

      try {
        const result = await api.get(
          `/activities${query ? `?${query}` : ""}`,
          { signal: controller.signal },
        );
        setData(result);
        setLoadState("success");
      } catch (error) {
        if (error.name === "AbortError") return;
        setErrorMessage(error.message);
        setLoadState("error");
      }
    }

    loadActivities();
    return () => controller.abort();
  }, [
    debouncedSearch,
    filters.segment,
    filters.status,
    filters.from,
    filters.to,
    reloadToken,
  ]);

  function updateFilter(name, value) {
    setFilters((current) => ({ ...current, [name]: value }));
    setActionError("");
  }

  function resetFilters() {
    setFilters(INITIAL_FILTERS);
    setDebouncedSearch("");
    setActionError("");
  }

  function refresh() {
    setActionError("");
    setReloadToken((token) => token + 1);
  }

  async function handleToggleStatus(item) {
    setActionError("");
    setPendingId(item.id);
    const nextStatus =
      item.status === "VISITED" ? "NOT_VISITED" : "VISITED";

    try {
      await api.patch(`/activities/${item.id}`, { status: nextStatus });
      refresh();
    } catch (error) {
      setActionError(error.message);
    } finally {
      setPendingId(null);
    }
  }

  function handleCreated() {
    setModalOpen(false);
    refresh();
  }

  const loading = loadState === "loading";

  return (
    <div className="min-h-screen">
      <header className="border-b border-slate-200 bg-white">
        <div className="mx-auto flex max-w-7xl items-center justify-between gap-4 px-4 py-4 sm:px-6">
          <div className="flex items-center gap-3">
            <span className="flex h-9 w-9 items-center justify-center rounded-lg bg-indigo-600 text-sm font-bold text-white">
              VF
            </span>
            <div>
              <p className="text-sm font-semibold text-slate-900">Visit Flow</p>
              <p className="text-xs text-slate-500">Sales visit tracker</p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <div className="hidden text-right sm:block">
              <p className="text-sm font-medium text-slate-800">{user?.name}</p>
              <p className="text-xs text-slate-500">Sales</p>
            </div>
            <button
              type="button"
              onClick={logout}
              className="rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50"
            >
              Keluar
            </button>
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6">
        <div className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
          <div>
            <h1 className="text-2xl font-semibold text-slate-900">
              Daftar Kunjungan
            </h1>
            <p className="mt-1 text-sm text-slate-500">
              Pantau rencana dan hasil kunjungan tim sales ke entitas.
            </p>
          </div>
          <button
            type="button"
            onClick={() => setModalOpen(true)}
            className="inline-flex items-center justify-center rounded-lg bg-indigo-600 px-4 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-indigo-700"
          >
            + Tambah Kunjungan
          </button>
        </div>

        <SummaryCards summary={data.summary} loading={loading} />

        <FilterBar
          filters={filters}
          onChange={updateFilter}
          onReset={resetFilters}
        />

        {actionError && (
          <p
            role="alert"
            className="mt-4 rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700"
          >
            {actionError}
          </p>
        )}

        <section className="mt-6" aria-live="polite" aria-busy={loading}>
          {loadState === "error" ? (
            <ErrorState message={errorMessage} onRetry={refresh} />
          ) : loading ? (
            <TableSkeleton />
          ) : data.items.length === 0 ? (
            <div className="rounded-xl border border-slate-200 bg-white shadow-sm">
              <EmptyState />
            </div>
          ) : (
            <ActivityTable
              items={data.items}
              onToggleStatus={handleToggleStatus}
              pendingId={pendingId}
            />
          )}
        </section>
      </main>

      <AddActivityModal
        open={isModalOpen}
        defaultSegment={filters.segment}
        onClose={() => setModalOpen(false)}
        onCreated={handleCreated}
      />
    </div>
  );
}
