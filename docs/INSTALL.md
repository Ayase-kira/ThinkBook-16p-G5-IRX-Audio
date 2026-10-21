# 试用与回退

本仓库没有自动EFI安装器。先备份自己的整个OC目录和config，并准备可启动的恢复介质。不可用本项目代替完整EFI配置。

仅在硬件、固件、左右顺序和自己的EFI校准均已验证后构建。Cirrus配置默认保持EnableThinkBookPlayback=false；完成只读身份确认、复核固件和校准后才在自己的构建Info.plist内启用。没有校准时不要尝试绕过保护。

当前已用的配置是alcid=16、alcverbs=1，AppleALC与CirrusAudioFixup启用；旧ThinkBookAmpProbe停用，不能并行访问功放。按自己的OpenCore版本维护Kernel/Add、路径及加载关系；不要复制参考机的全部boot-args。

一次只换一个已备份的组件，验证plist和对应版本ocvalidate后重启。先从低音量短音开始，分别实听左右、高低音，随后验证停止/重新播放、耳机、睡眠唤醒；任何异常先恢复上一个已知良好组件。恢复驱动后需重启；不要热卸载活动AppleHDA/AppleALC。保持自己的DSP固件、调音和校准。

不复制本项目参考机的校准，不提高到任意大增益。没有独立验证前不要宣称自己的机器完全兼容。
