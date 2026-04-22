const API_BASE =
  import.meta.env.VITE_API_BASE || "http://localhost:8000/api/v1";

export type QueryResponse = {
  question_id: number;
  question: string;
  sql: string;
  data: Array<Record<string, any>>;
  analysis: string;
  row_count: number;
};

export async function queryAgent(question: string): Promise<QueryResponse> {
  const res = await fetch(`${API_BASE}/agent/query`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question }),
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(`${res.status} ${res.statusText}: ${text}`);
  }

  return res.json();
}
