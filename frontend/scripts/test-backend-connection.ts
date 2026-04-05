const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL ?? "http://127.0.0.1:8000"

export {}

type EndpointCheck = {
  ok: boolean
  status: number
  body: string
}

async function check(path: string): Promise<EndpointCheck> {
  const response = await fetch(`${backendUrl}${path}`, {
    cache: "no-store",
  })

  return {
    ok: response.ok,
    status: response.status,
    body: await response.text(),
  }
}

async function main() {
  console.log(`Testing backend at ${backendUrl}`)

  const health = await check("/api/health")
  const db = await check("/api/db-check")

  console.log(`health_status=${health.status}`)
  console.log(`health_body=${health.body}`)
  console.log(`db_status=${db.status}`)
  console.log(`db_body=${db.body}`)

  if (!health.ok || !db.ok) {
    process.exitCode = 1
    throw new Error("Backend/frontend communication test failed.")
  }

  console.log("Backend/frontend communication test passed.")
}

await main()
