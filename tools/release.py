#!/usr/bin/env python3
"""
TinyTouch Automated App Store Connect Release Tool

Usage examples:
  1. Dry run (verify build & archive without uploading):
     python3 tools/release.py --dry-run

  2. Upload using App Store Connect API Key:
     python3 tools/release.py --api-key KEY_ID --api-issuer ISSUER_ID --p8-path /path/to/AuthKey.p8 --team-id YOUR_TEAM_ID

  3. Upload using Apple ID & App-Specific Password:
     python3 tools/release.py --username your_apple_id@example.com --password abcd-efgh-ijkl-mnop --team-id YOUR_TEAM_ID
"""

import argparse
import os
import subprocess
import sys
import glob

def run_command(cmd, desc=None, check=True):
    if desc:
        print(f"\n==> {desc}")
    print(f"$ {' '.join(cmd)}")
    result = subprocess.run(cmd)
    if check and result.returncode != 0:
        print(f"\n[ERROR] Command failed with exit code {result.returncode}")
        sys.exit(result.returncode)
    return result

def bump_build_number():
    print("\n==> Checking and incrementing build number...")
    proj_file = "tools/generate_project.py"
    with open(proj_file, "r") as f:
        content = f.read()
    
    # Extract current version
    import re
    match = re.search(r'CURRENT_PROJECT_VERSION = (\d+);', content)
    curr_build = int(match.group(1)) if match else 1
    new_build = curr_build + 1
    
    content = re.sub(r'CURRENT_PROJECT_VERSION = \d+;', f'CURRENT_PROJECT_VERSION = {new_build};', content)
    content = re.sub(r'INFOPLIST_KEY_CFBundleVersion = \d+;', f'INFOPLIST_KEY_CFBundleVersion = {new_build};', content)
    
    with open(proj_file, "w") as f:
        f.write(content)
        
    subprocess.run(["python3", "tools/generate_project.py"], check=True)
    print(f"Build number bumped from {curr_build} to {new_build}")

def main():
    parser = argparse.ArgumentParser(description="Automate App Store Connect archive, validation, and upload for TinyTouch")
    parser.add_argument("--dry-run", action="store_true", help="Build and archive without uploading")
    parser.add_argument("--validate-only", action="store_true", help="Validate with App Store Connect without submitting")
    parser.add_argument("--bump", action="store_true", help="Increment build number before archiving")
    parser.add_argument("--team-id", type=str, default="", help="Apple Developer Team ID (10 characters, e.g. ABCDE12345)")
    parser.add_argument("--api-key", type=str, help="App Store Connect API Key ID")
    parser.add_argument("--api-issuer", type=str, help="App Store Connect API Issuer ID")
    parser.add_argument("--p8-path", type=str, help="Path to AuthKey_<key_id>.p8 file")
    parser.add_argument("--username", type=str, help="Apple ID Email")
    parser.add_argument("--password", type=str, help="App-Specific Password")
    
    args = parser.parse_args()
    
    workspace_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(workspace_root)
    
    if args.bump:
        bump_build_number()
        
    archive_path = os.path.join(workspace_root, "build", "ToddlerPlay.xcarchive")
    export_path = os.path.join(workspace_root, "build", "AppStoreExport")
    os.makedirs(os.path.join(workspace_root, "build"), exist_ok=True)
    
    # 1. Archive
    archive_cmd = [
        "xcodebuild",
        "archive",
        "-scheme", "ToddlerPlay",
        "-destination", "generic/platform=watchOS",
        "-archivePath", archive_path
    ]
    
    if args.team_id:
        archive_cmd.append(f"DEVELOPMENT_TEAM={args.team_id}")
        archive_cmd.append("CODE_SIGN_STYLE=Automatic")
    elif args.dry_run:
        # For dry-run without signing certificates, disable code signing verification
        archive_cmd.append("CODE_SIGNING_ALLOWED=NO")
        
    run_command(archive_cmd, "Creating watchOS Archive (.xcarchive)")
    print(f"✓ Archive created at: {archive_path}")
    
    if args.dry_run:
        print("\n=======================================================")
        print("🎉 DRY RUN SUCCESSFUL!")
        print(f"Archive verified at: {archive_path}")
        print("To upload to App Store Connect, run with your credentials:")
        print("  python3 tools/release.py --api-key <KEY_ID> --api-issuer <ISSUER_ID> --team-id <TEAM_ID>")
        print("  OR:")
        print("  python3 tools/release.py --username <EMAIL> --password <APP_SPECIFIC_PWD> --team-id <TEAM_ID>")
        print("=======================================================")
        return

    # 2. Export Archive
    export_cmd = [
        "xcodebuild",
        "-exportArchive",
        "-archivePath", archive_path,
        "-exportPath", export_path,
        "-exportOptionsPlist", "ExportOptions.plist",
        "-allowProvisioningUpdates"
    ]
    run_command(export_cmd, "Exporting Package for App Store Connect Distribution")
    
    # Locate package (.ipa or .pkg)
    packages = glob.glob(os.path.join(export_path, "*.ipa")) + glob.glob(os.path.join(export_path, "*.pkg"))
    if not packages:
        print("[ERROR] No exported .ipa or .pkg found in " + export_path)
        sys.exit(1)
        
    pkg_file = packages[0]
    print(f"✓ App Store package ready: {pkg_file}")
    
    # 3. Authentication flags
    auth_flags = []
    if args.api_key and args.api_issuer:
        auth_flags.extend(["--api-key", args.api_key, "--api-issuer", args.api_issuer])
        if args.p8_path:
            auth_flags.extend(["--p8-file-path", args.p8_path])
    elif args.username and args.password:
        auth_flags.extend(["--username", args.username, "--password", args.password])
    else:
        print("\n[ERROR] Missing authentication. Provide either:")
        print("  --api-key and --api-issuer (recommended)")
        print("  OR --username and --password (app-specific password)")
        sys.exit(1)
        
    # 4. Validate with App Store Connect
    val_cmd = ["xcrun", "altool", "--validate-app", "-f", pkg_file] + auth_flags
    run_command(val_cmd, "Validating package with App Store Connect...")
    print("✓ Package validation passed with App Store Connect!")
    
    if args.validate_only:
        print("Validation complete. Skipping upload as requested.")
        return
        
    # 5. Upload to App Store Connect
    upload_cmd = ["xcrun", "altool", "--upload-app", "-f", pkg_file] + auth_flags
    run_command(upload_cmd, "Uploading package to App Store Connect...")
    
    print("\n=======================================================")
    print("🚀 SUCCESS! TinyTouch uploaded to App Store Connect.")
    print("Visit https://appstoreconnect.apple.com to select this build and submit for review!")
    print("=======================================================")

if __name__ == "__main__":
    main()
