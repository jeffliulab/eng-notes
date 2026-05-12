# 接线与PCB设计

## 概述

电子集成是机器人系统集成中最容易出问题的环节之一。本节涵盖接线最佳实践、连接器选型和自定义 PCB 设计基础。

---

## 接线基础

### 线材规格（AWG）

AWG（American Wire Gauge）是线材粗细的标准。**数字越小，线越粗**。

| AWG | 直径 (mm) | 载流量 (A) | 电阻 (mΩ/m) | 典型用途 |
|-----|----------|-----------|-------------|---------|
| 10 | 2.59 | 30 | 3.3 | 电池主线、大电机 |
| 12 | 2.05 | 20 | 5.2 | 电机电源 |
| 14 | 1.63 | 15 | 8.3 | 中功率设备 |
| 16 | 1.29 | 10 | 13.2 | 舵机电源 |
| 18 | 1.02 | 7 | 21.0 | 小型电机、传感器电源 |
| 20 | 0.81 | 5 | 33.3 | 传感器信号线 |
| 22 | 0.64 | 3 | 53.0 | 低功率信号 |
| 24 | 0.51 | 2 | 84.2 | I2C/SPI 信号线 |
| 26 | 0.40 | 1.3 | 134 | 细信号线 |
| 28 | 0.32 | 0.8 | 213 | 极细信号线 |

**选线原则**：

$$I_{wire\_rating} \geq 1.5 \times I_{max\_load}$$

留 50% 余量防止发热。

### 线材类型

| 类型 | 特点 | 适用 |
|------|------|------|
| **硅胶线** | 柔软耐高温（-60~200°C） | 机器人关节、电机接线 |
| **PVC 线** | 便宜、硬 | 固定布线 |
| **铁氟龙线** | 耐高温耐化学 | 恶劣环境 |
| **排线（FFC/FPC）** | 扁平柔性 | 显示屏、紧凑空间 |
| **双绞线** | 抗干扰 | CAN Bus、差分信号 |
| **屏蔽线** | 电磁屏蔽 | 模拟信号、编码器 |

### 颜色编码

标准颜色约定（无强制标准，但强烈建议遵循）：

| 颜色 | 用途 |
|------|------|
| **红色** | 正极电源（VCC/V+） |
| **黑色** | 地线（GND） |
| **黄色** | 信号线（PWM/Signal） |
| **绿色** | 通信（CAN-H/TX） |
| **蓝色** | 通信（CAN-L/RX） |
| **白色** | 通信（SDA/MOSI） |
| **橙色** | 备用/第二电源 |

**标签**：每根线的两端都贴标签，标注来源和去向。

---

## 连接器选型

### 电源连接器

| 连接器 | 额定电流 | 典型电压 | 特点 | 用途 |
|--------|---------|---------|------|------|
| **XT60** | 60A | 高压 | 大电流、锁扣 | 电池主接口 |
| **XT30** | 30A | 中压 | 中等电流 | 电机分路 |
| **DC barrel** | 1-5A | 5-24V | 简单 | 开发板供电 |
| **Anderson PP** | 15-180A | 高压 | 工业级 | 大型机器人 |
| **Deans (T-plug)** | 40A | 高压 | 航模常用 | 小型机器人 |

### 信号连接器

| 连接器 | 间距 | 引脚数 | 特点 | 用途 |
|--------|------|--------|------|------|
| **JST-XH** | 2.5mm | 2-16 | 带锁扣 | 电池平衡头、传感器 |
| **JST-PH** | 2.0mm | 2-16 | 小型 | 小传感器 |
| **JST-SH** | 1.0mm | 2-10 | 微型 | QWIIC (I2C) |
| **Molex Micro-Fit** | 3.0mm | 2-24 | 工业级 | 电机驱动器 |
| **DuPont 2.54mm** | 2.54mm | 任意 | 面包板友好 | 原型开发 |
| **Hirose DF13** | 1.25mm | 2-15 | 可靠紧凑 | Pixhawk 飞控 |

### 防水连接器

| 连接器 | 防护等级 | 引脚数 | 用途 |
|--------|---------|--------|------|
| **M8 圆形** | IP67 | 3-8 | 工业传感器 |
| **M12 圆形** | IP67 | 4-12 | EtherCAT、工业 |
| **IP67 USB** | IP67 | 4 | 户外相机 |

### 快拆设计

机器人维护时需要快速拆装：

- 关节线束使用带锁扣的连接器（不要焊死）
- 模块之间使用标准连接器（M8/M12）
- 每个可拆卸模块有独立的线束

---

## 应力释放（Strain Relief）

连接器最常见的失效模式是线缆拉扯导致焊点/压接点断裂。

**必须做应力释放的位置**：

- 连接器出线处
- 穿过板材的线缆
- 机器人关节附近的线缆
- 任何可能被拉扯的位置

