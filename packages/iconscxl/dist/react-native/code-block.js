import { createElement, forwardRef } from "react";
import { Svg, Path, Circle } from "react-native-svg";
export const CodeBlockIcon = /*#__PURE__*/ forwardRef(function CodeBlockIcon({size = 16, color = "currentColor", ...props}, ref) {
  return createElement(Svg, {...{"fill": "none", "viewBox": "0 0 16 16"}, width: size, height: size, color, ...props, ref} ,createElement(Path, {"d": "M8 0C1.42 0 0 1.42 0 8s1.42 8 8 8 8-1.42 8-8-1.42-8-8-8", "fill": "currentColor", "opacity": ".2"}), createElement(Path, {"d": "M5.89 4.75 A0.57 0.57 0 1 1 6.69 5.55 L4.24 8 L6.69 10.45 A0.57 0.57 0 1 1 5.89 11.25 L3.04 8.4 A0.57 0.57 0 0 1 3.04 7.6 Z M9.31 4.75 A0.57 0.57 0 0 1 10.11 4.75 L12.96 7.6 A0.57 0.57 0 0 1 12.96 8.4 L10.11 11.25 A0.57 0.57 0 1 1 9.31 10.45 L11.76 8 L9.31 5.55 A0.57 0.57 0 0 1 9.31 4.75", "fill": "currentColor"}));
});
