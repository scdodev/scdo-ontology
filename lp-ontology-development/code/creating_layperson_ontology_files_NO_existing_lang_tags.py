#creating_layperson_ontology_files_NO_existing_lang_tags.py

#Program that adds primary language tags to all term labels and descriptions in an owl file, as well as layperson labels and descriptions to terms where necessary.
#Note: This is only to be used on an ontology owl or owx file that does not contain other translations (e.g. French labels and definitions)

#Output:
#       2 rdf files:
#          1 rdf file with all ontology terms, including those that don't have layperson annotations added.
#          1 rdf file with only terms with layperson annotations

#Errors:
#       If this error occurs: "builtins.ModuleNotFoundError: No module named 'owlready2'" --> run "pip install Owlready2" in cmd
#       If you still get an error, run this command in anaconda prompt: "conda install -c conda-forge owlready2"
#       If you still get an error, run this command in anaconda prmpt: "pip install pysqlite3"
#       If you still get an error, go to "https://www.sqlite.org/download.html" and download the appropriate dll zip file and add to "C:\Users\YOURUSER\Anaconda3\DLLs"

#11 May 2020
#Jade Hotchkiss

from owlready2 import *

term_label_description_dict = {} # creates empty dictionary to which term ID will be added as keys and the term's layperson label and description as values in a list

term_synonyms_dict = {} # creates empty dictionary to which term ID will be added as keys and the list of remaining initial synonyms will be added as a value
term_new_synonyms_dict = {} # creates empty dictionary to which term ID will be added as keys and the list of new synonyms will be added as a value

##### Reads the file with layperson annotations and stores content in lists and dictionaries #####
def reads_layperson_annotations(layperson_annotations_file, layperson_annotations_file_cell1):
     ### Reads the file with the layperson annotations
     f = open(layperson_annotations_file, 'r') # opens the file containing layperson annotations
     
     for row in f:  # loops through the rows in the file
          row = (row.strip('\n')).split('\t') # strips the row of line endings and splits the row on tabs
          
          if row[0] != layperson_annotations_file_cell1: # if the row is not the header row...
               layperson_label_description_list = [] #creates a list for layperson label and description of the term
               term_ID = row[0] # assigns the content of the first cell in the row to a "term_ID" variable
               term_layperson_label = row[2].strip() # assigns the content of the third cell in the row to a "term_layperson_label" variable
               term_layperson_description = row[4].strip() # assigns the content of the fifth cell in the row to a "term_layperson_description" variable
               
               if term_layperson_label != "": # if the layperson label cell is not empty...
                    if term_layperson_label != "-": # if the layperson label cell doesn't contain "-"
                         layperson_label_description_list.append(term_layperson_label) # adds the layperson label to the "layperson_label_description_list" list
                         layperson_label_description_list.append(term_layperson_description) # adds the layperson description to the "layperson_label_description_list" list
                         
                         term_label_description_dict[term_ID] = layperson_label_description_list # adds the term id to the "term_label_description_dict" dictionary as a key with it's layperson labela dn description in a list as the values
                         
                         synonyms_list = row[5].strip("").split('|') # splits the 6th cell in the row on "|" and strips each component of spaces to make a list of synonyms
                         stripped_synonyms_list = [] # creates an empty list to to which synonyms stripped of spaces will be added
                         
                         for synonym in synonyms_list: # loops through the synonyms for the term
                              stripped_synonyms_list.append(synonym.strip()) # strips the synonym of spaces on either side

                         if stripped_synonyms_list != ['']: # if the list of stripped synonyms is not empty...
                              term_synonyms_dict[term_ID] = stripped_synonyms_list # adds the term ID to the "term_synonyms_dict" dictionary as a key and the list of stripped synonyms as a value
                         
                         new_synonyms_list =  row[6].split('|') # splits the 7th cell in the row on "|" and strips each component of spaces to make a list of new synonyms
                         stripped_new_synonyms_list = [] # creates an empty list to to which new synonyms stripped of spaces will be added
                         
                         for synonym in new_synonyms_list: # loops through the new synonyms for the term
                              stripped_new_synonyms_list.append(synonym.strip()) # strips the synonym of spaces on either side
                              
                         if stripped_new_synonyms_list != ['']: # if the list of stripped new synonyms is not empty...
                              term_new_synonyms_dict[term_ID] = stripped_new_synonyms_list # adds the term ID to the "term_new_synonyms_dict" dictionary as a key and the list of stripped new synonyms as a value

     f.close() # closes the file containing layperson annotations

