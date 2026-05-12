# Wiring and PCB Design

## Overview

Electronic integration is one of the most error-prone aspects of robot system integration. This section covers wiring best practices, connector selection, and custom PCB design fundamentals.

---

## Wiring Fundamentals

### Wire Gauge (AWG)

AWG (American Wire Gauge) is the standard for wire thickness. **Lower numbers mean thicker wire**.

| AWG | Diameter (mm) | Current Capacity (A) | Resistance (mΩ/m) | Typical Use |
|-----|----------|-----------|-------------|---------|
| 10 | 2.59 | 30 | 3.3 | Battery main, large motors |
| 12 | 2.05 | 20 | 5.2 | Motor power |
| 14 | 1.63 | 15 | 8.3 | Medium power devices |
| 16 | 1.29 | 10 | 13.2 | Servo power |
| 18 | 1.02 | 7 | 21.0 | Small motors, sensor power |
| 20 | 0.81 | 5 | 33.3 | Sensor signal lines |
| 22 | 0.64 | 3 | 53.0 | Low-power signals |
| 24 | 0.51 | 2 | 84.2 | I2C/SPI signal lines |
| 26 | 0.40 | 1.3 | 134 | Fine signal lines |
| 28 | 0.32 | 0.8 | 213 | Ultra-fine signal lines |

**Wire Selection Principle**:

$$I_{wire\_rating} \geq 1.5 \times I_{max\_load}$$

Leave 50% margin to prevent overheating.

### Wire Types

| Type | Features | Application |
|------|------|------|
| **Silicone wire** | Flexible, heat resistant (-60~200°C) | Robot joints, motor wiring |
| **PVC wire** | Cheap, stiff | Fixed routing |
| **Teflon wire** | Heat and chemical resistant | Harsh environments |
| **Ribbon cable (FFC/FPC)** | Flat, flexible | Displays, tight spaces |
| **Twisted pair** | Noise resistant | CAN Bus, differential signals |
| **Shielded cable** | Electromagnetic shielding | Analog signals, encoders |

### Color Coding

Standard color conventions (not mandatory, but strongly recommended):

| Color | Use |
|------|------|
| **Red** | Positive power (VCC/V+) |
| **Black** | Ground (GND) |
| **Yellow** | Signal (PWM/Signal) |
| **Green** | Communication (CAN-H/TX) |
| **Blue** | Communication (CAN-L/RX) |
| **White** | Communication (SDA/MOSI) |
| **Orange** | Spare/Secondary power |

**Labels**: Label both ends of every wire with source and destination.

---

## Connector Selection

### Power Connectors

| Connector | Current Rating | Typical Voltage | Features | Use |
|--------|---------|---------|------|------|
| **XT60** | 60A | High voltage | High current, latch | Battery main connector |
| **XT30** | 30A | Medium voltage | Medium current | Motor branch |
| **DC barrel** | 1-5A | 5-24V | Simple | Dev board power |
| **Anderson PP** | 15-180A | High voltage | Industrial grade | Large robots |
| **Deans (T-plug)** | 40A | High voltage | Common in RC | Small robots |

### Signal Connectors

| Connector | Pitch | Pin Count | Features | Use |
|--------|------|--------|------|------|
| **JST-XH** | 2.5mm | 2-16 | Latching | Battery balance, sensors |
| **JST-PH** | 2.0mm | 2-16 | Small | Small sensors |
| **JST-SH** | 1.0mm | 2-10 | Micro | QWIIC (I2C) |
| **Molex Micro-Fit** | 3.0mm | 2-24 | Industrial grade | Motor drivers |
| **DuPont 2.54mm** | 2.54mm | Any | Breadboard friendly | Prototyping |
| **Hirose DF13** | 1.25mm | 2-15 | Reliable, compact | Pixhawk flight controller |

### Waterproof Connectors

| Connector | Protection Rating | Pin Count | Use |
|--------|---------|--------|------|
| **M8 circular** | IP67 | 3-8 | Industrial sensors |
| **M12 circular** | IP67 | 4-12 | EtherCAT, industrial |
| **IP67 USB** | IP67 | 4 | Outdoor cameras |

