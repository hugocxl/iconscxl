import { test } from 'node:test';
import assert from 'node:assert/strict';
import { publishPackage, registryVersion } from '../scripts/publish-npm.mjs';

const artifact = { name: '@hugocxl/iconscxl', version: '0.1.4', file: 'release/web.tgz', integrity: 'sha512-example' };
const metadata = { name: artifact.name, version: artifact.version, dist: { integrity: artifact.integrity } };

test('a retry skips the package already published and checks its integrity', async () => {
  let published = false;
  await publishPackage(artifact, { lookup: async () => metadata, publish: () => { published = true; } });
  assert.equal(published, false);
  await assert.rejects(publishPackage(artifact, {
    lookup: async () => ({ ...metadata, dist: { integrity: 'different' } }),
    publish: () => assert.fail('Must not overwrite an existing version'),
  }), /do not match/);
});

test('a new package is published then verified, allowing registry propagation', async () => {
  let requests = 0;
  const published = [];
  await publishPackage(artifact, {
    lookup: async () => ++requests < 3 ? null : metadata,
    publish: file => published.push(file),
    pause: async () => {},
  });
  assert.deepEqual(published, [artifact.file]);
  assert.equal(requests, 3);
});

test('publication and verification errors prevent a successful release', async () => {
  await assert.rejects(publishPackage(artifact, {
    lookup: async () => null,
    publish: () => { throw new Error('Authentication failed'); },
  }), /Authentication failed/);
  await assert.rejects(publishPackage(artifact, {
    lookup: async () => null, publish: () => {}, pause: async () => {},
  }), /not visible/);
});

test('only a registry 404 is treated as an unpublished package', async () => {
  assert.equal(await registryVersion(artifact.name, artifact.version, async () => ({status: 404})), null);
  await assert.rejects(registryVersion(artifact.name, artifact.version, async () => ({status: 503, ok: false})), /503/);
});
