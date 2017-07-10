import pandas as pd
import numpy as np
import h5py
from scipy.ndimage.filters import gaussian_filter as gf
from scipy import signal
import seaborn as sns
import pylab as plt
sns.set_style('white')


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
    nrows=10**20,
).rename(columns=cols)
df.ax = (df.ax*2)/2**(15)
df.ay = (df.ay*2)/2**(15)
df.az = (df.az*2)/2**(15)

df.gx = (df.gx*2000)/2**(15)/(360.)
df.gy = (df.gy*2000)/2**(15)/(360.)
df.gz = (df.gz*2000)/2**(15)/(360.)

device_idx = df['device'].unique()

# Map each device to a dictionary
dev = dict(zip(*[device_idx,[df[df.device==x] for x in device_idx]]))

def detrend_ramped_time_series(T):
    max_clock_cycle = 2**32
    clock_threshold = 2**28
    dt = 1/(200.0*10**6)

    # Assumes data starts off at some time and when it reaches zero, resets
    idx = np.roll(np.ediff1d(T,0)>clock_threshold, 1)
    T -= np.cumsum(idx)*max_clock_cycle

    # Start data counting up
    T *= -1

    # Start time at 0
    T -= T[0]

    # Convert to seconds
    return dt*T

for i in dev:
    pd.options.mode.chained_assignment = None
    dev[i]['time'] = detrend_ramped_time_series(dev[i]['timestamp'].values)
    pd.options.mode.chained_assignment = 'warn'

    #dev[i].set_index('time',inplace=True)
    del dev[i]['timestamp']
    del dev[i]['device']


start_time = 81.5
end_time = 93.5
#end_time = start_time+52.8

f_save = 'data_processed/walking_collection.h5'
h5 = h5py.File(f_save,'w')

for idx in range(4):
    print "Plotting device", idx
    h5_g = h5.create_group(str(idx))

    df = dev[idx]
    time_idx = (df.time>=start_time) & (df.time<=end_time)
    df = dev[idx].copy()[time_idx]

    T = df.time[time_idx].values
    ax = df.ax[time_idx]
    ay = df.ay[time_idx]
    az = df.az[time_idx]

    #ax -= ax.mean()
    #ay -= ay.mean()
    #az -= az.mean()
    
    mag = (ax-ax.mean())**2 + (ay-ay.mean())**2 + (az-az.mean())**2
    mag = gf(mag,sigma=12.0)

    # Find the peaks
    peak_idx = signal.find_peaks_cwt(mag, T)

    # Cutoff up to the first peak
    print peak_idx
    x = T[peak_idx]
    y = mag[peak_idx]

    # Save the segmented data too
    color_keys = {'ax':'r','ay':'g','az':'b'}
        
    plt.figure()    
    for k,(i,j) in enumerate(zip(peak_idx, peak_idx[1:])):

        sample = h5_g.create_group(str(k))
        
        t = T[i:j]
        t -= t.min()
        
        for a,name in zip([ax,ay,az],color_keys):
            ag = gf(a[i:j], sigma=6.0)
            sample[name] = ag

            label=None
            if k==0: label=name
            
            plt.plot(t, ag,
                     label=label,
                     color=color_keys[name],
                     alpha=0.5)
            
        sample['t'] = t



    plt.xlabel('seconds')
    plt.ylabel('acceleration g/s')
    plt.legend()
    sns.despine()
    plt.tight_layout()
    #plt.show()

    continue

    '''
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
    
    
    
    axes[0][0].plot( T, df.ax )
    axes[0][1].plot( T, df.ay )
    axes[0][2].plot( T, df.az )
    
    axes[1][0].plot( T, df.gx )
    axes[1][1].plot( T, df.gy )
    axes[1][2].plot( T, df.gz )

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
    '''

plt.show()




