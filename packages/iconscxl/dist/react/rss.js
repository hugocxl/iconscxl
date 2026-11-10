import { createElement, forwardRef } from "react";
export const RssIcon = /*#__PURE__*/ forwardRef(function RssIcon({size = 16, color = "currentColor", ...props}, ref) {
  return createElement("svg", {...{"fill": "none", "viewBox": "0 0 16 16"}, width: size, height: size, color, "aria-hidden": props["aria-label"] || props["aria-labelledby"] ? undefined : true, ...props, ref} ,createElement("path", {"d": "M3.65 10.7a1.65 1.65 0 1 1 0 3.3 1.65 1.65 0 0 1 0-3.3M2 6.06A7.95 7.95 0 0 1 9.95 14H7.62A5.6 5.6 0 0 0 2 8.38zM2 2a12 12 0 0 1 12 12h-2.4A9.6 9.6 0 0 0 2 4.4z", "fill": "currentColor"}));
});
