from Model.test_binary_model import load_model, test_model
import threading
import asyncio
import keras
import concurrent.futures
class ModelHandler:
    
    def __init__(self):
        self.modelPath = "Model/Models/iau_phrase 99/model.h5"
        self.audioPath = "Audio/105-iau.wav"
        self.isModelLoaded = False
        self.model = None
        
    def loadModel(self):
        print("Start loading model ")
        print(f"Model Path : {self.modelPath}")
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(keras.models.load_model, self.modelPath)
            self.model = future.result()

        self.isModelLoaded = True
        print("Keras model loaded successfully!")
        
    def modelPredict(self, sessionDto):     
        if not self.isModelLoaded:
            print("Error: Model not loaded!")
            return
        
        # Perform prediction using the loaded model
        print(f"Start prediction session ID : {sessionDto.id}")
        print(self.model)
        if sessionDto.phrase != "":
            self.audioPath = sessionDto.audio_path + str(sessionDto.id) +"-iau.wav"
        else:
            self.audioPath = sessionDto.audio_path + str(sessionDto.id) +"-phrase.wav"

        result = test_model(self.model, self.audioPath)
        print(f"Result is: {result}")
        return result
