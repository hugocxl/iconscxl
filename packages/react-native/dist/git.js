import { createElement, forwardRef } from "react";
import { Svg, Path, Circle } from "react-native-svg";
export const GitIcon = /*#__PURE__*/ forwardRef(function GitIcon({size = 16, color = "currentColor", ...props}, ref) {
  return createElement(Svg, {...{"fill": "none", "viewBox": "0 0 16 16"}, width: size, height: size, color, ...props, ref} ,createElement(Path, {"d": "M8 0C1.42 0 0 1.42 0 8s1.42 8 8 8 8-1.42 8-8-1.42-8-8-8", "fill": "currentColor", "opacity": ".2"}), createElement(Path, {"d": "M12.94 7.54 L8.46 3.06 A0.66 0.66 0 0 0 7.53 3.06 L6.6 3.99 L7.78 5.17 A0.78 0.78 0 0 1 8.77 6.17 L9.91 7.31 A0.78 0.78 0 0 1 10.71 8.6 A0.78 0.78 0 0 1 9.45 7.76 L8.37 6.69 L8.37 9.48 A0.78 0.78 0 1 1 7.72 9.46 L7.72 6.65 A0.78 0.78 0 0 1 7.3 5.62 L6.13 4.44 L3.07 7.52 A0.66 0.66 0 0 0 3.07 8.45 L7.54 12.93 A0.66 0.66 0 0 0 8.48 12.93 L12.93 8.47 A0.66 0.66 0 0 0 12.93 7.54", "fill": "currentColor"}));
});
