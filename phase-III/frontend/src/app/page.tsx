"use client";

import { ThemeToggle } from "@/components/theme-toggle";

export default function HomePage() {
  return (
    <main className="min-h-screen flex items-center justify-center bg-background relative">
      {/* Theme toggle in corner */}
      <div className="absolute top-4 right-4">
        <ThemeToggle />
      </div>

      <div className="text-center px-4">
        <h1 className="text-4xl md:text-6xl font-bold text-foreground mb-4">
          Todo Full Stack Web Application
        </h1>
        <p className="text-lg md:text-xl text-muted-foreground mb-8">
          Advanced Todo Management System
        </p>
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <a
            href="/signin"
            className="px-6 py-3 bg-primary text-primary-foreground rounded-lg font-medium hover:bg-primary/90 transition-colors"
          >
            Sign In
          </a>
          <a
            href="/signup"
            className="px-6 py-3 bg-secondary text-secondary-foreground border border-border rounded-lg font-medium hover:bg-secondary/80 transition-colors"
          >
            Sign Up
          </a>
        </div>
      </div>
    </main>
  );
}
