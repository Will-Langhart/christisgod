import type { Metadata } from "next";
import Link from "next/link";
import { ArrowLeft, ArrowRight, Columns3 } from "lucide-react";
import { PassageExplorer } from "@/components/passage-explorer";
import { site } from "@/lib/site";

export const metadata: Metadata = {
  title: "Yahweh and Jesus: Side-by-Side Bible Passages",
  description: "Compare Old Testament passages about Yahweh with New Testament passages that apply the same language to Jesus.",
  alternates: { canonical: "/parallels" },
  openGraph: {
    title: "Yahweh and Jesus: Compare the Passages",
    description: "See five striking Old and New Testament parallels side by side.",
    url: `${site.url}/parallels`,
    type: "article",
  },
};

export default function ParallelsPage() {
  return (
    <main className="parallels-page min-h-full px-5 py-10 sm:px-6 sm:py-16">
      <div className="mx-auto max-w-6xl">
        <Link href="/#case" className="inline-flex items-center gap-1.5 font-[family-name:var(--font-ui)] text-xs font-semibold uppercase tracking-wider text-ink-faint transition hover:text-gold">
          <ArrowLeft className="h-3.5 w-3.5" /> Back to the cumulative case
        </Link>

        <header className="mx-auto max-w-3xl py-16 text-center sm:py-20">
          <span className="mx-auto flex h-12 w-12 items-center justify-center rounded-full border border-lapis/25 bg-lapis/10 text-lapis"><Columns3 className="h-5 w-5" /></span>
          <p className="mt-5 font-[family-name:var(--font-ui)] text-xs font-semibold uppercase tracking-[0.28em] text-vermillion">Read the texts together</p>
          <h1 className="mt-4 font-[family-name:var(--font-display)] text-5xl font-semibold leading-[1.04] text-ink sm:text-7xl">Yahweh in the Old Testament. Jesus in the New.</h1>
          <p className="mx-auto mt-6 max-w-2xl font-[family-name:var(--font-serif)] text-xl leading-relaxed text-ink-soft sm:text-2xl">
            The apostles take words, worship, and works belonging to Israel’s God and apply them directly to Jesus. Compare the language for yourself.
          </p>
        </header>

        <PassageExplorer />

        <section className="parallel-verdict mx-auto mt-16 max-w-3xl rounded-2xl border border-gold/30 p-7 text-center sm:p-10">
          <p className="font-[family-name:var(--font-ui)] text-xs font-semibold uppercase tracking-[0.2em] text-vermillion">The recurring pattern</p>
          <h2 className="mt-3 font-[family-name:var(--font-display)] text-3xl font-semibold text-ink sm:text-4xl">This is not one ambiguous verse.</h2>
          <p className="mt-4 font-[family-name:var(--font-serif)] text-lg leading-relaxed text-ink-soft">Across different authors and contexts, the New Testament repeatedly places Jesus within the identity and work of Yahweh.</p>
          <Link href="/read/iv-jesus-is-god" className="mt-7 inline-flex items-center gap-2 rounded-full bg-gold px-6 py-3 font-[family-name:var(--font-ui)] text-xs font-semibold uppercase tracking-wider text-parchment transition hover:bg-gold-bright">
            Read the complete argument <ArrowRight className="h-4 w-4" />
          </Link>
        </section>
      </div>
    </main>
  );
}
