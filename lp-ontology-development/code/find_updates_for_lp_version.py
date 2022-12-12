#find_updates_for_lp_version.py

#Program that compares content of an updated ontology file (owl or owx format) with the layperson labels and descriptions from the previous layperson version of the ontology, and outputs files to be used for updating the layperson annotations.

#Errors:
#       If this error occurs: "builtins.ModuleNotFoundError: No module named 'owlready2'" --> run "pip install Owlready2" in cmd
#       If you still get an error, run this command in the anaconda prompt: "conda install -c conda-forge owlready2"
#       If you still get an error, run this command in anaconda prmpt: "pip install pysqlite3"
#       If you still get an error, go to "https://www.sqlite.org/download.html" and download the appropriate dll zip file and add to "C:\Users\YOURUSER\Anaconda3\DLLs"

#10 March 2022
#Jade Hotchkiss

from owlready2 import *
from datetime import datetime

term_lp_label_description_dict = {} # creates empty dictionary to which term ID will be added as keys and the term's layperson label and description as values in a list

term_label_description_dict = {} # creates empty dictionary to which term ID will be added as keys and the term's primary language label and description as values in a listsynonyms

term_synonyms_dict = {} # creates empty dictionary to which term ID will be added as keys and the list of remaining initial synonyms will be added as a value

terms_new_synonyms_string_dict = {} # creates empty dictionary to which term ID will be added as keys and the string of new synonyms will be added as a value

term_new_synonyms_dict = {} # creates empty dictionary to which term ID will be added as keys and the list of new synonyms will be added as a value

##### Reads the file with layperson annotations and stores content in lists and dictionaries #####
def reads_layperson_annotations(layperson_annotations_file, layperson_annotations_file_cell1):
     ### Reads the file with the layperson annotations
     f = open(layperson_annotations_file, 'r', encoding="ISO-8859-1") # opens the file containing layperson annotations
     
     for row in f:  # loops through the rows in the file
          row = (row.strip('\n')).split('\t') # strips the row of line endings and splits the row on tabs
          
          if row[0] != layperson_annotations_file_cell1: # if the row is not the header row...
               label_description_list = [] #creates a list for label and description of the term
               layperson_label_description_list = [] #creates a list for layperson label and description of the term
               term_ID = row[0] # assigns the content of the first cell in the row to a "term_ID" variable
               term_label = row[1].strip() # assigns the content of the 2nd cell in the row to a "term_label" variable
               term_description = row[3].strip() # assigns the content of the fifth cell in the row to a "term_layperson_description" variable
               term_layperson_label = row[2].strip() # assigns the content of the third cell in the row to a "term_layperson_label" variable
               term_layperson_description = row[4].strip() # assigns the content of the fifth cell in the row to a "term_layperson_description" variable
               
               ##adds the term's label and definition to the "label_description_list" list
               label_description_list.append(term_label)
               label_description_list.append(term_description)
	       
	       ##adds the list with the term's label and definition as a value to the "term_label_description_dict" where the term's ID is the key
               term_label_description_dict[term_ID] =  label_description_list
               
               if term_layperson_label != "": # if the layperson label cell is not empty...
                    if term_layperson_label != "-": # if the layperson label cell doesn't contain "-"
                         layperson_label_description_list.append(term_layperson_label) # adds the layperson label to the "layperson_label_description_list" list
                         layperson_label_description_list.append(term_layperson_description) # adds the layperson description to the "layperson_label_description_list" list
                         
                         term_lp_label_description_dict[term_ID] = layperson_label_description_list # adds the term id to the "term_lp_label_description_dict" dictionary as a key with it's layperson labela dn description in a list as the values
                         
                         synonyms_list = row[5].strip("").split('|') # splits the 6th cell in the row on "|" and strips each component of spaces to make a list of synonyms
                         stripped_synonyms_list = [] # creates an empty list to to which synonyms stripped of spaces will be added
                         
                         for synonym in synonyms_list: # loops through the synonyms for the term
                              stripped_synonyms_list.append(synonym.strip()) # strips the synonym of spaces on either side

                         if stripped_synonyms_list != ['']: # if the list of stripped synonyms is not empty...
                              term_synonyms_dict[term_ID] = stripped_synonyms_list # adds the term ID to the "term_synonyms_dict" dictionary as a key and the list of stripped synonyms as a value
                         
                         new_synonyms_string = row[6].strip()
                         terms_new_synonyms_string_dict[term_ID] = new_synonyms_string
                         
                         new_synonyms_list =  row[6].split('|') # splits the 7th cell in the row on "|" and strips each component of spaces to make a list of new synonyms
                         stripped_new_synonyms_list = [] # creates an empty list to to which new synonyms stripped of spaces will be added
                         
                         for synonym in new_synonyms_list: # loops through the new synonyms for the term
                              stripped_new_synonyms_list.append(synonym.strip()) # strips the synonym of spaces on either side
                              
                         if stripped_new_synonyms_list != ['']: # if the list of stripped new synonyms is not empty...
                              term_new_synonyms_dict[term_ID] = stripped_new_synonyms_list # adds the term ID to the "term_new_synonyms_dict" dictionary as a key and the list of stripped new synonyms as a value

     f.close() # closes the file containing layperson annotations

