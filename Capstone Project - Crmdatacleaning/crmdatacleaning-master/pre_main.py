from codefiles.data_preprocessing import preprocess
from codefiles.trainingdatapreparation import trainingdataprep

preprocess("dataset/contacts.csv")
trainingdataprep("dataset/data_to_annotate.csv")