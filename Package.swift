// swift-tools-version: 6.0
import PackageDescription
let package = Package(
    name: "IconsCXL",
    platforms: [.macOS(.v12), .iOS(.v15), .tvOS(.v15), .watchOS(.v8)],
    products: [.library(name: "IconsCXL", targets: ["IconsCXL"])],
    targets: [
        .target(name: "IconsCXL", resources: [.process("Resources")]),
        .testTarget(name: "IconsCXLTests", dependencies: ["IconsCXL"], path: "tests/IconsCXLTests")
    ]
)
