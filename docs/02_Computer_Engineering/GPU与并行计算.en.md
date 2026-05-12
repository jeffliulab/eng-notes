# GPU and Parallel Computing

## Overview

The GPU (Graphics Processing Unit) was originally designed for graphics rendering, but its massively parallel architecture has made it the ideal accelerator for deep learning inference and sensor data processing. In robot systems, the GPU handles computationally intensive tasks such as visual perception, point cloud processing, and neural network inference.

## GPU Architecture Fundamentals

### CPU vs. GPU: Design Philosophy

| Feature | CPU | GPU |
|---------|-----|-----|
| Core Count | 4-16 (large cores) | Hundreds to thousands (small cores) |
| Clock Frequency | 2-5 GHz | 1-2 GHz |
| Cache | Large (tens of MB L3) | Small (a few MB L2) |
| Control Logic | Complex (branch prediction, out-of-order execution) | Simple |
| Suitable Tasks | Complex logic, low latency | Massively parallel, high throughput |
| Design Goal | Minimize latency | Maximize throughput |

```
CPU: Few large cores, latency-optimized
+----------------+  +----------------+
|   Large Core 1 |  |   Large Core 2 |
| [Control] [ALU]|  | [Control] [ALU]|
| [L1 Cache]     |  | [L1 Cache]     |
+----------------+  +----------------+
        +--------------------+
        |   Large L3 Cache   |
        +--------------------+

GPU: Many small cores, throughput-optimized
+----++----++----++----++----++----++----++----+
|core||core||core||core||core||core||core||core| ...
+----++----++----++----++----++----++----++----+
```

### NVIDIA GPU Architecture

Core organizational structure of NVIDIA GPUs:

**Streaming Multiprocessor (SM)**

The SM is the fundamental compute unit of a GPU. Each SM contains:

- **CUDA cores (FP32)**: Execute floating-point operations
- **Tensor cores**: Dedicated matrix operation accelerators
- **Shared Memory**: Low-latency storage shared among threads within an SM
- **Register file**: Large register files to support thread contexts
- **Warp schedulers**: Manage warp execution

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


### SIMT Execution Model

GPUs employ the **SIMT (Single Instruction, Multiple Threads)** execution model:

- Threads execute in groups of **Warps** (32 threads)
- All threads in the same warp execute the same instruction
- But can operate on different data (different addresses, different registers)

$$
\text{Total GPU Threads} = \text{Number of SMs} \times \text{Max Threads per SM}
$$

!!! warning "Warp Divergence"
    When threads within a warp encounter conditional branches and take different paths, the GPU must **serially execute** both paths. This severely degrades efficiency:
    
    ```c
    if (threadIdx.x % 2 == 0) {
        // Even threads execute here
    } else {
        // Odd threads execute here
    }
    // Worst case: performance halved
    ```

## CUDA Programming Fundamentals

### Thread Hierarchy

CUDA uses a hierarchical thread organization:

| Level | Description | Hardware Mapping |
|-------|------------|-----------------|
| Thread | Smallest execution unit | CUDA core |
| Warp | 32 threads | Warp scheduling unit within an SM |
| Block | Multiple warps | Mapped to one SM |
| Grid | Multiple blocks | Entire GPU |

### Memory Hierarchy

| Memory Type | Size | Latency | Scope |
|------------|------|---------|-------|
| Registers | ~256KB/SM | 1 cycle | Per thread |
| Shared Memory | 64-228KB/SM | ~5 cycles | Shared within a block |
| L1 Cache | Shared with shared memory | ~30 cycles | SM |
| L2 Cache | Several MB | ~200 cycles | Entire GPU |
| Global Memory (VRAM) | 4-80GB | ~400 cycles | Entire GPU |

### CUDA Kernel Example

```cuda
// Vector addition - the most basic CUDA kernel
__global__ void vectorAdd(float* A, float* B, float* C, int N) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx < N) {
        C[idx] = A[idx] + B[idx];
    }
}

// Launch kernel
int threadsPerBlock = 256;
int blocksPerGrid = (N + threadsPerBlock - 1) / threadsPerBlock;
vectorAdd<<<blocksPerGrid, threadsPerBlock>>>(d_A, d_B, d_C, N);
```

### Image Processing Example

```cuda
// Image grayscale conversion - robot vision preprocessing
__global__ void rgb2gray(unsigned char* rgb, unsigned char* gray, 
                         int width, int height) {
    int x = blockIdx.x * blockDim.x + threadIdx.x;
    int y = blockIdx.y * blockDim.y + threadIdx.y;
    
    if (x < width && y < height) {
        int idx = y * width + x;
        int rgb_idx = idx * 3;
        // ITU-R BT.601 standard
        gray[idx] = (unsigned char)(0.299f * rgb[rgb_idx] + 
                                     0.587f * rgb[rgb_idx+1] + 
                                     0.114f * rgb[rgb_idx+2]);
    }
}

// 2D grid launch
dim3 block(16, 16);
dim3 grid((width+15)/16, (height+15)/16);
rgb2gray<<<grid, block>>>(d_rgb, d_gray, width, height);
```

