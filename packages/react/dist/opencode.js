import { createElement, forwardRef } from "react";
export const OpencodeIcon = /*#__PURE__*/ forwardRef(function OpencodeIcon({size = 16, color = "currentColor", ...props}, ref) {
  return createElement("svg", {...{"fill": "none", "viewBox": "0 0 16 16"}, width: size, height: size, color, "aria-hidden": props["aria-label"] || props["aria-labelledby"] ? undefined : true, ...props, ref} ,createElement("path", {"d": "M8 0C1.42 0 0 1.42 0 8s1.42 8 8 8 8-1.42 8-8-1.42-8-8-8", "fill": "currentColor", "opacity": ".2"}), createElement("path", {"d": "M10.05 4.93 L5.95 4.93 L5.95 11.07 L10.05 11.07 L10.05 4.93 Z M12.1 13.12 L3.9 13.12 L3.9 2.88 L12.1 2.88 L12.1 13.12 Z", "fill": "currentColor", "fillRule": "evenodd"}));
});
