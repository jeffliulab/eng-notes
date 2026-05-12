# CPU Architecture

## Overview

The CPU (Central Processing Unit) is the core computing engine of a robot's brain. Understanding CPU architecture helps in selecting the right processor platform, optimizing program performance, and diagnosing system bottlenecks.

## Von Neumann vs. Harvard Architecture

### Von Neumann Architecture

Instructions and data share the same memory and bus:

```
+-------+     +------+     +--------+
|  CPU  |<--->| Bus  |<--->| Memory |
+-------+     +------+     +--------+
                              Instr+Data
```

- **Advantages**: Simple structure, high flexibility
- **Disadvantages**: Instructions and data cannot be accessed simultaneously (Von Neumann bottleneck)
- **Examples**: x86 PCs, most general-purpose processors

### Harvard Architecture

Instructions and data use separate memories and buses:

```
+-------+     +----------------+     +------------------+
|       |<--->| Instruction Bus|<--->| Instruction Memory|
|  CPU  |     +----------------+     +------------------+
|       |<--->| Data Bus       |<--->| Data Memory       |
+-------+     +----------------+     +------------------+
```

- **Advantages**: Instruction and data can be accessed in parallel, doubling bandwidth
- **Disadvantages**: More complex hardware
- **Examples**: STM32 and other MCUs (internally use Harvard architecture)

### Modified Harvard Architecture

Modern processors typically use a **Modified Harvard Architecture**:

- Separate L1 caches (I-Cache + D-Cache) -- Harvard characteristics
- Unified L2/L3 cache and main memory -- Von Neumann characteristics
- ARM Cortex-A series is a typical modified Harvard architecture

## Instruction Pipeline

### Classic Five-Stage Pipeline

A pipeline decomposes instruction execution into multiple stages, allowing multiple instructions to be in different stages simultaneously:

| Stage | Abbreviation | Function |
|-------|-------------|----------|
| Instruction Fetch | IF | Fetch instruction from memory |
| Instruction Decode | ID | Parse instruction, read registers |
| Execute | EX | ALU operation or address calculation |
| Memory Access | MEM | Read/write data memory |
| Write Back | WB | Write result back to register |

```
Clock cycle:  1    2    3    4    5    6    7    8
Instr 1:     IF   ID   EX  MEM   WB
Instr 2:          IF   ID   EX  MEM   WB
Instr 3:               IF   ID   EX  MEM   WB
Instr 4:                    IF   ID   EX  MEM   WB
```

Ideally, an $n$-stage pipeline in steady state has a **throughput** of:

$$
\text{Throughput} = \frac{1}{T_{\text{stage}}}
$$

While the non-pipelined throughput is $\frac{1}{n \cdot T_{\text{stage}}}$, giving a theoretical speedup of $n$.

### Pipeline Hazards

In practice, pipelines encounter three types of hazards:

**1. Data Hazard**

A subsequent instruction depends on the result of a preceding instruction:

```
ADD R1, R2, R3   ; R1 = R2 + R3
SUB R4, R1, R5   ; Needs the result of R1, but R1 has not been written back yet
```

Solution: **Data Forwarding/Bypassing**

**2. Control Hazard**

A branch instruction changes the program flow:

```
BEQ R1, R2, LABEL  ; If R1==R2 then branch
ADD R3, R4, R5      ; Should this instruction execute?
```

Solution: **Branch Prediction**

**3. Structural Hazard**

Hardware resource conflicts (e.g., two instructions need memory access simultaneously).

Solution: Add hardware resources (e.g., separate I-Cache and D-Cache)

## Cache Hierarchy

### Memory Hierarchy

$$
\text{Access Time}: \text{Registers} < \text{L1} < \text{L2} < \text{L3} < \text{DRAM} < \text{SSD} < \text{HDD}
$$

| Level | Typical Size | Typical Latency | Bandwidth |
|-------|-------------|----------------|-----------|
| Registers | ~1KB | <1ns | - |
| L1 Cache | 32-64KB | 1-2ns | ~500GB/s |
| L2 Cache | 256KB-1MB | 3-10ns | ~200GB/s |
| L3 Cache | 2-32MB | 10-30ns | ~100GB/s |
| DRAM | 4-32GB | 50-100ns | ~50GB/s |
| SSD | 128GB-2TB | ~100us | ~3GB/s |

### Cache Hit Rate

Cache performance depends on the **hit rate**:

$$
T_{\text{avg}} = T_{\text{hit}} + (1 - h) \times T_{\text{miss}}
$$

Where $h$ is the hit rate, $T_{\text{hit}}$ is the cache hit latency, and $T_{\text{miss}}$ is the additional latency on a cache miss.

