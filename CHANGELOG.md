# Changelog

## Unreleased

### Added

- Expand from 207 to 550 names across 19 categories: 343 additions, 126 existing
  UI symbols redrawn, and 81 retained brand marks.
- Rounded Duotone, Solid and Stroke artwork for 469 original UI icons, with
  matching JS, React, React Native and Swift exports (1,488 SVG drawings).
- Offline gallery with category/style search, size/tint controls, accessible
  details, SVG copying and downloads; generated machine-readable coverage catalog.
- Editable vector recipes, documented reference/design rules, bounds and tone
  validation, style export/tree-shaking tests, and gallery interaction tests.

### Changed

- Accept platform-dependent ordering of identical closed contours in authoring
  checks, with a Linux Film regression fixture; keep all reviewed SVGs unchanged.

- Audit every supported drawing at 16/24/32 points in both tints; refine 469
  names, repair Solid structural parts/counters, and correct ambiguous silhouettes.
- Add per-icon visual review hashes, native category sheets, and design regression
  checks for connectivity, symmetry, mirroring, counters and Boolean area loss.

- All default UI artwork is now duotone, including historical `*-fill` names.
  Existing icon names and imports remain compatible; their appearance changes.
- Validation checks canonical SVG bytes without modifying files and no longer
  requires a clean Git diff.

### Previously added

- Rename the repository and Swift library to IconsCXL and consolidate npm distribution as `@hugocxl/iconscxl`, with `/js`, `/react` and `/react-native` exports.
- Add dependency-free JavaScript SVG exports and optional framework peers.
- Publish the unified package to npm with OIDC provenance and verify registry integrity before publishing the GitHub release.

- Automatic GitHub releases after successful main-branch push checks, with version tags, npm tarballs and checksums.

- Generated Swift package and typed React / React Native packages from the canonical SVGs.
- Per-icon ESM imports, accessible web defaults, ref support, package validation and CI.

## 0.1.0 - 2026-11-09

### Added

- Published 207 SVG icons with a searchable gallery, drawing tools and upstream attribution.
