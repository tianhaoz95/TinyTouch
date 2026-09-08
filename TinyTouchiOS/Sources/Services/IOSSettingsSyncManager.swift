import Foundation
import WatchConnectivity
import Combine

/// Manages live settings synchronization and remote control from the iPhone companion app
/// to the Apple Watch app via WatchConnectivity.
final class IOSSettingsSyncManager: NSObject, ObservableObject, WCSessionDelegate {
    static let shared = IOSSettingsSyncManager()
    
    // Connectivity Status
    @Published var isSupported: Bool = false
    @Published var isWatchAppInstalled: Bool = false
    @Published var isReachable: Bool = false
    @Published var lastSyncTime: Date? = nil
    
    // Remote Settings State (Persisted on iPhone)
    @Published var selectedMode: String = "bubbles" {
        didSet { saveAndBroadcast() }
    }
    @Published var timerMinutes: Int = 0 {
        didSet { saveAndBroadcast() }
    }
    @Published var soundEnabled: Bool = true {
        didSet { saveAndBroadcast() }
    }
    @Published var voiceEnabled: Bool = true {
        didSet { saveAndBroadcast() }
    }
    @Published var hapticsEnabled: Bool = true {
        didSet { saveAndBroadcast() }
    }
    @Published var lowStimulation: Bool = false {
        didSet { saveAndBroadcast() }
    }
    @Published var lockHoldDuration: Double = 3.0 {
        didSet { saveAndBroadcast() }
    }
    
    // Live Watch Telemetry
    @Published var watchCurrentMode: String = "bubbles"
    @Published var watchTouchCount: Int = 0
    @Published var watchRemainingSeconds: Int = 0
    @Published var watchIsTimerActive: Bool = false
    @Published var watchLastHeard: Date? = nil
    
    private var isBroadcasting = false
    
    private override init() {
        super.init()
        loadLocalSettings()
        activateSession()
    }
    
    private func loadLocalSettings() {
        let defaults = UserDefaults.standard
        if defaults.object(forKey: "selectedMode") != nil {
            selectedMode = defaults.string(forKey: "selectedMode") ?? "bubbles"
            timerMinutes = defaults.integer(forKey: "timerMinutes")
            soundEnabled = defaults.bool(forKey: "soundEnabled")
            voiceEnabled = defaults.bool(forKey: "voiceEnabled")
            hapticsEnabled = defaults.bool(forKey: "hapticsEnabled")
            lowStimulation = defaults.bool(forKey: "lowStimulation")
            lockHoldDuration = defaults.double(forKey: "lockHoldDuration")
            if lockHoldDuration == 0 { lockHoldDuration = 3.0 }
        }
    }
    
    private func saveLocalSettings() {
        let defaults = UserDefaults.standard
        defaults.set(selectedMode, forKey: "selectedMode")
        defaults.set(timerMinutes, forKey: "timerMinutes")
        defaults.set(soundEnabled, forKey: "soundEnabled")
        defaults.set(voiceEnabled, forKey: "voiceEnabled")
        defaults.set(hapticsEnabled, forKey: "hapticsEnabled")
        defaults.set(lowStimulation, forKey: "lowStimulation")
        defaults.set(lockHoldDuration, forKey: "lockHoldDuration")
    }
    
    func activateSession() {
        guard WCSession.isSupported() else {
            isSupported = false
            return
        }
        isSupported = true
        let session = WCSession.default
        session.delegate = self
        session.activate()
    }
    
    // MARK: - WCSessionDelegate (iOS)
    
    func session(_ session: WCSession, activationDidCompleteWith activationState: WCSessionActivationState, error: Error?) {
        DispatchQueue.main.async {
            self.isWatchAppInstalled = session.isWatchAppInstalled
            self.isReachable = session.isReachable
            if activationState == .activated {
                self.sendSettingsToWatch()
            }
        }
    }
    
    func sessionDidBecomeInactive(_ session: WCSession) {}
    
    func sessionDidDeactivate(_ session: WCSession) {
        // Re-activate if switching Apple Watches
        session.activate()
    }
    
    func sessionWatchStateDidChange(_ session: WCSession) {
        DispatchQueue.main.async {
            self.isWatchAppInstalled = session.isWatchAppInstalled
            self.isReachable = session.isReachable
        }
    }
    
    func sessionReachabilityDidChange(_ session: WCSession) {
        DispatchQueue.main.async {
            self.isReachable = session.isReachable
            if session.isReachable {
                self.sendSettingsToWatch()
            }
        }
    }
    
    func session(_ session: WCSession, didReceiveApplicationContext applicationContext: [String : Any]) {
        DispatchQueue.main.async {
            self.processWatchTelemetry(applicationContext)
        }
    }
    
    func session(_ session: WCSession, didReceiveMessage message: [String : Any]) {
        DispatchQueue.main.async {
            self.processWatchTelemetry(message)
        }
    }
    
    private func processWatchTelemetry(_ dict: [String: Any]) {
        if let mode = dict["currentMode"] as? String {
            self.watchCurrentMode = mode
        }
        if let touches = dict["touchesCount"] as? Int {
            self.watchTouchCount = touches
        }
        if let remaining = dict["remainingSeconds"] as? Int {
            self.watchRemainingSeconds = remaining
        }
        if let timerActive = dict["isTimerActive"] as? Bool {
            self.watchIsTimerActive = timerActive
        }
        self.watchLastHeard = Date()
    }
    
    // MARK: - Actions
    
    private func saveAndBroadcast() {
        saveLocalSettings()
        sendSettingsToWatch()
    }
    
    func sendSettingsToWatch(extraPayload: [String: Any]? = nil) {
        guard WCSession.isSupported() else { return }
        let session = WCSession.default
        guard session.activationState == .activated else { return }
        
        var payload: [String: Any] = [
            "currentMode": selectedMode,
            "timerMinutes": timerMinutes,
            "soundEnabled": soundEnabled,
            "voiceEnabled": voiceEnabled,
            "hapticsEnabled": hapticsEnabled,
            "lowStimulation": lowStimulation,
            "lockHoldDuration": lockHoldDuration,
            "timestamp": Date().timeIntervalSince1970
        ]
        
        if let extra = extraPayload {
            for (k, v) in extra {
                payload[k] = v
            }
        }
        
        // 1. Immediate message if watch app is currently open and reachable
        if session.isReachable {
            session.sendMessage(payload, replyHandler: nil, errorHandler: nil)
        }
        
        // 2. Guaranteed background context update for when watch app opens next
        do {
            try session.updateApplicationContext(payload)
            DispatchQueue.main.async {
                self.lastSyncTime = Date()
            }
        } catch {
            print("Failed to update application context: \(error)")
        }
    }
    
    func switchWatchMode(to mode: String) {
        selectedMode = mode
        sendSettingsToWatch(extraPayload: ["currentMode": mode])
    }
    
    func triggerLullabyNow() {
        selectedMode = "lullaby"
        sendSettingsToWatch(extraPayload: [
            "currentMode": "lullaby",
            "action": "triggerLullaby"
        ])
    }
    
    func setWatchTimer(minutes: Int) {
        timerMinutes = minutes
        sendSettingsToWatch(extraPayload: ["timerMinutes": minutes])
    }
    
    var formattedWatchRemainingTime: String {
        guard watchIsTimerActive else { return "Off" }
        let mins = watchRemainingSeconds / 60
        let secs = watchRemainingSeconds % 60
        return String(format: "%d:%02d", mins, secs)
    }
}
