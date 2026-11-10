import { createElement, forwardRef } from "react";
import { Svg, Path, Circle } from "react-native-svg";
export const FileSymlinkIcon = /*#__PURE__*/ forwardRef(function FileSymlinkIcon({size = 16, color = "currentColor", ...props}, ref) {
  return createElement(Svg, {...{"fill": "none", "viewBox": "0 0 16 16"}, width: size, height: size, color, ...props, ref} ,createElement(Path, {"d": "M8 1 L8 4 A3 3 0 0 0 11 7 L14 7 L14 12.5 A2.5 2.5 0 0 1 11.49 15 L4.51 15 A2.5 2.5 0 0 1 2 12.5 L2 3.5 A2.5 2.5 0 0 1 4.51 1 Z", "fill": "currentColor", "opacity": ".4"}), createElement(Path, {"d": "M7.15 8.15 A0.5 0.5 0 0 1 7.85 8.85 L6.71 10 L10.5 10 A0.5 0.5 0 0 1 10.5 11 L6.71 11 L7.85 12.14 A0.5 0.5 0 1 1 7.15 12.85 L5.14 10.86 A0.5 0.5 0 0 1 5.14 10.15 Z M9.5 1 A0.5 0.5 0 0 1 9.85 1.15 L13.86 5.14 A0.5 0.5 0 0 1 14 5.5 L14 6 L11 6 A2 2 0 0 1 9 4 L9 1 Z", "fill": "currentColor"}));
});
