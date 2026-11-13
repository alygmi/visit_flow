import { useEffect, useState } from "react";

import { api } from "../api/client";

const inputClass =
  "mt-1 w-full rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm text-slate-900 shadow-sm outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100";

export default function AddActivityModal({
  open,
  defaultSegment = "",
  onClose,
  onCreated,
}) {
  const [segment, setSegment] = useState("");
  const [entityId, setEntityId] = useState("");
  const [visitDate, setVisitDate] = useState("");
  const [entities, setEntities] = useState([]);
  const [entityState, setEntityState] = useState("idle");
  const [entityError, setEntityError] = useState("");
  const [entityReload, setEntityReload] = useState(0);
  const [fieldErrors, setFieldErrors] = useState({});
  const [submitError, setSubmitError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    if (!open) return;
    setSegment(defaultSegment || "");
    setEntityId("");
    setVisitDate("");
    setEntities([]);
    setEntityState(defaultSegment ? "loading" : "idle");
    setEntityError("");
    setFieldErrors({});
    setSubmitError("");
    setSubmitting(false);
  }, [open, defaultSegment]);

  useEffect(() => {
    if (!open || !segment) {
      setEntities([]);
      setEntityState("idle");
      return undefined;
    }

    const controller = new AbortController();
    setEntityState("loading");
    setEntityError("");

    api
      .get(`/entities?segment=${encodeURIComponent(segment)}`, {
        signal: controller.signal,
      })
      .then((result) => {
        setEntities(result.items);
        setEntityState("success");
      })
      .catch((error) => {
        if (error.name === "AbortError") return;
        setEntityError(error.message);
        setEntityState("error");
      });

    return () => controller.abort();
  }, [open, segment, entityReload]);

  if (!open) return null;

  function handleSegmentChange(event) {
    setSegment(event.target.value);
    setEntityId("");
    setFieldErrors((current) => ({ ...current, segment: undefined }));
  }

  function validate() {
    const errors = {};
    if (!segment) errors.segment = "Segmen wajib dipilih.";
    if (!entityId) errors.entityId = "Entitas wajib dipilih.";
    if (!visitDate) errors.visitDate = "Tanggal kunjungan wajib diisi.";
    setFieldErrors(errors);
    return Object.keys(errors).length === 0;
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setSubmitError("");

    if (!validate()) return;

    setSubmitting(true);
    try {
      await api.post("/activities", { entityId, segment, visitDate });
      onCreated();
    } catch (error) {
      setSubmitError(error.message);
      setFieldErrors(error.errors || {});
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div
      className="fixed inset-0 z-50 flex items-end justify-center bg-slate-900/40 p-0 sm:items-center sm:p-4"
      role="presentation"
      onMouseDown={(event) => {
        if (event.target === event.currentTarget && !submitting) onClose();
      }}
    >
      <div
        role="dialog"
        aria-modal="true"
        aria-labelledby="add-activity-title"
        className="max-h-full w-full overflow-y-auto rounded-t-2xl bg-white p-6 shadow-xl sm:max-w-lg sm:rounded-2xl"
      >
        <div className="flex items-start justify-between gap-4">
          <div>
            <h2
              id="add-activity-title"
              className="text-lg font-semibold text-slate-900"
            >
              Tambah Kunjungan
            </h2>
            <p className="mt-1 text-sm text-slate-500">
              Pilih entitas, segmen, dan tanggal kunjungan.
            </p>
          </div>
          <button
            type="button"
            onClick={onClose}
            disabled={submitting}
            className="rounded-lg px-2 py-1 text-sm font-medium text-slate-500 hover:bg-slate-100 disabled:opacity-50"
            aria-label="Tutup"
          >
            ✕
          </button>
        </div>

        <form className="mt-6 space-y-4" onSubmit={handleSubmit} noValidate>
          <div>
            <label
              htmlFor="activity-segment"
              className="text-sm font-medium text-slate-700"
            >
              Segmen <span className="text-red-600">*</span>
            </label>
            <select
              id="activity-segment"
              value={segment}
              onChange={handleSegmentChange}
              className={inputClass}
            >
              <option value="">Pilih segmen</option>
              <option value="B2G">B2G</option>
              <option value="B2B">B2B</option>
            </select>
            {fieldErrors.segment && (
              <p className="mt-1 text-xs text-red-600">
                {fieldErrors.segment}
              </p>
            )}
          </div>

          <div>
            <label
              htmlFor="activity-entity"
              className="text-sm font-medium text-slate-700"
            >
              Entitas <span className="text-red-600">*</span>
            </label>
            <select
              id="activity-entity"
              value={entityId}
              onChange={(event) => {
                setEntityId(event.target.value);
                setFieldErrors((current) => ({
                  ...current,
                  entityId: undefined,
                }));
              }}
              disabled={!segment || entityState === "loading"}
              className={`${inputClass} disabled:cursor-not-allowed disabled:bg-slate-50 disabled:text-slate-400`}
            >
              <option value="">
                {!segment
                  ? "Pilih segmen terlebih dahulu"
                  : entityState === "loading"
                    ? "Memuat entitas..."
                    : "Pilih entitas"}
              </option>
              {entities.map((entity) => (
                <option key={entity.id} value={entity.id}>
                  {entity.label} — {entity.region}
                </option>
              ))}
            </select>
            {fieldErrors.entityId && (
              <p className="mt-1 text-xs text-red-600">
                {fieldErrors.entityId}
              </p>
            )}
            {segment && entityState === "success" && entities.length === 0 && (
              <p className="mt-1 text-xs text-slate-500">
                Tidak ada entitas untuk segmen ini.
              </p>
            )}
            {entityState === "error" && (
              <div className="mt-1 flex items-center gap-2 text-xs text-red-600">
                <span>{entityError}</span>
                <button
                  type="button"
                  onClick={() => setEntityReload((value) => value + 1)}
                  className="font-semibold underline"
                >
                  Coba lagi
                </button>
              </div>
            )}
          </div>

          <div>
            <label
              htmlFor="activity-date"
              className="text-sm font-medium text-slate-700"
            >
              Tanggal kunjungan <span className="text-red-600">*</span>
            </label>
            <input
              id="activity-date"
              type="date"
              value={visitDate}
              onChange={(event) => {
                setVisitDate(event.target.value);
                setFieldErrors((current) => ({
                  ...current,
                  visitDate: undefined,
                }));
              }}
              className={inputClass}
            />
            {fieldErrors.visitDate && (
              <p className="mt-1 text-xs text-red-600">
                {fieldErrors.visitDate}
              </p>
            )}
          </div>

          {submitError && (
            <p
              role="alert"
              className="rounded-lg border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700"
            >
              {submitError}
            </p>
          )}

          <div className="flex justify-end gap-2 pt-2">
            <button
              type="button"
              onClick={onClose}
              disabled={submitting}
              className="rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50 disabled:opacity-50"
            >
              Batal
            </button>
            <button
              type="submit"
              disabled={submitting || entityState === "loading"}
              className="rounded-lg bg-indigo-600 px-4 py-2 text-sm font-semibold text-white hover:bg-indigo-700 disabled:cursor-not-allowed disabled:opacity-60"
            >
              {submitting ? "Menyimpan..." : "Simpan Kunjungan"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
