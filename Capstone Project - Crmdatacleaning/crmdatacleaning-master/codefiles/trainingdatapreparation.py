def read_data(filename):
    """Function to read dataset from filename"""
    data_frame = None
    import pandas as pd

    if str(filename).endswith("csv"):
        data_frame = pd.read_csv(filename)
        # data_frame = pd.read_csv(filename)
    elif str(filename).endswith("xlsx"):
        data_frame = pd.read_excel(filename)
    else:
        print("Please Provide Dataset in CSV or Excel Format")
    return data_frame

def Rand(start, end, num): 
    import random
    res = [] 
    
    for j in range(num): 
        res.append(random.randint(start, end)) 

    return res

def trainingdataprep(filename):
    import pandas as pd
    print("preparing....")

    data = read_data(filename)


    train_data_same_name=pd.DataFrame()
    train_data_same_email=pd.DataFrame()
    train_data_same_title=pd.DataFrame()
    train_data_same_phone=pd.DataFrame()
    train_data_overall=pd.DataFrame()
    train_data_random=pd.DataFrame()
    
    train_data_same_name = train_data_same_name.append(data[data['fullname_1'] == data['fullname_2']])
    train_data_overall = train_data_overall.append(train_data_same_name.iloc[Rand(0,train_data_same_name.shape[0],150)])
    
    train_data_same_email = train_data_same_email.append(data[data['email_1'] == data['email_2']])
    train_data_overall = train_data_overall.append(train_data_same_email.iloc[Rand(0,train_data_same_email.shape[0],150)])
      
    train_data_same_title = train_data_same_title.append(data[data['title_1'] == data['title_2']])
    train_data_overall = train_data_overall.append(train_data_same_title.iloc[Rand(0,train_data_same_title.shape[0],150)])
    
    train_data_same_phone = train_data_same_phone.append(data[data['phone_1'] == data['phone_2']])
    train_data_overall = train_data_overall.append(train_data_same_phone.iloc[Rand(0,train_data_same_phone.shape[0],150)])
    
    train_data_random = train_data_random.append(data.iloc[Rand(0,4000000,150)])
    train_data_overall = train_data_overall.append(train_data_random)
    train_data_overall = train_data_overall[
        ["fullname_1", "fullname_2", "name_p_12", "name_p_21", "phone_1", "phone_2", "phone_present", "phone_p",
         "email_1", "email_2", "email_present", "email_p", "title_1", "title_2", "title_present", "title_p_12",
         "title_p_21", "address_1", "address_2", "address_p_12", "address_p_21", "Target"]]

    train_data_final = train_data_overall.sample(n=500)

    train_data_final=train_data_final[["fullname_1","fullname_2","name_p_12","name_p_21","phone_1","phone_2",
                                       "phone_present","phone_p","email_1","email_2","email_present","email_p","title_1",
                                       "title_2","title_present","title_p_12","title_p_21","address_1","address_2",
                                       "address_p_12","address_p_21","Target"]]
    train_data_final.to_csv('dataset/train_data_final.csv')
    print("done")
# if __name__=='__main__':
#     trainingdataprep('../dataset/data_to_annotate.csv')

