import logging
from scipy.fft import fft, fftfreq, fftshift
import numpy as np

logger = logging.getLogger(__name__)

class SignalProcessing():
    """ This class provides various signal processing methods that can then be used by nqrduck modules."""

    def __init__(self):
        pass

    @classmethod
    def fft(cls, tdx : np.array, tdy: np.array, freq_shift : float = 0, zero_padding = 1000) -> tuple[np.array, np.array]:
        """This method calculates the FFT of the time domain data.
        
        Args:
            tdx (np.array): Time domain x data in seconds.
            tdy (np.array): Time domain magnitude y data.
            freq_shift (float): Frequency shift in MHz - this can be useful if the spectrometer has it's frequency data in the IF band.
        
        Returns:
            np.array: Frequency domain x data in MHz.
            np.array: Frequency domain magnitude y data.
        """
        
        dwell_time = (tdx[1] - tdx[0])
            
        N = len(tdx) + zero_padding

        if freq_shift != 0:
            # Create the complex exponential to shift the frequency
            shift_signal = np.exp(-2j * np.pi * freq_shift * tdx)[:, np.newaxis]

            # Apply the shift by multiplying the time domain signal
            tdy_shift = np.abs(tdy * shift_signal)
            ydf = fftshift(fft(tdy_shift, N, axis=0), axes=0) 
        
        else:
            ydf = fftshift(fft(tdy, N, axis=0), axes=0)
        
        xdf = fftshift(fftfreq(N, dwell_time))

        return xdf, np.abs(ydf)