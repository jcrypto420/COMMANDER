#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const { Resvg } = require('@resvg/resvg-js');

const repo = '/home/josh/COMMANDER';
const inputDir = path.join(repo, 'assets/badboys/tiktok/svg');
const outputDir = path.join(repo, 'assets/badboys/tiktok/png');
fs.mkdirSync(outputDir, { recursive: true });

let count = 0;
const files = fs.readdirSync(inputDir)
  .filter(f => f.endsWith('.svg'))
  .sort();

for (const file of files) {
  const svgPath = path.join(inputDir, file);
  const svg = fs.readFileSync(svgPath);
  const resvg = new Resvg(svg, {
    fitTo: { mode: 'width', value: 1080 },
    font: { loadSystemFonts: true },
    resourcesDir: inputDir,
  });
  const pngData = resvg.render().asPng();
  const outName = file.replace(/\.svg$/i, '.png');
  const outPath = path.join(outputDir, outName);
  fs.writeFileSync(outPath, pngData);
  console.log(`${path.relative(repo, svgPath)} -> ${path.relative(repo, outPath)} (${pngData.length} bytes)`);
  count += 1;
}
console.log(`exported_png_count=${count}`);