**方法**：

| 方法 | 适用场景 |
|------|----------|
| 热缩管 + 胶 | 连接器尾部 |
| 扎带固定 | 线缆穿越点 |
| 线缆夹（P-clip） | 固定到机架 |
| 拖链 | 直线运动的线缆 |
| 盘簧管 | 旋转关节 |

---

## 压接工具

**强烈建议**使用正规压接工具而非烙铁焊接连接器端子：

| 工具 | 适用连接器 | 价格范围 |
|------|-----------|---------|
| **Engineer PA-09** | JST-XH/PH | ~$30 |
| **Engineer PA-20** | JST-SH、小端子 | ~$30 |
| **IWISS SN-28B** | DuPont 2.54mm | ~$20 |
| **Molex 手动压接钳** | Molex Micro-Fit | ~$40 |
| **XT60 焊接** | XT60（需焊接） | 烙铁 |

**压接 vs. 焊接**：

- 压接：可靠、可重复、专业
- 焊接：灵活但不一致、高温可能损伤线材
- 工业标准要求压接（航空航天强制）

---

## 自定义 PCB 设计

### 何时需要自定义 PCB

- 接线太多太乱（>20 根飞线 → 考虑 PCB）
- 需要特定的电源分配
- 需要信号调理电路（放大、滤波）
- 量产需求
- 尺寸/重量有严格限制

### KiCad 工作流

KiCad 是最流行的开源 PCB 设计软件。

**完整流程**：

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
  <text x="110" y="99" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">原理图设计</text>
  <rect x="270" y="70" width="140" height="50" rx="4" fill="var(--dia-bg-card)" stroke="var(--dia-stroke)" stroke-width="1.6"/>
  <rect x="270" y="70" width="3" height="50" fill="var(--dia-green)"/>
  <text x="340" y="99" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">电气规则检查 ERC</text>
  <rect x="500" y="70" width="140" height="50" rx="4" fill="var(--dia-bg-card)" stroke="var(--dia-stroke)" stroke-width="1.6"/>
  <rect x="500" y="70" width="3" height="50" fill="var(--dia-blue)"/>
  <text x="570" y="99" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">分配封装</text>
  <rect x="730" y="70" width="140" height="50" rx="4" fill="var(--dia-bg-card)" stroke="var(--dia-stroke)" stroke-width="1.6"/>
  <rect x="730" y="70" width="3" height="50" fill="var(--dia-accent)"/>
  <text x="800" y="99" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">PCB 布局</text>
  <rect x="960" y="70" width="140" height="50" rx="4" fill="var(--dia-bg-card)" stroke="var(--dia-stroke)" stroke-width="1.6"/>
  <rect x="960" y="70" width="3" height="50" fill="var(--dia-green)"/>
  <text x="1030" y="99" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">布线</text>
  <rect x="1190" y="70" width="140" height="50" rx="4" fill="var(--dia-bg-card)" stroke="var(--dia-stroke)" stroke-width="1.6"/>
  <rect x="1190" y="70" width="3" height="50" fill="var(--dia-blue)"/>
  <text x="1260" y="99" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">设计规则检查 DRC</text>
  <rect x="1420" y="70" width="140" height="50" rx="4" fill="var(--dia-bg-card)" stroke="var(--dia-stroke)" stroke-width="1.6"/>
  <rect x="1420" y="70" width="3" height="50" fill="var(--dia-accent)"/>
  <text x="1490" y="99" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">生成 Gerber</text>
  <rect x="1650" y="70" width="140" height="50" rx="4" fill="var(--dia-bg-card)" stroke="var(--dia-stroke)" stroke-width="1.6"/>
  <rect x="1650" y="70" width="3" height="50" fill="var(--dia-green)"/>
  <text x="1720" y="99" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">发送工厂制板</text>
  <rect x="1880" y="70" width="140" height="50" rx="4" fill="var(--dia-bg-card)" stroke="var(--dia-stroke)" stroke-width="1.6"/>
  <rect x="1880" y="70" width="3" height="50" fill="var(--dia-blue)"/>
  <text x="1950" y="99" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">焊接调试</text>
</svg>
</div>


### 原理图设计

原理图是电路的逻辑表达。关键步骤：

1. **放置元件**：从库中选择或创建符号
2. **连线**：用导线连接引脚
3. **添加电源符号**：VCC、GND 等
4. **添加去耦电容**：每个 IC 旁放 100nF + 10μF
5. **标注**：元件值、型号

### PCB 布局与布线

**布局原则**：

- 功率器件远离敏感信号
- 去耦电容紧贴 IC 引脚
- 连接器放在板边
- 考虑散热（大电流路径加宽、铺铜）

**布线规则**（2 层板参考）：

