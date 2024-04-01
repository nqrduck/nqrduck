"""Helper used for signal processing."""
import logging
from scipy.fft import fft, fftfreq, fftshift
import numpy as np
import sympy

logger = logging.getLogger(__name__)

class SignalProcessing:
    """This class provides various signal processing methods that can then be used by nqrduck modules."""

    @classmethod
    def fft(cls, tdx : np.array, tdy: np.array, freq_shift : float = 0, zero_padding = 1000) -> tuple[np.array, np.array]:
        """This method calculates the FFT of the time domain data.
        
        Args:
            tdx (np.array): Time domain x data in seconds.
            tdy (np.array): Time domain magnitude y data.
            freq_shift (float): Frequency shift in MHz - this can be useful if the spectrometer has it's frequency data in the IF band.
            zero_padding (float): Zero padding to be used in the FFT.
        
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

        return xdf, ydf
    
    @classmethod
    def baseline_correction(cls, fdx : np.array, fdy : np.array, order : int) -> np.array:
        """This method calculates the baseline correction of the frequency domain data.
        
        Args:
            fdx (np.array): Frequency domain x data in MHz.
            fdy (np.array): Frequency domain magnitude y data.
            order (int): Order of the polynomial used for baseline correction.
        
        Returns:
            np.array: Frequency domain magnitude y data with baseline correction.
        """
        pass
    
    @classmethod
    def apodization(cls, tdx : np.array, tdy : np.array, apodization_function : sympy.Expr) -> np.array:
        """This method calculates the apodization of the time domain data.
        
        Args:
            tdx (np.array): Time domain x data in seconds.
            tdy (np.array): Time domain magnitude y data.
            apodization_function (sympy.Expr): Apodization function.
        
        Returns:
            np.array: Time domain magnitude y data with apodization.
        """
        weight = np.array([apodization_function.subs("t", t) for t in tdx])
        return tdy * weight
    
    @classmethod
    def peak_picking(cls, fdx: np.array, fdy: np.array, threshold : float = 0.05) -> tuple[np.array, np.array]:
        """This method calculates the peak picking of the frequency domain data.
        
        Args:
            fdx (np.array): Frequency domain x data in MHz.
            fdy (np.array): Frequency domain magnitude y data.
            threshold (float): Threshold for peak picking.
        
        Returns:
            list: x,y data of the peaks.
        """
        pass
