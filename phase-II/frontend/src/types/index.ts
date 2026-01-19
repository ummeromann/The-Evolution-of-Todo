// Common types for the application

// ============================================
// API Response Types
// ============================================

/**
 * Task model as returned from the API
 */
export interface Task {
  id: string;
  description: string;
  is_completed: boolean;
  created_at: string;
  updated_at: string;
}

/**
 * POST /api/tasks request body
 */
export interface TaskCreate {
  description: string;
}

/**
 * PUT /api/tasks/{id} request body
 */
export interface TaskUpdate {
  description: string;
}

/**
 * User model from Better Auth session
 */
export interface User {
  id: string;
  email: string;
  name?: string;
}

/**
 * Better Auth session response
 */
export interface Session {
  user: User | null;
  session: {
    id: string;
    userId: string;
    expiresAt: string;
  } | null;
}

/**
 * Standard error response from FastAPI
 */
export interface ApiError {
  detail: string;
  code?: string;
  field?: string;
}

/**
 * Validation error response
 */
export interface ValidationError {
  detail: Array<{
    loc: string[];
    msg: string;
    type: string;
  }>;
}

/**
 * API response wrapper
 */
export interface ApiResponse<T> {
  data: T | null;
  error: ApiError | null;
  status: number;
}

// ============================================
// UI State Types
// ============================================

/**
 * Task list component state
 */
export interface TaskListState {
  tasks: Task[];
  isLoading: boolean;
  error: string | null;
}

/**
 * Dashboard statistics
 */
export interface TaskSummary {
  total: number;
  completed: number;
  pending: number;
}

// ============================================
// Component Props Types
// ============================================

/**
 * ErrorMessage component props
 */
export interface ErrorMessageProps {
  message: string;
  onRetry?: () => void;
  className?: string;
}

/**
 * ConfirmDialog component props
 */
export interface ConfirmDialogProps {
  isOpen: boolean;
  title: string;
  message: string;
  confirmLabel?: string;
  cancelLabel?: string;
  onConfirm: () => void;
  onCancel: () => void;
  isLoading?: boolean;
}
