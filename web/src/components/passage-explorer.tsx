import { ArrowDown, Link2 } from "lucide-react";
import { passageParallels } from "@/lib/passage-parallels";

function HighlightedText({ text, highlight }: { text: string; highlight: string }) {
  const start = text.toLowerCase().indexOf(highlight.toLowerCase());
  if (start < 0) return <>{text}</>;
  const end = start + highlight.length;
  return <>{text.slice(0, start)}<mark>{text.slice(start, end)}</mark>{text.slice(end)}</>;
}

export function PassageExplorer() {
  return (
    <div className="space-y-10">
      {passageParallels.map((pair, index) => (
        <article key={pair.theme} className="parallel-pair">
          <header className="mb-5 flex items-center gap-3">
            <span className="font-[family-name:var(--font-ui)] text-xs font-bold tabular-nums text-vermillion">{String(index + 1).padStart(2, "0")}</span>
            <h2 className="font-[family-name:var(--font-display)] text-2xl font-semibold text-ink sm:text-3xl">{pair.theme}</h2>
          </header>

          <div className="parallel-grid grid gap-3 md:grid-cols-[1fr_auto_1fr] md:items-stretch">
            <section className="parallel-text parallel-old rounded-2xl border border-rule p-6 sm:p-7" aria-label={`Old Testament: ${pair.oldRef}`}>
              <p className="parallel-label">Old Testament · Yahweh</p>
              <blockquote className="mt-4 font-[family-name:var(--font-serif)] text-xl leading-relaxed text-ink sm:text-2xl">
                “<HighlightedText text={pair.oldText} highlight={pair.oldHighlight} />”
              </blockquote>
              <p className="mt-5 font-[family-name:var(--font-ui)] text-xs font-bold uppercase tracking-[0.18em] text-gold">{pair.oldRef}</p>
            </section>

            <div className="parallel-connector flex items-center justify-center" aria-hidden>
              <span className="flex h-10 w-10 items-center justify-center rounded-full border border-gold/40 bg-parchment text-gold">
                <Link2 className="hidden h-4 w-4 md:block" />
                <ArrowDown className="h-4 w-4 md:hidden" />
              </span>
            </div>

            <section className="parallel-text parallel-new rounded-2xl border border-rule p-6 sm:p-7" aria-label={`New Testament: ${pair.newRef}`}>
              <p className="parallel-label">New Testament · Jesus</p>
              <blockquote className="mt-4 font-[family-name:var(--font-serif)] text-xl leading-relaxed text-ink sm:text-2xl">
                “<HighlightedText text={pair.newText} highlight={pair.newHighlight} />”
              </blockquote>
              <p className="mt-5 font-[family-name:var(--font-ui)] text-xs font-bold uppercase tracking-[0.18em] text-lapis">{pair.newRef}</p>
            </section>
          </div>

          <div className="parallel-explanation mx-auto max-w-3xl px-5 py-5 text-center">
            <p className="font-[family-name:var(--font-serif)] text-lg italic leading-relaxed text-ink-soft">{pair.explanation}</p>
          </div>
        </article>
      ))}
    </div>
  );
}
