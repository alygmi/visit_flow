import { SegmentBadge, StatusBadge } from "./Badges";

function formatDate(value) {
  if (!value) return "-";
  const [year, month, day] = value.split("-").map(Number);
  const months = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "Mei",
    "Jun",
    "Jul",
    "Agu",
    "Sep",
    "Okt",
    "Nov",
    "Des",
  ];
  if (!year || !month || !day) return value;
  return `${String(day).padStart(2, "0")} ${months[month - 1]} ${year}`;
}

export default function ActivityTable({
  items,
  onToggleStatus,
  pendingId,
}) {
  return (
    <div className="overflow-hidden rounded-xl border border-slate-200 bg-white shadow-sm">
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-slate-200">
          <thead className="bg-slate-50">
            <tr>
              <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wide text-slate-500">
                Entitas
              </th>
              <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wide text-slate-500">
                Segmen
              </th>
              <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wide text-slate-500">
                Wilayah
              </th>
              <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wide text-slate-500">
                Tanggal Kunjungan
              </th>
              <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wide text-slate-500">
                Status
              </th>
              <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wide text-slate-500">
                Sales
              </th>
              <th className="px-4 py-3 text-right text-xs font-semibold uppercase tracking-wide text-slate-500">
                Aksi
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {items.map((item) => {
              const pending = pendingId === item.id;
              const nextLabel =
                item.status === "VISITED"
                  ? "Tandai Not Visited"
                  : "Tandai Visited";

              return (
                <tr key={item.id} className="align-top hover:bg-slate-50/70">
                  <td className="whitespace-nowrap px-4 py-4">
                    <p className="text-sm font-medium text-slate-900">
                      {item.entityName}
                    </p>
                    <p className="mt-0.5 text-xs text-slate-500">
                      {item.entityType}
                    </p>
                  </td>
                  <td className="whitespace-nowrap px-4 py-4">
                    <SegmentBadge segment={item.segment} />
                  </td>
                  <td className="whitespace-nowrap px-4 py-4 text-sm text-slate-600">
                    {item.region}
                  </td>
                  <td className="whitespace-nowrap px-4 py-4 text-sm text-slate-600">
                    {formatDate(item.visitDate)}
                  </td>
                  <td className="whitespace-nowrap px-4 py-4">
                    <StatusBadge status={item.status} />
                  </td>
                  <td className="whitespace-nowrap px-4 py-4 text-sm text-slate-600">
                    {item.salesName}
                  </td>
                  <td className="whitespace-nowrap px-4 py-4 text-right">
                    {item.canEdit ? (
                      <button
                        type="button"
                        onClick={() => onToggleStatus(item)}
                        disabled={pending}
                        className="rounded-lg border border-slate-300 bg-white px-3 py-1.5 text-xs font-semibold text-slate-700 shadow-sm hover:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-60"
                      >
                        {pending ? "Menyimpan..." : nextLabel}
                      </button>
                    ) : (
                      <span
                        className="text-xs text-slate-400"
                        title="Hanya pemilik kunjungan yang dapat mengubah status"
                      >
                        —
                      </span>
                    )}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
