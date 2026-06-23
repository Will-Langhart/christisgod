import Link from "next/link";
import Image from "next/image";
import { ArrowRight } from "lucide-react";
import { bookMeta } from "@/lib/book-meta";
import { chapters } from "@/lib/chapters";
import { ThemeToggle } from "@/components/theme-toggle";
import { Hero } from "@/components/hero";

export default function Home() {
  return (
    <div className="flex min-h-full flex-col">
      <div className="absolute right-4 top-4 z-20 sm:right-6 sm:top-6">
        <ThemeToggle />
      </div>

      <Hero />

      {/* Epigraphs */}
      <section
        id="epigraphs"
        className="scroll-mt-8 border-y border-rule bg-parchment-deep/40 px-6 py-14"
      >
        <div className="mx-auto grid max-w-3xl gap-10 sm:grid-cols-2">
          {bookMeta.epigraphs.map((e) => (
            <figure key={e.ref} className="text-center">
              <blockquote className="font-[family-name:var(--font-serif)] text-xl italic leading-relaxed text-ink">
                &ldquo;{e.text}&rdquo;
              </blockquote>
              <figcaption className="mt-3 font-[family-name:var(--font-ui)] text-sm uppercase tracking-widest text-gold">
                {e.ref}
              </figcaption>
            </figure>
          ))}
        </div>
      </section>

      {/* Contents */}
      <section id="contents" className="mx-auto w-full max-w-4xl px-6 py-20">
        <h2 className="text-center font-[family-name:var(--font-display)] text-3xl font-semibold text-ink">
          Contents
        </h2>
        <div className="mx-auto mt-3 mb-12 h-px w-24 bg-gold" />
        <ol className="space-y-1">
          {chapters.map((c) => (
            <li key={c.slug}>
              <Link
                href={`/read/${c.slug}`}
                className="group flex items-baseline gap-4 rounded-lg px-4 py-3 transition hover:bg-parchment-deep/60"
              >
                <span className="w-10 shrink-0 text-right font-[family-name:var(--font-ui)] text-sm tabular-nums text-gold">
                  {c.numeral ?? "✦"}
                </span>
                <span className="min-w-0">
                  <span className="font-[family-name:var(--font-display)] text-xl text-ink group-hover:text-gold">
                    {c.title}
                  </span>
                  {c.subtitle && (
                    <span className="block font-[family-name:var(--font-serif)] text-base italic text-ink-faint">
                      {c.subtitle}
                    </span>
                  )}
                </span>
                <ArrowRight className="ml-auto mt-1 h-4 w-4 shrink-0 self-center text-rule-strong opacity-0 transition group-hover:opacity-100 group-hover:text-gold" />
              </Link>
            </li>
          ))}
        </ol>
      </section>

      <footer className="border-t border-rule px-6 py-10 text-center font-[family-name:var(--font-ui)] text-sm text-ink-faint">
        <Image
          src="/christisgod-logo.png"
          alt=""
          width={32}
          height={32}
          unoptimized
          className="mx-auto mb-3 h-8 w-auto opacity-80"
        />
        <p>
          {bookMeta.title} — {bookMeta.subtitle} · {bookMeta.year}
        </p>
        <p className="mt-1">Scripture quotations from the King James Version.</p>
      </footer>
    </div>
  );
}
