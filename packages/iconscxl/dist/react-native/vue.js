import { createElement, forwardRef } from "react";
import { Svg, Path, Circle } from "react-native-svg";
export const VueIcon = /*#__PURE__*/ forwardRef(function VueIcon({size = 16, color = "currentColor", ...props}, ref) {
  return createElement(Svg, {...{"fill": "none", "viewBox": "0 0 16 16"}, width: size, height: size, color, ...props, ref} ,createElement(Path, {"d": "M8 0C1.42 0 0 1.42 0 8s1.42 8 8 8 8-1.42 8-8-1.42-8-8-8", "fill": "currentColor", "opacity": ".2"}), createElement(Path, {"d": "M9.18 3.61 L8 5.63 L6.82 3.61 L2.88 3.61 L8 12.39 L13.12 3.61 Z M9.18 3.61 L8 5.63 L6.82 3.61 L5.07 3.61 L8 8.74 L10.93 3.61 Z", "fill": "currentColor", "fillRule": "evenodd"}));
});