def includes_layperson_annotations(owl_file_path):
     onto = get_ontology(owl_file_path).load() # loads the ontology as an "onto" object
     
     ##adds all non-depracated terms to a "non_deprecated_terms" list:
     all_terms = onto.classes()
     non_deprecated_terms = []
     for term in all_terms:
          if term.deprecated == []:
               if term.iri != "http://www.w3.org/2002/07/owl#Thing":
                    if term not in non_deprecated_terms:
                         non_deprecated_terms.append(term)     
     
     lp_label_needs_updating = [] # list for labels of terms that need their layperson label updated
     lp_def_needs_updating = [] # list for labels of terms that need their layperson definition updated
     lp_def_to_be_removed = [] # list for ids of terms that no longer have a definition
     same_lp_label = [] # list for ids of terms that should have the same layperson label as before
     same_lp_def = [] # list for ids of terms that should have the same layperson definition as before
     
     ## The generic header row for files containing layperson annotations in the template format
     header = "ID" + '\t' + "current label" + '\t' + "lp label" + '\t' + "current definition" + '\t' + "lp definition"  + '\t' + "hasExactSynonym" + '\t' + 	"newExactSynonym" + '\n'
     
     ## The header row for the file that will contain updates needing reviewing
     header2 = "ID" + '\t' + "previous label" + '\t' + "current label" + '\t' + "previous lp label" + '\t' + "lp label" + '\t' + "previous definition" + '\t' +"current definition" + '\t' + "previous lp definition" + '\t' + "lp definition"  + '\t' + "hasExactSynonym" + '\t' + 	"newExactSynonym" + '\n'
     
     current_date = datetime.now().date() # obtains current date
     
     ### Creates output file to which terms without layperson terms previously get written to
     newf1 = open('no_lp_annotations_' + str(current_date) + '.txt','w', encoding="utf8")
     newf1.write(header)     
     
     ### Creates output file to which new ontology terms will be written
     newf2 = open('new_terms_' + str(current_date) + '.txt','w', encoding="utf8")
     newf2.write(header)   
     
     ### Creates output file to which terms needing updates to layperson annotations will be written
     newf3 = open('lp_terms_needing_updating_' + str(current_date) + '.txt','w', encoding="utf8")
     newf3.write(header2)
     
     ### Creates output file to which terms with updates have same  annotations (not updated) written. These same terms will be in output file 3 with annotations needing updates reviewed
     newf4 = open('update_terms_same_lp_anns_' + str(current_date) + '.txt','w', encoding="utf8")
     newf4.write(header)      
     
     ### Creates output file to which terms not needing updates will be written
     newf5 = open('same_annotations_' + str(current_date) + '.txt','w', encoding="utf8")
     newf5.write(header)
     
     number_lp_labels_added = 0
     number_lp_defs_added = 0
     
     for term in non_deprecated_terms:
          term_id = term.name
          term_label = term.label.en[0]
          term_object = onto.search(label = term_label) # finds the term object in the OWL file by searching with the term's ID
          if len(term_object) >1:
               for term_object_id in term_object:
                    if "webprotege.stanford.edu" in str(term_object_id):
                         term_object.remove(term_object_id) # removes any residual old ids linked to this term	  
	  
          if term_id in term_lp_label_description_dict:
               if term_label_description_dict[term_id][0] == term.label.en[0]: # if the old English label is the same as in the updated owl file...
		    
                    same_lp_label.append(term_label)		    
		    
               else: # if label updated, adds term ID to list of terms needing label updates
                    lp_label_needs_updating.append(term_label)
		    
               if term.IAO_0000115.en != []: # if there are any English definitions
                    term_def = term_label_description_dict[term_id][1].strip()
                    if term_def[0] == '"':
                         term_def = term_def[1:-1]
                    if term_def == term.IAO_0000115.en[0]: # if the old English definition is the same as in the updated owl file...
			 
                         same_lp_def.append(term_label)
		 		  
                    else: # if label updated... 
                         lp_def_needs_updating.append(term_label) # adds term ID to list of terms needing definition updates
			 
               else: #if there are no longer En definitions in the updated ontology
                    lp_def_to_be_removed.append(term_id)       			 
		    
          else:
               synonyms = term.hasExactSynonym # obtains the terms synonyms stored in the owl file
               synonyms_merged = " | ".join(synonyms)  # merges the different synonyms into one string	   
	       
               definition = term.IAO_0000115.en

               if definition  == []: # i.e. no English tagged definition
                    definition = term.IAO_0000115
                    if definition == []:
                         definition = ""
                    if definition == ['']:
                         definition = definition[0]		 
                    if len(definition) > 1:
                         definition = term.IAO_0000115[0]
	
               elif definition == ['']: # Engish definition is blank
                    definition = definition[0]
               else:
                    definition = term.IAO_0000115.en[0]	# definition is the one tagged with an English language tag  
	
               if term_id in term_label_description_dict:  # if it's in the old and updated ontology but didn't have a layperson label previously...
		    
                    newf1.write(term_id + '\t' + term_label + '\t' + ""+ '\t' + definition + '\t' + "" + '\t' +  synonyms_merged + '\t' +""+'\n') # writes the new term's info to the output file
	       
	       ## Writes new terms to output file 2
               else:
                    newf2.write(term_id + '\t' + term_label + '\t' + ""+ '\t' + definition + '\t' + "" + '\t' +  synonyms_merged + '\t' +""+'\n') # writes the new term's info to the output file
		    
     for term_label in lp_label_needs_updating:
          term_object = onto.search(label = term_label)
          if len(term_object) >1:
               for term_object_id in term_object:
                    if "webprotege.stanford.edu" in str(term_object_id):
                         term_object.remove(term_object_id) # removes any residual old ids linked to this term 
	  
          term_exact_synonyms = getattr(term_object[0], "hasExactSynonym") # obtains the list of exact synonyms ascribed to the term
          if len(term_exact_synonyms) > 1:
               exact_synonyms_string = " | ".join(term_exact_synonyms)
          elif len(term_exact_synonyms) == 1:
               exact_synonyms_string = term_exact_synonyms[0]
          else:
               exact_synonyms_string = ""
	  
          term_id = term_object[0].name
	  
          newf3.write(term_id + '\t' + term_label_description_dict[term_id][0] + '\t' +term_object[0].label.en[0] +  '\t' + term_lp_label_description_dict[term_id][0] + '\t' + "" + '\t')
	  
	  ### writes the term's ID and current label to output file 4, leaving a blank cell for the layperson label
          newf4.write(term_id + '\t' + term_object[0].label.en[0] +  '\t' + "" + '\t')
	  
          if term_label in lp_def_needs_updating:
	       
	       ### writes the term's current definition to output file 4, leaving a blank cell for the layperson definition
               newf4.write(term_object[0].IAO_0000115.en[0] +  '\t' + "" + '\t')
	       
               if term_object[0].IAO_0000115 != []:
                    newf3.write(term_label_description_dict[term_id][1] + '\t' + term_object[0].IAO_0000115.en[0] +  '\t' + term_lp_label_description_dict[term_id][1] +'\t' + "" + '\t')
               else:
                    newf3.write(term_label_description_dict[term_id][1] +  '\t' + "" +  '\t' + "" + '\t'  + "" + '\t')
          else:
               newf3.write("NA" +  '\t' +"NA" +  '\t' + "NA" + '\t' + "NA" + '\t')
	       
               newf4.write(term_object[0].IAO_0000115.en[0] +  '\t' + term_lp_label_description_dict[term_id][1] + '\t')
	  
          newf3.write(exact_synonyms_string + '\t' + "" + '\n')
          newf4.write(exact_synonyms_string + '\t' + "" + '\n')
	       
     for term_label in lp_def_needs_updating:
          if term_label not in lp_label_needs_updating:
               term_object = onto.search(label = term_label)
               if len(term_object) >1:
                    for term_object_id in term_object:
                         if "webprotege.stanford.edu" in str(term_object_id):
                              term_object.remove(term_object_id) # removes any residual old ids linked to this term
			      
               term_exact_synonyms = getattr(term_object[0], "hasExactSynonym") # obtains the list of exact synonyms ascribed to the term
               if len(term_exact_synonyms) > 1:
                    exact_synonyms_string = " | ".join(term_exact_synonyms)
               elif len(term_exact_synonyms) == 1:
                    exact_synonyms_string = term_exact_synonyms[0]
               else:
                    exact_synonyms_string = ""
		    
               term_id = term_object[0].name
	       
               newf3.write(term_object[0].name + '\t' + "NA" +  '\t' + "NA" + '\t' + "NA" + '\t' + "NA" + '\t'+ term_label_description_dict[term_id][1] + '\t' + term_object[0].IAO_0000115.en[0] +  '\t' + term_lp_label_description_dict[term_id][1] + '\t' + "" + '\t' + exact_synonyms_string + '\t' + "" + '\n')
	       
	       ### writes all the term's info besides layperson definition to output file 4
               newf4.write(term_object[0].name + '\t' + term_object[0].label.en[0] + '\t' + term_lp_label_description_dict[term_id][0] + '\t' + term_object[0].IAO_0000115.en[0] + '\t' + "" + '\t' + exact_synonyms_string + '\t' + "" + '\n')
     
     ## Writes terms with no updates to layperson annotations to output file 5
     for term_label in same_lp_label:
          if term_label in same_lp_def:
               term_object = onto.search(label = term_label)
	       
               if len(term_object) >1:
                    for term_object_id in term_object:
                         if "webprotege.stanford.edu" in str(term_object_id):
                              term_object.remove(term_object_id) # removes any residual old ids linked to this term	       
	       
               term_ID = term_object[0].name
	       
               term_exact_synonyms = getattr(term_object[0], "hasExactSynonym") # obtains the list of exact synonyms ascribed to the term
               if len(term_exact_synonyms) > 1:
                    exact_synonyms_string = " | ".join(term_exact_synonyms)
               elif len(term_exact_synonyms) == 1:
                    exact_synonyms_string = term_exact_synonyms[0]
               else:
                    exact_synonyms_string = ""  	       
	       
               new_synonyms = terms_new_synonyms_string_dict[term_ID]
	       
	       ### writes all the term's info to output file 5
               newf5.write(term_ID + '\t' + term_object[0].label.en[0] + '\t' + term_lp_label_description_dict[term_ID][0] + '\t' + term_object[0].IAO_0000115.en[0] + '\t' +  term_lp_label_description_dict[term_ID][1] + '\t' + exact_synonyms_string + '\t' + new_synonyms + '\n')
     
     newf1.close()
     newf2.close()
     newf3.close()
     newf4.close()
     newf5.close()
     
print("Output files generated successfully!")    

def main():
     ##### User Input #####
     
     ## Input Files ##
     layperson_annotations_file = "C:/Users/01440397/Dropbox/Work_2016/layperson_terms/SCDO_layperson_annotations_downloaded/SCDO - Layperson_4June2020_IDs_updated_10March2022.txt" # path of .txt file containing layperson annotations
     owl_file_path = "C:/Users/01440397/Dropbox/Work_2016/SCDO/SCDO downloads/French_versions/french_scdo_8feb2022-ontologies/french_scdo_8feb2022-ontologies-owx-REVISION-HEAD/scdo.owx" # path of the owl file to which layperson annotations must be added (preferable to use rdf/xml file, not owl/xml file)
     
     ## Other variables ##
     layperson_annotations_file_cell1 = "ID" # content of the first cell in the input file containing layperson annotations
     
          
     #####Functions#####    
     reads_layperson_annotations(layperson_annotations_file, layperson_annotations_file_cell1)
     
     includes_layperson_annotations(owl_file_path)
     

if __name__ == '__main__':               
          main()