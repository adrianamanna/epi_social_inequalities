import numpy as np
import pandas as pd
import json

from copy import deepcopy
import itertools



# COMPUTE THE CONTACT MATRIX BY AGE
def weighted_contact_matrix(data_Ni, contact_type):
    '''
    NOTE: 
    Input are preprcesserd: 
    - outlier are escluded at p level (98%)
    - obs with NaN values in the contact variable are dropped

    '''
    age_contact_vars = [contact_type+str(i) for i in range(8)] # ie. proxy_0, proxy_1 etc.
    
    df = deepcopy(data_Ni)
    df.set_index('id', inplace = True)

    #. Dropping nan in contact vars: 
    #. NOTE:  this is important to have the right number at the denominator when computing the averages
    df = df.dropna(subset = age_contact_vars, how = 'all')
    # - - - - - - - - - - - - - - - - - - - - - - -  
    
    df = df[itertools.chain(age_contact_vars, ['age_group8', 'w'])]

    # COMPUTING THE MATRIX
    #. multiplying n contact for the weights
    df[age_contact_vars] = df[age_contact_vars].apply(lambda x: x*df.w)
    
    df_age = df.groupby('age_group8').agg({'w' :"sum"})
    df_age = df_age.join(pd.DataFrame(range(8)).set_index(0),how="right").fillna(0)
    
    df_grouped_sum = df.groupby('age_group8').agg({**{contact_type+str(i) :"sum" for i in range(8)}})
    df_grouped_mean = df_grouped_sum[age_contact_vars].apply(lambda x: x/df_age.w)

    M = df_grouped_mean[[contact_type+str(i)  for i in range(8)]].join(pd.DataFrame(range(8)).set_index(0),how="right").values
    
    k_mean = sum(df[[c for c in df.columns if contact_type in c]].sum(axis=1))/ df["w"].sum()
    # !! rows 'from' columns 'to' 
    return {'M': M.tolist(), 'k': k_mean, 'pop': df_age.values.tolist()}


def compute_decoupled_matrices(strat_vars, data, contact_type):
        
    DATA = deepcopy(data)
    
    if strat_vars[0] == 'aggregate':        
        agg_res = weighted_contact_matrix(DATA, contact_type)
        return  {'aggregate': agg_res }
        
    else:
        RES_var = {}
        # 1. drop the observation with nan in the strat_vars
        #DATA.dropna(subset =strat_vars, inplace = True)
 
        # 2. 
        for sub_data in DATA.groupby(strat_vars):
            # - defining the label
            if len(strat_vars)>1:
                label= '*'.join([var_n+'-'+str(var_val) for var_n, var_val in  zip(strat_vars, sub_data[0])])
            else:
                label = strat_vars[0]+'-'+str(sub_data[0]) 
            print('{}'.format(label), end = '\r')

            # we can add bootstrap
            RES_var[label] = weighted_contact_matrix(sub_data[1], contact_type)
    return RES_var 


# SAVING
def save_Ms(name, RES_M):
    with open('./_matrices/'+name+'.json', 'w') as fp:
        json.dump(RES_M, fp)
    fp.close()
    return

# UPLOADING
def upload_Ms(wave_type, data_type, dep_var, vars_):    
    file_path = './_matrices/Ms_{}_{}_{}_{}.json'.format(
        wave_type,data_type, dep_var,'-'.join(vars_))
    f = open (file_path, "r")
    Ms_allW = json.loads(f.read())

    return Ms_allW



# PREPROCESSING FOR MODELLING
def M_prep(wave_type, data_type, dep_var, vars_, wave):
    M_str = upload_Ms(wave_type, data_type,dep_var, vars_)[wave]

    M = {}
    for k_M in M_str.keys():
        #print(k_M)
        try:
            k_num = eval(k_M.split('*')[0].split('-')[1]),eval(k_M.split('*')[1].split('-')[1])
        except:
            k_num = (eval(k_M.split('-')[1]),)

        M.setdefault(k_num,{})
        M[k_num] = M_str[k_M]['M']
        
    return M
