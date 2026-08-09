import Link from "next/link";
import { ArrowRight, HelpCircle, Plus } from "lucide-react";
import { objections } from "@/lib/objections";

export function ObjectionExplorer() {
  return (
    <section id="questions" className="px-6 py-20 sm:py-24">
      <div className="mx-auto max-w-4xl">
        <header className="mx-auto max-w-2xl text-center">
          <span className="mx-auto flex h-12 w-12 items-center justify-center rounded-full border border-lapis/25 bg-lapis/10 text-lapis">
            <HelpCircle className="h-5 w-5" strokeWidth={1.7} />
          </span>
          <p className="mt-5 font-[family-name:var(--font-ui)] text-xs font-semibold uppercase tracking-[0.28em] text-lapis">
            Test the case
          </p>
          <h2 className="mt-3 font-[family-name:var(--font-display)] text-4xl font-semibold text-ink sm:text-5xl">
            Honest questions deserve careful answers.
          </h2>
          <p className="mt-4 font-[family-name:var(--font-serif)] text-xl leading-relaxed text-ink-soft">
            Open an objection for a concise response, then follow the evidence
            into its full scriptural and historical context.
          </p>
        </header>

        <div className="mt-12 space-y-3">
          {objections.map((objection, index) => (
            <details key={objection.question} className="objection-item group rounded-xl border border-rule bg-surface/70">
              <summary className="flex cursor-pointer list-none items-center gap-4 px-5 py-5 sm:px-7">
                <span className="font-[family-name:var(--font-ui)] text-xs font-semibold tabular-nums text-vermillion">
                  {String(index + 1).padStart(2, "0")}
                </span>
                <span className="flex-1 font-[family-name:var(--font-display)] text-xl font-semibold leading-snug text-ink sm:text-2xl">
                  {objection.question}
                </span>
                <Plus className="objection-plus h-5 w-5 shrink-0 text-gold" aria-hidden />
              </summary>

              <div className="objection-answer border-t border-rule px-5 pb-7 pt-6 sm:px-7 sm:pl-[4.5rem]">
                <p className="font-[family-name:var(--font-display)] text-xl font-semibold leading-snug text-gold">
                  {objection.shortAnswer}
                </p>
                <p className="mt-3 font-[family-name:var(--font-serif)] text-lg leading-relaxed text-ink-soft">
                  {objection.explanation}
                </p>
                <ul className="mt-5 flex flex-wrap gap-2" aria-label="Relevant passages">
                  {objection.passages.map((passage) => (
                    <li key={passage} className="rounded-full border border-lapis/20 bg-lapis/5 px-3 py-1 font-[family-name:var(--font-ui)] text-[0.7rem] font-medium tracking-wide text-lapis">
                      {passage}
                    </li>
                  ))}
                </ul>
                <Link href={objection.href} className="mt-6 inline-flex items-center gap-1.5 font-[family-name:var(--font-ui)] text-xs font-semibold uppercase tracking-wider text-lapis transition hover:text-lapis-bright">
                  {objection.linkLabel}
                  <ArrowRight className="h-3.5 w-3.5" />
                </Link>
              </div>
            </details>
          ))}
        </div>

        <div className="mt-9 text-center">
          <Link
            href="/dialogues"
            className="inline-flex items-center gap-2 rounded-full border border-gold/40 bg-gold/10 px-5 py-2.5 font-[family-name:var(--font-ui)] text-sm font-semibold text-gold transition hover:bg-gold/15"
          >
            Answered voice by voice — skeptic, Muslim, seeker
            <ArrowRight className="h-4 w-4" />
          </Link>
        </div>

        <p className="mx-auto mt-6 max-w-2xl text-center font-[family-name:var(--font-serif)] text-base italic text-ink-faint">
          Questions are not enemies of faith. The invitation is to examine the
          evidence patiently, in context, without being asked to pretend certainty.
        </p>
      </div>
    </section>
  );
}
