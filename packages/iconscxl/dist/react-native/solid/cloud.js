import { createElement, forwardRef } from "react";
import { Svg, Path, Circle, Rect, G } from "react-native-svg";
export const CloudIcon = /*#__PURE__*/ forwardRef(function CloudIcon({size = 16, color = "currentColor", ...props}, ref) {
  return createElement(Svg, {...{"fill": "none", "viewBox": "0 0 16 16"}, width: size, height: size, color, ...props, ref} ,createElement(Path, {"d": "M4.132 13.6609Q2.4105 13.6609 1.4263 12.5048Q0.5583 11.4852 0.6034 10.0206Q0.6241 9.3469 0.8561 8.7221Q1.0981 8.0702 1.5348 7.5693Q2.3457 6.6391 3.5429 6.4609Q3.7387 4.6872 4.9768 3.5499Q5.614 2.9645 6.4459 2.6507Q7.2447 2.3495 8.1119 2.3394Q8.9816 2.3293 9.7883 2.6137Q10.6319 2.9111 11.2871 3.4899Q12.5895 4.6405 12.8256 6.5161Q14.0465 6.8183 14.7532 7.8122Q15.5125 8.88 15.3788 10.2724Q15.2454 11.6629 14.2922 12.6082Q13.2309 13.6609 11.5993 13.6609Z", "fill": "currentColor"}));
});
