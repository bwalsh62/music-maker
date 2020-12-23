#%% Import libraries

from pygame import mixer

from wav_util import wav_write, wav_zpad

#%% Second take Song class

class Song:
        def __init__(self, note_list=['C', 'E', 'G'], note_start_list=[0, 0, 1], duration_list=[1,1,1], bpm=60):

            """Method for initializing a Melody object

            Args: 
                note_list (list of strings)
                note_start_list (list of integers)
                duration_list (list of integers)

            Attributes:
                note_list (list of strings): list of notes of a Song object
                note_start_list (list of integers): list of note index starts in beats
                duration_list (list of integers): list of note lengths in beats
                bpm (integer): integer beats per minute
                _file_name (string): Path to wav file once created
            """

            self.note_list = note_list # list of note names
            self.note_start_list = note_start_list # list of note starts in beats
            self.duration_list = duration_list # list of note durations in beats
            self.song_length = np.max(np.array(duration_list) + np.array(note_start_list)) # length of song in beats

            self._file_name = False # path to wav file

            # Method to create .wav file from melody
            def create_wav_file(self, file_name='./song.wav'):
                """Create .wav file based on .note_list 

                Args:
                file_name: string. The name of the output .wav file
                
                Returns: 
                wav_file_path: string. The file path to the new .wav file
                """
                
                for index, note in enumerate(self.note_list):

                    # Make initial wav file
                    wav_base = wav_write(note)
                    # Pad the note
                    padded_note = wav_zpad(wav_base, pad_time=note_start_list[index], pre_pad=True, wav_file_out=file_name)
                    # pre-pad = note_start_list[index]
                    # post-pad = self.song_length - note_start_list[index] - note_duration_list[index]

                    self._file_name = file_name

        return file_name

#%% Initial melody class

class Melody:
#class Melody(Note):
    def __init__(self, note_list=['C', 'G'], duration_list=[1, 1]):
        
        """Method for initializing a Melody object

        Args: 
            note_list (list of strings)
            duration_list (list of integers)

        Attributes:
            note_list (list of strings): list of notes of a Melody object
            duration_list (list of integers): list of note durations of a Melody object
            _file_name (string): Path to wav file once created
        """

        self.note_list = note_list # list of note names
        self.duration_list = duration_list # list of note durations in seconds

        #for note in self.note_list:
        #    Note.__init__(self, note, duration)
        self._file_name = False # path to wav file

    # Method to create .wav file from melody
    def create_wav_file(self, file_name='./melody.wav'):
        """Create .wav file based on .note_list 

        Args:
        file_name: string. The name of the output .wav file
        
        Returns: 
        wav_file_path: string. The file path to the new .wav file
        """
        
        for index, note in enumerate(self.note_list):
            # Initialize melody wav file with first note, otherwise append
            wav_write(note, file_name, append=index > 0)
            # note.create_wav_file(file_name, append=index>0)

            self._file_name = file_name

        return file_name

    def play(self):
        mixer.Sound(self._file_name).play(loops=0)