### Quick-Disconnect Design

Robots need quick disassembly for maintenance:

- Use latching connectors for joint harnesses (do not solder permanently)
- Use standard connectors between modules (M8/M12)
- Each removable module has its own wiring harness

---

## Strain Relief

The most common failure mode for connectors is cable pulling causing solder/crimp joint fracture.

**Locations that must have strain relief**:

- Connector exit points
- Cables passing through panels
- Cables near robot joints
- Any location where pulling may occur

**Methods**:

| Method | Application |
|------|----------|
| Heat shrink + adhesive | Connector tail |
| Cable ties | Cable crossing points |
| P-clips | Mounting to frame |
| Cable chain | Linear motion cables |
| Spiral wrap | Rotating joints |

---

## Crimping Tools

**Strongly recommended** to use proper crimping tools rather than soldering connector terminals:

| Tool | Compatible Connectors | Price Range |
|------|-----------|---------|
| **Engineer PA-09** | JST-XH/PH | ~$30 |
| **Engineer PA-20** | JST-SH, small terminals | ~$30 |
| **IWISS SN-28B** | DuPont 2.54mm | ~$20 |
| **Molex hand crimper** | Molex Micro-Fit | ~$40 |
| **XT60 soldering** | XT60 (requires soldering) | Soldering iron |

**Crimping vs. Soldering**:

- Crimping: Reliable, repeatable, professional
- Soldering: Flexible but inconsistent, heat may damage wire
- Industrial standards require crimping (mandatory in aerospace)

---

## Custom PCB Design

### When to Design a Custom PCB

- Too many messy wires (>20 fly wires -> consider PCB)
- Specific power distribution needs
- Signal conditioning circuits needed (amplification, filtering)
- Mass production requirements
- Strict size/weight constraints

### KiCad Workflow

KiCad is the most popular open-source PCB design software.

**Complete Process**:

