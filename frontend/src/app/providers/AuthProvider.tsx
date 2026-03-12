"use client";

import { createContext, useContext, useState } from "react";

type AuthContextType = {
  isAuthenticated: boolean;
  token: string | null;
  setToken: (token: string | null) => void;
};

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [token, setToken] = useState<string | null>(null);

  return (
    <AuthContext.Provider
      value={{ isAuthenticated: !!token, token, setToken }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuthContext() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuthContext must be used within AuthProvider");
  }
  return context;
}
