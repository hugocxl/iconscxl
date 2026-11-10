#!/usr/bin/env swift
import AppKit
import Foundation

// Native per-icon review: all available styles, 16/24/32pt, light/dark.
// Usage: swift scripts/icons/render-audit.swift ROOT OUT [category]
struct Entry: Decodable { let name: String; let category: String; let styles: [String] }
let args=CommandLine.arguments
let root=URL(fileURLWithPath:args.count>1 ? args[1] : ".")
let out=URL(fileURLWithPath:args.count>2 ? args[2] : "review/pages")
let catalog=try JSONDecoder().decode([Entry].self,from:Data(contentsOf:root.appendingPathComponent("catalog.json")))
try FileManager.default.createDirectory(at:out,withIntermediateDirectories:true)
let categories=Set(catalog.map(\.category)).sorted()
let scale:CGFloat=2, width:CGFloat=880, row:CGFloat=54, header:CGFloat=48
var manifest:[[String:Any]]=[]
for (categoryIndex,category) in categories.enumerated() {
    if args.count>3 && category != args[3] { continue }
    let entries=catalog.filter{$0.category==category}
    for page in stride(from:0,to:entries.count,by:18) {
        let batch=Array(entries[page..<min(page+18,entries.count)])
        let height=header+row*CGFloat(batch.count)
        let bitmap=NSBitmapImageRep(bitmapDataPlanes:nil,pixelsWide:Int(width*scale),pixelsHigh:Int(height*scale),bitsPerSample:8,samplesPerPixel:4,hasAlpha:true,isPlanar:false,colorSpaceName:.deviceRGB,bytesPerRow:0,bitsPerPixel:0)!
        let context=NSGraphicsContext(bitmapImageRep:bitmap)!
        NSGraphicsContext.saveGraphicsState();NSGraphicsContext.current=context
        context.cgContext.scaleBy(x:scale,y:scale)
        NSColor(white:0.87,alpha:1).setFill();NSRect(x:0,y:0,width:width,height:height).fill()
        func label(_ s:String,_ x:CGFloat,_ y:CGFloat,_ size:CGFloat=10) {
            (s as NSString).draw(at:NSPoint(x:x,y:y),withAttributes:[.font:NSFont.systemFont(ofSize:size),.foregroundColor:NSColor.black])
        }
        label(category,12,height-22,13)
        for (si,style) in ["duotone","solid","stroke"].enumerated(){label(style+"   16 · 24 · 32  /  16 · 24 · 32",160+CGFloat(si)*240,height-39,9)}
        for (i,entry) in batch.enumerated(){
            let y=height-header-row*CGFloat(i+1)
            label(entry.name,8,y+20,10)
            for (si,style) in ["duotone","solid","stroke"].enumerated(){
                guard entry.styles.contains(style) else { continue }
                let relative=style=="duotone" ? "icons/\(entry.name).svg" : "icons/styles/\(style)/\(entry.name).svg"
                guard let image=NSImage(contentsOf:root.appendingPathComponent(relative)),image.isValid else {fatalError(relative)}
                image.isTemplate=true
                for dark in 0...1 {for (ki,size) in [CGFloat(16),24,32].enumerated(){
                    let x=160+CGFloat(si)*240+CGFloat(dark*3+ki)*40
                    let tile=NSRect(x:x,y:y+5,width:40,height:44)
                    NSColor(white:dark==0 ? 0.98 : 0.09,alpha:1).setFill();tile.fill()
                    let tint=NSColor(white:dark==0 ? 0.08 : 0.98,alpha:1)
                    let tinted=NSImage(size:image.size,flipped:false){rect in
                        NSGraphicsContext.saveGraphicsState();defer{NSGraphicsContext.restoreGraphicsState()}
                        image.draw(in:rect);tint.set();rect.fill(using:.sourceAtop);return true
                    }
                    let fit=min(size/image.size.width,size/image.size.height)
                    let w=image.size.width*fit,h=image.size.height*fit
                    tinted.draw(in:NSRect(x:tile.midX-w/2,y:tile.midY-h/2,width:w,height:h),from:.zero,operation:.sourceOver,fraction:1)
                }}
            }
        }
        context.flushGraphics();NSGraphicsContext.restoreGraphicsState()
        let filename=String(format:"%02d-%02d.png",categoryIndex+1,page/18+1)
        try bitmap.representation(using:.png,properties:[:])!.write(to:out.appendingPathComponent(filename))
        manifest.append(["file":filename,"category":category,"names":batch.map(\.name)])
        print(filename+" "+category+": "+batch.map(\.name).joined(separator:", "))
    }
}
try JSONSerialization.data(withJSONObject:manifest,options:[.prettyPrinted,.sortedKeys]).write(to:out.appendingPathComponent("pages.json"))
