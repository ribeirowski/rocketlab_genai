import React from "react";

type Props = {
  role: "user" | "assistant";
  text: string;
};

export default function ChatMessage({ role, text }: Props) {
  const isUser = role === "user";
  return (
    <div className="user-bubble">
      <div className="whitespace-pre-wrap">{text}</div>
    </div>
  );
}
