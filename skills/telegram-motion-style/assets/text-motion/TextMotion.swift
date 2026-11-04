import Foundation

/// Renderer-neutral Normal/Emotional properties. See references/text-motion.md for source/adaptation boundaries.
public enum TextMotionStyle: String, Sendable { case normal, emotional }
public enum TextMotionPreset: String, Sendable { case promo, source }
public struct TextMotionProperties: Sendable {
    public var opacity: Double
    public var y: Double
    public var scaleY: Double
    public var rotation: Double
    public var blur: Double
    public static let natural = Self(opacity: 1, y: 0, scaleY: 1, rotation: 0, blur: 0)
}
public struct TextMotionTiming: Sendable {
    public var stagger: Double
    public var duration: Double
    public var firstDelay: Double
    public var pixelsPerUnit: Double
    public init(style: TextMotionStyle = .normal, preset: TextMotionPreset = .promo,
                stagger: Double? = nil, duration: Double? = nil,
                firstDelay: Double? = nil, pixelsPerUnit: Double = 1) {
        let baseStagger = preset == .promo ? 0.018 : style == .normal ? 0.015 : 0.025
        self.stagger = stagger ?? baseStagger
        self.duration = duration ?? (preset == .promo ? 0.300 : style == .normal ? 0.500 : 0.680)
        self.firstDelay = firstDelay ?? (preset == .promo ? self.stagger : style == .normal ? 0 : 0.025)
        self.pixelsPerUnit = pixelsPerUnit
        precondition([self.stagger, self.duration, self.firstDelay, pixelsPerUnit].allSatisfy(\.isFinite))
        precondition(self.stagger >= 0 && self.duration > 0 && self.firstDelay >= 0 && pixelsPerUnit > 0)
    }
    public func totalDuration(unitCount: Int) -> Double {
        precondition(unitCount >= 0)
        return unitCount == 0 ? 0 : firstDelay + Double(unitCount - 1) * stagger + duration
    }
}
public enum TextMotion {
    private static func clamp(_ x: Double) -> Double { min(1, max(0, x)) }
    public static func normalEase(_ time: Double) -> Double {
        let time = clamp(time)
        func bezier(_ u: Double, _ p: Double, _ q: Double) -> Double {
            3 * pow(1-u, 2) * u * p + 3 * (1-u) * u*u * q + u*u*u
        }
        var lo = 0.0, hi = 1.0
        for _ in 0..<36 {
            let u = (lo + hi)/2
            if bezier(u, 0.2, 0.2) < time { lo = u } else { hi = u }
        }
        return bezier((lo + hi)/2, 0.8, 1)
    }
    public static func emotionalSelector(local: Double, duration: Double = 0.300) -> Double {
        precondition(local.isFinite && duration.isFinite && duration > 0)
        if local <= 0 { return 1 }
        if local >= duration { return 0 }
        let t = local * (0.680 / duration)
        if t < 0.180 { return 1 - t / 0.180 }
        let d = t - 0.180, w = 2 * Double.pi
        return (-1 / 0.180) * sin(d*w) / (exp(10*d)*w)
    }
    public static func sample(style: TextMotionStyle, elapsed: Double, index: Int = 0,
                              timing: TextMotionTiming) -> TextMotionProperties {
        precondition(elapsed.isFinite && index >= 0)
        let local = elapsed - timing.firstDelay - Double(index) * timing.stagger
        if local >= timing.duration { return .natural }
        switch style {
        case .normal:
            let e = local <= 0 ? 0 : normalEase(local / timing.duration)
            return .init(opacity: e, y: 15 * (1-e) / timing.pixelsPerUnit, scaleY: 1, rotation: 0, blur: 0)
        case .emotional:
            let p = emotionalSelector(local: local, duration: timing.duration)
            return .init(opacity: clamp(1-p), y: 32*p / timing.pixelsPerUnit,
                         scaleY: 1 - 0.22*p, rotation: 12*p, blur: 10*max(p,0) / timing.pixelsPerUnit)
        }
    }
}
