"use client";

import { useState, FormEvent } from "react";
import { useRouter } from "next/navigation";
import { authApi } from "@/lib/api";
import { useAuth } from "@/contexts/auth-context";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Spinner } from "@/components/ui/spinner";

/**
 * User registration form component.
 *
 * Features:
 * - Client-side validation (email format, password minimum length)
 * - Real-time error display per field
 * - Loading state with spinner during submission
 * - Secure password hashing via Better Auth
 * - Automatic redirect to dashboard on success
 *
 * Security:
 * - Passwords are never stored in plain text
 * - Better Auth handles bcrypt hashing server-side
 * - Minimum password length of 8 characters enforced
 * - Email validation prevents malformed inputs
 */
export function SignupForm() {
  const router = useRouter();
  const { setUser } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [isLoading, setIsLoading] = useState(false);
  const [generalError, setGeneralError] = useState("");

  /**
   * Validates form inputs before submission.
   *
   * Validation rules:
   * - Email must match standard email format
   * - Password must be at least 8 characters
   * - Confirm password must match password
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

    // Password strength validation
    if (!password) {
      newErrors.password = "Password is required";
    } else if (password.length < 8) {
      newErrors.password = "Password must be at least 8 characters";
    }

    // Password confirmation validation
    if (!confirmPassword) {
      newErrors.confirmPassword = "Please confirm your password";
    } else if (password !== confirmPassword) {
      newErrors.confirmPassword = "Passwords do not match";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  /**
   * Handles form submission and user registration.
   *
   * Flow:
   * 1. Validate form inputs
   * 2. Call Better Auth signUp API
   * 3. Handle success (redirect) or error (display message)
   *
   * Error handling:
   * - Network errors are caught and displayed
   * - Validation errors from server (e.g., email exists) are shown
   * - Generic error message for unexpected failures
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

      // Call FastAPI signup endpoint
      const result = await authApi.signup({
        email: trimmedEmail,
        password,
      });

      // Set user in auth context
      setUser(result.user);

      // Success - redirect to dashboard (full page reload to ensure auth state is read)
      window.location.href = "/dashboard";
    } catch (error) {
      // Network or unexpected errors
      console.error("Sign up error:", error);
      const message = error instanceof Error ? error.message : "Sign up failed. Please try again.";
      setGeneralError(message);
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
        placeholder="Minimum 8 characters"
        autoComplete="new-password"
        required
      />

      {/* Confirm password input */}
      <Input
        label="Confirm Password"
        type="password"
        name="confirmPassword"
        value={confirmPassword}
        onChange={(e) => setConfirmPassword(e.target.value)}
        error={errors.confirmPassword}
        disabled={isLoading}
        placeholder="Re-enter your password"
        autoComplete="new-password"
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
            Creating account...
          </span>
        ) : (
          "Sign Up"
        )}
      </Button>
    </form>
  );
}
