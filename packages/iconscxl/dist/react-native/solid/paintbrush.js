import { createElement, forwardRef } from "react";
import { Svg, Path, Circle, Rect, G } from "react-native-svg";
export const PaintbrushIcon = /*#__PURE__*/ forwardRef(function PaintbrushIcon({size = 16, color = "currentColor", ...props}, ref) {
  return createElement(Svg, {...{"fill": "none", "viewBox": "0 0 16 16"}, width: size, height: size, color, ...props, ref} ,createElement(Path, {"d": "M4.3168 8.7562 9.1653 1.9683Q9.2099 1.9058 9.2645 1.8517Q10.4387 0.6875 11.6875 0.6875Q12.9464 0.6875 14.1294 1.8706Q15.3125 3.0536 15.3125 4.3125Q15.3125 5.5613 14.1483 6.7355Q14.0942 6.7901 14.0317 6.8347L7.2438 11.6832Q7.1789 11.7295 7.107 11.7638Q7.035 11.7981 6.9581 11.8193Q6.8813 11.8404 6.802 11.8479Q6.7302 11.8546 6.6584 11.8498Q6.27 15.3125 0.6875 15.3125Q1.6875 14.3125 1.6875 12.3125Q1.2757 11.0772 1.7117 10.3506Q2.2601 9.4367 4.1493 9.3274Q4.1461 9.2627 4.1521 9.1981Q4.1595 9.1187 4.1807 9.0419Q4.2019 8.965 4.2362 8.893Q4.2705 8.8211 4.3168 8.7562Z", "fill": "currentColor"}));
});
