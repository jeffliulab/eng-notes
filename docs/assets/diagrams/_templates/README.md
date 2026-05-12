# SVG 模板库

> 5 个 Tufte 风格 SVG 模板，作为新建图示的起点。
>
> - **风格规范**：仓库根目录 `全面升级plan.md` §3 Tufte SVG 规范
> - **调色板**：`docs/site_extra_styles/stylesheets/extra.css` 末尾的 `--dia-*` 变量
> - **Canonical 参考**：仓库根目录 `参考html代码包括hmms的图.html`

---

## 5 个模板渲染预览

### 1. graphical_model.svg — 图模型 (HMM/贝叶斯网式有向图)

适用：HMM、Bayesian Network、MRF、CRF 的图模型表示。圆形 = 隐藏节点，方形 = 观测节点。

<div class="diagram">
--8<-- "assets/diagrams/_templates/graphical_model.svg"
</div>
<p class="figure-caption">Template 1 — 图模型：圆形隐藏 + 方形观测，横向 transition + 纵向 emission。</p>

---

### 2. trellis.svg — 动态规划网格

适用：Forward / Viterbi / Beam Search 的 trellis 网格。每列一个时间步，每行一个状态，全连接 |S|×|S| 边。

<div class="diagram">
--8<-- "assets/diagrams/_templates/trellis.svg"
</div>
<p class="figure-caption">Template 2 — DP trellis：α 值递推，主黑色节点 + 副色描边区分状态。</p>

---

### 3. comparison_panel.svg — 对比卡片

适用：分类树 + 三栏并排对比。例如 HMM 三个基本问题（Evaluation/Decoding/Learning），三种 attention 变体对比。

<div class="diagram">
--8<-- "assets/diagrams/_templates/comparison_panel.svg"
</div>
<p class="figure-caption">Template 3 — Comparison panel：根概念 → 三分支 → 三卡片，左侧色条编码。</p>

---

### 4. architecture_block.svg — 架构块图

适用：Transformer Encoder/Decoder Block、ResNet Block、CNN/GNN block。主路径竖向，残差连接虚线。

<div class="diagram">
--8<-- "assets/diagrams/_templates/architecture_block.svg"
</div>
<p class="figure-caption">Template 4 — Architecture block：主路径竖向，子模块色条标注，残差虚线绕行。</p>

---

### 5. timeline_horizontal.svg — 横向时间轴

适用：领域里程碑、模型演进史、关键事件标注。节点上下交错避免标签拥挤。

<div class="diagram">
--8<-- "assets/diagrams/_templates/timeline_horizontal.svg"
</div>
<p class="figure-caption">Template 5 — Horizontal timeline：水平主轴，节点上下交错标签，关键节点高亮。</p>

---

## 使用方法

1. **从模板复制**：`cp docs/assets/diagrams/_templates/<template>.svg docs/<section>/<article>/diagrams/figure-N-<name>.svg`
2. **改坐标和标签**（用 viewBox + 数字坐标，不用 transform 嵌套）
3. **保留 CSS 变量**（`fill="var(--dia-bg-card)"` 等），自动响应 dark mode
4. **嵌入文章**：

   用 `<div class="diagram">` 包裹，里面用 pymdownx.snippets 的语法 `{{ "--8<--" }}` 引入 SVG 文件路径，下面跟 `<p class="figure-caption">` 写图注。

   或对短 SVG (< 80 行)，直接把 `<svg>` 标签内联到 .md（无需 snippets，markdown 原生支持）。

   实际示例见本 README 上方 5 个模板的渲染（页面源码 `_templates/README.md`）。

## 色板速查

| 用途 | 变量 | 浅色值 | 深色值 |
|---|---|---|---|
| 主背景 | `--dia-bg` | `#f5f0e8` | `#1a1612` |
| 卡片白底 | `--dia-bg-card` | `#ffffff` | `#252018` |
| 强调底色 | `--dia-bg-deep` | `#ede8df` | `#2e2820` |
| 主笔画 | `--dia-stroke` | `#1a1612` | `#e8e0d8` |
| 辅助笔画 | `--dia-stroke-soft` | `#6b5f4e` | `#a09888` |
| 主强调 (terracotta) | `--dia-accent` | `#c4673a` | `#da7756` |
| 公式 / 深红 | `--dia-accent-deep` | `#b55d32` | `#c4673a` |
| 副色 1 forest | `--dia-green` | `#4a6741` | `#8bc086` |
| 副色 2 deep blue | `--dia-blue` | `#2c4d6e` | `#7fa3c8` |
| 副色 3 gold | `--dia-gold` | `#b8932c` | `#e8c060` |

**与 jeffliulab.com 主站同源**：日后 ai-wiki 接入主站时 SVG 不需任何修改。
