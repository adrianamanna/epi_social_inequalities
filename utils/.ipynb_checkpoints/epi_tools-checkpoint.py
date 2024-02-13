import pandas as pd
import numpy as np
import itertools
import json
import scipy.linalg as la




# POPULATION
def initial_population(data, strat_vars):
    if (len(strat_vars)>1) & (strat_vars[-1]=='age_group7'):
        data_age = data.dropna(subset = ['age_group7'], how  = 'any')
        P_age = dict(data_age.groupby(['age_group7'])['w'].sum()/sum(data_age['w'])) 
    
    data = data.dropna(subset = strat_vars, how  = 'any')
    
    # - COMPUTING POPULATION DISTRIBUTION
    pop_dist = dict(data.groupby(strat_vars)['w'].sum()/sum(data['w']))

    
    # This loop is needed to be sure that the intitial 
    # population has the right number of compartments
    # ie. filling with 0 in case there are no observation 
    # in a given stratifiaction of the data
    try:
        var_values= [sorted(data[var].unique()) for var in strat_vars]
    except:
        var_values= [(data[var].unique()) for var in strat_vars]
        
    if len(strat_vars)>1:
        keys = list(itertools.product(*var_values))
    else:
        keys = var_values[0]

    # loop to put the zeros id missing observation in substrata 
    # any subset of the population
    for key in keys:
        try:
            pop_dist[key]
        except: 
            pop_dist[key] = 0

    pop_dist = dict(sorted(pop_dist.items()))
       
        
        
    # This condition serve a fare in modo che 
    # la somma sull'età della distribuzione per eta + 1dim/2dim è
    # la dist per età siano  ugiali
    
    if (len(strat_vars)>1) & (strat_vars[-1]=='age_group7'):
        dist_df = pd.DataFrame(pop_dist, index = range(1)).T.reset_index()
        cols_names = ['var_{}'.format(i) for i in range(len(strat_vars))]
        
        dist_df.columns = [*cols_names,'p']
        sum_lev_age = dict(dist_df.groupby(cols_names[-1]).sum().reset_index()['p'])
        
        dist_df['P_age']    = dist_df[cols_names[-1]].map(P_age)
        dist_df['sum_lev_age'] = dist_df[cols_names[-1]].map(sum_lev_age)
        dist_df['p_dist'] = dist_df['p']*dist_df['P_age']/dist_df['sum_lev_age']
        
        pop_dist  = dict(dist_df.groupby(cols_names)['p_dist'].sum())

    '''(var1, var2, var3):{}'''
    return pop_dist




def get_vax_dict(data, strat_vars, pop_dist, wave):

    d = data.groupby(strat_vars + ['covid_vax'])['w'].sum().reset_index()

    dp = d.pivot(index = 'covid_vax', columns = strat_vars ).T.reset_index().fillna(0).drop('level_0', axis = 1)
    dp['%vax'] = dp[1.0]/ (dp[1.0]+dp[2.0])

    if len(strat_vars) != 1:
        dp['key'] = dp[strat_vars].apply(lambda x: tuple(x), axis = 1)
    else:
        dp['key'] = dp[strat_vars].copy()

    VACC_dict = dict(dp[['key', '%vax']].values)

    # adding zeros for kids vaccination
    for key in pop_dist:
        try: 
            VACC_dict[key] = VACC_dict[key]
        except:
            VACC_dict[key] = 0
    return VACC_dict



def get_vax_scenario(wave,strat_vars,pop_dist,P_age,data_vax, vax_scenario = None):
    
    if vax_scenario =='by_ageANDvar2':
        vax_dist_d1age = get_vax_dict(data_vax, strat_vars, pop_dist, wave) # P(v|dim1,age)
        vax_dist = {key: vax_dist_d1age[key]*pop_dist[key] for key in pop_dist}
    
    elif vax_scenario == 'by_age':
        vax_dist_age = get_vax_dict(data_vax, [strat_vars[-1]], P_age, wave) # P(v|age)
        vax_dist = {key: vax_dist_age[key[-1]]*pop_dist[key] for key in pop_dist} 
        
    elif vax_scenario == 'no_vax':
        vax_dist = {key:0 for key in pop_dist}
    else:
        print('define vax_scenario: by_ageANDvar2, by_age,no_vax')
        return 
    return vax_dist


def get_vax_scenario_M1(wave,P_age,data_vax, vax_scenario = None):
    if vax_scenario == 'by_age':
        vax_dist_age = get_vax_dict(data_vax, ['age_group7'], P_age, wave) # P(v|age)
        vax_dist = {key: vax_dist_age[key]*P_age[key] for key in P_age} 
        
    elif vax_scenario == 'no_vax':
        vax_dist = {key:0 for key in P_age}
    else:
        print('define vax_scenario_M1:by_age,no_vax')
        return 
    return vax_dist


#  .. compartments 
def init_C_empty(keys):
    return {key:0 for key in keys}

def init_C_by_dist(keys, dist, tot_C):
    C0 = {}
    for key in keys:
        C0[key] = dist[key]*tot_C
    return C0



