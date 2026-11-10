import { createElement, forwardRef } from "react";
import { Svg, Path, Circle, Rect, G } from "react-native-svg";
export const ChartDonutIcon = /*#__PURE__*/ forwardRef(function ChartDonutIcon({size = 16, color = "currentColor", ...props}, ref) {
  return createElement(Svg, {...{"fill": "none", "viewBox": "0 0 16 16"}, width: size, height: size, color, ...props, ref} ,createElement(Path, {"d": "M2 8C2 4.6863 4.6863 2 8 2V4.7C6.1775 4.7 4.7 6.1775 4.7 8C4.7 9.8225 6.1775 11.3 8 11.3C9.8225 11.3 11.3 9.8225 11.3 8H14C14 11.3137 11.3137 14 8 14C4.6863 14 2 11.3137 2 8Z", "fill": "currentColor", "opacity": "0.3"}), createElement(Path, {"d": "M14 8H11.3C11.3 6.1775 9.8225 4.7 8 4.7V2C11.3137 2 14 4.6863 14 8Z", "fill": "currentColor"}));
});
