# Frontend API Client Contract

**Feature Branch**: `003-frontend-todo-webapp`
**Date**: 2026-01-15

## Overview

This document defines the frontend API client contract for communicating with the FastAPI backend. The client handles JWT token attachment, error handling, and response parsing.

---

## API Client Configuration

### Base URL

```typescript
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
```

### Headers

All requests include:

```typescript
const headers = {
  'Content-Type': 'application/json',
  'Authorization': `Bearer ${token}`,  // For protected routes
};
```

---

## Authentication Token Flow

```text
┌─────────────────────────────────────────────────────────────┐
│                    Token Attachment Flow                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. API Client initialized                                   │
│                    │                                         │
│                    ▼                                         │
│  2. Get session from Better Auth client                     │
│     const session = await authClient.getSession();          │
│                    │                                         │
│                    ▼                                         │
│  3. Extract token from session                               │
│     const token = session?.session?.token;                  │
│                    │                                         │
│                    ▼                                         │
│  4. Attach to Authorization header                           │
│     headers.set('Authorization', `Bearer ${token}`)         │
│                    │                                         │
│                    ▼                                         │
│  5. Make API request                                         │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## API Methods

### Task Operations

#### List Tasks

```typescript
async function listTasks(): Promise<ApiResponse<Task[]>> {
  return apiRequest<Task[]>('/api/tasks', { method: 'GET' });
}
```

**Request**: `GET /api/tasks`
**Headers**: `Authorization: Bearer <token>`
**Response**: `200 OK` with `Task[]`

#### Get Task

```typescript
async function getTask(id: string): Promise<ApiResponse<Task>> {
  return apiRequest<Task>(`/api/tasks/${id}`, { method: 'GET' });
}
```

**Request**: `GET /api/tasks/{id}`
**Headers**: `Authorization: Bearer <token>`
**Response**: `200 OK` with `Task` | `404 Not Found`

#### Create Task

```typescript
async function createTask(data: TaskCreate): Promise<ApiResponse<Task>> {
  return apiRequest<Task>('/api/tasks', {
    method: 'POST',
    body: data,
  });
}
```

**Request**: `POST /api/tasks`
**Headers**: `Authorization: Bearer <token>`, `Content-Type: application/json`
**Body**: `{ "description": "string" }`
**Response**: `201 Created` with `Task` | `400 Bad Request`

#### Update Task

```typescript
async function updateTask(id: string, data: TaskUpdate): Promise<ApiResponse<Task>> {
  return apiRequest<Task>(`/api/tasks/${id}`, {
    method: 'PUT',
    body: data,
  });
}
```

**Request**: `PUT /api/tasks/{id}`
**Headers**: `Authorization: Bearer <token>`, `Content-Type: application/json`
**Body**: `{ "description": "string" }`
**Response**: `200 OK` with `Task` | `400`/`403`/`404`

#### Delete Task

```typescript
async function deleteTask(id: string): Promise<ApiResponse<void>> {
  return apiRequest<void>(`/api/tasks/${id}`, { method: 'DELETE' });
}
```

**Request**: `DELETE /api/tasks/{id}`
**Headers**: `Authorization: Bearer <token>`
**Response**: `204 No Content` | `403`/`404`

#### Toggle Task

```typescript
async function toggleTask(id: string): Promise<ApiResponse<Task>> {
  return apiRequest<Task>(`/api/tasks/${id}/toggle`, { method: 'PATCH' });
}
```

**Request**: `PATCH /api/tasks/{id}/toggle`
**Headers**: `Authorization: Bearer <token>`
**Response**: `200 OK` with `Task` | `403`/`404`

---

## Error Handling

### Error Response Handler

```typescript
async function handleErrorResponse(response: Response): Promise<ApiError> {
  try {
    const data = await response.json();
    return {
      detail: data.detail || 'An error occurred',
      code: data.code,
      field: data.field,
    };
  } catch {
    return {
      detail: getDefaultErrorMessage(response.status),
    };
  }
}

function getDefaultErrorMessage(status: number): string {
  switch (status) {
    case 400: return 'Invalid request';
    case 401: return 'Please sign in to continue';
    case 403: return 'You do not have permission to perform this action';
    case 404: return 'Resource not found';
    case 500: return 'Server error. Please try again later.';
    default: return 'An unexpected error occurred';
  }
}
```

### 401 Unauthorized Handling

```typescript
// In API client base request function
if (response.status === 401) {
  // Clear auth state
  await authClient.signOut();
  // Redirect to signin
  window.location.href = '/signin?error=session_expired';
  throw new Error('Session expired');
}
```

---

## Request Timeout

```typescript
const REQUEST_TIMEOUT = 30000; // 30 seconds

