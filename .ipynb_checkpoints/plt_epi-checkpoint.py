import pandas as pd
import numpy as np 

import yaml
import pickle

import os
if not os.path.exists("./_figures"):
    os.makedirs("./_figures")

from utils.simulation_prep_tools import *
from utils.epi_tools import initial_population
from utils.labs import *

import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 10, 'font.style': 'normal', 'font.family':'serif'})


with open("./config_sim.yaml", "rb") as fp:
    config=yaml.load(fp, Loader=yaml.SafeLoader)

res_path = config['resPath']
fig_path = config['figPath']

data = pd.read_pickle( './data/data4th_all.pkl')


N = config['N']
strat_vars = [*config['vars'],'age_group7']

with open(config['resPath']+'/simulations_{}.pickle'.format(''.join(strat_vars)), 'rb') as f: 
    all_RES = pickle.load(f)

print('#simulations:', len(all_RES))



# PREPROCESSING
# . A. computing infection curves

ress_I = []
for IL, LEV in enumerate([0,1]):
    ress_I.append(des_by_lev(all_RES, 'new_I', LEV))



# . B. computing attack rate
Rs_key = des_by_key(all_RES, 'R')

pop_dist = initial_population(data,  strat_vars)
AR_key = {}
for key in Rs_key.keys():
    AR_key[key] = {}
    for stat in Rs_key[key].keys():

        AR_key[key][stat] = np.divide(Rs_key[key][stat][-1], pop_dist[key]*N,
                  out=np.full_like(Rs_key[key][stat][-1],np.nan),
                  where=(pop_dist[key]*N != 0))
        
AR_key_df = pd.DataFrame(AR_key).T.reset_index()
AR_key_df = AR_key_df.rename(columns = {'level_'+str(i):var for i,var in enumerate(strat_vars) })


# PLOT
lab_age=labs['age_group7']

fig, axs = plt.subplots(1, 3, figsize =(10, 3))#, sharey='row')

# .a. plotting infection curves
for IL, LEV in enumerate([0,1]):
    res_I = ress_I[IL]

    LAB = labs[strat_vars[IL]]
    c = C_VAR_LEVS[strat_vars[IL]]
    pop_dist = initial_population(data, [strat_vars[IL]])

    for il,i in enumerate(res_I):
        rI = res_I[i]
        x = range(len(rI['median']))
        axs[IL].plot(x, rI['median']/(pop_dist[i]*N),ls = '-',lw = 1.5,c = c[il], label = LAB[i])
        axs[IL].fill_between(x, rI['p25']/(pop_dist[i]*N), rI['p75']/(pop_dist[i]*N),color = c[il], alpha = 0.3)


    axs[IL].legend(fontsize = 8, loc = 'upper left', ncol = 1, frameon =False, columnspacing=0.5, handletextpad=0.12, labelspacing=0.14 )
    axs[IL].set_ylabel('% new infected')
    axs[IL].set_xlabel('time')
    axs[IL].set_title(strat_vars[IL], loc = 'left', fontsize = 11)

# .b. plotting attack rate
ax = axs[2]
x= np.arange(7)
    
for i_var, lev in enumerate(AR_key_df[strat_vars[0]].unique()):
    ar_df = AR_key_df[AR_key_df[strat_vars[0]]==lev]
    
    y = ar_df['median'].astype(float)
    yl = ar_df['p25'].astype(float)
    yu = ar_df['p75'].astype(float)

    c = C_VAR_LEVS[strat_vars[0]]
    LAB = labs[strat_vars[0]]

    ax.plot(x,y,ls = '-',lw = 1.1, c = c[i_var],marker ='o',mfc='w', mew =1.5,ms=4.4, alpha = 0.91, label = LAB[lev])
        
    ax.fill_between(x, yl, yu,color = c[i_var], alpha = 0.1)
    ax.set_xticks([i for i in list(lab_age.keys())])
    ax.set_xticklabels([lab_age[i] for i in x], fontsize= 9, rotation = 270)

    ax.legend(fontsize = 8, ncol = 1, frameon =False, columnspacing=0.5, handletextpad=0.12, labelspacing=0.14 )
    ax.set_ylabel('attack rate')
    ax.set_xlabel('age group')

fig.suptitle('vax scenario:'+ config['vax_scenario_m2']+ '  $- R_0$:' + str(config['r0']))
plt.tight_layout()
plt.savefig(config['figPath']+'/simulations_{}.pdf'.format(strat_vars[0]), bbox_inches='tight')

    
