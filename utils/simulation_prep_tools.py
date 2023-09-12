import numpy as np
import pandas as pd

from utils.epi_tools import  SUM_C, SUM_C_lev

def des_by_lev(all_RES, C, level):
    new_Ci = list(map(lambda x: SUM_C_lev(x, C, level), all_RES))
    levs = new_Ci[0].keys()

    res={}
    for lev in levs:
        res[lev] = {}
        list_lev = list(map(lambda x: x[lev], new_Ci))

        res[lev]['median'] = np.median(list_lev, axis =0)
        res[lev]['p50'] = np.percentile(list_lev,50, axis =0)
        res[lev]['p25'] = np.percentile(list_lev,25, axis =0)
        res[lev]['p75'] = np.percentile(list_lev,75, axis =0)
        
    return res

def des_overall(all_RES, C):
    res = {}
    new_Ci = list(map(lambda x: SUM_C(x, C), all_RES))
    res['median'] = np.median(new_Ci, axis =0)
    res['p25'] = np.percentile(new_Ci,25, axis =0)
    res['p75'] = np.percentile(new_Ci,75, axis =0)
    return res



def SUM_C_key(RES, C):
    keys = list(RES['S'][0].keys())
    SUM_key_lists = [[] for k in  range(len(keys))]
    for c_ in RES[C]:
        res_c = pd.DataFrame(c_).T
        res_c.loc[(slice(None), 6),:]=res_c.loc[(slice(None), 6),:].values+res_c.loc[(slice(None), 7),:].values
        res_c = res_c.loc[(slice(None), [i for i in range(7)]),:]
        res_c = res_c.T
        
        for key,SUM_list in zip(res_c.columns,SUM_key_lists):
            SUM_list.append(res_c[key].values)
    return {key: sum(SUM_list) for key,SUM_list in zip(res_c.columns,SUM_key_lists)}


def des_by_key(all_RES, C):
    new_Ci = list(map(lambda x: SUM_C_key(x, C), all_RES))
    levs = new_Ci[0].keys()

    res={}
    for lev in levs:
        res[lev] = {}
        list_lev = list(map(lambda x: x[lev], new_Ci))

        res[lev]['median'] = np.median(list_lev, axis =0)
        res[lev]['p50'] = np.percentile(list_lev,50, axis =0)
        res[lev]['p25'] = np.percentile(list_lev,25, axis =0)
        res[lev]['p75'] = np.percentile(list_lev,75, axis =0)
        
    return res



