help: 
	@echo 'copy: copy images, css, js etc..'
	@echo 'uml: build .uml files in graph/'
	@echo 'dot: build .dot files in graph/'
	@echo 'md: build .md file'
	@echo 'all: all above'
	@echo 'todo: bower, clean'
all: copy uml dot md 


copy:
	cp images/* dist/assets/
	cp css/* dist/assets/

uml:
	plantuml ./graph/*.uml -o ../dist/assets/ 

dot:
	@for file in `ls graph/*.dot `; do \
		( echo; echo generating $$file ; dot $$file -T png -O ) \
		done;
	mv graph/*.png dist/assets/

md:
	cd dist; pandoc -s --slide-level=2 -t revealjs -c assets/beige.css ../design.slide.md -o design.slide.html

#clean: 
#	rm -rf dist; cd app; python setup.py clean

bower:
	echo "TODO:bower download reveal.js to dist"

