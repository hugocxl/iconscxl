import { createElement, forwardRef } from "react";
export const DotIcon = /*#__PURE__*/ forwardRef(function DotIcon({size = 16, color = "currentColor", ...props}, ref) {
  return createElement("svg", {...{"fill": "none", "viewBox": "0 0 16 16"}, width: size, height: size, color, "aria-hidden": props["aria-label"] || props["aria-labelledby"] ? undefined : true, ...props, ref} ,createElement("circle", {"cx": "8", "cy": "8", "fill": "currentColor", "r": "2"}));
});
