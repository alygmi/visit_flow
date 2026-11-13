const cards = [
  {
    key: "total",
    label: "Total",
    accent: "bg-slate-100 text-slate-700",
  },
  {
    key: "visited",
    label: "Visited",
    accent: "bg-emerald-50 text-emerald-700",
  },
  {
    key: "notVisited",
    label: "Not Visited",
    accent: "bg-amber-50 text-amber-700",
  },
];

export default function SummaryCards({ summary, loading }) {
  return (
    <section className="mt-6 grid gap-4 sm:grid-cols-3">
      {cards.map((card) => (
        <div
          key={card.key}
          className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm"
        >
          <div className="flex items-center justify-between gap-3">
            <p className="text-sm font-medium text-slate-500">{card.label}</p>
            <span
              className={`inline-flex h-8 w-8 items-center justify-center rounded-full text-xs font-semibold ${card.accent}`}
            >
              #
            </span>
          </div>
          <p className="mt-3 text-3xl font-semibold text-slate-900">
            {loading || !summary ? "—" : summary[card.key]}
          </p>
          <p className="mt-1 text-xs text-slate-400">kunjungan</p>
        </div>
      ))}
    </section>
  );
}
