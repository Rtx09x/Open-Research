# Build the manuscript

From this directory, use a standard TeX Live installation with Latin Modern, BibTeX, xurl, and the packages declared in the source. Papers 1, 5 and 7 use native TikZ figures.

```sh
pdflatex -interaction=nonstopmode -halt-on-error deterministic_online_bin_packing.tex
bibtex deterministic_online_bin_packing
pdflatex -interaction=nonstopmode -halt-on-error deterministic_online_bin_packing.tex
pdflatex -interaction=nonstopmode -halt-on-error deterministic_online_bin_packing.tex
```

See the [project page](../README.md) for the research materials and verification instructions.
