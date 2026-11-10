import { createElement, forwardRef } from "react";
import { Svg, Path, Circle, Rect, G } from "react-native-svg";
export const CopyIcon = /*#__PURE__*/ forwardRef(function CopyIcon({size = 16, color = "currentColor", ...props}, ref) {
  return createElement(Svg, {...{"fill": "none", "viewBox": "0 0 16 16"}, width: size, height: size, color, ...props, ref} ,createElement(Path, {"d": "M6.7 4.375H12.8Q13.763 4.375 14.444 5.056Q15.125 5.737 15.125 6.7V12.8Q15.125 13.763 14.444 14.444Q13.763 15.125 12.8 15.125H6.7Q5.737 15.125 5.056 14.444Q4.375 13.763 4.375 12.8V6.7Q4.375 5.737 5.056 5.056Q5.737 4.375 6.7 4.375ZM3.2 0.875H8.8Q9.763 0.875 10.444 1.556Q11.125 2.237 11.125 3.2V3.625H6.7Q5.4263 3.625 4.5256 4.5256Q3.625 5.4263 3.625 6.7V12.125H3.2Q2.237 12.125 1.556 11.444Q0.875 10.763 0.875 9.8V3.2Q0.875 2.237 1.556 1.556Q2.237 0.875 3.2 0.875Z", "fill": "currentColor"}));
});
