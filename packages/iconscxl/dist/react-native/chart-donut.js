import { createElement, forwardRef } from "react";
import { Svg, Path, Circle, Rect, G } from "react-native-svg";
export const ChartDonutIcon = /*#__PURE__*/ forwardRef(function ChartDonutIcon({size = 16, color = "currentColor", ...props}, ref) {
  return createElement(Svg, {...{"fill": "none", "viewBox": "0 0 16 16"}, width: size, height: size, color, ...props, ref} ,createElement(Path, {"d": "M2 8C2 4.9145 4.329 2.373 7.325 2.0375V4.7Q7.325 4.7332 7.3283 4.7662L7.3285 4.7684C5.8279 5.0786 4.7 6.4076 4.7 8C4.7 9.8225 6.1775 11.3 8 11.3C9.5924 11.3 10.9214 10.1721 11.2316 8.6715L11.2338 8.6717Q11.2668 8.675 11.3 8.675H13.9625C13.627 11.671 11.0855 14 8 14C4.6863 14 2 11.3137 2 8ZM11.3 7.325Q11.2668 7.325 11.2338 7.3283L11.2316 7.3285C10.9663 6.0448 9.9552 5.0337 8.6715 4.7684L8.6717 4.7662Q8.675 4.7332 8.675 4.7V2.0375C11.4494 2.3482 13.6518 4.5506 13.9625 7.325Z", "fill": "currentColor"}));
});
