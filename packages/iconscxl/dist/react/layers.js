import { createElement, forwardRef } from "react";
export const LayersIcon = /*#__PURE__*/ forwardRef(function LayersIcon({size = 16, color = "currentColor", ...props}, ref) {
  return createElement("svg", {...{"fill": "none", "viewBox": "0 0 16 16"}, width: size, height: size, color, "aria-hidden": props["aria-label"] || props["aria-labelledby"] ? undefined : true, ...props, ref} ,createElement("path", {"d": "M1 9 8 13 15 9V11L8 15L1 11Z", "fill": "currentColor", "opacity": "0.4"}), createElement("path", {"d": "M1 5 8 1 15 5 8 9 1 5Z", "fill": "currentColor"}));
});
