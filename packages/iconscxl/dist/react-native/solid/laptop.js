import { createElement, forwardRef } from "react";
import { Svg, Path, Circle, Rect, G } from "react-native-svg";
export const LaptopIcon = /*#__PURE__*/ forwardRef(function LaptopIcon({size = 16, color = "currentColor", ...props}, ref) {
  return createElement(Svg, {...{"fill": "none", "viewBox": "0 0 16 16"}, width: size, height: size, color, ...props, ref} ,createElement(Path, {"d": "M4 1.375H12Q12.6731 1.375 13.149 1.851Q13.625 2.3269 13.625 3V10Q13.625 10.5709 13.2826 11H14L15 14H1L2 11H2.7174Q2.375 10.5709 2.375 10V3Q2.375 2.3269 2.851 1.851Q3.3269 1.375 4 1.375Z", "fill": "currentColor"}));
});