##### Adds language tags to labels and descriptions of all terms in the ontology, then adds layperson annotations where necessary and generates 2 files (1 with all ontology terms and 1 with only terms with layperson annotations)
def adds_language_tags_and_includes_layperson_annotations(owl_file_path, lang_tag, iri_path, layperson_tag, outputfile1_name, outputfile2_name):
     onto = get_ontology(owl_file_path).load() # loads the ontology as an "onto" object
     
     ### Adds language tags to all term labels and descriptions
     for term in list(onto.classes()): # loops through the list of classes in the ontology
          if term.deprecated == []: # ensures that only terms that are not deprecated have the language tags added
               label = term.label[0] # obtains the label of the term/class
               term.label.remove(str(term.label[0])) # removes label without language tag
               term.label.append(locstr(label, lang = lang_tag)) # re-adds it with the language tag included    
               if term.IAO_0000115 != []:
                    description = term.IAO_0000115[0] # obtains the description of the term/class
                    term.IAO_0000115.remove(str(term.IAO_0000115[0])) # removes description without language tag
                    term.IAO_0000115 = [locstr(description, lang = lang_tag)] # re-adds it with the language tag included
     
     print()
     print(term_label_description_dict)
              
     ### Adds layperson annotations to terms and creates 2 output files
     for term_ID in term_label_description_dict: #loops through the terms IDs in the "term_label_description_dict" dictionary (contains terms with layperson labels and descriptions)
          print(term_ID)
          term_object = onto.search_one(iri = iri_path + term_ID) # searches for the term object in the OWL file by using the term's IRI (constructed using the generic iri_path provided and the term's ID) and assigns it to a "term_object" variable
          print(iri_path + term_ID)
          ### Adds layperson label to term
          print(term_object)
          term_labels = getattr(term_object, "label") # obtains the list of labels ascribed to the term
          term_labels.append(locstr(term_label_description_dict[term_ID][0], lang = layperson_tag)) # adds the layperson label to the list along with a "layperson" tag for the new label

          ### Adds layperson description to term 
          term_descriptions = getattr(term_object, "IAO_0000115") # obtains the list of descriptions ascribed to the term
          term_descriptions.append(locstr(term_label_description_dict[term_ID][1], lang = layperson_tag)) # adds the layperson description to the list along with a "layperson" tag for the new description          
          
          ### Gets list of exact synonyms...
          term_exact_synonyms = getattr(term_object, "hasExactSynonym") # obtains the list of exact synonyms ascribed to the term
               
          ### If layperson label in list of exact synonyms for the term, removes it from the list
          if term_label_description_dict[term_ID][0] in term_exact_synonyms: # if the layperson label is in the list of exact synonyms ascribed to the term...
               term_exact_synonyms.remove(term_label_description_dict[term_ID][0]) # removes it from the term's list of exact synonyms
               
          ### Goes through list of new exact synonyms and adds to list of exact synonyms for the term, excepting the layperson label
          if term_ID in term_new_synonyms_dict: # if the term is in the dictionary for terms with layperson labels and descriptions...

               if term_label_description_dict[term_ID][0] in term_new_synonyms_dict[term_ID]: # if the layperson label is in the list of new synonyms recorded for the term by curators...
                    term_new_synonyms_dict[term_ID].remove(term_label_description_dict[term_ID][0]) # removes it from the list of new synonyms recorded for the term by curators...

               if len(term_new_synonyms_dict[term_ID]) > 0: # if the length of the list of new synonyms for the term is 1 or more...
                    for item in term_new_synonyms_dict[term_ID]: # loops through each new synonym in the list...
                         term_exact_synonyms.append(item) # adds it to the list of synonyms for the term in the ontology
     
     ### Saves a new ontology file (rdfxml format containing the edits made) containing all ontology terms
     onto.save(file = outputfile1_name, format = "rdfxml")     
               
     ### Removes from the ontology terms without layperson annotations
     layperson_IDs = [] # creates empty list to which term IDs of terms with layperson annotations will be added
     
     for term in term_label_description_dict: # loops through terms in list of terms with layperson annotations
          layperson_IDs.append(term) # adds the term's ID to the "layperson_IDs" list
          
     for term in list(onto.classes()): # loops through list of classes in the ontology
          if term.name not in layperson_IDs: # if term not in list of terms with layperson annotations...
               destroy_entity(term) # removes term from the ontology
               
     ### Saves a new ontology file (rdfxml format containing the edits made) containing only terms with layperson annotations 
     onto.save(file = outputfile2_name, format = "rdfxml")
     
def main():
     ##### User Input #####
     
     ## Input Files ##
     layperson_annotations_file = "merged_layperson_updates_11Dec2022_IDs_changed_for_compiled_owl.txt" # path of .txt file containing layperson annotations
     owl_file_path = "C:/Users/01440397/Dropbox/Work_2016/layperson_terms/creating_layperson_ontology_files/scdo_github_download_9Dec2022.owl" # path of the owl file to which layperson annotations must be added (preferable to use rdf/xml file, not owl/xml file)
     
     ## Other variables ##
     layperson_annotations_file_cell1 = "ID" # content of the first cell in the input file containing layperson annotations
     lang_tag = "en" # specifies the primary language tag to be added to labels and descriptions
     iri_path = "http://purl.obolibrary.org/obo/" # the specific generic IRI path that is used for terms in the ontology being translated
     layperson_tag = "en-x-lp" #specifies the tag to be added to all layperson annotations
     outputfile1_name = "entire_ontology_with_layperson_annotations_11Dec2022.rdf" # name of rdf file created with all ontology terms
     outputfile2_name = "layperson_only_ontology_11Dec2022.rdf" # name of rdf file created with only terms with layperson annotations
          
     #####Functions#####    
     reads_layperson_annotations(layperson_annotations_file, layperson_annotations_file_cell1)
     
     adds_language_tags_and_includes_layperson_annotations(owl_file_path, lang_tag, iri_path, layperson_tag, outputfile1_name, outputfile2_name)
     

if __name__ == '__main__':               
          main()