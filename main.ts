import { copyFileSync, mkdirSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const root = dirname(fileURLToPath(import.meta.url));
const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? join(root, "out");
const source = join(root, "entry.png");
const target = join(outputDir, "entry.png");

mkdirSync(outputDir, { recursive: true });
copyFileSync(source, target);

const size = statSync(target).size;
if (size === 0 || size > 1048576) {
  throw new Error(`entry.png has unexpected size: ${size} bytes`);
}

console.log(`wrote ${target} (${size} bytes)`);
