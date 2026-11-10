import { createElement, forwardRef } from "react";
export const StopIcon = /*#__PURE__*/ forwardRef(function StopIcon({size = 16, color = "currentColor", ...props}, ref) {
  return createElement("svg", {...{"fill": "none", "viewBox": "0 0 16 16"}, width: size, height: size, color, "aria-hidden": props["aria-label"] || props["aria-labelledby"] ? undefined : true, ...props, ref} ,createElement("path", {"d": "M4.5 3H11.5C12.32843 3 13 3.67157 13 4.5V11.5C13 12.32843 12.32843 13 11.5 13H4.5C3.67157 13 3 12.32843 3 11.5V4.5C3 3.67157 3.67157 3 4.5 3Z", "fill": "currentColor"}));
});
