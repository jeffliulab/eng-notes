# FPGA — Field-Programmable Gate Array

> *FPGA 是可在 field 重新配置的硬件 — 既不是 ASIC (一次性 mask) 也不是 CPU (固定 ISA)。在低 latency, parallel, custom hardware 场景独有优势。Xilinx (AMD) + Intel (Altera) 双寡头,新兴 Lattice / Microchip。*
>
> **难度**:Advanced
> **前置知识**:数字电路, [CPU 架构](CPU架构.md)

---

## 1. FPGA 内部

```
LUT (Look-Up Table) — 实现任意 truth table
FF (Flip-Flop) — 寄存器
DSP slice — multiply-accumulate
Block RAM — SRAM 块
PLL / clock — 时钟管理
I/O — high-speed serial / parallel
```

→ 一个 FPGA 可包含数百万 LUT + 数千 DSP slices。

---

## 2. vs CPU / GPU / ASIC

| 维度 | CPU | GPU | FPGA | ASIC |
|---|---|---|---|---|
| 可程化 | ✓ | ✓ | ✓ (硬件可配) | ❌ |
| 并行度 | 中 | 极高 | 高 | 极高 |
| Latency | μs-ms | ms | ns | ns |
| Power | 100W | 300W | 20-50W | 5-50W |
| 开发难度 | 简 | 中 | 难 | 极难 |
| 成本 (NRE) | $0 | $0 | $1-50k | $1M-100M |
| 单价 | $$ | $$$ | $$$ | $ (大量) |

→ FPGA 优势:**低-中 volume 高性能定制**。

---

## 3. HDL (Hardware Description Language)

### 3.1 Verilog

```verilog
module counter (
    input clk,
    input rst,
    output reg [7:0] count
);
    always @(posedge clk) begin
        if (rst) count <= 0;
        else count <= count + 1;
    end
endmodule
```

### 3.2 VHDL

更 verbose,航空 / 国防偏好。

### 3.3 HLS (High-Level Synthesis)

C / C++ → Verilog (Xilinx Vitis HLS, Intel HLS, Catapult)。
易写难调,生成代码不一定 optimal。

### 3.4 Chisel / Spinal HDL

Scala / Kotlin → Verilog,RISC-V Rocket 用 Chisel。

---

## 4. 工具链

- **Xilinx Vivado** (AMD): primary IDE
- **Intel Quartus**: Altera FPGA
- **Yosys + nextpnr**: open-source toolchain (Lattice iCE40, ECP5)
- **GHDL / Icarus Verilog**: open simulators
- **Verilator**: 最快 simulator

---

## 5. 应用

### 5.1 High-Frequency Trading

- < 1 μs market data → order roundtrip
- FPGA 替代 Linux kernel + TCP/IP stack

### 5.2 5G / Telecom

- Software-Defined Radio (SDR)
- Baseband processing

### 5.3 AI inference

- Microsoft Project Catapult (Bing 加速)
- AWS F1 instances
- 低 latency, 高 throughput

### 5.4 视频处理

- Real-time 4K / 8K encoding
- Live broadcast equipment

### 5.5 Aerospace / Defense

- Radar signal processing
- Avionics (FAA certified versions)

### 5.6 仪器 / 测量

- 示波器, 信号分析器内部用 FPGA

---

## 6. AI Accelerator (FPGA based)

```python
# 概念:FPGA 实现矩阵乘 (8-bit fixed-point)
# Verilog 不写,但思路:
#   - 1024 个 MAC 并行
#   - INT8 quantize
#   - On-chip BRAM 缓存 weights
# 性能: 100 TOPS / Watt (vs GPU 1 TOPS/W)
```

---

## 7. SoC FPGA

- Xilinx Zynq / UltraScale+ MPSoC
- Intel Stratix 10 SoC
- ARM cortex-A + FPGA fabric 在同 die
- 主流嵌入式 + AI 平台

---

## 8. 开发流程

```
1. RTL design (Verilog/VHDL)
2. Simulation (testbench)
3. Synthesis (RTL → netlist)
4. Place & Route (netlist → device specific)
5. Timing analysis (signal 内 clock period 内到达)
6. Bitstream generation
7. Program FPGA (JTAG)
```

---

## 9. Common Pitfalls

### 9.1 Verilog 不是软件

并行执行,没"行先后"概念 (always block 同时跑)。

### 9.2 Timing closure

设计 frequency 太高 → 信号来不及 propagate → 不能 close timing。

### 9.3 Resource utilization

LUT / FF / DSP / BRAM 各 limit;一种 bottleneck 限制设计。

### 9.4 Clock domain crossing

异步 clocks → 需 synchronizer 防 metastability。

### 9.5 Debug 难

vs CPU print debug,FPGA 需 ChipScope / SignalTap signal probe。

---

## 10. Related Concepts

- **同节**:[CPU 架构](CPU架构.md)、[RISC-V](RISC_V.md)、[GPU 与并行计算](GPU与并行计算.md)
- **应用**:[Sensors](../05_Sensors_Perception/index.md)

---

## References

1. **Brown, S. & Vranesic, Z.** *Fundamentals of Digital Logic with Verilog Design*. 3rd ed., 2014.
2. **Trimberger, S. M.** *Field-Programmable Gate Array Technology*. Springer, 2012.
3. **Xilinx UG949 — Vivado Design Suite User Guide**.
4. **Project IceStorm** (open-source iCE40 toolchain).
