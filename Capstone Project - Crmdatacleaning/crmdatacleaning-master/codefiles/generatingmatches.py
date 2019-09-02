

import pandas as pd
import re,pprint
from collections import Counter
from fuzzywuzzy import fuzz
import pickle

    
def load_model(filename='randomforest_model.sav'):
    model = pickle.load(open(filename, 'rb'))
    return model

def read_data(filename):
    """Function to read dataset from filename"""
    import pandas as pd
    data_frame = None

    if str(filename).endswith("csv"):
        data_frame = pd.read_csv(filename,usecols=["ContactID","FullName","MobilePhone","Email","Title","MailingStreet",
                                                   "MailingCity","MailingState","MailingZipCode","MailingCountry"])
        # data_frame = pd.read_csv(filename)
    elif str(filename).endswith("xlsx"):
        data_frame = pd.read_excel(filename)
    else:
        print("Please Provide Dataset in CSV or Excel Format")
    return data_frame

def preproces_entity(entity):
    """Function to pre process entity"""
    entities=[]
    try:
        entity = entity.lower().strip()
        entities = re.findall("\w+",entity)
    except Exception as e:
        print("Exception in Pre-Processing Data : ",e)
        pass
    return entities

def encode_percentages(percentage):
    """ Function to Encode Percentages """
    if 0<=percentage<=50:
        return 1
    elif 50<percentage<=75:
        return 2
    elif 75<percentage<=90:
        return 3
    else:
        return 4

def entity_matching(entity1, entity2):
    """ Function to Find Entity Percentages """
    p1=p2=0
    try:
        entities1 = preproces_entity(entity1)
        entities2 = preproces_entity(entity2)

        # Joining All Entities
        all_entities = list(set(entities1))+list(set(entities2))

        # Applying Counter
        counter = Counter(all_entities)

        # Finding Matched Words
        matched_words = [word for word in counter if counter[word]>1]

        # Finding Percentages
        p1 = (len(matched_words)/len(entities1))*100
        p2 = (len(matched_words)/len(entities2))*100
        return p1,p2

    except Exception as e:
        print('Exception in Finding Entity Matching : ',e)
        pass

def string_matching(string1, string2,fuzzy=False):
    """Function to find String Matching Percentages """
    if fuzzy:
        p12 = fuzz.ratio(string1,string2)
        return p12
    else:
        if string1.lower().strip() == string2.lower().strip():
            return 100
        else:
            return 0

def phone_matching(phone1, phone2):
    """Function to Find Phone Matching Percentages"""
    # Removing Punctuations from both entries
    st1 = "".join(re.findall("\d+",phone1))[-10:]
    st2 = "".join(re.findall("\d+",phone2))[-10:]
    percentage = string_matching(st1,st2,fuzzy=False)
    return percentage

cols=['phone_p', 'email_p', 'title_present', 'title_p_12', 'phone_present',
       'name_p_21', 'title_p_21', 'name_p_12', 'email_present','address_p_12','address_p_21']

def clean_match(filename):
    import json
    with open(filename, 'r') as file:
          data=json.loads(file.read())
    #       print(data)

    data={k: v for k, v in data.items() if v}
    # data

    for i in data.keys():
        if data[i]!=None and data[i]:
            list=data[i]
            for j in list:
                if '{}'.format(j) in data.keys():

                   data["{}".format(j)]=data["{}".format(j)].remove(int(i))
    data={k: v for k, v in data.items() if v}

    len(data)
    # data
    with open('txt files/matches_clean.txt', 'w') as file:
          file.write(json.dumps(data))


