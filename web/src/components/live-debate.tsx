"use client";

import { useEffect, useRef, useState } from "react";
import { Loader2, Send } from "lucide-react";
import { dialoguePersonas } from "@/lib/dialogues.generated";
import { linkifyScripture } from "@/lib/linkify-scripture";

// Configured at build time. When unset the whole box is dormant (renders nothing),
// so shipping this is safe before the service exists. Point it at the Render URL:
//   NEXT_PUBLIC_DEBATE_API=https://christisgod-service.onrender.com
const API = process.env.NEXT_PUBLIC_DEBATE_API;
// Optional bearer token. A browser token is NOT secret — prefer leaving the
// service's DEBATE_API_TOKEN unset and relying on its CORS + rate limit.
const TOKEN = process.env.NEXT_PUBLIC_DEBATE_TOKEN;

type PersonaId = (typeof dialoguePersonas)[number]["id"];
type Citation = { display: string; text: string | null };
type ChatMessage = {
  role: "user" | "assistant";
  content: string;
  status?: string; // "approved" | "degraded" | "deflected"
  citations?: Citation[];
};

function parseSSE(frame: string): { event: string; data: unknown } | null {
  let event = "message";
  const dataLines: string[] = [];
  for (const line of frame.split("\n")) {
    if (line.startsWith("event:")) event = line.slice(6).trim();
    else if (line.startsWith("data:")) dataLines.push(line.slice(5).trim());
  }
  if (!dataLines.length) return null;
  try {
    return { event, data: JSON.parse(dataLines.join("\n")) };
  } catch {
    return null;
  }
}

type Mode = "direct" | "debate";

