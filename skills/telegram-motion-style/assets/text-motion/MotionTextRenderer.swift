import SwiftUI

@available(iOS 18.0, macOS 15.0, tvOS 18.0, watchOS 11.0, visionOS 2.0, *)
private struct MotionUnitIndex: TextAttribute { let value: Int }

/// Tags extended grapheme clusters once, before line wrapping. Newlines have no extra clock delay.
/// Keep this tagged Text stable while elapsed changes; do not rebuild the application's text binding per frame.
@available(iOS 18.0, macOS 15.0, tvOS 18.0, watchOS 11.0, visionOS 2.0, *)
public func motionTaggedText(_ string: String) -> Text {
    var text = Text("")
    var index = 0
    for character in string {
        if character.isNewline { text = Text("\(text)\(String(character))"); continue }
        let unit = Text(String(character)).customAttribute(MotionUnitIndex(value: index))
        text = Text("\(text)\(unit)")
        index += 1
    }
    return text
}

/// An elapsed-time renderer, not a TextField replacement or an animation clock.
/// Host owns typography, layout, binding, timing, reduced-motion behavior and capture lifecycle.
@available(iOS 18.0, macOS 15.0, tvOS 18.0, watchOS 11.0, visionOS 2.0, *)
public struct MotionTextRenderer: TextRenderer {
    public var elapsed: Double
    public var style: TextMotionStyle
    public var timing: TextMotionTiming
    public init(elapsed: Double, style: TextMotionStyle = .gentle,
                timing: TextMotionTiming = .init()) {
        self.elapsed = elapsed; self.style = style; self.timing = timing
    }
    public func draw(layout: Text.Layout, in context: inout GraphicsContext) {
        for line in layout {
            for run in line {
                guard let unit = run[MotionUnitIndex.self] else { context.draw(run); continue }
                let p = TextMotion.sample(style: style, elapsed: elapsed, index: unit.value, timing: timing)
                guard p.opacity > 0 else { continue }
                var copy = context
                let rect = run.typographicBounds.rect
                copy.opacity *= p.opacity
                copy.translateBy(x: rect.midX, y: rect.midY + p.y)
                copy.rotate(by: .degrees(p.rotation))
                copy.scaleBy(x: 1, y: p.scaleY)
                copy.translateBy(x: -rect.midX, y: -rect.midY)
                if style == .emotional && p.blur > 0 { copy.addFilter(.blur(radius: p.blur)) }
                copy.draw(run)
            }
        }
    }
}