## Parallel Speedup Theory

### Theoretical Speedup

In the ideal case, the speedup with $N$ processing units:

$$
S_{\text{ideal}} = N
$$

Actual speedup is limited by:

$$
S_{\text{actual}} = \frac{T_{\text{serial}}}{T_{\text{parallel}}} = \frac{T_{\text{serial}}}{T_{\text{serial\_part}} + \frac{T_{\text{parallel\_part}}}{N} + T_{\text{overhead}}}
$$

Where $T_{\text{overhead}}$ includes:

- Thread creation and synchronization overhead
- Memory copy overhead (CPU <-> GPU)
- Load imbalance

### Gustafson's Law

Unlike Amdahl's Law (fixed problem size), Gustafson's Law considers **scaling the problem size as the number of processors increases**:

$$
S_G = N - \alpha(N-1)
$$

Where $\alpha$ is the fraction of the serial portion. This explains why GPUs are so effective for large-scale data processing.

## TensorRT Inference Acceleration

### TensorRT Optimization Pipeline

TensorRT is NVIDIA's deep learning inference optimizer:

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
  <text x="110" y="92" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">PyTorch/ONNX</text>
  <text x="110" y="106" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">Model</text>
  <rect x="270" y="70" width="140" height="50" rx="4" fill="var(--dia-bg-card)" stroke="var(--dia-stroke)" stroke-width="1.6"/>
  <rect x="270" y="70" width="3" height="50" fill="var(--dia-green)"/>
  <text x="340" y="99" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">TensorRT Parsing</text>
  <rect x="500" y="70" width="140" height="50" rx="4" fill="var(--dia-bg-card)" stroke="var(--dia-stroke)" stroke-width="1.6"/>
  <rect x="500" y="70" width="3" height="50" fill="var(--dia-blue)"/>
  <text x="570" y="99" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">Layer Fusion</text>
  <rect x="730" y="70" width="140" height="50" rx="4" fill="var(--dia-bg-card)" stroke="var(--dia-stroke)" stroke-width="1.6"/>
  <rect x="730" y="70" width="3" height="50" fill="var(--dia-accent)"/>
  <text x="800" y="85" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">Precision</text>
  <text x="800" y="99" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">Calibration</text>
  <text x="800" y="113" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">FP16/INT8</text>
  <rect x="960" y="70" width="140" height="50" rx="4" fill="var(--dia-bg-card)" stroke="var(--dia-stroke)" stroke-width="1.6"/>
  <rect x="960" y="70" width="3" height="50" fill="var(--dia-green)"/>
  <text x="1030" y="92" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">Kernel</text>
  <text x="1030" y="106" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">Auto-Tuning</text>
  <rect x="1190" y="70" width="140" height="50" rx="4" fill="var(--dia-bg-card)" stroke="var(--dia-stroke)" stroke-width="1.6"/>
  <rect x="1190" y="70" width="3" height="50" fill="var(--dia-blue)"/>
  <text x="1260" y="92" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">Optimized Engine</text>
  <text x="1260" y="106" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">TRT Engine</text>
</svg>
</div>


### Key Optimization Techniques

| Technique | Description | Typical Speedup |
|-----------|------------|----------------|
| Layer Fusion | Merge Conv+BN+ReLU into one kernel | 1.5-2x |
| FP16 Inference | Half-precision floating point | 2-3x |
| INT8 Quantization | 8-bit integer inference | 3-5x |
| Dynamic Batching | Automatically select optimal batch size | 1.2-1.5x |

### Inference Performance Examples

Typical inference performance on Jetson Orin NX:

| Model | FP32 | FP16 | INT8 | Use Case |
|-------|------|------|------|----------|
| YOLOv8n | 45 FPS | 120 FPS | 200 FPS | Object detection |
| YOLOv8s | 25 FPS | 70 FPS | 130 FPS | Object detection |
| MobileNetV3 | 200 FPS | 500 FPS | 800 FPS | Image classification |
| PointPillars | 15 FPS | 35 FPS | 60 FPS | 3D object detection |

## Jetson GPU Specifications Comparison

