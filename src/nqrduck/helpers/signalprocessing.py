from scipy.fft import fft, fftfreq, fftshift
import numpy as np

class SignalProcessing():
    """ This class provides various signal processing methods that can then be used by nqrduck modules."""

    def __init__(self):
        pass

    @classmethod
    def fft(cls, tdx : np.array, tdy: np.array) -> tuple[np.array, np.array]:
        """This method calculates the FFT of the time domain data.
        
        Args:
            tdx (np.array): Time domain x data in seconds.
            tdy (np.array): Time domain magnitude y data.
        
        Returns:
            np.array: Frequency domain x data in MHz.
            np.array: Frequency domain magnitude y data.
        """
        
        dwell_time = (tdx[1] - tdx[0])
            
        N = len(tdx) 
        
        ydf = fftshift(fft(tdy, axis=0), axes=0)
        xdf = fftshift(fftfreq(N, dwell_time))
        
        return xdf, ydf