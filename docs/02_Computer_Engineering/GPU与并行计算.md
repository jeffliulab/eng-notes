# GPU与并行计算

## 概述

GPU（图形处理单元）最初为图形渲染设计，但其大规模并行架构使其成为深度学习推理和传感器数据处理的理想加速器。在机器人系统中，GPU负责视觉感知、点云处理和神经网络推理等计算密集型任务。

## GPU架构基础

### CPU vs GPU：设计哲学

| 特性 | CPU | GPU |
|------|-----|-----|
| 核心数 | 4-16（大核） | 数百至数千（小核） |
| 时钟频率 | 2-5 GHz | 1-2 GHz |
| 缓存 | 大（数十MB L3） | 小（数MB L2） |
| 控制逻辑 | 复杂（分支预测、乱序执行） | 简单 |
| 适合任务 | 复杂逻辑、低延迟 | 大规模并行、高吞吐 |
| 设计目标 | 最小化延迟 | 最大化吞吐量 |

```
CPU: 少量大核心，优化延迟
┌──────────────┐  ┌──────────────┐
│   大核心 1    │  │   大核心 2    │
│ [控制] [ALU] │  │ [控制] [ALU] │
│ [L1 Cache]   │  │ [L1 Cache]   │
└──────────────┘  └──────────────┘
        ┌──────────────────┐
        │    大 L3 Cache    │
        └──────────────────┘

GPU: 大量小核心，优化吞吐
┌────┐┌────┐┌────┐┌────┐┌────┐┌────┐┌────┐┌────┐
│core││core││core││core││core││core││core││core│ ...
└────┘└────┘└────┘└────┘└────┘└────┘└────┘└────┘
```

### NVIDIA GPU架构

NVIDIA GPU的核心组织结构：

**Streaming Multiprocessor (SM)**

SM是GPU的基本计算单元，每个SM包含：

- **CUDA核心（FP32）**：执行浮点运算
- **Tensor核心**：专用矩阵运算加速器
- **共享内存（Shared Memory）**：SM内线程共享的低延迟存储
- **寄存器文件**：大量寄存器支持线程上下文
- **Warp调度器**：管理线程束的执行

