import { createElement, forwardRef } from "react";
import { Svg, Path, Circle } from "react-native-svg";
export const DotIcon = /*#__PURE__*/ forwardRef(function DotIcon({size = 16, color = "currentColor", ...props}, ref) {
  return createElement(Svg, {...{"fill": "none", "viewBox": "0 0 16 16"}, width: size, height: size, color, ...props, ref} ,createElement(Circle, {"cx": "8", "cy": "8", "fill": "currentColor", "r": "2"}));
});
