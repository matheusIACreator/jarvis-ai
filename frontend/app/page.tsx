"use client"
import { useEffect, useState, useRef, type FormEvent } from "react"
import {
  Activity,
  ArrowUp,
  AudioLines,
  Brain,
  ChevronRight,
  CircleHelp,
  Cpu,
  Fingerprint,
  Layers,
  MessageSquare,
  Search,
  Sparkles,
  X,
} from "lucide-react"
import { Button } from "@/components/ui/button"
type Message = { role: string; text: string }
type Note = { id: string; content: string }
const labels: Record<string, string> = {
  idle: "À sua disposição",
  starting: "Inicializando",
  listening: "Estou ouvindo",
  thinking: "Conectando ideias",
  speaking: "Falando com você",
  offline: "Aguardando conexão",
}
function Reactor({ phase }: { phase: string }) {
  return (
    <div
      className={`reactor ${phase}`}
      aria-label={`Núcleo Jarvis: ${labels[phase]}`}
    >
      <svg viewBox="0 0 600 600" aria-hidden="true">
        <defs>
          <radialGradient id="glow">
            <stop stopColor="#45ddec" stopOpacity=".15" />
            <stop offset="1" stopColor="#45ddec" stopOpacity="0" />
          </radialGradient>
        </defs>
        <circle cx="300" cy="300" r="290" fill="url(#glow)" />
        <g className="orbit slow">
          <circle
            cx="300"
            cy="300"
            r="265"
            className="hair"
            strokeDasharray="1 12"
          />
          {Array.from({ length: 36 }, (_, i) => (
            <g key={i} transform={`rotate(${i * 10} 300 300)`}>
              <line
                x1="300"
                y1="28"
                x2="300"
                y2={i % 3 === 0 ? 45 : 34}
                className="tick"
              />
              <circle cx="300" cy="45" r="1.5" fill="#a1e8ee" />
            </g>
          ))}
        </g>
        <g className="orbit">
          <circle
            cx="300"
            cy="300"
            r="236"
            className="ring"
            strokeWidth="4"
            strokeDasharray="360 25 90 16 210 38"
          />
          <circle cx="300" cy="300" r="228" className="hair" />
          {Array.from({ length: 72 }, (_, i) => (
            <line
              key={i}
              x1="300"
              y1="84"
              x2="300"
              y2={i % 6 === 0 ? 103 : 94}
              transform={`rotate(${i * 5} 300 300)`}
              className="tick"
            />
          ))}
        </g>
        <g className="orbit reverse">
          <circle
            cx="300"
            cy="300"
            r="195"
            fill="none"
            stroke="#56cbdc"
            strokeOpacity=".25"
            strokeWidth="19"
            strokeDasharray="270 24 300 38"
          />
          <circle
            cx="300"
            cy="300"
            r="178"
            fill="none"
            stroke="#e5cb79"
            strokeWidth="2"
            strokeDasharray="170 950"
          />
          <circle
            cx="300"
            cy="300"
            r="163"
            className="ring"
            strokeWidth="5"
            strokeDasharray="210 15 300 20"
          />
        </g>
        <circle cx="300" cy="300" r="151" className="hair" />
        <g className="particles">
          {Array.from({ length: 260 }, (_, i) => {
            const a = i * 2.39996,
              r = Math.sqrt(i / 260) * 139
            return (
              <circle
                key={i}
                cx={(300 + Math.cos(a) * r).toFixed(3)}
                cy={(300 + Math.sin(a) * r).toFixed(3)}
                r={i % 7 === 0 ? 1.5 : 0.7}
                fill="#9aebf2"
                opacity={0.2 + (i % 5) * 0.13}
              />
            )
          })}
        </g>
        <path
          d="M280 300h12l5-15 7 30 6-15h12"
          fill="none"
          stroke="#b9f9ff"
          strokeWidth="2"
        />
      </svg>
      <span className="core-caption">J.A.R.V.I.S.</span>
    </div>
  )
}
export default function Home() {
  const [phase, setPhase] = useState("offline"),
    [online, setOnline] = useState(false),
    [voice, setVoice] = useState<Message[]>([])
  const [tab, setTab] = useState("core"),
    [messages, setMessages] = useState<Message[]>([]),
    [input, setInput] = useState(""),
    [busy, setBusy] = useState(false),
    [error, setError] = useState("")
  const [notes, setNotes] = useState<Note[]>([]),
    [query, setQuery] = useState(""),
    [memoryError, setMemoryError] = useState(""),
    [selected, setSelected] = useState<Note | null>(null),
    [help, setHelp] = useState(false)
  const bottom = useRef<HTMLDivElement>(null)
  const dialog = useRef<HTMLDialogElement>(null)
  useEffect(() => {
    if (help || selected) dialog.current?.showModal()
    else dialog.current?.close()
  }, [help, selected])
  useEffect(() => {
    let stopped = false
    let timer: ReturnType<typeof setTimeout>
    async function poll() {
      try {
        const r = await fetch("/api/jarvis")
        if (!r.ok) throw Error()
        const d = await r.json()
        if (!stopped) {
          setOnline(true)
          setPhase(d.phase)
          setVoice(d.messages)
        }
      } catch {
        if (!stopped) {
          setOnline(false)
          setPhase("offline")
        }
      }
      if (!stopped) timer = setTimeout(poll, 400)
    }
    poll()
    return () => {
      stopped = true
      clearTimeout(timer)
    }
  }, [])
  useEffect(() => {
    if (tab !== "memory") return
    const controller = new AbortController()
    const timer = setTimeout(async () => {
      try {
        const r = await fetch(
          `/api/jarvis?resource=memory&q=${encodeURIComponent(query)}`,
          { signal: controller.signal }
        )
        if (!r.ok) throw Error()
        setNotes(await r.json())
        setMemoryError("")
      } catch {
        if (!controller.signal.aborted)
          setMemoryError("Conecte o Jarvis para consultar suas memórias.")
      }
    }, 250)
    return () => {
      clearTimeout(timer)
      controller.abort()
    }
  }, [tab, query, online])
  useEffect(() => {
    if (messages.length === 0 && !busy) return
    bottom.current?.scrollIntoView({ behavior: "smooth", block: "nearest" })
  }, [messages, busy])
  async function send(e: FormEvent) {
    e.preventDefault()
    if (!input.trim() || busy) return
    const text = input.trim()
    setInput("")
    setBusy(true)
    setError("")
    setMessages((m) => [...m, { role: "user", text }])
    try {
      const r = await fetch("/api/jarvis?resource=chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text }),
      })
      const d = await r.json()
      if (!r.ok) throw Error(d.error)
      setMessages((m) => [...m, { role: "assistant", text: d.reply }])
    } catch (e) {
      setError(e instanceof Error ? e.message : "Não foi possível enviar.")
      setInput(text)
    } finally {
      setBusy(false)
    }
  }
  const currentPhase = busy ? "thinking" : phase
  return (
    <div className="shell">
      <aside className="rail">
        <a href="/" className="brand-mark" aria-label="Jarvis início">
          J<span>·</span>
        </a>
        <nav>
          {[
            { id: "core", icon: Activity, name: "Núcleo" },
            { id: "chat", icon: MessageSquare, name: "Conversas" },
            { id: "memory", icon: Brain, name: "Memória" },
          ].map(({ id, icon: Icon, name }) => (
            <Button
              key={id}
              variant="ghost"
              className={`rail-button ${tab === id ? "active" : ""}`}
              onClick={() => setTab(id)}
              aria-label={name}
              title={name}
            >
              <Icon size={21} />
            </Button>
          ))}
        </nav>
        <Button
          variant="ghost"
          className="help-button"
          aria-label="Como conectar"
          onClick={() => setHelp(true)}
        >
          <CircleHelp size={20} />
        </Button>
        <div className="avatar">M</div>
      </aside>
      <div className="workspace">
        <header>
          <div className="wordmark">
            J.A.R.V.I.S.<span>PERSONAL INTELLIGENCE</span>
          </div>
          <div className="header-right">
            <span className={`connection ${online ? "connected" : ""}`}>
              <i />
              {online ? "SISTEMA CONECTADO" : "SISTEMA OFFLINE"}
            </span>
            <span className="header-divider" />
            <Fingerprint size={22} />
            <span>Matheus</span>
          </div>
        </header>
        <main>
          <div className="page-heading">
            <div>
              <div className="eyebrow">SEU ESPAÇO DE COMANDO</div>
              <h1>
                {tab === "memory"
                  ? "Memória compartilhada"
                  : tab === "chat"
                    ? "Vamos conversar."
                    : "Sempre por perto."}
              </h1>
              <p>
                {tab === "memory"
                  ? "Conexões que permanecem, mesmo depois da conversa."
                  : "Uma extensão das suas ideias. Pronto para o próximo passo."}
              </p>
            </div>
            <span className="version">
              MARK I <span>/</span> INTERFACE NEURAL
            </span>
          </div>
          {tab === "memory" ? (
            <section className="memory-view">
              <label className="search-box">
                <Search size={18} />
                <input
                  aria-label="Buscar memórias"
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  placeholder="Buscar nas nossas conversas..."
                />
              </label>
              {memoryError ? (
                <p role="status">{memoryError}</p>
              ) : notes.length ? (
                <div className="note-grid">
                  {notes.map((note) => (
                    <button
                      className="note"
                      key={note.id}
                      onClick={() => setSelected(note)}
                    >
                      <Brain size={20} />
                      <h2>{note.id.slice(0, 10)}</h2>
                      <p>
                        {note.content
                          .split("## Matheus")[1]
                          ?.split("## Jarvis")[0]
                          ?.replaceAll(">", "")
                          .trim()
                          .slice(0, 180)}
                      </p>
                      <span>
                        Abrir conversa <ChevronRight size={14} />
                      </span>
                    </button>
                  ))}
                </div>
              ) : (
                <div className="empty-memory">
                  <Layers size={38} />
                  <h2>
                    {query
                      ? "Nenhuma memória encontrada"
                      : "O começo de uma história"}
                  </h2>
                  <p>
                    {query
                      ? "Experimente outras palavras."
                      : "Suas próximas conversas aparecerão aqui, em notas do Obsidian."}
                  </p>
                </div>
              )}
            </section>
          ) : (
            <div className="command-grid">
              <section className="core-panel">
                <div className="panel-top">
                  <span>
                    <i /> NÚCLEO DE INTELIGÊNCIA
                  </span>
                  <span>01 / VOICE LINK</span>
                </div>
                <Reactor phase={currentPhase} />
                <div className="reactor-state">
                  <span className="eyebrow">
                    {currentPhase === "speaking"
                      ? "TRANSMISSÃO DE VOZ"
                      : "JARVIS · PRESENÇA ATIVA"}
                  </span>
                  <h2>{labels[currentPhase]}</h2>
                  <p>
                    {online
                      ? "Diga “Hey Jarvis” ou bata duas palmas para começar."
                      : "Inicie o Jarvis no computador para conectar o núcleo."}
                  </p>
                </div>
                <div
                  className={`waveform ${currentPhase === "speaking" ? "moving" : ""}`}
                  aria-hidden="true"
                >
                  {Array.from({ length: 45 }, (_, i) => (
                    <i
                      key={i}
                      style={{
                        height: Number((5 + (Math.sin(i * 1.8) + 1) * 12).toFixed(3)),
                        animationDelay: `${i * 27}ms`,
                      }}
                    />
                  ))}
                </div>
                <div className="core-bottom">
                  <span>
                    <AudioLines size={14} /> VOZ NATIVA
                  </span>
                  <span>
                    ELEVENLABS <i>·</i> GEORGE
                  </span>
                </div>
              </section>
              <aside className="side-stack">
                <section className="chat-panel">
                  <div className="section-title">
                    <span>
                      <MessageSquare size={16} /> Conversa
                    </span>
                    <span className="micro-label">
                      {tab === "chat" ? "TEXTO" : "AO VIVO"}
                    </span>
                  </div>
                  <div className="chat-scroll" aria-live="polite">
                    {(tab === "core" ? voice : messages).length === 0 ? (
                      <div className="chat-empty">
                        <Sparkles size={24} />
                        <h3>Às suas ordens, senhor.</h3>
                        <p>
                          {tab === "core"
                            ? "Sua conversa por voz aparece aqui. Para escrever, use o campo abaixo."
                            : "O que vamos descobrir hoje?"}
                        </p>
                      </div>
                    ) : (
                      (tab === "core" ? voice : messages).map((m, i) => (
                        <div className={`message ${m.role}`} key={i}>
                          <span>{m.role === "user" ? "VOCÊ" : "JARVIS"}</span>
                          <p>{m.text}</p>
                        </div>
                      ))
                    )}
                    {busy && (
                      <p className="thinking" role="status">
                        Jarvis está pensando...
                      </p>
                    )}
                    <div ref={bottom} />
                  </div>
                  {error && (
                    <p className="error" role="alert">
                      {error}
                    </p>
                  )}
                  <form onSubmit={send} className="composer">
                    <input
                      aria-label="Mensagem para Jarvis"
                      maxLength={4000}
                      value={input}
                      onFocus={() => setTab("chat")}
                      onChange={(e) => setInput(e.target.value)}
                      placeholder="Fale com o Jarvis..."
                      disabled={!online}
                    />
                    <Button
                      type="submit"
                      size="icon"
                      aria-label="Enviar mensagem"
                      disabled={!online || busy || !input.trim()}
                    >
                      <ArrowUp size={18} />
                    </Button>
                  </form>
                  <div className="composer-hint">
                    TEXTO NO PAINEL · VOZ PELO MICROFONE LOCAL
                  </div>
                </section>
                <button
                  className="memory-card"
                  onClick={() => setTab("memory")}
                >
                  <div className="memory-icon">
                    <Brain size={23} />
                  </div>
                  <div>
                    <h3>Uma memória conectada</h3>
                    <p>Suas conversas, sempre ao alcance.</p>
                    <span>
                      EXPLORAR MEMÓRIA <ChevronRight size={13} />
                    </span>
                  </div>
                  <span className="obsidian-gem">◇</span>
                </button>
              </aside>
            </div>
          )}
          <footer>
            <span>
              <Cpu size={14} /> LOCAL FIRST <b> / </b>{" "}
              {online ? "PONTE ATIVA" : "AGUARDANDO SERVIÇO"}
            </span>
            <span>
              FEITO PARA MATHEUS <span className="footer-star">✦</span>
            </span>
          </footer>
        </main>
      </div>
      <dialog
        ref={dialog}
        onCancel={() => {
          setHelp(false)
          setSelected(null)
        }}
        aria-label={help ? "Conectar Jarvis" : "Conversa salva"}
        className="modal"
      >
        <Button
          variant="ghost"
          autoFocus
          aria-label="Fechar"
          onClick={() => {
            setHelp(false)
            setSelected(null)
          }}
          className="close"
        >
          <X />
        </Button>
        {help ? (
          <>
            <h2>Conecte seu Jarvis</h2>
            <p>Na raiz do projeto, inicie o serviço:</p>
            <code>.venv/Scripts/python.exe -m jarvis</code>
            <p>
              Depois, diga “Hey Jarvis” ou bata duas palmas. O painel acompanha
              a voz. O chat por texto responde aqui, sem executar envios
              externos.
            </p>
            <p>
              Conversas são salvas localmente no vault do Obsidian. Evite
              compartilhar senhas ou credenciais.
            </p>
          </>
        ) : (
          <>
            <h2>Conversa salva</h2>
            <pre>{selected?.content}</pre>
          </>
        )}
      </dialog>
    </div>
  )
}
