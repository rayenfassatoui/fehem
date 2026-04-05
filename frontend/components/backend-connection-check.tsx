"use client"

import * as React from "react"

import { Button } from "@/components/ui/button"

type CheckState = {
  status: "idle" | "loading" | "ok" | "error"
  message: string
}

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL ?? "http://localhost:8000"

function StatusRow({
  label,
  state,
}: {
  label: string
  state: CheckState
}) {
  const colorClass =
    state.status === "ok"
      ? "bg-emerald-500"
      : state.status === "error"
        ? "bg-red-500"
        : state.status === "loading"
          ? "bg-amber-500"
          : "bg-muted-foreground"

  return (
    <div className="flex items-center gap-3 rounded-lg border border-border p-3">
      <span className={`size-2 rounded-full ${colorClass}`} />
      <div className="min-w-0 flex-1">
        <p className="text-xs font-semibold uppercase tracking-wide text-muted-foreground">
          {label}
        </p>
        <p className="truncate text-sm">{state.message}</p>
      </div>
    </div>
  )
}

export function BackendConnectionCheck() {
  const [apiState, setApiState] = React.useState<CheckState>({
    status: "idle",
    message: "Not checked yet.",
  })
  const [dbState, setDbState] = React.useState<CheckState>({
    status: "idle",
    message: "Not checked yet.",
  })
  const [lastCheckedAt, setLastCheckedAt] = React.useState<string>("-")

  const runCheck = React.useCallback(async () => {
    setApiState({ status: "loading", message: "Checking backend health..." })
    setDbState({ status: "loading", message: "Checking Neon PostgreSQL..." })

    try {
      const response = await fetch(`${BACKEND_URL}/api/health`, {
        cache: "no-store",
      })

      if (!response.ok) {
        throw new Error(`Backend health failed with status ${response.status}.`)
      }

      const payload = (await response.json()) as { status?: string; service?: string }

      setApiState({
        status: payload.status === "ok" ? "ok" : "error",
        message:
          payload.status === "ok"
            ? `Connected to ${payload.service ?? "backend"}.`
            : "Backend responded with unexpected payload.",
      })
    } catch (error) {
      const message = error instanceof Error ? error.message : "Unknown backend error."
      setApiState({ status: "error", message })
    }

    try {
      const response = await fetch(`${BACKEND_URL}/api/db-check`, {
        cache: "no-store",
      })
      const payload = (await response.json()) as {
        database?: string
        detail?: string
      }

      if (response.ok && payload.database === "connected") {
        setDbState({ status: "ok", message: payload.detail ?? "Database connected." })
      } else {
        setDbState({
          status: "error",
          message: payload.detail ?? `Database check failed with status ${response.status}.`,
        })
      }
    } catch (error) {
      const message = error instanceof Error ? error.message : "Unknown database error."
      setDbState({ status: "error", message })
    }

    setLastCheckedAt(new Date().toLocaleTimeString())
  }, [])

  React.useEffect(() => {
    void runCheck()
  }, [runCheck])

  return (
    <section className="w-full max-w-2xl space-y-4 rounded-2xl border border-border bg-card p-5 text-card-foreground">
      <div className="space-y-2">
        <h2 className="text-base font-semibold">Backend / Frontend Connection Test</h2>
        <p className="text-xs leading-relaxed text-muted-foreground">
          This checks frontend communication with backend API and Neon PostgreSQL.
        </p>
        <p className="text-xs text-muted-foreground">
          Backend URL: <span className="font-mono">{BACKEND_URL}</span>
        </p>
      </div>

      <div className="space-y-2">
        <StatusRow label="API Health" state={apiState} />
        <StatusRow label="Database" state={dbState} />
      </div>

      <div className="flex items-center gap-3">
        <Button onClick={() => void runCheck()}>Re-test connection</Button>
        <span className="text-xs text-muted-foreground">Last check: {lastCheckedAt}</span>
      </div>
    </section>
  )
}
