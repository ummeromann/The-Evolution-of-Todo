"use client";

import { Task } from "@/types";
import { TaskItem } from "./task-item";
import { EmptyState } from "./empty-state";
import { Spinner } from "@/components/ui/spinner";

interface TaskListProps {
  tasks: Task[];
  isLoading?: boolean;
  onToggle?: (taskId: string) => void;
  onEdit?: (taskId: string, description: string) => void;
  onDelete?: (taskId: string) => void;
}

export function TaskList({
  tasks,
  isLoading = false,
  onToggle,
  onEdit,
  onDelete,
}: TaskListProps) {
  if (isLoading) {
    return (
      <div className="flex justify-center py-8">
        <Spinner size="lg" />
      </div>
    );
  }

  if (tasks.length === 0) {
    return <EmptyState />;
  }

  return (
    <div className="space-y-3">
      {tasks.map((task) => (
        <TaskItem
          key={task.id}
          task={task}
          onToggle={onToggle}
          onEdit={onEdit}
          onDelete={onDelete}
        />
      ))}
    </div>
  );
}
