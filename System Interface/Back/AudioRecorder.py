import time
import pyaudio
import wave

class Recorder:
    def __init__(self):
        self.is_recording = False
        self.frames = []
        self.sample_rate = 50000  # Sample rate
        self.chunk = 1024  # Record in chunks of 1024 samples
        self.sample_format = pyaudio.paInt16  # 16 bits per sample
        self.channels = 1
        self.current_record_length = 0
        self.max_record_length = 30  # Maximum recording length in seconds
        self.max_seconds = self.max_record_length %60
        self.max_minutes = self.max_record_length //60 
        self.path = 'Audio/'

    def start_recording(self, recordPath, label, sliderHandler):
        """
        Starts recording audio from the default input device and saves it to a WAV file.
        
        Args:
            path (str): The path where the output file will be saved.
        """
        self.is_recording = True
        self.recordPath = recordPath
        self.frames = []
        
        # Create an interface to PortAudio
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(
            format=self.sample_format,
            channels=self.channels,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=self.chunk)
        
        start = time.time()
        self.minutes =0
        self.seconds=0
        while self.is_recording:
            data = self.stream.read(self.chunk)
            self.frames.append(data)

            # Calcualte time elapsed from starting the record
            self.current_record_length = time.time() - start
            self.minutes =int(self.current_record_length//60)
            self.seconds= int(self.current_record_length%60)
            
            if(sliderHandler.value()< int(self.current_record_length)):
                sliderHandler.setValue(int(self.current_record_length))
                
            # construct media player bar progress
            labelTxt = str(self.minutes) + ":" + str(self.seconds).zfill(2) + \
            '/'+ str(self.max_minutes) + ":" + str(self.max_seconds).zfill(2)
            
            label.setText(labelTxt)
            # Check duration if bigger allowed stop the recording
            if self.current_record_length >= self.max_record_length:
                self.is_recording = False
                break
            
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
        
        # Save the recorded audio to a WAV file
        wf = wave.open("Audio/"+self.recordPath + ".wav", 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.audio.get_sample_size(self.sample_format))
        wf.setframerate(self.sample_rate)
        wf.writeframes(b''.join(self.frames))
        wf.close() 
        
        return
    
    def stop_recording(self):
        """Stops the current recording."""
        self.is_recording = False