export function LiveDebate() {
  const [mode, setMode] = useState<Mode>("direct");
  const [persona, setPersona] = useState<PersonaId>("seeker");
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [busy, setBusy] = useState(false);
  const [progress, setProgress] = useState<string>("");
  const [error, setError] = useState<string>("");
  const scrollRef = useRef<HTMLDivElement>(null);

  // Keep the newest turn in view as the conversation and progress notes grow.
  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: "smooth" });
  }, [messages, progress]);

  if (!API) return null; // dormant until configured

  async function ask() {
    const question = input.trim();
    if (!question || busy) return;

    // Optimistically show the reader's turn and send the full transcript so the
    // stateless service can remember the exchange (AI-SPEC.md §9 — client holds memory).
    const history: ChatMessage[] = [...messages, { role: "user", content: question }];
    setMessages(history);
    setInput("");
    setBusy(true);
    setError("");
    setProgress("Reading your question…");

    try {
      const res = await fetch(`${API}/chat`, {
        method: "POST",
        headers: {
          "content-type": "application/json",
          ...(TOKEN ? { authorization: `Bearer ${TOKEN}` } : {}),
        },
        body: JSON.stringify({
          persona,
          mode,
          messages: history.map((m) => ({ role: m.role, content: m.content })),
        }),
      });
      if (!res.ok || !res.body) {
        setError(
          res.status === 429
            ? "Too many questions just now — give it a moment and try again."
            : `The service returned an error (${res.status}).`,
        );
        return;
      }

      const reader = res.body.getReader();
      const decoder = new TextDecoder();
      let buffer = "";
      for (;;) {
        const { done, value } = await reader.read();
        if (done) break;
        buffer += decoder.decode(value, { stream: true });
        const frames = buffer.split("\n\n");
        buffer = frames.pop() ?? "";
        for (const frame of frames) {
          const parsed = parseSSE(frame);
          if (!parsed) continue;
          const d = parsed.data as Record<string, unknown>;
          switch (parsed.event) {
            case "thinking":
            case "retrieving":
            case "drafting":
            case "verifying":
              setProgress(String(d.note ?? "Working…"));
              break;
            case "done":
              setMessages((prev) => [
                ...prev,
                {
                  role: "assistant",
                  content: String(d.answer ?? ""),
                  status: String(d.status ?? ""),
                  citations: (d.citations as Citation[]) ?? [],
                },
              ]);
              setProgress("");
              break;
            case "error":
              setError(String(d.message ?? "Something went wrong."));
              break;
          }
        }
      }
    } catch {
      setError("Could not reach the service. It may be waking up — try again in a moment.");
    } finally {
      setBusy(false);
      setProgress("");
    }
  }

  function onKeyDown(e: React.KeyboardEvent<HTMLTextAreaElement>) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      void ask();
    }
  }

  function switchMode(next: Mode) {
    if (next === mode || busy) return;
    setMode(next);
    setMessages([]); // a direct thread and a debate thread don't mix
    setError("");
    setProgress("");
  }

  const started = messages.length > 0 || busy;
  const debate = mode === "debate";

  return (
    <section className="border-t border-rule px-6 py-20 sm:py-24">
      <div className="mx-auto max-w-3xl">
        <header className="mx-auto max-w-2xl text-center">
          <p className="font-[family-name:var(--font-ui)] text-xs font-semibold uppercase tracking-[0.28em] text-vermillion">
            {debate ? "Defend the case" : "Ask your own question"}
          </p>
          <h2 className="mt-3 font-[family-name:var(--font-display)] text-3xl font-semibold text-ink sm:text-4xl">
            {debate ? "Take the other side on." : "Put the case to the test yourself."}
          </h2>
          <p className="mt-4 font-[family-name:var(--font-serif)] text-lg leading-relaxed text-ink-soft">
            {debate ? (
              <>
                Make your case for the deity of Christ and the voice below will
                press it — as a skeptic, a Muslim, or a Jehovah&rsquo;s Witness
                would. It argues in character, but it may never fabricate or
                misquote a verse. A sparring partner for your own answers.
              </>
            ) : (
              <>
                Ask anything about the deity of Christ and follow the thread as far
                as you like — every answer is generated in the moment and grounded
                in the King James text. Unlike the curated dialogues above, these
                responses are not individually reviewed.
              </>
            )}
          </p>
        </header>

        <div className="mt-8 flex justify-center">
          <div role="tablist" aria-label="Choose a mode" className="inline-flex rounded-full border border-rule bg-parchment/60 p-1">
            {(["direct", "debate"] as const).map((m) => {
              const on = m === mode;
              return (
                <button
                  key={m}
                  role="tab"
                  aria-selected={on}
                  onClick={() => switchMode(m)}
                  disabled={busy}
                  className={`rounded-full px-4 py-1.5 font-[family-name:var(--font-ui)] text-sm font-semibold transition disabled:opacity-50 ${
                    on ? "bg-gold/15 text-gold" : "text-ink-soft hover:text-lapis"
                  }`}
                >
                  {m === "direct" ? "Ask a question" : "Debate me"}
                </button>
              );
            })}
          </div>
        </div>

        <div className="mt-6 rounded-2xl border border-rule bg-surface/70 p-5 sm:p-7">
          <div
            role="tablist"
            aria-label={debate ? "Choose who challenges you" : "Choose an answering voice"}
            className="flex flex-wrap gap-2"
          >
            {dialoguePersonas.map((p) => {
              const selected = p.id === persona;
              return (
                <button
                  key={p.id}
                  role="tab"
                  aria-selected={selected}
                  onClick={() => setPersona(p.id)}
                  disabled={busy}
                  className={`rounded-full border px-3.5 py-1.5 font-[family-name:var(--font-ui)] text-sm font-medium transition disabled:opacity-50 ${
                    selected
                      ? "border-gold/40 bg-gold/10 text-gold"
                      : "border-rule bg-parchment/60 text-ink-soft hover:border-lapis/30 hover:text-lapis"
                  }`}
                >
                  {p.label}
                </button>
              );
            })}
          </div>

          {started && (
            <div
              ref={scrollRef}
              className="mt-6 max-h-[28rem] space-y-5 overflow-y-auto border-t border-rule pt-6"
            >
              {messages.map((m, i) =>
                m.role === "user" ? (
                  <div key={i} className="flex justify-end">
                    <p className="max-w-[85%] rounded-2xl rounded-br-sm border border-lapis/20 bg-lapis/5 px-4 py-2.5 font-[family-name:var(--font-serif)] text-lg text-ink">
                      {m.content}
                    </p>
                  </div>
                ) : (
                  <div key={i} className="flex justify-start">
                    <div className="max-w-[90%]">
                      <div className="space-y-3">
                        {m.content.split(/\n\s*\n/).map((para, j) => (
                          <p
                            key={j}
                            className="font-[family-name:var(--font-serif)] text-lg leading-relaxed text-ink-soft"
                          >
                            {m.status === "approved" ? linkifyScripture(para) : para}
                          </p>
                        ))}
                      </div>
                      {m.citations && m.citations.length > 0 && (
                        <ul className="mt-4 flex flex-wrap gap-2" aria-label="Cited passages">
                          {m.citations.map((c) => (
                            <li
                              key={c.display}
                              className="rounded-full border border-lapis/20 bg-lapis/5 px-3 py-1 font-[family-name:var(--font-ui)] text-[0.7rem] font-medium tracking-wide text-lapis"
                            >
                              {c.display}
                            </li>
                          ))}
                        </ul>
                      )}
                    </div>
                  </div>
                ),
              )}

              {progress && (
                <p className="flex items-center gap-2 font-[family-name:var(--font-serif)] text-base italic text-ink-faint">
                  <Loader2 className="h-4 w-4 animate-spin" />
                  {progress}
                </p>
              )}
            </div>
          )}

          <div className="mt-5 flex items-end gap-3">
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={onKeyDown}
              disabled={busy}
              rows={2}
              placeholder={
                messages.length
                  ? debate
                    ? "Answer the challenge…"
                    : "Ask a follow-up…"
                  : debate
                    ? "Make your case — e.g. Jesus forgave sins, which only God can do."
                    : "e.g. If Jesus is God, why did he not know the day or hour?"
              }
              className="w-full resize-y rounded-xl border border-rule bg-parchment/60 px-4 py-3 font-[family-name:var(--font-serif)] text-lg text-ink outline-none placeholder:text-ink-faint focus:border-gold/40"
            />
            <button
              onClick={ask}
              disabled={busy || !input.trim()}
              aria-label="Send question"
              className="inline-flex shrink-0 items-center gap-2 rounded-full border border-gold/40 bg-gold/10 px-5 py-3 font-[family-name:var(--font-ui)] text-sm font-semibold text-gold transition hover:bg-gold/15 disabled:opacity-40"
            >
              {busy ? <Loader2 className="h-4 w-4 animate-spin" /> : <Send className="h-4 w-4" />}
              <span className="hidden sm:inline">{busy ? "Weighing…" : "Ask"}</span>
            </button>
          </div>

          {error && (
            <p className="mt-3 font-[family-name:var(--font-serif)] text-base text-vermillion">{error}</p>
          )}
        </div>
      </div>
    </section>
  );
}
