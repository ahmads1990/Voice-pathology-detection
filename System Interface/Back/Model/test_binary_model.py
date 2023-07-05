import keras
from Model.preprocessing import *
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

#path = "./Model/Models/iau_phrase 99/model.h5"

# todo
def load_model(path):
    model = keras.models.load_model(path)
    print("#### Loaded Model")
    #print(model)
    
    return model

def prepare_input(audio_path):
    y, sr = librosa.load(audio_path, duration=1)
    input_test = (extract_mell_spectogram(concatenate_and_apply_fft(framing_signal(y))))

    input_test = np.repeat(input_test[..., np.newaxis], 1, -1)
    return input_test

def test_model(model,audio_path):
    input_test = prepare_input(audio_path)

    list_test = []
    list_test.append(input_test)
    list_test = np.array(list_test)
    list_test.shape

    y_pred = model.predict(list_test)
    y_pred = np.where(y_pred < 0.5, 0, 1)

    print(y_pred)

    if (y_pred[0] == 1):
        return "pathology"
    else:
        return "Healthy"

