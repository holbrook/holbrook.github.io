pandoc -t html5 \
--template=../../templates/pandoc/template-revealjs.html \
--self-contained \
--standalone \
--section-divs \
--variable theme="beige" \
--variable transition="linear" \
 ../source/_slides/cloud_computing.md -o cloud_computing.html
