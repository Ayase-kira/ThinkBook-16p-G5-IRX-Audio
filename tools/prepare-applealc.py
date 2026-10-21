#!/usr/bin/env python3
import argparse,subprocess,plistlib,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('source',type=Path);a=p.parse_args();s=a.source.resolve()
assert subprocess.check_output(['git','-C',str(s),'rev-parse','HEAD'],text=True).strip()=='ff01db21749271916d44605503499ceaa61d94b2','Wrong AppleALC base'
patch=ROOT/'applealc/stereo-tweeter-mirror.patch'
subprocess.run(['git','-C',str(s),'apply','--check',str(patch)],check=True)
subprocess.run(['git','-C',str(s),'apply',str(patch)],check=True)
shutil.copy2(ROOT/'applealc/ThinkBookTweeterMirror.hpp',s/'AppleALC/ThinkBookTweeterMirror.hpp')
r=s/'Resources/ALC287'
for name in ['layout16.xml','Platforms16.xml']:shutil.copy2(ROOT/'applealc/resources'/name,r/name)
p=r/'Info.plist';d=plistlib.loads(p.read_bytes())
for key,name in [('Layouts','layout16.xml.zlib'),('Platforms','Platforms16.xml.zlib')]:
 assert not any(e['Id']==16 for e in d['Files'][key]);d['Files'][key].append({'Id':16,'Path':name})
p.write_bytes(plistlib.dumps(d))
p=s/'Resources/PinConfigs.kext/Contents/Info.plist';d=plistlib.loads(p.read_bytes());entries=d['IOKitPersonalities']['as.vit9696.AppleALC']['HDAConfigDefault'];assert not any(e.get('CodecID')==283902599 and e.get('LayoutID')==16 for e in entries);entries.append(plistlib.loads((ROOT/'applealc/resources/PinConfig16.plist').read_bytes()));p.write_bytes(plistlib.dumps(d))
print('AppleALC source prepared; next generate your private identity header.')
