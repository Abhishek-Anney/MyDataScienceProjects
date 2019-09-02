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

def data_clean(data,retain=["name_p_12","name_p_21","phone_present","phone_p","email_present","email_p","title_present","title_p_12","title_p_21","address_p_12","address_p_21","Target"]):
    '''function to remove unnecessory column'''
    columns_to_retain = retain
    data_training = data[columns_to_retain]
    return data_training


def trainModel(filename):
    import pickle
    import pandas as pd
    print("started training ....")
    train_data=read_data(filename)
    #     train_data.head()
    train_data=data_clean(train_data)
    model_accuracy={}

    X=train_data.drop('Target',axis=1)
    # X=X.drop('Unnamed: 0.1',axis=1)

    Y=train_data['Target']

    from sklearn.svm import SVC
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score

    X_train,X_test, Y_train, Y_test = train_test_split(X,Y,random_state=0, test_size=0.2,stratify=Y)
    from sklearn.preprocessing import MinMaxScaler
    scaling = MinMaxScaler(feature_range=(-1,1)).fit(X_train)
    X_train_scale = scaling.transform(X_train)
    X_test_scale = scaling.transform(X_test)


    # %time
    model1_lin=SVC(kernel='linear')
    model1_lin.fit(X_train_scale,Y_train)
    svm_linear_model = 'model/svm_linear_model.sav'
    pickle.dump(model1_lin, open(svm_linear_model, 'wb'))
    svc_linear_predic=model1_lin.predict(X_test_scale)
    svc_linear_accuracy=accuracy_score(svc_linear_predic,Y_test)
    model_accuracy['svm_linear']=svc_linear_accuracy

    # %time
    model1_poly=SVC(kernel='poly')
    model1_poly.fit(X_train_scale,Y_train)
    svm_poly_model = 'model/svm_poly_model.sav'
    pickle.dump(model1_poly, open(svm_poly_model, 'wb'))
    svc_poly_predic=model1_poly.predict(X_test_scale)
    svc_poly_accuracy=accuracy_score(svc_poly_predic,Y_test)
    model_accuracy['svm_poly']=svc_poly_accuracy

    # %time
    model1_rbf=SVC(kernel='rbf')
    model1_rbf.fit(X_train_scale,Y_train)
    svm_rbf_model = 'model/svm_rbf_model.sav'
    pickle.dump(model1_rbf, open(svm_rbf_model, 'wb'))
    svc_rbf_predic=model1_rbf.predict(X_test_scale)
    svc_rbf_accuracy=accuracy_score(svc_rbf_predic,Y_test)
    model_accuracy['svm_rbf']=svc_rbf_accuracy

    # %time
    model1_sig=SVC(kernel='sigmoid')
    model1_sig.fit(X_train_scale,Y_train)
    svm_sig_model = 'model/svm_sig_model.sav'
    pickle.dump(model1_sig, open(svm_sig_model, 'wb'))
    svc_sigmoid_predic=model1_sig.predict(X_test_scale)
    svc_sigmoid_accuracy=accuracy_score(svc_sigmoid_predic,Y_test)
    model_accuracy['svm_sigmoid']=svc_sigmoid_accuracy

    from sklearn.ensemble import RandomForestClassifier
    model2=RandomForestClassifier()
    model2.fit(X_train,Y_train)
    randomforestmodel = 'model/randomforest_model.sav'
    pickle.dump(model2, open(randomforestmodel, 'wb'))
    rand_predic=model2.predict(X_test)
    rand_accuracy= accuracy_score(rand_predic,Y_test)
    model_accuracy['randomforest']=rand_accuracy


    from sklearn.tree import DecisionTreeClassifier
    model3=DecisionTreeClassifier()
    model3.fit(X_train,Y_train)
    decisiontreemodel = 'model/decisiontree_model.sav'
    pickle.dump(model3, open(decisiontreemodel, 'wb'))
    dec_predic=model3.predict(X_test)
    dec_accuracy=accuracy_score(dec_predic,Y_test)
    model_accuracy['decisiontree']=dec_accuracy
    print('finished training....')
    return model_accuracy


def validationfileprep(filename):
    """#Preparing Validation Set"""

    data = read_data("data_to_annotate.csv")


    import random
    import pandas as pd

    def Rand(start, end, num): 
        res = [] 

        for j in range(num): 
            res.append(random.randint(start, end)) 

        return res

    train_data_same_name=pd.DataFrame()
    train_data_same_email=pd.DataFrame()
    train_data_same_title=pd.DataFrame()
    train_data_same_phone=pd.DataFrame()
    train_data_overall=pd.DataFrame()

    train_data_random=pd.DataFrame()

    train_data_same_name = train_data_same_name.append(data[data['fullname_1'] == data['fullname_2']])
    train_data_overall= train_data_overall.append(train_data_same_name.iloc[Rand(0,train_data_same_name.shape[0],150)])

    train_data_same_email = train_data_same_email.append(data[data['email_1'] == data['email_2']])
    train_data_overall = train_data_overall.append(train_data_same_email.iloc[Rand(0,train_data_same_email.shape[0],150)])

    train_data_same_title = train_data_same_title.append(data[data['title_1'] == data['title_2']])
    train_data_overall = train_data_overall.append(train_data_same_title.iloc[Rand(0,train_data_same_title.shape[0],150)])

    train_data_same_phone = train_data_same_phone.append(data[data['phone_1'] == data['phone_2']])
    train_data_overall = train_data_overall.append(train_data_same_phone.iloc[Rand(0,train_data_same_phone.shape[0],150)])

    train_data_random = train_data_random.append(data.loc[Rand(0,4000000,150)])
    train_data_overall = train_data_overall.append(train_data_random)

    # train_data_random.to_csv('train_data_random.csv')
    # train_data_same_name.to_csv('train_data_same_name.csv')
    # train_data_same_title.to_csv('train_data_same_title.csv')
    # train_data_same_email.to_csv('train_data_same_email.csv')
    # train_data_same_phone.to_csv('train_data_same_phone.csv')
    train_data_overall.to_csv('train_data_overall_validation.csv')

    # train_data_overall.shape

    validation_final=pd.DataFrame()
    validation_final= validation_final.append(train_data_overall.iloc[Rand(0,train_data_overall.shape[0],200)])
    validation_final.to_csv('validation_final.csv')
    #exported to set target values


def validation(filename):
    import pickle
    #It includes the target values now
    train_data_overall=read_data('validation_final.csv')

    train_data= data_clean(train_data_overall)
    train_data.to_csv("train_data_final_clean.csv")

    X=train_data.drop('Target',axis=1)

    Y=train_data_overall['Target']

    loaded_model = pickle.load(open('randomforest_model.sav', 'rb'))
    result = loaded_model.score(X, Y)
    return result

if __name__ == '__main__':
  accuracy=trainModel("dataset/train_data_final.csv")
  print(accuracy)


