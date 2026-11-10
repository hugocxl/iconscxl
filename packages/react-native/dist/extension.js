import { createElement, forwardRef } from "react";
import { Svg, Path, Circle } from "react-native-svg";
export const ExtensionIcon = /*#__PURE__*/ forwardRef(function ExtensionIcon({size = 16, color = "currentColor", ...props}, ref) {
  return createElement(Svg, {...{"fill": "none", "viewBox": "0 0 16 16"}, width: size, height: size, color, ...props, ref} ,createElement(Path, {"d": "M7.25 3a.75.75 0 0 1 .75.75V8h4.25a.75.75 0 0 1 .75.75v3.75a1.5 1.5 0 0 1-1.5 1.5h-8A1.5 1.5 0 0 1 2 12.5v-8A1.5 1.5 0 0 1 3.5 3zM3 12.5a.5.5 0 0 0 .5.5H7V9H3zm5 .5h3.5a.5.5 0 0 0 .5-.5V9H8zM3.5 4a.5.5 0 0 0-.5.5V8h4V4zm10-3A1.5 1.5 0 0 1 15 2.5v3.75a.75.75 0 0 1-.75.75h-4.5A.75.75 0 0 1 9 6.25v-4.5A.75.75 0 0 1 9.75 1zM10 6h4V2.5a.5.5 0 0 0-.5-.5H10z", "fill": "currentColor"}));
});
