import type { Metadata } from "next";
import { DialogueExplorer } from "@/components/dialogue-explorer";
import { LiveDebate } from "@/components/live-debate";
import { site } from "@/lib/site";

export const metadata: Metadata = {
  title: "Test the Case — Dialogues",
  description:
    "Careful, fully cited answers to the strongest objections against the deity of Christ, voiced by a skeptic, a Muslim, a Jehovah's Witness, and an honest seeker.",
  alternates: { canonical: "/dialogues" },
  openGraph: {
    title: "Test the Case — Dialogues",
    description:
      "Read careful, KJV-grounded responses to the hardest objections against the divinity of Jesus Christ.",
    url: `${site.url}/dialogues`,
    type: "article",
  },
};

export default function DialoguesPage() {
  return (
    <>
      <DialogueExplorer />
      <LiveDebate />
    </>
  );
}
