import { ExternalLink } from "lucide-react";
import { timelineEvents } from "@/lib/history-timeline";

const eraClass = {
  "New Testament": "timeline-era-nt",
  "Early Church": "timeline-era-church",
  Council: "timeline-era-council",
} as const;

export function HistoryTimeline() {
  return (
    <ol className="history-timeline" aria-label="Timeline of belief in the divinity of Christ">
      {timelineEvents.map((event, index) => (
        <li key={`${event.date}-${event.title}`} className="timeline-event">
          <div className="timeline-marker" aria-hidden>
            <span>{index + 1}</span>
          </div>
          <article className="timeline-card rounded-2xl border border-rule bg-surface/75 p-6 sm:p-8">
            <div className="flex flex-wrap items-center gap-3">
              <time className="font-[family-name:var(--font-ui)] text-sm font-bold tracking-wide text-gold">{event.date}</time>
              <span className={`timeline-era ${eraClass[event.era]}`}>{event.era}</span>
            </div>
            <h2 className="mt-3 font-[family-name:var(--font-display)] text-2xl font-semibold leading-tight text-ink sm:text-3xl">{event.title}</h2>
            <p className="mt-4 font-[family-name:var(--font-serif)] text-lg leading-relaxed text-ink-soft">{event.witness}</p>
            <div className="mt-5 border-l-2 border-gold/45 pl-4">
              <p className="font-[family-name:var(--font-ui)] text-[0.65rem] font-semibold uppercase tracking-[0.18em] text-vermillion">Why it matters</p>
              <p className="mt-1 font-[family-name:var(--font-serif)] text-base italic leading-relaxed text-ink-faint">{event.significance}</p>
            </div>
            {event.source && (
              <a href={event.source} target="_blank" rel="noreferrer" className="mt-5 inline-flex items-center gap-1.5 font-[family-name:var(--font-ui)] text-xs font-semibold uppercase tracking-wider text-lapis transition hover:text-lapis-bright">
                Read the primary source <ExternalLink className="h-3.5 w-3.5" />
              </a>
            )}
          </article>
        </li>
      ))}
    </ol>
  );
}
