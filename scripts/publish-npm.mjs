#!/usr/bin/env node
import { readFileSync, readdirSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { execFileSync } from 'node:child_process';
import { pathToFileURL } from 'node:url';

const registry = 'https://registry.npmjs.org';

export async function registryVersion(name, version, request = fetch) {
  const response = await request(`${registry}/${encodeURIComponent(name)}/${version}`);
  if (response.status === 404) return null;
  if (!response.ok) throw new Error(`npm registry returned ${response.status} for ${name}@${version}`);
  return response.json();
}

export function verifyIntegrity(metadata, integrity, name, version) {
  if (metadata?.name !== name || metadata?.version !== version || metadata?.dist?.integrity !== integrity) {
    throw new Error(`Registry contents do not match the release tarball: ${name}@${version}`);
  }
}

export async function publishPackage({ name, version, file, integrity }, {
  lookup = registryVersion,
  publish = file => execFileSync('npm', ['publish', file, '--access', 'public', '--provenance', '--registry', registry], { stdio: 'inherit' }),
  pause = () => new Promise(resolve => setTimeout(resolve, 5000)),
} = {}) {
  const existing = await lookup(name, version);
  if (existing) {
    verifyIntegrity(existing, integrity, name, version);
    console.log(`${name}@${version} already published with matching integrity.`);
    return;
  }
  publish(file);
  for (let attempt = 0; attempt < 60; attempt++) {
    const metadata = await lookup(name, version);
    if (metadata) {
      verifyIntegrity(metadata, integrity, name, version);
      console.log(`Verified ${name}@${version} on npm.`);
      return;
    }
    await pause();
  }
  throw new Error(`Published version not visible on npm: ${name}@${version}`);
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  const files = readdirSync('release').filter(file => file.endsWith('.tgz')).sort();
  if (files.length !== 1) throw new Error('Expected exactly one release tarball');
  for (const filename of files) {
    const file = `release/${filename}`;
    const { name, version } = JSON.parse(execFileSync('tar', ['-xOf', file, 'package/package.json'], { encoding: 'utf8' }));
    if (name !== '@hugocxl/iconscxl') {
      throw new Error(`Unexpected package: ${name}`);
    }
    const integrity = `sha512-${createHash('sha512').update(readFileSync(file)).digest('base64')}`;
    await publishPackage({ name, version, file, integrity });
  }
}
