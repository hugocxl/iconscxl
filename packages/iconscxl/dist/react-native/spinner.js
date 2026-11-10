import { createElement, forwardRef } from "react";
import { Svg, Path, Circle } from "react-native-svg";
export const SpinnerIcon = /*#__PURE__*/ forwardRef(function SpinnerIcon({size = 16, color = "currentColor", ...props}, ref) {
  return createElement(Svg, {...{"fill": "none", "viewBox": "0 0 16 16"}, width: size, height: size, color, ...props, ref} ,createElement(Path, {"d": "M8 1A7 7 0 1 1 1.3426 10.16312A.75 .75 0 0 1 2.76919 9.69959A5.5 5.5 0 1 0 8 2.5A.75 .75 0 0 1 8 1Z", "fill": "currentColor"}));
});
