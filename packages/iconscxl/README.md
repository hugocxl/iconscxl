# IconsCXL

550 rounded icons with selective duotone (469 also available in Solid and Stroke) in one package, with typed, tree-shakeable exports for JavaScript,
React and React Native.

```sh
npm install @hugocxl/iconscxl
```

```js
// Pure JavaScript: SVG strings, no framework dependency.
import { SearchIcon } from '@hugocxl/iconscxl/js';
// React components:
import { SearchIcon as ReactSearchIcon } from '@hugocxl/iconscxl/react';
// React Native components (install react-native-svg in your app):
import { SearchIcon as NativeSearchIcon } from '@hugocxl/iconscxl/react-native';
// Per-icon imports:
import { SearchIcon as singleSvg } from '@hugocxl/iconscxl/js/search';
```

React adapters accept `size`, `color`, platform SVG props, and refs. Unlabelled
web icons are decorative; use `aria-label` for meaningful icons. Native apps
should install `react-native-svg` (Expo: `npx expo install react-native-svg`).
The package root is the pure JavaScript adapter. Framework peers are optional;
install the peers needed by the adapter you use.

See https://github.com/hugocxl/iconscxl for Swift support and full usage.
Redistribute LICENSE, NOTICE and THIRD_PARTY_LICENSES.md with the artwork.

Style imports use `/js/solid`, `/react/solid`, `/react-native/solid` or the
matching `/stroke` paths. Per-icon style imports are supported too, for example
`@hugocxl/iconscxl/react/stroke/search`. `/duotone` explicitly selects the default.
Brand marks are available in Duotone only. The exported `catalog.json` records
style availability, category, keywords, provenance, and `defaultTone` for every
name. Arrows, chevrons and other linear symbols are fully opaque; two tones are
reserved for meaningful surfaces and depth, such as the Pencil and Trash bodies.
