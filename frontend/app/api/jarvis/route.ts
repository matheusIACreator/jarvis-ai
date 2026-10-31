export const dynamic = "force-dynamic"
async function proxy(request: Request) {
  const url = new URL(request.url)
  const host = request.headers.get("host") || ""
  if (!/^(localhost|127\.0\.0\.1):\d+$/.test(host))
    return Response.json({ error: "Acesso local apenas" }, { status: 403 })
  const origin = request.headers.get("origin")
  if (origin && origin !== `http://${host}`)
    return Response.json({ error: "Origem inválida" }, { status: 403 })
  const resource = url.searchParams.get("resource") || "state"
  if (
    !(request.method === "GET" ? ["state", "memory"] : ["chat"]).includes(
      resource
    )
  )
    return new Response(null, { status: 404 })
  try {
    let body: string | undefined
    if (request.method === "POST") {
      if (Number(request.headers.get("content-length")) > 20000)
        return new Response(null, { status: 413 })
      body = await request.text()
      if (body.length > 20000) return new Response(null, { status: 413 })
    }
    const response = await fetch(
      `http://127.0.0.1:8765/${resource}?q=${encodeURIComponent(url.searchParams.get("q") || "")}`,
      {
        method: request.method,
        body,
        headers: { "Content-Type": "application/json" },
        cache: "no-store",
        signal: AbortSignal.timeout(request.method === "POST" ? 120000 : 3000),
      }
    )
    return new Response(await response.text(), {
      status: response.status,
      headers: {
        "Content-Type": "application/json",
        "Cache-Control": "no-store",
      },
    })
  } catch {
    return Response.json(
      { error: "Jarvis desconectado. Inicie o serviço Python para continuar." },
      { status: 503 }
    )
  }
}
export const GET = proxy
export const POST = proxy
