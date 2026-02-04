"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/contexts/auth-context";
import { Button } from "@/components/ui/button";
import { Spinner } from "@/components/ui/spinner";
import { ThemeToggle } from "@/components/theme-toggle";

/**
 * Protected layout wrapper for authenticated pages.
 *
 * This layout ensures that only authenticated users can access protected routes:
 * - Checks auth state using JWT token from localStorage
 * - Redirects unauthenticated users to sign-in page
 * - Displays loading state during auth verification
 * - Provides header with user info and sign-out button
 *
 * Security:
 * - Auth validation occurs on every render
 * - Automatic redirect prevents unauthorized access
 * - Sign-out properly clears JWT tokens
 * - No protected content shown during loading state
 *
 * Layout structure:
 * - Header with app title, user email, and sign-out button
 * - Main content area with max-width constraint
 * - Responsive padding and spacing
 */
export default function ProtectedLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const router = useRouter();
  const { user, isLoading, isAuthenticated, signout } = useAuth();
  const [isSigningOut, setIsSigningOut] = useState(false);

  /**
   * Redirect to sign-in if not authenticated.
   *
   * This effect runs whenever auth state changes:
   * - During initial load (isLoading = true)
   * - After auth verification completes
   * - When session expires or is invalidated
   *
   * Security note: No protected content is rendered until auth is verified.
   */
  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      // Use window.location for full page load to avoid hydration issues
      window.location.href = "/signin";
    }
  }, [isAuthenticated, isLoading]);

  /**
   * Handles user sign-out.
   *
   * Flow:
   * 1. Set loading state
   * 2. Clear JWT token from storage
   * 3. Redirect to sign-in page
   *
   * Security:
   * - JWT token is cleared from localStorage
   * - User is redirected to prevent lingering on protected pages
   */
  const handleSignOut = () => {
    setIsSigningOut(true);
    signout();
  };

  // Show loading spinner during auth verification
  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <div className="text-center">
          <Spinner size="lg" />
          <p className="mt-4 text-sm text-muted-foreground">Verifying session...</p>
        </div>
      </div>
    );
  }

  // Don't render protected content if not authenticated
  if (!isAuthenticated) {
    return null;
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Header with user info and sign-out */}
      <header className="bg-card border-b border-border shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <h1 className="text-xl font-bold text-foreground">Smart Todo Manager</h1>

            <div className="flex items-center gap-4">
              {/* Theme toggle */}
              <ThemeToggle />

              {/* Sign-out button */}
              <Button
                variant="secondary"
                size="sm"
                onClick={handleSignOut}
                disabled={isSigningOut}
              >
                {isSigningOut ? (
                  <span className="flex items-center gap-2">
                    <Spinner size="sm" />
                    Signing out...
                  </span>
                ) : (
                  "Sign Out"
                )}
              </Button>
            </div>
          </div>
        </div>
      </header>

      {/* Main content area */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {children}
      </main>
    </div>
  );
}
