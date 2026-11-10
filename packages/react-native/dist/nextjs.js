import { createElement, forwardRef } from "react";
import { Svg, Path, Circle } from "react-native-svg";
export const NextjsIcon = /*#__PURE__*/ forwardRef(function NextjsIcon({size = 16, color = "currentColor", ...props}, ref) {
  return createElement(Svg, {...{"fill": "none", "viewBox": "0 0 16 16"}, width: size, height: size, color, ...props, ref} ,createElement(Path, {"d": "M8 0C1.42 0 0 1.42 0 8s1.42 8 8 8 8-1.42 8-8-1.42-8-8-8", "fill": "currentColor", "opacity": ".2"}), createElement(Path, {"d": "M3.61 2.88 L4.72 2.88 L4.72 9.53 L3.61 9.53 Z", "fill": "currentColor"}), createElement(Path, {"d": "M5 2.88 L12.39 12.44 Q11.98 12.82 11.52 13.12 L4.72 4.3 Z", "fill": "currentColor"}), createElement(Path, {"d": "M10.32 2.88 L9.22 2.88 L9.22 9.54 L10.32 9.54 Z", "fill": "currentColor"}));
});
