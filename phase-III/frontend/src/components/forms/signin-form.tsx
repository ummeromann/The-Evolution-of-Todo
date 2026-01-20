"use client";

import { useState, FormEvent } from "react";
import { useRouter } from "next/navigation";
import { authApi } from "@/lib/api";
import { useAuth } from "@/contexts/auth-context";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Spinner } from "@/components/ui/spinner";

/**
 * User sign-in form component.
 *
 * Features:
 * - Client-side validation (email format, required fields)
 * - Real-time error display
 * - Loading state with spinner during submission
 * - JWT token authentication via Better Auth
 * - Automatic redirect to dashboard on success
 *
 * Security:
 * - Credentials validated before database lookup
 * - Generic error messages to prevent user enumeration
 * - Password verification using constant-time comparison server-side
 * - JWT tokens stored in HTTP-only cookies by Better Auth
 */
export function SigninForm() {
  const router = useRouter();
  const { setUser } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [isLoading, setIsLoading] = useState(false);
  const [generalError, setGeneralError] = useState("");

  /**
   * Validates form inputs before submission.
   *
   * Validation rules:
   * - Email must be provided and match standard format
   * - Password must be provided
   *
   * @returns true if all validations pass, false otherwise
   */
  const validateForm = (): boolean => {
    const newErrors: Record<string, string> = {};

    // Email format validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!email) {
      newErrors.email = "Email is required";
    } else if (!emailRegex.test(email)) {
      newErrors.email = "Invalid email format";
    }

    // Password required validation
    if (!password) {
      newErrors.password = "Password is required";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  /**
   * Handles form submission and user authentication.
   *
   * Flow:
   * 1. Validate form inputs client-side
   * 2. Call Better Auth signIn API
   * 3. Handle success (redirect) or error (display generic message)
   *
   * Security considerations:
   * - Generic error messages prevent user enumeration attacks
   * - Server performs constant-time password comparison
   * - Rate limiting should be implemented on backend to prevent brute force
   *
   * Error handling:
   * - Network errors are caught and displayed
   * - Authentication failures show generic "Invalid credentials" message
   * - Unexpected errors show user-friendly message without leaking info
   */
  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setGeneralError("");

    // Client-side validation
    if (!validateForm()) {
      return;
    }

    setIsLoading(true);

    try {
      // Trim email to remove whitespace before submission
      const trimmedEmail = email.trim();

      // Call FastAPI signin endpoint
      const result = await authApi.signin({
        email: trimmedEmail,
        password,
      });

      // Set user in auth context
      setUser(result.user);

      // Success - redirect to dashboard (full page reload to ensure auth state is read)
      window.location.href = "/dashboard";
    } catch (error) {
      // Network or unexpected errors
      console.error("Sign in error:", error);
      // Generic error message to prevent user enumeration
      setGeneralError("Invalid email or password");
      setIsLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {/* General error message */}
      {generalError && (
        <div className="p-3 bg-destructive/10 border border-destructive/30 rounded-md">
          <p className="text-sm text-destructive">{generalError}</p>
        </div>
      )}

      {/* Email input */}
      <Input
        label="Email"
        type="email"
        name="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        error={errors.email}
        disabled={isLoading}
        placeholder="you@example.com"
        autoComplete="email"
        required
      />

      {/* Password input */}
      <Input
        label="Password"
        type="password"
        name="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        error={errors.password}
        disabled={isLoading}
        placeholder="Enter your password"
        autoComplete="current-password"
        required
      />

      {/* Submit button with loading state */}
      <Button
        type="submit"
        disabled={isLoading}
        className="w-full"
      >
        {isLoading ? (
          <span className="flex items-center justify-center gap-2">
            <Spinner size="sm" />
            Signing in...
          </span>
        ) : (
          "Sign In"
        )}
      </Button>
    </form>
  );
}