<div class="diagram">
<svg viewBox="0 0 560 860" xmlns="http://www.w3.org/2000/svg">
  <defs><marker id="arr-m0" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="var(--dia-stroke)"/></marker></defs>
  
  <line x1="195" y1="540" x2="280" y2="630" stroke="var(--dia-stroke)" stroke-width="1.5" marker-end="url(#arr-m0)"/>
  <line x1="365" y1="540" x2="280" y2="630" stroke="var(--dia-stroke)" stroke-width="1.5" marker-end="url(#arr-m0)"/>
  <line x1="450" y1="400" x2="280" y2="630" stroke="var(--dia-stroke)" stroke-width="1.5" marker-end="url(#arr-m0)"/>
  <line x1="280" y1="680" x2="280" y2="770" stroke="var(--dia-stroke)" stroke-width="1.5" marker-end="url(#arr-m0)"/>
  <rect x="40" y="70" width="140" height="50" rx="4" fill="var(--dia-bg-card)" stroke="var(--dia-stroke)" stroke-width="1.6"/>
  <rect x="40" y="70" width="3" height="50" fill="var(--dia-accent)"/>
  <text x="110" y="99" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">CUDA Cores x128</text>
  <rect x="210" y="70" width="140" height="50" rx="4" fill="var(--dia-bg-card)" stroke="var(--dia-stroke)" stroke-width="1.6"/>
  <rect x="210" y="70" width="3" height="50" fill="var(--dia-accent)"/>
  <text x="280" y="99" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">Tensor Cores x4</text>
  <rect x="380" y="70" width="140" height="50" rx="4" fill="var(--dia-bg-card)" stroke="var(--dia-stroke)" stroke-width="1.6"/>
  <rect x="380" y="70" width="3" height="50" fill="var(--dia-accent)"/>
  <text x="450" y="92" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">Shared Memory</text>
  <text x="450" y="106" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">128KB</text>
  <rect x="40" y="210" width="140" height="50" rx="4" fill="var(--dia-bg-card)" stroke="var(--dia-stroke)" stroke-width="1.6"/>
  <rect x="40" y="210" width="3" height="50" fill="var(--dia-accent)"/>
  <text x="110" y="232" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">Warp Schedulers</text>
  <text x="110" y="246" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">x4</text>
  <rect x="210" y="210" width="140" height="50" rx="4" fill="var(--dia-bg-card)" stroke="var(--dia-stroke)" stroke-width="1.6"/>
  <rect x="210" y="210" width="3" height="50" fill="var(--dia-accent)"/>
  <text x="280" y="239" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">CUDA Cores x128</text>
  <rect x="380" y="210" width="140" height="50" rx="4" fill="var(--dia-bg-card)" stroke="var(--dia-stroke)" stroke-width="1.6"/>
  <rect x="380" y="210" width="3" height="50" fill="var(--dia-accent)"/>
  <text x="450" y="239" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">Tensor Cores x4</text>
  <rect x="40" y="350" width="140" height="50" rx="4" fill="var(--dia-bg-card)" stroke="var(--dia-stroke)" stroke-width="1.6"/>
  <rect x="40" y="350" width="3" height="50" fill="var(--dia-accent)"/>
  <text x="110" y="372" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">Shared Memory</text>
  <text x="110" y="386" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">128KB</text>
  <rect x="210" y="350" width="140" height="50" rx="4" fill="var(--dia-bg-card)" stroke="var(--dia-stroke)" stroke-width="1.6"/>
  <rect x="210" y="350" width="3" height="50" fill="var(--dia-accent)"/>
  <text x="280" y="372" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">Warp Schedulers</text>
  <text x="280" y="386" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">x4</text>
  <rect x="380" y="350" width="140" height="50" rx="4" fill="var(--dia-bg-card)" stroke="var(--dia-stroke)" stroke-width="1.6"/>
  <rect x="380" y="350" width="3" height="50" fill="var(--dia-accent)"/>
  <text x="450" y="379" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">... SM N</text>
  <rect x="210" y="630" width="140" height="50" rx="4" fill="var(--dia-bg-card)" stroke="var(--dia-stroke)" stroke-width="1.6"/>
  <rect x="210" y="630" width="3" height="50" fill="var(--dia-green)"/>
  <text x="280" y="659" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">L2 Cache</text>
  <rect x="210" y="770" width="140" height="50" rx="4" fill="var(--dia-bg-card)" stroke="var(--dia-stroke)" stroke-width="1.6"/>
  <rect x="210" y="770" width="3" height="50" fill="var(--dia-blue)"/>
  <text x="280" y="792" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">Global Memory /</text>
  <text x="280" y="806" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">VRAM</text>
  <rect x="125" y="490" width="140" height="50" rx="4" fill="var(--dia-bg-card)" stroke="var(--dia-stroke)" stroke-width="1.6"/>
  <rect x="125" y="490" width="3" height="50" fill="var(--dia-accent)"/>
  <text x="195" y="519" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">SM_0</text>
  <rect x="295" y="490" width="140" height="50" rx="4" fill="var(--dia-bg-card)" stroke="var(--dia-stroke)" stroke-width="1.6"/>
  <rect x="295" y="490" width="3" height="50" fill="var(--dia-accent)"/>
  <text x="365" y="519" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">SM_1</text>
</svg>
</div>


### SIMT执行模型

GPU采用**SIMT（Single Instruction, Multiple Threads）**执行模型：

- 线程以**Warp**（32个线程）为单位执行
- 同一Warp内的线程执行相同的指令
- 但可以操作不同的数据（不同地址、不同寄存器）

$$
\text{GPU总线程数} = \text{SM数量} \times \text{每SM最大线程数}
$$

!!! warning "Warp分歧（Warp Divergence）"
    当Warp内的线程遇到条件分支走向不同路径时，GPU必须**串行执行**两条路径。这会严重降低效率：
    
    ```c
    if (threadIdx.x % 2 == 0) {
        // 偶数线程执行这里
    } else {
        // 奇数线程执行这里
    }
    // 最坏情况：性能减半
    ```

## CUDA编程基础

### 线程层次

CUDA采用分层的线程组织：

| 层次 | 说明 | 对应硬件 |
|------|------|----------|
| Thread | 最小执行单位 | CUDA核心 |
| Warp | 32个线程 | SM中的Warp调度单位 |
| Block | 多个Warp | 映射到一个SM |
| Grid | 多个Block | 整个GPU |

### 内存层次

