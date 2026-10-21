#pragma once
// No stream binding, format, DSP, codec coefficient or gain changes.
struct ThinkBookTweeterState {
 bool owned=false, fault=false;
 template<class IO> bool restore(IO &io) {
  bool ok=io.set(0x300,0xa080);ok=io.set(0x300,0x9080)&&ok;
  ok=io.set(0x707,0)&&ok;ok=io.set(0x705,3)&&ok;io.wait();
  unsigned p=0,l=0,r=0;
  ok=io.get(0x14,0xf07,0,p)&&io.get(0x14,0xb00,0xa000,l)&&io.get(0x14,0xb00,0x8000,r)&&p==0&&l==0x80&&r==0x80&&ok;
  if(ok)owned=false;else fault=true;return ok;
 }
 template<class IO> void update(IO &io) {
  unsigned id=0,fmt=0,stream=0,pin=0,power=0,dacpower=0,hp=0,p14=0,pw14=0,l=0,r=0,conn=0,eapd=0;
  bool read=io.get(0,0xf00,0,id)&&id==0x10ec0287&&io.get(2,0xa00,0,fmt)&&
   io.get(2,0xf06,0,stream)&&io.get(0x17,0xf07,0,pin)&&io.get(0x17,0xf05,0,power)&&
   io.get(2,0xf05,0,dacpower)&&io.get(0x21,0xf09,0,hp)&&io.get(0x14,0xf07,0,p14)&&
   io.get(0x14,0xf05,0,pw14)&&io.get(0x14,0xb00,0xa000,l)&&io.get(0x14,0xb00,0x8000,r)&&
   io.get(0x14,0xf02,0,conn)&&io.get(0x14,0xf0c,0,eapd);
  if(!read){if(owned)restore(io);return;}
  bool active=fmt==0x31&&(stream>>4)!=0&&!(stream&15)&&pin==0x40&&!(power&15)&&!(dacpower&15)&&!(hp&0x80000000U)&&conn==2&&eapd==2;
  if(!active){if(owned)restore(io);return;}
  if(fault)return;
  if(owned){if(p14!=0x40||(pw14&15)||l!=0||r!=0)restore(io);return;}
  if(p14!=0||(pw14&15)!=3||l!=0x80||r!=0x80)return;
  owned=true;
  bool ok=io.set(0x705,0);io.wait();ok=io.set(0x707,0x40)&&ok;ok=io.set(0x300,0xb000)&&ok;
  unsigned post=0;ok=io.get(0x14,0xf07,0,post)&&post==0x40&&ok;
  if(!ok){fault=true;restore(io);}
 }
};
