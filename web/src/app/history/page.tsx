import type { Metadata } from "next";
import Link from "next/link";
import { ArrowLeft, ArrowRight, Clock3 } from "lucide-react";
import { HistoryTimeline } from "@/components/history-timeline";
import { site } from "@/lib/site";

export const metadata: Metadata = {
  title: "Was Jesus Made God at Nicaea? A Historical Timeline",
  description: "Follow the evidence for Christian belief in the divinity of Jesus from the New Testament to the Council of Nicaea.",
  alternates: { canonical: "/history" },
  openGraph: {
    title: "Before Nicaea: The Earliest Belief About Jesus",
    description: "A visual timeline of Christian belief in the divinity of Christ before AD 325.",
    url: `${site.url}/history`,
    type: "article",
  },
};

export default function HistoryPage() {
  return (
    <main className="history-page min-h-full px-6 py-10 sm:py-16">
      <div className="mx-auto max-w-4xl">
        <Link href="/#questions" className="inline-flex items-center gap-1.5 font-[family-name:var(--font-ui)] text-xs font-semibold uppercase tracking-wider text-ink-faint transition hover:text-gold">
          <ArrowLeft className="h-3.5 w-3.5" /> Back to the questions
        </Link>

        <header className="mx-auto max-w-3xl py-16 text-center sm:py-20">
          <span className="mx-auto flex h-12 w-12 items-center justify-center rounded-full border border-gold/30 bg-gold/10 text-gold"><Clock3 className="h-5 w-5" /></span>
          <p className="mt-5 font-[family-name:var(--font-ui)] text-xs font-semibold uppercase tracking-[0.28em] text-vermillion">Before Nicaea</p>
          <h1 className="mt-4 font-[family-name:var(--font-display)] text-5xl font-semibold leading-[1.04] text-ink sm:text-7xl">The council did not create a new Jesus.</h1>
          <p className="mx-auto mt-6 max-w-2xl font-[family-name:var(--font-serif)] text-xl leading-relaxed text-ink-soft sm:text-2xl">
            The sources form a continuous trail from the apostles to AD 325. Nicaea gave precise language to a confession Christians had already prayed, sung, and died for.
          </p>
        </header>

        <HistoryTimeline />

        <section className="history-verdict mx-auto mt-16 max-w-3xl rounded-2xl border border-gold/30 p-7 text-center sm:p-10">
          <p className="font-[family-name:var(--font-ui)] text-xs font-semibold uppercase tracking-[0.2em] text-vermillion">The historical verdict</p>
          <h2 className="mt-3 font-[family-name:var(--font-display)] text-3xl font-semibold text-ink sm:text-4xl">Nicaea was a guardrail, not a starting gun.</h2>
          <p className="mt-4 font-[family-name:var(--font-serif)] text-lg leading-relaxed text-ink-soft">The council’s language became more technical, but the belief it protected was already ancient.</p>
          <Link href="/read/xi-how-early-is-this-belief" className="mt-7 inline-flex items-center gap-2 rounded-full bg-gold px-6 py-3 font-[family-name:var(--font-ui)] text-xs font-semibold uppercase tracking-wider text-parchment transition hover:bg-gold-bright">
            Read the full historical case <ArrowRight className="h-4 w-4" />
          </Link>
        </section>
      </div>
    </main>
  );
}
