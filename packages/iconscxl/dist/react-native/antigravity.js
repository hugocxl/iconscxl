import { createElement, forwardRef } from "react";
import { Svg, Path, Circle, Rect, G } from "react-native-svg";
export const AntigravityIcon = /*#__PURE__*/ forwardRef(function AntigravityIcon({size = 16, color = "currentColor", ...props}, ref) {
  return createElement(Svg, {...{"fill": "none", "viewBox": "0 0 16 16"}, width: size, height: size, color, ...props, ref} ,createElement(Path, {"d": "M8 0C1.42 0 0 1.42 0 8s1.42 8 8 8 8-1.42 8-8-1.42-8-8-8", "fill": "currentColor", "opacity": ".2"}), createElement(Path, {"d": "M12.17 12.51 C12.74 12.94 13.59 12.65 12.81 11.87 C10.44 9.58 10.96 3.27 8.02 3.27 C5.08 3.27 5.59 9.58 3.23 11.87 C2.36 12.73 3.29 12.94 3.86 12.51 C6.08 11 5.94 8.36 8.02 8.36 C10.09 8.36 9.95 11 12.17 12.51 Z", "fill": "currentColor", "fillRule": "evenodd"}));
});