| 内存类型 | 大小 | 延迟 | 作用域 |
|----------|------|------|--------|
| 寄存器 | ~256KB/SM | 1周期 | 单线程 |
| 共享内存 | 64-228KB/SM | ~5周期 | Block内共享 |
| L1 Cache | 与共享内存共享 | ~30周期 | SM |
| L2 Cache | 数MB | ~200周期 | 全GPU |
| Global Memory (VRAM) | 4-80GB | ~400周期 | 全GPU |

### CUDA Kernel示例

```cuda
// 向量加法 - 最基本的CUDA kernel
__global__ void vectorAdd(float* A, float* B, float* C, int N) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx < N) {
        C[idx] = A[idx] + B[idx];
    }
}

// 启动kernel
int threadsPerBlock = 256;
int blocksPerGrid = (N + threadsPerBlock - 1) / threadsPerBlock;
vectorAdd<<<blocksPerGrid, threadsPerBlock>>>(d_A, d_B, d_C, N);
```

### 图像处理示例

```cuda
// 图像灰度化 - 机器人视觉预处理
__global__ void rgb2gray(unsigned char* rgb, unsigned char* gray, 
                         int width, int height) {
    int x = blockIdx.x * blockDim.x + threadIdx.x;
    int y = blockIdx.y * blockDim.y + threadIdx.y;
    
    if (x < width && y < height) {
        int idx = y * width + x;
        int rgb_idx = idx * 3;
        // ITU-R BT.601 标准
        gray[idx] = (unsigned char)(0.299f * rgb[rgb_idx] + 
                                     0.587f * rgb[rgb_idx+1] + 
                                     0.114f * rgb[rgb_idx+2]);
    }
}

// 2D grid启动
dim3 block(16, 16);
dim3 grid((width+15)/16, (height+15)/16);
rgb2gray<<<grid, block>>>(d_rgb, d_gray, width, height);
```

## 并行加速理论

### 理论加速比

理想情况下，$N$ 个处理单元的加速比：

$$
S_{\text{ideal}} = N
$$

实际加速比受限于：

$$
S_{\text{actual}} = \frac{T_{\text{serial}}}{T_{\text{parallel}}} = \frac{T_{\text{serial}}}{T_{\text{serial\_part}} + \frac{T_{\text{parallel\_part}}}{N} + T_{\text{overhead}}}
$$

其中 $T_{\text{overhead}}$ 包括：

- 线程创建和同步开销
- 内存拷贝开销（CPU↔GPU）
- 负载不均衡

### Gustafson定律

与Amdahl定律（固定问题规模）不同，Gustafson定律考虑**随处理器数增加扩展问题规模**：

$$
S_G = N - \alpha(N-1)
$$

其中 $\alpha$ 是串行部分的比例。这解释了为什么GPU在大规模数据处理中如此有效。

## TensorRT推理加速

### TensorRT优化流程

TensorRT是NVIDIA的深度学习推理优化器：

<div class="diagram">
<svg viewBox="0 0 900 200" xmlns="http://www.w3.org/2000/svg">
  <defs><marker id="arr-m0" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="var(--dia-stroke)"/></marker></defs>
  
  <line x1="180" y1="95" x2="270" y2="95" stroke="var(--dia-stroke)" stroke-width="1.5" marker-end="url(#arr-m0)"/>
  <line x1="410" y1="95" x2="500" y2="95" stroke="var(--dia-stroke)" stroke-width="1.5" marker-end="url(#arr-m0)"/>
  <line x1="640" y1="95" x2="730" y2="95" stroke="var(--dia-stroke)" stroke-width="1.5" marker-end="url(#arr-m0)"/>
  <line x1="870" y1="95" x2="960" y2="95" stroke="var(--dia-stroke)" stroke-width="1.5" marker-end="url(#arr-m0)"/>
  <line x1="1100" y1="95" x2="1190" y2="95" stroke="var(--dia-stroke)" stroke-width="1.5" marker-end="url(#arr-m0)"/>
  <rect x="40" y="70" width="140" height="50" rx="4" fill="var(--dia-bg-card)" stroke="var(--dia-stroke)" stroke-width="1.6"/>
  <rect x="40" y="70" width="3" height="50" fill="var(--dia-accent)"/>
  <text x="110" y="99" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">PyTorch/ONNX模型</text>
  <rect x="270" y="70" width="140" height="50" rx="4" fill="var(--dia-bg-card)" stroke="var(--dia-stroke)" stroke-width="1.6"/>
  <rect x="270" y="70" width="3" height="50" fill="var(--dia-green)"/>
  <text x="340" y="99" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">TensorRT解析</text>
  <rect x="500" y="70" width="140" height="50" rx="4" fill="var(--dia-bg-card)" stroke="var(--dia-stroke)" stroke-width="1.6"/>
  <rect x="500" y="70" width="3" height="50" fill="var(--dia-blue)"/>
  <text x="570" y="99" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">层融合 Layer Fusion</text>
  <rect x="730" y="70" width="140" height="50" rx="4" fill="var(--dia-bg-card)" stroke="var(--dia-stroke)" stroke-width="1.6"/>
  <rect x="730" y="70" width="3" height="50" fill="var(--dia-accent)"/>
  <text x="800" y="99" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">精度校准 FP16/INT8</text>
  <rect x="960" y="70" width="140" height="50" rx="4" fill="var(--dia-bg-card)" stroke="var(--dia-stroke)" stroke-width="1.6"/>
  <rect x="960" y="70" width="3" height="50" fill="var(--dia-green)"/>
  <text x="1030" y="92" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">Kernel自动调优</text>
  <text x="1030" y="106" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">Auto-Tuning</text>
  <rect x="1190" y="70" width="140" height="50" rx="4" fill="var(--dia-bg-card)" stroke="var(--dia-stroke)" stroke-width="1.6"/>
  <rect x="1190" y="70" width="3" height="50" fill="var(--dia-blue)"/>
  <text x="1260" y="99" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">优化后的引擎 TRT Engine</text>
