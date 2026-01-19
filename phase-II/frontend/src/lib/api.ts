// API client utility for communicating with FastAPI backend

import { Task, TaskCreate, TaskUpdate, ApiResponse } from '@/types';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
const REQUEST_TIMEOUT = 30000; // 30 seconds

/**
 * Redirect to signin page on authentication failure.
 *
 * This function is called when:
 * - JWT token is expired (401 with "Token has expired")
 * - JWT token is invalid or missing (401)
 * - User session is no longer valid
 *
 * Security: Prevents authenticated API calls with invalid tokens
 * by redirecting users to re-authenticate.
 */
function redirectToSignin() {
  if (typeof window !== 'undefined') {
    // Store current path to redirect back after signin
    const currentPath = window.location.pathname;
    if (currentPath !== '/signin' && currentPath !== '/signup') {
      sessionStorage.setItem('redirect_after_signin', currentPath);
    }
    window.location.href = '/signin';
  }
}

/**
 * Storage key for JWT access token.
 */
const TOKEN_STORAGE_KEY = 'todo_access_token';

/**
 * Retrieves the JWT access token from localStorage.
 *
 * The token is stored after successful signup/signin with the FastAPI backend.
 *
 * Security:
 * - Tokens are stored in localStorage (accessible to JavaScript)
 * - For production, consider httpOnly cookies via backend
 * - Backend must validate tokens on every protected request
 *
 * @returns JWT access token or null if not found
 */
function getAccessToken(): string | null {
  if (typeof window === 'undefined') {
    return null; // Server-side, no localStorage available
  }

  return localStorage.getItem(TOKEN_STORAGE_KEY);
}

/**
 * Stores the JWT access token in localStorage.
 *
 * @param token - JWT access token to store
 */
export function setAccessToken(token: string): void {
  if (typeof window !== 'undefined') {
    localStorage.setItem(TOKEN_STORAGE_KEY, token);
  }
}

/**
 * Removes the JWT access token from localStorage.
 * Call this on signout.
 */
export function clearAccessToken(): void {
  if (typeof window !== 'undefined') {
    localStorage.removeItem(TOKEN_STORAGE_KEY);
  }
}

/**
 * Checks if a JWT token is expired by examining its payload.
 *
 * This provides a client-side check to avoid unnecessary API calls
 * with expired tokens. The backend ALWAYS validates tokens, so this
 * is an optimization, not a security measure.
 *
 * Security note:
 * - This check is for UX optimization only
 * - Backend validation is the authoritative security check
 * - Expired tokens are rejected by backend with 401
 *
 * @param token - JWT token string
 * @returns true if token is expired or invalid, false otherwise
 */
function isTokenExpired(token: string): boolean {
  try {
    // JWT format: header.payload.signature
    const parts = token.split('.');
    if (parts.length !== 3) {
      return true; // Malformed token
    }

    // Decode payload (base64url)
    const payload = JSON.parse(atob(parts[1].replace(/-/g, '+').replace(/_/g, '/')));

    if (!payload.exp) {
      return false; // No expiration claim, let backend decide
    }

    // Check if token is expired (exp is in seconds, Date.now() is in milliseconds)
    const now = Math.floor(Date.now() / 1000);
    return payload.exp < now;
  } catch (error) {
    // If we can't decode the token, treat it as expired
    return true;
  }
}

export class ApiClient {
  private baseUrl: string;
  private token: string | null = null;

  constructor(baseUrl: string = API_URL) {
    this.baseUrl = baseUrl;
  }

  /**
   * Manually set authentication token.
   *
   * This is primarily for testing or special cases where the token
   * needs to be set explicitly. In most cases, tokens are automatically
   * retrieved from Better Auth cookies.
   *
   * @param token - JWT access token or null to clear
   */
  setToken(token: string | null) {
    this.token = token;
  }

