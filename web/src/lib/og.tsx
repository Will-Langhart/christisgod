import { readFileSync } from "node:fs";
import { join } from "node:path";
import { ImageResponse } from "next/og";

export const OG_SIZE = { width: 1200, height: 630 };
export const OG_CONTENT_TYPE = "image/png";

const FONT_DIR = join(process.cwd(), "src", "app", "_og");

// Brand palette (light/parchment theme).
const PARCHMENT = "#f7f1e6";
const PARCHMENT_DEEP = "#efe6d4";
const INK = "#211c15";
const INK_FAINT = "#6f6451";
const GOLD = "#9a7b3f";
const RULE = "#cbbb98";

let fonts: { name: string; data: Buffer; weight: 400 | 600; style: "normal" }[] | null = null;

function loadFonts() {
  if (!fonts) {
    fonts = [
      {
        name: "Cormorant",
        data: readFileSync(join(FONT_DIR, "Cormorant-SemiBold.ttf")),
        weight: 600,
        style: "normal",
      },
      {
        name: "EB Garamond",
        data: readFileSync(join(FONT_DIR, "EBGaramond-Regular.ttf")),
        weight: 400,
        style: "normal",
      },
    ];
  }
  return fonts;
}

type OgOptions = {
  /** Small uppercase eyebrow, e.g. "Chapter III". */
  eyebrow?: string;
  /** The large display title. */
  title: string;
  /** Optional italic subtitle / hook line. */
  subtitle?: string;
};

/**
 * Renders the shared gold-on-parchment OG card used across the site.
 */
export function renderOgImage({ eyebrow, title, subtitle }: OgOptions) {
  return new ImageResponse(
    (
      <div
        style={{
          width: "100%",
          height: "100%",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          padding: "72px 96px",
          background: `linear-gradient(150deg, ${PARCHMENT} 0%, ${PARCHMENT_DEEP} 100%)`,
          fontFamily: "EB Garamond",
          position: "relative",
        }}
      >
        {/* Inner gold frame */}
        <div
          style={{
            position: "absolute",
            inset: 36,
            border: `2px solid ${RULE}`,
            borderRadius: 8,
          }}
        />
        {/* Cross mark */}
        <div
          style={{
            fontSize: 92,
            color: GOLD,
            lineHeight: 1,
            marginBottom: 28,
          }}
        >
          ✠
        </div>
        {eyebrow ? (
          <div
            style={{
              fontFamily: "EB Garamond",
              fontSize: 26,
              letterSpacing: 8,
              textTransform: "uppercase",
              color: GOLD,
              marginBottom: 20,
            }}
          >
            {eyebrow}
          </div>
        ) : null}
        <div
          style={{
            fontFamily: "Cormorant",
            fontWeight: 600,
            fontSize: title.length > 38 ? 76 : 96,
            lineHeight: 1.05,
            color: INK,
            textAlign: "center",
            maxWidth: 960,
          }}
        >
          {title}
        </div>
        {subtitle ? (
          <div
            style={{
              fontFamily: "EB Garamond",
              fontStyle: "italic",
              fontSize: 36,
              color: INK_FAINT,
              textAlign: "center",
              marginTop: 24,
              maxWidth: 880,
            }}
          >
            {subtitle}
          </div>
        ) : null}
        {/* Gold rule + wordmark */}
        <div style={{ width: 120, height: 2, background: GOLD, marginTop: 40 }} />
        <div
          style={{
            fontFamily: "EB Garamond",
            fontSize: 24,
            letterSpacing: 4,
            textTransform: "uppercase",
            color: INK_FAINT,
            marginTop: 28,
          }}
        >
          Christ Is God · The Divinity of Christ
        </div>
      </div>
    ),
    {
      ...OG_SIZE,
      fonts: loadFonts().map(({ name, data, weight, style }) => ({
        name,
        data: data as unknown as ArrayBuffer,
        weight,
        style,
      })),
    },
  );
}
