import { createElement, forwardRef } from "react";
import { Svg, Path, Circle } from "react-native-svg";
export const FolderPlusIcon = /*#__PURE__*/ forwardRef(function FolderPlusIcon({size = 16, color = "currentColor", ...props}, ref) {
  return createElement(Svg, {...{"fill": "none", "viewBox": "0 0 16 16"}, width: size, height: size, color, ...props, ref} ,createElement(Path, {"d": "M14 7.416A5 5 0 0 0 7.417 14H2a2 2 0 0 1-2-2V6h14zM4.585 2a2 2 0 0 1 1.028.285l1.788 1.072a1 1 0 0 0 .514.143H12A2 2 0 0 1 13.935 5H0V4a2 2 0 0 1 2-2z", "fill": "currentColor"}), createElement(Path, {"clipRule": "evenodd", "d": "M12 8a4 4 0 1 1 0 8 4 4 0 0 1 0-8m0 1.5a.5.5 0 0 0-.5.5v1.5H10a.5.5 0 0 0 0 1h1.5V14a.5.5 0 0 0 1 0v-1.5H14a.5.5 0 0 0 0-1h-1.5V10a.5.5 0 0 0-.5-.5", "fill": "currentColor", "fillRule": "evenodd"}));
});
