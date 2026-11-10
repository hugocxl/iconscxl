import Testing
@testable import TabIcons

@Test func iconNamesAreUniqueAndRoundTrip() {
    let icons = TabIcon.allCases
    #expect(!icons.isEmpty)
    #expect(Set(icons.map(\.rawValue)).count == icons.count)
    for icon in icons {
        #expect(TabIcon(rawValue: icon.rawValue) == icon)
    }
    #expect(TabIcon(rawValue: "not-an-icon") == nil)
}

@Test func swiftUIImagesCanBeCreated() {
    for icon in TabIcon.allCases {
        _ = icon.image
    }
}

#if canImport(AppKit)
@Test func appKitImagesLoadFromTheResourceBundle() {
    for icon in TabIcon.allCases {
        #expect(icon.nsImage != nil, "Missing image: \(icon.rawValue)")
        #expect(icon.nsImage?.isTemplate == true)
    }
}
#endif
