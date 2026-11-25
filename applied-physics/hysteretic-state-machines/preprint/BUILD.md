# Build the manuscript

From this directory, use a standard TeX Live installation with Latin Modern, BibTeX, xurl, and the packages declared in the source. Papers 1, 5 and 7 use native TikZ figures.

```sh
pdflatex -interaction=nonstopmode -halt-on-error physical_resource_complexity_hysteretic_state_machines.tex
bibtex physical_resource_complexity_hysteretic_state_machines
pdflatex -interaction=nonstopmode -halt-on-error physical_resource_complexity_hysteretic_state_machines.tex
pdflatex -interaction=nonstopmode -halt-on-error physical_resource_complexity_hysteretic_state_machines.tex
```

See the [project page](../README.md) for the research materials and verification instructions.
