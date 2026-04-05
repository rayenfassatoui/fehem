const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL ?? "http://127.0.0.1:8000"

export {}

async function main() {
  console.log(`Testing semantic pgvector flow at ${backendUrl}`)

  const upsertResponse = await fetch(`${backendUrl}/api/ai/semantic-documents`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      id: "chunk-intro",
      content: "Fehem helps students and teachers learn faster with AI.",
      embedding: [0.11, 0.22, 0.33],
      metadata: {
        topic: "intro",
        source: "local-test",
      },
    }),
  })

  const upsertBody = await upsertResponse.text()
  console.log(`semantic_upsert_status=${upsertResponse.status}`)
  console.log(`semantic_upsert_body=${upsertBody}`)

  if (!upsertResponse.ok) {
    process.exitCode = 1
    throw new Error("Semantic upsert failed.")
  }

  const searchResponse = await fetch(`${backendUrl}/api/ai/semantic-search`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      query_embedding: [0.11, 0.22, 0.33],
      top_k: 3,
    }),
  })

  const searchBody = await searchResponse.text()
  console.log(`semantic_search_status=${searchResponse.status}`)
  console.log(`semantic_search_body=${searchBody}`)

  if (!searchResponse.ok) {
    process.exitCode = 1
    throw new Error("Semantic search failed.")
  }

  const parsed = JSON.parse(searchBody) as {
    count?: number
    matches?: Array<{ id?: string }>
  }

  if (!parsed.count || !parsed.matches?.length) {
    process.exitCode = 1
    throw new Error("Semantic search returned no results.")
  }

  console.log("Semantic pgvector flow passed.")
}

await main()
