#!/usr/bin/env node

import { constants } from "node:fs";
import { access, copyFile, readFile, writeFile } from "node:fs/promises";
import path from "node:path";

const packageRoot = path.resolve(import.meta.dirname, "..");
const templatesDir = path.join(packageRoot, "templates");

const templateFiles = [
  { source: "AGENTS.md", target: "AGENTS.md" },
  { source: ".cleancode-rules.md", target: ".cleancode-rules.md" },
];

const cleanCodeRules = [
  "No file exceeds 300 lines (File Size)",
  "No function exceeds 40 lines (Function / Method Size)",
  "No more than 4 parameters (Parameter Count)",
  "No nesting deeper than 4 levels (Nesting Depth)",
  "All names reveal intent (Meaningful Naming)",
  "Apply SOLID principles and prefer small classes (Object-Oriented Principles)",
  "Every public TypeScript API has an explicit interface (Interfaces)",
  "Do not duplicate logic (DRY)",
  "Comments explain why, not what (Comments)",
  "A new contributor understands a file in 5 minutes (Principle of Least Surprise)",
  "Don't reach through objects (Law of Demeter)",
  "Check inputs early, never hide errors (Fail Fast / Defensive Programming)",
  "Only build what you need; leave code cleaner than you found it (YAGNI + Boy Scout Rule)",
  "Tests should be as clean as the code they test (Arrange / Act / Assert)",
  "Clean module & folder structure (Cohesion at Package Level)",
];

function usage() {
  return `Usage: cleancode-codex <command> [options]

Commands:
  init [--force]  Copy AGENTS.md and .cleancode-rules.md into the current project
  update          Refresh AGENTS.md and offer latest rules without overwriting edits
  rules           Print the 15 clean code rules
`;
}

async function exists(filePath) {
  try {
    await access(filePath, constants.F_OK);
    return true;
  } catch {
    return false;
  }
}

function printRules(header = "Loaded 15 clean code rules:") {
  console.log(header);
  cleanCodeRules.forEach((rule, index) => {
    console.log(`${index + 1}. ${rule}`);
  });
}

async function initProject({ force }) {
  const cwd = process.cwd();

  for (const file of templateFiles) {
    const targetPath = path.join(cwd, file.target);
    if (!force && await exists(targetPath)) {
      throw new Error(`Refusing to overwrite ${file.target}. Re-run with --force to replace it.`);
    }
  }

  for (const file of templateFiles) {
    await copyFile(path.join(templatesDir, file.source), path.join(cwd, file.target));
  }

  console.log("cleancode-codex init complete");
  console.log("Wrote AGENTS.md and .cleancode-rules.md");
  printRules();
}

async function readTemplate(name) {
  return readFile(path.join(templatesDir, name), "utf8");
}

async function updateProject() {
  const cwd = process.cwd();
  const agentsTarget = path.join(cwd, "AGENTS.md");
  const rulesTarget = path.join(cwd, ".cleancode-rules.md");
  const latestRulesTarget = path.join(cwd, ".cleancode-rules.md.latest");
  const latestAgents = await readTemplate("AGENTS.md");
  const latestRules = await readTemplate(".cleancode-rules.md");

  await writeFile(agentsTarget, latestAgents);
  console.log("Updated AGENTS.md from the cleancode-codex package templates.");

  if (!await exists(rulesTarget)) {
    await writeFile(rulesTarget, latestRules);
    console.log("Wrote .cleancode-rules.md.");
    return;
  }

  const currentRules = await readFile(rulesTarget, "utf8");
  if (currentRules === latestRules) {
    await writeFile(rulesTarget, latestRules);
    console.log(".cleancode-rules.md already matches the latest template.");
    return;
  }

  await writeFile(latestRulesTarget, latestRules);
  console.log("Local .cleancode-rules.md has edits; preserved it and wrote .cleancode-rules.md.latest for review.");
}

async function main() {
  const [command, ...args] = process.argv.slice(2);

  try {
    if (command === "init") {
      await initProject({ force: args.includes("--force") });
      return;
    }

    if (command === "update") {
      await updateProject();
      return;
    }

    if (command === "rules") {
      printRules("15 clean code rules:");
      return;
    }

    console.log(usage());
    process.exitCode = command ? 1 : 0;
  } catch (error) {
    console.error(error.message);
    process.exitCode = 1;
  }
}

await main();