<div class="diagram">
<svg viewBox="0 0 900 200" xmlns="http://www.w3.org/2000/svg">
  <defs><marker id="arr-m0" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="var(--dia-stroke)"/></marker></defs>
  
  <line x1="180" y1="95" x2="270" y2="95" stroke="var(--dia-stroke)" stroke-width="1.5" marker-end="url(#arr-m0)"/>
  <line x1="410" y1="95" x2="500" y2="95" stroke="var(--dia-stroke)" stroke-width="1.5" marker-end="url(#arr-m0)"/>
  <line x1="640" y1="95" x2="730" y2="95" stroke="var(--dia-stroke)" stroke-width="1.5" marker-end="url(#arr-m0)"/>
  <line x1="870" y1="95" x2="960" y2="95" stroke="var(--dia-stroke)" stroke-width="1.5" marker-end="url(#arr-m0)"/>
  <line x1="1100" y1="95" x2="1190" y2="95" stroke="var(--dia-stroke)" stroke-width="1.5" marker-end="url(#arr-m0)"/>
  <line x1="1330" y1="95" x2="1420" y2="95" stroke="var(--dia-stroke)" stroke-width="1.5" marker-end="url(#arr-m0)"/>
  <line x1="1560" y1="95" x2="1650" y2="95" stroke="var(--dia-stroke)" stroke-width="1.5" marker-end="url(#arr-m0)"/>
  <line x1="1790" y1="95" x2="1880" y2="95" stroke="var(--dia-stroke)" stroke-width="1.5" marker-end="url(#arr-m0)"/>
  <rect x="40" y="70" width="140" height="50" rx="4" fill="var(--dia-bg-card)" stroke="var(--dia-stroke)" stroke-width="1.6"/>
  <rect x="40" y="70" width="3" height="50" fill="var(--dia-accent)"/>
  <text x="110" y="99" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">Schematic Design</text>
  <rect x="270" y="70" width="140" height="50" rx="4" fill="var(--dia-bg-card)" stroke="var(--dia-stroke)" stroke-width="1.6"/>
  <rect x="270" y="70" width="3" height="50" fill="var(--dia-green)"/>
  <text x="340" y="92" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">Electrical Rules</text>
  <text x="340" y="106" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">Check ERC</text>
  <rect x="500" y="70" width="140" height="50" rx="4" fill="var(--dia-bg-card)" stroke="var(--dia-stroke)" stroke-width="1.6"/>
  <rect x="500" y="70" width="3" height="50" fill="var(--dia-blue)"/>
  <text x="570" y="99" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">Assign Footprints</text>
  <rect x="730" y="70" width="140" height="50" rx="4" fill="var(--dia-bg-card)" stroke="var(--dia-stroke)" stroke-width="1.6"/>
  <rect x="730" y="70" width="3" height="50" fill="var(--dia-accent)"/>
  <text x="800" y="99" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">PCB Layout</text>
  <rect x="960" y="70" width="140" height="50" rx="4" fill="var(--dia-bg-card)" stroke="var(--dia-stroke)" stroke-width="1.6"/>
  <rect x="960" y="70" width="3" height="50" fill="var(--dia-green)"/>
  <text x="1030" y="99" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">Routing</text>
  <rect x="1190" y="70" width="140" height="50" rx="4" fill="var(--dia-bg-card)" stroke="var(--dia-stroke)" stroke-width="1.6"/>
  <rect x="1190" y="70" width="3" height="50" fill="var(--dia-blue)"/>
  <text x="1260" y="92" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">Design Rules</text>
  <text x="1260" y="106" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">Check DRC</text>
  <rect x="1420" y="70" width="140" height="50" rx="4" fill="var(--dia-bg-card)" stroke="var(--dia-stroke)" stroke-width="1.6"/>
  <rect x="1420" y="70" width="3" height="50" fill="var(--dia-accent)"/>
  <text x="1490" y="92" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">Generate Gerber</text>
  <text x="1490" y="106" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">Files</text>
  <rect x="1650" y="70" width="140" height="50" rx="4" fill="var(--dia-bg-card)" stroke="var(--dia-stroke)" stroke-width="1.6"/>
  <rect x="1650" y="70" width="3" height="50" fill="var(--dia-green)"/>
  <text x="1720" y="92" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">Send to</text>
  <text x="1720" y="106" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">Manufacturer</text>
  <rect x="1880" y="70" width="140" height="50" rx="4" fill="var(--dia-bg-card)" stroke="var(--dia-stroke)" stroke-width="1.6"/>
  <rect x="1880" y="70" width="3" height="50" fill="var(--dia-blue)"/>
  <text x="1950" y="92" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">Soldering and</text>
  <text x="1950" y="106" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">Debugging</text>
</svg>
</div>


### Schematic Design

The schematic is the logical representation of the circuit. Key steps:

1. **Place components**: Select or create symbols from libraries
2. **Wire connections**: Connect pins with wires
3. **Add power symbols**: VCC, GND, etc.
4. **Add decoupling capacitors**: Place 100nF + 10μF near each IC
5. **Annotate**: Component values, part numbers

### PCB Layout and Routing

**Layout Principles**:

- Keep power components away from sensitive signals
- Place decoupling capacitors close to IC pins
- Place connectors at board edges
- Consider thermal management (widen high-current paths, copper pour)

**Routing Rules** (2-layer board reference):

| Trace Width | Current Capacity | Use |
|------|---------|------|
| 0.2mm | ~0.3A | Signal traces |
| 0.5mm | ~1A | Low power |
| 1.0mm | ~2A | Medium power |
| 2.0mm | ~4A | Power traces |
| Copper pour | >5A | High current |

Empirical formula (outer layer, 1oz copper):

$$I_{max} \approx 0.048 \cdot \Delta T^{0.44} \cdot A^{0.725}$$

where $A$ is the conductor cross-section area (mil²) and $\Delta T$ is the allowable temperature rise (°C).

### Common Circuit Modules

#### Voltage Divider

Used for voltage sensing (e.g., battery voltage measurement):

$$V_{out} = V_{in} \cdot \frac{R_2}{R_1 + R_2}$$

