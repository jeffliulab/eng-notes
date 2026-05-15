# GPU Architecture

> *NVIDIA's 1999 GeForce 256 introduced the "GPU" trademark. CPUs are latency-optimized few-core; GPUs are throughput-optimized 10,000+ cores. CUDA (2007), Tensor Core (Volta 2017), HBM, NVLink are key. The AI revolution was driven by GPUs. Hopper H100 (80B trans, 80 GB HBM3) is LLM training standard. Blackwell B200 (208B trans, 192 GB) is current. AMD MI300, Google TPU, Cerebras WSE, Huawei Ascend are alternatives.*
>
> **Difficulty**: Advanced
> **Prerequisites**: CPU architecture, parallel programming

---

## 1. GPU vs CPU

| Dimension | CPU | GPU |
|---|---|---|
| Cores | 8-128 | 10000-200000 |
| Clock | 3-5 GHz | 1-2 GHz |
| Cache / core | Large | Small |
| Latency | Low | High |
| Throughput | Medium | Extreme |
| Control unit | Complex | Simple |
| Branch prediction | Strong | Weak |
| Best for | Sequential, branchy | Parallel SIMD |

---

## 2. GPU Hierarchy (NVIDIA)

```
GPU
 ├── GPC (Graphics Processing Cluster) × many
 │    ├── SM (Streaming Multiprocessor) × many
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

H100: 132 SM × 128 cores = 16,896 CUDA cores + 528 Tensor cores.

---

## 3. SIMT Model

- **SIMT** = Single Instruction, Multiple Threads
- Warp = 32 threads, execute same instruction
- Different data per thread
- Branch divergence → performance loss

---

## 4. Memory Hierarchy

| Level | Latency | Bandwidth |
|---|---|---|
| Register | 1 cycle | Extreme |
| Shared memory / L1 | 20-30 cycles | High |
| L2 cache | 200 cycles | Medium |
| HBM | 400-800 cycles | 3 TB/s (H100) |
| Host (PCIe) | Thousands of cycles | 64 GB/s (PCIe 5) |

→ Algorithms must maximize HBM data reuse.

---

## 5. Tensor Core

- Introduced in Volta (V100, 2017)
- One cycle 4×4×4 matrix multiply-accumulate (FP16, FP32 acc)
- Ampere (A100, 2020): TF32, BF16
- Hopper (H100): FP8, Transformer Engine
- Blackwell (B200): FP4 inference

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

## 7. NVIDIA GPU Generations

| Arch | Year | Flagship | FP32 TFLOPs | Note |
|---|---|---|---|---|
| Kepler | 2012 | K80 | 8.7 | First big AI |
| Maxwell | 2014 | M40 | 7 | |
| Pascal | 2016 | P100 | 10.6 | HBM2 |
| Volta | 2017 | V100 | 15.7 | Tensor Core 1 |
| Turing | 2018 | T4 / RTX 20 | 8.1 | RT Core |
| Ampere | 2020 | A100 | 19.5 | TF32 |
| Hopper | 2022 | H100 | 67 (FP8 ~ 4000 TOPS) | Transformer Engine |
| Blackwell | 2024 | B200 | 80 (FP4 ~ 20 PFLOPs) | NVLink Switch |

---

## 8. AMD GPU + CUDA Alternatives

- **AMD MI300X** (2023): 192 GB HBM3, comparable to H100
- **AMD ROCm**: HIP API (CUDA-like)
- **Intel Ponte Vecchio / Gaudi** (Habana)
- **Google TPU v5p / Trillium** (Ironwood)
- **Cerebras WSE-3** (4 trillion transistors, wafer-scale)
- **Graphcore IPU**
- **Huawei Ascend 910B**

---

## 9. PyTorch GPU Usage

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

## 10. AI Training vs Inference

- **Training**: FP32/BF16, memory + compute bound, multi-GPU + NVLink
- **Inference**: FP16/INT8/FP8/FP4, latency-critical, often single GPU
- **Serving**: vLLM, TensorRT-LLM, ONNX Runtime

---

## 11. Common Pitfalls

### 11.1 GPU Slower than CPU

Small batch / branchy code → kernel launch overhead dominates. GPU suits large parallel work.

### 11.2 OOM

Model + gradients + optimizer state + activations. LLM training: model × 16-20 needed.

### 11.3 PCIe Bottleneck

CPU↔GPU transfer slow; keep host data on GPU.

### 11.4 Branch Divergence

if/else in warp → serialized. Reorganize data to avoid.

### 11.5 Multi-GPU Not Auto-Fast

Need NCCL, proper sharding (DDP, FSDP, ZeRO, Megatron-LM).

---

## 12. Related Concepts

- **Same section**: [RISC-V](RISC_V.en.md), [FPGA](FPGA.en.md)
- **Embedded**: [ARM Cortex-M](../03_Embedded_Systems/ARM_Cortex_M.en.md)
- **AI**: PyTorch, CUDA — https://jeffliulab.github.io/ai-notes/

---

## References

1. **NVIDIA** *Hopper Architecture White Paper*. 2022.
2. **NVIDIA** *Blackwell Architecture White Paper*. 2024.
3. **Patterson, D. A. & Hennessy, J. L.** *Computer Architecture: A Quantitative Approach*. 6th ed., 2017.
4. **Kirk, D. B. & Hwu, W. W.** *Programming Massively Parallel Processors*. 4th ed., 2022.
