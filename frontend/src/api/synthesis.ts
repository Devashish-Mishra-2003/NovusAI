export async function callSynthesis(message: string, conversationId?: string) {
  const res = await fetch("http://127.0.0.1:8000/api/synthesize", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      message,
      conversation_id: conversationId ?? null,
    }),
  });

  if (!res.ok) {
    throw new Error("Synthesis request failed");
  }

  return res.json();
}
