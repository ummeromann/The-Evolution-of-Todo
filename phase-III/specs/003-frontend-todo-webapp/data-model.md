# Frontend Data Models: Todo Web Application

**Feature Branch**: `003-frontend-todo-webapp`
**Date**: 2026-01-15

## Overview

This document defines the frontend TypeScript types and interfaces used for data representation, API communication, and UI state management.

---

## API Response Types

### Task Model

```typescript
// Represents a task as returned from the API
interface Task {
  id: string;           // UUID
  description: string;  // 1-500 characters
  is_completed: boolean;
  created_at: string;   // ISO 8601 datetime
  updated_at: string;   // ISO 8601 datetime
}
```

### Task Create/Update Payloads

```typescript
// POST /api/tasks request body
interface TaskCreate {
  description: string;  // 1-500 characters, required
}

// PUT /api/tasks/{id} request body
interface TaskUpdate {
  description: string;  // 1-500 characters, required
}
```

### User Model

```typescript
// User data from Better Auth session
interface User {
  id: string;         // UUID
  email: string;
  name?: string;
}
```

### Session Model

```typescript
// Better Auth session response
interface Session {
  user: User | null;
  session: {
    id: string;
    userId: string;
    expiresAt: string;
  } | null;
}
```

### API Error Response

```typescript
// Standard error response from FastAPI
interface ApiError {
  detail: string;
  code?: string;
  field?: string;
}

// Validation error response
interface ValidationError {
  detail: Array<{
    loc: string[];
    msg: string;
    type: string;
  }>;
}
```

---

## UI State Types

### Form State

```typescript
// Generic form state for any form
interface FormState<T> {
  values: T;
  errors: Record<keyof T, string | null>;
  isSubmitting: boolean;
  isValid: boolean;
}

// Signup form specific
interface SignupFormValues {
  email: string;
  password: string;
  name?: string;
}

// Signin form specific
interface SigninFormValues {
  email: string;
  password: string;
}

// Task form specific
interface TaskFormValues {
  description: string;
}
```

### Task List State

```typescript
// Task list component state
interface TaskListState {
  tasks: Task[];
  isLoading: boolean;
  error: string | null;
}

// Individual task item state (for optimistic updates)
interface TaskItemState {
  task: Task;
  isEditing: boolean;
  isDeleting: boolean;
  isToggling: boolean;
  error: string | null;
}
```

### Auth State

```typescript
// Authentication context state
interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
}
```

### Dashboard Summary

```typescript
// Dashboard statistics
interface TaskSummary {
  total: number;
  completed: number;
  pending: number;
}
```

---

## API Client Types

### Request Configuration

```typescript
// API request options
interface ApiRequestOptions {
  method: 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE';
  body?: unknown;
  signal?: AbortSignal;
}

// API response wrapper
interface ApiResponse<T> {
  data: T | null;
  error: ApiError | null;
  status: number;
}
```

### API Functions Type Signatures

```typescript
// Task API function signatures
type ListTasks = () => Promise<ApiResponse<Task[]>>;
type GetTask = (id: string) => Promise<ApiResponse<Task>>;
type CreateTask = (data: TaskCreate) => Promise<ApiResponse<Task>>;
type UpdateTask = (id: string, data: TaskUpdate) => Promise<ApiResponse<Task>>;
type DeleteTask = (id: string) => Promise<ApiResponse<void>>;
type ToggleTask = (id: string) => Promise<ApiResponse<Task>>;
```

---

## Component Props Types

### UI Components

```typescript
// Button component
interface ButtonProps {
  children: React.ReactNode;
  type?: 'button' | 'submit' | 'reset';
  variant?: 'primary' | 'secondary' | 'danger' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  isLoading?: boolean;
  disabled?: boolean;
  onClick?: () => void;
  className?: string;
}

// Input component
interface InputProps {
  id: string;
  name: string;
  type?: 'text' | 'email' | 'password';
  label?: string;
  placeholder?: string;
  value: string;
  error?: string | null;
  disabled?: boolean;
  maxLength?: number;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  onBlur?: (e: React.FocusEvent<HTMLInputElement>) => void;
  className?: string;
}

// Card component
interface CardProps {
  children: React.ReactNode;
  className?: string;
}
```

### Task Components

