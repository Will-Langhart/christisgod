"use client";

import { useState } from "react";
import Link from "next/link";
import { ArrowLeft, ArrowRight, BookOpen, RotateCcw } from "lucide-react";
import { guidedCaseSteps } from "@/lib/guided-case";

export function GuidedCase() {
  const [current, setCurrent] = useState(0);
  const step = guidedCaseSteps[current];
  const isLast = current === guidedCaseSteps.length - 1;
  const progress = ((current + 1) / guidedCaseSteps.length) * 100;

  return (
    <div className="guided-case-shell">
      <div className="guided-case-progress" aria-hidden>
        <span style={{ width: `${progress}%` }} />
      </div>

      <header className="flex items-center justify-between px-5 py-5 sm:px-8">
        <Link href="/" className="inline-flex items-center gap-1.5 font-[family-name:var(--font-ui)] text-xs font-semibold uppercase tracking-wider text-ink-faint transition hover:text-gold">
          <ArrowLeft className="h-3.5 w-3.5" /> Home
        </Link>
        <span className="font-[family-name:var(--font-ui)] text-xs font-semibold tabular-nums tracking-wider text-ink-faint">
          {current + 1} / {guidedCaseSteps.length}
        </span>
      </header>

      <main className="mx-auto flex w-full max-w-4xl flex-1 items-center px-6 py-10 sm:py-14">
        <article key={current} className="guided-case-step w-full">
          <div className="grid items-center gap-10 lg:grid-cols-[1.05fr_0.95fr] lg:gap-16">
            <div>
              <p className="font-[family-name:var(--font-ui)] text-xs font-semibold uppercase tracking-[0.28em] text-vermillion">
                {step.eyebrow}
              </p>
              <h1 className="mt-4 font-[family-name:var(--font-display)] text-4xl font-semibold leading-[1.05] text-ink sm:text-6xl">
                {step.title}
              </h1>
              <p className="mt-6 font-[family-name:var(--font-serif)] text-xl italic leading-relaxed text-gold sm:text-2xl">
                {step.thesis}
              </p>
              <p className="mt-6 font-[family-name:var(--font-serif)] text-lg leading-relaxed text-ink-soft">
                {step.explanation}
              </p>
            </div>

            <div className="guided-scripture rounded-2xl border border-gold/30 p-7 sm:p-9">
              <span className="font-[family-name:var(--font-display)] text-6xl leading-none text-gold/25" aria-hidden>“</span>
              <blockquote className="-mt-4 font-[family-name:var(--font-serif)] text-2xl italic leading-relaxed text-ink">
                {step.quotation}
              </blockquote>
              <p className="mt-5 font-[family-name:var(--font-ui)] text-xs font-semibold uppercase tracking-[0.2em] text-gold">
                {step.reference}
              </p>
              <div className="mt-7 border-t border-rule pt-5">
                <p className="font-[family-name:var(--font-ui)] text-[0.65rem] font-semibold uppercase tracking-widest text-ink-faint">Read alongside</p>
                <ul className="mt-3 flex flex-wrap gap-2">
                  {step.supporting.map((item) => (
                    <li key={item} className="rounded-full border border-rule bg-parchment/60 px-3 py-1 font-[family-name:var(--font-ui)] text-[0.7rem] text-ink-faint">{item}</li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        </article>
      </main>

      <footer className="border-t border-rule bg-surface/45 px-5 py-5 backdrop-blur-sm sm:px-8">
        <div className="mx-auto flex max-w-4xl items-center justify-between gap-4">
          <button
            type="button"
            onClick={() => setCurrent((value) => Math.max(0, value - 1))}
            disabled={current === 0}
            className="guided-nav-button"
          >
            <ArrowLeft className="h-4 w-4" /> Back
          </button>

          {isLast ? (
            <div className="flex gap-2">
              <button type="button" onClick={() => setCurrent(0)} className="guided-nav-button hidden sm:inline-flex">
                <RotateCcw className="h-4 w-4" /> Revisit
              </button>
              <Link href="/read/xv-a-compact-apologetic-case" className="guided-nav-primary">
                Read the full case <BookOpen className="h-4 w-4" />
              </Link>
            </div>
          ) : (
            <button type="button" onClick={() => setCurrent((value) => Math.min(guidedCaseSteps.length - 1, value + 1))} className="guided-nav-primary">
              Continue <ArrowRight className="h-4 w-4" />
            </button>
          )}
        </div>
      </footer>
    </div>
  );
}
