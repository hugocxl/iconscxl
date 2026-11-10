import { createElement, forwardRef } from "react";
export const MinusIcon = /*#__PURE__*/ forwardRef(function MinusIcon({size = 16, color = "currentColor", ...props}, ref) {
  return createElement("svg", {...{"fill": "none", "viewBox": "0 0 16 16"}, width: size, height: size, color, "aria-hidden": props["aria-label"] || props["aria-labelledby"] ? undefined : true, ...props, ref} ,createElement("path", {"d": "M13 8C13 7.58579 12.6642 7.25 12.25 7.25H3.75C3.33579 7.25 3 7.58579 3 8C3 8.41421 3.33579 8.75 3.75 8.75H12.25C12.6642 8.75 13 8.41421 13 8Z", "fill": "currentColor"}));
});
