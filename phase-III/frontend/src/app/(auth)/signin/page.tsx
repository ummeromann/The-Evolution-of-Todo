"use client";

import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { useEffect, useState, Suspense } from "react";
import { SigninForm } from "@/components/forms/signin-form";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { useAuth } from "@/contexts/auth-context";

/**
 * Inner component that uses useSearchParams.
 * Separated to allow proper Suspense boundary wrapping.
 */
function SigninContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const { isAuthenticated, isLoading } = useAuth();
  const [sessionExpiredMessage, setSessionExpiredMessage] = useState<string | null>(null);

  /**
   * Check for session_expired query parameter and show appropriate message.
   * This handles cases where user was redirected due to expired session.
   */
  useEffect(() => {
    const error = searchParams.get("error");
    if (error === "session_expired") {
      setSessionExpiredMessage("Your session has expired. Please sign in again.");
    }
  }, [searchParams]);

  /**
   * Redirect authenticated users to dashboard.
   * This prevents already logged-in users from seeing the signin page.
   * Security: Reduces confusion and prevents unnecessary auth attempts.
   */
  useEffect(() => {
    if (!isLoading && isAuthenticated) {
      window.location.href = "/dashboard";
    }
  }, [isAuthenticated, isLoading]);

  // Show loading or nothing while checking auth status
  if (isLoading || isAuthenticated) {
    return null;
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Welcome back</CardTitle>
        <p className="text-sm text-muted-foreground mt-1">
          Sign in to your account to continue
        </p>
      </CardHeader>
      <CardContent>
        {/* Session expired message */}
        {sessionExpiredMessage && (
          <div className="mb-4 p-3 bg-yellow-500/10 border border-yellow-500/30 rounded-md">
            <p className="text-sm text-yellow-600 dark:text-yellow-400">{sessionExpiredMessage}</p>
          </div>
        )}
        <SigninForm />

        {/* Link to sign-up page */}
        <div className="mt-6 text-center">
          <p className="text-sm text-muted-foreground">
            Don&apos;t have an account?{" "}
            <Link
              href="/signup"
              className="text-primary hover:text-primary/80 font-medium"
            >
              Sign up
            </Link>
          </p>
        </div>
      </CardContent>
    </Card>
  );
}

/**
 * User sign-in page.
 *
 * This page allows existing users to authenticate with:
 * - Email and password credentials
 * - Client-side validation
 * - JWT token authentication via Better Auth
 * - Automatic redirect to dashboard on success
 *
 * Layout:
 * - Centered card design via AuthLayout
 * - Link to sign-up page for new users
 * - Responsive design for all screen sizes
 *
 * Security:
 * - Generic error messages prevent user enumeration
 * - Session tokens stored in HTTP-only cookies
 * - Rate limiting prevents brute force attacks (backend)
 * - Already authenticated users are redirected to dashboard (T021)
 */
export default function SigninPage() {
  return (
    <Suspense fallback={null}>
      <SigninContent />
    </Suspense>
  );
}
