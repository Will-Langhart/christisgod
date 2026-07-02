import type { Metadata } from "next";
import { GuidedCase } from "@/components/guided-case";
import { site } from "@/lib/site";

export const metadata: Metadata = {
  title: "The 10-Minute Case That Jesus Is God",
  description: "Examine seven converging lines of scriptural and historical evidence for the divinity of Jesus Christ.",
  alternates: { canonical: "/case" },
  openGraph: {
    title: "The 10-Minute Case That Jesus Is God",
    description: "Follow the evidence and judge the cumulative case for yourself.",
    url: `${site.url}/case`,
    type: "article",
  },
};

export default function CasePage() {
  return <GuidedCase />;
}
