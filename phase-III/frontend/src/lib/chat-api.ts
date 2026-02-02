/**
 * Chat API client for AI-powered todo management.
 *
 * This module provides typed functions for interacting with the chat endpoints:
 * - Send messages to the AI assistant
 * - List and manage conversations
 * - Handle real-time responses
 */

import { apiClient } from './api';

// ============================================================================
// Types
// ============================================================================

export interface ToolCallRecord {
  tool_name: string;
  parameters: Record<string, unknown>;
  result: Record<string, unknown> | null;
}

export interface ChatRequest {
  message: string;
  conversation_id?: string | null;
}

export interface ChatResponse {
  conversation_id: string;
  message: string;
  tool_calls: ToolCallRecord[];
}

export interface ConversationSummary {
  id: string;
  title: string | null;
  created_at: string;
  updated_at: string;
  message_count: number;
}

export interface ConversationListResponse {
  conversations: ConversationSummary[];
  total: number;
}

export interface MessageResponse {
  id: string;
  role: 'user' | 'assistant' | 'tool';
  content: string;
  tool_call_id: string | null;
  created_at: string;
}

export interface ConversationDetailResponse {
  id: string;
  title: string | null;
  messages: MessageResponse[];
  created_at: string;
  updated_at: string;
}

// ============================================================================
// Chat API Functions
// ============================================================================

export const chatApi = {
  /**
   * Send a message to the AI assistant.
   *
   * Creates a new conversation if conversation_id is not provided.
   *
   * @param message - Natural language message
   * @param conversationId - Optional existing conversation ID
   * @returns Chat response with assistant's reply and tool calls
   */
  sendMessage: async (
    message: string,
    conversationId?: string | null
  ): Promise<ChatResponse> => {
    const request: ChatRequest = {
      message,
      conversation_id: conversationId || null,
    };
    return apiClient.post<ChatResponse>('/api/chat', request);
  },

  /**
   * List all conversations for the authenticated user.
   *
   * @param limit - Maximum number of conversations (default 20)
   * @param offset - Number to skip (default 0)
   * @returns List of conversation summaries
   */
  listConversations: async (
    limit: number = 20,
    offset: number = 0
  ): Promise<ConversationListResponse> => {
    return apiClient.get<ConversationListResponse>(
      `/api/conversations?limit=${limit}&offset=${offset}`
    );
  },

  /**
   * Get a specific conversation with all messages.
   *
   * @param conversationId - Conversation UUID
   * @returns Full conversation with message history
   */
  getConversation: async (
    conversationId: string
  ): Promise<ConversationDetailResponse> => {
    return apiClient.get<ConversationDetailResponse>(
      `/api/conversations/${conversationId}`
    );
  },

  /**
   * Delete a conversation and all its messages.
   *
   * @param conversationId - Conversation UUID
   */
  deleteConversation: async (conversationId: string): Promise<void> => {
    return apiClient.delete<void>(`/api/conversations/${conversationId}`);
  },
};
