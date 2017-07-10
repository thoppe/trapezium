import numpy as np
import h5py
from scipy.ndimage.filters import gaussian_filter as gf
from scipy.interpolate import interp1d
from scipy.signal import correlate
import seaborn as sns
import pylab as plt
import itertools
sns.set_style('white')

device_idx = '1'

f_save = 'data_processed/walking_collection.h5'
data = {}
tn = 2000
time = np.linspace(0,1.2,tn)
dt = time[1]-time[0]

with h5py.File(f_save) as h5:
    g = h5[device_idx]
    for i in g:
        t = g[i]['t'][:]
        data[int(i)] = {'t':time}

        for key in ['ax','ay','az']:
            x = g[i][key][:]
            f = interp1d(t, x, fill_value=0.0, bounds_error=False)
            data[int(i)][key] = f(time)

            
S = []
for i in data:

    shift_val = []
    shift_weight = []
    for j in data:
        if i == j: continue
        x1 = data[i]['ax']
        x2 = data[j]['ax']
        c  = np.correlate(x2, x1, 'full')
        idx = c.argmax()
        shift_val.append(idx - tn)
        shift_weight.append(c[idx])
        #print i,j, idx - tn, c[idx]

    shift = int(np.average(shift_val, weights=shift_weight))
    print i, shift
    S.append(shift)

color_keys = {'ax':'r','ay':'g','az':'b'}

for i in data:
    for name in color_keys:
        label = name if i==0 else None

        y = data[i][name]
        x = time+dt*S[i]

        y[x<0] = None
        y[y==0] = None
        
        plt.plot(x, y,
                 label=label,
                 color=color_keys[name],
                 alpha=0.45)

plt.xlabel('seconds')
plt.ylabel('acceleration g/s')
plt.legend()
sns.despine()
plt.tight_layout()
plt.show()
