#!/usr/bin/env python3
import argparse,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('profile',type=Path);p.add_argument('--applealc',required=True,type=Path);a=p.parse_args();d=json.loads(a.profile.read_text())
uids=[int(d[k],0) for k in ['uid_left','uid_right']]
assert all(0<x<0xffffffffffffffff for x in uids) and len(set(uids))==2,'Supply distinct real hardware UIDs from your own machine'
rs=[d[k] for k in ['cal_r_left','cal_r_right']];assert all(type(x) is int and 0<x<=0xffff for x in rs),'Supply your own validated EFI calibration values'
x='#pragma once\n// PRIVATE generated machine identity: do not commit or redistribute.\n'+f'#define TB_UID_LEFT 0x{uids[0]:016x}ULL\n#define TB_UID_RIGHT 0x{uids[1]:016x}ULL\n#define TB_CAL_R_LEFT {rs[0]}U\n#define TB_CAL_R_RIGHT {rs[1]}U\n'
paths=[ROOT/'src/CirrusAudioFixup/CirrusAudioFixup/MachineIdentity.hpp',a.applealc.resolve()/'AppleALC/MachineIdentity.hpp']
for target in paths:
 assert target.parent.is_dir();target.write_text(x);target.chmod(0o600)
print('Private headers generated; values intentionally not printed. Runtime EFI UID validation remains required.')
