# Audio Morph Studio Pro

一款全功能的音频风格转换工作站，支持从8-bit复古游戏音效到现代AI生成音乐的全面转换。

## 🚀 快速开始

### 1. 环境准备
确保已安装 Python 3.8+ 并安装依赖：
```bash
pip install -r requirements.txt
```
*注意：AI功能需要 PyTorch 和 Torchaudio。如果需要 GPU 加速，请安装 CUDA 版本的 PyTorch。*

### 2. 启动图形界面 (GUI)
我们提供了现代化的深色主题界面，无需编写代码即可使用。
```bash
python run_ui.py
```
- **左侧**: 选择预设（如 "NES Console", "Worn Vinyl LP"）。
- **右侧**: 选择输入/输出文件，调整参数，点击 "MORPH AUDIO" 开始转换。

### 3. 命令行使用 (CLI)
适合批量处理或服务器部署。
```bash
# 列出所有预设
python src/main.py --list-presets

# 运行转换
python src/main.py -i input.wav -o output.wav -p "Nintendo 8-bit"
```

---

## 🧠 AI 模型训练指南

本项目内置了基于 CNN Autoencoder 的风格特征学习框架。您可以训练自己的模型来捕捉特定音乐流派的特征。

### 1. 准备数据
创建一个文件夹，放入您想要模仿的风格的音频文件（建议 50+ 个 .wav 或 .mp3 文件）。
```bash
mkdir data/my_style
# 将音频文件放入 data/my_style
```

### 2. 运行训练脚本
使用 `src/train.py` 开始训练：
```bash
python src/train.py --data_dir data/my_style --style_name my_custom_style --epochs 100 --batch_size 8
```
- 模型将保存到 `models/my_custom_style.pth`。

### 3. 使用训练好的模型
在 `src/presets_data` 中创建一个新的 YAML 预设文件（例如 `my_style.yaml`）：
```yaml
name: My Custom Style
category: AI
engine_type: ai
style: neural_style
params:
  model_path: "models/my_custom_style.pth"
```
然后即可在 GUI 或 CLI 中选择该预设。

---

## 🗺️ 功能实现状态与路线图

### ✅ 已实现功能 (Implemented)
- **核心引擎**:
  - DSP 引擎 (复古效果, 物理模拟)
  - AI 引擎 (CNN 风格迁移框架)
  - 混合引擎 (Hybrid pipeline)
- **复古/模拟效果**:
  - [x] 8-bit / Bitcrushing (NES, GameBoy)
  - [x] 磁带模拟 (Saturation, Hiss)
  - [x] 黑胶唱片 (Crackle, Wow & Flutter)
  - [x] 通讯设备 (Telephone, Radio)
- **AI 功能**:
  - [x] 风格迁移推理接口
  - [x] 模型训练脚本 (`train.py`)
  - [x] 基础流派变形 (基于效果链)
- **系统**:
  - [x] YAML 预设管理系统
  - [x] PyQt6 现代化图形界面

### 🚧 待开发/缺失功能 (Gap Analysis)
根据完整项目规划，以下模块尚待开发：

1.  **高级 DSP 模拟**:
    - [ ] **16-bit/32-bit 时代**: SNES (SPC700), Sega Genesis (FM Synthesis) 的芯片级模拟。
    - [ ] **专业录音设备**: 电子管麦克风 (Neumann U47)、压缩器 (LA-2A) 的电路级物理建模。
    - [ ] **空间声学**: 基于卷积混响 (Convolution Reverb) 的真实环境模拟（音乐厅、教堂）。

2.  **高级 AI 模型**:
    - [ ] **GAN/Diffusion**: 集成 Riffusion 或 MusicLM 以实现生成式风格转换。
    - [ ] **音色替换**: 基于 RVC (Retrieval-based Voice Conversion) 的乐器/人声替换。
    - [ ] **Stem 分离**: 集成 Spleeter/Demucs 实现分轨处理。

3.  **用户体验增强**:
    - [ ] **实时预览**: 低延迟的实时音频处理监听。
    - [ ] **可视化**: 频谱图、波形图的实时显示。
    - [ ] **插件化**: 导出为 VST/AU 插件格式。

---

## 核心转换引擎架构

### 1. 多维风格转换矩阵
- **时代风格转换**: 复古游戏机 (70s-90s), 经典磁带机, 数字时代, 现代流媒体, 未来主义
- **音乐流派转换**: 电子, 古典, 摇滚, 流行, 民族
- **设备模拟转换**: 录音设备, 播放设备, 通信设备, 环境声学
- **特殊效果转换**: 影视特效, 游戏音效, 艺术实验, AI生成

## 目录结构
- `src/engine`: 核心处理引擎 (DSP, AI, Hybrid)
- `src/presets`: 预设管理
- `src/ui`: 用户界面
- `src/train.py`: AI 训练入口
- `models/`: 存放训练好的模型权重
- `tests`: 测试套件
