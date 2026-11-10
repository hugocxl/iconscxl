import { createElement, forwardRef } from "react";
import { Svg, Path, Circle } from "react-native-svg";
export const KotlinIcon = /*#__PURE__*/ forwardRef(function KotlinIcon({size = 16, color = "currentColor", ...props}, ref) {
  return createElement(Svg, {...{"fill": "none", "viewBox": "0 0 16 16"}, width: size, height: size, color, ...props, ref} ,createElement(Path, {"d": "M8 0C1.42 0 0 1.42 0 8s1.42 8 8 8 8-1.42 8-8-1.42-8-8-8", "fill": "currentColor", "opacity": ".2"}), createElement(Path, {"d": "M2.92 3.11 Q2.92 2.88 3.17 2.88 L12.94 2.88 Q13.17 2.88 13.01 3.04 L8.22 7.83 Q8.05 8 8.22 8.17 L13.01 12.96 Q13.17 13.12 12.94 13.12 L3.17 13.12 Q2.92 13.12 2.92 12.89 Z", "fill": "currentColor"}));
});
