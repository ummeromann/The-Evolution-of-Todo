"use client";

import { useRef, useEffect } from "react";

export interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
}

interface MessageListProps {
  messages: Message[];
  isLoading?: boolean;
  error?: string | null;
  onDismissError?: () => void;
}

/**
 * Message list component for displaying chat history.
 *
 * Features:
 * - Renders user and assistant messages with distinct styling
 * - Auto-scrolls to latest message
 * - Shows loading indicator during AI processing
 * - Displays error messages with dismiss option
 * - Empty state with helpful suggestions
 */
export function MessageList({
  messages,
  isLoading = false,
  error = null,
  onDismissError,
}: MessageListProps) {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading]);

  return (
    <div className="flex-1 overflow-y-auto p-4 space-y-4">
      {/* Empty state */}
      {messages.length === 0 && !isLoading && (
        <div className="text-center text-muted-foreground py-12">
          <div className="text-4xl mb-4">💬</div>
          <h3 className="text-lg font-medium mb-2">Start a conversation</h3>
          <p className="text-sm max-w-md mx-auto">
            Ask me to help manage your todos. Try saying:
            <br />
            <span className="text-foreground font-medium">"Add a task to buy groceries"</span>
            <br />
            <span className="text-foreground font-medium">"Show me my tasks"</span>
            <br />
            <span className="text-foreground font-medium">"Mark groceries as done"</span>
          </p>
        </div>
      )}

      {/* Message list */}
      {messages.map((message) => (
        <MessageBubble key={message.id} message={message} />
      ))}

      {/* Loading indicator */}
      {isLoading && (
        <div className="flex justify-start">
          <div className="bg-muted rounded-lg px-4 py-3">
            <div className="flex items-center gap-2">
              <div className="flex gap-1">
                <span
                  className="w-2 h-2 bg-muted-foreground rounded-full animate-bounce"
                  style={{ animationDelay: "0ms" }}
                />
                <span
                  className="w-2 h-2 bg-muted-foreground rounded-full animate-bounce"
                  style={{ animationDelay: "150ms" }}
                />
                <span
                  className="w-2 h-2 bg-muted-foreground rounded-full animate-bounce"
                  style={{ animationDelay: "300ms" }}
                />
              </div>
              <span className="text-sm text-muted-foreground">Thinking...</span>
            </div>
          </div>
        </div>
      )}

      {/* Error message */}
      {error && (
        <div className="flex justify-center">
          <div className="bg-destructive/10 text-destructive rounded-lg px-4 py-3 max-w-md">
            <p className="text-sm">{error}</p>
            {onDismissError && (
              <button
                onClick={onDismissError}
                className="text-xs underline mt-1"
              >
                Dismiss
              </button>
            )}
          </div>
        </div>
      )}

      {/* Scroll anchor */}
      <div ref={messagesEndRef} />
    </div>
  );
}

/**
 * Individual message bubble component.
 */
function MessageBubble({ message }: { message: Message }) {
  const isUser = message.role === "user";

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"}`}>
      <div
        className={`max-w-[80%] rounded-lg px-4 py-3 ${
          isUser
            ? "bg-primary text-primary-foreground"
            : "bg-muted text-foreground"
        }`}
      >
        {/* Message content with markdown-like formatting */}
        <div className="whitespace-pre-wrap">
          {formatMessageContent(message.content)}
        </div>

        {/* Timestamp */}
        <p
          className={`text-xs mt-1 ${
            isUser ? "text-primary-foreground/70" : "text-muted-foreground"
          }`}
        >
          {message.timestamp.toLocaleTimeString([], {
            hour: "2-digit",
            minute: "2-digit",
          })}
        </p>
      </div>
    </div>
  );
}

/**
 * Format message content for display.
 * Handles task lists with checkmarks.
 */
function formatMessageContent(content: string): React.ReactNode {
  // Split by lines and format
  const lines = content.split("\n");

  return lines.map((line, index) => {
    // Check for completed task pattern (✓ or [x])
    if (line.match(/^[\d]+\.\s*[✓✔☑\[x\]]/i)) {
      return (
        <span key={index} className="block text-green-600 dark:text-green-400">
          {line}
          {index < lines.length - 1 && "\n"}
        </span>
      );
    }

    // Check for incomplete task pattern
    if (line.match(/^[\d]+\.\s*[☐\[\s\]]/)) {
      return (
        <span key={index} className="block">
          {line}
          {index < lines.length - 1 && "\n"}
        </span>
      );
    }

    // Regular line
    return (
      <span key={index}>
        {line}
        {index < lines.length - 1 && "\n"}
      </span>
    );
  });
}
