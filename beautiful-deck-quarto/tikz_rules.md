# TikZ Rules — Measurement-First Diagrams

The core principle: **TikZ collisions are prevented by measurement at write-time, not repaired at audit-time.** A diagram built without explicit dimensions will need a repair pass. A diagram built with declared dimensions and a coordinate map usually renders correctly the first time.

This file is loaded by reference from `SKILL.md`. Apply when generating any TikZ block.

---

## The protocol

### 1. Declare node dimensions explicitly

```latex
% NO — variable size, depends on text length
\node (A) {Some label};

% YES — fixed dimensions, predictable layout
\node[draw, minimum width=3cm, minimum height=1cm, align=center] (A)
  {Some\\ label};
```

When dimensions are explicit, you can place edges with confidence that they will not pierce the node body or terminate inside the text.

### 2. Build a coordinate map before drawing edges

Before any `\draw` command, lay down all nodes at named coordinates. Verify the layout is what you intended *as nodes only*, then add edges. This separates "where things are" from "how things connect" and makes errors obvious.

```latex
% Step A: place nodes
\node[<style>] (start)   at (0, 0)  {Start};
\node[<style>] (middle)  at (4, 0)  {Middle};
\node[<style>] (end)     at (8, 0)  {End};

% Step B: edges, only after layout is confirmed
\draw[->] (start) -- (middle);
\draw[->] (middle) -- (end);
```

### 3. Edge-label gap calculations

Labels on edges (`node[midway, above] {label}`) collide with arrow heads when the edge is short. For edges shorter than 2cm, use `node[pos=0.4]` or `node[pos=0.6]` to push the label off the midpoint, or place the label as a separate node anchored to the edge.

### 4. Boundary clearances

The slide's text width on a 16:9 Beamer frame at default Quarto settings is approximately 12cm. Diagrams wider than 11cm risk overflow. Either constrain `xmin`/`xmax` of node coordinates to fit, or wrap the whole `tikzpicture` in `\resizebox{\textwidth}{!}{...}`.

Vertical: a frame's content area is roughly 6cm tall after frame title and footer. Diagrams taller than this overflow into the footer.

### 5. Bézier curve depths

Curved edges in `\draw [bend left=N]` form: `N=15` is subtle, `N=30` is a clear arc, `N>45` produces a deep curve that often crosses other elements. For parallel edges between the same two nodes (e.g., showing a bidirectional flow), use `bend left=20` and `bend right=20` together — symmetric, predictable.

### 6. Cross-slide consistency

When the same conceptual element appears on multiple slides (e.g., a "data" box that recurs through a methods walkthrough), copy the exact node definition. Do not eyeball "approximately the same".

---

## Canonical templates

### Pipeline diagram (left-to-right, n boxes)

```latex
\begin{tikzpicture}[
  node distance=1.2cm,
  box/.style={draw=wehiTealDark, fill=wehiTealTint, minimum width=2.5cm,
              minimum height=1cm, align=center, rounded corners=2pt},
  arrow/.style={->, thick, wehiTealDark}
]
  \node[box] (n1) {Step 1};
  \node[box, right=of n1] (n2) {Step 2};
  \node[box, right=of n2] (n3) {Step 3};
  \draw[arrow] (n1) -- (n2);
  \draw[arrow] (n2) -- (n3);
\end{tikzpicture}
```

### Two-state contrast (correct vs. wrong)

```latex
\begin{tikzpicture}[
  good/.style={draw=wehiGreen, fill=wehiGreen!10, minimum width=4cm,
               minimum height=2cm, align=center},
  bad/.style={draw=wehiOrange, fill=wehiOrange!10, minimum width=4cm,
              minimum height=2cm, align=center}
]
  \node[good] (a) at (0, 0) {Correct\\ interpretation};
  \node[bad]  (b) at (5, 0) {Wrong\\ interpretation};
\end{tikzpicture}
```

### Hierarchy / tree

Use `\usetikzlibrary{trees}` and `child` syntax — far less error-prone than manual coordinates for branching structures.

```latex
\begin{tikzpicture}[
  level distance=1.5cm,
  level 1/.style={sibling distance=4cm},
  level 2/.style={sibling distance=2cm},
  every node/.style={draw=wehiTealDark, fill=wehiTealTint, rounded corners=2pt,
                     minimum width=1.8cm, align=center}
]
  \node {Root}
    child { node {A}
      child { node {A1} }
      child { node {A2} }
    }
    child { node {B}
      child { node {B1} }
    };
\end{tikzpicture}
```

---

## Things that fail silently

LaTeX compiles successfully even when:
- A node is placed at `(5, 3)` but you meant `(3, 5)`
- An edge points to the wrong target because of a typo in the node name
- A label sits on top of another label

The compile log will not warn you. **You must look at the rendered PDF.** If you cannot view PDFs, ask the user to look or describe what they see.

When the user reports a TikZ collision, do not respond by tweaking and recompiling blindly. Re-derive the coordinates. Print the layout as text to verify. Then fix.
