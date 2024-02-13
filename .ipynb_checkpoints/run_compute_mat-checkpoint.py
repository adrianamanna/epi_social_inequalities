from utils.fn_matrices import *
import yaml

import os

if not os.path.exists("./_matrices"):
    os.makedirs("./_matrices")

with open("./config_mats.yaml", "rb") as fp:
    config=yaml.load(fp, Loader=yaml.SafeLoader)
print(config)

# a. uploading data
data_path = './data/'
data = pd.read_pickle(data_path+f'data4th_{config["data_type"]}.pkl')

for vars_ in config['VARS']:
    print(vars_)
    
    #b. computing matrices 
    RES = {}
            
    # cleaning outliers at 99 percentile
    p = 98
    cut = np.percentile(data['tot_all_'],p)
    data = data[data['tot_all_']<=cut]

    RES['4th W'] = compute_decoupled_matrices(vars_, data, 'all_')
        
    # c. saving 
    save_Ms('Ms_epi_wave_a_'+config['data_type']+'_all__'+'-'.join(vars_), RES)
    print('Computing matrices decoupled by:'+'-'.join(vars_))