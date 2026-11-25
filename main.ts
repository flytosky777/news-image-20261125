import { copyFile, mkdir, readFile, stat } from "node:fs/promises";
import { createHash } from "node:crypto";
import path from "node:path";
import { fileURLToPath } from "node:url";

const ONE_MIB = 1048576;
const PNG_MAGIC = Buffer.from([
  0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a,
]);

async function run() {
  const repoDir = path.dirname(fileURLToPath(import.meta.url));
  const source = path.join(repoDir, "entry.png");
  const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
  const target = path.join(outDir, "entry.png");

  const info = await stat(source);
  if (info.size > ONE_MIB) {
    throw new Error(`entry.png is ${info.size} bytes, over the 1 MiB cap`);
  }
  const bytes = await readFile(source);
  if (!bytes.subarray(0, 8).equals(PNG_MAGIC)) {
    throw new Error("entry.png does not start with the PNG magic bytes");
  }
  await mkdir(outDir, { recursive: true });
  await copyFile(source, target);
  // Prove the copy landed intact: same size and same sha256 as the source.
  const written = await readFile(target);
  if (written.length !== info.size) {
    throw new Error(`copied ${written.length} bytes, expected ${info.size}`);
  }
  const digest = createHash("sha256").update(written).digest("hex");
  console.log(`wrote ${target} (${info.size} bytes) sha256 ${digest}`);
}

await run();
