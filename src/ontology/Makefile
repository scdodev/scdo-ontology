# ----------------------------------------
# Standard Constants
# ----------------------------------------
# these can be overwritten on the command line

OBO=http://purl.obolibrary.org/obo
ONT=scdo
BASE=$(OBO)/$(ONT)
SRC=$(ONT)-edit.owl
SRC_OBO=$(ONT)-edit-with-obo-ids.owl
RELEASEDIR=../..
ROBOT= ../../bin/robot
OWLTOOLS= ../../bin/owltools
USECAT= --use-catalog
SPARQLDIR = ../sparql
PREFIX="SCDO: http://scdontology.h3abionet.org/ontology/SCDO_"
# ----------------------------------------
# Top-level targets
# ----------------------------------------

all: sparql_test $(ONT).owl $(ONT).obo $(ONT)_hpo_merged.owl scdo_hp_bridge.owl results/hp_module.owl imports/hp_import.txt mappings/scdo-sssom-xrefs.tsv
test: sparql_test all

prepare_release: all
	cp $(ONT).owl scdo_hpo_merged.owl $(RELEASEDIR) &&\
	mkdir -p $(RELEASEDIR)/imports $(RELEASEDIR)/mappings &&\
	cp imports/*.owl $(RELEASEDIR)/imports &&\
	cp mappings/*.tsv $(RELEASEDIR)/mappings &&\
	git add $(RELEASEDIR)/imports/*.owl &&\
	echo "Release files are now in $(RELEASEDIR) - now you should commit, push and make a release on github"

# ----------------------------------------
# Main release targets
# ----------------------------------------

TEMPLATES=caused_by causes_condition causes_molecular_phenotype causes_or_contributes_to_condition causes_or_contributes_to_molecular_phenotype code_requires_phenotype collects contributes_to_genotype diagnosed_by diagnosed_using_measurement diagnosed_using_tool has_answer_option has_answer_standard_unit has_causal_genotype has_causal_molecular_phenotype has_causal_or_contributing_genetic_variation has_clinical_code has_contributing_genetic_variation has_essential_measure has_manifestation has_mode_of_inheritance has_output_measurement has_possible_finding induced_by in_guideline is_question_type measures modified_by modifies obtained_via_diagnostic_tool output_of_diagnostic_device treated_with treats used_by_diagnostic_tool uses_diagnostic_device
TEMPLATE_FILES = $(patsubst %, templates/%.tsv, $(TEMPLATES))
# by default we use Elk to perform a reason-relax-reduce chain
# after that we annotate the ontology with the release versionInfo
$(ONT).owl: $(TEMPLATE_FILES) mappings/scdo-sssom-xrefs-rename.tsv
	$(ROBOT) template --input $(SRC) $(patsubst %, --merge-before --prefix $(PREFIX) --template %, $(TEMPLATE_FILES)) \
		query --update $(SPARQLDIR)/sssom-xrefs-rename-scdoid.ru \
		reason -s true -m false --exclude-tautologies structural -r ELK \
		rename --prefix "ExO: http://purl.obolibrary.org/obo/ExO_" --prefix "GSSO: http://purl.obolibrary.org/obo/GSSO_" --prefix "SCDO: http://scdontology.h3abionet.org/ontology/SCDO_" --mappings mappings/scdo-sssom-xrefs-rename.tsv --allow-missing-entities true \
		annotate -V $(BASE)/releases/`date +%Y-%m-%d`/$(ONT).owl convert -f owl -o $@

#$(ONT).owl: $(SRC) /home/gaston/SCDO-Ontologygithub/templates/AllTermsFinal.tsv /home/gaston/SCDO-Ontologygithub/templates/Topology.tsv templates/haemoglobinopathies.tsv
#	$(ROBOT) template --input $(SRC) \
--merge-before --prefix $(PREFIX) --template /home/gaston/SCDO-Ontologygithub/templates/AllTermsFinal.tsv template \
--merge-before --prefix $(PREFIX) --template /home/gaston/SCDO-Ontologygithub/templates/Topology.tsv template \
--merge-before --prefix $(PREFIX) --template templates/haemoglobinopathies.tsv reason -s true -m false -r ELK annotate -V $(BASE)/releases/`date +%Y-%m-%d`/$(ONT).owl -o $@

$(ONT)_hpo_merged.owl: $(SRC) scdo_hp_bridge.owl results/hp_module.owl
	$(ROBOT) merge --input $(SRC) --input scdo_hp_bridge.owl --input results/hp_module.owl reason -s true -m false -r ELK annotate -V $(BASE)/releases/`date +%Y-%m-%d`/$(ONT)_hpo_merged.owl -o $@

$(ONT).obo: $(ONT).owl
	$(ROBOT) convert -i $(ONT).owl --check false -f obo -o $@.tmp.obo && grep -v ^owl-axioms $@.tmp.obo > $@ && rm $@.tmp.obo

# ----------------------------------------
# Import modules
# ----------------------------------------
# Most ontologies are modularly constructed using portions of other ontologies
# These live in the imports/ folder
# These can be regenerated with make all_imports

imports/hp_import.txt: $(ONT).owl imports/hp.owl
	$(ROBOT) merge --input imports/hp.owl --input $(ONT).owl query --select $(SPARQLDIR)/get_hpo_mappings.sparql imports/hp_import.txt 

results/hp_module.owl: imports/hp_import.txt
	$(ROBOT) extract  --method BOT --input imports/hp.owl --term-file imports/hp_import.txt --output results/hp_module.owl

scdo_hp_bridge.owl: $(ONT).owl imports/hp.owl
	$(ROBOT) query --input $(ONT).owl --format ttl --construct $(SPARQLDIR)/construct_hpo_bridge.sparql scdo_hp_bridge.owl


# ----------------------------------------
# Release
# ----------------------------------------
# copy from staging area (this directory) to top-level
release: $(ONT).o*
	cp $^ $(RELEASEDIR) && cp imports/* $(RELEASEDIR)/imports

# ----------------------------------------
# Sparql queries: Q/C
# ----------------------------------------

# these live in the ../sparql directory, and have suffix -violation.sparql
# adding the name here will make the violation check live
VCHECKS = equivalent-classes trailing-whitespace owldef-self-reference xref-syntax nolabels

# run all violation checks
VQUERIES = $(foreach V,$(VCHECKS),$(SPARQLDIR)/$V-violation.sparql)
sparql_test: $(SRC)
	$(ROBOT) verify -i $(SRC) --queries $(VQUERIES) -O reports/

# ----------------------------------------
# Sparql queries: Reports
# ----------------------------------------

REPORTS = basic-report class-count-by-prefix edges xrefs obsoletes synonyms
REPORT_ARGS = $(foreach V,$(REPORTS),-s $(SPARQLDIR)/$V.sparql reports/$V.tsv)
all_reports: $(SRC)
	$(ROBOT) query -f tsv -i $(SRC) $(REPORT_ARGS)
	
	
# ----------------------------------------
# SSSOM file
# ----------------------------------------

mappings/:
	mkdir -p $@

mappings/scdo-sssom-xrefs.tsv: scdo-edit.owl | mappings/
	$(ROBOT) query -i scdo-edit.owl -f tsv --query $(SPARQLDIR)/sssom-xrefs.sparql $@
	sed -i -E 's/[<>?"]//g' $@
	
mappings/scdo-sssom-xrefs-rename.tsv: $(SRC) | mappings/
	$(ROBOT) query -i $(SRC) -f tsv --query $(SPARQLDIR)/sssom-xrefs-rename.sparql $@
	sed -i -E 's/[<>?"]//g' $@

obo_release:
	make all release