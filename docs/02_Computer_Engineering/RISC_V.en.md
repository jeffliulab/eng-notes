# RISC-V — Open-Source ISA Revolution

> *RISC-V is an **open-source ISA** developed at Berkeley in 2010. No license fee, modular, clean design — already standard in embedded / IoT / AI accelerators. SiFive, Andes, T-Head (Alibaba), and many vendors. Linus Torvalds: "Eventually all CPUs will be RISC-V".*
>
> **Difficulty**: Intermediate
> **Prerequisites**: [CPU Architecture](CPU架构.en.md)

---

## 1. Why RISC-V Matters

- **Open source**: Apache 2 license — no royalty
- **Modular**: base ISA (RV32I/RV64I) + extensions (M, A, F, D, C, V, B)
- **Clean design**: 47 base instructions, no legacy baggage
- **Academic foundation**: David Patterson / Krste Asanovic
- **Mature ecosystem**: GCC / LLVM / Linux / FreeRTOS support

---

## 2. ISA Modules

| Module | Description |
|---|---|
| **I** | Base integer (32 or 64 bit) |
| **M** | Multiply / divide |
| **A** | Atomic |
| **F** | Single-precision float |
| **D** | Double-precision float |
| **C** | Compressed (16-bit) |
| **V** | Vector (SIMD) |
| **B** | Bit manipulation |
| **K** | Crypto |

Common combinations: RV32IMC (embedded), RV64GC = IMAFD + C (general purpose).

---

## 3. Register Set

- 32 GPRs: x0 (zero) - x31
- ABI aliases: ra, sp, gp, tp, t0-t6, s0-s11, a0-a7
- 32 FPRs (if F/D): f0-f31
- PC

vs x86's 8 GPRs + complex SIMD, RISC-V is more uniform.

---

## 4. Major Vendors / Chips

- **SiFive** (Berkeley spinoff): U54, U74, P870
- **Andes** (Taiwan): NX27V
- **T-Head (Alibaba)**: XuanTie C910 (2019), used in OpenHarmony
- **Gigadevice**: GD32V (RV32IMC, $1 MCU)
- **Western Digital**: SweRV (open-source)
- **NVIDIA Falcon → RISC-V** migration
- **Intel Horse Creek** (2023): server-class RV

---

## 5. Applications

- **MCU**: GD32V, ESP32-C3 (low-end)
- **AI accelerator**: NVIDIA SoC, Tesla AI chip
- **Data center**: Alibaba Hanguang 800, Tenstorrent
- **Mobile** (experimental): RISC-V applications still rare
- **Teaching**: Berkeley CS61C, MIT courses

---

## 6. vs x86 / ARM

| Aspect | x86 | ARM | RISC-V |
|---|---|---|---|
| License | Intel/AMD proprietary | ARM fee | Open |
| Complexity | High (CISC + legacy) | Medium | Simple |
| Power eff. | Medium | High | High |
| Ecosystem | PC/server dominant | Mobile/embedded dominant | Rising |
| Performance | Very high (single-thread) | High | Medium-high (design dependent) |

---

## 7. C — Simple RISC-V Assembly

```assembly
.text
main:
    li a0, 5
    li a1, 7
    add a2, a0, a1  # a2 = 12
    
    li a7, 93
    li a0, 0
    ecall
```

C → RISC-V: `riscv64-unknown-elf-gcc main.c -o main`.

---

## 8. Toolchain

- **GCC**: `riscv64-unknown-elf-gcc`
- **LLVM**: `clang --target=riscv64`
- **QEMU**: `qemu-system-riscv64`
- **Spike**: official RISC-V simulator
- **Boards**: SiFive HiFive Unmatched, BeagleV, Allwinner D1

---

## 9. AI on RISC-V

- Vector extension (V) → SIMD for ML
- Custom extensions for ML primitives (BF16, INT4)
- Still weaker than GPU/TPU, but practical for edge AI

---

## 10. Common Pitfalls

### 10.1 ISA Fragmentation

Many custom extensions → ecosystem fragmentation risk. RISC-V Foundation standardization efforts.

### 10.2 Performance vs Intel / Apple

Mature RISC-V still lags Apple M-series performance.

### 10.3 Software Compatibility

Old Windows / proprietary software has no RISC-V port.

### 10.4 Compiler Maturity

GCC / LLVM on RISC-V not as optimized as x86 / ARM.

### 10.5 China / US Geopolitics

Geopolitics may affect RISC-V global ecosystem.

---

## 11. Related Concepts

- **Same section**: [CPU Architecture](CPU架构.en.md), [GPU & Parallel Computing](GPU与并行计算.en.md), [Embedded Systems](嵌入式系统.en.md)
- **Embedded**: [ARM Cortex-M](../03_Embedded_Systems/ARM_Cortex_M.en.md)

---

## References

1. **Patterson, D. A. & Hennessy, J. L.** *Computer Organization and Design: RISC-V Edition*. 2nd ed., 2020.
2. **Waterman, A. & Asanovic, K.** *The RISC-V Instruction Set Manual*. 2019.
3. **RISC-V International** — https://riscv.org/
4. **SiFive, Andes, T-Head** documentation.
