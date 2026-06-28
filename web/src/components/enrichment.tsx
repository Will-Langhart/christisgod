import Link from "next/link";
import type { ReactNode } from "react";
import { chapters } from "@/lib/chapters";

/* ----------------------------------------------------------------------------
   KeyTakeaways — a titled summary card distilling a chapter's argument.
   Usage in MDX:
     <KeyTakeaways points={["First point", "Second point"]} />
---------------------------------------------------------------------------- */
export function KeyTakeaways({
  points,
  title = "In Brief",
}: {
  points: string[];
  title?: string;
}) {
  return (
    <aside className="key-takeaways" role="note" aria-label={title}>
      <p className="key-takeaways__title">{title}</p>
      <ul className="key-takeaways__list">
        {points.map((p, i) => (
          <li key={i}>{p}</li>
        ))}
      </ul>
    </aside>
  );
}

/* ----------------------------------------------------------------------------
   WordStudy — an original-language gloss (Greek/Hebrew) shown as a sidebar card.
   Usage:
     <WordStudy term="θεός" translit="theos" gloss="God" lang="Greek">
       Explanatory note about the word's force in this passage.
     </WordStudy>
---------------------------------------------------------------------------- */
export function WordStudy({
  term,
  translit,
  gloss,
  lang,
  strongs,
  children,
}: {
  term: string;
  translit?: string;
  gloss?: string;
  lang?: "Greek" | "Hebrew" | "Aramaic" | string;
  strongs?: string;
  children?: ReactNode;
}) {
  return (
    <aside className="word-study" aria-label={`Word study: ${term}`}>
      <p className="word-study__eyebrow">
        {lang ?? "Original language"}
        {strongs ? <span className="word-study__strongs"> · {strongs}</span> : null}
      </p>
      <p
        className="word-study__term"
        lang={
          lang === "Hebrew"
            ? "he"
            : lang === "Aramaic"
              ? "arc"
              : lang === "Arabic"
                ? "ar"
                : "el"
        }
        dir={lang === "Hebrew" || lang === "Arabic" ? "rtl" : undefined}
      >
        {term}
      </p>
      {(translit || gloss) && (
        <p className="word-study__line">
          {translit ? <span className="word-study__translit">{translit}</span> : null}
          {translit && gloss ? <span className="word-study__sep"> — </span> : null}
          {gloss ? <span className="word-study__gloss">“{gloss}”</span> : null}
        </p>
      )}
      {children ? <div className="word-study__note">{children}</div> : null}
    </aside>
  );
}

/* ----------------------------------------------------------------------------
   PullQuote — a large, set-apart quotation to give the eye a resting point.
   Usage:
     <PullQuote cite="Tertullian, Against Praxeas">When Christ is considered
     in Himself, Paul can call Him God.</PullQuote>
---------------------------------------------------------------------------- */
export function PullQuote({
  children,
  cite,
}: {
  children: ReactNode;
  cite?: string;
}) {
  return (
    <figure className="pull-quote">
      <blockquote>{children}</blockquote>
      {cite ? <figcaption>{cite}</figcaption> : null}
    </figure>
  );
}

/* ----------------------------------------------------------------------------
   SeeAlso — cross-reference chips linking to related chapters by slug.
   Usage:
     <SeeAlso slugs={["x-the-holy-trinity", "iv-jesus-is-god"]} />
---------------------------------------------------------------------------- */
export function SeeAlso({ slugs }: { slugs: string[] }) {
  const items = slugs
    .map((slug) => chapters.find((c) => c.slug === slug))
    .filter((c): c is (typeof chapters)[number] => Boolean(c));

  if (items.length === 0) return null;

  return (
    <aside className="see-also" aria-label="Related chapters">
      <span className="see-also__label">See also</span>
      <span className="see-also__chips">
        {items.map((c) => (
          <Link key={c.slug} href={`/read/${c.slug}`} className="see-also__chip">
            {c.numeral ? <span className="see-also__num">{c.numeral}</span> : null}
            {c.title}
          </Link>
        ))}
      </span>
    </aside>
  );
}
