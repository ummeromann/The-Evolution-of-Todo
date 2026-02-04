"use client";

import { useState, useEffect } from "react";
import { chatApi, ConversationSummary } from "@/lib/chat-api";
import { Button } from "@/components/ui/button";

interface ConversationListProps {
  currentConversationId?: string | null;
  onSelectConversation: (id: string | null) => void;
  onNewConversation: () => void;
}

/**
 * Sidebar component for listing and managing conversations.
 *
 * Features:
 * - List all user conversations
 * - Select a conversation to continue
 * - Start a new conversation
 * - Delete conversations
 * - Shows message count and last updated time
 */
export function ConversationList({
  currentConversationId,
  onSelectConversation,
  onNewConversation,
}: ConversationListProps) {
  const [conversations, setConversations] = useState<ConversationSummary[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Load conversations on mount
  useEffect(() => {
    loadConversations();
  }, []);

  const loadConversations = async () => {
    try {
      setIsLoading(true);
      setError(null);
      const response = await chatApi.listConversations(50, 0);
      setConversations(response.conversations);
    } catch (err) {
      setError("Failed to load conversations");
      console.error("Failed to load conversations:", err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleDelete = async (id: string, e: React.MouseEvent) => {
    e.stopPropagation(); // Prevent selecting the conversation

    if (!confirm("Delete this conversation?")) {
      return;
    }

    // Optimistically remove from UI first
    setConversations((prev) => prev.filter((c) => c.id !== id));

    // If we deleted the current conversation, start a new one immediately
    if (currentConversationId === id) {
      onNewConversation();
    }

    try {
      await chatApi.deleteConversation(id);
    } catch (err) {
      // Ignore 404 errors - conversation already deleted
      const errorMessage = err instanceof Error ? err.message : String(err);
      if (!errorMessage.includes("not found") && !errorMessage.includes("404")) {
        console.error("Failed to delete conversation:", err);
        // Reload the list to get the correct state
        loadConversations();
      }
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diff = now.getTime() - date.getTime();
    const days = Math.floor(diff / (1000 * 60 * 60 * 24));

    if (days === 0) {
      return date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
    } else if (days === 1) {
      return "Yesterday";
    } else if (days < 7) {
      return date.toLocaleDateString([], { weekday: "short" });
    } else {
      return date.toLocaleDateString([], { month: "short", day: "numeric" });
    }
  };

  const getConversationTitle = (conv: ConversationSummary) => {
    if (conv.title) {
      return conv.title;
    }
    return `Conversation ${formatDate(conv.created_at)}`;
  };

  return (
    <div className="flex flex-col h-full">
      {/* Header */}
      <div className="p-3 border-b border-border">
        <Button
          onClick={onNewConversation}
          className="w-full"
          variant="outline"
        >
          + New Chat
        </Button>
      </div>

      {/* Conversation list */}
      <div className="flex-1 overflow-y-auto">
        {isLoading && (
          <div className="p-4 text-center text-muted-foreground text-sm">
            Loading...
          </div>
        )}

        {error && (
          <div className="p-4 text-center text-destructive text-sm">
            {error}
            <button
              onClick={loadConversations}
              className="block mx-auto mt-2 underline"
            >
              Retry
            </button>
          </div>
        )}

        {!isLoading && !error && conversations.length === 0 && (
          <div className="p-4 text-center text-muted-foreground text-sm">
            No conversations yet.
            <br />
            Start chatting to create one!
          </div>
        )}

        {conversations.map((conv) => (
          <div
            key={conv.id}
            onClick={() => onSelectConversation(conv.id)}
            className={`p-3 border-b border-border cursor-pointer hover:bg-muted/50 transition-colors ${
              currentConversationId === conv.id ? "bg-muted" : ""
            }`}
          >
            <div className="flex justify-between items-start gap-2">
              <div className="flex-1 min-w-0">
                <p className="font-medium text-sm truncate">
                  {getConversationTitle(conv)}
                </p>
                <p className="text-xs text-muted-foreground mt-1">
                  {conv.message_count} messages · {formatDate(conv.updated_at)}
                </p>
              </div>
              <button
                onClick={(e) => handleDelete(conv.id, e)}
                className="text-muted-foreground hover:text-destructive p-1 rounded"
                title="Delete conversation"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="14"
                  height="14"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                >
                  <path d="M3 6h18" />
                  <path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6" />
                  <path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2" />
                </svg>
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* Refresh button */}
      <div className="p-3 border-t border-border">
        <button
          onClick={loadConversations}
          className="w-full text-xs text-muted-foreground hover:text-foreground"
        >
          Refresh list
        </button>
      </div>
    </div>
  );
}
