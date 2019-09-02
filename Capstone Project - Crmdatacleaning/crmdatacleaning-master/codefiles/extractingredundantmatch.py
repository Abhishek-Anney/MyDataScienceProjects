def read_data(filename):
    """Function to read dataset from filename"""
    data_frame = None
    import pandas as pd
    if str(filename).endswith("csv"):
        data_frame = pd.read_csv(filename,usecols=["ContactID","FullName","MobilePhone","Email","Title","MailingStreet",
                                                   "MailingCity","MailingState","MailingZipCode","MailingCountry"])
#         data_frame = pd.read_csv(filename)
    elif str(filename).endswith("xlsx"):
        data_frame = pd.read_excel(filename)
    elif str(filename).endswith("txt"):
        import json
        with open(filename,'r') as file:
          data_frame=json.loads(file.read())
    else:
        print("Please Provide Dataset in CSV or Excel Format")
    return data_frame

def extract_redundancy(filename1,filename2):
    import json
    import pandas as pd
    print("extracting matches.......")

    # with open(filename2,'r') as file:
    #     data=json.loads(file.read())
    data=read_data(filename2)

    contacts=read_data(filename1)
    redundant=pd.DataFrame(columns=list(contacts.columns))

    for i in data.keys():
        redundant=redundant.append(contacts.iloc[int(i)])
        for k in data['{}'.format(i)]:
            redundant=redundant.append(contacts.iloc[k])

    redundant.to_csv("dataset/redundant.csv")
    print("done")
# if __name__=='__main__':
#   extract_redundancy('../dataset/contacts.csv','../txt files/matches_clean.txt')



