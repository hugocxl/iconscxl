import { createElement, forwardRef } from "react";
import { Svg, Path, Circle, Rect, G } from "react-native-svg";
export const PillIcon = /*#__PURE__*/ forwardRef(function PillIcon({size = 16, color = "currentColor", ...props}, ref) {
  return createElement(Svg, {...{"fill": "none", "viewBox": "0 0 16 16"}, width: size, height: size, color, ...props, ref} ,createElement(Path, {"d": "M13.3917 2.6083Q14.0568 3.2734 14.4076 4.1386Q14.7463 4.9738 14.7463 5.8787Q14.7463 6.7835 14.4076 7.6188Q14.0567 8.484 13.3917 9.149L9.149 13.3917Q8.484 14.0567 7.6188 14.4076Q6.7835 14.7463 5.8787 14.7463Q4.9738 14.7463 4.1386 14.4076Q3.2734 14.0568 2.6083 13.3917Q1.9432 12.7266 1.5924 11.8614Q1.2537 11.0262 1.2537 10.1213Q1.2537 9.2165 1.5924 8.3812Q1.9433 7.516 2.6083 6.851L6.851 2.6083Q7.516 1.9432 8.3812 1.5924Q9.2165 1.2537 10.1213 1.2537Q11.0262 1.2537 11.8614 1.5924Q12.7266 1.9432 13.3917 2.6083ZM4.8887 5.8433 10.1567 11.1113 11.1113 10.1567 5.8433 4.8887Z", "fill": "currentColor"}));
});
