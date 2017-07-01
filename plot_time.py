import pandas as pd
import numpy as np

f_csv = "data_collection/travis_walking_indoor_test5.dat"
cols = {
    0:'device',
    1:'timestamp',
    2:'ax',
    3:'ay',
    4:'az',
    5:'gx',
    6:'gy',
    7:'gz',
}
df = pd.read_csv(
    f_csv,
    header = None,
    sep=' ',
).rename(columns=cols)
df.ax = (df.ax*2)/2**(15)
df.ay = (df.ay*2)/2**(15)
df.az = (df.az*2)/2**(15)

df.gx = (df.gx*2000)/2**(15)/(360.)
df.gy = (df.gy*2000)/2**(15)/(360.)
df.gz = (df.gz*2000)/2**(15)/(360.)


device_idx = df['device'].unique()
dev = dict(zip(*[device_idx,[df[df.device==x] for x in device_idx]]))


for i in dev:
    # timestamp looks broken ... use order instead
    #dev[i] = dev[i].sort_values('timestamp').set_index('timestamp')
    del dev[i]['timestamp']
    del dev[i]['device']

import seaborn as sns
import pylab as plt

start_time = 77.0
#end_time = 95.0
end_time = start_time+52.8

for idx in range(4):
    fig, axes = plt.subplots(2,3, figsize=(8,4), sharey='row', sharex='row')
    
    # Approx time delta for samples (this isn't quite correct)
    T = np.arange(0, len(dev[idx].ax), 1/400.)
    T = T[:len(dev[idx].ax)]
    
    axes[0][0].plot( T, dev[idx].ax )
    axes[0][1].plot( T, dev[idx].ay )
    axes[0][2].plot( T, dev[idx].az )
    
    axes[1][0].plot( T, dev[idx].gx )
    axes[1][1].plot( T, dev[idx].gy )
    axes[1][2].plot( T, dev[idx].gz )

    plt.suptitle("device {}".format(idx))
    
    axes[0][0].set_ylabel('ax (g/s)')
    axes[0][1].set_ylabel('ay (g/s)')
    axes[0][2].set_ylabel('az (g/s)')

    axes[1][0].set_ylabel('gx (rad/s)')
    axes[1][1].set_ylabel('gy (rad/s)')
    axes[1][2].set_ylabel('gz (rad/s)')

    if start_time is not None and end_time is not None:
        axes[0][0].set_xlim(start_time, end_time)
    
    plt.tight_layout()


plt.show()




