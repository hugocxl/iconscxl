# Tab Icons

207 SVG icons for apps, developer tools, files and brands, adapted and extended for [Tab](https://github.com/hugocxl/tab).

![Tab Icons preview](preview.png)

## Use

Download or clone this repository and copy the SVGs you need from `icons/`.
No dependencies or build step are required to use the artwork.

```sh
git clone https://github.com/hugocxl/tab-icons.git
```

Icons use `currentColor`, filled geometry and their original viewBox. Most are
16 units high; preserve aspect ratio when sizing them. Duo icons use opacity
for a secondary layer of the same color.

Inline an SVG in HTML to inherit CSS `color`. When loading SVGs through an
`<img>` tag, parent CSS color does not propagate into the file. Native apps can
load them as template images and apply their own tint.

Open [index.html](index.html) locally for a searchable gallery of every icon.

## Contribute

See [the drawing guide](scripts/icons/STYLE.md) for geometry and naming conventions.
Tools use Python 3's standard library; the contact sheet requires Swift and AppKit
on macOS.

```sh
python3 -I scripts/icons/normalize.py icons
python3 -I scripts/icons/test-adapt-brand.py
swift scripts/icons/render-sheet.swift icons preview.png --size 16 --scale 2
scripts/validate.sh
```

The importer and brand adapter in `scripts/icons/` help prepare new artwork.
Preserve upstream attribution when adapting artwork.

## License and attribution

Original Tab contributions and tooling are [MIT licensed](LICENSE).
The collection includes artwork adapted from Pierre Icons (Apache 2.0),
Pierre's file icons (MIT), Simple Icons (CC0 1.0), LobeHub Icons (MIT), and
Devicon (MIT). Upstream artwork retains its original license; the collection
is not solely MIT licensed. Keep [NOTICE](NOTICE),
[the upstream license texts](THIRD_PARTY_LICENSES.md), and applicable copyright
notices with redistributed artwork.

Brand marks remain the trademarks of their owners. Inclusion does not imply
endorsement or grant trademark rights.
