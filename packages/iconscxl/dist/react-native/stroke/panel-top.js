import { createElement, forwardRef } from "react";
import { Svg, Path, Circle, Rect, G } from "react-native-svg";
export const PanelTopIcon = /*#__PURE__*/ forwardRef(function PanelTopIcon({size = 16, color = "currentColor", ...props}, ref) {
  return createElement(Svg, {...{"fill": "none", "viewBox": "0 0 16 16"}, width: size, height: size, color, ...props, ref} ,createElement(Path, {"d": "M3.5 1.375H12.5Q13.5873 1.375 14.3562 2.1438Q15.125 2.9127 15.125 4V12Q15.125 13.0873 14.3562 13.8562Q13.5873 14.625 12.5 14.625H3.5Q2.4127 14.625 1.6438 13.8562Q0.875 13.0873 0.875 12V4Q0.875 2.9127 1.6438 2.1438Q2.4127 1.375 3.5 1.375ZM2.125 6.675V12Q2.125 12.5695 2.5277 12.9723Q2.9305 13.375 3.5 13.375H12.5Q13.0695 13.375 13.4723 12.9723Q13.875 12.5695 13.875 12V6.675H2.125ZM3.5 2.625Q2.9305 2.625 2.5277 3.0277Q2.125 3.4305 2.125 4V5.325H13.875V4Q13.875 3.4305 13.4723 3.0277Q13.0695 2.625 12.5 2.625Z", "fill": "currentColor"}));
});
