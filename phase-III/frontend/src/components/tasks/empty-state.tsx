/**
 * Empty state component shown when user has no tasks.
 */

export function EmptyState() {
  return (
    <div className="text-center py-8">
      <div className="text-muted-foreground mb-2">
        <svg
          className="mx-auto h-12 w-12"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          aria-hidden="true"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={1.5}
            d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
          />
        </svg>
      </div>
      <h3 className="text-lg font-medium text-foreground mb-1">No tasks yet</h3>
      <p className="text-muted-foreground">
        Create your first task to get started!
      </p>
    </div>
  );
}
