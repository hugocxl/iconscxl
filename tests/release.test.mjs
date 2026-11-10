import { test } from 'node:test';
import assert from 'node:assert/strict';
import { releaseVersion, stampVersion } from '../scripts/prepare-release.mjs';

test('release versions are deterministic on retry and distinct across runs', () => {
  assert.equal(releaseVersion('2'), '0.1.2');
  assert.equal(releaseVersion('2'), releaseVersion(2));
  assert.notEqual(releaseVersion(2), releaseVersion(3));
  for (const invalid of [undefined, 0, -1, '1.2', '01', 'abc', '9007199254740992']) {
    assert.throws(() => releaseVersion(invalid));
  }
});

test('release stamping keeps package and lockfile versions aligned', () => {
  const manifests = {
    'packages/iconscxl': { name: '@hugocxl/iconscxl', version: '0.1.0' },
  };
  const lock = { packages: structuredClone(manifests), lockfileVersion: 3 };
  stampVersion(manifests, lock, '0.1.8');
  assert.deepEqual(lock.packages, manifests);
  assert.equal(manifests['packages/iconscxl'].version, '0.1.8');
  assert.equal(lock.lockfileVersion, 3);
  assert.throws(() => stampVersion(manifests, { packages: {} }, '0.1.9'));
});

import { mkdtempSync, mkdirSync, writeFileSync, readFileSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, resolve } from 'node:path';
import { execFileSync, spawnSync } from 'node:child_process';

test('publication recovers drafts, skips published releases and rejects tag collisions', () => {
  const directory = mkdtempSync(join(tmpdir(), 'cxl-release-'));
  const script = resolve('scripts/publish-release.sh');
  try {
    const git = (...args) => execFileSync('git', args, { cwd: directory, encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] }).trim();
    git('init', '--bare', 'origin.git');
    git('init', 'work');
    const work = join(directory, 'work');
    const workGit = (...args) => execFileSync('git', ['-C', work, ...args], { encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] }).trim();
    workGit('config', 'user.email', 'test@example.com');
    workGit('config', 'user.name', 'Test');
    workGit('commit', '--allow-empty', '-m', 'Source');
    workGit('remote', 'add', 'origin', join(directory, 'origin.git'));
    mkdirSync(join(directory, 'bin'));
    mkdirSync(join(work, 'release'));
    for (const file of ['web.tgz', 'native.tgz', 'SHA256SUMS']) writeFileSync(join(work, 'release', file), 'test');
    const state = join(directory, 'state');
    const calls = join(directory, 'calls');
    writeFileSync(state, 'missing');
    writeFileSync(calls, '');
    writeFileSync(join(directory, 'bin/gh'), `#!/usr/bin/env node
const fs = require('node:fs');
const args = process.argv.slice(2);
fs.appendFileSync(process.env.CALLS, args.join(' ') + '\\n');
const state = fs.readFileSync(process.env.STATE, 'utf8');
if (args[1] === 'view') {
  if (state === 'missing') process.exit(1);
  console.log(args.includes('--jq') ? String(state === 'draft') : JSON.stringify({isDraft: state === 'draft'}));
}
if (args[1] === 'create') fs.writeFileSync(process.env.STATE, 'draft');
if (args[1] === 'upload' && process.env.FAIL_UPLOAD === '1') process.exit(1);
if (args[1] === 'edit') fs.writeFileSync(process.env.STATE, 'published');
`, { mode: 0o755 });
    const env = { ...process.env, PATH: `${join(directory, 'bin')}:${process.env.PATH}`, STATE: state, CALLS: calls,
      GH_REPO: 'test/icons', GITHUB_SHA: workGit('rev-parse', 'HEAD'), RELEASE_TAG: 'v0.1.2' };
    const run = extra => spawnSync('bash', [script], { cwd: work, env: { ...env, ...extra }, encoding: 'utf8' });
    const failedUpload = run({ FAIL_UPLOAD: '1' });
    assert.notEqual(failedUpload.status, 0);
    assert.equal(readFileSync(state, 'utf8'), 'draft', failedUpload.stderr);
    assert.equal(run().status, 0);
    assert.equal(readFileSync(state, 'utf8'), 'published');
    writeFileSync(calls, '');
    assert.equal(run().status, 0);
    assert.doesNotMatch(readFileSync(calls, 'utf8'), /upload|edit|create/);
    workGit('commit', '--allow-empty', '-m', 'Different source');
    assert.notEqual(run({ GITHUB_SHA: workGit('rev-parse', 'HEAD') }).status, 0);
  } finally {
    rmSync(directory, { recursive: true, force: true });
  }
});