!!! example "Impact of Cache on Robotics"
    During image processing, scanning row-by-row (row-major) is more cache-friendly than scanning column-by-column, because images are stored in row-major order in memory. Exploiting this **spatial locality** can significantly improve processing speed.

### Cache Mapping Strategies

- **Direct Mapped**: Each address maps to exactly one cache line
- **Fully Associative**: Each address can map to any cache line
- **Set Associative**: A compromise -- N-way set associative

## x86 vs. ARM vs. RISC-V

### Instruction Set Comparison

| Feature | x86-64 | ARM (AArch64) | RISC-V |
|---------|--------|---------------|--------|
| Type | CISC | RISC | RISC |
| Instruction Length | Variable (1-15 bytes) | Fixed (4 bytes) | Fixed (4 bytes) |
| Register Count | 16 general-purpose | 31 general-purpose | 32 general-purpose |
| Instruction Count | ~1500+ | ~1000 | ~50 (base) |
| Power Efficiency | Low | High | High |
| Ecosystem | Most mature | Mature on mobile | Rapidly growing |
| Licensing Model | Intel/AMD proprietary | ARM licensing | Open-source, free |

### ARM in Robotics

ARM processors dominate robotics due to their high energy efficiency:

**Cortex-A Series (Application Processors)**:

| Processor | Core | Frequency | Features | Application Platform |
|-----------|------|-----------|----------|---------------------|
| Cortex-A55 | ARMv8.2 | 1.8GHz | High-efficiency core | Low-power SoCs |
| Cortex-A76 | ARMv8.2 | 3.0GHz | High-performance core | Raspberry Pi 5 |
| Cortex-A78AE | ARMv8.2 | 2.2GHz | Automotive safety grade | Jetson Orin series |

**Cortex-M Series (Microcontrollers)**:

| Processor | Architecture | Frequency | Features | Typical Chip |
|-----------|-------------|-----------|----------|-------------|
| Cortex-M0+ | ARMv6-M | 48MHz | Lowest power | STM32L0 |
| Cortex-M4 | ARMv7E-M | 168MHz | DSP+FPU | STM32F4 |
| Cortex-M7 | ARMv7E-M | 480MHz | Double-precision FPU | STM32H7 |
| Cortex-M33 | ARMv8-M | 160MHz | TrustZone security | STM32U5 |

### The Potential of RISC-V

RISC-V, as an open-source ISA, is gaining attention in the embedded and robotics domains:

- **Modular design**: Base integer instruction set (I) + optional extensions (M/A/F/D/C/V)
- **No licensing fees**: Reduces chip costs
- **Customizable**: Custom instructions can be added to accelerate specific tasks
- **Representative chips**: ESP32-C3, StarFive JH7110

## Performance Analysis

### CPI (Cycles Per Instruction)

$$
\text{CPI} = \frac{\text{Total Clock Cycles}}{\text{Total Instructions}}
$$

Weighted CPI for different instruction categories:

$$
\text{CPI}_{\text{avg}} = \sum_{i=1}^{n} \text{CPI}_i \times f_i
$$

Where $f_i$ is the frequency proportion of the $i$-th instruction class.

### Amdahl's Law

When optimizing a portion of a system, the overall speedup is:

$$
S = \frac{1}{(1-P) + \frac{P}{N}}
$$

Where:

- $P$ = fraction that can be parallelized
- $N$ = number of parallel processing units
- $S$ = overall speedup

!!! example "Amdahl's Law Example"
    If 80% of a program can be parallelized ($P=0.8$), using 4 cores ($N=4$):
    
    $$S = \frac{1}{(1-0.8) + \frac{0.8}{4}} = \frac{1}{0.2 + 0.2} = 2.5$$
    
    Even with infinitely many cores:
    
    $$S_{\max} = \frac{1}{1-P} = \frac{1}{0.2} = 5$$
    
    The serial portion determines the upper bound on speedup.

### Practical Example: Robot Path Planning

Suppose a path planning algorithm has:

- A* search (serial): 60% of computation time
- Collision detection (parallelizable): 40% of computation time

On a Jetson Orin (8-core A78AE + 2048 CUDA cores):

$$
S_{\text{CPU}} = \frac{1}{0.6 + \frac{0.4}{8}} = \frac{1}{0.65} \approx 1.54
$$

Even if collision detection is fully parallelized on the GPU:

$$
S_{\text{GPU}} = \frac{1}{0.6 + \frac{0.4}{2048}} \approx \frac{1}{0.6002} \approx 1.67
$$

The key bottleneck lies in the serial A* search portion.

## Processor Selection Guide

