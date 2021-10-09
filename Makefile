all: pdf github
.PHONY: all clean

pdf:
	mkdir -p build
	pandoc -f markdown manifesto.md -t latex -V colorlinks=true -s -o build/manifesto.tex
	pdflatex --output-directory=build build/manifesto.tex
	mv build/manifesto.pdf manifesto.pdf

github:
	mkdir -p build
	./githubiffy.py manifesto.md
	pandoc -f markdown -t gfm build/manifesto.gf.md -o README.md

clean:
	rm build/*
	rm manifesto.pdf
	rm README.md
