import { createElement, forwardRef } from "react";
import { Svg, Path, Circle, Rect, G } from "react-native-svg";
export const EllipsisVerticalIcon = /*#__PURE__*/ forwardRef(function EllipsisVerticalIcon({size = 16, color = "currentColor", ...props}, ref) {
  return createElement(Svg, {...{"fill": "none", "viewBox": "0 0 16 16"}, width: size, height: size, color, ...props, ref} ,createElement(Path, {"d": "M6.9 13C6.9 12.3925 7.3925 11.9 8 11.9C8.6075 11.9 9.1 12.3925 9.1 13C9.1 13.6075 8.6075 14.1 8 14.1C7.3925 14.1 6.9 13.6075 6.9 13ZM6.9 3C6.9 2.3925 7.3925 1.9 8 1.9C8.6075 1.9 9.1 2.3925 9.1 3C9.1 3.6075 8.6075 4.1 8 4.1C7.3925 4.1 6.9 3.6075 6.9 3Z", "fill": "currentColor", "opacity": "0.4"}), createElement(Path, {"d": "M6.9 8C6.9 8.6075 7.3925 9.1 8 9.1C8.6075 9.1 9.1 8.6075 9.1 8C9.1 7.3925 8.6075 6.9 8 6.9C7.3925 6.9 6.9 7.3925 6.9 8Z", "fill": "currentColor"}));
});
