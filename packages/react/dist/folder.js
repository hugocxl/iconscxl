import { createElement, forwardRef } from "react";
export const FolderIcon = /*#__PURE__*/ forwardRef(function FolderIcon({size = 16, color = "currentColor", ...props}, ref) {
  return createElement("svg", {...{"fill": "none", "viewBox": "0 0 16 16"}, width: size, height: size, color, "aria-hidden": props["aria-label"] || props["aria-labelledby"] ? undefined : true, ...props, ref} ,createElement("path", {"d": "M15 12 A2 2 0 0 1 13 14 L3 14 A2 2 0 0 1 1 12 L1 6 L15 6 Z", "fill": "currentColor"}), createElement("path", {"d": "M5.59 2 A2 2 0 0 1 6.61 2.28 L8.41 3.36 A1 1 0 0 0 8.91 3.5 L13 3.5 A2 2 0 0 1 14.94 5 L1 5 L1 4 A2 2 0 0 1 3 2 Z", "fill": "currentColor", "opacity": ".5"}));
});
