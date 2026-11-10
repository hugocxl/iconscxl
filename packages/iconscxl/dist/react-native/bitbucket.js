import { createElement, forwardRef } from "react";
import { Svg, Path, Circle, Rect, G } from "react-native-svg";
export const BitbucketIcon = /*#__PURE__*/ forwardRef(function BitbucketIcon({size = 16, color = "currentColor", ...props}, ref) {
  return createElement(Svg, {...{"fill": "none", "viewBox": "0 0 16 16"}, width: size, height: size, color, ...props, ref} ,createElement(Path, {"d": "M8 0C1.42 0 0 1.42 0 8s1.42 8 8 8 8-1.42 8-8-1.42-8-8-8", "fill": "currentColor", "opacity": ".2"}), createElement(Path, {"d": "M3.2 3.39 A0.34 0.34 0 0 0 2.88 3.77 L4.27 12.24 C4.31 12.45 4.49 12.61 4.71 12.61 L11.4 12.61 A0.34 0.34 0 0 0 11.72 12.33 L13.12 3.77 A0.34 0.34 0 0 0 12.8 3.39 Z M9.08 9.51 L6.95 9.51 L6.37 6.49 L9.59 6.49 Z", "fill": "currentColor"}));
});
