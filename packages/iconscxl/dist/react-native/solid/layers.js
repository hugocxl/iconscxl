import { createElement, forwardRef } from "react";
import { Svg, Path, Circle, Rect, G } from "react-native-svg";
export const LayersIcon = /*#__PURE__*/ forwardRef(function LayersIcon({size = 16, color = "currentColor", ...props}, ref) {
  return createElement(Svg, {...{"fill": "none", "viewBox": "0 0 16 16"}, width: size, height: size, color, ...props, ref} ,createElement(Path, {"d": "M1 5 8 1 15 5 8 9ZM1 9 8 13 15 9V11L8 15L1 11Z", "fill": "currentColor"}));
});
