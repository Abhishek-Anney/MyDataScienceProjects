
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
        try:
            with open(filename,'r') as file:
              data_frame=json.loads(file.read())
        except Exception as e:
            print(e)
            pass
    else:
        print("Please Provide Dataset in CSV or Excel Format")
    return data_frame

def preproces_entity(entity):
    """Function to pre process entity"""
    import re
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

def encode_percentages2(percentage):
    """ Function to Encode Percentages for partial exact potential match"""
    if 0<=percentage<=30:
        return 0
    elif 30<percentage<=70:
        return 1
    elif 75<percentage<=90:
        return 2
    else:
        return 3

def entity_matching(entity1, entity2):
    """ Function to Find Entity Percentages """
    p1=p2=0
    from collections import Counter
    try:
        entities1 = list(set(preproces_entity(entity1)))
        entities2 = list(set(preproces_entity(entity2)))
#         print(entities1)
#         print(entities2)
        

        # Joining All Entities
        all_entities = list(set(entities1))+list(set(entities2))

        # Applying Counter
        counter = Counter(all_entities)
#         print(counter)

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
    from fuzzywuzzy import fuzz
    if fuzzy:
        p12 = fuzz.ratio(string1,string2)
        return p12
    else:
        if string1.lower().strip() == string2.lower().strip():
            return 100
        else:
            return 0

def phone_matching(phone1, phone2):
    import re
    """Function to Find Phone Matching Percentages"""
    # Removing Punctuations from both entries
    st1 = "".join(re.findall("\d+",phone1))[-10:]
    st2 = "".join(re.findall("\d+",phone2))[-10:]
    percentage = string_matching(st1,st2,fuzzy=False)
    return percentage

cols=['ContactID', 'IsDeleted', 'MasterRecordID', 'AccountID', 'LastName',
       'FirstName', 'Salutation', 'FullName', 'OtherStreet', 'OtherCity',
       'OtherState', 'OtherZipCode', 'OtherCountry', 'MailingStreet',
       'MailingCity', 'MailingState', 'MailingZipCode', 'MailingCountry',
       'BusinessPhone', 'BusinessFax', 'MobilePhone', 'HomePhone',
       'OtherPhone', 'AssistantPhone', 'ReportsToID', 'Email', 'Title',
       'Department', 'AssistantName', 'LeadSource', 'Birthdate',
       'ContactDescription', 'OwnerID', 'OwnerName', 'CreatedDate',
       'CreatedByID', 'LastModifiedDate', 'LastModifiedByID', 'SystemModstamp',
       'LastActivityDate', 'LastStayInTouchRequestDate',
       'LastStayInTouchSaveDate', 'EmailBouncedReason', 'EmailBouncedDate',
       'NewsSearchOverride', 'AccountRecordTypeName', 'AccountStatus',
       'AccountWebsite', 'ContactRole', 'DateOfValidation', 'DaysNotValidated',
       'ValidatedInd', 'LegacyContactId', 'GeographyCovered', 'YesNoValidated',
       'ISContactId', 'ISSourced', 'ISContactURL', 'EcoSystemAdminInd',
       'EcoSystemRecordInd', 'EcoSystemUserEmail', 'Region', 'EmailBouncedInd',
       'PhotoURL', 'OtherStateCode', 'OtherCountryCode', 'MailingStateCode',
       'MailingCountryCode', 'Last_Updated_User_ID', 'Last_Updated_Date',
       'Created_User_ID', 'Created_Date', 'LastReferencedDate',
       'LastViewedDate', 'MailingGeocodeAccuracy', 'MailingLatitude',
       'MailingLongitude', 'ManagerName', 'OtherGeocodeAccuracy',
       'OtherLatitude', 'OtherLongitude', 'EmailHasOptedOut',
       'EmailAlternative', 'PiPardotHardBouncedInd']

