import { createElement, forwardRef } from "react";
export const DotIcon = /*#__PURE__*/ forwardRef(function DotIcon({size = 16, color = "currentColor", ...props}, ref) {
  return createElement("svg", {...{"fill": "none", "viewBox": "0 0 16 16"}, width: size, height: size, color, "aria-hidden": props["aria-label"] || props["aria-labelledby"] ? undefined : true, ...props, ref} ,createElement("path", {"d": "M4 8C4 5.7909 5.7909 4 8 4C10.2091 4 12 5.7909 12 8C12 10.2091 10.2091 12 8 12C5.7909 12 4 10.2091 4 8Z", "fill": "currentColor"}));
});
