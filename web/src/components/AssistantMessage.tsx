import React from "react";
import type { QueryResponse } from "../lib/api";

type Props = {
  response: QueryResponse;
};

function renderDataTable(data: Array<Record<string, any>>) {
  if (!data || data.length === 0) return <div className="meta">Sem dados.</div>;
  const keys = Object.keys(data[0]);
  return (
    <div className="mt-3">
      <table className="data-table">
        <thead>
          <tr>
            {keys.map((k) => (
              <th key={k}>{k}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((row, idx) => (
            <tr key={idx}>
              {keys.map((k) => (
                <td key={k + idx}>{String(row[k] ?? "")}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default function AssistantMessage({ response }: Props) {
  function escapeHtml(s: string) {
    return s
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }

  function mdToHtml(s: string) {
    // Very small markdown-like replacements: bold **text** -> <strong>text</strong>
    let out = escapeHtml(s);
    // replace **bold** (greedy minimal)
    out = out.replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");
    // replace inline `code`
    out = out.replace(/`([^`]+?)`/g, "<code>$1</code>");
    // preserve single line breaks inside paragraph
    out = out.replace(/\n/g, "<br/>");
    return out;
  }

  return (
    <div className="assistant-bubble">
      <div className="prose">
        {/* Analysis: keep paragraphs and render basic markdown (bold, inline code) */}
        {response.analysis ? (
          response.analysis
            .split(/\n\n+/)
            .map((p, i) => (
              <p
                key={i}
                className="mb-2"
                dangerouslySetInnerHTML={{ __html: mdToHtml(p) }}
              />
            ))
        ) : (
          <p className="mb-2">Nenhuma análise disponível.</p>
        )}

        <div className="mt-3">
          <div className="text-sm font-medium mb-2">SQL gerado:</div>
          <pre className="sql-block">{response.sql}</pre>
        </div>

        <div className="mt-3">
          <div className="text-sm font-medium">Rows: {response.row_count}</div>
          {renderDataTable(response.data)}
        </div>
      </div>
    </div>
  );
}