| 线宽 | 电流能力 | 用途 |
|------|---------|------|
| 0.2mm | ~0.3A | 信号线 |
| 0.5mm | ~1A | 低功率 |
| 1.0mm | ~2A | 中功率 |
| 2.0mm | ~4A | 电源线 |
| 铺铜 | >5A | 大电流 |

经验公式（外层，1oz 铜厚）：

$$I_{max} \approx 0.048 \cdot \Delta T^{0.44} \cdot A^{0.725}$$

其中 $A$ 为导体截面积（mil²），$\Delta T$ 为允许温升（°C）。

### 常用电路模块

#### 电压分压器

用于电压检测（如电池电压测量）：

$$V_{out} = V_{in} \cdot \frac{R_2}{R_1 + R_2}$$

例：24V 电池电压 → 3.3V ADC 范围：

$$\frac{R_2}{R_1 + R_2} = \frac{3.3}{24} \approx 0.1375$$

选 $R_1 = 100k\Omega$, $R_2 = 15.8k\Omega$。

#### 电平转换器（Level Shifter）

3.3V 和 5V 逻辑互联：

- **单向**：MOSFET + 上拉电阻（BSS138 方案）
- **双向**：TXB0108（8 通道自动方向检测）
- **I2C 专用**：PCA9306（双向，支持不同电压总线）

#### 连接器分线板

将单个高密度连接器分出到多个子系统：

```
                  ┌── IMU (SPI)
[主控板] ── [分线板] ── 电机驱动 (CAN)
                  ├── 传感器 (I2C)
                  └── GPS (UART)
```

---

## PCB 打样

### 国内厂商

| 厂商 | 最低价 | 制板周期 | 特色 |
|------|--------|---------|------|
| **嘉立创 (JLCPCB)** | 5片/¥2 | 1-3天 | 极致性价比 |
| **捷配 (PCBWay)** | 5片/$5 | 2-5天 | 海外发货友好 |
| **华秋 (HQ PCB)** | 5片/¥10 | 1-3天 | KiCad 插件 |

### 打样注意事项

- **最小线宽/线距**：0.15mm（标准工艺）
- **最小孔径**：0.3mm
- **铜厚**：1oz（35μm）标准，2oz 大电流
- **表面处理**：HASL（便宜）、ENIG（焊盘好）
- **板厚**：1.6mm 标准
- **阻焊颜色**：绿色最便宜

### 焊接

**手动焊接**（原型）：

- 烙铁温度：300-360°C
- 助焊剂必不可少
- 0402 以上封装可手焊（经验足够时）
- QFP/TQFP 需要拖焊技巧

**回流焊**（小批量）：

- 钢网涂锡膏 → 贴片 → 加热回流
- 廉价方案：锡膏 + 热风枪 / 电烤箱改装

---

## 线束设计

### 线束图

在复杂机器人中，线束图（Wire Harness Diagram）至关重要：

```
电池 ─[XT60]─ 分电板 ─┬─[XT30]─ 电机驱动器 1
                       ├─[XT30]─ 电机驱动器 2
                       ├─[DC barrel]─ Jetson
                       └─[JST-XH]─ 传感器板

主控 ─┬─[USB-C]─ 深度相机
      ├─[M12]─── LiDAR
      ├─[SPI(JST-SH)]─ IMU
      └─[CAN(Molex)]─── 电机驱动器 CAN 总线
```

### 线束标注规范

每根线/线束应标注：

1. **编号**：W001, W002, ...
2. **来源**：模块名 + 引脚
3. **去向**：模块名 + 引脚
4. **线材**：AWG + 颜色
5. **长度**：实测 + 10% 余量

---

## 电磁兼容（EMC）基础

### 常见干扰源

| 干扰源 | 频率范围 | 影响 |
|--------|---------|------|
| BLDC 电机 PWM | 10-100 kHz | ADC 噪声 |
| 开关电源 | 100 kHz - 1 MHz | 传感器干扰 |
| 数字信号 | MHz 级 | 射频干扰 |

### 缓解措施

1. **电源滤波**：大容量电解电容 + 高频陶瓷电容
2. **地线分离**：模拟地和数字地单点连接
3. **信号屏蔽**：敏感信号使用屏蔽线
4. **布局隔离**：大功率和小信号物理分开
5. **铁氧体磁珠**：抑制高频干扰

$$Z_{ferrite}(f) = R(f) + jX(f)$$

在目标频率范围（通常 10-100 MHz），阻抗显著增大，衰减干扰。

---

## 参考资源

- KiCad 官方教程: [kicad.org](https://www.kicad.org/)
- JLCPCB: [jlcpcb.com](https://jlcpcb.com/)
- IPC-2221: Generic Standard on Printed Board Design
- Phil's Lab (YouTube): PCB 设计实战教程
