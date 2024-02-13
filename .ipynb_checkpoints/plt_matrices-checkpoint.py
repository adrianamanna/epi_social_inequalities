from utils.fn_matrices import upload_Ms
from utils.plot_tools import *
import yaml

import os
if not os.path.exists("./_figures"):
    os.makedirs("./_figures")

with open("./config_mats.yaml", "rb") as fp:
    config=yaml.load(fp, Loader=yaml.SafeLoader)

    

for var in config['VARS_plt']:
    print(var)
    res =  upload_Ms('epi_wave_a', config['data_type'], 'all_', var)
    res_wave = res[config['wave']]
    plot_res(res_wave, min_cb =0.01, max_cb =8, c_map = P_VAR[var[0]] , lab_dict =labs[var[0]])

    plt.savefig(config['figPath']+'/Ms_{}.pdf'.format(var), bbox_inches='tight')



