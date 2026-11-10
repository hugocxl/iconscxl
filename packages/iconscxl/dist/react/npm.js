import { createElement, forwardRef } from "react";
export const NpmIcon = /*#__PURE__*/ forwardRef(function NpmIcon({size = 16, color = "currentColor", ...props}, ref) {
  return createElement("svg", {...{"fill": "none", "viewBox": "0 0 16 16"}, width: size, height: size, color, "aria-hidden": props["aria-label"] || props["aria-labelledby"] ? undefined : true, ...props, ref} ,createElement("path", {"d": "M8 0C1.42 0 0 1.42 0 8s1.42 8 8 8 8-1.42 8-8-1.42-8-8-8", "fill": "currentColor", "opacity": ".2"}), createElement("path", {"d": "M10.56 13.12 L13.12 13.12 L13.12 2.88 L2.88 2.88 L2.88 13.12 L8 13.12 L8 5.44 L10.56 5.44 Z", "fill": "currentColor"}));
});