def postprocess(filename1,filename2):
    """Main Function to Run Data Preprocessing"""
    import pandas as pd
    import re
    df = pd.read_csv(filename1)
    data= read_data(filename2)
    df = df.fillna("None")
    print(data)
    contacts = pd.DataFrame(columns=cols)
    partial = pd.DataFrame(columns=cols)
    exact = pd.DataFrame(columns=cols)
    potential = pd.DataFrame(columns=cols)
    if data:
        contacts=pd.DataFrame()
        for i in data.keys():
            for j in data['{}'.format(i)]:
                    address1=''.join([str(df["MailingStreet"][int(i)]).replace("\n", " ") ," ",str(df["MailingCity"][int(i)]).replace("\n", " ")," ",str(df["MailingState"][int(i)]).replace("\n", " ")," ",str(df["MailingCountry"][int(i)]).replace("\n", " ")," ",str(df["MailingZipCode"][int(i)]).replace("\n", "").replace("-","").replace(" ","")])
                    address2=''.join([str(df["MailingStreet"][j]).replace("\n", " ") ," ",str(df["MailingCity"][j]).replace("\n", " ")," ",str(df["MailingState"][j]).replace("\n", " ")," ",str(df["MailingCountry"][j]).replace("\n", " ")," ",str(df["MailingZipCode"][j]).replace("\n", "").replace("-","").replace(" ","")])
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
                        name_12, name_21 = entity_matching(df.iloc[int(i)]["FullName"], df.iloc[j]["FullName"])
                        n12 = encode_percentages(name_12)
                        n21 = encode_percentages(name_21)
    #                     print(df.iloc[int(i)]["FullName"], df.iloc[j]["FullName"],n12,n21)
                    except Exception as e:
                        print("Exception in finding Name Matching : ",e)
                        pass

                     # Performing address Matching
                    try:
    #                     print(i,df["FullName"][i],"  ",j, df["FullName"][j])
                        a12, a21 = entity_matching(address1,address2)
                        outdict["address_p_12"] = encode_percentages(a12)
                        outdict["address_p_21"] = encode_percentages(a21)
                    except Exception as e:
                        print("Exception in finding Name Matching : ",e)
                        pass

                    # Performing email Matching
                    try:
                        if df.iloc[int(i)]["Email"] != "None" and df.iloc[j]["Email"] != "None":
                            e11 = string_matching(df.iloc[int(i)]["Email"], df.iloc[j]["Email"])
                            ep =encode_percentages(e11)

                        elif df.iloc[int(i)]["Email"] == "None" and df.iloc[j]["Email"] == "None":
                            ep=None
                        else:
                            ep=2
    #                     print(df.iloc[int(i)]["Email"], df.iloc[j]["Email"],ep)
                    except Exception as e:
                        print("Exception in finding Email Matching : ",e)
                        pass

                    # Performing Mobile Matching
                    try:
                        if df.iloc[int(i)]["MobilePhone"] != "None" and df.iloc[j]["MobilePhone"] != "None":
                            p12 = phone_matching(df.iloc[int(i)]["MobilePhone"], df.iloc[j]["MobilePhone"])
                            pp=encode_percentages(p12)
                        elif df.iloc[int(i)]["MobilePhone"] == "None" and df.iloc[j]["MobilePhone"] == "None":
                            pp=None
                        else:
                            pp=2
    #                     print(df.iloc[int(i)]["MobilePhone"], df.iloc[j]["MobilePhone"],pp)
                    except Exception as e:
                        print("Exception in Finding Phone Matching Percentages : ",e)
                        pass

                    # Performing Title Matching

                    try:
                        if df.iloc[int(i)]["Title"] != "None" and df.iloc[j]["Title"] != "None":
                            t_12, t_21 = entity_matching(df.iloc[int(i)]["Title"], df.iloc[j]["Title"])
                            t12 = encode_percentages(t_12)
                            t21 = encode_percentages(t_21)
                        elif df.iloc[int(i)]["Title"] == "None" and df.iloc[j]["Title"] == "None":
                            t12=None
                            t21=None
                        else:
                            t21=2
                            t12=2
    #                     print(df.iloc[int(i)]["Title"], df.iloc[j]["Title"],t21,t12)
                    except Exception as e:
                        print("Exception in Finding Phone Matching Percentages : ",e)
                        pass
    #                 print(n12,n21,pp,ep,t12,t21)

                    if ((n12==4 or n12==None) and (n21==4 or n21==None) and (ep==4 or ep==None) and (pp==4 or pp==None) and (t12==4 or t12==None) and (t21==4 or t21==None)):
                        # print('Exact Match')
                        contacts=contacts.append(df.iloc[int(i)])
                        exact = exact.append(df.iloc[int(i)])
                        exact = exact.append(df.iloc[int(j)])

                    elif ((n12>2 and n21>2 )and (ep==4 or pp==4 or (a12==4 and a21==4)))  :
                        # print('Potential Match')
                        potential = potential.append(df.iloc[int(i)])
                        potential = potential.append(df.iloc[int(j)])

                        if df.iloc[int(i)]["Email"] and df.iloc[int(j)]["Email"] and ( df.iloc[int(i)]["Email"] != df.iloc[int(j)]["Email"]):
                            df.iloc[int(i)]["Email"]="".join([str(df.iloc[int(i)]["Email"]),",",str(df.iloc[int(j)]["Email"])])
                        if df.iloc[int(i)]["MobilePhone"] and df.iloc[int(j)]["MobilePhone"] and (df.iloc[int(i)]["MobilePhone"] != df.iloc[int(j)]["MobilePhone"]):
                            df.iloc[int(i)]["MobilePhone"]="".join([str(df.iloc[int(i)]["MobilePhone"]),",",str(df.iloc[int(j)]["MobilePhone"])])
                        contacts=contacts.append(df.iloc[int(i)])
                        # Uncomment the below line if you want to add the changed line to be added to the csv
                        # potential = potential.append(df.iloc[int(i)])
    #
                    else :
                        # print('Partial Match')
                        contacts=contacts.append(df.iloc[int(i)])
                        contacts=contacts.append(df.iloc[j])
                        partial = partial.append(df.iloc[int(i)])
                        partial = partial.append(df.iloc[j])
        fin=[]

        for i in data.keys():
            fin.append(int(i))
            for j in data['{}'.format(i)]:
                # print(j)
                fin.append(j)
        df=df.drop(df.index[fin])
        contacts=contacts[cols]
        partial = partial[cols]
        potential = potential[cols]
        exact = exact[cols]
        df=df[cols]
    #     print(contacts.shape)
        contacts=contacts.append([df])
        contacts.to_csv('dataset/contacts_clean.csv')
        partial.to_csv("dataset/partial_matches.csv")
        potential.to_csv("dataset/potential_matches.csv")
        exact.to_csv("dataset/exact_matches.csv")
    #     print(df.shape,contacts.shape)
    else:
        print("No match found")
# if __name__ == '__main__':
#    postprocess('../dataset/contacts.csv','../txt files/matches_clean.txt')



