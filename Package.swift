// swift-tools-version: 6.0
import PackageDescription
let package = Package(
    name: "TabIcons",
    platforms: [.macOS(.v12), .iOS(.v15), .tvOS(.v15), .watchOS(.v8)],
    products: [.library(name: "TabIcons", targets: ["TabIcons"])],
    targets: [
        .target(name: "TabIcons", resources: [.process("Resources")]),
        .testTarget(name: "TabIconsTests", dependencies: ["TabIcons"], path: "tests/TabIconsTests")
    ]
)
