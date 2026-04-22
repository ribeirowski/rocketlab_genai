import React, { useState } from "react";
import ChatMessage from "./ChatMessage";
import AssistantMessage from "./AssistantMessage";
import LoadingSkeleton from "./LoadingSkeleton";
import { queryAgent, type QueryResponse } from "../lib/api";

type UserMessage = { role: "user"; text: string };
type AssistantMsg = { role: "assistant"; response: QueryResponse };
type Message = UserMessage | AssistantMsg;

export default function Chat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSend() {
    if (!input.trim()) return;
    const question = input.trim();
    setMessages((m) => [...m, { role: "user", text: question }]);
    setInput("");
    setLoading(true);
    setError(null);
    try {
      const res = await queryAgent(question);
      setMessages((m) => [...m, { role: "assistant", response: res }]);
    } catch (err: any) {
      setError(err?.message ?? String(err));
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="page-center app-bg">
      <div className="card">
        <div className="card-body">
          <div className="flex items-center justify-between mb-4">
            <h1 className="text-xl font-bold">RocketLab Agent Chat</h1>
          </div>

          <div className="chat-scroll">
            {messages.map((m, idx) =>
              m.role === "user" ? (
                <div key={idx} className="flex justify-end">
                  <div className="user-bubble">
                    <div>{m.text}</div>
                  </div>
                </div>
              ) : (
                <div key={idx} className="flex justify-start">
                  <AssistantMessage response={m.response} />
                </div>
              ),
            )}
            {loading && (
              <div className="flex justify-start">
                <LoadingSkeleton />
              </div>
            )}
          </div>

          {error && <div className="text-red-600 mb-2">{error}</div>}

          <div className="input-row">
            <input
              className="rounded-input"
              placeholder="Faça uma pergunta sobre os dados..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter" && !e.shiftKey) {
                  e.preventDefault();
                  handleSend();
                }
              }}
            />
            <button
              className="btn-primary"
              onClick={handleSend}
              disabled={loading}
            >
              {loading ? "Enviando..." : "Enviar"}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
