#!/usr/bin/env python3
import argparse,json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--wmfw',type=Path,required=True);p.add_argument('--left',type=Path,required=True);p.add_argument('--right',type=Path,required=True);a=p.parse_args();manifest=json.loads((ROOT/'config/firmware-hashes.json').read_text());parts=[]
for name,path in [('tb_wmfw',a.wmfw),('tb_left',a.left),('tb_right',a.right)]:
 data=path.read_bytes();assert len(data)==manifest[name]['size'] and hashlib.sha256(data).hexdigest()==manifest[name]['sha256'],f'Firmware/tuning mismatch: {name}'
 body='\n'.join(' '+','.join(f'0x{x:02x}' for x in data[i:i+24])+',' for i in range(0,len(data),24));parts.append('static const uint8_t '+name+'[]={\n'+body+'\n};\n')
target=ROOT/'src/CirrusAudioFixup/CirrusAudioFixup/Devices/CS35L41/Resources/Firmware.hpp'
target.write_text('#pragma once\n// Local OEM firmware embedding. Not covered by source license; do not commit.\n#include <IOKit/IOLib.h>\n'+''.join(parts)+(ROOT/'tools/firmware-footer.txt').read_text());print('Exact matching firmware header generated locally; not installed.')
