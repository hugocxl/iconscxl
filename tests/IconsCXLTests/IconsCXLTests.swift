import Testing
@testable import IconsCXL

@Test func iconNamesAreUniqueAndRoundTrip() {
    let icons = Icon.allCases
    #expect(!icons.isEmpty)
    #expect(Set(icons.map(\.rawValue)).count == icons.count)
    for icon in icons {
        #expect(Icon(rawValue: icon.rawValue) == icon)
    }
    #expect(Icon(rawValue: "not-an-icon") == nil)
}

@Test func swiftUIImagesCanBeCreated() {
    for icon in Icon.allCases {
        _ = icon.image
    }
}

#if canImport(AppKit)
@Test func appKitImagesLoadFromTheResourceBundle() {
    for icon in Icon.allCases {
        #expect(icon.nsImage != nil, "Missing image: \(icon.rawValue)")
        #expect(icon.nsImage?.isTemplate == true)
    }
}
#endif
