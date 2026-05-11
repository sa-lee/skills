# Quarto-Beamer Patterns

Quarto sits between markdown and LaTeX. Most slide content can be written as plain markdown headers and lists, but some Beamer features require raw LaTeX or fenced divs. This file documents the idioms.

## Contents

- [Slide structure](#slide-structure)
- [Sections](#sections)
- [Two-column layouts](#two-column-layouts)
- [Callout blocks (the teal-tint key result panel)](#callout-blocks-the-teal-tint-key-result-panel)
- [Emphasis (orange — max one per slide)](#emphasis-orange--max-one-per-slide)
- [Math](#math)
- [TikZ blocks](#tikz-blocks)
- [Code-generated figures](#code-generated-figures)
- [Speaker notes](#speaker-notes)
- [Citations](#citations)
- [What NOT to do](#what-not-to-do)

---

## Slide structure

Each `##` heading starts a new slide (Beamer frame). The text after `##` becomes the frame title.

```markdown
## Treatment increased survival by 34%

Body content here.

## Hazard ratio held across pre-specified subgroups

Next slide's content.
```

To suppress the frame title (for a quote slide or full-bleed image), use:

```markdown
## {.plain}

Title-less content.
```

---

## Sections

A `#` heading triggers `\section{...}` which fires the section divider template (gradient top band) defined in `preamble.tex`. Use sparingly — three to five sections in a 30-slide deck.

```markdown
# Methods

## Frame title within methods section
```

---

## Two-column layouts

Quarto supports column fenced divs. Use this pattern for slides with a figure on one side and explanation on the other.

```markdown
## Hazard ratio: 0.66

::: {.columns}

::: {.column width="45%"}
![](figures/km_curve.pdf)
:::

::: {.column width="55%"}
- Pre-specified primary endpoint
- Stratified Cox model
- Held across all subgroups
:::

:::
```

---

## Callout blocks (the teal-tint key result panel)

Beamer's native `\begin{block}` is wired to the WEHI teal-tint via `preamble.tex`. Use a fenced div or a raw block:

```markdown
::: {.block}
### Hazard ratio
**0.66** (95% CI: 0.51–0.86, p = 0.002)
:::
```

Or for finer control, raw LaTeX:

```{=latex}
\begin{block}{Hazard ratio}
\textbf{0.66} (95\% CI: 0.51--0.86, $p = 0.002$)
\end{block}
```

---

## Emphasis (orange — max one per slide)

Inline orange:

```markdown
Treatment increased survival by [34%]{.emph}
```

Define `.emph` in the preamble (already in WEHI preamble): or use raw LaTeX inline:

```markdown
Treatment increased survival by \textcolor{wehiOrange}{34%}
```

The first form is cleaner; the second is more portable. Either works.

---

## Math

Quarto passes LaTeX math through. Display math:

```markdown
$$
\hat{\beta} = (X^\top X)^{-1} X^\top y
$$
```

Inline: `$y_i = \alpha + \beta x_i + \varepsilon_i$`

For equations that carry the argument, give them their own slide. Don't crowd math into a slide also doing other work.

---

## TikZ blocks

TikZ goes in raw LaTeX blocks. **Always** wrap in `{=latex}`:

````markdown
## Pipeline overview

```{=latex}
\begin{center}
\begin{tikzpicture}[node distance=1.2cm,
  box/.style={draw=wehiTealDark, fill=wehiTealTint,
              minimum width=2.5cm, minimum height=1cm,
              align=center, rounded corners=2pt}]
  \node[box] (a) {Raw FASTQ};
  \node[box, right=of a] (b) {Aligned BAM};
  \node[box, right=of b] (c) {Variants};
  \draw[->, thick] (a) -- (b);
  \draw[->, thick] (b) -- (c);
\end{tikzpicture}
\end{center}
```
````

The `\begin{center}` wrapper centers the figure on the slide.

---

## Code-generated figures

For data graphics, use a Quarto code chunk with `fig-format: pdf`:

````markdown
## Effect held across age strata

```{r}
#| fig-width: 8
#| fig-height: 4.5
#| fig-format: pdf
#| echo: false

library(ggplot2)
wehi_cat <- c("#FF6105", "#ED5E82", "#9F71E5", "#578CFF", "#4EA749")

ggplot(data, aes(x = age_group, y = hr, color = subgroup)) +
  geom_pointrange(aes(ymin = ci_low, ymax = ci_high)) +
  scale_color_manual(values = wehi_cat) +
  geom_hline(yintercept = 1, linetype = "dashed", color = "grey50") +
  theme_minimal(base_family = "Arial") +
  labs(x = "Age group", y = "Hazard ratio (95% CI)")
```
````

For Python figures, swap `{r}` for `{python}` and use matplotlib with the same palette.

**For CVD-safe plots** (subgroup comparisons by ancestry, sex, condition), use Okabe-Ito instead:

```r
okabe_ito <- c("#E69F00", "#56B4E9", "#009E73", "#F0E442",
               "#0072B2", "#D55E00", "#CC79A7", "#000000")
```

---

## Speaker notes

The user has opted out of speaker notes. Do not generate them. If the user changes their mind later, Quarto-Beamer notes go in fenced divs:

```markdown
::: {.notes}
Speaker note here. Will not appear on slide.
:::
```

This requires `format: beamer: notes: true` in YAML. Default off.

---

## Citations

If a `.bib` is linked in YAML (`bibliography: refs.bib`), Quarto handles `[@smith2024]` -> `(Smith 2024)` automatically. By Rhetoric of Decks default, **strip these** from slide bodies and place spoken-attribution form (small grey upper right) only where attribution genuinely matters on screen.

For a single small attribution in the corner of a slide:

```markdown
## Treatment increased survival by 34%

[Content]

\hfill \textcolor{wehiGrey50}{\small Smith et al. 2024}
```

The references slide at the end is generated automatically by Quarto from cited keys.

---

## What NOT to do

**Don't** use HTML tags in Quarto-Beamer (`<br>`, `<div class="...">`). They render as literal text. Use fenced divs or raw LaTeX.

**Don't** rely on `incremental: true` for line-by-line reveals unless the user asks for it. Auto-incremental builds usually fail the "one idea per slide" test — if you need to reveal across multiple beats, those beats are different slides.

**Don't** use the default `theme: AnnArbor` or other built-in Beamer themes. The WEHI preamble overrides templates directly; loading another theme will conflict.

**Don't** put `<image>` references with relative paths that won't resolve at render time. Quarto renders from the project root; figure paths should be relative to that.
