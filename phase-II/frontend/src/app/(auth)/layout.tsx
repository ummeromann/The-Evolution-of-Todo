"use client";

import { ReactNode } from "react";
import { ThemeToggle } from "@/components/theme-toggle";

/**
 * Layout for authentication pages (sign up, sign in, etc.).
 *
 * This layout provides a centered, responsive card design for auth forms:
 * - Full-height viewport with vertical centering
 * - Horizontal padding for mobile devices
 * - Max width constraint for better readability on large screens
 * - Theme-aware background
 *
 * Pages wrapped by this layout:
 * - /signup
 * - /signin
 * - /forgot-password (future)
 */
export default function AuthLayout({ children }: { children: ReactNode }) {
  return (
    <div className="min-h-screen flex items-center justify-center bg-muted px-4 relative">
      {/* Theme toggle in corner */}
      <div className="absolute top-4 right-4">
        <ThemeToggle />
      </div>
      <div className="w-full max-w-md">
        {children}
      </div>
    </div>
  );
}