def init_S(keys, N, pop,
           E0,  E0v1,  E0v2,
           I0,  I0v1,  I0v2,
           R0,  R0v1,  R0v2,
           D0,  D0v1,  D0v2,
                S0v1,  S0v2):
    S0 = {}
    for key in keys:
        S0[key] =  pop[key]* N -(E0[key]+ E0v1[key]+ E0v2[key]+
                                 I0[key]+ I0v1[key]+ I0v1[key]+
                                 R0[key]+ R0v1[key]+ R0v1[key]+
                                 D0[key]+ D0v1[key]+ D0v1[key]+
                                          S0v1[key]+ S0v2[key])
    return S0



def init_C0(pop, N, seeds_E, seeds_I, seeds_R,dist_init_v1 = None,dist_init_v2 = None):
    keys = pop.keys()
    # nota: la 2 dose non è modellata qui!!!!!!
    
    if dist_init_v1 != None:
        pv1 = sum(dist_init_v1.values())
    else:
        pv1 = 0
    
    N_v1 = N * pv1
    seed_E_v1 =  seeds_E * pv1
    seed_I_v1 =  seeds_I * pv1
    seed_R_v1 =  seeds_R * pv1
    
    
    D0v1 = init_C_empty(keys)
    D0v2 = init_C_empty(keys)
    Da0v1 = init_C_empty(keys)
    Da0v2 = init_C_empty(keys)

    E0 = init_C_by_dist(keys,pop,seeds_E-seed_E_v1)
    I0 = init_C_by_dist(keys,pop,seeds_I-seed_I_v1)
    R0 = init_C_by_dist(keys,pop,seeds_R-seed_R_v1)
    D0  = init_C_empty(keys)
    Da0 = init_C_empty(keys)

    if dist_init_v1 == None:
        S0v1 = init_C_empty(keys)
        E0v1 = init_C_empty(keys)
        I0v1 = init_C_empty(keys)
        R0v1 = init_C_empty(keys)
    else:
        S0v1 =  init_C_by_dist(keys, dist_init_v1, N_v1-seed_E_v1-seed_I_v1-seed_R_v1)
        E0v1 =  init_C_by_dist(keys, dist_init_v1, seed_E_v1) 
        I0v1 =  init_C_by_dist(keys, dist_init_v1, seed_I_v1) 
        R0v1 =  init_C_by_dist(keys, dist_init_v1, seed_R_v1) 
    
    
    
    if dist_init_v2 == None:
        S0v2 = init_C_empty(keys)
        E0v2 = init_C_empty(keys)
        I0v2 = init_C_empty(keys)
        R0v2 = init_C_empty(keys)
        
    S0 =   init_S(keys,N,pop, 
                  E0,  E0v1,  E0v2,
                  I0,  I0v1,  I0v2, 
                  R0,  R0v1,  R0v2,
                  D0,  D0v1,  D0v2,
                  S0v1,  S0v2)

    C0 = [S0, S0v1, S0v2, E0, E0v1, E0v2, I0, I0v1, I0v2,R0, R0v1, R0v2, D0, D0v1, D0v2, Da0, Da0v1, Da0v2]
    return C0


# - EPI PARAMETERS

def get_beta(M,r0,mu_val):
    eigvals, eigvecs = la.eig(M)
    leading  = eigvals.real[0]
    beta_val = mu_val*r0/(leading)
    return beta_val



#- MANIPULATING RESULTS

# Getting the sum over compartments of vaccination [by age]
def SUM_C_key(RES, C):
    keys = list(RES['S'][0].keys())
    SUM_key_lists = [[] for k in  range(len(keys))]
    for c_ in RES[C]:
        res_c_ = pd.DataFrame(c_)
        for key,SUM_list in zip(res_c_.columns,SUM_key_lists):
            SUM_list.append(res_c_[key].values)
    return {key: sum(SUM_list) for key,SUM_list in zip(res_c_.columns,SUM_key_lists)}



def SUM_C_lev(RES,C,lev):
    #keys = list(pd.DataFrame(RES['S'][0]).sum(level = lev, axis = 1).columns)
    keys = list(pd.DataFrame(RES['S'][0]).groupby(level = lev, axis =1).sum().columns)

    SUM_key_lists = [[] for k in  range(len(keys))]
    for c_ in RES[C]:
        res_c_ = pd.DataFrame(c_).groupby(level = lev, axis = 1).sum()
        for key,SUM_list in zip(res_c_.columns,SUM_key_lists):
            SUM_list.append(res_c_[key].values)
    return {key: sum(SUM_list) for key,SUM_list in zip(res_c_.columns,SUM_key_lists)}



#. Getting the sum over ages and vaccination compartments 
#. S_tot = S+Sv1+Sv2
def SUM_C(RES, C):
    SUM_key_list = []
    for c_ in RES[C]:
        SUM_key_list.append(pd.DataFrame(c_).T.sum(axis = 0).values)
    return  sum(SUM_key_list)





