#include "../applealc/ThinkBookTweeterMirror.hpp"
#include <map>
#include <tuple>
#include <vector>
#include <cassert>
#include <cstdio>
struct Mock {
 std::map<std::tuple<unsigned,unsigned,unsigned>,unsigned> regs;
 std::vector<std::pair<unsigned,unsigned>> writes;
 unsigned failVerb=0;bool failed=false;
 Mock(){regs={{ {0,0xf00,0},0x10ec0287},{{2,0xa00,0},0x31},{{2,0xf06,0},0x10},{{0x17,0xf07,0},0x40},{{0x17,0xf05,0},0},{{2,0xf05,0},0},{{0x21,0xf09,0},0},{{0x14,0xf07,0},0},{{0x14,0xf05,0},0x33},{{0x14,0xb00,0xa000},0x80},{{0x14,0xb00,0x8000},0x80},{{0x14,0xf02,0},2},{{0x14,0xf0c,0},2}};}
 void wait(){}
 bool get(unsigned n,unsigned v,unsigned a,unsigned &o){auto it=regs.find({n,v,a});if(it==regs.end())return false;o=it->second;return true;}
 bool set(unsigned v,unsigned a){writes.push_back({v,a});if(v==failVerb&&!failed){failed=true;return false;}if(v==0x705)regs[{0x14,0xf05,0}]=a|(a<<4);else if(v==0x707)regs[{0x14,0xf07,0}]=a;else if(v==0x300){if(a==0xb000){regs[{0x14,0xb00,0xa000}]=0;regs[{0x14,0xb00,0x8000}]=0;}else if(a==0xa080)regs[{0x14,0xb00,0xa000}]=0x80;else if(a==0x9080)regs[{0x14,0xb00,0x8000}]=0x80;else assert(false);}else assert(false);return true;}
};
int main(){
 {Mock m;ThinkBookTweeterState s;s.update(m);assert(s.owned&&!s.fault&&m.writes.size()==3);auto n=m.writes.size();s.update(m);assert(m.writes.size()==n);m.regs[{2,0xf06,0}]=0;s.update(m);assert(!s.owned&&!s.fault);s.update(m);assert(m.writes.size()==7);m.regs[{2,0xf06,0}]=0x10;s.update(m);assert(s.owned);m.regs[{0x21,0xf09,0}]=0x80000000;s.update(m);assert(!s.owned);}
 for(auto change: std::vector<std::pair<std::tuple<unsigned,unsigned,unsigned>,unsigned>>{{{2,0xa00,0},0x33},{{2,0xf06,0},0x12},{{0x21,0xf09,0},0x80000000},{{0x14,0xf02,0},3},{{0x14,0xf0c,0},0},{{0,0xf00,0},0x10ec0298},{{0x17,0xf05,0},0x33},{{0x14,0xf07,0},0x40}}){Mock m;ThinkBookTweeterState s;m.regs[change.first]=change.second;s.update(m);assert(!s.owned&&m.writes.empty());}
 {Mock m;ThinkBookTweeterState s;m.failVerb=0x707;s.update(m);assert(s.fault&&!s.owned);auto n=m.writes.size();s.update(m);assert(m.writes.size()==n);}
 {Mock m;ThinkBookTweeterState s;s.update(m);m.regs.erase({2,0xa00,0});s.update(m);assert(!s.owned);}
 puts("PASS: stereo enable/idle/resume, headphones, four-channel rejection, wrong identity/route, ownership, failed write rollback and fault latch");
}
