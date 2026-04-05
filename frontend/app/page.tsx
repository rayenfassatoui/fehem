import { BackendConnectionCheck } from "@/components/backend-connection-check"
import { Button } from "@/components/ui/button"

export default function Page() {
  return (
    <main className="flex min-h-svh w-full justify-center p-6 md:p-10">
      <div className="flex w-full max-w-3xl min-w-0 flex-col gap-6 text-sm leading-loose">
        <div className="space-y-2">
          <h1 className="text-xl font-semibold">Fehem Local Connectivity</h1>
          <p className="text-muted-foreground">
            Frontend is wired to backend health and Neon database checks.
          </p>
          <Button variant="outline">UI Ready</Button>
        </div>
        <div className="font-mono text-xs text-muted-foreground">
          (Press <kbd>d</kbd> to toggle dark mode)
        </div>
        <BackendConnectionCheck />
      </div>
    </main>
  )
}
