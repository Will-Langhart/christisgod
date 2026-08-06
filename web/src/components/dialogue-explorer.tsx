"use client";

import { useState } from "react";
import Link from "next/link";
import { ArrowRight, MessagesSquare, Plus } from "lucide-react";
import { dialogues, dialoguePersonas } from "@/lib/dialogues.generated";
import { linkifyScripture } from "@/lib/linkify-scripture";

export function DialogueExplorer() {
  const [persona, setPersona] = useState(dialoguePersonas[0].id);
  const active = dialoguePersonas.find((p) => p.id === persona) ?? dialoguePersonas[0];

  return (
    <section className="px-6 py-20 sm:py-24">
      <div className="mx-auto max-w-4xl">
        <header className="mx-auto max-w-2xl text-center">
          <span className="mx-auto flex h-12 w-12 items-center justify-center rounded-full border border-lapis/25 bg-lapis/10 text-lapis">
            <MessagesSquare className="h-5 w-5" strokeWidth={1.7} />
          </span>
          <p className="mt-5 font-[family-name:var(--font-ui)] text-xs font-semibold uppercase tracking-[0.28em] text-lapis">
            Test the case
          </p>
          <h1 className="mt-3 font-[family-name:var(--font-display)] text-4xl font-semibold text-ink sm:text-5xl">
            Answered in their own words.
          </h1>
          <p className="mt-4 font-[family-name:var(--font-serif)] text-xl leading-relaxed text-ink-soft">
            Choose the voice raising the objection, then read a careful, fully
            cited response. Every scripture reference is grounded in the King
            James text.
          </p>
        </header>

        {/* Persona selector */}
        <div className="mt-10">
          <div
            role="tablist"
            aria-label="Choose an interlocutor"
            className="flex flex-wrap justify-center gap-2"
          >
            {dialoguePersonas.map((p) => {
              const selected = p.id === persona;
              return (
                <button
                  key={p.id}
                  role="tab"
                  aria-selected={selected}
                  onClick={() => setPersona(p.id)}
                  className={`rounded-full border px-4 py-2 font-[family-name:var(--font-ui)] text-sm font-medium transition ${
                    selected
                      ? "border-gold/40 bg-gold/10 text-gold"
                      : "border-rule bg-surface/60 text-ink-soft hover:border-lapis/30 hover:text-lapis"
                  }`}
                >
                  {p.label}
                </button>
              );
            })}
          </div>
          <p className="mt-3 text-center font-[family-name:var(--font-serif)] text-base italic text-ink-faint">
            {active.blurb}
          </p>
        </div>

        {/* Objections */}
        <div className="mt-10 space-y-3">
          {dialogues.map((set, index) => {
            const answer = set.answers.find((a) => a.persona === persona);
            return (
              <details
                key={set.question}
                className="objection-item group rounded-xl border border-rule bg-surface/70"
              >
                <summary className="flex cursor-pointer list-none items-center gap-4 px-5 py-5 sm:px-7">
                  <span className="font-[family-name:var(--font-ui)] text-xs font-semibold tabular-nums text-vermillion">
                    {String(index + 1).padStart(2, "0")}
                  </span>
                  <span className="flex-1 font-[family-name:var(--font-display)] text-xl font-semibold leading-snug text-ink sm:text-2xl">
                    {set.question}
                  </span>
                  <Plus className="objection-plus h-5 w-5 shrink-0 text-gold" aria-hidden />
                </summary>

                <div className="objection-answer border-t border-rule px-5 pb-7 pt-6 sm:px-7">
                  {answer ? (
                    <>
                      <div className="space-y-4">
                        {answer.answer.split(/\n\s*\n/).map((para, i) => (
                          <p
                            key={i}
                            className="font-[family-name:var(--font-serif)] text-lg leading-relaxed text-ink-soft"
                          >
                            {linkifyScripture(para)}
                          </p>
                        ))}
                      </div>
                      {answer.refs.length > 0 && (
                        <ul className="mt-6 flex flex-wrap gap-2" aria-label="Cited passages">
                          {answer.refs.map((ref) => (
                            <li
                              key={ref}
                              className="rounded-full border border-lapis/20 bg-lapis/5 px-3 py-1 font-[family-name:var(--font-ui)] text-[0.7rem] font-medium tracking-wide text-lapis"
                            >
                              {ref}
                            </li>
                          ))}
                        </ul>
                      )}
                    </>
                  ) : (
                    <p className="font-[family-name:var(--font-serif)] text-base italic text-ink-faint">
                      No response recorded for this voice yet.
                    </p>
                  )}
                  <Link
                    href={set.href}
                    className="mt-6 inline-flex items-center gap-1.5 font-[family-name:var(--font-ui)] text-xs font-semibold uppercase tracking-wider text-lapis transition hover:text-lapis-bright"
                  >
                    {set.linkLabel}
                    <ArrowRight className="h-3.5 w-3.5" />
                  </Link>
                </div>
              </details>
            );
          })}
        </div>

        <p className="mx-auto mt-10 max-w-2xl text-center font-[family-name:var(--font-serif)] text-base italic text-ink-faint">
          Each answer was checked against the full King James text before being
          recorded—no invented citations, no misquoted verses.
        </p>
      </div>
    </section>
  );
}
