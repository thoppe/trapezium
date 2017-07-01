import pandas as pd
import numpy as np
from scipy.ndimage.filters import gaussian_filter as gf
from scipy import signal


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
    del dev[i]['timestamp']
    del dev[i]['device']

import seaborn as sns
import pylab as plt
sns.set_style('white')

start_time = 81.5
end_time = 93.5
#end_time = start_time+52.8

for idx in range(4):
    idx = 2
    
    # Approx time delta for samples (this isn't quite correct)
    T = np.arange(0, len(dev[idx].ax), 1/400.)
    T = T[:len(dev[idx].ax)]

    time_idx = (T>=start_time) & (T<end_time)
    T = T[time_idx]

    ax = dev[idx].ax[time_idx]
    ay = dev[idx].ay[time_idx]
    az = dev[idx].az[time_idx]

    ax -= ax.mean()
    ay -= ay.mean()
    az -= az.mean()

    mag = ax**2 + ay**2 + ax**2
    mag = gf(mag,sigma=12.0)

    # Find the peaks
    peak_idx = signal.find_peaks_cwt(mag, T)

    # Cutoff up to the first peak
    print peak_idx
    x = T[peak_idx]
    y = mag[peak_idx]

    #T = T[peak_idx[0]:peak_idx[-1]]
    #mag = mag[peak_idx[0]:peak_idx[-1]]

    t,AX,AY,AZ = [],[],[],[]
    for i,j in zip(peak_idx, peak_idx[1:]):
        t.append(T[i:j])
        AX.append(ax[i:j])
        AY.append(ay[i:j])
        AZ.append(az[i:j])


    for y in AX:
        y = y.values
        y = gf(y,sigma=6.0)
        plt.plot(y, color='r',alpha=0.5)

    for y in AY:
        y = y.values
        y = gf(y,sigma=6.0)
        plt.plot(y, color='b',alpha=0.5)

    for y in AZ:
        y = y.values
        y = gf(y,sigma=6.0)
        plt.plot(y, color='g',alpha=0.5)
    plt.show()
    
    exit()
    
    print x
    print y
    plt.plot(T,mag)
    
    plt.scatter(x,y,color='r',alpha=0.8)
    plt.xlim(x.min(), x.max())
    
    plt.tight_layout()
    
    #plt.scatter(ay,az )
    #w = np.fft.fft(ax)
    #freqs = np.fft.fftfreq(len(w))
    #print w
    #print freqs
    #plt.plot(freqs, np.absolute(w))
    plt.show()
    
    exit()
    
    
    
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




