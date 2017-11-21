
# This Makefile is for use by the scdo Release Manager.
#
# requirements: Oort (http://code.google.com/p/owltools/wiki/OortIntro)
#
# To make a release, type 'make release' in this directory

OBO = http://purl.obolibrary.org/obo

initial-build: scdo.obo
build: scdo.obo minidiff
release: scdo.obo diff

# all release files are derived from the editors version.
# we use the default Oort setup (hermit as reasoner)
scdo.obo: scdo-edit.owl
	ontology-release-runner $< --allow-overwrite --asserted --simple

# ----------------------------------------
# Imports
# ----------------------------------------
all_imports: imports/go_import.owl imports/pato_import.owl

imports/%_import.owl: scdo-edit.owl
	owltools $< $(OBO)/$*.owl --add-imports-from-supports --extract-module -s $(OBO)/$*.owl -c --extract-mingraph  --set-ontology-id $(OBO)/go/extensions/$@ -o $@

# ----------------------------------------
# Diffs
# ----------------------------------------

# 
diff: scdo.obo
	cd diffs && touch scdo-diff && rm scdo-*diff* && make

# Minidiff: intra-release differences
minidiff: scdo.obo
	cd diffs  && touch scdo-diff && rm scdo-*diff* && make TGTS='html txt' SRC=../scdo.obo && mail -s scdo-diffs RELEASE-MANAGER@FOO.BAR < scdo-combined-diff.txt

