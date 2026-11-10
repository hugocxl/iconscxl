import { createElement, forwardRef } from "react";
import { Svg, Path, Circle } from "react-native-svg";
export const SvgIcon = /*#__PURE__*/ forwardRef(function SvgIcon({size = 16, color = "currentColor", ...props}, ref) {
  return createElement(Svg, {...{"fill": "none", "viewBox": "0 0 16 16"}, width: size, height: size, color, ...props, ref} ,createElement(Path, {"d": "M8 0C1.42 0 0 1.42 0 8s1.42 8 8 8 8-1.42 8-8-1.42-8-8-8", "fill": "currentColor", "opacity": ".2"}), createElement(Path, {"d": "M5.8 7.26 A1.46 1.46 0 0 1 7.27 5.8 L11.66 5.8 A1.46 1.46 0 0 1 13.12 7.26 L13.12 11.66 A1.46 1.46 0 0 1 11.66 13.12 L7.27 13.12 A1.46 1.46 0 0 1 5.8 11.66 Z", "fill": "currentColor"}), createElement(Path, {"d": "M6.54 2.88 A3.66 3.66 0 0 1 9.88 5.08 L7.27 5.08 A2.2 2.2 0 0 0 5.07 7.26 L5.07 9.89 A3.66 3.66 0 0 1 6.54 2.88", "fill": "currentColor"}));
});
