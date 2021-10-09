pdf:
	pandoc -f markdown manifesto.md -o manifesto.pdf

github:
	mkdir -p build
	./githubiffy.py manifesto.md
	pandoc -f markdown -t gfm build/manifesto.gf.md -o README.md

clean:
	rm build/*
	rm manifesto.pdf
	rm README.md