</svg>
</div>


### 关键优化技术

| 技术 | 说明 | 典型加速比 |
|------|------|-----------|
| 层融合 | 合并Conv+BN+ReLU为一个kernel | 1.5-2x |
| FP16推理 | 半精度浮点 | 2-3x |
| INT8量化 | 8位整数推理 | 3-5x |
| 动态batch | 自动选择最优batch size | 1.2-1.5x |

### 推理性能示例

在Jetson Orin NX上的典型推理性能：

| 模型 | FP32 | FP16 | INT8 | 用途 |
|------|------|------|------|------|
| YOLOv8n | 45 FPS | 120 FPS | 200 FPS | 目标检测 |
| YOLOv8s | 25 FPS | 70 FPS | 130 FPS | 目标检测 |
| MobileNetV3 | 200 FPS | 500 FPS | 800 FPS | 图像分类 |
| PointPillars | 15 FPS | 35 FPS | 60 FPS | 3D目标检测 |

## Jetson GPU规格对比

| 特性 | Orin Nano | Orin NX | AGX Orin |
|------|-----------|---------|----------|
| GPU架构 | Ampere | Ampere | Ampere |
| CUDA核心 | 1024 | 2048 | 2048 |
| Tensor核心 | 32 | 64 | 64 |
| GPU频率 | 625 MHz | 918 MHz | 1.3 GHz |
| AI算力 (INT8) | 40 TOPS | 100 TOPS | 275 TOPS |
| 显存 | 8GB共享 | 8/16GB共享 | 32/64GB共享 |
| 功耗 | 7-15W | 10-25W | 15-60W |

## GPU编程最佳实践

### 1. 最大化占用率

确保足够多的线程来隐藏内存延迟：

$$
\text{占用率} = \frac{\text{活跃Warp数}}{\text{SM最大Warp数}}
$$

目标占用率 > 50%。

### 2. 合并内存访问

相邻线程访问相邻内存地址：

```c
// 好：合并访问（Coalesced）
C[threadIdx.x] = A[threadIdx.x] + B[threadIdx.x];

// 差：跨步访问（Strided）
C[threadIdx.x] = A[threadIdx.x * stride];
```

### 3. 减少CPU-GPU数据传输

```python
# 差：频繁拷贝
for frame in camera_stream:
    gpu_frame = frame.to('cuda')     # CPU -> GPU
    result = model(gpu_frame)         # GPU推理
    cpu_result = result.to('cpu')     # GPU -> CPU

# 好：流水线化，使用CUDA Stream
stream1 = torch.cuda.Stream()
stream2 = torch.cuda.Stream()
# 在stream1上传输数据的同时，stream2上执行推理
```

### 4. 使用Tensor核心

利用Tensor核心加速矩阵运算：

$$
D = A \times B + C \quad \text{（矩阵乘加）}
$$

Tensor核心在一个时钟周期内完成 $4 \times 4$ 矩阵的乘加运算。

