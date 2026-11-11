# Strict design audit — 11 November 2026

> Baseline before the [selective-duotone correction](TONE-REVIEW.md). The hashes
> and counts below preserve that inspection. Trending Down has since been fixed;
> the other reported design concerns remain open.

## Acceptance contract

This is an independent reassessment of the existing artwork, not an endorsement
of the previous review. A name passes only if **every supported style** passes at
16, 24 and 32 points, on light and dark backgrounds, at both 1× and 2× AppKit
rasterization. All 550 names and 1,488 SVGs are in scope, including legacy brands.

| Criterion | Required for acceptance |
| --- | --- |
| Meaning | The silhouette and essential details communicate the intended concept; adjacent states remain distinguishable. A familiar convention may be learned, but a label must not rescue malformed geometry. |
| Construction | No accidental tangencies, joined details, spikes, broken contours or inconsistent occlusion. |
| Small-size legibility | Essential counters and gaps remain visibly open at 16 points; badges and interior details remain distinguishable at 1×. |
| Optical balance | Apparent mass, margins and alignment are balanced for the shape; mathematical centering alone is insufficient. |
| Family consistency | Related symbols share credible proportions, weight, rounding, badge placement and directional logic. |
| Style integrity | Duotone hierarchy supports meaning; Solid preserves essential negative space; Stroke retains essential structure without crowded double contours. |
| Tone and background | Structure remains legible in both tints, with no accidental alpha buildup or disappearing essential secondary segment. |
| Brands | Supplied marks remain visually coherent and legible. Official identity and current trademark compliance are outside this visual audit. |

**Fail:** a concrete material defect in any supported variant. **Needs review:**
a credible unresolved concern or an assessment that needs specialist/contextual
confirmation. **Pass:** no material defect found in the inspected matrix. There
is no average score and no quota for passing. Minor observations do not become
material failures solely to increase the rejection count. Uncertainty never
becomes automatic approval.

Major findings block strict design acceptance for the affected variant. Blocker
is reserved for unusable/missing or fundamentally incorrect artwork. Minor means
polish without a demonstrated material legibility or meaning loss.

## Method and limitations

Three independent GPT-6.1 Sol reviewers, each with medium reasoning, inspected
disjoint categories. The coordinating reviewer inspected the supplied screenshot,
checked the folder family, and adjudicated selected findings. These are AI visual
judgments, not a human usability study or independent brand certification.

Native sheets contain 17,856 rendered instances across 76 pages. The 2× sheets
use `scripts/icons/render-audit.swift`; the 1× sheets use the same source with only
`let scale:CGFloat=2` changed to `let scale:CGFloat=1`. Evidence is under the
ignored local directory `review/strict-2026-11-11/{1x,2x}`. Each directory includes
`pages.json`, mapping rows to names. The audit JSON preserves the source hashes;
the HTML report provides a portable way to examine the current source SVGs.
Browser rendering in that report is a review aid, not a claim of browser/device
visual verification. Subpixel positioning, non-neutral tints, actual UI contrast,
and physical device rendering are outside this matrix.

The screenshot shows a small open-folder-like icon. The current `folder-open`
artwork was examined as the likely match; the image alone cannot establish which
package version, style or application scaling produced it.

## Automated verification

The unchanged source artwork passes `npm run validate`, all ten design regression
tests, and `draw.py --check`. Validation includes normalization, geometry, old
review-hash coverage, generated exports, JavaScript tests, TypeScript and package
dry run. These checks establish structural consistency, **not visual quality**.
The previous all-approved hash ledger remains a historical record and is not the
acceptance result of this stricter review. No artwork or generated adapters were
changed by this audit.

## Results

**527 pass · 13 fail · 10 need review.** All 550 names have an individual
assessment; every supported style is listed and SHA-256 hashed. The library does
**not** pass this strict audit as a whole. The 23 flagged names remain unapproved.

- [Searchable visual report](design-audit-2026-11-11.html)
- [Complete machine-readable ledger](design-audit-2026-11-11.json)
- [Native 1× sheet manifest](../review/strict-2026-11-11/1x/pages.json)
- [Native 2× sheet manifest](../review/strict-2026-11-11/2x/pages.json)

The coordinator moved `user-x` from the category reviewer's pass-with-minor-note
to needs-review: its readable X does not settle whether the shoulder tangency is
acceptable under the strict construction criterion. All other category verdicts
were retained. “Needs review” is not approval and does not allege a proven defect.

