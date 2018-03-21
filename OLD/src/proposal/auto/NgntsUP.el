(TeX-add-style-hook
 "NgntsUP"
 (lambda ()
   (TeX-add-to-alist 'LaTeX-provided-class-options
                     '(("article" "10pt" "a4paper")))
   (TeX-add-to-alist 'LaTeX-provided-package-options
                     '(("hyperref" "xetex" "colorlinks=true" "CJKbookmarks=true" "linkcolor=blue" "urlcolor=blue" "menucolor=blue")))
   (TeX-run-style-hooks
    "latex2e"
    "article"
    "art10"
    "graphicx"
    "xcolor"
    "xeCJK"
    "lmodern"
    "verbatim"
    "fixltx2e"
    "longtable"
    "float"
    "tikz"
    "wrapfig"
    "soul"
    "textcomp"
    "listings"
    "geometry"
    "algorithm"
    "algorithmic"
    "marvosym"
    "wasysym"
    "latexsym"
    "natbib"
    "fancyhdr"
    "hyperref"
    "fontspec"
    "xunicode"
    "xltxtra")
   (TeX-add-symbols
    '("alert" 1)
    '("mono" 1)
    "fontnamemono")
   (LaTeX-add-labels
    "sec-1"
    "sec-1-1"
    "sec-2"
    "sec-3"
    "sec-4"
    "sec-4-1"
    "sec-4-2"
    "sec-5"
    "sec-5-1"
    "sec-5-2"
    "sec-5-3"
    "sec-5-3-1"
    "sec-5-4"
    "sec-5-5"
    "sec-5-6"
    "sec-6"
    "sec-7"
    "sec-8")))

