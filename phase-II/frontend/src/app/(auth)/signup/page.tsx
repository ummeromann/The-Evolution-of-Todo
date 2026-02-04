"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect } from "react";
import { SignupForm } from "@/components/forms/signup-form";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { useAuth } from "@/contexts/auth-context";

/**
 * User registration page.
 *
 * This page allows new users to create an account with:
 * - Email and password authentication
 * - Client-side validation
 * - Secure password hashing via FastAPI backend
 * - Automatic redirect to dashboard on success
 *
 * Layout:
 * - Centered card design via AuthLayout
 * - Link to sign-in page for existing users
 * - Responsive design for all screen sizes
 *
 * Security:
 * - Already authenticated users are redirected to dashboard (T022)
 */
export default function SignupPage() {
  const router = useRouter();
  const { isAuthenticated, isLoading } = useAuth();

  /**
   * Redirect authenticated users to dashboard.
   * This prevents already logged-in users from seeing the signup page.
   * Security: Reduces confusion and prevents duplicate account creation attempts.
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
        <CardTitle>Create an account</CardTitle>
        <p className="text-sm text-muted-foreground mt-1">
          Sign up to start managing your todos
        </p>
      </CardHeader>
      <CardContent>
        <SignupForm />

        {/* Link to sign-in page */}
        <div className="mt-6 text-center">
          <p className="text-sm text-muted-foreground">
            Already have an account?{" "}
            <Link
              href="/signin"
              className="text-primary hover:text-primary/80 font-medium"
            >
              Sign in
            </Link>
          </p>
        </div>
      </CardContent>
    </Card>
  );
}
