// Exports the curated objections to shared/objections.json for the Python
// runner (service/runner). Single source of truth: objections.ts stays the
// authoritative list; this just serializes it. Relies on Node's native TS
// import (Node 22+ type stripping).
//
// Run:  node scripts/export-objections.mjs
import { writeFile, mkdir } from "node:fs/promises";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { objections } from "../src/lib/objections.ts";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const OUT_DIR = join(ROOT, "..", "shared");
await mkdir(OUT_DIR, { recursive: true });
await writeFile(
  join(OUT_DIR, "objections.json"),
  JSON.stringify(objections, null, 2) + "\n",
  "utf8",
);
console.log(`✓ wrote ${objections.length} objections → ${join(OUT_DIR, "objections.json")}`);
