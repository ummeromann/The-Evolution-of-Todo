"use client";

import { Button } from "@/components/ui/button";
import { ErrorMessageProps } from "@/types";

/**
 * Error message display component with optional retry action.
 *
 * Features:
 * - Displays error message in a styled container
 * - Optional retry button for recoverable errors
 * - Consistent error styling across the application
 *
 * Usage:
 * - API failures with retry capability
 * - Form validation errors
 * - Network errors
 */
export function ErrorMessage({
  message,
  onRetry,
  className = "",
}: ErrorMessageProps) {
  return (
    <div
      className={`p-4 bg-destructive/10 border border-destructive/30 rounded-lg ${className}`}
      role="alert"
    >
      <div className="flex items-center justify-between gap-4">
        <div className="flex items-center gap-2">
          <svg
            className="w-5 h-5 text-destructive flex-shrink-0"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
            />
          </svg>
          <p className="text-sm text-destructive">{message}</p>
        </div>

        {onRetry && (
          <Button
            variant="secondary"
            size="sm"
            onClick={onRetry}
            className="flex-shrink-0"
          >
            Try again
          </Button>
        )}
      </div>
    </div>
  );
}
