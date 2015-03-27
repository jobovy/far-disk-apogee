RM=/bin/rm -vf
FIGS= marshall_ext.eps green_ext.eps \
	ext27_marshall.eps ext34_marshall.eps ext64_marshall.eps \
	ext27_marshall_thresh.eps ext34_marshall_thresh.eps \
	ext64_marshall_thresh.eps

all: bovy_apogee2_anc15.pdf

%.pdf: %.ps
	ps2pdf -dMaxSubsetPct=100 -dCompatibilityLevel=1.2 -dSubsetFonts=true -dEmbedAllFonts=true $<

%.ps: %.dvi
	dvips -t letter $< -o

%.dvi: %.tex $(FIGS)
	latex -shell-escape $<
	latex -shell-escape $<
	- bash -c " ( grep Rerun $*.log && latex -shell-escape $< ) || echo noRerun "
	- bash -c " ( grep Rerun $*.log && latex -shell-escape $< ) || echo noRerun "

%_ext.eps: %_ext.ps Makefile
	cp $< tmp.ps
	echo "1,\$$s/%%BoundingBox: 3 251 608 540/%%BoundingBox: 33 314 521 453/g" > edcmd
	echo "w" >> edcmd
	ed $< < edcmd
	cp $< $@
	cp tmp.ps $< 
	rm edcmd tmp.ps

ext%.eps: ext%.ps Makefile
	cp $< tmp.ps
	echo "1,\$$s/%%BoundingBox: 121 215 486 576/%%BoundingBox: 119 218 454 542/g" > edcmd
	echo "w" >> edcmd
	ed $< < edcmd
	cp $< $@
	cp tmp.ps $< 
	rm edcmd tmp.ps

%.dvi: %.tex

.PHONY: clean spotless

clean:
	$(RM) *.aux *.log

spotless: clean
	$(RM) ms.pdf