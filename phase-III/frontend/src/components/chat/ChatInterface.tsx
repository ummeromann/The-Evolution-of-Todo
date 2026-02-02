"use client";

import { useState, useEffect } from "react";
import { ChatInput } from "./ChatInput";
import { MessageList, Message } from "./MessageList";
import { chatApi } from "@/lib/chat-api";

interface ChatInterfaceProps {
  conversationId?: string | null;
  onConversationCreated?: (id: string) => void;
}

/**
 * Main chat interface component.
 *
 * Features:
 * - Display message history via MessageList
 * - Send messages to AI assistant
 * - Auto-scroll to latest message
 * - Loading states during AI processing
 * - Error handling with user-friendly messages
 * - Conversation persistence
 */
export function ChatInterface({
  conversationId: initialConversationId,
  onConversationCreated,
}: ChatInterfaceProps) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [conversationId, setConversationId] = useState<string | null>(
    initialConversationId || null
  );
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Load existing conversation if ID provided
  useEffect(() => {
    if (initialConversationId) {
      loadConversation(initialConversationId);
    }
  }, [initialConversationId]);

  const loadConversation = async (id: string) => {
    try {
      setIsLoading(true);
      setError(null);
      const conversation = await chatApi.getConversation(id);
      setConversationId(id);
      setMessages(
        conversation.messages
          .filter((m) => m.role === "user" || m.role === "assistant")
          .map((m) => ({
            id: m.id,
            role: m.role as "user" | "assistant",
            content: m.content,
            timestamp: new Date(m.created_at),
          }))
      );
    } catch (err) {
      setError("Failed to load conversation. Please try again.");
      console.error("Failed to load conversation:", err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSend = async (message: string) => {
    // Add user message immediately for responsiveness
    const userMessage: Message = {
      id: `temp-${Date.now()}`,
      role: "user",
      content: message,
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);
    setError(null);

    try {
      const response = await chatApi.sendMessage(message, conversationId);

      // Update conversation ID if this is a new conversation
      if (!conversationId && response.conversation_id) {
        setConversationId(response.conversation_id);
        onConversationCreated?.(response.conversation_id);
      }

      // Add assistant response
      const assistantMessage: Message = {
        id: `assistant-${Date.now()}`,
        role: "assistant",
        content: response.message,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, assistantMessage]);
    } catch (err) {
      // Remove the optimistic user message on error
      setMessages((prev) => prev.filter((m) => m.id !== userMessage.id));

      const errorMessage =
        err instanceof Error ? err.message : "Failed to send message";
      setError(errorMessage);
      console.error("Chat error:", err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleDismissError = () => {
    setError(null);
  };

  return (
    <div className="flex flex-col h-full">
      {/* Messages area */}
      <MessageList
        messages={messages}
        isLoading={isLoading}
        error={error}
        onDismissError={handleDismissError}
      />

      {/* Input area */}
      <div className="border-t border-border p-4 bg-background">
        <ChatInput
          onSend={handleSend}
          disabled={isLoading}
          placeholder="Ask me to help with your todos..."
        />
      </div>
    </div>
  );
}
