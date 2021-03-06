# -*- coding: utf-8 -*-
"""Transfer_Learning_Vgg.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1bTDdAOOi2DxjMz6Pue0cjHDIxpd-QtsQ

Importing the  required modules
"""

!pip install keras.utils

from google.colab import drive
drive.mount('/drive')
root = '/drive/My Drive/Colab Notebooks/101_ObjectCategories'

from google.colab import drive
drive.mount('/content/drive')

root = '/drive/My Drive/101_ObjectCategories'



import os

import random
import numpy as np
import keras

import matplotlib.pyplot as plt
from matplotlib.pyplot import imshow

import tensorflow

from tensorflow.keras.utils import to_categorical
from sklearn.metrics import f1_score,plot_roc_curve

from keras.preprocessing import image
from keras.applications import vgg16
from keras.applications.imagenet_utils import preprocess_input
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Activation
from keras.layers import Conv2D, MaxPooling2D
from keras.models import Model

import os

"""Importing Caltech10 dataset"""

# Unzipping the dataset
import shutil
shutil.unpack_archive("/content/101_ObjectCategories.tar.gz","/content/sample_data/101_ObjectCategories")

# Reading the contents

root = '/content/data/101_ObjectCategories' #specify the path to the root folder
exclude = ['BACKGROUND_Google', 'Motorbikes', 'airplanes', 'Faces_easy', 'Faces']
include = ['beaver','bass','cannon','emu','kangaroo','lotus','snoopy','starfish','revolver','wrench']
train_split, val_split = 0.7, 0.15

categories = [x[0] for x in os.walk(root) if x[0]][1:]
categories = [c for c in categories if c  not in [os.path.join(root, e) for e in exclude]]


print(categories)

# Getting the images

def get_image(path):
    img = image.load_img(path, target_size=(224, 224))
   # print(img)
    x = image.img_to_array(img)
  #  x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    return x

data = []
image_type = ('.jpg', '.jpeg', '.png', '.ppm', '.bmp', '.pgm', '.tif', '.tiff', '.webp')

def get_data(category):
    data = []
    for c, category in enumerate(category):
        images = [os.path.join(dp, f) for dp, dn, filenames 
                in os.walk(category) for f in filenames 
                if os.path.splitext(f)[1].lower() in image_type]
    for img_path in images:
            img, x = get_image(img_path)
            data.append({'x':np.array(x[0]), 'y':c})

# count the number of classes
num_classes = len(categories)
print(num_classes)

#Shuffling the data
data = get_data(categories)
random.shuffle(data)

#Splitting into train,test and validation
idx_val = int(train_split * len(data))
idx_test = int((train_split + val_split) * len(data))
train = data[:idx_val]
val = data[idx_val:idx_test]
test = data[idx_test:]

print(train)

x_train, y_train = np.array([t["x"] for t in train]), [t["y"] for t in train]
x_val, y_val = np.array([t["x"] for t in val]), [t["y"] for t in val]
x_test, y_test = np.array([t["x"] for t in test]), [t["y"] for t in test]
print(y_test)

# normalize data
x_train = x_train.astype('float32') / 255.
x_val = x_val.astype('float32') / 255.
x_test = x_test.astype('float32') / 255.

# convert labels to one-hot vectors
y_train = tensorflow.keras.utils.to_categorical(y_train, num_classes)
y_val = tensorflow.keras.utils.to_categorical(y_val, num_classes)
y_test = tensorflow.keras.utils.to_categorical(y_test, num_classes)
print(y_test.shape)

categories_10 = [c for c in categories if c   in [os.path.join(root, i) for i in include]]

num_classes_10 = len(categories_10)
data = get_data(categories_10)
random.shuffle(data)

idx_val = int(train_split_10 * len(data))
idx_test = int((train_split_10 + val_split_10) * len(data))
train_10 = data[:idx_val]
val_10 = data[idx_val:idx_test]
test_10 = data[idx_test:]

x_train_10, y_train_10 = np.array([t["x"] for t in train_10]), [t["y"] for t in train_10]
x_val_10, y_val_10 =     np.array([t["x"] for t in val_10]), [t["y"] for t in val_10]
x_test_10, y_test_10 =   np.array([t["x"] for t in test_10]), [t["y"] for t in test_10]

# normalize data
x_train_10 = x_train_10.astype('float32') / 255.
x_val_10 = x_val_10.astype('float32') / 255.
x_test_10 = x_test_10.astype('float32') / 255.

