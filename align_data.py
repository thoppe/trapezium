import numpy as np
import h5py
from scipy.ndimage.filters import gaussian_filter as gf
from scipy.interpolate import interp1d
from scipy.signal import correlate
import seaborn as sns
import pylab as plt
import itertools
sns.set_style('white')

device_idx = '2'

f_save = 'data_processed/walking_collection.h5'
data = {}
tn = 1000
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
            y1 = data[i][key](time-offset[i]*dt)
            y2 = data[j][key](time-offset[j]*dt)
            
            c  = np.correlate(y2, y1, 'full')
            idx = c.argmax()
            shift_val[j] = idx - tn
            shift_weight[j] = c[idx]
            #print i,j, idx - tn, c[idx]

        if shift_weight.sum()==0:
            shift_weight += 1

        shift[i] = np.average(shift_val, weights=shift_weight)
        #print i, key, shift[i]
    return shift

def compute_loss(shift):
    loss = 0.0
    for key in directions:
        for i,j in itertools.combinations(data, r=2):
            
            y1 = data[i][key](time-shift[i]*dt)
            y2 = data[j][key](time-shift[j]*dt)
            loss += ((y1-y2)**2).sum()
    print "LOSS", loss
    return loss

directions = ['ax','ay','az']
shift = np.median([find_average_shift(data, k) for k in directions],axis=0)
print compute_loss(shift)
print shift*dt


name = 'az'
x = np.array([time,]*len(data)).ravel()
y = np.array([data[i][name](time - dt*shift[i]) for i in data]).ravel()
idx = (x<0) | (y==0)
x = x[~idx]
y = y[~idx]

x = x.reshape(-1,1)
y = y.reshape(-1,1)

#N = 12
#x = np.random.rand(N,1)
#y = np.sin(12*x) + 0.66*np.cos(25*x) + np.random.randn(N,1)*0.1 + 3

import GPflow
k = GPflow.kernels.Matern52(1, lengthscales=0.3)
m = GPflow.gpr.GPR(x, y, kern=k)
m.likelihood.variance = 0.01
mean,var = m.predict_y(time[:,None])
plt.plot(time[:,None], mean)
plt.fill_between(time[:,None][:,0],
                 mean[:,0] - 2*np.sqrt(var[:,0]),
                 mean[:,0] + 2*np.sqrt(var[:,0]), color='blue', alpha=0.15)

plt.scatter(x,y,color='k',s=1,alpha=0.15)
plt.show()

print x.shape,y.shape
exit()


'''
from scipy.optimize import minimize
sol = minimize(compute_loss, shift, method='L-BFGS-B',
               options={"maxiter":10})
shift = sol.x

print shift*dt
print compute_loss(shift)
'''

color_keys = {'ax':'r','ay':'g','az':'b'}

for i in data:
    for name in color_keys:
        label = name if i==0 else None

        x = time - dt*shift[i]
        y = data[i][name](x)        

        y[x<0] = None
        y[y==0] = None
        
        plt.plot(time, y,
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

