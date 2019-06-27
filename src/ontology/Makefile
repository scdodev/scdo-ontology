# ----------------------------------------
# Standard Constants
# ----------------------------------------
# these can be overwritten on the command line

OBO=http://purl.obolibrary.org/obo
ONT=scdo
BASE=$(OBO)/$(ONT)
SRC=$(ONT)-edit.owl
RELEASEDIR=../..
ROBOT= ../../bin/robot
OWLTOOLS= ../../bin/owltools
USECAT= --use-catalog
SPARQLDIR = ../sparql
PREFIX="SCDO: http://scdontology.h3abionet.org/ontology/SCDO_"
# ----------------------------------------
# Top-level targets
# ----------------------------------------

all: sparql_test $(ONT).owl $(ONT).obo $(ONT)_hpo_merged.owl scdo_hp_bridge.owl results/hp_module.owl imports/hp_import.txt
test: sparql_test all
prepare_release: all
	cp $(ONT).owl scdo_hpo_merged.owl $(RELEASEDIR) &&\
	mkdir -p $(RELEASEDIR)/imports &&\
	cp imports/*.owl $(RELEASEDIR)/imports &&\
	git add $(RELEASEDIR)/imports/*.owl &&\
	echo "Release files are now in $(RELEASEDIR) - now you should commit, push and make a release on github"

# ----------------------------------------
# Main release targets
# ----------------------------------------

# by default we use Elk to perform a reason-relax-reduce chain
# after that we annotate the ontology with the release versionInfo
<<<<<<< HEAD
$(ONT).owl: $(SRC) templates/caused_by.tsv templates/causes_condition.tsv templates/causes_molecular_phenotype.tsv templates/causes_or_contributes_to_condition.tsv templates/causes_or_contributes_to_molecular_phenotype.tsv templates/contributes_to_genotype.tsv templates/diagnosed_by.tsv templates/diagnosed_using_measurement.tsv templates/diagnosed_using_tool.tsv templates/has_causal_genotype.tsv templates/has_causal_or_contributing_genetic_variation.tsv templates/has_clinical_code.tsv templates/has_contributing_genetic_variation.tsv templates/has_essential_measure.tsv templates/has_manifestation.tsv templates/has_molecular_phenotype.tsv templates/has_output_measurement.tsv templates/has_phenotype.tsv templates/has_risk_factor.tsv templates/induced_by.tsv templates/in_guideline.tsv templates/inheritance.tsv templates/measures.tsv templates/modified_by.tsv templates/modifies.tsv templates/obtained_via_diagnostic_tool.tsv templates/output_by_diagnostic_device.tsv templates/risk_factor_for.tsv templates/treated_with.tsv templates/used_by_diagnostic_tool.tsv templates/uses_diagnostic_device.tsv templates/has_causal_molecular_phenotype.tsv templates/treats.tsv
	$(ROBOT) template --input $(SRC) --merge-before --prefix $(PREFIX) --template templates/caused_by.tsv --merge-before --prefix $(PREFIX) --template templates/causes_condition.tsv --merge-before --prefix $(PREFIX) --template templates/causes_molecular_phenotype.tsv --merge-before --prefix $(PREFIX) --template templates/causes_or_contributes_to_condition.tsv --merge-before --prefix $(PREFIX) --template templates/causes_or_contributes_to_molecular_phenotype.tsv --merge-before --prefix $(PREFIX) --template templates/contributes_to_genotype.tsv --merge-before --prefix $(PREFIX) --template templates/diagnosed_by.tsv --merge-before --prefix $(PREFIX) --template templates/diagnosed_using_measurement.tsv --merge-before --prefix $(PREFIX) --template templates/diagnosed_using_tool.tsv --merge-before --prefix $(PREFIX) --template templates/has_causal_genotype.tsv --merge-before --prefix $(PREFIX) --template templates/has_causal_or_contributing_genetic_variation.tsv --merge-before --prefix $(PREFIX) --template templates/has_clinical_code.tsv --merge-before --prefix $(PREFIX) --template templates/has_contributing_genetic_variation.tsv --merge-before --prefix $(PREFIX) --template templates/has_essential_measure.tsv --merge-before --prefix $(PREFIX) --template templates/has_manifestation.tsv --merge-before --prefix $(PREFIX) --template templates/has_molecular_phenotype.tsv --merge-before --prefix $(PREFIX) --template templates/has_output_measurement.tsv --merge-before --prefix $(PREFIX) --template templates/has_phenotype.tsv --merge-before --prefix $(PREFIX) --template templates/has_risk_factor.tsv --merge-before --prefix $(PREFIX) --template templates/induced_by.tsv --merge-before --prefix $(PREFIX) --template templates/in_guideline.tsv --merge-before --prefix $(PREFIX) --template templates/inheritance.tsv --merge-before --prefix $(PREFIX) --template templates/measures.tsv --merge-before --prefix $(PREFIX) --template templates/modified_by.tsv --merge-before --prefix $(PREFIX) --template templates/modifies.tsv --merge-before --prefix $(PREFIX) --template templates/obtained_via_diagnostic_tool.tsv --merge-before --prefix $(PREFIX) --template templates/output_by_diagnostic_device.tsv --merge-before --prefix $(PREFIX) --template templates/risk_factor_for.tsv --merge-before --prefix $(PREFIX) --template templates/used_by_diagnostic_tool.tsv --merge-before --prefix $(PREFIX) --template templates/uses_diagnostic_device.tsv --merge-before --prefix $(PREFIX) --template templates/treated_with.tsv --merge-before --prefix $(PREFIX) --template templates/has_causal_molecular_phenotype.tsv --merge-before --prefix $(PREFIX) --template templates/treats.tsv reason -s true -m false -r ELK annotate -V $(BASE)/releases/`date +%Y-%m-%d`/$(ONT).owl -o $@
=======
$(ONT).owl: $(SRC) templates/caused_by.tsv templates/causes_condition.tsv templates/causes_molecular_phenotype.tsv templates/causes_or_contributes_to_condition.tsv templates/causes_or_contributes_to_molecular_phenotype.tsv templates/contributes_to_genotype.tsv templates/diagnosed_by.tsv templates/diagnosed_using_measurement.tsv templates/diagnosed_using_tool.tsv templates/has_causal_genotype.tsv templates/has_causal_or_contributing_genetic_variation.tsv templates/has_clinical_code.tsv templates/has_contributing_genetic_variation.tsv templates/has_essential_measure.tsv templates/has_manifestation.tsv templates/has_causal_molecular_phenotype.tsv templates/has_output_measurement.tsv templates/induced_by.tsv templates/in_guideline.tsv templates/has_mode_of_inheritance.tsv templates/measures.tsv templates/modified_by.tsv templates/modifies.tsv templates/obtained_via_diagnostic_tool.tsv templates/output_of_diagnostic_device.tsv templates/treated_with.tsv templates/used_by_diagnostic_tool.tsv templates/uses_diagnostic_device.tsv templates/has_causal_molecular_phenotype.tsv templates/treats.tsv
	$(ROBOT) template --input $(SRC) --merge-before --prefix $(PREFIX) --template templates/caused_by.tsv --merge-before --prefix $(PREFIX) --template templates/causes_condition.tsv --merge-before --prefix $(PREFIX) --template templates/causes_molecular_phenotype.tsv --merge-before --prefix $(PREFIX) --template templates/causes_or_contributes_to_condition.tsv --merge-before --prefix $(PREFIX) --template templates/causes_or_contributes_to_molecular_phenotype.tsv --merge-before --prefix $(PREFIX) --template templates/contributes_to_genotype.tsv --merge-before --prefix $(PREFIX) --template templates/diagnosed_by.tsv --merge-before --prefix $(PREFIX) --template templates/diagnosed_using_measurement.tsv --merge-before --prefix $(PREFIX) --template templates/diagnosed_using_tool.tsv --merge-before --prefix $(PREFIX) --template templates/has_causal_genotype.tsv --merge-before --prefix $(PREFIX) --template templates/has_causal_or_contributing_genetic_variation.tsv --merge-before --prefix $(PREFIX) --template templates/has_clinical_code.tsv --merge-before --prefix $(PREFIX) --template templates/has_contributing_genetic_variation.tsv --merge-before --prefix $(PREFIX) --template templates/has_essential_measure.tsv --merge-before --prefix $(PREFIX) --template templates/has_manifestation.tsv --merge-before --prefix $(PREFIX) --template templates/has_causal_molecular_phenotype.tsv --merge-before --prefix $(PREFIX) --template templates/has_output_measurement.tsv --merge-before --prefix $(PREFIX) --template templates/induced_by.tsv --merge-before --prefix $(PREFIX) --template templates/in_guideline.tsv --merge-before --prefix $(PREFIX) --template templates/has_mode_of_inheritance.tsv --merge-before --prefix $(PREFIX) --template templates/measures.tsv --merge-before --prefix $(PREFIX) --template templates/modified_by.tsv --merge-before --prefix $(PREFIX) --template templates/modifies.tsv --merge-before --prefix $(PREFIX) --template templates/obtained_via_diagnostic_tool.tsv --merge-before --prefix $(PREFIX) --template templates/output_of_diagnostic_device.tsv --merge-before --prefix $(PREFIX) --template templates/used_by_diagnostic_tool.tsv --merge-before --prefix $(PREFIX) --template templates/uses_diagnostic_device.tsv --merge-before --prefix $(PREFIX) --template templates/treated_with.tsv --merge-before --prefix $(PREFIX) --template templates/has_causal_molecular_phenotype.tsv --merge-before --prefix $(PREFIX) --template templates/treats.tsv reason -s true -m false -r ELK annotate -V $(BASE)/releases/`date +%Y-%m-%d`/$(ONT).owl -o $@
>>>>>>> new-repo

#$(ONT).owl: $(SRC) /home/gaston/SCDO-Ontologygithub/templates/AllTermsFinal.tsv /home/gaston/SCDO-Ontologygithub/templates/Topology.tsv templates/haemoglobinopathies.tsv
#	$(ROBOT) template --input $(SRC) --merge-before --prefix $(PREFIX) --template /home/gaston/SCDO-Ontologygithub/templates/AllTermsFinal.tsv template --merge-before --prefix $(PREFIX) --template /home/gaston/SCDO-Ontologygithub/templates/Topology.tsv template --merge-before --prefix $(PREFIX) --template templates/haemoglobinopathies.tsv reason -s true -m false -r ELK annotate -V $(BASE)/releases/`date +%Y-%m-%d`/$(ONT).owl -o $@

$(ONT)_hpo_merged.owl: $(SRC) scdo_hp_bridge.owl results/hp_module.owl
	$(ROBOT) merge --input $(SRC) --input scdo_hp_bridge.owl --input results/hp_module.owl reason -s true -m false -r ELK annotate -V $(BASE)/releases/`date +%Y-%m-%d`/$(ONT)_hpo_merged.owl -o $@

$(ONT).obo: $(ONT).owl
	$(ROBOT) convert -i $< -f obo -o $(ONT).obo.tmp && mv $(ONT).obo.tmp $@

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
	$(ROBOT) verify -i $< --queries $(VQUERIES) -O reports/

# ----------------------------------------
# Sparql queries: Reports
# ----------------------------------------

REPORTS = basic-report class-count-by-prefix edges xrefs obsoletes synonyms
REPORT_ARGS = $(foreach V,$(REPORTS),-s $(SPARQLDIR)/$V.sparql reports/$V.tsv)
all_reports: $(SRC)
	$(ROBOT) query -f tsv -i $< $(REPORT_ARGS)
