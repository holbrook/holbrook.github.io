---
layout: post
$if(title)$title: $title$$endif$
$if(date-meta)$date: $date-meta$$endif$
$if(update)$update: $update$$endif$
$if(description)$description: $description$$endif$
$if(category)$category: $category$$endif$
$if(tags)$tags: [$for(tags)$$tags$, $endfor$]$endif$
---
$if(toc)$
<div id="$idprefix$TOC">
<h3>目录</h3>
$toc$
</div>
$endif$
$body$
$for(include-after)$
$include-after$
$endfor$
