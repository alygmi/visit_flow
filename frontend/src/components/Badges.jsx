const statusStyles = {
  VISITED: "bg-emerald-50 text-emerald-700 ring-emerald-600/20",
  NOT_VISITED: "bg-amber-50 text-amber-700 ring-amber-600/20",
};

const statusLabels = {
  VISITED: "Visited",
  NOT_VISITED: "Not Visited",
};

const segmentStyles = {
  B2G: "bg-blue-50 text-blue-700 ring-blue-600/20",
  B2B: "bg-violet-50 text-violet-700 ring-violet-600/20",
};

export function StatusBadge({ status }) {
  return (
    <span
      className={`inline-flex items-center rounded-full px-2.5 py-1 text-xs font-medium ring-1 ring-inset ${
        statusStyles[status] || "bg-slate-50 text-slate-700 ring-slate-600/20"
      }`}
    >
      {statusLabels[status] || status}
    </span>
  );
}

export function SegmentBadge({ segment }) {
  return (
    <span
      className={`inline-flex items-center rounded-full px-2.5 py-1 text-xs font-medium ring-1 ring-inset ${
        segmentStyles[segment] || "bg-slate-50 text-slate-700 ring-slate-600/20"
      }`}
    >
      {segment}
    </span>
  );
}