### Confirmed failures

| Icon | Affected styles | Finding |
| --- | --- | --- |
| `battery` | solid | Solid uses negative charge marks: empty is a filled slab, full (and battery alias) has a large hollow center, and low has a small hollow bar, reversing the positive-fill state language of Duotone and Stroke. |
| `battery-empty` | solid | Solid uses negative charge marks: empty is a filled slab, full (and battery alias) has a large hollow center, and low has a small hollow bar, reversing the positive-fill state language of Duotone and Stroke. |
| `battery-full` | solid | Solid uses negative charge marks: empty is a filled slab, full (and battery alias) has a large hollow center, and low has a small hollow bar, reversing the positive-fill state language of Duotone and Stroke. |
| `battery-low` | solid | Solid uses negative charge marks: empty is a filled slab, full (and battery alias) has a large hollow center, and low has a small hollow bar, reversing the positive-fill state language of Duotone and Stroke. |
| `bicycle` | duotone, solid, stroke | Detached upper handlebar has no connecting stem in any style. Inspected at 16/24/32 pt, both tints, 1× and 2×. |
| `cast` | duotone, stroke | Radiating arcs collide with the unbroken lower-left display frame. Inspected at 16/24/32 pt, both tints, 1× and 2×. |
| `cpp` | duotone | The two tiny plus signs merge into an indistinct right-side cluster at 16 points 1x; the C is readable but the C++ discriminator is not. |
| `folder-open` | stroke | The outlined front flap crowds the rear lower contour into pointed corner wedges. |
| `folder-search` | duotone, stroke | The magnifier handle touches the bottom folder contour in outlined variants. |
| `headphones` | solid | Solid fills the headband arch into a helmet-like crown. Inspected at 16/24/32 pt, both tints, 1× and 2×. |
| `qr-code` | stroke | Stroke omits all three finder-center squares present in Duotone and Solid, leaving empty boxes and weakening the QR-specific structure. |
| `swatch` | solid | Solid combines the upper fan leaves into an undivided mass. |
| `trending-down` | solid, stroke | The descending arrowhead merges into the chart baseline in monochrome styles. |

### Unresolved concerns

| Icon | Concern |
| --- | --- |
| `calendar-range` | Single horizontal range mark can also read as calendar minus. Inspected at 16/24/32 pt, both tints, 1× and 2×. |
| `eye-off` | Solid removes the pupil entirely, leaving a slashed almond; the eye-like outer silhouette survives, but its relationship to the pupil-bearing eye variant warrants review. |
| `git-compare` | One-sided arrowheads create unresolved ambiguity with numeral-like marks. |
| `graphql` | At 16 points 1x the dense node-and-edge lattice crowds its central gaps; the outer network remains coherent, but internal readability is marginal. |
| `hard-drive` | Flat rounded rectangle and lower indicator dots are coherent, but the frontal window-like silhouette has limited storage-specific cues. |
| `pipette` | The straight capped barrel resembles a syringe; dropper meaning needs confirmation. |
| `podcast` | Simplified ring and torso may require context to communicate podcast. Inspected at 16/24/32 pt, both tints, 1× and 2×. |
| `simulator` | Phone plus play reads clearly as a device running media; simulator-specific meaning depends on product context. |
| `ssh` | Arrow between two corner marks reads clearly as remote entry, but the artwork alone does not distinguish SSH from a general connection action. |
| `user-x` | The X remains readable, but its joined shoulder edge requires a deliberate clearance decision before strict acceptance. |

### Correction priorities

1. Correct the Solid battery state language as a family, then verify state recognition side by side.
2. Repair structural joins and occlusion: bicycle, folder-open, folder-search, cast and trending-down.
3. Restore essential separation or detail in Solid swatch/headphones and Stroke qr-code; improve C++ small-size discrimination.
4. Resolve the ten pending concerns with focused design/context review. Re-render any changed artwork through the complete matrix before approving it.

The likely screenshot match, `folder-open`, fails specifically in Stroke; this is
not proof that the attached screenshot used that style. Its Duotone and Solid
variants were not assigned the same confirmed defect.

The report's complete coverage, style lists, source hashes, and 76 sheet hashes
were checked. Its search and verdict filters and all 8,928 SVG preview references
were verified with jsdom. This is DOM verification, not browser visual approval.
