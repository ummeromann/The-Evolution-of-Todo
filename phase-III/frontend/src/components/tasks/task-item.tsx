"use client";

import { Task } from "@/types";
import { cn } from "@/lib/utils";

interface TaskItemProps {
  task: Task;
  onToggle?: (taskId: string) => void;
  onEdit?: (taskId: string, description: string) => void;
  onDelete?: (taskId: string) => void;
}

export function TaskItem({ task, onToggle, onEdit, onDelete }: TaskItemProps) {
  return (
    <div
      className={cn(
        "flex items-center justify-between p-4 rounded-lg border transition-colors",
        task.is_completed
          ? "bg-green-500/10 border-green-500/30"
          : "bg-card border-border hover:border-primary/50"
      )}
    >
      <div className="flex items-center gap-3 flex-1">
        {/* Completion checkbox */}
        <button
          onClick={() => onToggle?.(task.id)}
          className={cn(
            "w-5 h-5 rounded border-2 flex items-center justify-center transition-colors",
            task.is_completed
              ? "bg-green-500 border-green-500 text-white"
              : "border-muted-foreground/50 hover:border-primary"
          )}
          aria-label={task.is_completed ? "Mark as pending" : "Mark as completed"}
        >
          {task.is_completed && (
            <svg
              className="w-3 h-3"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={3}
                d="M5 13l4 4L19 7"
              />
            </svg>
          )}
        </button>

        {/* Task description */}
        <span
          className={cn(
            "flex-1 text-foreground",
            task.is_completed && "line-through text-muted-foreground"
          )}
        >
          {task.description}
        </span>
      </div>

      {/* Action buttons */}
      <div className="flex items-center gap-2">
        {onEdit && (
          <button
            onClick={() => onEdit(task.id, task.description)}
            className="p-1 text-muted-foreground hover:text-primary transition-colors"
            aria-label="Edit task"
          >
            <svg
              className="w-4 h-4"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"
              />
            </svg>
          </button>
        )}
        {onDelete && (
          <button
            onClick={() => onDelete(task.id)}
            className="p-1 text-muted-foreground hover:text-destructive transition-colors"
            aria-label="Delete task"
          >
            <svg
              className="w-4 h-4"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
              />
            </svg>
          </button>
        )}
      </div>
    </div>
  );
}
