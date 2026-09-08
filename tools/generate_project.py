#!/usr/bin/env python3
import os
import sys

def generate_project(source_files, resource_files):
    os.makedirs("ToddlerPlay.xcodeproj/xcshareddata/xcschemes", exist_ok=True)
    
    # Static IDs for predictable diffing
    proj_id = "000100010001000100010001"
    target_id = "000200020002000200020002"
    main_group_id = "000300030003000300030003"
    sources_group_id = "000400040004000400040004"
    resources_group_id = "000500050005000500050005"
    products_group_id = "000600060006000600060006"
    app_product_id = "000700070007000700070007"
    
    sources_build_phase_id = "000800080008000800080008"
    resources_build_phase_id = "000900090009000900090009"
    frameworks_build_phase_id = "000A000A000A000A000A000A"
    
    proj_cfg_list_id = "000B000B000B000B000B000B"
    proj_debug_cfg_id = "000C000C000C000C000C000C"
    proj_release_cfg_id = "000D000D000D000D000D000D"
    
    target_cfg_list_id = "000E000E000E000E000E000E"
    target_debug_cfg_id = "000F000F000F000F000F000F"
    target_release_cfg_id = "001000100010001000100010"
    
    file_entries = [] # (file_ref_id, build_file_id, filename, filepath, is_source, is_resource)
    
    id_counter = 0x100
    def next_id():
        nonlocal id_counter
        id_counter += 1
        return f"{id_counter:024X}"
    
    for f in source_files:
        f_ref = next_id()
        b_ref = next_id()
        file_entries.append((f_ref, b_ref, os.path.basename(f), f, True, False))
        
    for f in resource_files:
        f_ref = next_id()
        b_ref = next_id()
        file_entries.append((f_ref, b_ref, os.path.basename(f), f, False, True))
        
    pbx = []
    pbx.append("// !$*UTF8*$!")
    pbx.append("{")
    pbx.append("\tarchiveVersion = 1;")
    pbx.append("\tclasses = {")
    pbx.append("\t};")
    pbx.append("\tobjectVersion = 56;")
    pbx.append("\tobjects = {")
    
    # PBXBuildFile
    pbx.append("/* Begin PBXBuildFile section */")
    for f_ref, b_ref, fname, fpath, is_src, is_res in file_entries:
        if is_src:
            pbx.append(f"\t\t{b_ref} /* {fname} in Sources */ = {{isa = PBXBuildFile; fileRef = {f_ref} /* {fname} */; }};")
        elif is_res:
            pbx.append(f"\t\t{b_ref} /* {fname} in Resources */ = {{isa = PBXBuildFile; fileRef = {f_ref} /* {fname} */; }};")
    pbx.append("/* End PBXBuildFile section */")
    pbx.append("")
    
    # PBXFileReference
    pbx.append("/* Begin PBXFileReference section */")
    pbx.append(f"\t\t{app_product_id} /* ToddlerPlay.app */ = {{isa = PBXFileReference; explicitFileType = wrapper.application; includeInIndex = 0; path = ToddlerPlay.app; sourceTree = BUILT_PRODUCTS_DIR; }};")
    for f_ref, b_ref, fname, fpath, is_src, is_res in file_entries:
        if fname.endswith(".swift"):
            ft = "sourcecode.swift"
        elif fname.endswith(".xcassets"):
            ft = "folder.assetcatalog"
        elif fname.endswith(".wav"):
            ft = "audio.wav"
        elif fname.endswith(".xcprivacy"):
            ft = "text.xml"
        else:
            ft = "text"
        pbx.append(f"\t\t{f_ref} /* {fname} */ = {{isa = PBXFileReference; lastKnownFileType = {ft}; path = \"{fpath}\"; sourceTree = \"<group>\"; }};")
    pbx.append("/* End PBXFileReference section */")
    pbx.append("")
    
    # PBXFrameworksBuildPhase
    pbx.append("/* Begin PBXFrameworksBuildPhase section */")
    pbx.append(f"\t\t{frameworks_build_phase_id} /* Frameworks */ = {{")
    pbx.append("\t\t\tisa = PBXFrameworksBuildPhase;")
    pbx.append("\t\t\tbuildActionMask = 2147483647;")
    pbx.append("\t\t\tfiles = (")
    pbx.append("\t\t\t);")
    pbx.append("\t\t\trunOnlyForDeploymentPostprocessing = 0;")
    pbx.append("\t\t};")
    pbx.append("/* End PBXFrameworksBuildPhase section */")
    pbx.append("")
    
    # PBXGroup
    pbx.append("/* Begin PBXGroup section */")
    pbx.append(f"\t\t{main_group_id} = {{")
    pbx.append("\t\t\tisa = PBXGroup;")
    pbx.append("\t\t\tchildren = (")
    pbx.append(f"\t\t\t\t{sources_group_id} /* Sources */,")
    pbx.append(f"\t\t\t\t{resources_group_id} /* Resources */,")
    pbx.append(f"\t\t\t\t{products_group_id} /* Products */,")
    pbx.append("\t\t\t);")
    pbx.append("\t\t\tsourceTree = \"<group>\";")
    pbx.append("\t\t};")
    
    pbx.append(f"\t\t{sources_group_id} /* Sources */ = {{")
    pbx.append("\t\t\tisa = PBXGroup;")
    pbx.append("\t\t\tchildren = (")
    for f_ref, b_ref, fname, fpath, is_src, is_res in file_entries:
        if is_src:
            pbx.append(f"\t\t\t\t{f_ref} /* {fname} */,")
    pbx.append("\t\t\t);")
    pbx.append("\t\t\tname = Sources;")
    pbx.append("\t\t\tsourceTree = \"<group>\";")
    pbx.append("\t\t};")
    
    pbx.append(f"\t\t{resources_group_id} /* Resources */ = {{")
    pbx.append("\t\t\tisa = PBXGroup;")
    pbx.append("\t\t\tchildren = (")
    for f_ref, b_ref, fname, fpath, is_src, is_res in file_entries:
        if is_res:
            pbx.append(f"\t\t\t\t{f_ref} /* {fname} */,")
    pbx.append("\t\t\t);")
    pbx.append("\t\t\tname = Resources;")
    pbx.append("\t\t\tsourceTree = \"<group>\";")
    pbx.append("\t\t};")
    
    pbx.append(f"\t\t{products_group_id} /* Products */ = {{")
    pbx.append("\t\t\tisa = PBXGroup;")
    pbx.append("\t\t\tchildren = (")
    pbx.append(f"\t\t\t\t{app_product_id} /* ToddlerPlay.app */,")
    pbx.append("\t\t\t);")
    pbx.append("\t\t\tname = Products;")
    pbx.append("\t\t\tsourceTree = \"<group>\";")
    pbx.append("\t\t};")
    pbx.append("/* End PBXGroup section */")
    pbx.append("")
    
    # PBXNativeTarget
    pbx.append("/* Begin PBXNativeTarget section */")
    pbx.append(f"\t\t{target_id} /* ToddlerPlay */ = {{")
    pbx.append("\t\t\tisa = PBXNativeTarget;")
    pbx.append(f"\t\t\tbuildConfigurationList = {target_cfg_list_id} /* Build configuration list for PBXNativeTarget \"ToddlerPlay\" */;")
    pbx.append("\t\t\tbuildPhases = (")
    pbx.append(f"\t\t\t\t{sources_build_phase_id} /* Sources */,")
    pbx.append(f"\t\t\t\t{frameworks_build_phase_id} /* Frameworks */,")
    pbx.append(f"\t\t\t\t{resources_build_phase_id} /* Resources */,")
    pbx.append("\t\t\t);")
    pbx.append("\t\t\tbuildRules = (")
    pbx.append("\t\t\t);")
    pbx.append("\t\t\tdependencies = (")
    pbx.append("\t\t\t);")
    pbx.append("\t\t\tname = ToddlerPlay;")
    pbx.append("\t\t\tproductName = ToddlerPlay;")
    pbx.append(f"\t\t\tproductReference = {app_product_id} /* ToddlerPlay.app */;")
    pbx.append("\t\t\tproductType = \"com.apple.product-type.application\";")
    pbx.append("\t\t};")
    pbx.append("/* End PBXNativeTarget section */")
    pbx.append("")
    
    # PBXProject
    pbx.append("/* Begin PBXProject section */")
    pbx.append(f"\t\t{proj_id} /* Project object */ = {{")
    pbx.append("\t\t\tisa = PBXProject;")
    pbx.append("\t\t\tattributes = {")
    pbx.append("\t\t\t\tBuildIndependentTargetsInParallel = 1;")
    pbx.append("\t\t\t\tLastUpgradeCheck = 1500;")
    pbx.append("\t\t\t\tTargetAttributes = {")
    pbx.append(f"\t\t\t\t\t{target_id} = {{")
    pbx.append("\t\t\t\t\t\tCreatedOnToolsVersion = 15.0;")
    pbx.append("\t\t\t\t\t};")
    pbx.append("\t\t\t\t};")
    pbx.append("\t\t\t};")
    pbx.append(f"\t\t\tbuildConfigurationList = {proj_cfg_list_id} /* Build configuration list for PBXProject \"ToddlerPlay\" */;")
    pbx.append("\t\t\tcompatibilityVersion = \"Xcode 14.0\";")
    pbx.append("\t\t\tdevelopmentRegion = en;")
    pbx.append("\t\t\thasScannedForEncodings = 0;")
    pbx.append("\t\t\tknownRegions = (")
    pbx.append("\t\t\t\ten,")
    pbx.append("\t\t\t\tBase,")
    pbx.append("\t\t\t);")
    pbx.append(f"\t\t\tmainGroup = {main_group_id};")
    pbx.append(f"\t\t\tproductRefGroup = {products_group_id} /* Products */;")
    pbx.append("\t\t\tprojectDirPath = \"\";")
    pbx.append("\t\t\tprojectRoot = \"\";")
    pbx.append("\t\t\ttargets = (")
    pbx.append(f"\t\t\t\t{target_id} /* ToddlerPlay */,")
    pbx.append("\t\t\t);")
    pbx.append("\t\t};")
    pbx.append("/* End PBXProject section */")
    pbx.append("")
    
    # PBXResourcesBuildPhase
    pbx.append("/* Begin PBXResourcesBuildPhase section */")
    pbx.append(f"\t\t{resources_build_phase_id} /* Resources */ = {{")
    pbx.append("\t\t\tisa = PBXResourcesBuildPhase;")
    pbx.append("\t\t\tbuildActionMask = 2147483647;")
    pbx.append("\t\t\tfiles = (")
    for f_ref, b_ref, fname, fpath, is_src, is_res in file_entries:
        if is_res:
            pbx.append(f"\t\t\t\t{b_ref} /* {fname} in Resources */,")
    pbx.append("\t\t\t);")
    pbx.append("\t\t\trunOnlyForDeploymentPostprocessing = 0;")
    pbx.append("\t\t};")
    pbx.append("/* End PBXResourcesBuildPhase section */")
    pbx.append("")
    
    # PBXSourcesBuildPhase
    pbx.append("/* Begin PBXSourcesBuildPhase section */")
    pbx.append(f"\t\t{sources_build_phase_id} /* Sources */ = {{")
    pbx.append("\t\t\tisa = PBXSourcesBuildPhase;")
    pbx.append("\t\t\tbuildActionMask = 2147483647;")
    pbx.append("\t\t\tfiles = (")
    for f_ref, b_ref, fname, fpath, is_src, is_res in file_entries:
        if is_src:
            pbx.append(f"\t\t\t\t{b_ref} /* {fname} in Sources */,")
    pbx.append("\t\t\t);")
    pbx.append("\t\t\trunOnlyForDeploymentPostprocessing = 0;")
    pbx.append("\t\t};")
    pbx.append("/* End PBXSourcesBuildPhase section */")
    pbx.append("")
    
    # XCBuildConfiguration
    pbx.append("/* Begin XCBuildConfiguration section */")
    # Project Debug
    pbx.append(f"\t\t{proj_debug_cfg_id} /* Debug */ = {{")
    pbx.append("\t\t\tisa = XCBuildConfiguration;")
    pbx.append("\t\t\tbuildSettings = {")
    pbx.append("\t\t\t\tALWAYS_SEARCH_USER_PATHS = NO;")
    pbx.append("\t\t\t\tCLANG_ANALYZER_NONNULL = YES;")
    pbx.append("\t\t\t\tCLANG_CXX_LANGUAGE_STANDARD = \"gnu++20\";")
    pbx.append("\t\t\t\tCLANG_ENABLE_MODULES = YES;")
    pbx.append("\t\t\t\tCLANG_ENABLE_OBJC_ARC = YES;")
    pbx.append("\t\t\t\tCOPY_PHASE_STRIP = NO;")
    pbx.append("\t\t\t\tDEBUG_INFORMATION_FORMAT = dwarf;")
    pbx.append("\t\t\t\tENABLE_STRICT_OBJC_MSGSEND = YES;")
    pbx.append("\t\t\t\tENABLE_TESTABILITY = YES;")
    pbx.append("\t\t\t\tGCC_OPTIMIZATION_LEVEL = 0;")
    pbx.append("\t\t\t\tGCC_PREPROCESSOR_DEFINITIONS = (")
    pbx.append("\t\t\t\t\t\"DEBUG=1\",")
    pbx.append("\t\t\t\t\t\"$(inherited)\",")
    pbx.append("\t\t\t\t);")
    pbx.append("\t\t\t\tMTL_ENABLE_DEBUG_INFO = INCLUDE_SOURCE;")
    pbx.append("\t\t\t\tMTL_FAST_MATH = YES;")
    pbx.append("\t\t\t\tONLY_ACTIVE_ARCH = YES;")
    pbx.append("\t\t\t\tSDKROOT = watchos;")
    pbx.append("\t\t\t\tWATCHOS_DEPLOYMENT_TARGET = 10.0;")
    pbx.append("\t\t\t};")
    pbx.append("\t\t\tname = Debug;")
    pbx.append("\t\t};")
    
    # Project Release
    pbx.append(f"\t\t{proj_release_cfg_id} /* Release */ = {{")
    pbx.append("\t\t\tisa = XCBuildConfiguration;")
    pbx.append("\t\t\tbuildSettings = {")
    pbx.append("\t\t\t\tALWAYS_SEARCH_USER_PATHS = NO;")
    pbx.append("\t\t\t\tCLANG_ANALYZER_NONNULL = YES;")
    pbx.append("\t\t\t\tCLANG_CXX_LANGUAGE_STANDARD = \"gnu++20\";")
    pbx.append("\t\t\t\tCLANG_ENABLE_MODULES = YES;")
    pbx.append("\t\t\t\tCLANG_ENABLE_OBJC_ARC = YES;")
    pbx.append("\t\t\t\tCOPY_PHASE_STRIP = NO;")
    pbx.append("\t\t\t\tDEBUG_INFORMATION_FORMAT = \"dwarf-with-dsym\";")
    pbx.append("\t\t\t\tENABLE_NS_ASSERTIONS = NO;")
    pbx.append("\t\t\t\tENABLE_STRICT_OBJC_MSGSEND = YES;")
    pbx.append("\t\t\t\tGCC_OPTIMIZATION_LEVEL = s;")
    pbx.append("\t\t\t\tMTL_ENABLE_DEBUG_INFO = NO;")
    pbx.append("\t\t\t\tMTL_FAST_MATH = YES;")
    pbx.append("\t\t\t\tSDKROOT = watchos;")
    pbx.append("\t\t\t\tWATCHOS_DEPLOYMENT_TARGET = 10.0;")
    pbx.append("\t\t\t};")
    pbx.append("\t\t\tname = Release;")
    pbx.append("\t\t};")
    
    # Target Debug
    pbx.append(f"\t\t{target_debug_cfg_id} /* Debug */ = {{")
    pbx.append("\t\t\tisa = XCBuildConfiguration;")
    pbx.append("\t\t\tbuildSettings = {")
    pbx.append("\t\t\t\tASSETCATALOG_COMPILER_APPICON_NAME = AppIcon;")
    pbx.append("\t\t\t\tASSETCATALOG_COMPILER_GLOBAL_ACCENT_COLOR_NAME = AccentColor;")
    pbx.append("\t\t\t\tCODE_SIGN_STYLE = Automatic;")
    pbx.append("\t\t\t\tCODE_SIGN_IDENTITY = \"-\";")
    pbx.append("\t\t\t\tDEVELOPMENT_TEAM = \"\";")
    pbx.append("\t\t\t\tENABLE_PREVIEWS = YES;")
    pbx.append("\t\t\t\tGENERATE_INFOPLIST_FILE = YES;")
    pbx.append("\t\t\t\tINFOPLIST_KEY_CFBundleDisplayName = \"TinyTouch\";")
    pbx.append("\t\t\t\tINFOPLIST_KEY_UISupportedInterfaceOrientations = \"UIInterfaceOrientationPortrait UIInterfaceOrientationPortraitUpsideDown\";")
    pbx.append("\t\t\t\tINFOPLIST_KEY_WKApplication = YES;")
    pbx.append("\t\t\t\tINFOPLIST_KEY_WKWatchOnly = YES;")
    pbx.append("\t\t\t\tINFOPLIST_KEY_WKBackgroundModes = \"self-care\";")
    pbx.append("\t\t\t\tMARKETING_VERSION = 1.0.0;")
    pbx.append("\t\t\t\tCURRENT_PROJECT_VERSION = 1;")
    pbx.append("\t\t\t\tINFOPLIST_KEY_CFBundleShortVersionString = 1.0.0;")
    pbx.append("\t\t\t\tINFOPLIST_KEY_CFBundleVersion = 1;")
    pbx.append("\t\t\t\tLD_RUNPATH_SEARCH_PATHS = (")
    pbx.append("\t\t\t\t\t\"$(inherited)\",")
    pbx.append("\t\t\t\t\t\"@executable_path/Frameworks\",")
    pbx.append("\t\t\t\t);")
    pbx.append("\t\t\t\tPRODUCT_BUNDLE_IDENTIFIER = com.tianhaoz.tinytouch;")
    pbx.append("\t\t\t\tPRODUCT_NAME = \"$(TARGET_NAME)\";")
    pbx.append("\t\t\t\tSDKROOT = watchos;")
    pbx.append("\t\t\t\tSKIP_INSTALL = NO;")
    pbx.append("\t\t\t\tSWIFT_ACTIVE_COMPILATION_CONDITIONS = \"DEBUG $(inherited)\";")
    pbx.append("\t\t\t\tSWIFT_OPTIMIZATION_LEVEL = \"-Onone\";")
    pbx.append("\t\t\t\tSWIFT_VERSION = 5.0;")
    pbx.append("\t\t\t\tTARGETED_DEVICE_FAMILY = 4;")
    pbx.append("\t\t\t\tWATCHOS_DEPLOYMENT_TARGET = 10.0;")
    pbx.append("\t\t\t};")
    pbx.append("\t\t\tname = Debug;")
    pbx.append("\t\t};")
    
    # Target Release
    pbx.append(f"\t\t{target_release_cfg_id} /* Release */ = {{")
    pbx.append("\t\t\tisa = XCBuildConfiguration;")
    pbx.append("\t\t\tbuildSettings = {")
    pbx.append("\t\t\t\tASSETCATALOG_COMPILER_APPICON_NAME = AppIcon;")
    pbx.append("\t\t\t\tASSETCATALOG_COMPILER_GLOBAL_ACCENT_COLOR_NAME = AccentColor;")
    pbx.append("\t\t\t\tCODE_SIGN_STYLE = Automatic;")
    pbx.append("\t\t\t\tCODE_SIGN_IDENTITY = \"-\";")
    pbx.append("\t\t\t\tDEVELOPMENT_TEAM = \"\";")
    pbx.append("\t\t\t\tENABLE_PREVIEWS = YES;")
    pbx.append("\t\t\t\tGENERATE_INFOPLIST_FILE = YES;")
    pbx.append("\t\t\t\tINFOPLIST_KEY_CFBundleDisplayName = \"TinyTouch\";")
    pbx.append("\t\t\t\tINFOPLIST_KEY_UISupportedInterfaceOrientations = \"UIInterfaceOrientationPortrait UIInterfaceOrientationPortraitUpsideDown\";")
    pbx.append("\t\t\t\tINFOPLIST_KEY_WKApplication = YES;")
    pbx.append("\t\t\t\tINFOPLIST_KEY_WKWatchOnly = YES;")
    pbx.append("\t\t\t\tINFOPLIST_KEY_WKBackgroundModes = \"self-care\";")
    pbx.append("\t\t\t\tMARKETING_VERSION = 1.0.0;")
    pbx.append("\t\t\t\tCURRENT_PROJECT_VERSION = 1;")
    pbx.append("\t\t\t\tINFOPLIST_KEY_CFBundleShortVersionString = 1.0.0;")
    pbx.append("\t\t\t\tINFOPLIST_KEY_CFBundleVersion = 1;")
    pbx.append("\t\t\t\tLD_RUNPATH_SEARCH_PATHS = (")
    pbx.append("\t\t\t\t\t\"$(inherited)\",")
    pbx.append("\t\t\t\t\t\"@executable_path/Frameworks\",")
    pbx.append("\t\t\t\t);")
    pbx.append("\t\t\t\tPRODUCT_BUNDLE_IDENTIFIER = com.tianhaoz.tinytouch;")
    pbx.append("\t\t\t\tPRODUCT_NAME = \"$(TARGET_NAME)\";")
    pbx.append("\t\t\t\tSDKROOT = watchos;")
    pbx.append("\t\t\t\tSKIP_INSTALL = NO;")
    pbx.append("\t\t\t\tSWIFT_OPTIMIZATION_LEVEL = \"-O\";")
    pbx.append("\t\t\t\tSWIFT_VERSION = 5.0;")
    pbx.append("\t\t\t\tTARGETED_DEVICE_FAMILY = 4;")
    pbx.append("\t\t\t\tWATCHOS_DEPLOYMENT_TARGET = 10.0;")
    pbx.append("\t\t\t};")
    pbx.append("\t\t\tname = Release;")
    pbx.append("\t\t};")
    pbx.append("/* End XCBuildConfiguration section */")
    pbx.append("")
    
    # XCConfigurationList
    pbx.append("/* Begin XCConfigurationList section */")
    pbx.append(f"\t\t{proj_cfg_list_id} /* Build configuration list for PBXProject \"ToddlerPlay\" */ = {{")
    pbx.append("\t\t\tisa = XCConfigurationList;")
    pbx.append("\t\t\tbuildConfigurations = (")
    pbx.append(f"\t\t\t\t{proj_debug_cfg_id} /* Debug */,")
    pbx.append(f"\t\t\t\t{proj_release_cfg_id} /* Release */,")
    pbx.append("\t\t\t);")
    pbx.append("\t\t\tdefaultConfigurationIsVisible = 0;")
    pbx.append("\t\t\tdefaultConfigurationName = Release;")
    pbx.append("\t\t};")
    
    pbx.append(f"\t\t{target_cfg_list_id} /* Build configuration list for PBXNativeTarget \"ToddlerPlay\" */ = {{")
    pbx.append("\t\t\tisa = XCConfigurationList;")
    pbx.append("\t\t\tbuildConfigurations = (")
    pbx.append(f"\t\t\t\t{target_debug_cfg_id} /* Debug */,")
    pbx.append(f"\t\t\t\t{target_release_cfg_id} /* Release */,")
    pbx.append("\t\t\t);")
    pbx.append("\t\t\tdefaultConfigurationIsVisible = 0;")
    pbx.append("\t\t\tdefaultConfigurationName = Release;")
    pbx.append("\t\t};")
    pbx.append("/* End XCConfigurationList section */")
    pbx.append("")
    
    pbx.append("\t};")
    pbx.append(f"\trootObject = {proj_id} /* Project object */;")
    pbx.append("}")
    
    with open("ToddlerPlay.xcodeproj/project.pbxproj", "w") as f:
        f.write("\n".join(pbx) + "\n")
    print("Generated ToddlerPlay.xcodeproj/project.pbxproj")
    
    # Also write scheme
    scheme = f"""<?xml version="1.0" encoding="UTF-8"?>
<Scheme
   LastUpgradeVersion = "1500"
   version = "1.7">
   <BuildAction
      parallelizeBuildables = "YES"
      buildImplicitDependencies = "YES">
      <BuildActionEntries>
         <BuildActionEntry
            buildForTesting = "YES"
            buildForRunning = "YES"
            buildForProfiling = "YES"
            buildForArchiving = "YES"
            buildForAnalyzing = "YES">
            <BuildableReference
               BuildableIdentifier = "primary"
               BlueprintIdentifier = "{target_id}"
               BuildableName = "ToddlerPlay.app"
               BlueprintName = "ToddlerPlay"
               ReferencedContainer = "container:ToddlerPlay.xcodeproj">
            </BuildableReference>
         </BuildActionEntry>
      </BuildActionEntries>
   </BuildAction>
   <TestAction
      buildConfiguration = "Debug"
      selectedDebuggerIdentifier = "Xcode.DebuggerFoundation.Debugger.LLDB"
      selectedLauncherIdentifier = "Xcode.DebuggerFoundation.Launcher.LLDB"
      shouldUseLaunchSchemeArgsEnv = "YES">
      <Testables>
      </Testables>
   </TestAction>
   <LaunchAction
      buildConfiguration = "Debug"
      selectedDebuggerIdentifier = "Xcode.DebuggerFoundation.Debugger.LLDB"
      selectedLauncherIdentifier = "Xcode.DebuggerFoundation.Launcher.LLDB"
      launchStyle = "0"
      useCustomWorkingDirectory = "NO"
      ignoresPersistentStateOnLaunch = "NO"
      debugDocumentVersioning = "YES"
      debugServiceExtension = "internal"
      allowLocationSimulation = "YES">
      <BuildableProductRunnable
         runnableDebuggingMode = "0">
         <BuildableReference
            BuildableIdentifier = "primary"
            BlueprintIdentifier = "{target_id}"
            BuildableName = "ToddlerPlay.app"
            BlueprintName = "ToddlerPlay"
            ReferencedContainer = "container:ToddlerPlay.xcodeproj">
         </BuildableReference>
      </BuildableProductRunnable>
   </LaunchAction>
   <ProfileAction
      buildConfiguration = "Release"
      shouldUseLaunchSchemeArgsEnv = "YES"
      savedToolIdentifier = ""
      useCustomWorkingDirectory = "NO"
      debugDocumentVersioning = "YES">
      <BuildableProductRunnable
         runnableDebuggingMode = "0">
         <BuildableReference
            BuildableIdentifier = "primary"
            BlueprintIdentifier = "{target_id}"
            BuildableName = "ToddlerPlay.app"
            BlueprintName = "ToddlerPlay"
            ReferencedContainer = "container:ToddlerPlay.xcodeproj">
         </BuildableReference>
      </BuildableProductRunnable>
   </ProfileAction>
   <AnalyzeAction
      buildConfiguration = "Debug">
   </AnalyzeAction>
   <ArchiveAction
      buildConfiguration = "Release"
      revealArchiveInOrganizer = "YES">
   </ArchiveAction>
</Scheme>
"""
    with open("ToddlerPlay.xcodeproj/xcshareddata/xcschemes/ToddlerPlay.xcscheme", "w") as f:
        f.write(scheme)
    print("Generated scheme ToddlerPlay.xcscheme")

if __name__ == "__main__":
    sources = []
    for root, _, files in os.walk("ToddlerPlay/Sources"):
        for file in files:
            if file.endswith(".swift"):
                sources.append(os.path.join(root, file))
    
    resources = []
    if os.path.exists("ToddlerPlay/Resources/Assets.xcassets"):
        resources.append("ToddlerPlay/Resources/Assets.xcassets")
    if os.path.exists("ToddlerPlay/Resources/PrivacyInfo.xcprivacy"):
        resources.append("ToddlerPlay/Resources/PrivacyInfo.xcprivacy")
    for root, _, files in os.walk("ToddlerPlay/Resources/Sounds"):
        for file in files:
            if file.endswith(".wav"):
                resources.append(os.path.join(root, file))
                
    generate_project(sorted(sources), sorted(resources))
