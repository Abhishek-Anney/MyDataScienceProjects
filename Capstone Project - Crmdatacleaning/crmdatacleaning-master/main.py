from codefiles.generatingmatches import process_clean
from codefiles.classifyingmatches import postprocess
from codefiles.extractingredundantmatch import extract_redundancy

process_clean("dataset/contacts.csv","model/randomforest_model.sav")
postprocess("dataset/contacts.csv","txt files/matches_clean.txt")
extract_redundancy('dataset/contacts.csv','txt files/matches_clean.txt')