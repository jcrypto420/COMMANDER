# Bad Boys Asset Intake

Put Bad Boys IP/assets here only if you are comfortable storing them in this GitHub repo.

## Safe-to-add examples

- Logos / marks you want Commander to reference.
- Character art, sketches, style references, mood boards.
- Brand docs, lore notes, slogans, voice/tone notes.
- Product mockups, merch concepts, Roblox/game references.
- Public account handles, domains, storefront notes, and links.

## Do NOT add

- Secrets, API keys, passwords, seed phrases, wallet files, private keys.
- Personal identity docs, tax/legal docs, private family photos.
- Anything you do not want in GitHub history.
- Licensed third-party assets unless you have rights to use them.

## Recommended organization

```text
assets/badboys/
  README.md
  inventory.md
  logos/
  characters/
  lore/
  merch/
  roblox/
  social/
  references/
```

## After adding files

Tell Commander:

```text
I added Bad Boys assets. Inventory them and update assets/badboys/inventory.md.
```

Commander should then inspect filenames and safe text assets, avoid printing private/sensitive content unnecessarily, and summarize what is usable for the 69-day sprint.
