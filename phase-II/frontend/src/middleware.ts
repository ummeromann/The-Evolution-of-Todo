import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

/**
 * Next.js middleware to add security headers to protected routes.
 *
 * This middleware intercepts requests to protected routes and adds
 * cache control headers to prevent sensitive content from being
 * cached by the browser.
 *
 * Security Purpose (T050):
 * - Prevents browser back button from exposing protected content after signout
 * - Ensures sensitive data is not stored in browser cache
 * - Forces browser to revalidate authentication on every visit
 */
export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  // Apply cache control headers to protected routes
  const isProtectedRoute =
    pathname.startsWith("/dashboard") ||
    pathname.startsWith("/todos") ||
    (pathname !== "/" &&
      pathname !== "/signin" &&
      pathname !== "/signup" &&
      !pathname.startsWith("/_next") &&
      !pathname.startsWith("/api"));

  if (isProtectedRoute) {
    const response = NextResponse.next();

    // T050: Cache control headers to prevent browser back button exposure
    response.headers.set(
      "Cache-Control",
      "no-store, no-cache, must-revalidate, private, max-age=0"
    );

    // Additional security headers
    response.headers.set("X-Frame-Options", "DENY");
    response.headers.set("X-Content-Type-Options", "nosniff");
    response.headers.set("X-XSS-Protection", "1; mode=block");

    return response;
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/((?!_next/static|_next/image|favicon.ico).*)"],
};
