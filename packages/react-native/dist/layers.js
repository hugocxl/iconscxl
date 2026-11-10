import { createElement, forwardRef } from "react";
import { Svg, Path, Circle } from "react-native-svg";
export const LayersIcon = /*#__PURE__*/ forwardRef(function LayersIcon({size = 16, color = "currentColor", ...props}, ref) {
  return createElement(Svg, {...{"fill": "none", "viewBox": "0 0 16 16"}, width: size, height: size, color, ...props, ref} ,createElement(Path, {"d": "M15.1 11.55a.5.5 0 0 1 0 .9l-6.65 3.33-.11.04a1 1 0 0 1-.68 0l-.1-.04L.9 12.45a.5.5 0 0 1 0-.9l1.98-1 1.68.85-1.2.6L8 14.32 12.65 12l-1.21-.6 1.68-.84z", "fill": "currentColor"}), createElement(Path, {"clipRule": "evenodd", "d": "M7.55.22a1 1 0 0 1 .9 0l6.66 3.33a.5.5 0 0 1 0 .9L8.45 7.78l-.11.04a1 1 0 0 1-.68 0l-.1-.04L.9 4.45a.5.5 0 0 1 0-.9zM3.35 4 8 6.32 12.65 4 8 1.68z", "fill": "currentColor", "fillRule": "evenodd"}), createElement(Path, {"d": "M15.1 7.55a.5.5 0 0 1 0 .9l-6.65 3.33a1 1 0 0 1-.9 0L.9 8.45a.5.5 0 0 1 0-.9l1.98-1 4.23 2.12a2 2 0 0 0 1.79 0l4.22-2.11z", "fill": "currentColor"}));
});
