# Fastlane for TinyTouch 🚀

Fastlane automates the testing, building, metadata synchronization, and TestFlight deployment of the TinyTouch iOS & watchOS app suite.

---

## Available Lanes

### 1. `fastlane test`
Runs the complete 71+ test suite (Game modes, WatchConnectivity remote sync, audio assets, parent shield, WidgetKit complication).
```bash
bundle exec fastlane test
```

### 2. `fastlane build`
Builds and archives the universal iOS + watchOS + WidgetKit application locally without uploading (great for dry runs).
```bash
bundle exec fastlane build
```

### 3. `fastlane beta`
Builds and uploads directly to TestFlight via `pilot` using the App Store Connect API Key.
```bash
# Auto-bump build number and release to TestFlight
bundle exec fastlane beta bump:true

# Or set an explicit build number:
bundle exec fastlane beta build_number:4
```

### 4. `fastlane upload_metadata`
Uploads all App Store listing descriptions, keywords, promotional texts, URLs, review notes, and screenshots to App Store Connect via `deliver`.
```bash
bundle exec fastlane upload_metadata
```

---

## Setup & Credentials

Fastlane uses an **App Store Connect API Key** (`.p8`), which avoids 2FA login prompts.

Create a file named `.env` in `fastlane/` (copied from `fastlane/.env.example`):
```bash
APP_STORE_CONNECT_KEY_ID="YOUR_KEY_ID"
APP_STORE_CONNECT_ISSUER_ID="YOUR_ISSUER_UUID"
APP_STORE_CONNECT_KEY_PATH="/Users/you/.appstoreconnect/private_keys/AuthKey_KEYID.p8"
```
