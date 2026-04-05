const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL ?? "http://127.0.0.1:8000"

export {}

async function main() {
  console.log(`Testing AI bridge at ${backendUrl}`)

  const response = await fetch(`${backendUrl}/api/ai/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      prompt: "Say hello from Fehem",
      max_tokens: 64,
    }),
  })

  const body = await response.text()

  console.log(`ai_chat_status=${response.status}`)
  console.log(`ai_chat_body=${body}`)

  if (response.status === 200) {
    console.log("AI bridge is working with NVIDIA provider.")
    return
  }

  if (response.status === 503) {
    console.log("AI bridge reached backend, but NVIDIA_API_KEY is not configured yet.")
    return
  }

  process.exitCode = 1
  throw new Error("AI bridge test failed with unexpected status.")
}

await main()
