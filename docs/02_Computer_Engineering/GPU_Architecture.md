# GPU 架构 (GPU Architecture)

> *GPU 1999 NVIDIA GeForce 256 首"GPU" 商标。CPU 是 latency-optimized few cores,GPU 是 throughput-optimized 10000+ cores。CUDA (2007)、Tensor Core (Volta 2017)、HBM、NVLink 是关键。AI revolution 由 GPU 推动。Hopper H100 (80B trans, 80 GB HBM3) 是 LLM 训练标配。Blackwell B200 (208B trans, 192 GB) 是当代。AMD MI300、Google TPU、Cerebras WSE、华为昇腾是替代。*
>
> **难度**:Advanced
> **前置知识**:CPU 架构、并行编程

---

## 1. GPU vs CPU

| 维度 | CPU | GPU |
|---|---|---|
| Cores | 8-128 | 10000-200000 |
| Clock | 3-5 GHz | 1-2 GHz |
| Cache / core | 大 | 小 |
| Latency | 低 | 高 |
| Throughput | 中 | 极高 |
| 控制单元 | 复杂 | 简单 |
| Branch prediction | 强 | 弱 |
| 适合 | sequential, branchy | parallel SIMD |

---

## 2. GPU 架构层级 (NVIDIA)

```
GPU
 ├── GPC (Graphics Processing Cluster) × 多
 │    ├── SM (Streaming Multiprocessor) × 多
 │    │    ├── CUDA Core × 64-128
 │    │    ├── Tensor Core × 4-8 (per SM, since Volta)
 │    │    ├── RT Core (since Turing, ray tracing)
 │    │    ├── Warp Scheduler × 4
 │    │    ├── L1 cache + Shared memory (combined)
 │    │    └── Register file (256 KB)
 ├── L2 cache (shared, 40-50 MB Hopper)
 ├── HBM (16-80 GB)
 └── NVLink / PCIe interconnect
```

H100: 132 SM × 128 cores = 16,896 CUDA cores + 528 Tensor cores。

---

## 3. SIMT 模型

- **SIMT** = Single Instruction, Multiple Threads
- Warp = 32 threads,同时执行同 instruction
- 不同 thread 数据不同
- Branch divergence → 性能损失

---

## 4. Memory Hierarchy

| 层级 | 延迟 | 带宽 |
|---|---|---|
| Register | 1 cycle | 极高 |
| Shared memory / L1 | 20-30 cycles | 高 |
| L2 cache | 200 cycles | 中 |
| HBM | 400-800 cycles | 3 TB/s (H100) |
| Host (PCIe) | 数千 cycles | 64 GB/s (PCIe 5) |

→ 算法必 maximize HBM 数据 reuse。

---

## 5. Tensor Core

- Volta (V100, 2017) 引入
- 一 cycle 4×4×4 matrix multiply-accumulate (FP16, ACC FP32)
- Ampere (A100, 2020): TF32、BF16
- Hopper (H100): FP8、Transformer Engine
- Blackwell (B200): FP4 推理

---

## 6. CUDA Programming

```cpp
__global__ void add_kernel(float *a, float *b, float *c, int N) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < N) c[i] = a[i] + b[i];
}

int main() {
    int N = 1<<20;
    float *d_a, *d_b, *d_c;
    cudaMalloc(&d_a, N*sizeof(float));
    cudaMalloc(&d_b, N*sizeof(float));
    cudaMalloc(&d_c, N*sizeof(float));
    
    int threads = 256;
    int blocks = (N + threads - 1) / threads;
    add_kernel<<<blocks, threads>>>(d_a, d_b, d_c, N);
    cudaDeviceSynchronize();
}
```

---

## 7. NVIDIA GPU 世代

| Arch | 年 | 代表 | FP32 TFLOPs | 备注 |
|---|---|---|---|---|
| Kepler | 2012 | K80 | 8.7 | first big AI |
| Maxwell | 2014 | M40 | 7 | |
| Pascal | 2016 | P100 | 10.6 | HBM2 |
| Volta | 2017 | V100 | 15.7 | Tensor Core 1 |
| Turing | 2018 | T4 / RTX 20 | 8.1 | RT Core |
| Ampere | 2020 | A100 | 19.5 | TF32 |
| Hopper | 2022 | H100 | 67 (FP8 ~ 4000 TOPS) | Transformer Engine |
| Blackwell | 2024 | B200 | 80 (FP4 ~ 20 PFLOPs) | NVLink Switch |

---

## 8. AMD GPU + Cuda 替代

- **AMD MI300X** (2023): 192 GB HBM3,与 H100 性能可比
- **AMD ROCm**: HIP API (CUDA-like)
- **Intel Ponte Vecchio / Gaudi** (Habana)
- **Google TPU v5p / Trillium** (Ironwood)
- **Cerebras WSE-3** (4 trillion 晶体管,wafer-scale)
- **Graphcore IPU**
- **华为昇腾 Ascend 910B**

---

## 9. PyTorch GPU 使用

```python
import torch

x = torch.randn(10000, 10000, device='cuda')
y = torch.randn(10000, 10000, device='cuda')
z = x @ y  # GPU matmul
print(z.device, z.shape)

# Mixed precision
with torch.amp.autocast('cuda'):
    z = x @ y
```

---

## 10. AI 训练 vs 推理

- **Training**: FP32/BF16,memory + compute bound,multi-GPU + NVLink
- **Inference**: FP16/INT8/FP8/FP4,latency 关键,single GPU 多
- **Serving**: vLLM、TensorRT-LLM、ONNX Runtime

---

## 11. 常见问题

### 11.1 GPU 慢于 CPU

小 batch / branchy code → kernel launch overhead 主导。GPU 适合大 parallel work。

### 11.2 OOM

模型 + 梯度 + optimizer state + activations。LLM 训练:模型 × 16-20 才够。

### 11.3 PCIe 瓶颈

CPU↔GPU 传输慢;尽量 host data 留 GPU。

### 11.4 Branch Divergence

if/else in warp → 串行化。Re-organize 数据避。

### 11.5 Multi-GPU 不自动 fast

需 NCCL、proper sharding (DDP、FSDP、ZeRO、Megatron-LM)。

---

## 12. Related Concepts

- **同节**:[RISC-V](RISC_V.md)、[FPGA](FPGA.md)
- **嵌入式**:[ARM Cortex-M](../03_Embedded_Systems/ARM_Cortex_M.md)
- **AI**: PyTorch、CUDA — https://jeffliulab.github.io/ai-notes/

---

## References

1. **NVIDIA** *Hopper Architecture White Paper*. 2022.
2. **NVIDIA** *Blackwell Architecture White Paper*. 2024.
3. **Patterson, D. A. & Hennessy, J. L.** *Computer Architecture: A Quantitative Approach*. 6th ed., 2017.
4. **Kirk, D. B. & Hwu, W. W.** *Programming Massively Parallel Processors*. 4th ed., 2022.
