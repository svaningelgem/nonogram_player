from collections import Counter
from typing import Dict

from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D, Input
from keras_preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt
from keras.callbacks import EarlyStopping,ReduceLROnPlateau,ModelCheckpoint
import keras

from sklearn.utils import class_weight

from src.utils import scale_image_to_100x100

input_shape = (100, 100)
batch_size = 32
epochs = 100

datagen = ImageDataGenerator(
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    zoom_range=0.3,  # [0.7 -> 1.3]
    rescale=1./255,  # Convert 'large' RGB (255) to floats (1.0)

    validation_split=0.3,

    preprocessing_function=scale_image_to_100x100,
)

train_data = datagen.flow_from_directory(
    './images',
    target_size=input_shape,
    batch_size=batch_size,
    interpolation="lanczos",
    shuffle=True,
    subset='training',
)

validation_data = datagen.flow_from_directory(
    './images',
    target_size=input_shape,
    batch_size=batch_size,
    interpolation="lanczos",
    shuffle=True,
    subset='validation',
)


def get_class_weights(train) -> Dict[int, float]:
    itemCt = Counter(train.classes)
    maxCt = float(max(itemCt.values()))
    return {clsID: maxCt/numImg for clsID, numImg in itemCt.items()}


class StopTrainingIfEnoughAcc(keras.callbacks.Callback):
    # https://medium.com/analytics-vidhya/transfer-learning-using-inception-v3-for-image-classification-86700411251b
    def on_epoch_end(self, epoch, logs={}):
        # Available in logs: 'loss', 'accuracy', 'val_<same>'
        if logs['accuracy'] > 0.99:
            print(f"\nGot to accuracy '{logs.get('accuracy')*100:.2f}%'")
            self.model.stop_training = True


def do_fit(model, train, test, tgt, epochs=20_000):
    callbacks = [
        ReduceLROnPlateau(monitor='val_loss', patience=5, cooldown=3, rate=0.6, min_lr=1e-18, verbose=1),
        EarlyStopping(monitor='val_loss', patience=10, verbose=1),
        ModelCheckpoint(f'./{tgt}/epoch_{{epoch:03d}}-{{val_accuracy:.5f}}.hdf5', monitor='accuracy', initial_value_threshold=0.85, verbose=1, save_best_only=True, mode='max'),
        StopTrainingIfEnoughAcc(),
    ]

    hist = model.fit(
        train,
        validation_data=test,
        epochs=epochs,  # We do early stopping. So this will always stop before this point
        shuffle=True,
        callbacks=callbacks,
        verbose=1,
        class_weight=get_class_weights(train),
    )

    # print_history(hist)

    globals()[f'{tgt}_hist'] = hist

# **IMPORTANT** !!! We need to know the right class indexes otherwise we can't predict them right.
print('class_indices =', train_data.class_indices)


model = Sequential()
model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=input_shape + (3,)))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(train_data.num_classes, activation='softmax'))

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])


do_fit(model, train_data, validation_data, 'model1')
