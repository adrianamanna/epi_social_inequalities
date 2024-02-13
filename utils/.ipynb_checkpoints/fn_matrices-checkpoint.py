import numpy as np
import pandas as pd
import json

from copy import deepcopy
import itertools
import numpy as np
import pandas as pd
import json

from copy import deepcopy
import itertools


#  fn for symmetry
# ----------------
def compute_scaling_matrix(Ms,D):
    scaling_M = []
    for M in Ms:
        #M/D
        scaling_M.append(np.divide(M, D, out=np.zeros_like(M), where=(D != 0)))
    return np.array(scaling_M)

def compute_symmetrized_matrices(D_sym, scaling_M):
    Ms_sym=[]
    for M in scaling_M:
        Ms_sym.append(D_sym * M)
    return np.array(Ms_sym)
# ----------------


#COMPUTE THE CONTACT MATRIX BY AGE

def weighted_contact_matrix(data_Ni, contact_type):
    '''
    NOTE: 
    Input are preprcesserd: 
    - outlier are escluded at p level (98%)
    - obs with NaN values in the contact variable are dropped
    '''

    age_contact_vars = [contact_type+str(i) for i in range(7)] # ie. all_0, all_1 etc.
    
    # .7x7 matrix
    df = deepcopy(data_Ni)
    data_Ni[contact_type+'6'] = data_Ni[contact_type+'6']+data_Ni[contact_type+'7']
    data_Ni.drop(columns=[contact_type+'7'], inplace=True)

    df.set_index('id', inplace = True)

    #. Dropping nan in contact vars: 
    #. NOTE:  this is important to have the right number at the denominator when computing the averages
    df = df.dropna(subset = age_contact_vars, how = 'all')
    # - - - - - - - - - - - - - - - - - - - - - - -  
    
    df = df[itertools.chain(age_contact_vars, ['age_group7', 'w'])]

    # COMPUTING THE MATRIX
    #. multiplying n contact for the weights
    df[age_contact_vars] = df[age_contact_vars].apply(lambda x: x*df.w)
    
    df_age = df.groupby('age_group7').agg({'w' :"sum"})
    df_age = df_age.join(pd.DataFrame(range(7)).set_index(0),how="right").fillna(0)
    
    df_grouped_sum = df.groupby('age_group7').agg({**{contact_type+str(i) :"sum" for i in range(7)}})
    df_grouped_mean = df_grouped_sum[age_contact_vars].apply(lambda x: x/df_age.w)

    M = df_grouped_mean[[contact_type+str(i)  for i in range(7)]].join(pd.DataFrame(range(7)).set_index(0),how="right").values
    
    k_mean = sum(df[[c for c in df.columns if contact_type in c]].sum(axis=1))/ df["w"].sum()
    # !! rows 'from' columns 'to' 
    return {'M': M.tolist(), 'k': k_mean, 'pop': df_age.values.tolist()}


def compute_decoupled_matrices(strat_vars, data, contact_type):  
    DATA = deepcopy(data)
    
    if strat_vars[0] == 'aggregate':        
        agg_res = weighted_contact_matrix(DATA, contact_type)
        RES_var =  {'aggregate': agg_res }
        
    else:
        RES_var = {}
        for sub_data in DATA.groupby(strat_vars):
            # - defining the label
            if len(strat_vars)>1:
                label= '*'.join([var_n+'-'+str(var_val) for var_n, var_val in  zip(strat_vars, sub_data[0])])
            else:
                label = strat_vars[0]+'-'+str(sub_data[0]) 
            print('{}'.format(label), end = '\r')

            RES_var[label] = weighted_contact_matrix(sub_data[1], contact_type)  

    # SYMMETRIZATION
    # 1. compute total number of contacts
    Ms_Ctot=[]
    for k in RES_var.keys():
        Ms_Ctot.append(np.nan_to_num(RES_var[k]['M'])*np.array(RES_var[k]['pop']).reshape(1,-1).T) 
    Ms_Ctot = np.array(Ms_Ctot)
        
    # 2. aggregated matrix
    D=np.sum(Ms_Ctot,axis=0)
    D_sym = (D + D.T) / 2

    # 3. symmetrized matrices
    B      = compute_scaling_matrix(Ms_Ctot,D)
    Ms_sym = compute_symmetrized_matrices(D_sym, B)

    # 4. goiung back to the avg values
    RES_var_sy={}
    for i,k in enumerate(RES_var.keys()):
        
        #Cdij = Ms_sym[i]/np.array(RES_var[k]['pop']).reshape(1,-1).T
        Cdij = np.divide(Ms_sym[i],np.array(RES_var[k]['pop']).reshape(1,-1).T,
                         out=np.zeros_like(Ms_sym[i]), where = (np.array(RES_var[k]['pop']).reshape(1,-1).T != 0))
        Cdij = np.nan_to_num(Cdij)
        RES_var_sy[k] = {'M': Cdij.tolist(), 'k': RES_var[k]['k'], 'pop': RES_var[k]['pop']}

    return RES_var_sy


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