```typescript
// TaskList component
interface TaskListProps {
  // No props - fetches its own data
}

// TaskItem component
interface TaskItemProps {
  task: Task;
  onEdit: (task: Task) => void;
  onDelete: (taskId: string) => void;
  onToggle: (taskId: string) => void;
}

// TaskForm component (create/edit)
interface TaskFormProps {
  mode: 'create' | 'edit';
  initialTask?: Task;
  onSubmit: (data: TaskCreate | TaskUpdate) => Promise<void>;
  onCancel?: () => void;
}

// EmptyState component
interface EmptyStateProps {
  title: string;
  message: string;
  action?: {
    label: string;
    onClick: () => void;
  };
}
```

### Layout Components

```typescript
// Header component
interface HeaderProps {
  user: User | null;
  onSignOut: () => void;
}

// NavMenu component
interface NavMenuProps {
  isOpen: boolean;
  onClose: () => void;
}
```

### Common Components

```typescript
// LoadingSpinner component
interface LoadingSpinnerProps {
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}

// ErrorMessage component
interface ErrorMessageProps {
  message: string;
  onRetry?: () => void;
  className?: string;
}

// ConfirmDialog component
interface ConfirmDialogProps {
  isOpen: boolean;
  title: string;
  message: string;
  confirmLabel?: string;
  cancelLabel?: string;
  onConfirm: () => void;
  onCancel: () => void;
  isLoading?: boolean;
}
```

---

## Validation Rules

### Email Validation

```typescript
const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

function validateEmail(email: string): string | null {
  if (!email) return 'Email is required';
  if (!EMAIL_REGEX.test(email)) return 'Invalid email format';
  return null;
}
```

### Password Validation

```typescript
const MIN_PASSWORD_LENGTH = 8;

function validatePassword(password: string): string | null {
  if (!password) return 'Password is required';
  if (password.length < MIN_PASSWORD_LENGTH) {
    return `Password must be at least ${MIN_PASSWORD_LENGTH} characters`;
  }
  return null;
}
```

### Task Description Validation

```typescript
const MIN_DESCRIPTION_LENGTH = 1;
const MAX_DESCRIPTION_LENGTH = 500;

function validateTaskDescription(description: string): string | null {
  const trimmed = description.trim();
  if (!trimmed) return 'Description is required';
  if (trimmed.length > MAX_DESCRIPTION_LENGTH) {
    return `Description must be ${MAX_DESCRIPTION_LENGTH} characters or less`;
  }
  return null;
}
```

---

## State Relationships

```text
┌─────────────────────────────────────────────────────────────┐
│                        App State                             │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────────┐                                        │
│  │   AuthState     │ ← Better Auth session                  │
│  │   (Global)      │                                        │
│  └────────┬────────┘                                        │
│           │                                                  │
│           ▼                                                  │
│  ┌─────────────────┐     ┌─────────────────┐               │
│  │ TaskListState   │────►│ TaskItemState   │ × N           │
│  │ (Tasks page)    │     │ (Per task)      │               │
│  └────────┬────────┘     └─────────────────┘               │
│           │                                                  │
│           ▼                                                  │
│  ┌─────────────────┐                                        │
│  │  TaskSummary    │ ← Derived from tasks                   │
│  │  (Dashboard)    │                                        │
│  └─────────────────┘                                        │
│                                                              │
│  ┌─────────────────┐                                        │
│  │   FormState     │ ← Per form instance                    │
│  │   (Local)       │   (signin, signup, task)               │
│  └─────────────────┘                                        │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Type Export File

All types should be exported from `frontend/src/types/index.ts`:

```typescript
// frontend/src/types/index.ts

// API Types
export type { Task, TaskCreate, TaskUpdate } from './task';
export type { User, Session } from './auth';
export type { ApiError, ValidationError, ApiResponse, ApiRequestOptions } from './api';

// UI State Types
export type { FormState, SignupFormValues, SigninFormValues, TaskFormValues } from './forms';
export type { TaskListState, TaskItemState, TaskSummary } from './tasks';
export type { AuthState } from './auth';

// Component Props Types
export type { ButtonProps, InputProps, CardProps } from './ui';
export type { TaskListProps, TaskItemProps, TaskFormProps, EmptyStateProps } from './tasks';
export type { HeaderProps, NavMenuProps } from './layout';
export type { LoadingSpinnerProps, ErrorMessageProps, ConfirmDialogProps } from './common';
```
