from numpy import *
from scipy.io import wavfile

from util import *
 
 
POSS_FREQS = [54.999999999999915, 61.73541265701542, 69.29565774421793, 73.4161919793518, 82.40688922821738, 92.4986056779085, 103.82617439498618, 109.99999999999989, 123.4708253140309, 138.59131548843592, 146.83238395870364, 164.81377845643485, 184.9972113558171, 207.65234878997245, 219.9999999999999, 246.94165062806198, 277.182630976872, 293.66476791740746, 329.62755691286986, 369.99442271163434, 415.3046975799451, 440.0, 493.8833012561241, 554.3652619537443, 587.3295358348153, 659.2551138257401, 739.988845423269, 830.6093951598907, 880.0000000000003, 987.7666025122488, 1108.7305239074892, 1174.659071669631, 1318.5102276514808, 1479.977690846539, 1661.218790319782, 1760.000000000002, 1975.5332050244986, 2217.4610478149793, 2349.3181433392633, 2637.020455302963, 2959.9553816930793, 3322.437580639566, 3520.0000000000055]

FUND = 131

def pitchshifter(sigin,sigout,deltime, tones, fund_tone=131.):
    size = deltime       # delay time in samples
    delay = zeros(size) # delay line
    env = bartlett(size)   # fade envelope table
    tap1 = 0            # tap positions
    tap2 = size/2
    wp = 0              # write pos
        
    
    for i in range(0, len(sigin)):
        delay[wp] = sigin[i]   # fill the delay line
            

        # first tap, linear interp readout
        frac = tap1 - int(tap1)
        if tap1 < size - 1 : delaynext = delay[tap1+1]
        else: delaynext = delay[0]
        sig1  =  delay[int(tap1)] + frac*(delaynext - delay[int(tap1)])

        # second tap, linear interp readout
        frac = tap2 - int(tap2)
        if tap2 < size - 1 : delaynext = delay[tap2+1]
        else: delaynext = delay[0]
        sig2  =  delay[int(tap2)] + frac*(delaynext - delay[int(tap2)])

        # fade envelope positions
        ep1 = tap1 - wp
        if ep1 < 0: ep1 += size
        ep2 = tap2 - wp
        if ep2 <  0: ep2 += size

        # combine tap signals
        sigout[i] = env[ep1]*sig1 + env[ep2]*sig2

        # increment tap pos according to pitch transposition
        # pitch = 2.**(tones[i]/12.)
        pitch = tones[i]/fund_tone
           
        tap1 += pitch
        tap2 = tap1 + size/2

        # keep tap pos within the delay memory bounds
        while tap1 >= size: tap1 -= size
        while tap1 < 0: tap1 += size

        while tap2 >= size: tap2 -= size
        while tap2 < 0: tap2 += size

        # increment write pos
        wp += 1
        if wp == size: wp = 0
 
    return sigout



def get_f0(signal, dtime, min_freq=131/2., max_freq=131*1.5):
    fourier = fft.fft(signal)
    frequencies = fft.fftfreq(len(signal), d=dtime)
    
    fourier = fourier[(frequencies < max_freq)]
    frequencies = frequencies[(frequencies < max_freq)]
    
    fourier = fourier[(frequencies > min_freq)]
    frequencies = frequencies[(frequencies > min_freq)]
        
    return frequencies[fourier.argmax()]
    
def get_f0_tones(signal, dtime, block_length, key=None, min_freq=131/2., max_freq=131*1.5):
    
    tones = zeros(signal.shape)
    
    for i in range(block_length, len(signal), block_length):
        
        current_tone = get_f0(signal[i-block_length:i], 1/44100., min_freq=min_freq, max_freq=max_freq)
        
        if key is not None:
            final_k = key[0]
            cur_dist = abs(final_k - current_tone)
            for k in key:
                if abs(k - current_tone) < cur_dist:
                    final_k = k
                    cur_dist = abs(k - current_tone)
            
            current_tone = final_k
            
        tones[i-block_length:i] = tile(current_tone, block_length)
       
    return tones


def harmonize_wav_file(filename, poss_freqs=POSS_FREQS):

    nfo("Harmonizing")
    (sr,signalin) = wavfile.read(filename)
    nfo("Wav file read")
    if signalin.shape[1] > 1:
        signalin = (signalin[:, 1] + signalin[:, 0]) / 2

    fund = FUND
    signalout = zeros(len(signalin))
    dsize = int(sr/(fund*0.5))

    # tones = np.array([floor(float(i)/len(signalin)*24.)+1 for i in range(len(signalin))])
    # tones = np.array([1 + ((i * 10 / len(signalin)) % 3) * 7 for i in range(len(signalin))])

    nfo("Fetching F0s")
    f0_tones = get_f0_tones(signalin, 1/44100., 22050, min_freq=54, max_freq=220, key=poss_freqs)
    nfo("Fetched F0s")

    nfo("Shift pitches")
    signalout = pitchshifter(signalin,signalout,dsize, f0_tones)

    nfo("Store file")

    wavfile.write('%s_harm.wav' % filename.replace(".wav",""),sr,array(signalout, dtype='int16'))

    nfo("Done",True)