<div class="diagram">
<svg viewBox="0 0 560 720" xmlns="http://www.w3.org/2000/svg">
  <defs><marker id="arr-m0" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="var(--dia-stroke)"/></marker></defs>
  
  <line x1="110" y1="120" x2="280" y2="630" stroke="var(--dia-stroke)" stroke-width="1.5" marker-end="url(#arr-m0)"/>
  <rect x="40" y="70" width="140" height="50" rx="4" fill="var(--dia-bg-card)" stroke="var(--dia-stroke)" stroke-width="1.6"/>
  <rect x="40" y="70" width="3" height="50" fill="var(--dia-accent)"/>
  <text x="110" y="92" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">Robot Task</text>
  <text x="110" y="106" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">Requirements</text>
  <rect x="210" y="630" width="140" height="50" rx="4" fill="var(--dia-bg-card)" stroke="var(--dia-stroke)" stroke-width="1.6"/>
  <rect x="210" y="630" width="3" height="50" fill="var(--dia-green)"/>
  <text x="280" y="652" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">Deep learning</text>
  <text x="280" y="666" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">needed?</text>
  <rect x="210" y="70" width="140" height="50" rx="4" fill="var(--dia-bg-card)" stroke="var(--dia-stroke)" stroke-width="1.6"/>
  <rect x="210" y="70" width="3" height="50" fill="var(--dia-accent)"/>
  <text x="280" y="99" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">Power budget?</text>
  <rect x="380" y="70" width="140" height="50" rx="4" fill="var(--dia-bg-card)" stroke="var(--dia-stroke)" stroke-width="1.6"/>
  <rect x="380" y="70" width="3" height="50" fill="var(--dia-accent)"/>
  <text x="450" y="92" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">Real-time control</text>
  <text x="450" y="106" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">needed?</text>
  <rect x="40" y="210" width="140" height="50" rx="4" fill="var(--dia-bg-card)" stroke="var(--dia-stroke)" stroke-width="1.6"/>
  <rect x="40" y="210" width="3" height="50" fill="var(--dia-accent)"/>
  <text x="110" y="239" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">Jetson Orin Nano</text>
  <rect x="210" y="210" width="140" height="50" rx="4" fill="var(--dia-bg-card)" stroke="var(--dia-stroke)" stroke-width="1.6"/>
  <rect x="210" y="210" width="3" height="50" fill="var(--dia-accent)"/>
  <text x="280" y="239" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">Jetson Orin NX</text>
  <rect x="380" y="210" width="140" height="50" rx="4" fill="var(--dia-bg-card)" stroke="var(--dia-stroke)" stroke-width="1.6"/>
  <rect x="380" y="210" width="3" height="50" fill="var(--dia-accent)"/>
  <text x="450" y="239" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">Jetson AGX Orin</text>
  <rect x="40" y="350" width="140" height="50" rx="4" fill="var(--dia-bg-card)" stroke="var(--dia-stroke)" stroke-width="1.6"/>
  <rect x="40" y="350" width="3" height="50" fill="var(--dia-accent)"/>
  <text x="110" y="379" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">Complexity?</text>
  <rect x="210" y="350" width="140" height="50" rx="4" fill="var(--dia-bg-card)" stroke="var(--dia-stroke)" stroke-width="1.6"/>
  <rect x="210" y="350" width="3" height="50" fill="var(--dia-accent)"/>
  <text x="280" y="379" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">Raspberry Pi 5</text>
  <rect x="380" y="350" width="140" height="50" rx="4" fill="var(--dia-bg-card)" stroke="var(--dia-stroke)" stroke-width="1.6"/>
  <rect x="380" y="350" width="3" height="50" fill="var(--dia-accent)"/>
  <text x="450" y="379" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">STM32F4</text>
  <rect x="210" y="490" width="140" height="50" rx="4" fill="var(--dia-bg-card)" stroke="var(--dia-stroke)" stroke-width="1.6"/>
  <rect x="210" y="490" width="3" height="50" fill="var(--dia-accent)"/>
  <text x="280" y="519" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">STM32H7</text>
</svg>
</div>


## Summary

1. Modern CPUs use a **modified Harvard architecture**, balancing performance and flexibility
2. **Pipelining** is the basic method for increasing CPU throughput, but is limited by various hazards
3. The **cache hierarchy** has a huge impact on performance; writing cache-friendly code is important
4. **ARM dominates robotics**, with Cortex-A for main control and Cortex-M for real-time control
5. **Amdahl's Law** reminds us to focus on serial bottlenecks

## References

- Patterson, D. A., & Hennessy, J. L. *Computer Organization and Design: The RISC-V Edition*
- ARM Architecture Reference Manual for A-profile architecture
- RISC-V ISA Specification: [https://riscv.org/specifications/](https://riscv.org/specifications/)
