import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, readdirSync } from 'node:fs';
import { createElement } from 'react';
import { renderToStaticMarkup } from 'react-dom/server';
import * as icons from '../packages/react/dist/index.js';
test('all icons render and preserve geometry, view boxes and opacity', () => {
  const files = readdirSync('icons').filter(x => x.endsWith('.svg'));
  assert.equal(Object.keys(icons).length, files.length);
  for (const file of files) {
    const name = file.slice(0,-4).split('-').map(x=>x[0].toUpperCase()+x.slice(1)).join('')+'Icon';
    const source = readFileSync('icons/'+file,'utf8');
    const rendered = renderToStaticMarkup(createElement(icons[name], {size:24, color:'red', 'aria-label':'Example', 'aria-hidden':false}));
    assert.ok(rendered.includes('width="24"'));
    assert.ok(rendered.includes('aria-hidden="false"'));
    for (const match of source.matchAll(/(?:viewBox|d|opacity|fill-rule|clip-rule)="[^"]*"/g)) assert.ok(rendered.includes(match[0]), file+': '+match[0]);
  }
});

test('web accessibility defaults and explicit overrides', () => {
  const render = props => renderToStaticMarkup(createElement(icons.SearchIcon, props));
  assert.match(render({}), /aria-hidden="true"/);
  assert.doesNotMatch(render({'aria-label': 'Search'}), /aria-hidden/);
  assert.doesNotMatch(render({'aria-labelledby': 'label'}), /aria-hidden/);
  assert.match(render({'aria-label': 'Search', 'aria-hidden': true}), /aria-hidden="true"/);
  assert.match(render({size: 24, width: 32}), /width="32"/);
});

test('package entry points and per-icon imports resolve', async () => {
  const root = await import('@hugocxl/cxl-icons-react');
  const single = await import('@hugocxl/cxl-icons-react/search');
  assert.equal(root.SearchIcon, single.SearchIcon);
  for (const platform of ['react', 'react-native']) {
    const manifest = JSON.parse(readFileSync(`packages/${platform}/package.json`));
    assert.equal(manifest.sideEffects, false);
    assert.equal(manifest.exports['.'].default, './dist/index.js');
    for (const file of ['LICENSE', 'NOTICE', 'THIRD_PARTY_LICENSES.md']) {
      assert.equal(readFileSync(`packages/${platform}/${file}`, 'utf8'), readFileSync(file, 'utf8'));
    }
  }
});

test('both packages bundle and tree shake unused icons', async () => {
  const { build } = await import('esbuild');
  for (const platform of ['react', 'react-native']) {
    const result = await build({
      stdin: { contents: `export { SearchIcon } from '@hugocxl/cxl-icons-${platform}';`, resolveDir: process.cwd() },
      bundle: true,
      write: false,
      format: 'esm',
      external: ['react', 'react-native-svg'],
      metafile: true,
    });
    const output = result.outputFiles[0].text;
    assert.match(output, /SearchIcon/);
    assert.doesNotMatch(output, /TerminalIcon/);
    const included = Object.entries(Object.values(result.metafile.outputs)[0].inputs)
      .filter(([path, info]) => path.includes('/dist/') && info.bytesInOutput > 0)
      .map(([path]) => path);
    assert.deepEqual(included, [`packages/${platform}/dist/search.js`]);
  }
});
