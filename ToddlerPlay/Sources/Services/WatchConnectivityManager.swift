import Foundation
import WatchConnectivity

/// Manages bidirectional synchronization between the Apple Watch app and the iPhone companion app.
final class WatchConnectivityManager: NSObject, ObservableObject, WCSessionDelegate {
    static let shared = WatchConnectivityManager()
    
    weak var appState: AppState?
    
    @Published var isReachable: Bool = false
    
    private override init() {
        super.init()
        activateSession()
    }
    
    func activateSession() {
        guard WCSession.isSupported() else { return }
        let session = WCSession.default
        session.delegate = self
        session.activate()
    }
    
    // MARK: - WCSessionDelegate (watchOS)
    
    func session(_ session: WCSession, activationDidCompleteWith activationState: WCSessionActivationState, error: Error?) {
        DispatchQueue.main.async {
            self.isReachable = session.isReachable
            if activationState == .activated {
                // Check if there's any existing application context from phone
                self.applySettings(session.receivedApplicationContext)
            }
        }
    }
    
    func sessionReachabilityDidChange(_ session: WCSession) {
        DispatchQueue.main.async {
            self.isReachable = session.isReachable
            if session.isReachable {
                self.sendStatusUpdate()
            }
        }
    }
    
    func session(_ session: WCSession, didReceiveApplicationContext applicationContext: [String : Any]) {
        DispatchQueue.main.async {
            self.applySettings(applicationContext)
        }
    }
    
    func session(_ session: WCSession, didReceiveMessage message: [String : Any], replyHandler: @escaping ([String : Any]) -> Void) {
        DispatchQueue.main.async {
            self.applySettings(message)
            replyHandler(["status": "acknowledged"])
        }
    }
    
    // MARK: - Applying incoming settings from iPhone
    
    func applySettings(_ dict: [String: Any]) {
        guard let appState = self.appState else { return }
        
        // 1. Game mode change
        if let modeRaw = dict["currentMode"] as? String, let mode = GameMode(rawValue: modeRaw) {
            if appState.currentMode != mode {
                appState.currentMode = mode
            }
        }
        
        // 2. Sensory toggles
        if let sound = dict["soundEnabled"] as? Bool {
            appState.soundEnabled = sound
        }
        if let voice = dict["voiceEnabled"] as? Bool {
            appState.voiceEnabled = voice
        }
        if let haptics = dict["hapticsEnabled"] as? Bool {
            appState.hapticsEnabled = haptics
        }
        if let lowStim = dict["lowStimulation"] as? Bool {
            appState.lowStimulation = lowStim
        }
        
        // 3. Timer change
        if let timerMinutes = dict["timerMinutes"] as? Int {
            appState.setPlayTimer(minutes: timerMinutes)
        }
        
        // 4. Remote actions
        if let action = dict["action"] as? String {
            if action == "triggerLullaby" {
                appState.currentMode = .lullaby
            }
        }
        
        // 5. Lock hold duration
        if let holdDuration = dict["lockHoldDuration"] as? Double {
            appState.lockHoldDuration = holdDuration
        }
    }
    
    // MARK: - Sending live telemetry to iPhone
    
    func sendStatusUpdate() {
        guard WCSession.isSupported() else { return }
        let session = WCSession.default
        guard session.activationState == .activated else { return }
        
        guard let appState = self.appState else { return }
        
        let telemetry: [String: Any] = [
            "currentMode": appState.currentMode.rawValue,
            "touchesCount": appState.sessionTouchesCount,
            "isTimerActive": appState.isTimerActive,
            "remainingSeconds": appState.remainingSeconds,
            "soundEnabled": appState.soundEnabled,
            "voiceEnabled": appState.voiceEnabled,
            "hapticsEnabled": appState.hapticsEnabled,
            "lowStimulation": appState.lowStimulation,
            "timestamp": Date().timeIntervalSince1970
        ]
        
        // If reachable, send immediate message
        if session.isReachable {
            session.sendMessage(telemetry, replyHandler: nil, errorHandler: nil)
        }
        
        // Also update application context so iPhone gets it even if backgrounded
        do {
            try session.updateApplicationContext(telemetry)
        } catch {
            // Context update may fail if identical, which is fine
        }
    }
}
