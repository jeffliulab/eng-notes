# RISC-V — 开源 ISA 革命

> *RISC-V 是 2010 Berkeley 开发的**开源 ISA**。无许可费、模块化、设计简洁 — 已成嵌入式 / IoT / AI accelerator 标配。SiFive, Andes, 阿里平头哥, 兆易等众多 vendor。Linus Torvalds 评:"将来 CPU 都会用 RISC-V"。*
>
> **难度**:Intermediate
> **前置知识**:[CPU 架构](CPU架构.md)

---

## 1. 为什么 RISC-V 重要

- **开源**: Apache 2 license — 无 royalty
- **模块化**: 基础 ISA (RV32I/RV64I) + extensions (M, A, F, D, C, V, B)
- **干净设计**: 47 base instructions, 不带 legacy 包袱
- **academic foundation**: David Patterson / Krste Asanovic 设计
- **生态成熟**: GCC / LLVM / Linux / FreeRTOS 全支持

---

## 2. ISA 模块

| 模块 | 描述 |
|---|---|
| **I** | Base integer (32 or 64 bit) |
| **M** | Multiply / divide |
| **A** | Atomic |
| **F** | Single-precision float |
| **D** | Double-precision float |
| **C** | Compressed (16-bit instructions) |
| **V** | Vector (SIMD) |
| **B** | Bit manipulation |
| **K** | Crypto |

常见组合:RV32IMC (嵌入式), RV64GC = IMAFD + C (general purpose)。

---

## 3. 寄存器集

- 32 个 GPR: x0 (zero) - x31
- ABI alias: ra (return addr), sp (stack ptr), gp, tp, t0-t6 (temp), s0-s11 (saved), a0-a7 (args)
- 32 个 FPR (若 F/D 扩展): f0-f31
- PC (program counter)

vs x86 8 GPR + 复杂 SIMD 寄存器,RISC-V 更 uniform。

---

## 4. 主要 vendor / 芯片

- **SiFive** (Berkeley spinoff): U54, U74, P870
- **Andes** (Taiwan): NX27V
- **阿里平头哥**: 玄铁 C910 (2019), 用 OpenHarmony
- **兆易创新**: GD32V (RV32IMC, $1 MCU)
- **Western Digital**: SweRV (open-source)
- **NVIDIA Falcon → RISC-V** migration
- **Intel Horse Creek** (2023): server-class RV

---

## 5. 应用

- **MCU**: GD32V, ESP32-C3 (低端)
- **AI accelerator**: NVIDIA SoC, Tesla AI chip
- **数据中心**: Alibaba Hanguang 800, Tenstorrent
- **手机** (实验): RISC-V 应用尚少
- **教学**: Berkeley CS61C, MIT 课程

---

## 6. vs x86 / ARM

| 维度 | x86 | ARM | RISC-V |
|---|---|---|---|
| License | Intel/AMD 专有 | ARM 收费 | 开源 |
| 复杂度 | 高 (CISC + legacy) | 中 | 简 |
| Power eff. | 中 | 高 | 高 |
| 生态 | PC/server 主导 | 手机/嵌入式 主导 | 兴起中 |
| 性能 | 极高 (single-thread) | 高 | 中-高 (设计依赖) |

---

## 7. PyTorch / C — 简单 RISC-V 汇编

```assembly
# Add two numbers
.text
main:
    li a0, 5        # load immediate 5 to a0
    li a1, 7        # load 7 to a1
    add a2, a0, a1  # a2 = a0 + a1 (= 12)
    
    # Exit syscall
    li a7, 93       # exit syscall number
    li a0, 0        # exit code 0
    ecall
```

C → RISC-V 编译:`riscv64-unknown-elf-gcc main.c -o main`。

---

## 8. 工具链

- **GCC**: `riscv64-unknown-elf-gcc`
- **LLVM**: `clang --target=riscv64`
- **QEMU**: `qemu-system-riscv64`
- **Spike**: official RISC-V simulator
- **Boards**: SiFive HiFive Unmatched, BeagleV, Allwinner D1

---

## 9. AI on RISC-V

- Vector extension (V) → SIMD for ML
- Custom extensions for ML primitives (BF16, INT4)
- 与 GPU/TPU 比仍弱,但 edge AI 实用

---

## 10. Common Pitfalls

### 10.1 ISA fragmentation

许多 custom extensions → 生态碎片化风险。RISC-V Foundation 标准化 effort。

### 10.2 性能 vs Intel / Apple

Mature RISC-V 仍落后 Apple M-series 性能。

### 10.3 软件兼容性

旧 Windows / proprietary software 没有 RISC-V port。

### 10.4 Compiler maturity

GCC / LLVM 在 RISC-V 上 optimization 不如 x86 / ARM 成熟。

### 10.5 China / 美国 geopolitics

地缘政治可能影响 RISC-V 全球生态。

---

## 11. Related Concepts

- **同节**:[CPU 架构](CPU架构.md)、[GPU 与并行计算](GPU与并行计算.md)、[嵌入式系统](嵌入式系统.md)
- **嵌入式**:[ARM Cortex-M](../03_Embedded_Systems/ARM_Cortex_M.md)

---

## References

1. **Patterson, D. A. & Hennessy, J. L.** *Computer Organization and Design: RISC-V Edition*. 2nd ed., 2020.
2. **Waterman, A. & Asanovic, K.** *The RISC-V Instruction Set Manual*. 2019.
3. **RISC-V International** — https://riscv.org/
4. **SiFive, Andes, T-Head** documentation.
