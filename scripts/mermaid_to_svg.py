#!/usr/bin/env python3
"""
mermaid_to_svg.py — Convert mermaid blocks in markdown to inline Tufte-style SVG.

Supports:
  - graph TD/LR/TB/RL, flowchart TD/LR/TB/RL — simple flowchart layout (most common)
  - timeline — horizontal timeline
  - stateDiagram-v2 — same layout as flowchart
  - sequenceDiagram — vertical message flow
  - pie / gitGraph — fallback descriptive table

Usage:
  python mermaid_to_svg.py docs/                # process all markdown under docs/
  python mermaid_to_svg.py docs/01_CA/ --dry    # show what would change
  python mermaid_to_svg.py path/to/file.md      # single file

Palette: uses var(--dia-*) variables matching the site's Tufte CSS.
Layout: simple topological layer assignment, fixed node sizes, basic edge routing.
"""

import argparse
import os
import re
import sys
import html
from collections import defaultdict, OrderedDict
from typing import List, Tuple, Dict, Optional


# ===== SVG building primitives =====
def svg_header(width: int, height: int, title: str = "") -> str:
    title_y = 30
    title_svg = (
        f'<text x="{width//2}" y="{title_y}" text-anchor="middle" '
        f'font-family="Fraunces, Georgia, serif" font-style="italic" font-weight="600" '
        f'font-size="18" fill="var(--dia-stroke)">{html.escape(title)}</text>'
    ) if title else ""
    return (
        f'<div class="diagram">\n'
        f'<svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">\n'
        f'  <defs><marker id="arr-{title_id(title)}" markerWidth="10" markerHeight="10" '
        f'refX="9" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="var(--dia-stroke)"/>'
        f'</marker></defs>\n'
        f'  {title_svg}\n'
    )


def title_id(title: str) -> str:
    h = abs(hash(title)) % 100000
    return f"m{h}"


def svg_footer(caption: str = "") -> str:
    cap = f'<p class="figure-caption">{html.escape(caption)}</p>\n' if caption else ""
    return f'</svg>\n</div>\n{cap}'


def svg_node(x: int, y: int, w: int, h: int, label: str, accent: str = "accent") -> str:
    """Tufte-style node: rounded rect with accent stripe, centered label."""
    color_map = {"accent": "var(--dia-accent)", "green": "var(--dia-green)", "blue": "var(--dia-blue)"}
    accent_color = color_map.get(accent, "var(--dia-accent)")
    label_lines = wrap_label(label, w)
    line_h = 14
    total_text_h = line_h * len(label_lines)
    start_y = y + h / 2 - total_text_h / 2 + 11
    texts = []
    for i, line in enumerate(label_lines):
        texts.append(
            f'  <text x="{x + w/2:.0f}" y="{start_y + i*line_h:.0f}" text-anchor="middle" '
            f'font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">'
            f'{html.escape(line)}</text>'
        )
    return (
        f'  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="var(--dia-bg-card)" '
        f'stroke="var(--dia-stroke)" stroke-width="1.6"/>\n'
        f'  <rect x="{x}" y="{y}" width="3" height="{h}" fill="{accent_color}"/>\n'
        + "\n".join(texts) + "\n"
    )


