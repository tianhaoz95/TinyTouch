#!/usr/bin/env python3
"""
TinyTouch Automated TestFlight & App Store Connect Release Tool

Usage examples:
  1. Dry run (verify tests, build & archive without uploading):
     ./tools/release.sh --dry-run

  2. Automated TestFlight Upload (auto-increments build number and uploads):
     ./tools/release.sh --upload --bump

  3. Automated Upload with App Store Connect API Key:
     ./tools/release.sh --upload --bump --api-key KEY_ID --api-issuer ISSUER_ID --p8-path /path/to/AuthKey.p8
"""

import argparse
import os
import subprocess
import sys
import glob
import re

DEFAULT_TEAM_ID = "6522A974B3"

def run_command(cmd, desc=None, check=True):
    if desc:
        print(f"\n==> {desc}")
    print(f"$ {' '.join(cmd)}")
    result = subprocess.run(cmd)
    if check and result.returncode != 0:
        print(f"\n[ERROR] Command failed with exit code {result.returncode}")
        sys.exit(result.returncode)
    return result

def run_tests():
    print("\n==> Running Unit Tests Suite...")
    res = subprocess.run(["swift", "tools/run_tests.swift"])
    if res.returncode != 0:
        print("\n[ERROR] Unit tests failed! Fix tests before releasing.")
        sys.exit(res.returncode)
    print("✓ All unit tests passed cleanly.")

def bump_build_number():
    print("\n==> Checking and incrementing build number...")
    proj_file = "tools/generate_project.py"
    with open(proj_file, "r") as f:
        content = f.read()
    
    # Extract current version
    match = re.search(r'CURRENT_PROJECT_VERSION = (\d+);', content)
    curr_build = int(match.group(1)) if match else 1
    new_build = curr_build + 1
    
    content = re.sub(r'CURRENT_PROJECT_VERSION = \d+;', f'CURRENT_PROJECT_VERSION = {new_build};', content)
    content = re.sub(r'INFOPLIST_KEY_CFBundleVersion = \d+;', f'INFOPLIST_KEY_CFBundleVersion = {new_build};', content)
    
    with open(proj_file, "w") as f:
        f.write(content)
        
    subprocess.run(["python3", "tools/generate_project.py"], check=True)
    print(f"✓ Build number bumped from {curr_build} to {new_build}")
    return new_build

def main():
    parser = argparse.ArgumentParser(description="Automate App Store Connect & TestFlight release for TinyTouch")
    parser.add_argument("--dry-run", action="store_true", help="Build and archive without uploading")
    parser.add_argument("--upload", action="store_true", help="Automatically upload to TestFlight / App Store Connect")
    parser.add_argument("--validate-only", action="store_true", help="Validate with App Store Connect without submitting")
    parser.add_argument("--bump", action="store_true", help="Increment build number before archiving")
    parser.add_argument("--no-test", action="store_true", help="Skip running unit tests")
    parser.add_argument("--team-id", type=str, default=DEFAULT_TEAM_ID, help=f"Apple Developer Team ID (default: {DEFAULT_TEAM_ID})")
    parser.add_argument("--api-key", type=str, help="App Store Connect API Key ID")
    parser.add_argument("--api-issuer", type=str, help="App Store Connect API Issuer ID")
    parser.add_argument("--p8-path", type=str, help="Path to AuthKey_<key_id>.p8 file")
    parser.add_argument("--username", type=str, help="Apple ID Email")
    parser.add_argument("--password", type=str, help="App-Specific Password")
    
    args = parser.parse_args()
    
    workspace_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(workspace_root)
    
    # 1. Tests
    if not args.no_test:
        run_tests()
        
    # 2. Bump build number if requested
    if args.bump:
        bump_build_number()
        
    archive_path = os.path.join(workspace_root, "build", "TinyTouch.xcarchive")
    export_path = os.path.join(workspace_root, "build", "AppStoreExport")
    os.makedirs(os.path.join(workspace_root, "build"), exist_ok=True)
    
    # 3. Create Archive
    archive_cmd = [
        "xcodebuild",
        "archive",
        "-scheme", "TinyTouch",
        "-destination", "generic/platform=iOS",
        "-archivePath", archive_path
    ]
    
    if args.dry_run:
        archive_cmd.append("CODE_SIGNING_ALLOWED=NO")
    else:
        archive_cmd.extend([
            f"DEVELOPMENT_TEAM={args.team_id}",
            "CODE_SIGN_STYLE=Automatic",
            "-allowProvisioningUpdates"
        ])
        
    run_command(archive_cmd, "Creating Universal iOS + watchOS + Widget Archive (.xcarchive)")
    print(f"✓ Universal Archive created at: {archive_path}")
    
    if args.dry_run:
        print("\n=======================================================")
        print("🎉 DRY RUN SUCCESSFUL!")
        print(f"Universal Archive verified at: {archive_path}")
        print("To upload directly to TestFlight, run:")
        print("  ./tools/release.sh --upload")
        print("  OR with build bump:")
        print("  ./tools/release.sh --upload --bump")
        print("=======================================================")
        return

    # 4. Determine Upload / Export configuration
    api_key = args.api_key or os.environ.get("APP_STORE_CONNECT_API_KEY_ID")
    api_issuer = args.api_issuer or os.environ.get("APP_STORE_CONNECT_API_ISSUER_ID")
    p8_path = args.p8_path or os.environ.get("APP_STORE_CONNECT_KEY_PATH")
    
    if api_key and not p8_path:
        # Check standard search path
        candidate = os.path.expanduser(f"~/.appstoreconnect/private_keys/AuthKey_{api_key}.p8")
        if os.path.exists(candidate):
            p8_path = candidate
            
    plist_name = "ExportOptionsUpload.plist" if args.upload else "ExportOptions.plist"
    
    export_cmd = [
        "xcodebuild",
        "-exportArchive",
        "-archivePath", archive_path,
        "-exportPath", export_path,
        "-exportOptionsPlist", plist_name,
        "-allowProvisioningUpdates"
    ]
    
    if api_key and api_issuer and p8_path:
        export_cmd.extend([
            "-authenticationKeyPath", p8_path,
            "-authenticationKeyID", api_key,
            "-authenticationKeyIssuerID", api_issuer
        ])
        
    desc_label = "Exporting & Uploading directly to TestFlight / App Store Connect" if args.upload else "Exporting Package for Distribution"
    run_command(export_cmd, desc_label)
    
    if args.upload:
        print("\n=======================================================")
        print("🚀 SUCCESS! TinyTouch uploaded to TestFlight & App Store Connect!")
        print("Processing typically takes 5-15 minutes on Apple servers.")
        print("View build status & invite internal testers at:")
        print("  https://appstoreconnect.apple.com/apps")
        print("=======================================================")
    else:
        # Locate package (.ipa or .pkg)
        packages = glob.glob(os.path.join(export_path, "*.ipa")) + glob.glob(os.path.join(export_path, "*.pkg"))
        if packages:
            print(f"\n✓ App Store package exported to: {packages[0]}")
            print("To upload this build to TestFlight, run with --upload")

if __name__ == "__main__":
    main()
