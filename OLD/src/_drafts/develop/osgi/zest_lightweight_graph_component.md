---
layout: post
title: "Zest: Eclipse中的轻量级绘图组件"
description: ""
category: 软件开发
tags: [eclipse]
lastmod: 
---

尽管Eclipse体系中的GMF、GEF实现了强大的绘图和基于图形的编辑功能，但是这两个框架过于厚重，学习成本也比较高。如果只是实现类似展现拓扑图这样的功能，大可不必使用上述框架(Framework)，仅仅使用`Zest`组件(Component)即可。

与GMF类似，[Eclipse Zest]() 基于 SWT/Draw2D ，可以在JFace视图中使用，支持模型和展现的分离。

# 图(Graph)模型




