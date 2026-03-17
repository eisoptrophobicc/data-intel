// app/api/claude/route.js
// Server-side proxy — keeps your API key off the client

export async function POST(req) {
  const body = await req.json();

  const res = await fetch("http://127.0.0.1:8000/query", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      question: body.question,
      mode: body.mode
    }),
  });

  const data = await res.json();

  return Response.json(data);
}