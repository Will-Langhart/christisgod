import Link from "next/link";
import Image from "next/image";
import { ArrowRight, BookOpen, ChevronDown } from "lucide-react";
import { bookMeta } from "@/lib/book-meta";
import { chapters } from "@/lib/chapters";

export function Hero() {
  const first = chapters[0];

  return (
    <section className="hero">
      {/* Animated background layers */}
      <div className="hero-base" aria-hidden />
      <div className="hero-rays" aria-hidden />
      <div className="hero-cross" aria-hidden>
        <Image
          src="/christisgod-logo.png"
          alt=""
          width={640}
          height={640}
          priority
          unoptimized
          className="hero-cross-img"
        />
      </div>
      <div className="hero-blob hero-blob-1" aria-hidden />
      <div className="hero-blob hero-blob-2" aria-hidden />
      <div className="hero-vignette" aria-hidden />

      {/* Foreground */}
      <div className="relative z-10 flex flex-col items-center">
        <p
          className="hero-rise font-[family-name:var(--font-ui)] text-xs font-semibold uppercase tracking-[0.45em] text-gold"
          style={{ animationDelay: "0.05s" }}
        >
          {bookMeta.year} &middot; An Apologetic
        </p>

        <h1
          className="hero-rise hero-title mt-6 text-7xl sm:text-8xl md:text-[8.5rem]"
          style={{ animationDelay: "0.15s" }}
        >
          {bookMeta.title}
        </h1>

        <p
          className="hero-rise mt-3 font-[family-name:var(--font-display)] text-3xl font-medium italic text-gold sm:text-4xl"
          style={{ animationDelay: "0.3s" }}
        >
          {bookMeta.subtitle}
        </p>

        <p
          className="hero-rise mx-auto mt-7 max-w-xl font-[family-name:var(--font-serif)] text-lg leading-relaxed text-ink-soft"
          style={{ animationDelay: "0.45s" }}
        >
          {bookMeta.tagline}
        </p>

        <div
          className="hero-rise mt-11 flex flex-wrap items-center justify-center gap-3"
          style={{ animationDelay: "0.6s" }}
        >
          <Link
            href={`/read/${first.slug}`}
            className="btn-sheen inline-flex items-center gap-2 rounded-full bg-gold px-8 py-3.5 font-[family-name:var(--font-ui)] text-sm font-semibold text-parchment shadow-xl shadow-gold/30 transition hover:bg-gold-bright hover:shadow-gold/40"
          >
            Begin Reading <ArrowRight className="h-4 w-4" />
          </Link>
          <a
            href="#contents"
            className="inline-flex items-center gap-2 rounded-full border border-rule-strong bg-surface/40 px-8 py-3.5 font-[family-name:var(--font-ui)] text-sm font-semibold text-ink-soft backdrop-blur-sm transition hover:border-gold hover:text-gold"
          >
            <BookOpen className="h-4 w-4" /> Table of Contents
          </a>
        </div>
      </div>

      <a
        href="#epigraphs"
        aria-label="Scroll to read more"
        className="hero-scrollcue z-10"
      >
        <ChevronDown className="h-6 w-6" />
      </a>
    </section>
  );
}
