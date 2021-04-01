PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix oio: <http://www.geneontology.org/formats/oboInOwl#>
prefix def: <http://purl.obolibrary.org/obo/IAO_0000115>
prefix owl: <http://www.w3.org/2002/07/owl#>

INSERT {
  ?subject <http://scdontology.h3abionet.org/ontology/SCDO_1000910> ?subject_id .
}
WHERE 
{
  ?subject oio:hasDbXref ?object  .
  ?subject <http://scdontology.h3abionet.org/ontology/SCDO_1000288> ?sufficient .
  FILTER (str(?sufficient) = "Sufficient")
  FILTER(isIRI(?subject) && regex(str(?subject), "http[:][/][/]scdontology[.]h3abionet[.]org[/]ontology[/]SCDO[_]"))
  BIND(REPLACE(STR(?subject), "http[:][/][/]scdontology[.]h3abionet[.]org[/]ontology[/]SCDO[_]", "SCDO:", "i") AS ?subject_id)
}