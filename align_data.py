import numpy as np
import h5py
from scipy.ndimage.filters import gaussian_filter as gf
from scipy.interpolate import interp1d
from scipy.signal import correlate
import seaborn as sns
import pylab as plt
import itertools
sns.set_style('white')

device_idx = '3'

f_save = 'data_processed/walking_collection.h5'
data = {}
tn = 2000
time = np.linspace(0,1.2,tn)
dt = time[1]-time[0]

directions = ['ax','ay','az']

with h5py.File(f_save) as h5:
    g = h5[device_idx]
    for i in g:
        t = g[i]['t'][:]
        data[int(i)] = {'t':time}

        for key in directions:
            x = g[i][key][:]
            f = interp1d(t, x, fill_value=0.0, bounds_error=False)
            data[int(i)][key] = f


def find_average_shift(data, key, offset=None):

    N = len(data)

    if offset is None:
        offset = np.zeros(N)

    shift = np.zeros(N)
        
    for i in data:

        shift_val = np.zeros(N)
        shift_weight = np.zeros(N)
        for j in data:
            if i == j: continue
            x1 = data[i][key](time+offset[i]*dt)
            x2 = data[j][key](time+offset[j]*dt)
            
            c  = np.correlate(x2, x1, 'full')
            idx = c.argmax()
            shift_val[j] = idx - tn
            shift_weight[j] = c[idx]
            #print i,j, idx - tn, c[idx]

        if shift_weight.sum()==0:
            shift_weight += 1

        shift[i] = int(np.average(shift_val, weights=shift_weight))
        #print i, key, shift[i]
    return shift


shift = np.median([find_average_shift(data, k) for k in directions],axis=0)

#for _ in range(5):
#    shift = np.median([find_average_shift(data, k, shift) for k in directions],axis=0)
#    print np.abs(shift).sum(), shift
print shift

color_keys = {'ax':'r','ay':'g','az':'b'}

for i in data:
    for name in color_keys:
        label = name if i==0 else None

        x = time - dt*shift[i]
        y = data[i][name](x)
        

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
plt.savefig("figures/walking_steps_segmented_dev_{}.png".format(device_idx))
plt.show()

