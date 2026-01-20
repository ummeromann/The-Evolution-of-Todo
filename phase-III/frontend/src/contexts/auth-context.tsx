"use client";

import { createContext, useContext, useState, useEffect, ReactNode } from "react";
import { AuthUser, clearAccessToken } from "@/lib/api";

/**
 * Auth context state.
 */
interface AuthContextState {
  user: AuthUser | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  setUser: (user: AuthUser | null) => void;
  signout: () => void;
}

const AuthContext = createContext<AuthContextState | undefined>(undefined);

const TOKEN_STORAGE_KEY = "todo_access_token";

/**
 * Checks if a JWT token is expired.
 * @param token - JWT token string
 * @returns true if expired, false otherwise
 */
function isTokenExpired(token: string): boolean {
  try {
    const parts = token.split(".");
    if (parts.length !== 3) return true;
    const payload = JSON.parse(atob(parts[1].replace(/-/g, "+").replace(/_/g, "/")));
    if (!payload.exp) return false;
    return payload.exp < Math.floor(Date.now() / 1000);
  } catch {
    return true;
  }
}

/**
 * Decodes JWT payload to extract user information.
 * @param token - JWT access token
 * @returns User info from token payload or null
 */
function decodeJwtUser(token: string): AuthUser | null {
  try {
    const parts = token.split(".");
    if (parts.length !== 3) return null;

    const payload = JSON.parse(atob(parts[1].replace(/-/g, "+").replace(/_/g, "/")));

    return {
      id: payload.sub,
      email: payload.email,
      created_at: new Date(payload.iat * 1000).toISOString(),
    };
  } catch {
    return null;
  }
}

/**
 * Get initial user from localStorage token (client-side only).
 */
function getInitialUser(): AuthUser | null {
  if (typeof window === "undefined") return null;

  const token = localStorage.getItem(TOKEN_STORAGE_KEY);
  if (!token || isTokenExpired(token)) return null;

  return decodeJwtUser(token);
}

/**
 * Auth provider component.
 * Manages user authentication state across the app.
 */
export function AuthProvider({ children }: { children: ReactNode }) {
  // Initialize with user from localStorage if available (client-side)
  const [user, setUser] = useState<AuthUser | null>(() => getInitialUser());
  const [isLoading, setIsLoading] = useState(true);
  const [isMounted, setIsMounted] = useState(false);

  // Handle hydration mismatch by checking auth on client mount
  useEffect(() => {
    // Re-check auth on mount to handle SSR/client mismatch
    const token = localStorage.getItem(TOKEN_STORAGE_KEY);
    if (token && !isTokenExpired(token)) {
      const userData = decodeJwtUser(token);
      if (userData) {
        setUser(userData);
      }
    }
    setIsMounted(true);
    setIsLoading(false);
  }, []);

  const signout = () => {
    clearAccessToken();
    setUser(null);
    if (typeof window !== "undefined") {
      window.location.href = "/signin";
    }
  };

  const value: AuthContextState = {
    user,
    isLoading,
    isAuthenticated: !!user,
    setUser,
    signout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

/**
 * Hook to access auth context.
 * @returns Auth context state
 * @throws Error if used outside AuthProvider
 */
export function useAuth(): AuthContextState {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}
