import { auth } from "@/lib/auth";
import { toNextJsHandler } from "better-auth/next-js";

/**
 * Better Auth API route handler for Next.js App Router.
 *
 * This catch-all route handles all Better Auth endpoints:
 * - POST /api/auth/sign-up/email - Register new user
 * - POST /api/auth/sign-in/email - Authenticate user
 * - POST /api/auth/sign-out - End session
 * - GET /api/auth/session - Get current session
 *
 * The toNextJsHandler adapter converts Better Auth's internal
 * request/response format to Next.js App Router format.
 *
 * Security:
 * - All password operations use bcrypt hashing
 * - Sessions are stored securely in PostgreSQL
 * - JWT tokens are signed with BETTER_AUTH_SECRET
 */
export const { POST, GET } = toNextJsHandler(auth);
