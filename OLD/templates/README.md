writing
=======
# metadata

http://pandoc.org/demo/example9/pandocs-markdown.html



## yaml_metadata_block

```yaml
---
title:  'This is the title: it contains a colon'
author:
- name: Author One
  affiliation: University of Somewhere
  - name: Author Two
    affiliation: University of Nowhere
tags: [nothing, nothingness]
abstract: |
  This is the abstract.

  It consists of two paragraphs.
  ...
---
```

useage:

```bash
pandoc chap1.md chap2.md chap3.md metadata.yaml -s -o book.html
```

##  pandoc_title_block

```pandoc
% title
% author(s) (separated by semicolons)
% date
```


## citations extention

```
---
references:
- id: fenner2012a
  title: One-click science marketing
    author:
      - family: Fenner
        given: Martin
        container-title: Nature Materials
        volume: 11
        URL: 'http://dx.doi.org/10.1038/nmat3283'
        DOI: 10.1038/nmat3283
        issue: 4
        publisher: Nature Publishing Group
        page: 261-263
        type: article-journal
        issued:
        year: 2012
        month: 3
---
```


