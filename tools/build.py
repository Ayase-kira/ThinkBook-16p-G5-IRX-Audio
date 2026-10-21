#!/usr/bin/env python3
import argparse,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--sdk',required=True,type=Path);p.add_argument('--voodooi2c-headers',required=True,type=Path);p.add_argument('--applealc',required=True,type=Path);p.add_argument('--lilu',required=True,type=Path);a=p.parse_args();sdk=a.sdk.resolve();alc=a.applealc.resolve();lilu=a.lilu.resolve()
for path in [sdk/'Headers',sdk/'Library/x86_64',a.voodooi2c_headers,alc/'AppleALC/MachineIdentity.hpp',ROOT/'src/CirrusAudioFixup/CirrusAudioFixup/MachineIdentity.hpp',ROOT/'src/CirrusAudioFixup/CirrusAudioFixup/Devices/CS35L41/Resources/Firmware.hpp',lilu/'Contents/Resources/Headers/kern_api.hpp']:assert path.exists(),f'Missing {path}'
for link,target in [(alc/'MacKernelSDK',sdk),(alc/'Lilu.kext',lilu)]:
 if not link.exists():link.symlink_to(target,target_is_directory=True)
 else:assert link.resolve()==target,'Use a fresh AppleALC checkout and the requested dependencies'
subprocess.run(['xcodebuild','-project',str(ROOT/'src/CirrusAudioFixup/CirrusAudioFixup.xcodeproj'),'-scheme','CirrusAudioFixup','-configuration','Debug','-derivedDataPath',str(ROOT/'build/cirrus'),'build','CODE_SIGNING_ALLOWED=NO',f'KERNEL_EXTENSION_HEADER_SEARCH_PATHS={sdk}/Headers',f'KERNEL_FRAMEWORK_HEADERS={sdk}/Headers',f'LIBRARY_SEARCH_PATHS={sdk}/Library/x86_64',f'HEADER_SEARCH_PATHS={a.voodooi2c_headers.resolve()}'],check=True)
subprocess.run(['xcodebuild','-project',str(alc/'AppleALC.xcodeproj'),'-scheme','AppleALC','-configuration','Debug','-derivedDataPath',str(ROOT/'build/applealc'),'build','CODE_SIGNING_ALLOWED=NO'],check=True)
print('Builds finished in build/. Nothing installed; playback remains disabled by default in Cirrus source plist.')
