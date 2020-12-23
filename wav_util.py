#%% Import libraries

import wave
import numpy as np

#%% Define music file locations

MUSIC_FILES = { \
    'C': r"C:\Users\benja\OneDrive\Documents\Python\liloquy-git\piano-gui\music_files\piano\Piano.mf.C4_2p4s.wav",
    'G': r"C:\Users\benja\OneDrive\Documents\Python\liloquy-git\piano-gui\music_files\piano\Piano.mf.G4_2p4s.wav",
    'A': r"C:\Users\benja\OneDrive\Documents\Python\liloquy-git\piano-gui\music_files\piano\Piano.mf.A4_2p4s.wav",
    'F': r"C:\Users\benja\OneDrive\Documents\Python\liloquy-git\piano-gui\music_files\piano\Piano.mf.F4_2p4s.wav"}

#%% Function to write wav_file

def wav_write(note, file_name, append=False):
        
    # Open wav file to read
    wav_note = wave.open(MUSIC_FILES[note], 'r')

    # Get sampling rate
    fs = wav_note.getframerate() 
    # Get other parameters to replicate in new file
    n_channels = wav_note.getnchannels()
    samp_width = wav_note.getsampwidth()
    
    # Based on fs, get number of frames for input time length
    wav_note_n_frames = wav_note.getnframes()
        
    wav_note_data = wav_note.readframes(wav_note_n_frames)
    wav_note.close()
    
    if append is False:
        # Open new wav file
        new_wav_note = wave.open(file_name, 'wb')
        new_wav_note.setnframes(wav_note_n_frames)
        new_wav_note.setnchannels(n_channels)
        new_wav_note.setsampwidth(samp_width)
        new_wav_note.setframerate(fs)
        new_wav_note.writeframes(wav_note_data) 
        new_wav_note.close()

    elif append is True:
        # Read current wav file
        original_wav_note = wave.open(file_name, 'r')
        original_wav_n_frames = original_wav_note.getnframes()
        original_wav_data = original_wav_note.readframes(original_wav_n_frames)
        original_wav_note.close()

        # Open new wav file
        new_wav_note = wave.open(file_name, 'wb')
        new_wav_note.setnframes(wav_note_n_frames + original_wav_n_frames)
        new_wav_note.setnchannels(n_channels)
        new_wav_note.setsampwidth(samp_width)
        new_wav_note.setframerate(fs)
        new_wav_note.writeframes(original_wav_data + wav_note_data) 
        new_wav_note.close()
        
    return file_name

#%% Function to mix 2 wav files

def wav_mix(wav_file1, wav_file2, wav_mixed="./mix.wav"):
    wavs = [wave.open(fn) for fn in [wav_file1, wav_file2]]
    frames = [w.readframes(w.getnframes()) for w in wavs]
    # here's efficient numpy conversion of the raw byte buffers
    # '<i2' is a little-endian two-byte integer.
    samples = [np.frombuffer(f, dtype='<i2') for f in frames]
    samples = [samp.astype(np.float64) for samp in samples]
    # mix as much as possible up to the shorter file's length
    n = min(map(len, samples))
    print(type(samples[0]))
    print(samples[0].shape)
    mix = samples[0][:n] + samples[1][:n]
    print(type(mix))
    # Save the result
    mix_wav = wave.open(wav_mixed, 'w')
    mix_wav.setparams(wavs[0].getparams())
    # before saving, we want to convert back to '<i2' bytes:
    mix_wav.writeframes(mix.astype('<i2').tobytes())
    mix_wav.close()

    return wav_mixed

#%% Function to pad wav file with zeros
# Note - may have to double the pad length or account for 2 channels

def wav_zpad(wav_file_in, pad_time=1, pre_pad=True, wav_file_out="./zpadded.wav"):
    
    # Open file
    wav_in = wave.open(wav_file_in)
    
    # Read frames
    original_wav_data = wav_in.readframes(wav_in.getnframes()) 

    # Generate pre pad as array then convert to bytes 
    pad_data = np.zeros([wav_in.getframerate()*pad_time,]).astype('<i2').tobytes()
    pad_frames = len(pad_data)

    padded_wav = wave.open(wav_file_out, 'wb')
    padded_wav.setparams(wav_in.getparams())
    padded_wav.setnframes(pad_frames + wav_in.getnframes())
    padded_wav.writeframes(pad_data + original_wav_data) 
    padded_wav.close()

    return wav_file_out