!!! tip "在PyTorch中启用Tensor核心"
    ```python
    # 使用FP16自动混合精度
    with torch.cuda.amp.autocast():
        output = model(input)
    ```

## 机器人视觉处理流水线

<div class="diagram">
<svg viewBox="0 0 900 200" xmlns="http://www.w3.org/2000/svg">
  <defs><marker id="arr-m0" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="var(--dia-stroke)"/></marker></defs>
  
  <line x1="180" y1="95" x2="270" y2="95" stroke="var(--dia-stroke)" stroke-width="1.5" marker-end="url(#arr-m0)"/>
  <line x1="410" y1="95" x2="500" y2="95" stroke="var(--dia-stroke)" stroke-width="1.5" marker-end="url(#arr-m0)"/>
  <line x1="640" y1="95" x2="730" y2="95" stroke="var(--dia-stroke)" stroke-width="1.5" marker-end="url(#arr-m0)"/>
  <line x1="870" y1="95" x2="960" y2="95" stroke="var(--dia-stroke)" stroke-width="1.5" marker-end="url(#arr-m0)"/>
  <line x1="1100" y1="95" x2="1190" y2="95" stroke="var(--dia-stroke)" stroke-width="1.5" marker-end="url(#arr-m0)"/>
  <rect x="40" y="70" width="140" height="50" rx="4" fill="var(--dia-bg-card)" stroke="var(--dia-stroke)" stroke-width="1.6"/>
  <rect x="40" y="70" width="3" height="50" fill="var(--dia-accent)"/>
  <text x="110" y="99" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">Camera CSI/USB</text>
  <rect x="270" y="70" width="140" height="50" rx="4" fill="var(--dia-bg-card)" stroke="var(--dia-stroke)" stroke-width="1.6"/>
  <rect x="270" y="70" width="3" height="50" fill="var(--dia-green)"/>
  <text x="340" y="99" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">CPU 图像解码</text>
  <rect x="500" y="70" width="140" height="50" rx="4" fill="var(--dia-bg-card)" stroke="var(--dia-stroke)" stroke-width="1.6"/>
  <rect x="500" y="70" width="3" height="50" fill="var(--dia-blue)"/>
  <text x="570" y="92" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">GPU 预处理</text>
  <text x="570" y="106" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">resize/normalize</text>
  <rect x="730" y="70" width="140" height="50" rx="4" fill="var(--dia-bg-card)" stroke="var(--dia-stroke)" stroke-width="1.6"/>
  <rect x="730" y="70" width="3" height="50" fill="var(--dia-accent)"/>
  <text x="800" y="99" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">GPU 神经网络推理 检测/分割</text>
  <rect x="960" y="70" width="140" height="50" rx="4" fill="var(--dia-bg-card)" stroke="var(--dia-stroke)" stroke-width="1.6"/>
  <rect x="960" y="70" width="3" height="50" fill="var(--dia-green)"/>
  <text x="1030" y="99" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">GPU 后处理 NMS/解码</text>
  <rect x="1190" y="70" width="140" height="50" rx="4" fill="var(--dia-bg-card)" stroke="var(--dia-stroke)" stroke-width="1.6"/>
  <rect x="1190" y="70" width="3" height="50" fill="var(--dia-blue)"/>
  <text x="1260" y="92" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">CPU 结果发布 ROS2</text>
  <text x="1260" y="106" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">Topic</text>
</svg>
</div>


使用GStreamer + DeepStream可以实现全GPU流水线，避免CPU-GPU之间的数据拷贝。

## 小结

1. **GPU通过大规模并行**弥补单线程性能的不足
2. **SIMT模型**要求避免Warp分歧
3. **内存层次**和**合并访问**对GPU性能至关重要
4. **TensorRT**可以将推理性能提升3-5倍
5. **减少CPU-GPU数据传输**是优化的关键
6. Jetson系列为机器人提供了从40到275 TOPS的AI算力选择

## 参考资料

- NVIDIA CUDA Programming Guide: [https://docs.nvidia.com/cuda/](https://docs.nvidia.com/cuda/)
- NVIDIA TensorRT Documentation: [https://developer.nvidia.com/tensorrt](https://developer.nvidia.com/tensorrt)
- NVIDIA Jetson Developer Guide: [https://developer.nvidia.com/embedded/](https://developer.nvidia.com/embedded/)
- Kirk, D. B., & Hwu, W. *Programming Massively Parallel Processors*
