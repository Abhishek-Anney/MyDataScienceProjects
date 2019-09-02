
import pandas as pd
import re,pprint
from collections import Counter
from fuzzywuzzy import fuzz

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

def read_data(filename):
    """Function to read dataset from filename"""
    data_frame = None
    import pandas as pd

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

    try:
        entities1 = preproces_entity(entity1)
        entities2 = preproces_entity(entity2)

        # Joining All Entities
        all_entities = entities1 + entities2

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

def preprocess(filename):
    """Main Function to Run Data Preprocessing"""
    df = read_data(filename)
    df = df.fillna("None")
#     print(df.head())
#     print()
    outarray = []
    for i in range(len(df)):
        for j in range(len(df)):
                address1=''.join([str(df["MailingStreet"][i]).replace("\n", " ") ," ",str(df["MailingCity"][i]).replace("\n", " ")," ",str(df["MailingState"][i]).replace("\n", " ")," ",str(df["MailingCountry"][i]).replace("\n", " ")," ",str(df["MailingZipCode"][i]).replace("\n", "").replace("-","").replace(" ","")])
                address2=''.join([str(df["MailingStreet"][j]).replace("\n", " ") ," ",str(df["MailingCity"][j]).replace("\n", " ")," ",str(df["MailingState"][j]).replace("\n", " ")," ",str(df["MailingCountry"][j]).replace("\n", " ")," ",str(df["MailingZipCode"][j]).replace("\n", "").replace("-","").replace(" ","")]) 
          # Condition for avoiding matching with the same field
            # if df["ContactID"][i]!=df["ContactID"][j]:
                
                # Defining Output Dictionary Format
                outdict={}
                outdict["fullname_1"] = df["FullName"][i]
                outdict["fullname_2"] = df["FullName"][j]
                outdict["email_1"] = df["Email"][i]
                outdict["email_2"] = df["Email"][j]
                outdict["phone_1"] = df["MobilePhone"][i]
                outdict["phone_2"] = df["MobilePhone"][j]
                outdict["title_1"] = df["Title"][i]
                outdict["title_2"] = df["Title"][j]
                outdict["address_1"]=address1
                outdict["address_2"]=address2
                
                outdict["address_p_12"]=0
                outdict["address_p_21"]=0
                outdict["email_present"] = 0
                outdict["title_present"] = 0
                outdict["phone_present"] = 0
                outdict["name_p_12"] = 0
                outdict["name_p_21"] = 0
                outdict["email_p"] = 0
                outdict["phone_p"] = 0
                outdict["title_p_12"] = 0
                outdict["title_p_21"] = 0
                outdict["Target"] = 0
                
                # Performing Name Matching
                try:
                    n12, n21 = entity_matching(df["FullName"][i], df["FullName"][j])
                    outdict["name_p_12"] = encode_percentages(n12)
                    outdict["name_p_21"] = encode_percentages(n21)
                except Exception as e:
                    print("Exception in finding Name Matching : ",e)
                    pass
                  
                try:
                    n12, n21 = entity_matching(address1, address2)
                    outdict["address_p_12"] = encode_percentages(n12)
                    outdict["address_p_21"] = encode_percentages(n21)
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

                # print(preproces_entity(df["FullName"][i]),preproces_entity(df["FullName"][j]))
                # pprint.pprint(outdict)
                #   print(outdict)
    
                outarray.append(outdict)
        if(((int(i)/len(df))*100) % 10==0.0):
            print((int(i)/len(df))*100,"% completed")
            
    
    print("done")
    final_df = pd.DataFrame(outarray)
#     print(final_df)
    final_df=final_df[["fullname_1","fullname_2","name_p_12","name_p_21","phone_1","phone_2","phone_present","phone_p","email_1","email_2","email_present","email_p","title_1","title_2","title_present","title_p_12","title_p_21","address_1","address_2","address_p_12","address_p_21","Target"]]
    final_df.to_csv("dataset/data_to_annotate.csv")
# if __name__ == '__main__':
#     preprocess('dataset/contacts.csv')