Example: 24V battery voltage -> 3.3V ADC range:

$$\frac{R_2}{R_1 + R_2} = \frac{3.3}{24} \approx 0.1375$$

Choose $R_1 = 100k\Omega$, $R_2 = 15.8k\Omega$.

#### Level Shifter

Interfacing 3.3V and 5V logic:

- **Unidirectional**: MOSFET + pull-up resistor (BSS138 approach)
- **Bidirectional**: TXB0108 (8-channel auto-direction detection)
- **I2C specific**: PCA9306 (bidirectional, supports different voltage buses)

#### Breakout Board

Distributes a single high-density connector to multiple subsystems:

```
                  ┌── IMU (SPI)
[Main Board] ── [Breakout Board] ── Motor Driver (CAN)
                  ├── Sensor (I2C)
                  └── GPS (UART)
```

---

## PCB Prototyping

### Manufacturers

| Manufacturer | Minimum Price | Lead Time | Features |
|------|--------|---------|------|
| **JLCPCB** | 5 pcs/$2 | 1-3 days | Best value |
| **PCBWay** | 5 pcs/$5 | 2-5 days | International shipping friendly |
| **HQ PCB** | 5 pcs/$3 | 1-3 days | KiCad plugin |

### Prototyping Notes

- **Minimum trace width/spacing**: 0.15mm (standard process)
- **Minimum hole diameter**: 0.3mm
- **Copper weight**: 1oz (35μm) standard, 2oz for high current
- **Surface finish**: HASL (cheap), ENIG (better pads)
- **Board thickness**: 1.6mm standard
- **Solder mask color**: Green is cheapest

### Soldering

**Manual Soldering** (prototyping):

- Iron temperature: 300-360°C
- Flux is essential
- 0402 and larger packages can be hand-soldered (with experience)
- QFP/TQFP requires drag-soldering technique

**Reflow Soldering** (small batch):

- Stencil + solder paste -> Place components -> Heat reflow
- Budget option: Solder paste + hot air gun / modified toaster oven

---

## Wire Harness Design

### Harness Diagram

For complex robots, a wire harness diagram is essential:

```
Battery ─[XT60]─ Power Distribution ─┬─[XT30]─ Motor Driver 1
                                      ├─[XT30]─ Motor Driver 2
                                      ├─[DC barrel]─ Jetson
                                      └─[JST-XH]─ Sensor Board

Main Controller ─┬─[USB-C]─ Depth Camera
                  ├─[M12]─── LiDAR
                  ├─[SPI(JST-SH)]─ IMU
                  └─[CAN(Molex)]─── Motor Driver CAN Bus
```

### Harness Labeling Standards

Each wire/harness should be labeled with:

1. **Number**: W001, W002, ...
2. **Source**: Module name + pin
3. **Destination**: Module name + pin
4. **Wire**: AWG + color
5. **Length**: Measured + 10% margin

---

## Electromagnetic Compatibility (EMC) Basics

### Common Interference Sources

| Source | Frequency Range | Impact |
|--------|---------|------|
| BLDC motor PWM | 10-100 kHz | ADC noise |
| Switching power supply | 100 kHz - 1 MHz | Sensor interference |
| Digital signals | MHz range | RF interference |

### Mitigation Measures

1. **Power filtering**: Large electrolytic capacitors + high-frequency ceramic capacitors
2. **Ground separation**: Connect analog and digital ground at a single point
3. **Signal shielding**: Use shielded cable for sensitive signals
4. **Layout isolation**: Physically separate high-power and low-signal areas
5. **Ferrite beads**: Suppress high-frequency interference

$$Z_{ferrite}(f) = R(f) + jX(f)$$

At the target frequency range (typically 10-100 MHz), impedance increases significantly, attenuating interference.

---

## References

- KiCad Official Tutorials: [kicad.org](https://www.kicad.org/)
- JLCPCB: [jlcpcb.com](https://jlcpcb.com/)
- IPC-2221: Generic Standard on Printed Board Design
- Phil's Lab (YouTube): Practical PCB design tutorials
