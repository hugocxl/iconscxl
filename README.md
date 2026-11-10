# IconsCXL

207 lightweight SVG icons for apps, developer tools, files, and brands. Use the
artwork directly or consume the generated Swift, React, and React Native
adapters. The collection was adapted and extended for [Tab](https://github.com/hugocxl/tab).

![IconsCXL preview](preview.png)

## Choose an integration

| Need | Start here |
| --- | --- |
| Use an SVG in a web page, design, or native app | [Raw SVGs](#raw-svgs) |
| Use icons in SwiftUI, UIKit, or AppKit | [Swift / SwiftUI](#swift--swiftui) |
| Use icons in a React app | [React](#react) |
| Use icons in React Native or Expo | [React Native / Expo](#react-native--expo) |

All integrations use the same icon names and source artwork. The default icon
size is 16, and icons use `currentColor` or an explicit platform tint.

## Raw SVGs

Download or clone the repository and copy the SVGs you need from [`icons/`](icons/).
No dependencies or build step are required to use the artwork.

```sh
git clone https://github.com/hugocxl/iconscxl.git
```

Icons use `currentColor`, filled geometry and their original viewBox. Most are
16 units high; preserve aspect ratio when sizing them. Duo icons use opacity
for a secondary layer of the same color.

Inline an SVG in HTML to inherit CSS `color`. When loading SVGs through an
`<img>` tag, parent CSS color does not propagate into the file. Native apps can
load them as template images and apply their own tint.

Open [`index.html`](index.html) locally for a searchable gallery of every icon.

## Swift / SwiftUI

The Swift package exposes the `IconsCXL` library for Swift 6+, macOS 12+, iOS
15+, tvOS 15+, and watchOS 8+. Add the repository as a Swift Package Manager
dependency using a release tag, or add it as a local package while developing.
Then add `IconsCXL` to your app target.

```swift
import IconsCXL
import SwiftUI

Icon.search.image
    .resizable()
    .scaledToFit()
    .frame(width: 24, height: 24)
    .foregroundStyle(.secondary)
    .accessibilityLabel("Search")
```

Use `Icon.search.uiImage` in UIKit or `Icon.search.nsImage` in AppKit.
Images come from the package's vector asset catalog and use template rendering.
`Icon.allCases` and `Icon(rawValue: "search")` support dynamic selection.

## JavaScript (no framework)

All JavaScript integrations come from one npm package, `@hugocxl/iconscxl`.
Choose `/js`, `/react`, or `/react-native`; per-icon imports are available too.
React and React Native dependencies are optional, so a plain JavaScript install
adds no framework dependencies.

```sh
npm install @hugocxl/iconscxl
```

```js
import { SearchIcon } from '@hugocxl/iconscxl/js';
// Or: import { SearchIcon } from '@hugocxl/iconscxl/js/search';
// The package root also exports the plain JavaScript adapter.
document.querySelector('#search-icon').innerHTML = SearchIcon;
```

The JS adapter exports SVG strings, usable in the browser or server-side.
These are the trusted, bundled artwork strings. Use CSS to size and tint inline
SVGs (`#search-icon svg { width: 24px; height: 24px; color: rebeccapurple; }`).
Add accessible labels on the containing control when used as button icons.

## React

The React package provides typed ESM components with per-icon exports and tree
shaking. Install it from npm:

```sh
npm install @hugocxl/iconscxl
```

```tsx
import { SearchIcon } from '@hugocxl/iconscxl/react';
// Per-icon imports are also supported:
import { TerminalIcon } from '@hugocxl/iconscxl/react/terminal';

<SearchIcon size={24} color="currentColor" aria-label="Search" />
<TerminalIcon size={16} />
```

Components support React 18 and 19, SVG props, and forwarded SVG refs.
Unlabelled icons are decorative (`aria-hidden`). Supply `aria-label` or
`aria-labelledby` for meaningful icons; explicit `aria-hidden` takes precedence.
For icon-only buttons, label the button and leave the icon decorative.

To create a local package tarball from this repository, run `npm ci`,
`npm run generate`, then `npm pack --workspace @hugocxl/iconscxl`.

## React Native / Expo

The React Native package provides the same typed, per-icon API for React Native
and Expo. Install it from npm along with its peer dependency:

```sh
npm install @hugocxl/iconscxl
npx expo install react-native-svg
# Or, in a bare React Native app:
npm install react-native-svg
```

```tsx
import { SearchIcon } from '@hugocxl/iconscxl/react-native';

<SearchIcon size={24} color="#64748b" accessibilityLabel="Search" />
```

Native components accept `react-native-svg` props and refs. No SVG transformer
or custom Metro configuration is needed. Install iOS pods using your app's
normal workflow. To create a local package tarball, run `npm ci`,
`npm run generate`, then `npm pack --workspace @hugocxl/iconscxl-native`.

Both JavaScript packages ship typed ESM with per-icon exports and tree shaking.
The peer ranges are compatibility declarations; CI checks the versions in the
lockfile, not every older React Native release.

## Development and validation

Use Node 22+, npm, Python 3, and Xcode with Swift 6+ for Apple builds.

```sh
npm ci
npm run generate       # regenerate adapters after editing icons/
npm run validate       # artwork, generation drift, rendering, types, packaging
xcodebuild -scheme IconsCXL -destination 'platform=macOS' test
xcodebuild -scheme IconsCXL -destination 'generic/platform=iOS Simulator' CODE_SIGNING_ALLOWED=NO build
```

`icons/` is the source of truth. Commit generated `packages/*/dist` and
`Sources/IconsCXL` resources so consumers do not need Python or a generation
step. Do not edit generated files directly. Build caches and dependencies are
ignored. CI validates JavaScript packages on Linux and Swift on macOS, including
an iOS Simulator build. Use Xcode for asset-catalog tests; standalone SwiftPM resource compilation varies
with the installed toolchain. Device rendering and a running React Native app still
need app-level verification.

### Automatic releases

Every push to `main` runs the JavaScript and Apple checks, publishes the single npm
package with provenance, verifies its registry integrity, then creates a GitHub
release with a Swift Package Manager tag, the npm package tarball, SHA-256
checksums, and generated release notes. Pull requests and other branches only
validate. A failed check prevents publication. Push runs are not cancelled by
newer pushes.

Versions use `0.1.<GitHub workflow run number>` (for example, `v0.1.12`). This
keeps versions unique without bot commits to `main`; numbers can have gaps due
to pull requests or failed runs. Retrying the same run reuses its version,
recovers an incomplete draft, and leaves an already published release intact.
The tag points to the exact validated commit. npm tarball manifests and their
lockfile workspace entries are stamped during packaging; source manifests keep
the development version. Change the `0.1` release line in
`scripts/prepare-release.mjs` when planning a minor or major version change.

Publishing uses npm trusted publishing (OIDC) from `validate.yml`, with
`id-token: write` and a compatible npm CLI on Node 24. The package authorizes
`hugocxl/iconscxl` and this workflow filename on npm. No npm token is stored in
GitHub. The GitHub release uses `GITHUB_TOKEN` with `contents: write`; repository
rules must permit version tags. The initial package must exist before trust
can be configured; that one-time bootstrap requires the npm owner's login.

Retries verify and skip an already published npm version. An integrity mismatch or publication failure stops the
GitHub release. All three adapters share one version and one tarball; rerun a failed workflow
to recover a release interrupted after npm publication.

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