  /**
   * Makes an authenticated request to the FastAPI backend.
   *
   * This method automatically:
   * 1. Retrieves JWT token from Better Auth session cookies
   * 2. Checks if token is expired (client-side optimization)
   * 3. Attaches token to Authorization header
   * 4. Sends request to backend with timeout
   * 5. Intercepts 401 responses and redirects to signin
   * 6. Handles response and errors
   *
   * Security:
   * - JWT token is automatically attached to all requests
   * - Client-side expiration check prevents unnecessary API calls
   * - 401 responses trigger automatic redirect to signin page
   * - Manual token (via setToken) takes precedence over cookie token
   * - Backend must validate token on protected endpoints
   * - Errors don't leak sensitive information
   *
   * @param endpoint - API endpoint path (e.g., "/api/tasks")
   * @param options - Fetch options (method, body, headers, etc.)
   * @returns Promise resolving to typed response data
   * @throws Error with user-friendly message on failure
   */
  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
      ...(options.headers as Record<string, string>),
    };

    // Automatically attach JWT token from Better Auth session
    // Manual token (via setToken) takes precedence
    const token = this.token || getAccessToken();

    // Client-side token expiration check before API request
    // This is an optimization to avoid unnecessary API calls with expired tokens
    // Backend validation is still the authoritative security check
    if (token && isTokenExpired(token)) {
      redirectToSignin();
      throw new Error('Session expired. Please sign in again.');
    }

    // Attach Authorization header with Bearer token
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    // Set up timeout with AbortController
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), REQUEST_TIMEOUT);

    try {
      const response = await fetch(`${this.baseUrl}${endpoint}`, {
        ...options,
        headers,
        credentials: 'include', // Include cookies for Better Auth
        signal: controller.signal,
      });

      clearTimeout(timeoutId);

      // Intercept 401 responses and redirect to signin
      if (response.status === 401) {
        redirectToSignin();
        throw new Error('Authentication required. Redirecting to sign in...');
      }

      // Handle no content response (e.g., DELETE)
      if (response.status === 204) {
        return null as T;
      }

      if (!response.ok) {
        const error = await response.json().catch(() => ({
          detail: 'An error occurred',
        }));
        throw new Error(error.detail || error.message || `HTTP ${response.status}`);
      }

      return response.json();
    } catch (error) {
      clearTimeout(timeoutId);

      if (error instanceof Error && error.name === 'AbortError') {
        throw new Error('Request timed out. Please try again.');
      }

      throw error;
    }
  }

  async get<T>(endpoint: string): Promise<T> {
    return this.request<T>(endpoint, { method: 'GET' });
  }

  async post<T>(endpoint: string, data?: unknown): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'POST',
      body: data ? JSON.stringify(data) : undefined,
    });
  }

  async put<T>(endpoint: string, data?: unknown): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'PUT',
      body: data ? JSON.stringify(data) : undefined,
    });
  }

  async delete<T>(endpoint: string): Promise<T> {
    return this.request<T>(endpoint, { method: 'DELETE' });
  }

  async patch<T>(endpoint: string, data?: unknown): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'PATCH',
      body: data ? JSON.stringify(data) : undefined,
    });
  }
}

export const apiClient = new ApiClient();

/**
 * Task API functions for CRUD operations.
 *
 * These functions provide a typed interface for all task-related
 * API calls, ensuring consistent error handling and response parsing.
 */
export const taskApi = {
  /**
   * Fetch all tasks for the authenticated user.
   * @returns Array of tasks
   */
  list: (): Promise<Task[]> => apiClient.get<Task[]>('/api/tasks'),

  /**
   * Fetch a single task by ID.
   * @param id - Task UUID
   * @returns Task object
   */
  get: (id: string): Promise<Task> => apiClient.get<Task>(`/api/tasks/${id}`),

  /**
   * Create a new task.
   * @param data - Task creation data (description)
   * @returns Created task object
   */
  create: (data: TaskCreate): Promise<Task> =>
    apiClient.post<Task>('/api/tasks', data),

  /**
   * Update an existing task.
   * @param id - Task UUID
   * @param data - Task update data (description)
   * @returns Updated task object
   */
  update: (id: string, data: TaskUpdate): Promise<Task> =>
    apiClient.put<Task>(`/api/tasks/${id}`, data),

  /**
   * Delete a task.
   * @param id - Task UUID
   */
  delete: (id: string): Promise<void> =>
    apiClient.delete<void>(`/api/tasks/${id}`),

  /**
   * Toggle task completion status.
   * @param id - Task UUID
   * @returns Updated task object with toggled is_completed
   */
  toggle: (id: string): Promise<Task> =>
    apiClient.patch<Task>(`/api/tasks/${id}/toggle`),
};

/**
 * Auth response types for FastAPI backend.
 */
export interface AuthUser {
  id: string;
  email: string;
  created_at: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: AuthUser;
}

export interface SignupData {
  email: string;
  password: string;
}

export interface SigninData {
  email: string;
  password: string;
}

/**
 * Auth API functions for signup and signin.
 *
 * These functions communicate with the FastAPI backend auth endpoints
 * and handle JWT token storage.
 */
export const authApi = {
  /**
   * Register a new user account.
   * Stores JWT token on success.
   * @param data - User registration data (email, password)
   * @returns Auth response with token and user
   */
  signup: async (data: SignupData): Promise<AuthResponse> => {
    const response = await fetch(`${API_URL}/auth/signup`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Signup failed' }));
      throw new Error(error.detail || 'Signup failed');
    }

    const result: AuthResponse = await response.json();
    setAccessToken(result.access_token);
    return result;
  },

  /**
   * Sign in an existing user.
   * Stores JWT token on success.
   * @param data - User login data (email, password)
   * @returns Auth response with token and user
   */
  signin: async (data: SigninData): Promise<AuthResponse> => {
    const response = await fetch(`${API_URL}/auth/signin`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Signin failed' }));
      throw new Error(error.detail || 'Signin failed');
    }

    const result: AuthResponse = await response.json();
    setAccessToken(result.access_token);
    return result;
  },

  /**
   * Sign out the current user.
   * Clears JWT token from storage.
   */
  signout: (): void => {
    clearAccessToken();
  },

  /**
   * Check if user is authenticated.
   * @returns true if JWT token exists and is not expired
   */
  isAuthenticated: (): boolean => {
    const token = getAccessToken();
    if (!token) return false;
    return !isTokenExpired(token);
  },
};
