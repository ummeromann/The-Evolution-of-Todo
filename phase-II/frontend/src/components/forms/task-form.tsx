"use client";

import { useState } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Spinner } from "@/components/ui/spinner";
import { taskApi } from "@/lib/api";
import { Task } from "@/types";

interface TaskFormProps {
  onTaskCreated: (task: Task) => void;
}

export function TaskForm({ onTaskCreated }: TaskFormProps) {
  const [description, setDescription] = useState("");
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    const trimmedDescription = description.trim();

    if (!trimmedDescription) {
      setError("Task description is required");
      return;
    }

    if (trimmedDescription.length > 500) {
      setError("Task description must be 500 characters or less");
      return;
    }

    setIsLoading(true);

    try {
      const task = await taskApi.create({
        description: trimmedDescription,
      });
      setDescription("");
      onTaskCreated(task);
    } catch (err: unknown) {
      const errorMessage =
        err instanceof Error ? err.message : "Failed to create task";
      setError(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex gap-2">
      <div className="flex-1">
        <Input
          type="text"
          placeholder="Enter a new task..."
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          maxLength={500}
          error={error}
        />
      </div>
      <Button type="submit" disabled={isLoading}>
        {isLoading ? <Spinner size="sm" /> : "Add Task"}
      </Button>
    </form>
  );
}
