% Embedded diagrams in pandoc's markdown
% Jakob Voss

# Introduction

**mddia** is a simple, dirty Perl script to preprocess and convert diagrams
embedded in pandoc's markdown syntax. This is a temporary hack because of
lacking Haskell skills. Anyway, the script may be rewritten, but the underlying
principles and data format will stay.[^1] Up to now the script supports the
following diagram types:

[^1]: A better implementation would be based on pandoc's scripting API:
<http://johnmacfarlane.net/pandoc/scripting.html>. See the dot plugin at
<http://gitit.net/> for how to dot it.

# Examples

## Input source code

``` {.dot .Grankdir:LR}
digraph {
  A -> B -> C;
  A -> C;
}
```
## Generated diagrams

~~~~ {.dot .Grankdir:LR}
digraph {
  A -> B -> C;
  A -> C;
}
~~~~
