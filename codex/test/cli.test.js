import assert from "node:assert/strict";
import { execFile } from "node:child_process";
import { mkdtemp, readFile, rm, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import test from "node:test";
import path from "node:path";
import { promisify } from "node:util";

const execFileAsync = promisify(execFile);
const repoRoot = path.resolve(import.meta.dirname, "../..");
const cliPath = path.join(repoRoot, "codex/bin/cleancode-codex.js");

async function runCli(args, cwd) {
  return execFileAsync(process.execPath, [cliPath, ...args], { cwd });
}

async function withTempProject(testBody) {
  const projectPath = await mkdtemp(path.join(tmpdir(), "cleancode-codex-"));
  try {
    await testBody(projectPath);
  } finally {
    await rm(projectPath, { recursive: true, force: true });
  }
}

test("init writes Codex templates and prints all 15 rules", async () => {
  await withTempProject(async (projectPath) => {
    const { stdout } = await runCli(["init"], projectPath);

    const agents = await readFile(path.join(projectPath, "AGENTS.md"), "utf8");
    const rules = await readFile(path.join(projectPath, ".cleancode-rules.md"), "utf8");

    assert.match(agents, /Agent Instructions/);
    assert.match(rules, /## 15\. Clean Module & Folder Structure/);
    assert.match(stdout, /Loaded 15 clean code rules/);
    assert.match(stdout, /1\. No file exceeds 300 lines \(File Size\)/);
    assert.match(stdout, /15\. Clean module & folder structure \(Cohesion at Package Level\)/);
  });
});

test("init refuses to overwrite existing files without force", async () => {
  await withTempProject(async (projectPath) => {
    await writeFile(path.join(projectPath, "AGENTS.md"), "custom\n");

    await assert.rejects(
      runCli(["init"], projectPath),
      (error) =>
        error.code === 1 &&
        /Refusing to overwrite AGENTS\.md/.test(error.stderr),
    );

    assert.equal(await readFile(path.join(projectPath, "AGENTS.md"), "utf8"), "custom\n");
  });
});

test("init --force overwrites existing templates", async () => {
  await withTempProject(async (projectPath) => {
    await writeFile(path.join(projectPath, "AGENTS.md"), "custom\n");

    await runCli(["init", "--force"], projectPath);

    const agents = await readFile(path.join(projectPath, "AGENTS.md"), "utf8");
    assert.match(agents, /Clean Code Standards/);
  });
});

test("rules prints the 15 rules in plain language with formal terms", async () => {
  await withTempProject(async (projectPath) => {
    const { stdout } = await runCli(["rules"], projectPath);

    const lines = stdout.split("\n").filter((line) => /^\d+\./.test(line));

    assert.equal(lines.length, 15);
    assert.equal(lines[0], "1. No file exceeds 300 lines (File Size)");
    assert.equal(lines[10], "11. Don't reach through objects (Law of Demeter)");
  });
});

test("update preserves edited rules and writes latest rules beside them", async () => {
  await withTempProject(async (projectPath) => {
    await runCli(["init"], projectPath);
    await writeFile(
      path.join(projectPath, ".cleancode-rules.md"),
      "# Project-specific clean code rules\n\nCustom threshold: 250 lines.\n",
    );

    const { stdout } = await runCli(["update"], projectPath);

    const currentRules = await readFile(path.join(projectPath, ".cleancode-rules.md"), "utf8");
    const latestRules = await readFile(path.join(projectPath, ".cleancode-rules.md.latest"), "utf8");

    assert.match(stdout, /Local .cleancode-rules.md has edits/);
    assert.match(currentRules, /Custom threshold: 250 lines/);
    assert.match(latestRules, /Clean Code Rules — Canonical Ruleset/);
  });
});
