import tensorflow as tf
from AlzheimerClassifier.utils.common import load_data, process_data
from AlzheimerClassifier.entity.config_entity import TrainingConfig
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau


class Training:
    def __init__(self, config=TrainingConfig):
        self.config = config

    def get_callbacks(self):
        callbacks = []

        # Use correct syntax for ModelCheckpoint
        checkpoint = ModelCheckpoint(
            filepath=self.config.model_path,
            verbose=1,
            monitor="val_accuracy",
            mode="max",
        )
        callbacks.append(checkpoint)

        # Import ReduceLROnPlateau if not imported earlier
        reduce_lr = ReduceLROnPlateau(
            monitor="val_loss", factor=0.2, patience=3, min_lr=1e-6, verbose=1
        )
        callbacks.append(reduce_lr)

        # Import EarlyStopping if not imported earlier
        early_stopping = EarlyStopping(
            monitor="val_loss", patience=5, restore_best_weights=True, verbose=1
        )
        callbacks.append(early_stopping)

        return callbacks

    def train(self):
        df = load_data(self.config.dataset)
        train_gen, valid_gen, _ = process_data(df)

        # Create Xception base model
        base_model = tf.keras.applications.Xception(
            input_shape=(224, 224, 3), include_top=False, weights=self.config.weights
        )

        base_model.trainable = True

        x = base_model.output

        x = tf.keras.layers.GlobalAveragePooling2D()(x)

        y = tf.keras.layers.Dense(256, activation="relu")(x)

        predictions = tf.keras.layers.Dense(4, activation="softmax", name="final")(y)

        model_Xception = tf.keras.models.Model(
            inputs=base_model.input, outputs=predictions
        )

        model_Xception.compile(
            optimizer=tf.keras.optimizers.Adamax(learning_rate=0.001),
            loss="categorical_crossentropy",
            metrics=["accuracy"],
        )

        callbacks = self.get_callbacks()
        model_Xception.fit(
            train_gen,
            epochs=self.config.epochs,
            validation_data=valid_gen,
            callbacks=[callbacks],
        )
