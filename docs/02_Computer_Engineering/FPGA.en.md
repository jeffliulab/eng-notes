# FPGA — Field-Programmable Gate Array

> *FPGA is hardware reconfigurable in the field — not ASIC (one-time mask) or CPU (fixed ISA). Unique advantage in low-latency, parallel, custom hardware scenarios. Xilinx (AMD) + Intel (Altera) duopoly; emerging Lattice / Microchip.*
>
> **Difficulty**: Advanced
> **Prerequisites**: digital logic, [CPU Architecture](CPU架构.en.md)

---

## 1. FPGA Internals

```
LUT (Look-Up Table) — implements arbitrary truth table
FF (Flip-Flop) — registers
DSP slice — multiply-accumulate
Block RAM — SRAM blocks
PLL / clock — clock management
I/O — high-speed serial / parallel
```

→ An FPGA may contain millions of LUTs + thousands of DSP slices.

---

## 2. vs CPU / GPU / ASIC

| Aspect | CPU | GPU | FPGA | ASIC |
|---|---|---|---|---|
| Programmable | ✓ | ✓ | ✓ (hardware) | ❌ |
| Parallelism | Medium | Very high | High | Very high |
| Latency | μs-ms | ms | ns | ns |
| Power | 100W | 300W | 20-50W | 5-50W |
| Dev difficulty | Easy | Medium | Hard | Very hard |
| Cost (NRE) | $0 | $0 | $1-50k | $1M-100M |
| Unit price | $$ | $$$ | $$$ | $ (volume) |

→ FPGA advantage: **low-mid volume high-performance custom**.

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

More verbose; aerospace / defense preferred.

### 3.3 HLS (High-Level Synthesis)

C / C++ → Verilog (Xilinx Vitis HLS, Intel HLS, Catapult).
Easy to write but hard to debug; generated code not always optimal.

### 3.4 Chisel / Spinal HDL

Scala / Kotlin → Verilog; RISC-V Rocket uses Chisel.

---

## 4. Toolchain

- **Xilinx Vivado** (AMD): primary IDE
- **Intel Quartus**: Altera FPGA
- **Yosys + nextpnr**: open-source toolchain (Lattice iCE40, ECP5)
- **GHDL / Icarus Verilog**: open simulators
- **Verilator**: fastest simulator

---

## 5. Applications

### 5.1 High-Frequency Trading

- < 1 μs market data → order roundtrip
- FPGA replaces Linux kernel + TCP/IP stack

### 5.2 5G / Telecom

- Software-Defined Radio (SDR)
- Baseband processing

### 5.3 AI Inference

- Microsoft Project Catapult (Bing acceleration)
- AWS F1 instances
- Low latency, high throughput

### 5.4 Video Processing

- Real-time 4K / 8K encoding
- Live broadcast equipment

### 5.5 Aerospace / Defense

- Radar signal processing
- Avionics (FAA certified versions)

### 5.6 Instrumentation

- Oscilloscopes, signal analyzers use FPGA internally

---

## 6. AI Accelerator (FPGA-based)

```python
# Concept: FPGA implementing matrix mul (8-bit fixed-point)
# Not Verilog, but conceptually:
#   - 1024 parallel MACs
#   - INT8 quantize
#   - On-chip BRAM caches weights
# Performance: 100 TOPS / Watt (vs GPU 1 TOPS/W)
```

---

## 7. SoC FPGA

- Xilinx Zynq / UltraScale+ MPSoC
- Intel Stratix 10 SoC
- ARM Cortex-A + FPGA fabric on same die
- Mainstream embedded + AI platform

---

## 8. Development Flow

```
1. RTL design (Verilog/VHDL)
2. Simulation (testbench)
3. Synthesis (RTL → netlist)
4. Place & Route (netlist → device specific)
5. Timing analysis (signals arrive within clock period)
6. Bitstream generation
7. Program FPGA (JTAG)
```

---

## 9. Common Pitfalls

### 9.1 Verilog Isn't Software

Parallel execution; no "line ordering" concept (always blocks run simultaneously).

### 9.2 Timing Closure

Design frequency too high → signals can't propagate → can't close timing.

### 9.3 Resource Utilization

LUT / FF / DSP / BRAM each have limits; one bottleneck constrains design.

### 9.4 Clock Domain Crossing

Async clocks → need synchronizer for metastability.

### 9.5 Debug Hard

vs CPU print debug, FPGA needs ChipScope / SignalTap signal probe.

---

## 10. Related Concepts

- **Same section**: [CPU Architecture](CPU架构.en.md), [RISC-V](RISC_V.en.md), [GPU & Parallel Computing](GPU与并行计算.en.md)

---

## References

1. **Brown, S. & Vranesic, Z.** *Fundamentals of Digital Logic with Verilog Design*. 3rd ed., 2014.
2. **Trimberger, S. M.** *Field-Programmable Gate Array Technology*. Springer, 2012.
3. **Xilinx UG949 — Vivado Design Suite User Guide**.
4. **Project IceStorm** (open-source iCE40 toolchain).