| Feature | Orin Nano | Orin NX | AGX Orin |
|---------|-----------|---------|----------|
| GPU Architecture | Ampere | Ampere | Ampere |
| CUDA Cores | 1024 | 2048 | 2048 |
| Tensor Cores | 32 | 64 | 64 |
| GPU Frequency | 625 MHz | 918 MHz | 1.3 GHz |
| AI Performance (INT8) | 40 TOPS | 100 TOPS | 275 TOPS |
| Memory | 8GB shared | 8/16GB shared | 32/64GB shared |
| Power | 7-15W | 10-25W | 15-60W |

## GPU Programming Best Practices

### 1. Maximize Occupancy

Ensure enough threads to hide memory latency:

$$
\text{Occupancy} = \frac{\text{Active Warps}}{\text{Max Warps per SM}}
$$

Target occupancy > 50%.

### 2. Coalesced Memory Access

Adjacent threads access adjacent memory addresses:

```c
// Good: Coalesced access
C[threadIdx.x] = A[threadIdx.x] + B[threadIdx.x];

// Bad: Strided access
C[threadIdx.x] = A[threadIdx.x * stride];
```

### 3. Minimize CPU-GPU Data Transfers

```python
# Bad: Frequent copies
for frame in camera_stream:
    gpu_frame = frame.to('cuda')     # CPU -> GPU
    result = model(gpu_frame)         # GPU inference
    cpu_result = result.to('cpu')     # GPU -> CPU

# Good: Pipelined using CUDA Streams
stream1 = torch.cuda.Stream()
stream2 = torch.cuda.Stream()
# Transfer data on stream1 while executing inference on stream2
```

### 4. Leverage Tensor Cores

Use Tensor cores to accelerate matrix operations:

$$
D = A \times B + C \quad \text{(Matrix multiply-add)}
$$

Tensor cores complete a $4 \times 4$ matrix multiply-add in a single clock cycle.

!!! tip "Enabling Tensor Cores in PyTorch"
    ```python
    # Use FP16 automatic mixed precision
    with torch.cuda.amp.autocast():
        output = model(input)
    ```

## Robot Vision Processing Pipeline

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
  <text x="340" y="92" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">CPU Image</text>
  <text x="340" y="106" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">Decoding</text>
  <rect x="500" y="70" width="140" height="50" rx="4" fill="var(--dia-bg-card)" stroke="var(--dia-stroke)" stroke-width="1.6"/>
  <rect x="500" y="70" width="3" height="50" fill="var(--dia-blue)"/>
  <text x="570" y="92" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">GPU Preprocessing</text>
  <text x="570" y="106" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">resize/normalize</text>
  <rect x="730" y="70" width="140" height="50" rx="4" fill="var(--dia-bg-card)" stroke="var(--dia-stroke)" stroke-width="1.6"/>
  <rect x="730" y="70" width="3" height="50" fill="var(--dia-accent)"/>
  <text x="800" y="85" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">GPU Neural</text>
  <text x="800" y="99" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">Network Inference</text>
  <text x="800" y="113" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">Detection/Segmentation</text>
  <rect x="960" y="70" width="140" height="50" rx="4" fill="var(--dia-bg-card)" stroke="var(--dia-stroke)" stroke-width="1.6"/>
  <rect x="960" y="70" width="3" height="50" fill="var(--dia-green)"/>
  <text x="1030" y="85" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">GPU</text>
  <text x="1030" y="99" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">Post-processing</text>
  <text x="1030" y="113" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">NMS/Decoding</text>
  <rect x="1190" y="70" width="140" height="50" rx="4" fill="var(--dia-bg-card)" stroke="var(--dia-stroke)" stroke-width="1.6"/>
  <rect x="1190" y="70" width="3" height="50" fill="var(--dia-blue)"/>
  <text x="1260" y="85" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">CPU Result</text>
  <text x="1260" y="99" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">Publishing ROS2</text>
  <text x="1260" y="113" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">Topic</text>
</svg>
</div>


Using GStreamer + DeepStream enables a full GPU pipeline, avoiding data copies between CPU and GPU.

## Summary

1. **GPUs compensate for single-thread performance limitations through massive parallelism**
2. **The SIMT model** requires avoiding warp divergence
3. **Memory hierarchy** and **coalesced access** are critical for GPU performance
4. **TensorRT** can boost inference performance by 3-5x
5. **Minimizing CPU-GPU data transfers** is key to optimization
6. The Jetson series provides AI performance options ranging from 40 to 275 TOPS for robotics

## References

- NVIDIA CUDA Programming Guide: [https://docs.nvidia.com/cuda/](https://docs.nvidia.com/cuda/)
- NVIDIA TensorRT Documentation: [https://developer.nvidia.com/tensorrt](https://developer.nvidia.com/tensorrt)
- NVIDIA Jetson Developer Guide: [https://developer.nvidia.com/embedded/](https://developer.nvidia.com/embedded/)
- Kirk, D. B., & Hwu, W. *Programming Massively Parallel Processors*
