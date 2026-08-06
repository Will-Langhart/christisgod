"use client";

import { useState } from "react";
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

export function LiveDebate() {
  const [persona, setPersona] = useState<PersonaId>("seeker");
  const [objection, setObjection] = useState("");
  const [busy, setBusy] = useState(false);
  const [progress, setProgress] = useState<string>("");
  const [answer, setAnswer] = useState<string>("");
  const [status, setStatus] = useState<string>("");
  const [citations, setCitations] = useState<Citation[]>([]);
  const [error, setError] = useState<string>("");

  if (!API) return null; // dormant until configured

  async function ask() {
    if (!objection.trim() || busy) return;
    setBusy(true);
    setProgress("Reading the question…");
    setAnswer("");
    setStatus("");
    setCitations([]);
    setError("");

    try {
      const res = await fetch(`${API}/debate`, {
        method: "POST",
        headers: {
          "content-type": "application/json",
          ...(TOKEN ? { authorization: `Bearer ${TOKEN}` } : {}),
        },
        body: JSON.stringify({ persona, objection }),
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
          if (parsed.event === "interlocutor") setProgress("Considering the objection…");
          else if (parsed.event === "draft") setProgress("Drafting a grounded answer…");
          else if (parsed.event === "progress") setProgress("Checking every citation against the KJV…");
          else if (parsed.event === "done") {
            setAnswer(String(d.answer ?? ""));
            setStatus(String(d.status ?? ""));
            setCitations((d.citations as Citation[]) ?? []);
            setProgress("");
          } else if (parsed.event === "error") {
            setError(String(d.message ?? "Something went wrong."));
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

  const degraded = status === "degraded";

  return (
    <section className="border-t border-rule px-6 py-20 sm:py-24">
      <div className="mx-auto max-w-3xl">
        <header className="mx-auto max-w-2xl text-center">
          <p className="font-[family-name:var(--font-ui)] text-xs font-semibold uppercase tracking-[0.28em] text-vermillion">
            Ask your own question
          </p>
          <h2 className="mt-3 font-[family-name:var(--font-display)] text-3xl font-semibold text-ink sm:text-4xl">
            Put the case to the test yourself.
          </h2>
          <p className="mt-4 font-[family-name:var(--font-serif)] text-lg leading-relaxed text-ink-soft">
            Pose any objection and hear it answered live, grounded in the King
            James text. These responses are generated in the moment and—unlike the
            curated dialogues above—are not individually reviewed.
          </p>
        </header>

        <div className="mt-9 rounded-2xl border border-rule bg-surface/70 p-5 sm:p-7">
          <div role="tablist" aria-label="Choose an interlocutor" className="flex flex-wrap gap-2">
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

          <textarea
            value={objection}
            onChange={(e) => setObjection(e.target.value)}
            disabled={busy}
            rows={3}
            placeholder="e.g. If Jesus is God, why did he not know the day or hour?"
            className="mt-4 w-full resize-y rounded-xl border border-rule bg-parchment/60 px-4 py-3 font-[family-name:var(--font-serif)] text-lg text-ink outline-none placeholder:text-ink-faint focus:border-gold/40"
          />

          <div className="mt-3 flex items-center justify-end">
            <button
              onClick={ask}
              disabled={busy || !objection.trim()}
              className="inline-flex items-center gap-2 rounded-full border border-gold/40 bg-gold/10 px-5 py-2.5 font-[family-name:var(--font-ui)] text-sm font-semibold text-gold transition hover:bg-gold/15 disabled:opacity-40"
            >
              {busy ? <Loader2 className="h-4 w-4 animate-spin" /> : <Send className="h-4 w-4" />}
              {busy ? "Weighing the evidence…" : "Ask"}
            </button>
          </div>

          {(progress || answer || error) && (
            <div className="mt-6 border-t border-rule pt-6">
              {error ? (
                <p className="font-[family-name:var(--font-serif)] text-base text-vermillion">{error}</p>
              ) : progress ? (
                <p className="flex items-center gap-2 font-[family-name:var(--font-serif)] text-base italic text-ink-faint">
                  <Loader2 className="h-4 w-4 animate-spin" />
                  {progress}
                </p>
              ) : degraded ? (
                <p className="font-[family-name:var(--font-serif)] text-lg leading-relaxed text-ink-soft">
                  {answer}
                </p>
              ) : (
                <>
                  <div className="space-y-4">
                    {answer.split(/\n\s*\n/).map((para, i) => (
                      <p
                        key={i}
                        className="font-[family-name:var(--font-serif)] text-lg leading-relaxed text-ink-soft"
                      >
                        {linkifyScripture(para)}
                      </p>
                    ))}
                  </div>
                  {citations.length > 0 && (
                    <ul className="mt-5 flex flex-wrap gap-2" aria-label="Cited passages">
                      {citations.map((c) => (
                        <li
                          key={c.display}
                          className="rounded-full border border-lapis/20 bg-lapis/5 px-3 py-1 font-[family-name:var(--font-ui)] text-[0.7rem] font-medium tracking-wide text-lapis"
                        >
                          {c.display}
                        </li>
                      ))}
                    </ul>
                  )}
                </>
              )}
            </div>
          )}
        </div>
      </div>
    </section>
  );
}
