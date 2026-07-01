const fs = require('fs');
const path = require('path');
const { Resvg } = require('@resvg/resvg-js');

const repo = path.resolve(__dirname, '..');
const srcPath = path.join(repo, 'assets/badboys/account-ready-real-assets-v0/avatar-primary-insideface.png');
const outDir = path.join(repo, 'assets/badboys/account-ready-real-assets-v0/avatar-background-test');
fs.mkdirSync(outDir, { recursive: true });

const srcBase64 = fs.readFileSync(srcPath).toString('base64');
const variants = [
  {
    slug: 'bone-circle',
    label: 'Bone circle — safest TikTok contrast',
    bg: '#f4ead7',
    ring: '#ff5a1f',
    frame: '#111111',
    note: 'Best default: warm, high contrast, still mischievous.'
  },
  {
    slug: 'orange-warning',
    label: 'Orange warning — loudest small-icon read',
    bg: '#ff5a1f',
    ring: '#f7e7b7',
    frame: '#090909',
    note: 'Most aggressive; good for signal, can feel more mascot/sticker.'
  },
  {
    slug: 'white-sticker',
    label: 'White sticker — cleanest app UI visibility',
    bg: '#f7f7f2',
    ring: '#222222',
    frame: '#ff5a1f',
    note: 'Clean and platform-safe; a bit less “Bad Boys” energy.'
  }
];

function svgFor(v) {
  return `<?xml version="1.0" encoding="UTF-8"?>
<svg width="1080" height="1080" viewBox="0 0 1080 1080" xmlns="http://www.w3.org/2000/svg">
  <rect width="1080" height="1080" fill="#0b0b0c"/>
  <circle cx="540" cy="540" r="454" fill="${v.frame}"/>
  <circle cx="540" cy="540" r="414" fill="${v.ring}"/>
  <circle cx="540" cy="540" r="376" fill="${v.bg}"/>
  <image href="data:image/png;base64,${srcBase64}" x="226" y="142" width="628" height="888" preserveAspectRatio="xMidYMid meet"/>
  <circle cx="540" cy="540" r="516" fill="none" stroke="#000000" stroke-width="8" opacity="0.6"/>
</svg>`;
}

for (const v of variants) {
  const svg = svgFor(v);
  const svgPath = path.join(outDir, `${v.slug}.svg`);
  const pngPath = path.join(outDir, `${v.slug}.png`);
  fs.writeFileSync(svgPath, svg);
  const resvg = new Resvg(svg, { fitTo: { mode: 'width', value: 1080 }, background: 'rgba(0,0,0,0)' });
  fs.writeFileSync(pngPath, resvg.render().asPng());
}

const html = `<!doctype html>
<meta charset="utf-8">
<title>Bad Boys Avatar Background Test</title>
<style>
  body{font-family:Arial,sans-serif;background:#09090a;color:#eee;margin:24px;line-height:1.45}
  h1{color:#ff5a1f;margin-bottom:4px}.note{max-width:920px;color:#ddd}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:18px;margin-top:18px}
  figure{background:#151517;border:1px solid #333;border-radius:14px;padding:14px;margin:0}img{width:100%;height:auto;border-radius:50%;background:#111}figcaption{font-size:14px;color:#ddd;margin-top:10px}strong{color:#fff}.small{color:#aaa;font-size:12px}
</style>
<h1>Bad Boys Avatar Background Test</h1>
<p class="note">Purpose: keep the real Josh-provided face mark, but make it survive TikTok’s tiny circular avatar crop and dark UI. Recommendation: <strong>bone-circle</strong>.</p>
<div class="grid">
${variants.map(v => `<figure><img src="${v.slug}.png" alt="${v.label}"><figcaption><strong>${v.label}</strong><br>${v.note}<br><span class="small">${v.slug}.png / ${v.slug}.svg</span></figcaption></figure>`).join('\n')}
</div>
`;
fs.writeFileSync(path.join(outDir, 'review.html'), html);

console.log(`created ${variants.length} avatar background variants in ${outDir}`);
for (const v of variants) console.log(`- ${v.slug}.png`);
