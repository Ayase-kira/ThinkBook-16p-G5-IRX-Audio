# ThinkBook 16p G5 IRX — macOS 内置扬声器修复记录与源码

面向 Lenovo ThinkBook 16p G5 IRX、Realtek ALC287（SSID `17AA:38F9`）与两颗 CS35L41 的实验性音频移植。**一台机器上用户已确认播放音乐正常；尚不能保证所有同型号或不同批次通用。**

本仓库公开实现与复现方法，不提供整套 EFI，也不提供可直接照搬的个人校准数据或预编译安装包。当前移植需要每台机器自己的功放 UID 和 EFI 出厂校准记录；请先阅读 [适配边界](docs/COMPATIBILITY.md)。

## 当前方案

- 定制 CirrusAudioFixup 1.0.6：驱动两颗低音功放，保留匹配本机的正常 DSP 固件、调音、UID 校准及保护；修正停止播放命令，限制最终 I2C 写入。
- 定制 AppleALC 1.9.9：保留 layout 16 的双声道 `Pin17 → DAC2`，耳机 `Pin21 → DAC3`；通过已有音频命令钩子让 `Pin14 → DAC2` 高音跟随双声道播放与停止。
- **不是四个独立声道，也未实现独立的软件高低音分频。**曾添加并行 PathMap，实际产生四声道/通道偏移并导致低音不启动，因此已撤回。
- 不替换使用者现有的 VoodooI2C，不安装后台常驻服务；本移植直接调用适配时使用的 VoodooI2C 原生传输接口，不能据此认定任意版本兼容。

## 已确认与未确认

| 项目 | 状态 |
| --- | --- |
| 两个低音实际发声、左右分离 | 用户实听确认 |
| 正常双声道下临时打开高音 | 多次实听确认 |
| 最终高音跟随版播放音乐 | 用户反馈完全正常；按用户要求未再采集寄存器复测 |
| 睡眠唤醒、耳机切换、长时间稳定性 | 最终版本尚未逐项实测 |
| 其他同型号机器 | 尚无独立复现 |
| Windows 等效响度、频响、原厂分频点 | 未测定 |

开发时系统为 macOS 15.6；不据此保证其他系统版本可用。`READY_DSP`、寄存器读回成功均不等于实际扬声器已发声。

## 使用与构建

先阅读 [构建说明](docs/BUILD.md)、[试用与回退](docs/INSTALL.md)及 [技术过程](docs/TECHNICAL.md)。固件文件需从你有权使用的 OEM 驱动或匹配来源自行获取，本仓库仅保留名称/哈希及本地嵌入工具。请勿关闭 DSP 保护、清零校准或套用别人的 UID/电阻值。

## 来源、致谢与许可证

本项目基于 [hoaug-tran/CirrusAudioFixup](https://github.com/hoaug-tran/CirrusAudioFixup)、[acidanthera/AppleALC](https://github.com/acidanthera/AppleALC)、[acidanthera/Lilu](https://github.com/acidanthera/Lilu) 与 Linux ALSA 驱动资料；[DexterSLamb/CmlSOFAudio](https://github.com/DexterSLamb/CmlSOFAudio) 为思路参考。原作者与各项目许可证必须保留。

CirrusAudioFixup 使用上游的非商业软件分发许可证：允许免费修改及分发，禁止出售软件或放入收费 EFI 包。AppleALC 使用 BSD 3-Clause。固件不因嵌入驱动而自动变成上述许可证。详见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) 与 `licenses/`。

欢迎同硬件用户反馈；提交 Issue 请只贴已脱敏的硬件标识、版本和症状，不要上传完整 EFI、三码、UUID、NVRAM、个人校准或完整系统转储。