async function apiRequest<T>(
  endpoint: string,
  options: ApiRequestOptions
): Promise<ApiResponse<T>> {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), REQUEST_TIMEOUT);

  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      ...options,
      signal: controller.signal,
    });
    // ... handle response
  } finally {
    clearTimeout(timeoutId);
  }
}
```

---

## Response Type

```typescript
interface ApiResponse<T> {
  data: T | null;
  error: ApiError | null;
  status: number;
}

// Usage example
const response = await createTask({ description: 'My task' });
if (response.error) {
  // Handle error
  console.error(response.error.detail);
} else {
  // Use data
  const task = response.data;
}
```

---

## Complete API Client Implementation

```typescript
// frontend/src/lib/api.ts

import { authClient } from './auth-client';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
const REQUEST_TIMEOUT = 30000;

interface ApiRequestOptions {
  method: 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE';
  body?: unknown;
}

interface ApiResponse<T> {
  data: T | null;
  error: { detail: string; code?: string } | null;
  status: number;
}

async function getAuthToken(): Promise<string | null> {
  const session = await authClient.getSession();
  return session?.session?.token || null;
}

async function apiRequest<T>(
  endpoint: string,
  options: ApiRequestOptions
): Promise<ApiResponse<T>> {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), REQUEST_TIMEOUT);

  try {
    const token = await getAuthToken();
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
    };

    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      method: options.method,
      headers,
      body: options.body ? JSON.stringify(options.body) : undefined,
      signal: controller.signal,
    });

    clearTimeout(timeoutId);

    // Handle 401 - redirect to signin
    if (response.status === 401) {
      await authClient.signOut();
      window.location.href = '/signin?error=session_expired';
      return { data: null, error: { detail: 'Session expired' }, status: 401 };
    }

    // Handle no content response
    if (response.status === 204) {
      return { data: null, error: null, status: 204 };
    }

    // Parse JSON response
    const data = await response.json();

    if (!response.ok) {
      return {
        data: null,
        error: { detail: data.detail || 'An error occurred', code: data.code },
        status: response.status,
      };
    }

    return { data, error: null, status: response.status };
  } catch (error) {
    clearTimeout(timeoutId);

    if (error instanceof Error && error.name === 'AbortError') {
      return { data: null, error: { detail: 'Request timed out' }, status: 0 };
    }

    return { data: null, error: { detail: 'Network error' }, status: 0 };
  }
}

// Task API functions
export const taskApi = {
  list: () => apiRequest<Task[]>('/api/tasks', { method: 'GET' }),
  get: (id: string) => apiRequest<Task>(`/api/tasks/${id}`, { method: 'GET' }),
  create: (data: TaskCreate) => apiRequest<Task>('/api/tasks', { method: 'POST', body: data }),
  update: (id: string, data: TaskUpdate) => apiRequest<Task>(`/api/tasks/${id}`, { method: 'PUT', body: data }),
  delete: (id: string) => apiRequest<void>(`/api/tasks/${id}`, { method: 'DELETE' }),
  toggle: (id: string) => apiRequest<Task>(`/api/tasks/${id}/toggle`, { method: 'PATCH' }),
};
```

---

## Environment Variables

### Frontend (.env.local)

```bash
# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000

# Better Auth configuration
BETTER_AUTH_SECRET=<same-as-backend>
BETTER_AUTH_URL=http://localhost:3000
DATABASE_URL=<neon-connection-string>
```

---

## Testing Contract

### Success Cases

```typescript
// List tasks - empty
const emptyResult = await taskApi.list();
expect(emptyResult.status).toBe(200);
expect(emptyResult.data).toEqual([]);

// Create task
const createResult = await taskApi.create({ description: 'Test' });
expect(createResult.status).toBe(201);
expect(createResult.data?.description).toBe('Test');

// Toggle task
const toggleResult = await taskApi.toggle(taskId);
expect(toggleResult.status).toBe(200);
expect(toggleResult.data?.is_completed).toBe(true);

// Delete task
const deleteResult = await taskApi.delete(taskId);
expect(deleteResult.status).toBe(204);
```

### Error Cases

```typescript
// No token - 401
const noAuthResult = await taskApi.list(); // without auth
expect(noAuthResult.status).toBe(401);

// Invalid task ID - 404
const notFoundResult = await taskApi.get('invalid-uuid');
expect(notFoundResult.status).toBe(404);

// Empty description - 400
const validationResult = await taskApi.create({ description: '' });
expect(validationResult.status).toBe(400);
```