# convert labels to one-hot vectors
y_train_10 = keras.utils.np_utils.to_categorical(y_train_10, num_classes_10)
y_val_10 = keras.utils.np_utils.to_categorical(y_val_10, num_classes_10)
y_test_10 = keras.utils.np_utils.to_categorical(y_test_10, num_classes_10)
print(y_test_vector_10.shape)

# summary
print("finished loading %d images from %d categories"%(len(data), num_classes))
print("train / validation / test split: %d, %d, %d"%(len(x_train), len(x_val), len(x_test)))
print("training data shape: ", x_train.shape)
print("training labels shape: ", y_train.shape)
print("validation data shape:",x_val.shape)

images = [os.path.join(dp, f) for dp, dn, filenames in os.walk(root) for f in filenames if os.path.splitext(f)[1].lower() in ['.jpg','.png','.jpeg']]
idx = [int(len(images) * random.random()) for i in range(8)]
imgs = [image.load_img(images[i], target_size=(224, 224)) for i in idx]
concat_image = np.concatenate([np.asarray(img) for img in imgs], axis=1)
plt.figure(figsize=(16,4))

plt.imshow(concat_image)



# build the network

#x_train.reshape(x_train.shape[0],224,224,3)
Input_shape=(224,224,3)
model = Sequential()
#print("Input dimensions: ",Input_shape)

model.add(Conv2D(32, (3, 3), input_shape=x_train.shape[1:]))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(32, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Dropout(0.25))

