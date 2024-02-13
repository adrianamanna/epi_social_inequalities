import numpy as np
from utils.epi_tools import *



def SEIRDv_age_1dim(
               stop:int,
               P_age, C0, pop, N, M,
               beta_val:float,
               mu_val:float,
               eps_val:float,
               Delta:float=0, 
               g1_v1:float=0,
               g1_v2:float=0,
               g2_v1:float=0,
               g2_v2:float=0, 
               Delta_v2:float = 0,
               
               Omega=None, 
               IFR=None,
               pp=None):
    
    '''
    stop:   number of timesteps to simulate
    P_age:  dict with distribution of population by age 
    
    C0: list of dictionaries [S0,Sv1_0 ..,E0,..,I0,..R0,..D0..]
        [dict {key: pop in C0}, ...]
    pop: dict {key: pop in}
    M:  contact matrix
        dict {key:{key1:c_val, key2:c_val}}
    
    beta_val: infection probability 
    mu_val:   recovery rate (1/d , d:generation time)
    eps_val:  probability to become infectious
    Delta:    delay in reporting the number of deaths [days]
    
    [v]
    g1_v1, g1_v1: efficaci of vaccination against infection (1st,2nd dose)
    g2_v1, g2_v1: efficaci of vaccination death infection (1st,2nd dose)

    Omega: dict {key:{t:percentage_new_vaccinated_t }}
    IFR: rate of death given infection
         dict {key: IFR_key}
         
    '''
    #. CONTROLLI
    [S0,  S0v1,  S0v2, # suseptibles 
     E0,  E0v1,  E0v2, # exposed
     I0,  I0v1,  I0v2, # infecte
     R0,  R0v1,  R0v2, # recovered
     D0,  D0v1,  D0v2, # death
     Da0, D0av1, D0av2 # death registered
    ] = C0

    #if pop.keys()!= M.keys():
        #raise 'Population dict and Contact matrix must have same keys!'   
    #else:
    keys=pop.keys()
    

    if Omega == None:
        Omega = {a: {t:0 for t in range(stop)} for a in keys}
        vaccination = ''
    else:
        if pop.keys()!= Omega.keys():
            raise 'Population dict and Omega dict must have same keys!'    
        vaccination = '[v]'

        
    if IFR == None:
        IFR = {key:0 for key in keys}
        model_type = 'SEIR'
        
    else:
        if pop.keys()!= IFR.keys():
            raise 'Population vector and IFR must have same keys!'
        model_type = 'SEIRD'
    
    # .PRINT
    if pp == True:
        print('Model {}{}[age+1dim]\n::PARAMS::\
        \n\tbeta: {}\n\tmu_val: {}\n\teps: {}\n\tDelta: {}\
        \n\tg1: {},{}\n\tg2:{},{}\n\tDelta_v2: {} '.format(
            model_type,vaccination,
            beta_val,mu_val, eps_val,Delta,
            g1_v1, g1_v2, g2_v1, g2_v2,
            Delta_v2
    
        ))

    #. SET INITIAL COMPARTMENTS
    #  compartment = [var1,var2][time]
    S, Sv1, Sv2 = {}, {}, {}
    E, Ev1, Ev2 = {}, {}, {}
    I, Iv1, Iv2 = {}, {}, {}
    R, Rv1, Rv2 = {}, {}, {}
    D, Dv1, Dv2 = {}, {}, {}
    Da, Dav1, Dav2 = {}, {}, {}

    new_I, new_Iv1, new_Iv2 = {}, {}, {}
    new_D, new_Dv1, new_Dv2 = {}, {}, {}
    new_Da, new_Dav1, new_Dav2 = {}, {}, {}
    
    C_dicts = [S,  Sv1,  Sv2, 
               E,  Ev1,  Ev2,
               I,  Iv1,  Iv2,
               R,  Rv1,  Rv2,
               D,  Dv1,  Dv2,
               Da, Dav1, Dav2,
               new_I,  new_Iv1, new_Iv2,
               new_D,  new_Dv1, new_Dv2,
               new_Da, new_Dav1, new_Dav2]
    
    
    for i,key in enumerate(pop):  
        for c_dict,c0 in zip(C_dicts,C0+[I0, I0v1, I0v2,D0, D0v1, D0v2,Da0, D0av1, D0av2]):

            c_dict.setdefault(key,{})
            c_dict[key][0] = c0[key]

    # . SIMULATING THE EPIDEMIC
    for t in range(1,stop):
        #print('t_{} '.format(t), end = '\r')        
        
        
        #I_age = [(I[key][t-1]+Iv1[key][t-1]+Iv2[key][t-1])/(pop[key]*N) for key in keys]
        I_age = [(sum([I[m_key+(i,)][t-1]   for m_key in M.keys()])+
                  sum([Iv1[m_key+(i,)][t-1] for m_key in M.keys()])+
                  sum([Iv2[m_key+(i,)][t-1] for m_key in M.keys()])
                 )/(P_age[i]*N) for i in range(7)]

        for m_key in M.keys():
            for age_i in range(7):
                M_di = np.nan_to_num(M[m_key][age_i])
                c_d_agei = np.dot(M_di, I_age)
                lambda_val = beta_val*c_d_agei
                
                key = m_key+(age_i,)
                newE   = np.random.binomial(S[key][t-1]   , 1.-np.exp(-lambda_val))
                newEv1 = np.random.binomial(Sv1[key][t-1] , 1.-np.exp(-((1-g1_v1)*lambda_val)))
                newEv2 = np.random.binomial(Sv2[key][t-1] , 1.-np.exp(-((1-g1_v2)*lambda_val)))


                newI   = np.random.binomial(E[key][t-1]   , eps_val)
                newIv1 = np.random.binomial(Ev1[key][t-1] , eps_val)
                newIv2 = np.random.binomial(Ev2[key][t-1] , eps_val)

                potential_deaths = np.random.binomial(I[key][t-1] , mu_val)
                potential_deaths_v1 = np.random.binomial(Iv1[key][t-1] , mu_val)
                potential_deaths_v2 = np.random.binomial(Iv2[key][t-1] , mu_val)  

                newR   = (1-IFR[key])*potential_deaths
                newRv1 = ((1.-((1-g2_v1) * IFR[key])))*potential_deaths_v1
                newRv2 = ((1.-((1-g2_v2) * IFR[key])))*potential_deaths_v2

                newD   = IFR[key]*potential_deaths
                newDv1 = (1-g2_v1)*IFR[key]*potential_deaths_v1
                newDv2 = (1-g2_v2)*IFR[key]*potential_deaths_v2


                newDa   = Delta*newD
                newDav1 = Delta*newDv1
                newDav2 = Delta*newDv2


                S[key][t]   =  S[key][t-1]   -  newE   - Omega[key][t]*S[key][t-1]
                Sv1[key][t] =  Sv1[key][t-1] -  newEv1 + Omega[key][t]*S[key][t-1] - Delta_v2*Sv1[key][t-1]
                Sv2[key][t] =  Sv2[key][t-1] -  newEv2 + Delta_v2*Sv1[key][t-1]

                E[key][t]   =  E[key][t-1]   +  newE   -  newI   - Omega[key][t]*E[key][t-1]
                Ev1[key][t] =  Ev1[key][t-1] +  newEv1 -  newIv1 + Omega[key][t]*E[key][t-1] - Delta_v2*Ev1[key][t-1]
                Ev2[key][t] =  Ev2[key][t-1] +  newEv2 -  newIv2 + Delta_v2*Ev1[key][t-1]


                I[key][t]   =  I[key][t-1]   +  newI   -  newR
                Iv1[key][t] =  Iv1[key][t-1] +  newIv1 -  newRv1
                Iv2[key][t] =  Iv2[key][t-1] +  newIv2 -  newRv2

                R[key][t]   =  R[key][t-1]   +  newR
                Rv1[key][t] =  Rv1[key][t-1] +  newRv1
                Rv2[key][t] =  Rv2[key][t-1] +  newRv2

                D[key][t]   =  D[key][t-1]   +  newD
                Dv1[key][t] =  Dv1[key][t-1] +  newDv1
                Dv2[key][t] =  Dv2[key][t-1] +  newDv2


                #print(m_key, t)
                #print(Da[m_key][t-1] )
                Da[key][t]   =  Da[key][t-1]   +  newDa
                Dav1[key][t] =  Dav1[key][t-1] +  newDav1
                Dav2[key][t] =  Dav2[key][t-1] +  newDav2

                new_I[key][t]   = newI
                new_Iv1[key][t] = newIv1
                new_Iv2[key][t] = newIv2

                new_D[key][t]   = newD
                new_Dv1[key][t] = newDv1
                new_Dv2[key][t] = newDv2

                new_Da[key][t]   = newDa
                new_Dav1[key][t] = newDav1
                new_Dav2[key][t] = newDav2
        
        totI = sum([I[key][t]+Iv1[key][t]+Iv2[key][t] for key in keys])
        #print(totI, t)
        
        if (t >400) and (totI < 12):
            break
    
    
    RES = {'S':[S,Sv1,Sv2],
           'E':[E,Ev1,Ev2],
           'I':[I,Iv1,Iv2], 
           'R':[R,Rv1,Rv2], 
           'D':[D,Dv1,Dv2],
           'Da':[Da,Dav1,Dav2],
           'new_I' :[new_I, new_Iv1, new_Iv2],
           'new_D' :[new_D, new_Dv1, new_Dv2],
           'new_Da':[new_Da,new_Dav1,new_Dav2]}
    
    return RES,t


def RES_SEIRDv_age_1dim(RES,strat_vars): 
    # Getting the sum over compartments of vaccination
    #. - overall (C_tot = C+Cv1+Cv2)
    
    '''RES_tot ={'S':[], 'E':} '''
    RES_tot = {}
    for C in RES.keys():
        RES_tot[C] = SUM_C(RES, C)  

    #. - by age and dim1/...
    ''' RES_ = {C:{ key0:[] , key2:[]}}'''
    RES_key= {}
    for C in RES.keys():
        RES_key[C] = SUM_C_key(RES, C) 

    RES_all = {}
    for lev,var in enumerate(strat_vars):
        print(lev,var)

        RES_var = {}
        for C in RES.keys():
            RES_var[C] = SUM_C_lev(RES, C,lev)

        RES_all['RES_{}'.format(var)] = RES_var
    
    RES_all['RES_tot'] = RES_tot
    RES_all['RES_key'] = RES_key
    
    return RES_all