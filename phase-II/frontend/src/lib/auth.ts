import { betterAuth } from "better-auth";
import { Pool } from "pg";

/**
 * Better Auth server configuration.
 *
 * This configures Better Auth to handle user authentication with:
 * - PostgreSQL database for storing users and sessions
 * - Email/password authentication with minimum password length of 8
 * - Session expiration of 7 days with daily update checks
 *
 * Security Notes:
 * - BETTER_AUTH_SECRET must be cryptographically random (min 32 chars)
 * - Database credentials should never be committed to version control
 * - Sessions are stored in the database for persistent authentication
 */
export const auth = betterAuth({
  database: new Pool({
    connectionString: process.env.DATABASE_URL,
  }),
  emailAndPassword: {
    enabled: true,
    minPasswordLength: 8, // Enforces password security requirement
  },
  session: {
    expiresIn: 60 * 60 * 24 * 7, // 7 days - balance between security and convenience
    updateAge: 60 * 60 * 24, // 1 day - session is refreshed if older than this
  },
  secret: process.env.BETTER_AUTH_SECRET, // Used for JWT signing and encryption
});
