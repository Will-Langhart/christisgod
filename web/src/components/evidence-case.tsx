import Link from "next/link";
import { ArrowRight, Timer } from "lucide-react";
import { evidenceStrands } from "@/lib/evidence-case";

export function EvidenceCase() {
  return (
    <section id="case" className="px-6 py-20 sm:py-24">
      <div className="mx-auto max-w-6xl">
        <div className="mx-auto max-w-3xl text-center">
          <p className="font-[family-name:var(--font-ui)] text-xs font-semibold uppercase tracking-[0.28em] text-vermillion">
            The cumulative case
          </p>
          <h2 className="mt-4 font-[family-name:var(--font-display)] text-4xl font-semibold leading-tight text-ink sm:text-5xl">
            One claim. Six converging lines of evidence.
          </h2>
          <p className="mt-5 font-[family-name:var(--font-serif)] text-xl leading-relaxed text-ink-soft">
            No single verse must carry the whole case. Scripture presents a
            unified portrait: Jesus shares the names, works, honor, and identity
            of the God of Israel.
          </p>
        </div>

        <div className="evidence-grid relative mt-14 grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {evidenceStrands.map((strand, index) => {
            const Icon = strand.icon;
            return (
              <Link
                href={strand.href}
                key={strand.title}
                className="evidence-card group relative overflow-hidden rounded-2xl border border-rule bg-surface/75 p-6"
              >
                <span className="evidence-number" aria-hidden>{String(index + 1).padStart(2, "0")}</span>
                <div className="relative z-10">
                  <span className="mb-5 inline-flex h-11 w-11 items-center justify-center rounded-full border border-gold/40 bg-gold/10 text-gold">
                    <Icon className="h-5 w-5" strokeWidth={1.6} />
                  </span>
                  <h3 className="font-[family-name:var(--font-display)] text-2xl font-semibold text-ink transition-colors group-hover:text-gold">
                    {strand.title}
                  </h3>
                  <p className="mt-2 font-[family-name:var(--font-serif)] text-lg leading-snug text-ink-soft">
                    {strand.summary}
                  </p>
                  <ul className="mt-5 flex flex-wrap gap-2" aria-label="Key passages">
                    {strand.references.map((reference) => (
                      <li key={reference} className="rounded-full border border-rule bg-parchment/70 px-3 py-1 font-[family-name:var(--font-ui)] text-[0.68rem] font-medium tracking-wide text-ink-faint">
                        {reference}
                      </li>
                    ))}
                  </ul>
                  <span className="mt-6 inline-flex items-center gap-1.5 font-[family-name:var(--font-ui)] text-xs font-semibold uppercase tracking-wider text-lapis">
                    Examine the evidence <ArrowRight className="h-3.5 w-3.5 transition-transform group-hover:translate-x-1" />
                  </span>
                </div>
              </Link>
            );
          })}
        </div>

        <div className="case-conclusion mx-auto mt-10 max-w-3xl rounded-2xl border border-gold/30 px-6 py-7 text-center sm:px-10">
          <p className="font-[family-name:var(--font-display)] text-2xl font-semibold text-ink sm:text-3xl">
            The best explanation of the whole portrait:
            <span className="block text-gold">Jesus truly is God.</span>
          </p>
          <p className="mt-3 font-[family-name:var(--font-serif)] text-base italic text-ink-faint">
            Explore each strand, test the passages in context, and judge the case for yourself.
          </p>
          <Link href="/case" className="mt-6 inline-flex items-center gap-2 rounded-full bg-gold px-6 py-3 font-[family-name:var(--font-ui)] text-xs font-semibold uppercase tracking-wider text-parchment transition hover:bg-gold-bright">
            <Timer className="h-4 w-4" /> Take the 10-minute journey <ArrowRight className="h-4 w-4" />
          </Link>
        </div>
      </div>
    </section>
  );
}
