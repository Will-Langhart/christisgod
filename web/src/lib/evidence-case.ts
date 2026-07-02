import type { LucideIcon } from "lucide-react";
import {
  BookMarked,
  Crown,
  Fingerprint,
  History,
  Orbit,
  Sparkles,
} from "lucide-react";

export type EvidenceStrand = {
  title: string;
  summary: string;
  references: string[];
  href: string;
  icon: LucideIcon;
};

export const evidenceStrands: EvidenceStrand[] = [
  {
    title: "He bears God’s names",
    summary: "The New Testament directly calls Jesus God and Lord.",
    references: ["John 1:1", "John 20:28", "Romans 9:5", "Titus 2:13"],
    href: "/read/iv-jesus-is-god",
    icon: Fingerprint,
  },
  {
    title: "He does God’s works",
    summary: "Creation, forgiveness, judgment, and the giving of life belong to him.",
    references: ["Colossians 1:16–17", "Mark 2:5–12", "John 5:21–23"],
    href: "/read/vi-the-divine-works-of-christ",
    icon: Sparkles,
  },
  {
    title: "He receives God’s worship",
    summary: "Jesus accepts the honor Scripture reserves for God alone.",
    references: ["Matthew 14:33", "Hebrews 1:6", "Revelation 5:11–14"],
    href: "/read/viii-worship-given-to-christ",
    icon: Crown,
  },
  {
    title: "Yahweh’s words point to him",
    summary: "New Testament writers apply Old Testament passages about Yahweh to Jesus.",
    references: ["Isaiah 40:3 / Mark 1:3", "Joel 2:32 / Romans 10:13"],
    href: "/parallels",
    icon: BookMarked,
  },
  {
    title: "He shares God’s identity",
    summary: "Jesus is distinct from the Father, yet included within the identity of the one God.",
    references: ["Matthew 28:19", "1 Corinthians 8:6", "John 17:5"],
    href: "/read/x-the-holy-trinity",
    icon: Orbit,
  },
  {
    title: "The confession is early",
    summary: "Christ’s divinity appears in the earliest Christian testimony—not as a late invention.",
    references: ["Philippians 2:5–11", "1 Corinthians 8:6", "Pliny, c. AD 112"],
    href: "/read/xi-how-early-is-this-belief",
    icon: History,
  },
];
