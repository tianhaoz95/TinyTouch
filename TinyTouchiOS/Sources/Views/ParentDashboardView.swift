import SwiftUI

/// Main iOS Companion Dashboard for parents.
/// Provides safety instructions, game mode previews, screen time guidance,
/// and privacy disclosures.
struct ParentDashboardView: View {
    @State private var showingSafetyGuide = false
    @State private var showingGamePreview = false
    
    var body: some View {
        NavigationStack {
            ScrollView {
                VStack(spacing: 20) {
                    // Hero Banner
                    VStack(alignment: .leading, spacing: 12) {
                        HStack(spacing: 12) {
                            ZStack {
                                RoundedRectangle(cornerRadius: 16)
                                    .fill(
                                        LinearGradient(
                                            colors: [.pink, .purple],
                                            startPoint: .topLeading,
                                            endPoint: .bottomTrailing
                                        )
                                    )
                                    .frame(width: 54, height: 54)
                                
                                Image(systemName: "applewatch.radiowaves.left.and.right")
                                    .font(.title2)
                                    .foregroundColor(.white)
                            }
                            
                            VStack(alignment: .leading, spacing: 2) {
                                Text("TinyTouch")
                                    .font(.title2.weight(.bold))
                                Text("Companion & Safety Hub")
                                    .font(.subheadline)
                                    .foregroundColor(.secondary)
                            }
                        }
                        
                        Text("Transform your Apple Watch into a safe, engaging sensory playground while preventing accidental calls, SOS dials, and unwanted taps.")
                            .font(.subheadline)
                            .foregroundColor(.secondary)
                            .lineSpacing(4)
                        
                        HStack {
                            Image(systemName: "checkmark.seal.fill")
                                .foregroundColor(.green)
                            Text("Apple Watch App Included & Auto-Installed")
                                .font(.footnote.weight(.semibold))
                                .foregroundColor(.green)
                        }
                        .padding(.top, 4)
                    }
                    .padding(20)
                    .frame(maxWidth: .infinity, alignment: .leading)
                    .background(Color(uiColor: .secondarySystemBackground))
                    .cornerRadius(20)
                    
                    // Action 1: Safety Guide
                    NavigationLink(destination: SafetyGuideView()) {
                        HStack(spacing: 16) {
                            ZStack {
                                Circle()
                                    .fill(Color.red.opacity(0.15))
                                    .frame(width: 50, height: 50)
                                Image(systemName: "shield.checkered")
                                    .font(.title3.weight(.bold))
                                    .foregroundColor(.red)
                            }
                            
                            VStack(alignment: .leading, spacing: 4) {
                                Text("Toddler Lock & SOS Guide")
                                    .font(.headline)
                                    .foregroundColor(.primary)
                                Text("Disable accidental 911 calls & lock touch inputs")
                                    .font(.subheadline)
                                    .foregroundColor(.secondary)
                            }
                            
                            Spacer()
                            Image(systemName: "chevron.right")
                                .foregroundColor(.secondary)
                        }
                        .padding(16)
                        .background(Color(uiColor: .secondarySystemBackground))
                        .cornerRadius(16)
                    }
                    
                    // Action 2: Interactive Sandbox Preview
                    NavigationLink(destination: GamePreviewView()) {
                        HStack(spacing: 16) {
                            ZStack {
                                Circle()
                                    .fill(Color.blue.opacity(0.15))
                                    .frame(width: 50, height: 50)
                                Image(systemName: "sparkles.rectangle.stack.fill")
                                    .font(.title3.weight(.bold))
                                    .foregroundColor(.blue)
                            }
                            
                            VStack(alignment: .leading, spacing: 4) {
                                Text("Sensory Games Preview")
                                    .font(.headline)
                                    .foregroundColor(.primary)
                                Text("Test the 5 activities, sounds & music on iPhone")
                                    .font(.subheadline)
                                    .foregroundColor(.secondary)
                            }
                            
                            Spacer()
                            Image(systemName: "chevron.right")
                                .foregroundColor(.secondary)
                        }
                        .padding(16)
                        .background(Color(uiColor: .secondarySystemBackground))
                        .cornerRadius(16)
                    }
                    
                    // Screen Time Best Practices
                    VStack(alignment: .leading, spacing: 12) {
                        Label("Pediatric Screen Time Recommendations", systemImage: "clock.badge.checkmark")
                            .font(.headline)
                            .foregroundColor(.primary)
                        
                        Text("For toddlers between 12-24 months, high-stimulation content should be limited. TinyTouch is built with:")
                            .font(.footnote)
                            .foregroundColor(.secondary)
                        
                        VStack(alignment: .leading, spacing: 8) {
                            RecommendationRow(icon: "speaker.wave.1.fill", color: .purple, title: "Gentle Audio Levels", desc: "Acoustic chimes and soft pops that never startle.")
                            RecommendationRow(icon: "hand.tap.fill", color: .orange, title: "Tactile Taptic Feedback", desc: "Haptic reinforcement connected directly to motor action.")
                            RecommendationRow(icon: "timer", color: .blue, title: "Recommended 3-5m Sessions", desc: "Use the built-in timer on the watch to gently wrap up play.")
                            RecommendationRow(icon: "moon.fill", color: .indigo, title: "Calming Bedtime Mode", desc: "Dark background with lullaby chimes for winding down.")
                        }
                    }
                    .padding(20)
                    .frame(maxWidth: .infinity, alignment: .leading)
                    .background(Color(uiColor: .secondarySystemBackground))
                    .cornerRadius(20)
                    
                    // Privacy & Trust
                    HStack(spacing: 14) {
                        Image(systemName: "lock.circle.fill")
                            .font(.system(size: 36))
                            .foregroundColor(.green)
                        
                        VStack(alignment: .leading, spacing: 2) {
                            Text("100% Kid-Safe & Private")
                                .font(.subheadline.weight(.semibold))
                            Text("No internet access required. Zero tracking, zero ads, zero data collection ever.")
                                .font(.caption)
                                .foregroundColor(.secondary)
                        }
                    }
                    .padding(16)
                    .frame(maxWidth: .infinity, alignment: .leading)
                    .background(Color.green.opacity(0.1))
                    .cornerRadius(16)
                    
                    // Version info
                    Text("TinyTouch v1.0.0 • Built with love for curious toddlers")
                        .font(.caption2)
                        .foregroundColor(.secondary)
                        .padding(.top, 10)
                        .padding(.bottom, 20)
                }
                .padding()
            }
            .navigationTitle("TinyTouch")
        }
    }
}

struct RecommendationRow: View {
    let icon: String
    let color: Color
    let title: String
    let desc: String
    
    var body: some View {
        HStack(alignment: .top, spacing: 10) {
            Image(systemName: icon)
                .foregroundColor(color)
                .frame(width: 20)
                .padding(.top, 2)
            
            VStack(alignment: .leading, spacing: 2) {
                Text(title)
                    .font(.footnote.weight(.semibold))
                Text(desc)
                    .font(.caption)
                    .foregroundColor(.secondary)
            }
        }
    }
}
