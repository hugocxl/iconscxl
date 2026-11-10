# IconsCXL design system

IconsCXL is a rounded, duotone-first family for product interfaces. The expanded
foundation contains 550 names in 19 categories, including 469 original UI symbols
and 81 retained brand marks. There are 343 new names and 126 redrawn existing UI
symbols. [The generated catalog](CATALOG.md) defines the delivered set;
[`catalog.json`](../catalog.json) is its machine-readable counterpart.

## References and authorship

- [Hugeicons Duotone Rounded](https://hugeicons.com/icons/duotone-rounded):
  rounded construction, expressive secondary masses, coherent related families.
- [Lucide](https://lucide.dev/icons/): clear names, discoverable categories,
  consistent directional and status variants, broad interface coverage.
- [SF Symbols](https://developer.apple.com/sf-symbols/): optical balance,
  legibility beside text, recognizable silhouettes, and semantic family coverage.

These references inform the design brief. The new UI geometry is authored here;
no Hugeicons, Lucide, or SF Symbols artwork is included. This library does not
implement SF Symbols' variable weights, animations, localization, or font metrics.
Retained brand artwork keeps the attribution and licenses in NOTICE and
THIRD_PARTY_LICENSES.md.

## Visual contract

New UI artwork uses a square 16 × 16 canvas with optical fitting, typically
0.65–1.5 units of clearance. The primary centerline width is 1.35 units; body
outlines are 1.25 units. Round caps and round joins are expanded to filled Bézier
contours. Smaller interior details may use 1–1.2 units; dense document labels use
0.8. Shapes are fitted by their actual bounds, including outlines, rather than
by their control points. Curves remain curves in the exported SVG.

Duotone uses the same tint at two opacity levels. Body symbols use a 0.24
secondary silhouette and an opaque outline/detail layer. Linear symbols use
0.4 for a subordinate segment and 1 for the identifying segment. Boolean
subtraction removes overlaps between the layers so alpha does not compound.
No common background tile is added to unrelated UI symbols.

Names are lower kebab-case, with direction and state suffixes. Common nouns
come first (`calendar-check`, `folder-lock`, `cloud-download`). Existing names
remain available, including historical `*-fill` names; their default artwork is
now duotone. Some names are compatibility aliases: `mail`/`envelope`,
`circle-info`/`info`, `checkbox`/`checkbox-fill`, and the historical circle-fill
names. They do not represent distinct new concepts.

## Styles and supported exports

| Style | Construction | Coverage |
| --- | --- | --- |
| Rounded Duotone | Secondary mass with primary contours/details | All 550 names |
| Rounded Solid | Filled silhouette with negative-space details | 469 UI names |
| Rounded Stroke | Expanded contour and identifying detail lines | 469 UI names |

Minimal linear symbols can intentionally share Solid and Stroke geometry. A
single arrow shaft does not need a different silhouette merely to increase the
variant count. Compound pictograms can retain small filled details in Stroke
(e.g. pupils, status dots, musical note heads).

Brands retain their duotone treatment. They are absent from the Solid and Stroke
namespaces; no style silently substitutes an unrelated drawing. Bulk, Twotone,
Standard, Sharp, multiple weights, and arbitrary two-color palettes are not part
of this release. They require a separate design and review pass.

The default SVG and JS/React/React Native imports and Swift `Icon` enum remain
compatible. Style-specific imports use `/react/solid`, `/react/stroke`, and the
matching `/js` and `/react-native` namespaces; per-icon paths are also supported.
`/duotone` explicitly names the default style. Swift provides `SolidIcon` and
`StrokeIcon` enums, each containing exactly the names supported by that style.

## Coverage priorities

The delivered set covers everyday navigation and actions; documents and folders;
messaging and notifications; people and accessibility; security and identity;
time and tasks; media and capture; layouts; text and design tools; code, Git,
AI, devices and connectivity; analytics; money and commerce; work and education;
health and fitness; maps and transport; weather and nature; home and food.

This is a general product foundation, not a claim that every niche is covered.
Future work should add useful semantic families before decorative variations:
more fitness movements and health measurements, richer transport and wayfinding,
more food and animals, specialist developer tools, international signs, and
additional accessibility and communication states. New requests should first
search the existing catalog, add a clear noun/state name, and review the family
beside its nearest existing symbols.

## Review and maintenance

The SVGs are the canonical distribution assets. `scripts/icons/draw.py` contains
editable body/detail recipes for all original UI drawings. It expands round
strokes and uses boolean geometry while authoring; consumers need no geometry
library. Do not patch platform adapters or asset catalog copies by hand.

Before accepting an addition:

1. Check its silhouette and meaning at 16, 24, and 32 points beside related icons.
2. Inspect dark and light tinting, counters, diagonals, small gaps, and badges.
3. Inspect each supported style independently; negative-space Solid details must
   remain readable, and Stroke must preserve identifying interior information.
4. Run the geometry/opacity/catalog gate, platform rendering tests, tree-shaking
   and type checks, packaging, and the macOS/iOS resource builds.
5. Regenerate adapters, catalog, coverage documentation, and offline gallery.

For this expansion, AppKit contact sheets were used for actual SVG rendering in
both tints. Live browser inspection was unavailable in the execution environment;
gallery interaction is covered with DOM tests. Device-level React Native testing
and exhaustive human review on every display size are still separate checks.

The [full artwork review](REVIEW.md) records the subsequent per-icon inspection
and corrections. Solid construction preserves structural parts separately from
negative interior details; complex occlusion is authored explicitly. Round body
corners, high-resolution stroke expansion and area-checked Boolean operations
prevent the geometric failures found in that review. Review hashes are checked
by validation; changed artwork must be rendered and inspected again.
