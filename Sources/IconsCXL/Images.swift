import SwiftUI
#if canImport(UIKit)
import UIKit
#elseif canImport(AppKit)
import AppKit
#endif

extension Icon {
    /// A template image that inherits the caller's foreground style.
    public var image: Image { Image(rawValue, bundle: .module).renderingMode(.template) }
#if canImport(UIKit)
    /// The catalog image, suitable for tinting in UIKit.
    public var uiImage: UIImage? {
        UIImage(named: rawValue, in: .module, compatibleWith: nil)?.withRenderingMode(.alwaysTemplate)
    }
#elseif canImport(AppKit)
    /// The catalog image, suitable for tinting in AppKit.
    public var nsImage: NSImage? { Bundle.module.image(forResource: NSImage.Name(rawValue)) }
#endif
}
