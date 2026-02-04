import { createAuthClient } from "better-auth/react";

/**
 * Better Auth client SDK for React components.
 *
 * This provides client-side authentication methods that can be used
 * in React components to:
 * - Sign up new users
 * - Sign in existing users
 * - Sign out users
 * - Access current session state
 *
 * The baseURL determines where auth requests are sent:
 * - In development: defaults to http://localhost:3000
 * - In production: should be set via NEXT_PUBLIC_API_URL env var
 *
 * Usage:
 * ```tsx
 * import { signUp, signIn, signOut, useSession } from "@/lib/auth-client";
 *
 * function MyComponent() {
 *   const { data: session } = useSession();
 *   // ... use auth methods
 * }
 * ```
 */
export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_BETTER_AUTH_URL || "http://localhost:3000",
});

// Export commonly used auth methods for convenience
export const { signIn, signUp, signOut, useSession } = authClient;
