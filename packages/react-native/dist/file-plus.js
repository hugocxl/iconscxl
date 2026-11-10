import { createElement, forwardRef } from "react";
import { Svg, Path, Circle } from "react-native-svg";
export const FilePlusIcon = /*#__PURE__*/ forwardRef(function FilePlusIcon({size = 16, color = "currentColor", ...props}, ref) {
  return createElement(Svg, {...{"fill": "none", "viewBox": "0 0 16 16"}, width: size, height: size, color, ...props, ref} ,createElement(Path, {"d": "M9.5 1a.5.5 0 0 1 .354.146l4 4A.5.5 0 0 1 14 5.5v1.916A5 5 0 0 0 8 15H4.5A2.5 2.5 0 0 1 2 12.5v-9A2.5 2.5 0 0 1 4.5 1z", "fill": "currentColor", "opacity": ".4"}), createElement(Path, {"clipRule": "evenodd", "d": "M12 8a4 4 0 1 1 0 8 4 4 0 0 1 0-8m0 1.5a.5.5 0 0 0-.5.5v1.5H10a.5.5 0 0 0 0 1h1.5V14a.5.5 0 0 0 1 0v-1.5H14a.5.5 0 0 0 0-1h-1.5V10a.5.5 0 0 0-.5-.5", "fill": "currentColor", "fillRule": "evenodd"}));
});
