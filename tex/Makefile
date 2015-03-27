RM=/bin/rm -vf

all: bovy_apogee2_anc15.pdf

%.pdf: %.ps
	ps2pdf -dMaxSubsetPct=100 -dCompatibilityLevel=1.2 -dSubsetFonts=true -dEmbedAllFonts=true $<

%.ps: %.dvi
	dvips -t letter $< -o

%.dvi: %.tex
	latex $<
	latex $<
	- bash -c " ( grep Rerun $*.log && latex $< ) || echo noRerun "
	- bash -c " ( grep Rerun $*.log && latex $< ) || echo noRerun "

.PHONY: clean spotless

clean:
	$(RM) *.aux *.log

spotless: clean
	$(RM) ms.pdf