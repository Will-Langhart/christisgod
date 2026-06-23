import type { NextConfig } from "next";
import path from "node:path";
import createMDX from "@next/mdx";

const nextConfig: NextConfig = {
  pageExtensions: ["ts", "tsx", "mdx"],
};

// Absolute path so @next/mdx's require.resolve finds the plugin regardless of
// which MDX file's directory it resolves from.
const scripturePlugin = path.resolve(
  process.cwd(),
  "src/lib/rehype-scripture.mjs",
);

// Turbopack requires MDX plugin options to be serializable, so plugins are
// referenced by string specifier (not imported function references).
const withMDX = createMDX({
  options: {
    remarkPlugins: [["remark-gfm", {}]],
    rehypePlugins: [
      ["rehype-slug", {}],
      [scripturePlugin, {}],
      [
        "rehype-autolink-headings",
        {
          behavior: "append",
          properties: { className: ["heading-anchor"], ariaHidden: true, tabIndex: -1 },
          content: { type: "text", value: "#" },
        },
      ],
    ],
  },
});

export default withMDX(nextConfig);
