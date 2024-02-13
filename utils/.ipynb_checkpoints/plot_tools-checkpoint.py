import matplotlib.pyplot as plt
import numpy as np


from utils.labs import *

lab_age=labs['age_group7']
plt.rcParams.update({'font.size': 11, 'font.style': 'normal', 'font.family':'serif', 'figure.facecolor':'white'})

def plot_res(res, min_cb, max_cb,c_map,  lab_dict =None):
    cols, rows =len(res.keys()),1
    fig,axs = plt.subplots(rows,cols,figsize = (2.5*cols,2.5*rows), sharex = True)  
    
    axs[0].set_ylabel("age class $j$")
    
    for ik,key in enumerate(sorted(res.keys())):
        ax = axs[ik]       
        ax.axvline(x = 1.5, color = 'grey', ls = '--',lw = 1.9, alpha = 0.7)
        key_l = float(key.split('-')[-1])
        
        
        if lab_dict!= None:
            ax.set_title(lab_dict[key_l], fontsize = 11)
        else:
            ax.set_title('\n'.join(key.split('*')))
                
        ax.set_xlabel("age class $i$")
        
        cb1 = ax.imshow(np.array(res[key]['M']).T,cmap=c_map, vmin = min_cb , vmax = max_cb)
        
        if ik == cols-1:
            b = ax.get_position()
            cax = fig.add_axes([b.x1+0.02, b.y0, .009, b.y1-b.y0])
            fig.colorbar(cb1,orientation='vertical', cax=cax)
    
        for i in range(1):
            ax.invert_yaxis()
            ax.set_xticks(range(7))
            ax.set_xticklabels([lab_age[i] for i in range(7)], fontsize= 9, rotation = 270)
            ax.set_yticks(range(7))
            ax.set_yticklabels(['' for i in range(7)], fontsize= 9)
        axs[0].set_yticklabels([lab_age[i] for i in range(7)], fontsize= 9)
