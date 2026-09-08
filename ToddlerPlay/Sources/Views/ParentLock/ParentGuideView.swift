import SwiftUI

/// Safe holding and hardware lock guide for parents
struct ParentGuideView: View {
    @Environment(\.dismiss) var dismiss
    
    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 14) {
                HStack {
                    Image(systemName: "hand.raised.fill")
                        .foregroundColor(.blue)
                        .font(.title3)
                    Text("Safety & Lock Guide")
                        .font(.headline)
                }
                .padding(.top, 4)
                
                // Tip 1: Screen Containment
                VStack(alignment: .leading, spacing: 4) {
                    Label("Screen Lockout", systemImage: "lock.shield.fill")
                        .font(.system(size: 13, weight: .bold))
                        .foregroundColor(.green)
                    Text("While TinyTouch is open, edge-to-edge gestures are absorbed by the app. Accidental phone calls, notification swipes, and watch face complications cannot be triggered by the toddler.")
                        .font(.system(size: 10))
                        .foregroundColor(.gray)
                }
                .padding(8)
                .background(RoundedRectangle(cornerRadius: 8).fill(Color.white.opacity(0.08)))
                
                // Tip 2: Digital Crown Taming
                VStack(alignment: .leading, spacing: 4) {
                    Label("Digital Crown Tamed", systemImage: "circle.circle")
                        .font(.system(size: 13, weight: .bold))
                        .foregroundColor(.orange)
                    Text("Turning the Crown won't dismiss the app or open system menus. Instead, it plays musical notes, inflates bubbles, and spins animals with haptic ticks!")
                        .font(.system(size: 10))
                        .foregroundColor(.gray)
                }
                .padding(8)
                .background(RoundedRectangle(cornerRadius: 8).fill(Color.white.opacity(0.08)))
                
                // Tip 3: Total Touch Freeze (Water Lock)
                VStack(alignment: .leading, spacing: 4) {
                    Label("Water Lock Trick", systemImage: "drop.fill")
                        .font(.system(size: 13, weight: .bold))
                        .foregroundColor(.cyan)
                    Text("If you want the child to watch animations or listen to lullabies with ZERO touch input, press your watch's Side Button and tap the Water Drop icon. Apple Watch will ignore all taps until you press and hold the Crown.")
                        .font(.system(size: 10))
                        .foregroundColor(.gray)
                }
                .padding(8)
                .background(RoundedRectangle(cornerRadius: 8).fill(Color.white.opacity(0.08)))
                
                // Tip 4: Screen Awake
                VStack(alignment: .leading, spacing: 4) {
                    Label("Screen Stays Awake", systemImage: "sun.max.fill")
                        .font(.system(size: 13, weight: .bold))
                        .foregroundColor(.yellow)
                    Text("TinyTouch runs an active extended session, keeping the display alive even when your wrist is angled while holding your toddler.")
                        .font(.system(size: 10))
                        .foregroundColor(.gray)
                }
                .padding(8)
                .background(RoundedRectangle(cornerRadius: 8).fill(Color.white.opacity(0.08)))
                
                Button(action: {
                    dismiss()
                }) {
                    Text("Got It")
                        .font(.system(size: 12, weight: .bold))
                        .frame(maxWidth: .infinity)
                }
                .padding(.top, 6)
            }
            .padding(.horizontal, 6)
        }
    }
}
