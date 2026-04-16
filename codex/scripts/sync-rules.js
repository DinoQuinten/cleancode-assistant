#!/usr/bin/env node

import { mkdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";

const packageRoot = path.resolve(import.meta.dirname, "..");
const repoRoot = path.resolve(packageRoot, "..");
const templatesDir = path.join(packageRoot, "templates");

const sourceCandidates = {
  rules: [
    path.join(repoRoot, "cleancode/skills/init/references/rules.md"),
    path.join(repoRoot, "claude-code/skills/init/references/rules.md"),
    path.join(repoRoot, "skills/init/references/rules.md"),
  ],
  agents: [
    path.join(repoRoot, "cleancode/skills/setup/references/codex-agents.md"),
    path.join(repoRoot, "claude-code/skills/setup/references/codex-agents.md"),
    path.join(repoRoot, "skills/setup/references/codex-agents.md"),
  ],
};

async function readFirstExisting(paths) {
  for (const filePath of paths) {
    try {
      return {
        filePath,
        content: await readFile(filePath, "utf8"),
      };
    } catch (error) {
      if (error.code !== "ENOENT") {
        throw error;
      }
    }
  }

  throw new Error(`Could not find any source file:\n${paths.join("\n")}`);
}

function extractMarkdownFence(content, sourcePath) {
  const match = content.match(/```markdown\r?\n([\s\S]*?)\r?\n```/);
  if (!match) {
    throw new Error(`Could not find a markdown code fence in ${sourcePath}`);
  }

  return `${match[1].trimEnd()}\n`;
}

const rules = await readFirstExisting(sourceCandidates.rules);
const agents = await readFirstExisting(sourceCandidates.agents);

await mkdir(templatesDir, { recursive: true });
await writeFile(path.join(templatesDir, ".cleancode-rules.md"), rules.content);
await writeFile(path.join(templatesDir, "AGENTS.md"), extractMarkdownFence(agents.content, agents.filePath));

console.log(`Synced rules from ${path.relative(repoRoot, rules.filePath)}`);
console.log(`Synced AGENTS.md from ${path.relative(repoRoot, agents.filePath)}`);
