import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, readdirSync } from 'node:fs';
import { createElement } from 'react';
import { renderToStaticMarkup } from 'react-dom/server';
import { build } from 'esbuild';
const catalog=JSON.parse(readFileSync('catalog.json'));
const symbol=name=>name.split('-').map(w=>w[0].toUpperCase()+w.slice(1)).join('')+'Icon';
test('catalog exhaustively describes default artwork and available styles',async()=>{
 assert.deepEqual(catalog.map(i=>i.name),readdirSync('icons').filter(f=>f.endsWith('.svg')).map(f=>f.slice(0,-4)).sort());
 const packaged=await import('@hugocxl/iconscxl/catalog.json',{with:{type:'json'}});
 assert.deepEqual(packaged.default,catalog);
 for(const style of ['solid','stroke']){
  assert.deepEqual(catalog.filter(i=>i.styles.includes(style)).map(i=>i.name),readdirSync(`icons/styles/${style}`).map(f=>f.slice(0,-4)).sort());
 }
 for(const item of catalog){
  assert.ok(item.category && item.origin);
  const svg=readFileSync(`icons/${item.name}.svg`,'utf8');
  assert.match(svg,/opacity="(?:0?\.\d+)"/,item.name+' must be duotone');
 }
});
test('each style resolves and preserves all SVG geometry and React accessibility',async()=>{
 for(const style of ['duotone','solid','stroke']){
  const js=await import(`@hugocxl/iconscxl/js/${style}`);
  const react=await import(`@hugocxl/iconscxl/react/${style}`);
  const items=catalog.filter(i=>i.styles.includes(style));
  assert.equal(Object.keys(js).length,items.length);
  assert.equal(Object.keys(react).length,items.length);
  for(const item of items){
   const svg=readFileSync(`icons/${style==='duotone'?'':`styles/${style}/`}${item.name}.svg`,'utf8');
   assert.equal(js[symbol(item.name)],svg);
   const markup=renderToStaticMarkup(createElement(react[symbol(item.name)],{size:20,'aria-label':item.name}));
   assert.doesNotMatch(markup,/aria-hidden/);
   for(const match of svg.matchAll(/(?:viewBox|d|opacity|fill-rule)="[^"]*"/g))assert.ok(markup.includes(match[0]),`${style}/${item.name}: ${match[0]}`);
  }
 }
});
test('every platform supports style-specific imports and tree shaking',async()=>{
 for(const platform of ['js','react','react-native'])for(const style of ['duotone','solid','stroke']){
  const result=await build({stdin:{contents:`export { SearchIcon } from '@hugocxl/iconscxl/${platform}/${style}';`,resolveDir:process.cwd()},bundle:true,write:false,format:'esm',external:['react','react-native-svg'],metafile:true});
  assert.match(result.outputFiles[0].text,/SearchIcon/);
  assert.doesNotMatch(result.outputFiles[0].text,/TerminalIcon/);
  const single=await build({stdin:{contents:`export { SearchIcon } from '@hugocxl/iconscxl/${platform}/${style}/search';`,resolveDir:process.cwd()},bundle:true,write:false,format:'esm',external:['react','react-native-svg']});
  assert.equal(single.outputFiles[0].text,result.outputFiles[0].text);
 }
});
