import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useState,
} from "react";

import {
  api,
  getTokenExpiry,
  readSession,
  setUnauthorizedHandler,
  writeSession,
  clearSession,
} from "../api/client";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [session, setSession] = useState(() => readSession());

  const logout = useCallback(() => {
    clearSession();
    setSession(null);
  }, []);

  useEffect(() => {
    setUnauthorizedHandler(logout);
    return () => setUnauthorizedHandler(null);
  }, [logout]);

  useEffect(() => {
    if (!session?.token) return undefined;
    const expiry = getTokenExpiry(session.token);
    if (expiry === null) return undefined;

    const remaining = expiry - Date.now();
    if (remaining <= 0) {
      logout();
      return undefined;
    }

    const timer = window.setTimeout(
      logout,
      Math.min(remaining, 2_147_483_647),
    );
    return () => window.clearTimeout(timer);
  }, [session, logout]);

  const login = useCallback(async (username, password) => {
    const data = await api.post(
      "/auth/login",
      { username, password },
      { auth: false },
    );
    const nextSession = { token: data.token, user: data.user };
    writeSession(nextSession);
    setSession(nextSession);
    return nextSession;
  }, []);

  const value = {
    session,
    user: session?.user || null,
    isAuthenticated: Boolean(session),
    login,
    logout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth harus dipakai di dalam AuthProvider.");
  }
  return context;
}
