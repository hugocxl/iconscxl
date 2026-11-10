import { createElement, forwardRef } from "react";
import { Svg, Path, Circle } from "react-native-svg";
export const FolderOpenIcon = /*#__PURE__*/ forwardRef(function FolderOpenIcon({size = 16, color = "currentColor", ...props}, ref) {
  return createElement(Svg, {...{"fill": "none", "viewBox": "0 0 16 16"}, width: size, height: size, color, ...props, ref} ,createElement(Path, {"d": "M13.68 6.22 A1.33 1.33 0 0 1 14.94 7.93 L13.71 12.07 A1.78 1.78 0 0 1 12 13.33 L3.18 13.33 A1.78 1.78 0 0 1 1.47 11.09 L2.52 7.2 A1.33 1.33 0 0 1 3.82 6.22 Z", "fill": "currentColor"}), createElement(Path, {"d": "M5.08 2.67 A1.78 1.78 0 0 1 5.98 2.92 L7.59 3.88 A0.88 0.88 0 0 0 8.03 4 L11.66 4 A1.78 1.78 0 0 1 13.39 5.33 L3.82 5.33 A2.22 2.22 0 0 0 1.67 6.98 L1 9.44 L1 4.45 A1.78 1.78 0 0 1 2.78 2.67 Z", "fill": "currentColor", "opacity": ".5"}));
});
