"use client";

import { useState, useEffect, useCallback } from "react";
import { TaskForm } from "@/components/forms/task-form";
import { TaskList } from "@/components/tasks/task-list";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { ErrorMessage } from "@/components/common/error-message";
import { ConfirmDialog } from "@/components/common/confirm-dialog";
import { Task } from "@/types";
import { taskApi } from "@/lib/api";
import { useAuth } from "@/contexts/auth-context";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Spinner } from "@/components/ui/spinner";

/**
 * Dashboard page - main task management interface.
 *
 * Features:
 * - Task list display with loading and empty states
 * - Create new tasks inline
 * - Toggle task completion with optimistic updates
 * - Edit task description via modal
 * - Delete task with confirmation dialog
 * - Error handling with retry capability
 */
export default function DashboardPage() {
  const { user } = useAuth();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Edit modal state
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [editDescription, setEditDescription] = useState("");
  const [isEditing, setIsEditing] = useState(false);
  const [editError, setEditError] = useState("");

  // Delete confirmation state
  const [deletingTaskId, setDeletingTaskId] = useState<string | null>(null);
  const [isDeleting, setIsDeleting] = useState(false);

  // Fetch tasks on mount
  const fetchTasks = useCallback(async () => {
    try {
      setIsLoading(true);
      setError(null);
      const data = await taskApi.list();
      setTasks(data);
    } catch (err) {
      const message = err instanceof Error ? err.message : "Failed to load tasks";
      setError(message);
      console.error("Error fetching tasks:", err);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchTasks();
  }, [fetchTasks]);

  // Calculate task statistics
  const totalTasks = tasks.length;
  const completedTasks = tasks.filter((t) => t.is_completed).length;
  const pendingTasks = totalTasks - completedTasks;

  // Handle new task creation
  const handleTaskCreated = (task: Task) => {
    setTasks((prev) => [task, ...prev]);
  };

  // Handle task toggle with optimistic update
  const handleToggle = async (taskId: string) => {
    // Optimistic update
    setTasks((prev) =>
      prev.map((t) =>
        t.id === taskId ? { ...t, is_completed: !t.is_completed } : t
      )
    );

    try {
      const updatedTask = await taskApi.toggle(taskId);
      // Update with server response
      setTasks((prev) =>
        prev.map((t) => (t.id === taskId ? updatedTask : t))
      );
    } catch (err) {
      // Revert optimistic update on error
      setTasks((prev) =>
        prev.map((t) =>
          t.id === taskId ? { ...t, is_completed: !t.is_completed } : t
        )
      );
      console.error("Error toggling task:", err);
    }
  };

  // Open edit modal
  const handleEdit = (taskId: string, description: string) => {
    const task = tasks.find((t) => t.id === taskId);
    if (task) {
      setEditingTask(task);
      setEditDescription(description);
      setEditError("");
    }
  };

  // Submit edit
  const handleEditSubmit = async () => {
    if (!editingTask) return;

    const trimmed = editDescription.trim();
    if (!trimmed) {
      setEditError("Description is required");
      return;
    }
    if (trimmed.length > 500) {
      setEditError("Description must be 500 characters or less");
      return;
    }
    if (trimmed === editingTask.description) {
      setEditingTask(null);
      return;
    }

    setIsEditing(true);
    setEditError("");

    try {
      const updatedTask = await taskApi.update(editingTask.id, {
        description: trimmed,
      });
      setTasks((prev) =>
        prev.map((t) => (t.id === editingTask.id ? updatedTask : t))
      );
      setEditingTask(null);
    } catch (err) {
      const message = err instanceof Error ? err.message : "Failed to update task";
      setEditError(message);
    } finally {
      setIsEditing(false);
    }
  };

  // Close edit modal
  const handleEditCancel = () => {
    setEditingTask(null);
    setEditError("");
  };

  // Open delete confirmation
  const handleDelete = (taskId: string) => {
    setDeletingTaskId(taskId);
  };

  // Confirm delete
  const handleDeleteConfirm = async () => {
    if (!deletingTaskId) return;

    setIsDeleting(true);

    try {
      await taskApi.delete(deletingTaskId);
      setTasks((prev) => prev.filter((t) => t.id !== deletingTaskId));
      setDeletingTaskId(null);
    } catch (err) {
      console.error("Error deleting task:", err);
    } finally {
      setIsDeleting(false);
    }
  };

  // Cancel delete
  const handleDeleteCancel = () => {
    setDeletingTaskId(null);
  };

  return (
    <div className="space-y-6">
      {/* Welcome message with user email */}
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-foreground">
          Welcome back!
        </h2>
        <p className="text-muted-foreground">Manage your tasks, stay productive, and achieve more today.</p>
      </div>

      {/* Task Statistics */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <Card>
          <CardContent className="p-4">
            <div className="text-center">
              <p className="text-3xl font-bold text-foreground">{totalTasks}</p>
              <p className="text-sm text-muted-foreground">Total Tasks</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <div className="text-center">
              <p className="text-3xl font-bold text-green-500">{completedTasks}</p>
              <p className="text-sm text-muted-foreground">Completed</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <div className="text-center">
              <p className="text-3xl font-bold text-primary">{pendingTasks}</p>
              <p className="text-sm text-muted-foreground">Pending</p>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Create Task Form */}
      <Card>
        <CardHeader>
          <CardTitle>Create Task</CardTitle>
        </CardHeader>
        <CardContent>
          <TaskForm onTaskCreated={handleTaskCreated} />
        </CardContent>
      </Card>

      {/* Task List */}
      <Card>
        <CardHeader>
          <CardTitle>My Tasks</CardTitle>
        </CardHeader>
        <CardContent>
          {error ? (
            <ErrorMessage message={error} onRetry={fetchTasks} />
          ) : (
            <TaskList
              tasks={tasks}
              isLoading={isLoading}
              onToggle={handleToggle}
              onEdit={handleEdit}
              onDelete={handleDelete}
            />
          )}
        </CardContent>
      </Card>

      {/* Edit Task Modal */}
      {editingTask && (
        <div
          className="fixed inset-0 z-50 flex items-center justify-center"
          role="dialog"
          aria-modal="true"
        >
          <div
            className="absolute inset-0 bg-black/50"
            onClick={handleEditCancel}
          />
          <div className="relative bg-card text-card-foreground rounded-lg shadow-xl max-w-md w-full mx-4 p-6 border border-border">
            <h2 className="text-lg font-semibold text-foreground mb-4">
              Edit Task
            </h2>
            <div className="space-y-4">
              <Input
                type="text"
                value={editDescription}
                onChange={(e) => setEditDescription(e.target.value)}
                placeholder="Task description"
                maxLength={500}
                error={editError}
                disabled={isEditing}
              />
              <div className="text-xs text-muted-foreground text-right">
                {editDescription.length}/500
              </div>
              <div className="flex justify-end gap-3">
                <Button
                  variant="secondary"
                  onClick={handleEditCancel}
                  disabled={isEditing}
                >
                  Cancel
                </Button>
                <Button onClick={handleEditSubmit} disabled={isEditing}>
                  {isEditing ? (
                    <span className="flex items-center gap-2">
                      <Spinner size="sm" />
                      Saving...
                    </span>
                  ) : (
                    "Save"
                  )}
                </Button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Delete Confirmation Dialog */}
      <ConfirmDialog
        isOpen={!!deletingTaskId}
        title="Delete Task"
        message="Are you sure you want to delete this task? This action cannot be undone."
        confirmLabel="Delete"
        cancelLabel="Cancel"
        onConfirm={handleDeleteConfirm}
        onCancel={handleDeleteCancel}
        isLoading={isDeleting}
      />
    </div>
  );
}
