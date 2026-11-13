import { useState } from "react";
import { Navigate, useLocation, useNavigate } from "react-router-dom";

import { useAuth } from "../auth/AuthContext";

const inputClass =
  "mt-1 w-full rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm text-slate-900 shadow-sm outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100";

export default function LoginPage() {
  const { isAuthenticated, login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  if (isAuthenticated) {
    return <Navigate to="/" replace />;
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setError("");

    if (!username.trim() || !password) {
      setError("Username dan password wajib diisi.");
      return;
    }

    setSubmitting(true);
    try {
      await login(username.trim(), password);
      const destination = location.state?.from || "/";
      navigate(destination, { replace: true });
    } catch (requestError) {
      setError(requestError.message || "Login gagal. Silakan coba lagi.");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <main className="flex min-h-screen items-center justify-center bg-slate-100 px-4 py-10">
      <div className="grid w-full max-w-4xl overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm md:grid-cols-2">
        <section className="bg-indigo-700 p-8 text-white sm:p-10">
          <p className="text-sm font-semibold uppercase tracking-widest text-indigo-200">
            Sales Visit Tracker
          </p>
          <h1 className="mt-3 text-3xl font-semibold">Visit Flow</h1>
          <p className="mt-4 text-sm leading-6 text-indigo-100">
            Catat rencana kunjungan, pantau status, dan lihat riwayat kunjungan
            tim sales dalam satu tempat.
          </p>
          <div className="mt-8 rounded-lg bg-indigo-600/60 p-4 text-sm text-indigo-50">
            <p className="font-medium">Akun demo</p>
            <p className="mt-1">
              sales1 / sales2 / sales3
              <br />
              Password: <span className="font-mono">password123</span>
            </p>
          </div>
        </section>

        <section className="p-8 sm:p-10">
          <h2 className="text-xl font-semibold text-slate-900">Masuk</h2>
          <p className="mt-1 text-sm text-slate-500">
            Gunakan akun sales untuk melanjutkan.
          </p>

          <form className="mt-6 space-y-4" onSubmit={handleSubmit}>
            <div>
              <label
                htmlFor="username"
                className="text-sm font-medium text-slate-700"
              >
                Username
              </label>
              <input
                id="username"
                name="username"
                type="text"
                autoComplete="username"
                value={username}
                onChange={(event) => setUsername(event.target.value)}
                className={inputClass}
                placeholder="sales1"
              />
            </div>

            <div>
              <label
                htmlFor="password"
                className="text-sm font-medium text-slate-700"
              >
                Password
              </label>
              <input
                id="password"
                name="password"
                type="password"
                autoComplete="current-password"
                value={password}
                onChange={(event) => setPassword(event.target.value)}
                className={inputClass}
                placeholder="••••••••"
              />
            </div>

            {error && (
              <p
                role="alert"
                className="rounded-lg border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700"
              >
                {error}
              </p>
            )}

            <button
              type="submit"
              disabled={submitting}
              className="w-full rounded-lg bg-indigo-600 px-4 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-indigo-700 disabled:cursor-not-allowed disabled:opacity-60"
            >
              {submitting ? "Memproses..." : "Masuk"}
            </button>
          </form>
        </section>
      </div>
    </main>
  );
}
