from tensorflow.python import keras

class LossHistory(keras.callbacks.Callback):
    """A class for keras to use to store training losses for the model to use:
       1. initialize a LossHistory object inside your agent
       2. and put callbacks= [self.lossHistory] in the model.fit() call
    """
    def __init__(self):
        self.losses = []

    def on_train_begin(self, logs={}):
        pass

    def on_batch_end(self, batch, logs={}):
        self.losses.append(logs.get('loss'))

    def losses_clear(self):
        self.losses = []