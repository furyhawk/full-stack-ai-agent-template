"use client";

import { ChatContainer, ConversationSidebar } from "@/components/chat";
{%- if cookiecutter.enable_teams and cookiecutter.enable_rag %}
import { KBPanel } from "@/components/chat";
{%- endif %}

export default function ChatPage() {
  // The ?id= query param is read by useConversations.fetchConversations on mount;
  // it sets currentConversationId AND loads messages atomically. Pre-setting the
  // id here would short-circuit that loader and leave the chat empty on refresh.
  return (
    <div className="-m-3 flex min-h-0 flex-1 sm:-m-6">
      <ConversationSidebar />
      <div className="flex min-w-0 flex-1 flex-col">
        <div className="flex min-h-0 flex-1">
          <div className="min-w-0 flex-1">
            <ChatContainer />
          </div>
{%- if cookiecutter.enable_teams and cookiecutter.enable_rag %}
          <KBPanel />
{%- endif %}
        </div>
      </div>
    </div>
  );
}