def wrap_label(label: str, w: int, max_chars_per_line: int = None) -> List[str]:
    """Wrap label to fit within node width. Honors explicit <br/> breaks."""
    if max_chars_per_line is None:
        max_chars_per_line = max(8, w // 8)
    # Honor explicit breaks
    parts = re.split(r'<br\s*/?>', label)
    lines: List[str] = []
    for part in parts:
        part = part.strip()
        if not part:
            continue
        if len(part) <= max_chars_per_line:
            lines.append(part)
        else:
            # Soft wrap by spaces
            words = part.split()
            cur = ""
            for w_ in words:
                if not cur:
                    cur = w_
                elif len(cur) + 1 + len(w_) <= max_chars_per_line:
                    cur += " " + w_
                else:
                    lines.append(cur)
                    cur = w_
            if cur:
                lines.append(cur)
    return lines if lines else [""]


def svg_edge(x1: int, y1: int, x2: int, y2: int, label: str = "", arrow_id: str = "") -> str:
    label_svg = ""
    if label:
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        label_svg = (
            f'  <text x="{mx:.0f}" y="{my-4:.0f}" text-anchor="middle" '
            f'font-family="Fraunces, Georgia, serif" font-style="italic" font-size="10" '
            f'fill="var(--dia-stroke-soft)">{html.escape(label)}</text>\n'
        )
    return (
        f'  <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="var(--dia-stroke)" '
        f'stroke-width="1.5" marker-end="url(#arr-{arrow_id})"/>\n' + label_svg
    )


# ===== Mermaid parser =====
NODE_RE = re.compile(r'^\s*(\w+)\s*(?:\[([^\]]*)\]|\(([^)]*)\)|\{([^}]*)\}|\(\(([^)]*)\)\)|>([^\]]*)\])?')
EDGE_RE = re.compile(r'(\w+)\s*(-->|-\.->|---|==>|-->\|[^|]+\|)\s*(\w+)(?:\s*\|([^|]+)\|)?')
LABELED_EDGE_RE = re.compile(r'(\w+)\s*--\s*([^->|]+?)\s*-->\s*(\w+)')


def parse_graph(code: str) -> Optional[Dict]:
    """Parse a graph/flowchart mermaid block. Returns dict {nodes, edges, direction, title}."""
    lines = [l.strip() for l in code.strip().split('\n')]
    if not lines:
        return None
    first = lines[0]
    # Match: graph TD | flowchart LR | stateDiagram-v2
    m = re.match(r'(graph|flowchart|stateDiagram-v2|stateDiagram)\s*(TD|LR|TB|RL|BT)?', first, re.IGNORECASE)
    if not m:
        return None
    direction = (m.group(2) or 'TD').upper()
    if m.group(1).lower() in ('statediagram-v2', 'statediagram'):
        # treat as flowchart
        direction = 'TD'

    nodes = OrderedDict()    # id -> label
    edges = []               # list of (src_id, dst_id, label)
    title = ""
    in_subgraph = False
    subgraph_label = ""
    for raw in lines[1:]:
        if not raw or raw.startswith('%%') or raw.startswith('classDef') or raw.startswith('class '):
            continue
        if raw.startswith('subgraph'):
            in_subgraph = True
            subgraph_label = raw.replace('subgraph', '').strip().strip('"\'')
            continue
        if raw == 'end':
            in_subgraph = False
            continue
        if raw.startswith('title'):
            title = raw.replace('title', '').strip()
            continue
        if raw.startswith('style ') or raw.startswith('linkStyle'):
            continue

        # Parse edges first (most common)
        # Pattern: A --> B | A --> B :label | A -- label --> B
        # Handle labelled edges first
        labeled = LABELED_EDGE_RE.search(raw)
        if labeled:
            src, lbl, dst = labeled.group(1), labeled.group(2).strip(), labeled.group(3)
            # capture node defs in source
            extract_node_def(raw, src, nodes)
            extract_node_def(raw, dst, nodes)
            edges.append((src, dst, lbl))
            continue

        # Simple edges A --> B[label]
        for em in re.finditer(r'(\w+)(?:\[([^\]]*)\]|\(([^)]*)\)|\{([^}]*)\})?\s*(?:-->|--\s*-|==>)\s*(\w+)(?:\[([^\]]*)\]|\(([^)]*)\)|\{([^}]*)\})?', raw):
            src_id = em.group(1)
            src_label = em.group(2) or em.group(3) or em.group(4) or src_id
            dst_id = em.group(5)
            dst_label = em.group(6) or em.group(7) or em.group(8) or dst_id
            if src_id not in nodes:
                nodes[src_id] = strip_label(src_label)
            elif nodes[src_id] == src_id and src_label != src_id:
                nodes[src_id] = strip_label(src_label)
            if dst_id not in nodes:
                nodes[dst_id] = strip_label(dst_label)
            elif nodes[dst_id] == dst_id and dst_label != dst_id:
                nodes[dst_id] = strip_label(dst_label)
            edges.append((src_id, dst_id, ""))

        # Standalone node def
        for nm in re.finditer(r'(\w+)\[([^\]]+)\]', raw):
            nid, nlbl = nm.group(1), nm.group(2)
            if nid not in nodes or nodes[nid] == nid:
                nodes[nid] = strip_label(nlbl)
        for nm in re.finditer(r'(\w+)\(([^)]+)\)', raw):
            nid, nlbl = nm.group(1), nm.group(2)
            if nid not in nodes or nodes[nid] == nid:
                nodes[nid] = strip_label(nlbl)
        for nm in re.finditer(r'(\w+)\{([^}]+)\}', raw):
            nid, nlbl = nm.group(1), nm.group(2)
            if nid not in nodes or nodes[nid] == nid:
                nodes[nid] = strip_label(nlbl)

    return {
        'nodes': nodes,
        'edges': edges,
        'direction': direction,
        'title': title,
    }


def extract_node_def(raw: str, node_id: str, nodes: Dict):
    """If raw contains 'NodeId[label]' for node_id, set nodes[node_id] = label."""
    m = re.search(rf'{re.escape(node_id)}\[([^\]]+)\]', raw)
    if m:
        if node_id not in nodes or nodes[node_id] == node_id:
            nodes[node_id] = strip_label(m.group(1))
        return
    m = re.search(rf'{re.escape(node_id)}\(([^)]+)\)', raw)
    if m:
        if node_id not in nodes or nodes[node_id] == node_id:
            nodes[node_id] = strip_label(m.group(1))
        return
    if node_id not in nodes:
        nodes[node_id] = node_id


def strip_label(s: str) -> str:
    s = s.strip().strip('"\'').replace('\\n', ' ').replace('<br/>', ' ').replace('<br>', ' ')
    s = re.sub(r'\s+', ' ', s)
    return s


# ===== Layout (topological layered) =====
def layer_assign(nodes: List[str], edges: List[Tuple[str, str, str]]) -> Dict[str, int]:
    """Assign each node a layer (depth from sources)."""
    # Build adjacency
    adj = defaultdict(list)
    rev_adj = defaultdict(list)
    for src, dst, _ in edges:
        adj[src].append(dst)
        rev_adj[dst].append(src)
    layer = {n: 0 for n in nodes}
    # BFS from sources (no incoming) in original order — DAG only
    changed = True
    iters = 0
    while changed and iters < 100:
        changed = False
        for n in nodes:
            for parent in rev_adj.get(n, []):
                if layer.get(parent, 0) + 1 > layer[n]:
                    layer[n] = layer.get(parent, 0) + 1
                    changed = True
        iters += 1
    return layer


def render_graph(parsed: Dict, fallback_title: str = "") -> str:
    """Render parsed graph dict to SVG string."""
    nodes = parsed['nodes']
    edges = parsed['edges']
    direction = parsed['direction']
    title = parsed['title'] or fallback_title

    if not nodes:
        return svg_header(720, 100, title) + svg_footer()

    node_ids = list(nodes.keys())
    layer = layer_assign(node_ids, edges)
    # group nodes by layer
    by_layer = defaultdict(list)
    for n in node_ids:
        by_layer[layer[n]].append(n)
    max_layer = max(by_layer.keys()) if by_layer else 0
    max_per_layer = max(len(v) for v in by_layer.values()) if by_layer else 1

    NODE_W = 140
    NODE_H = 50
    LAYER_GAP = 90
    INTRA_GAP = 30
    MARGIN_X = 40
    MARGIN_Y = 60 + (30 if title else 10)

    # Wrap layers that are too wide: cap items per row to fit width budget.
    MAX_WIDTH = 720
    MAX_PER_ROW_H = max(1, (MAX_WIDTH - 2*MARGIN_X + INTRA_GAP) // (NODE_W + INTRA_GAP))
    MAX_PER_ROW_V = MAX_PER_ROW_H

    if direction in ('LR', 'RL'):
        # horizontal layout: cap each layer's vertical count too
        layer_rows = {}
        for l, ns in by_layer.items():
            # split into chunks if too many
            chunks = [ns[i:i+MAX_PER_ROW_V] for i in range(0, len(ns), MAX_PER_ROW_V)]
            layer_rows[l] = chunks
        max_chunk_h = max(len(c) for cs in layer_rows.values() for c in cs)
        # total cols = sum of chunks per layer
        total_cols = sum(len(cs) for cs in layer_rows.values())
        width = MARGIN_X*2 + total_cols * (NODE_W + LAYER_GAP) - LAYER_GAP
        height = MARGIN_Y + max_chunk_h * (NODE_H + INTRA_GAP) - INTRA_GAP + 40
        pos = {}
        col = 0
        for l in sorted(layer_rows.keys()):
            for chunk in layer_rows[l]:
                total_h = len(chunk) * (NODE_H + INTRA_GAP) - INTRA_GAP
                start_y = MARGIN_Y + (max_chunk_h * (NODE_H + INTRA_GAP) - INTRA_GAP - total_h) / 2
                for i, n in enumerate(chunk):
                    x = MARGIN_X + col * (NODE_W + LAYER_GAP)
                    y = start_y + i * (NODE_H + INTRA_GAP)
                    if direction == 'RL':
                        x = width - x - NODE_W
                    pos[n] = (x, y)
                col += 1
    else:
        # vertical layout: wrap layers if too wide
        layer_rows = {}
        for l, ns in by_layer.items():
            chunks = [ns[i:i+MAX_PER_ROW_H] for i in range(0, len(ns), MAX_PER_ROW_H)]
            layer_rows[l] = chunks
        max_chunk_w = max(len(c) for cs in layer_rows.values() for c in cs)
        # total rows = sum of chunks per layer
        total_rows = sum(len(cs) for cs in layer_rows.values())
        width = MARGIN_X*2 + max_chunk_w * (NODE_W + INTRA_GAP) - INTRA_GAP
        height = MARGIN_Y + total_rows * (NODE_H + LAYER_GAP) - LAYER_GAP + 40
        pos = {}
        row = 0
        for l in sorted(layer_rows.keys()):
            for chunk in layer_rows[l]:
                total_w = len(chunk) * (NODE_W + INTRA_GAP) - INTRA_GAP
                start_x = MARGIN_X + (max_chunk_w * (NODE_W + INTRA_GAP) - INTRA_GAP - total_w) / 2
                for i, n in enumerate(chunk):
                    x = start_x + i * (NODE_W + INTRA_GAP)
                    y = MARGIN_Y + row * (NODE_H + LAYER_GAP)
                    if direction == 'BT':
                        y = height - y - NODE_H
                    pos[n] = (x, y)
                row += 1

    width = int(min(max(width, 480), 900))   # hard cap 900 to avoid overflow
    height = int(max(height, 200))
    out = svg_header(width, height, title)
    arrow_id = title_id(title)

    # Edges first (under nodes)
    for src, dst, lbl in edges:
        if src not in pos or dst not in pos:
            continue
        x1, y1 = pos[src]
        x2, y2 = pos[dst]
        # connect right of src to left of dst, or bottom-to-top
        if direction in ('LR', 'RL'):
            sx, sy = x1 + NODE_W, y1 + NODE_H/2
            tx, ty = x2, y2 + NODE_H/2
        else:
            sx, sy = x1 + NODE_W/2, y1 + NODE_H
            tx, ty = x2 + NODE_W/2, y2
        out += svg_edge(int(sx), int(sy), int(tx), int(ty), lbl[:40] if lbl else "", arrow_id)

    # Nodes
    accents = ['accent', 'green', 'blue']
    for i, (nid, label) in enumerate(nodes.items()):
        if nid not in pos:
            continue
        x, y = pos[nid]
        a = accents[layer[nid] % 3]
        out += svg_node(int(x), int(y), NODE_W, NODE_H, label or nid, a)

    out += svg_footer()
    return out


def render_timeline(code: str) -> str:
    """Render mermaid timeline as horizontal timeline SVG."""
    lines = [l.strip() for l in code.strip().split('\n')[1:] if l.strip()]
    title = ""
    events = []  # list of (period, [items])
    cur_period = None
    for raw in lines:
        if raw.startswith('title'):
            title = raw.replace('title', '').strip()
        elif raw.startswith('section'):
            cur_period = raw.replace('section', '').strip()
            events.append((cur_period, []))
        elif ':' in raw:
            year, *items = raw.split(':')
            events.append((year.strip(), [':'.join(items).strip()]))
        else:
            if events:
                events[-1][1].append(raw)
            else:
                events.append((raw, []))

    if not events:
        return svg_header(720, 100, title) + svg_footer()

    n = len(events)
    # Cap width: wrap timeline into multiple rows if needed
    MAX_W = 900
    EVT_W = 160
    max_per_row = max(2, (MAX_W - 80) // EVT_W)        # at least 2 per row
    n_rows = (n + max_per_row - 1) // max_per_row
    width = min(MAX_W, max(480, 40 + min(n, max_per_row) * EVT_W))
    row_h = 130
    height = 60 + n_rows * row_h
    out = svg_header(width, height, title or "Timeline")
    for r in range(n_rows):
        y_base = 90 + r * row_h
        events_in_row = events[r*max_per_row:(r+1)*max_per_row]
        out += f'  <line x1="40" y1="{y_base}" x2="{width-40}" y2="{y_base}" stroke="var(--dia-stroke)" stroke-width="1.5"/>\n'
        for i, (period, items) in enumerate(events_in_row):
            x = 40 + i * EVT_W + EVT_W // 2
            out += f'  <circle cx="{x}" cy="{y_base}" r="6" fill="var(--dia-accent)"/>\n'
            out += f'  <text x="{x}" y="{y_base-20}" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="12" fill="var(--dia-accent-deep)" font-weight="600">{html.escape(period[:18])}</text>\n'
            for j, item in enumerate(items[:3]):
                out += f'  <text x="{x}" y="{y_base+25 + j*16}" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-style="italic" font-size="11" fill="var(--dia-stroke)">{html.escape(item[:24])}</text>\n'
    out += svg_footer()
    return out


def render_sequence(code: str) -> str:
    """Render mermaid sequenceDiagram as vertical message flow."""
    lines = [l.strip() for l in code.strip().split('\n')[1:] if l.strip()]
    title = ""
    participants = []
    messages = []  # (src, dst, label)
    for raw in lines:
        if raw.startswith('title'):
            title = raw.replace('title', '').strip()
        elif raw.startswith('participant'):
            p = raw.replace('participant', '').strip()
            if ' as ' in p:
                p_id, _, p_lbl = p.partition(' as ')
                participants.append((p_id.strip(), p_lbl.strip()))
            else:
                participants.append((p, p))
        else:
            m = re.match(r'(\w+)\s*(->>|-->>|->|-->)\s*(\w+)\s*:\s*(.*)', raw)
            if m:
                src, _, dst, lbl = m.group(1), m.group(2), m.group(3), m.group(4)
                # auto-discover participants
                for p_id in (src, dst):
                    if not any(pp[0] == p_id for pp in participants):
                        participants.append((p_id, p_id))
                messages.append((src, dst, lbl))

    if not participants or not messages:
        return svg_header(720, 100, title or "Sequence") + svg_footer()

    P_W = max(150, 720 // len(participants))
    width = max(480, 40 + len(participants) * P_W)
    height = 80 + 40 * len(messages) + 40
    out = svg_header(width, height, title or "Sequence Diagram")
    arrow_id = title_id(title or "seq")

    # participants top bar
    pid_to_x = {}
    for i, (p_id, p_lbl) in enumerate(participants):
        x = 40 + i * P_W + P_W // 2
        pid_to_x[p_id] = x
        out += f'  <rect x="{x-60}" y="60" width="120" height="30" rx="4" fill="var(--dia-bg-card)" stroke="var(--dia-stroke)" stroke-width="1.6"/>\n'
        out += f'  <text x="{x}" y="80" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-weight="600" font-size="13" fill="var(--dia-stroke)">{html.escape(p_lbl[:18])}</text>\n'
        # lifeline
        out += f'  <line x1="{x}" y1="90" x2="{x}" y2="{height-20}" stroke="var(--dia-stroke-soft)" stroke-width="1" stroke-dasharray="3,3"/>\n'

    # messages
    for i, (src, dst, lbl) in enumerate(messages):
        if src not in pid_to_x or dst not in pid_to_x:
            continue
        y = 110 + i * 40
        x1, x2 = pid_to_x[src], pid_to_x[dst]
        out += svg_edge(int(x1), int(y), int(x2), int(y), lbl[:40], arrow_id)

    out += svg_footer()
    return out


def render_fallback(code: str, type_name: str) -> str:
    """For pie/gitGraph etc., produce a labeled card with truncated source."""
    out = svg_header(720, 180, f"[{type_name}]")
    out += (
        '  <rect x="40" y="60" width="640" height="100" rx="4" fill="var(--dia-bg-card)" '
        'stroke="var(--dia-stroke)" stroke-width="1.6"/>\n'
        f'  <text x="360" y="110" text-anchor="middle" font-family="Fraunces, Georgia, serif" '
        f'font-style="italic" font-size="12" fill="var(--dia-stroke-soft)">'
        f'See accompanying text for details ({html.escape(type_name)})</text>\n'
    )
    out += svg_footer()
    return out


# ===== Top-level conversion =====
def convert_mermaid_block(code: str) -> str:
    """Take mermaid code, return SVG markdown chunk."""
    first_line = code.strip().split('\n', 1)[0].strip()
    type_lower = first_line.lower()
    if type_lower.startswith('graph') or type_lower.startswith('flowchart') or type_lower.startswith('statediagram'):
        parsed = parse_graph(code)
        if parsed and parsed['nodes']:
            return render_graph(parsed)
        return render_fallback(code, type_lower.split()[0])
    if type_lower.startswith('timeline'):
        return render_timeline(code)
    if type_lower.startswith('sequencediagram'):
        return render_sequence(code)
    # fallback for pie/gitGraph/etc.
    return render_fallback(code, type_lower.split()[0])


MERMAID_BLOCK_RE = re.compile(r'```mermaid\n(.*?)\n```', re.DOTALL)


def process_file(path: str, dry: bool = False) -> Tuple[int, int]:
    """Process one .md file. Returns (blocks_found, blocks_converted)."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return 0, 0
    matches = list(MERMAID_BLOCK_RE.finditer(content))
    if not matches:
        return 0, 0
    new_content = MERMAID_BLOCK_RE.sub(lambda m: convert_mermaid_block(m.group(1)), content)
    if not dry:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
    return len(matches), len(matches)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('targets', nargs='+', help='Files or directories to process')
    p.add_argument('--dry', action='store_true', help='Dry run, show counts only')
    args = p.parse_args()

    total_found = 0
    total_converted = 0
    files_touched = 0
    for target in args.targets:
        if os.path.isdir(target):
            for root, _, files in os.walk(target):
                for fn in files:
                    if fn.endswith('.md') or fn.endswith('.en.md'):
                        path = os.path.join(root, fn)
                        f, c = process_file(path, args.dry)
                        if f > 0:
                            files_touched += 1
                            print(f"  {os.path.relpath(path)}: {c}/{f} blocks")
                        total_found += f
                        total_converted += c
        elif os.path.isfile(target):
            f, c = process_file(target, args.dry)
            print(f"{target}: {c}/{f} blocks")
            total_found += f
            total_converted += c
    print(f"\nTotal: {total_converted}/{total_found} mermaid blocks converted in {files_touched} files")
    print("(dry run, no changes written)" if args.dry else "(changes written)")


if __name__ == '__main__':
    main()
