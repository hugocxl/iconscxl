import { createElement, forwardRef } from "react";
import { Svg, Path, Circle } from "react-native-svg";
export const CodeIcon = /*#__PURE__*/ forwardRef(function CodeIcon({size = 16, color = "currentColor", ...props}, ref) {
  return createElement(Svg, {...{"fill": "none", "viewBox": "0 0 16 16"}, width: size, height: size, color, ...props, ref} ,createElement(Path, {"d": "M9.63 2.02a.5.5 0 0 1 .35.61l-3 11a.5.5 0 0 1-.96-.26l3-11a.5.5 0 0 1 .61-.35M4.15 4.65a.5.5 0 1 1 .7.7L2.21 8l2.64 2.65a.5.5 0 1 1-.7.7l-3-3a.5.5 0 0 1 0-.7zm7 0a.5.5 0 0 1 .7 0l3 3a.5.5 0 0 1 0 .7l-3 3a.5.5 0 1 1-.7-.7L13.79 8l-2.64-2.65a.5.5 0 0 1 0-.7", "fill": "currentColor"}));
});
