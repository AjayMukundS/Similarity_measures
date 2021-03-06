import pandas as pd
import numpy as np
import category_encoders as ce

def Frequency_table(data):
    num_cat= []
    for col_num in range(len(data.columns)):
        col_name= data.columns[col_num]
        categories = list(data[col_name].unique())
        num_cat.append(len(categories))
    r = data.shape[0]
    s = data.shape[1] 
    freq_table= np.zeros(shape=(max(num_cat),s))
    
    for i in range(s): 
        for j in range(num_cat[i]): 
            count= []
            for num in range(0, r):
                count.append(0)
            for k in range(0,r):
                if (data.iat[k,i] -1== j): 
                    count[k] = 1
                else:
                    count[k] = 0
            freq_table[j][i] = sum(count)
    return(freq_table)

def Goodall2(data):
    data= ordinal_encode(data)
    r = data.shape[0]
    s = data.shape[1]  
    
    freq_table= Frequency_table(data)
    print(freq_table)
    
    freq_rel= freq_table/r
    print(freq_rel)
    
    freq_rel2= freq_rel**2
    print(freq_rel2)
    
    agreement= []
    for i in range(s):
        agreement.append(0)
    
    good2= np.zeros(shape=(r,r))
    
    for i in range(r-1):
        for j in range(1+i, r):
            for k in range(s):
                c = data.iat[i,k]-1
                if (data.iat[i,k] == data.iat[j,k]):
                    logic= freq_rel[:, k] >= freq_rel[c][k]
                    agreement[k] = 1 - sum(freq_rel2[:, k] * logic)
                else:
                    agreement[k] = 0
            if i == j:
                good2[i][j]= 0
            else:
                good2[i][j] = 1-(sum(agreement)/s)
                good2[j][i] = good2[i][j]
    return(good2)
    
def ordinal_encode(data):
    encoding_data= data.copy()
    encoder= ce.OrdinalEncoder(encoding_data)
    data_encoded= encoder.fit_transform(encoding_data)
    return(data_encoded)
