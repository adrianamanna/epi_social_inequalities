import yaml
import pickle

from multiprocessing import cpu_count
#import joblib

from utils.epi_models_age_1dim import *
from utils.fn_matrices import M_prep , upload_Ms
import os



with open("./config_sim.yaml", "rb") as fp:
    config=yaml.load(fp, Loader=yaml.SafeLoader)
print(config)

if not os.path.exists("./"+config['resPath']):
    os.makedirs("./"+config['resPath'])


# b. read MASZK data
data_vax = pd.read_pickle( './data/data4th_a.pkl')
data = pd.read_pickle( './data/data4th_all.pkl')
strat_vars= [*config['vars'],'age_group8']


# P
pop_dist = initial_population(data,  strat_vars)
P_age    = initial_population(data,   ['age_group8'])

# MATRICES
M = M_prep('epi_wave_a', config['data_type'], 'all_', config["vars"],config["wave"])
M = np.nan_to_num(M)

# VACCINATION COVERAGE
vax_dist = get_vax_scenario('epi_wave_a',strat_vars,pop_dist,P_age,data_vax, config["vax_scenario_m2"])


# SETTING PARAMETERS

# .computing the infection rate
M_str_all = upload_Ms('epi_wave_a', config['data_type'], 'all_', ['aggregate'])[config["wave"]]
M_all = M_str_all['aggregate']['M']

beta_val = get_beta(M_all,config['r0'], config['mu_val'])

# . setting parameters
mu_val =   config['mu_val']
eps_val = config['eps_val']

seeds_E = config['seeds_E']
seeds_I = config['seeds_I']
seeds_R = config['seeds_R']

if config['vax_scenario_m2']=='no_vax':
    g1_v1_val = 0
    g2_v1_val = 0
else:
    g1_v1_val = config['g1_v1_val']
    g2_v1_val = config['g2_v1_val']


def run():

    C0_M2 = init_C0(pop_dist, config['N'], seeds_E, seeds_I, seeds_R,dist_init_v1 = vax_dist,dist_init_v2 = None)
    RESa_M2,t_m2 = SEIRDv_age_1dim(
                           config['stop_epi'],P_age, C0_M2, pop_dist, config['N'], M,
                           beta_val,
                           mu_val,
                           eps_val,
                           Delta=0, 
                           g1_v1 = g1_v1_val,
                           g1_v2 = 0,
                           g2_v1= g2_v1_val,
                           g2_v2=0, Delta_v2=0,

                           Omega=None, 
                           IFR=None,
                           pp=False)
    return RESa_M2

all_RES=[]
for i in range(config['iterations']):
    print('iteration #: '+str(i), end='\r')
    res_ =run() 
    all_RES.append(res_)


#executor = joblib.Parallel(n_jobs=1, backend='multiprocessing')
#tasks = (joblib.delayed(run)(i) for i in range(config['iterations']))
#all_RES = executor(tasks)

with open(config['resPath']+'/simulations_{}.pickle'.format(''.join(strat_vars)),  'wb') as handle:
    pickle.dump(all_RES, handle)

print('SIMULATIONS ARE OVER')  