def process_clean(filename,filename1):
    """Main Function to Run Data Preprocessing"""
    import pandas as pd
    df =read_data(filename)

    df = df.fillna("None")
    model=load_model(filename1)

    print()
    matches={}
    for i in range(df.shape[0]):
        matches["{}".format(i)]=set()
        for j in range(df.shape[0]):
            
            # Condition for avoiding matching with the same field
            if i!=j:
                address1=''.join([str(df["MailingStreet"][i]).replace("\n", " ") ," ",str(df["MailingCity"][i]).replace("\n", " ")," ",str(df["MailingState"][i]).replace("\n", " ")," ",str(df["MailingCountry"][i]).replace("\n", " ")," ",str(df["MailingZipCode"][i]).replace("\n", "").replace("-","").replace(" ","")])
                address2=''.join([str(df["MailingStreet"][j]).replace("\n", " ") ," ",str(df["MailingCity"][j]).replace("\n", " ")," ",str(df["MailingState"][j]).replace("\n", " ")," ",str(df["MailingCountry"][j]).replace("\n", " ")," ",str(df["MailingZipCode"][j]).replace("\n", "").replace("-","").replace(" ","")])
                # Defining Output Dictionary Format
                outdict={}
        
                
                outdict["email_present"] = 0
                outdict["title_present"] = 0
                outdict["phone_present"] = 0
                outdict["name_p_12"] = 0
                outdict["name_p_21"] = 0
                outdict["email_p"] = 0
                outdict["phone_p"] = 0
                outdict["title_p_12"] = 0
                outdict["title_p_21"] = 0
                outdict["address_p_12"]=0
                outdict["address_p_21"]=0
               
                

                # Performing Name Matching
                try:

                    n12, n21 = entity_matching(df["FullName"][i], df["FullName"][j])
                    outdict["name_p_12"] = encode_percentages(n12)
                    outdict["name_p_21"] = encode_percentages(n21)
                except Exception as e:
                    print("Exception in finding Name Matching : ",e)
                    pass
                
                # Performing address Matching
                try:

                    a12, a21 = entity_matching(address1,address2)
                    outdict["address_p_12"] = encode_percentages(a12)
                    outdict["address_p_21"] = encode_percentages(a21)
                except Exception as e:
                    print("Exception in finding Name Matching : ",e)
                    pass

                # Performing Email Matching
                try:
                    if df["Email"][i] != "None" and df["Email"][j]!="None":
                        e11 = string_matching(df["Email"][i], df["Email"][j])
                        outdict["email_present"] = 1
                        outdict["email_p"]=encode_percentages(e11)
                except Exception as e:
                    print("Exception in finding Email Matching : ",e)
                    pass

                # Performing Title Matching
                try:
                    if df["Title"][i]!='None' and df["Title"][j]!='None':
                        t12, t21 = entity_matching(df["Title"][i], df["Title"][j])
                        outdict["title_present"]=1
                        outdict["title_p_12"] = encode_percentages(t12)
                        outdict["title_p_21"] = encode_percentages(t21)
                except Exception as e:
                    print('Exception in Finding Title Matching : ',e)
                    pass

                # Performing Phone Matching
                try:
                    if df["MobilePhone"][i] !='None' and df["MobilePhone"][j]!='None':
                        p12 = phone_matching(str(df["MobilePhone"][i]), str(df["MobilePhone"][j]))
                        outdict["phone_present"]=1
                        outdict["phone_p"]=encode_percentages(p12)
                except Exception as e:
                    print("Exception in Finding Phone Matching Percentages : ",e)
                    pass


                outdict = pd.DataFrame([outdict])
                outdict=outdict[cols]


                # Predicting Matches
                match=model.predict(outdict.iloc[0].values.reshape(1,-1))[0]   
                
                # Adding the location of match in the Matches set for the ith key in dictionary
                if (match):
                    matches["{}".format(i)].add(j)
        if (float((int(i) / len(df)) * 100) % 1.0):
            print(int(((int(i) / len(df)) * 100)), "% completed")
        matches["{}".format(i)]=list(matches["{}".format(i)])
                    
    print("done")

    import json
    with open('txt files/matches.txt', 'w') as file:
        file.write(json.dumps(matches))
    clean_match('txt files/matches.txt')
    


if __name__ == '__main__':
 #   process('contacts.csv','randomforest_model.sav')

    process_clean('../dataset/contacts.csv','../model/randomforest_model.sav')



