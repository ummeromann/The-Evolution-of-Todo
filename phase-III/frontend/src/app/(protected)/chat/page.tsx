"use client";

import { useState, useCallback } from "react";
import { ChatInterface } from "@/components/chat/ChatInterface";
import { ConversationList } from "@/components/chat/ConversationList";

/**
 * Chat page for AI-powered todo management.
 *
 * This page provides a conversational interface for users to:
 * - Add tasks using natural language
 * - View their todo list
 * - Complete, update, or delete tasks
 * - Get help and suggestions from the AI
 * - Resume previous conversations
 *
 * The conversation persists across page reloads via the backend API.
 */
export default function ChatPage() {
  const [conversationId, setConversationId] = useState<string | null>(null);
  const [refreshKey, setRefreshKey] = useState(0);

  const handleSelectConversation = useCallback((id: string | null) => {
    setConversationId(id);
    // Force re-render of ChatInterface to load the conversation
    setRefreshKey((prev) => prev + 1);
  }, []);

  const handleNewConversation = useCallback(() => {
    setConversationId(null);
    setRefreshKey((prev) => prev + 1);
  }, []);

  const handleConversationCreated = useCallback((id: string) => {
    setConversationId(id);
  }, []);

  return (
    <div className="h-[calc(100vh-140px)] flex gap-4">
      {/* Sidebar - Conversation list */}
      <div className="w-64 flex-shrink-0 bg-card rounded-lg border border-border shadow-sm overflow-hidden hidden md:block">
        <ConversationList
          currentConversationId={conversationId}
          onSelectConversation={handleSelectConversation}
          onNewConversation={handleNewConversation}
        />
      </div>

      {/* Main content */}
      <div className="flex-1 flex flex-col min-w-0">
        {/* Page header */}
        <div className="mb-4 flex justify-between items-start">
          <div>
            <h2 className="text-2xl font-bold text-foreground">AI Chat Assistant</h2>
            <p className="text-muted-foreground">
              Manage your todos using natural language
            </p>
          </div>

          {/* Mobile: New chat button */}
          <button
            onClick={handleNewConversation}
            className="md:hidden px-3 py-2 text-sm bg-primary text-primary-foreground rounded-md"
          >
            New Chat
          </button>
        </div>

        {/* Chat interface */}
        <div className="flex-1 bg-card rounded-lg border border-border shadow-sm overflow-hidden">
          <ChatInterface
            key={refreshKey}
            conversationId={conversationId}
            onConversationCreated={handleConversationCreated}
          />
        </div>

        {/* Helper text */}
        <div className="mt-4 text-center text-sm text-muted-foreground">
          <p>
            Try: "Add a task to buy milk" · "Show my todos" · "Mark milk as done"
          </p>
        </div>
      </div>
    </div>
  );
}