model.add(Conv2D(32, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(32, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(256))
model.add(Activation('relu'))

model.add(Dropout(0.5))

model.add(Dense(num_classes))
model.add(Activation('softmax'))

model.summary()

# compile the model to use categorical cross-entropy loss function and adadelta optimizer
model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

history = model.fit(x_train, y_train,
                    batch_size=128,
                    epochs=10,
                    validation_data=(x_val, y_val))

fig = plt.figure(figsize=(16,4))
ax = fig.add_subplot(121)
ax.plot(history.history["val_loss"])
ax.set_title("validation loss")
ax.set_xlabel("epochs")

ax2 = fig.add_subplot(122)
ax2.plot(history.history["val_accuracy"])
ax2.set_title("validation accuracy")
ax2.set_xlabel("epochs")
ax2.set_ylim(0, 1)

loss, accuracy = model.evaluate(x_test, y_test, verbose=0)
print('Test loss:', loss)
print('Test accuracy:', accuracy)

#downloading vgg16
vgg = keras.applications.vgg16.VGG16(weights='imagenet', include_top=True,input_tensor=None,
    input_shape=None,
    pooling=None,
    classes=1000,
    classifier_activation="softmax",)
vgg.summary()

# make a reference to VGG's input layer
inp = vgg.input

def model_create(last,count_of_classes):

    # make a new softmax layer with num_classes neurons
    new_classification_layer = Dense(count_of_classes, activation='softmax')

    # connect our new layer to the second to last layer in VGG, and make a reference to it
    out = new_classification_layer(vgg.layers[-2].output)

    # create a new network between inp and out
    model_new = Model(inp, out)

    # make all layers untrainable by freezing weights (except for last layer)
    for l, layer in enumerate(model_new.layers[:-1]):
        layer.trainable = False

    # ensure the last layer is trainable/not frozen
    for l, layer in enumerate(model_new.layers[-1:]):
        layer.trainable = True

    model_new.compile(loss='categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])

    model_new.summary()

fpr_list = []
tpr_list = []
precision_list = []
recall_list = []

def predict_model(model_tmp):
    y_pred = model_tmp.predict(x_test_10)

    y_pred_classes = []
    y_prob = []
    y = []
    for i in range(len(y_test_10)):
        predicted = y_pred[i]
        actual = y_test_10[i]
       
        max_prob_index = np.argmax(predicted)
        y_pred_classes.append(max_prob_index)
        y_prob.append(predicted[max_prob_index])
        if max_prob_index == actual:
            y.append(1)
        else:
            y.append(0)

    print("Classification Report for selected Category: \n", classification_report(y_test_10, y_pred_classes))
    fpr, tpr, thresholds = roc_curve(y, y_prob)
    fpr_list.append(fpr)
    tpr_list.append(tpr)
    precision, recall, thresholds = precision_recall_curve(y, y_prob)
    precision_list.append(precision)
    recall_list.append(recall)

# make all layers untrainable by freezing weights (except for  last two layers)
for l, layer in enumerate(model_new.layers[:-2]):
    layer.trainable = False

# ensure the last layer is trainable/not frozen
for l, layer in enumerate(model_new.layers[-2:]):
    layer.trainable = True

model_new.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

model_new.summary()

#make all layers untrainable by freezing weights (except for  last three layers)
for l, layer in enumerate(model_new.layers[:-3]):
    layer.trainable = False

# ensure the last layer is trainable/not frozen
for l, layer in enumerate(model_new.layers[-3:]):
    layer.trainable = True

model_new.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

model_new.summary()

#Freezing all layers except last layer for 101 classes
model_new = model_create(-1, num_classes)

history_1 = model_new.fit(x_train, y_train,
                         batch_size=128, 
                         epochs=5, 
                         validation_data=(x_val, y_val))

loss, accuracy = model_new.evaluate(x_test, y_test, verbose=0)

print(' loss Model 1 for 101     :', loss)
print('accuracy Model 1 for 101 :', accuracy)

#Freezing all layers except last layer for 10 classes

model_new = model_create(-1, num_classes_10)

model_new.fit(x_train_10, y_train_10, 
                         batch_size=128, 
                         epochs=5, 
                         validation_data=(x_val_10, y_val_10))

loss, accuracy = model_new.evaluate(x_test_10, y_test_10, verbose=0)

print(' loss Model 1 for 10     :', loss)
print(' accuracy Model 1 for 10 :', accuracy)



predict_model(model_new)

#Freezing all layers except last two layers for 101 classes

model_1 = model_create(-2, num_classes)

history_1 = model_1.fit(x_train, y_train,
                         batch_size=128, 
                         epochs=5, 
                         validation_data=(x_val, y_val))

loss, accuracy = model_1.evaluate(x_test, y_test, verbose=0)

print(' loss Model 1 for 101     :', loss)
print('accuracy Model 1 for 101 :', accuracy)

#Freezing all layers except last two  layers for 10 classes


model_1 = model_create(-2, num_classes_10)

model_1.fit(x_train_10, y_train_10, 
                         batch_size=128, 
                         epochs=5, 
                         validation_data=(x_val_10, y_val_10))

loss, accuracy = model_1.evaluate(x_test_10, y_test_10, verbose=0)


print('Overall loss Model 1 for 10     :', loss)
print('Overall accuracy Model 1 for 10 :', accuracy)

predict_model(model_1)

#Freezing all layers except last three layers for 101 classes

model_2 = model_create(-3, num_classes)

history_1 = model_2.fit(x_train, y_train,
                         batch_size=128, 
                         epochs=5, 
                         validation_data=(x_val, y_val))

loss, accuracy = model_2.evaluate(x_test, y_test, verbose=0)

print('loss Model 1 for 101     :', loss)
print('accuracy Model 1 for 101 :', accuracy)



#Freezing all layers except last threes layer for 10 classes

model_2 = model_create(-2, num_classes_10)

model_2.fit(x_train_10, y_train_10, 
                         batch_size=128, 
                         epochs=5, 
                         validation_data=(x_val_10, y_val_10))

loss, accuracy = model_2.evaluate(x_test_10, y_test_10, verbose=0)

print('loss Model 1 for 10     :', loss)
print('accuracy Model 1 for 10 :', accuracy)

predict_model(model_2)

# Question 2 :ReInitializing the last three layers and training the new model

from keras import initializers
inp = vgg.input


initializer = initializers.RandomNormal(mean=0., stddev=1.)
layer_fc1 = Dense(4096, kernel_initializer=initializer)

layer_fc2 = Dense(4096, kernel_initializer=initializer)

layer_predicition = Dense(97, kernel_initializer=initializer)

output1 = layer_fc1(vgg.layers[-4].output)
model_new = Model(inp, out)

output2 = layer_fc2(vgg.layers[-3].output)
model_new = Model(inp, out_1)


output3 = layer_predicition(vgg.layers[-2].output)
model_new = Model(inp, out_2)

for i in range(len(fpr_list)):
    plt.plot(fpr_list[i], tpr_list[i], marker='.', label='Model-'+str(i+1))
# axis labels
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
# show the legend
plt.legend()
# show the plot
plt.show()

for i in range(len(precision_list)):
    plt.plot(precision_list[i], recall_list[i], marker='.', label='Model-'+str(i+1))
# axis labels
plt.xlabel('Precision')
plt.ylabel('Recall')
# show the legend
plt.legend()
# show the plot
plt.show()