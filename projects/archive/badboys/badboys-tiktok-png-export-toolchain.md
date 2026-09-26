# Bad Boys TikTok PNG Export Toolchain v0

Status: active local toolchain.

## Purpose

Export internal SVG draft assets to TikTok-ready 1080x1920 PNGs.

## Tooling installed

Local repo npm package:
- `@resvg/resvg-js`

Install command used:

```bash
npm install --no-audit --no-fund @resvg/resvg-js
```

No sudo/system package install was used.

## Export script

Script:
- `scripts/export_badboys_svgs_to_png.js`

Run:

```bash
node scripts/export_badboys_svgs_to_png.js
```

## Inputs

- `assets/badboys/tiktok/svg/*.svg`

## Outputs

- `assets/badboys/tiktok/png/*.png`

## Verification

Validated after export:
- 30 PNG files created
- all PNGs are 1080x1920
- all source SVGs parse as valid XML

## Public safety

Exporting files is safe/local.
Posting/uploading remains approval-gated.
