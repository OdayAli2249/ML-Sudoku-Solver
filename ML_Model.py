# macine learning model
import keras
new_model = keras.Sequential([
    keras.layers.Flatten(input_shape=(10, 20)),
    keras.layers.Dense(10, activation='relu'),
    keras.layers.Dense(9,activation='softmax')
])

new_modelV2 = keras.Sequential([
    keras.layers.Flatten(input_shape=(121, 441)),
    keras.layers.Dense(10, activation='relu'),
    keras.layers.Dense(9,activation='softmax')
])


new_model.load_weights('Resources/model/ocr_digits.h5')
new_modelV2.load_weights('Resources/model/hog_features_classifier.h5')

