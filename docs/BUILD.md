# 从源码构建

这是按机器配置的开发流程，不是即装即用包。要求 Xcode/命令行工具、Python3、Git；另行取得 MacKernelSDK、兼容的 VoodooI2C 原生控制器头文件、Lilu DEBUG kext 开发头文件。参考机运行Lilu1.7.1、VoodooI2C2.9.1；本工程不替换你的依赖，不保证任意版本的ABI兼容。

1. 克隆并固定 AppleALC 基线（勿改成不同提交直接套补丁）：

```sh
mkdir -p deps local
git clone https://github.com/acidanthera/AppleALC.git deps/AppleALC
git -C deps/AppleALC checkout ff01db21749271916d44605503499ceaa61d94b2
python3 tools/prepare-applealc.py deps/AppleALC
```

2. 把 `config/machine.example.json` 复制到 `local/machine.json`，填入你自己的左右功放硬件UID和经过验证的EFI出厂电阻校准。左右分别对应I2C 0x41/0x40，不能按其他机型顺序猜测。没有这些数据先停止；本仓库不提供可编造的默认值。然后：

```sh
python3 tools/configure-machine.py local/machine.json --applealc deps/AppleALC
```

3. 自行取得匹配且有权使用的以下文件；工具强制核对工作案例中的SHA256和长度。相同型号但调音不同的机器不可强行沿用这组文件。

- `halo_cspl_RAM_revB2_29.63.1.wmfw`
- `cs35l41-dsp1-spk-prot-17aa38f9-spkid1-l0.bin`
- `cs35l41-dsp1-spk-prot-17aa38f9-spkid1-r0.bin`

这些名称可在Linux firmware的Cirrus目录对应到参考调音；来源许可独立于本仓库。不要使用无DSP旁路或替换成其他板子的调音。

```sh
python3 tools/embed-firmware.py \
  --wmfw local/halo_cspl_RAM_revB2_29.63.1.wmfw \
  --left local/cs35l41-dsp1-spk-prot-17aa38f9-spkid1-l0.bin \
  --right local/cs35l41-dsp1-spk-prot-17aa38f9-spkid1-r0.bin
```

4. 运行保护逻辑测试：

```sh
bash tools/test.sh
```

停止测试会故意模拟一次mailbox超时并打印ERROR；最终PASS才是预期结果。旧完整runtime mock不支持此原生I2C移植，未作为通过项。主机测试不等于真机功放测试。

5. 提供你实际审查过的开发依赖绝对路径，构建两个kext：

```sh
python3 tools/build.py \
  --sdk /absolute/path/to/MacKernelSDK \
  --voodooi2c-headers /absolute/path/to/VoodooI2CDevice \
  --applealc deps/AppleALC \
  --lilu /absolute/path/to/DEBUG/Lilu.kext
```

Lilu开发头文件必须含Darwin25枚举`KernelVersion::Tahoe`；参考机旧1.7.1开发头文件在本地仅补充过`Tahoe=25`以便编译，但系统Lilu未改。推荐自行匹配兼容开发头文件，不能将缺符号警告当作可忽略。MacKernelSDK的libkmod与框架路径需完整。

产物分别在 `build/cirrus/Build/Products/Debug/` 与 `build/applealc/Build/Products/Debug/`。脚本不安装驱动，也不改EFI。Cirrus构建的EnableThinkBookPlayback默认false，读完INSTALL.md并核对自己硬件后再决定是否启用。

生成的MachineIdentity.hpp、Firmware.hpp、local/、deps/、build/均被Git忽略。不要打包或上传这些目录；其中可能有个人硬件身份、校准与独立许可固件。
