import warnings

import tensorflow as tf
from ray.rllib.models.modelv2 import ModelV2
from ray.rllib.models.tf.fcnet import FullyConnectedNetwork
from ray.rllib.models.tf.misc import normc_initializer
from ray.rllib.models.tf.tf_modelv2 import TFModelV2
from ray.rllib.policy.sample_batch import SampleBatch
from ray.rllib.utils.annotations import override
from ray.rllib.utils.framework import try_import_torch

torch, nn = try_import_torch()
warnings.filterwarnings("ignore")


class BatchNormModel(TFModelV2):

    def __init__(self, obs_space, action_space, num_outputs, model_config, name):
        super().__init__(obs_space, action_space, num_outputs, model_config, name)
        inputs = tf.keras.layers.Input(shape=obs_space.shape, name="inputs")
        is_training = tf.keras.layers.Input(shape=(), dtype=tf.bool, batch_size=1, name="is_training")

        var_1, var_2, var_3, var_4, var_5 = tf.split(inputs, num_or_size_splits=5, axis=1)
        normalized_var_2 = tf.keras.layers.BatchNormalization()(var_2)
        normalized_var_3 = tf.keras.layers.BatchNormalization()(var_3)
        normalized_var_4 = tf.keras.layers.BatchNormalization()(var_4)
        normalized_var_5 = tf.keras.layers.BatchNormalization()(var_5)
        normalized_inputs = tf.concat([var_1, normalized_var_2, normalized_var_3, normalized_var_4, normalized_var_5],
                                      axis=1)
        last_layer = normalized_inputs

        hiddens = [256, 256, 256, 256]
        for i, size in enumerate(hiddens):
            label = "fc{}".format(i)
            last_layer = tf.keras.layers.Dense(
                units=size,
                kernel_initializer=normc_initializer(1.0),
                activation=tf.nn.tanh,
                name=label,
            )(last_layer)
            # If you want to add batch normalization layers in between hidden layers
            # last_layer = tf.keras.layers.BatchNormalization()(
            #     last_layer, training=is_training[0]
            # )

        output = tf.keras.layers.Dense(
            units=self.num_outputs,
            kernel_initializer=normc_initializer(0.01),
            activation=None,
            name="fc_out",
        )(last_layer)
        value_out = tf.keras.layers.Dense(
            units=1,
            kernel_initializer=normc_initializer(0.01),
            activation=None,
            name="value_out",
        )(last_layer)

        self.base_model = tf.keras.models.Model(
            inputs=[inputs, is_training], outputs=[output, value_out]
        )

    @override(ModelV2)
    def forward(self, input_dict, state, seq_lens):
        if isinstance(input_dict, SampleBatch):
            is_training = input_dict.is_training
        else:
            is_training = input_dict["is_training"]
        out, self._value_out = self.base_model(
            [input_dict["obs"], tf.expand_dims(is_training, 0)]
        )
        return out, []

    @override(ModelV2)
    def value_function(self):
        return tf.reshape(self._value_out, [-1])


class BatchNormModel2(TFModelV2):

    def __init__(self, obs_space, action_space, num_outputs, model_config, name):
        super().__init__(obs_space, action_space, num_outputs, model_config, name)
        inputs = tf.keras.layers.Input(shape=obs_space.shape, name="inputs")
        is_training = tf.keras.layers.Input(shape=(), dtype=tf.bool, batch_size=1, name="is_training")

        var_1, var_2, var_3, var_4, var_5, var_6 = tf.split(inputs, num_or_size_splits=6, axis=1)
        normalized_var_3 = tf.keras.layers.BatchNormalization()(var_3)
        normalized_var_4 = tf.keras.layers.BatchNormalization()(var_4)
        normalized_var_5 = tf.keras.layers.BatchNormalization()(var_5)
        normalized_var_6 = tf.keras.layers.BatchNormalization()(var_6)
        normalized_inputs = tf.concat([var_1, normalized_var_3, normalized_var_4, normalized_var_5, normalized_var_6],
                                      axis=1)
        last_layer = normalized_inputs

        hiddens = [256, 256, 256, 256]
        for i, size in enumerate(hiddens):
            label = "fc{}".format(i)
            last_layer = tf.keras.layers.Dense(
                units=size,
                kernel_initializer=normc_initializer(1.0),
                activation=tf.nn.tanh,
                name=label,
            )(last_layer)
            # If you want to add batch normalization layers in between hidden layers
            # last_layer = tf.keras.layers.BatchNormalization()(
            #     last_layer, training=is_training[0]
            # )

        output = tf.keras.layers.Dense(
            units=self.num_outputs,
            kernel_initializer=normc_initializer(0.01),
            activation=None,
            name="fc_out",
        )(last_layer)
        value_out = tf.keras.layers.Dense(
            units=1,
            kernel_initializer=normc_initializer(0.01),
            activation=None,
            name="value_out",
        )(last_layer)

        self.base_model = tf.keras.models.Model(
            inputs=[inputs, is_training], outputs=[output, value_out]
        )

    @override(ModelV2)
    def forward(self, input_dict, state, seq_lens):
        if isinstance(input_dict, SampleBatch):
            is_training = input_dict.is_training
        else:
            is_training = input_dict["is_training"]
        out, self._value_out = self.base_model(
            [input_dict["obs"], tf.expand_dims(is_training, 0)]
        )
        return out, []

    @override(ModelV2)
    def value_function(self):
        return tf.reshape(self._value_out, [-1])


class BatchNormModel3(TFModelV2):

    def __init__(self, obs_space, action_space, num_outputs, model_config, name):
        super().__init__(obs_space, action_space, num_outputs, model_config, name)
        inputs = tf.keras.layers.Input(shape=obs_space.shape, name="inputs")
        is_training = tf.keras.layers.Input(shape=(), dtype=tf.bool, batch_size=1, name="is_training")

        var_1, var_2, var_3, var_4, var_5, var_6, var_7, var_8 = tf.split(inputs, num_or_size_splits=8, axis=1)
        normalized_var_3 = tf.keras.layers.BatchNormalization()(var_3)
        normalized_var_4 = tf.keras.layers.BatchNormalization()(var_4)
        normalized_var_5 = tf.keras.layers.BatchNormalization()(var_5)
        normalized_var_6 = tf.keras.layers.BatchNormalization()(var_6)
        normalized_var_7 = tf.keras.layers.BatchNormalization()(var_7)
        normalized_var_8 = tf.keras.layers.BatchNormalization()(var_8)
        normalized_inputs = tf.concat(
            [var_1, normalized_var_3, normalized_var_4, normalized_var_5, normalized_var_6, normalized_var_7,
             normalized_var_8],
            axis=1)
        last_layer = normalized_inputs

        hiddens = [256, 256, 256, 256]
        for i, size in enumerate(hiddens):
            label = "fc{}".format(i)
            last_layer = tf.keras.layers.Dense(
                units=size,
                kernel_initializer=normc_initializer(1.0),
                activation=tf.nn.tanh,
                name=label,
            )(last_layer)
            # If you want to add batch normalization layers in between hidden layers
            # last_layer = tf.keras.layers.BatchNormalization()(
            #     last_layer, training=is_training[0]
            # )

        output = tf.keras.layers.Dense(
            units=self.num_outputs,
            kernel_initializer=normc_initializer(0.01),
            activation=None,
            name="fc_out",
        )(last_layer)
        value_out = tf.keras.layers.Dense(
            units=1,
            kernel_initializer=normc_initializer(0.01),
            activation=None,
            name="value_out",
        )(last_layer)

        self.base_model = tf.keras.models.Model(
            inputs=[inputs, is_training], outputs=[output, value_out]
        )

    @override(ModelV2)
    def forward(self, input_dict, state, seq_lens):
        if isinstance(input_dict, SampleBatch):
            is_training = input_dict.is_training
        else:
            is_training = input_dict["is_training"]
        out, self._value_out = self.base_model(
            [input_dict["obs"], tf.expand_dims(is_training, 0)]
        )
        return out, []

    @override(ModelV2)
    def value_function(self):
        return tf.reshape(self._value_out, [-1])


class BatchNormModel4(TFModelV2):

    def __init__(self, obs_space, action_space, num_outputs, model_config, name):
        super().__init__(obs_space, action_space, num_outputs, model_config, name)
        inputs = tf.keras.layers.Input(shape=obs_space.shape, name="inputs")
        is_training = tf.keras.layers.Input(shape=(), dtype=tf.bool, batch_size=1, name="is_training")

        var_1, var_2, var_3, var_4, var_5, var_6, var_7, var_8, var_9 = tf.split(inputs, num_or_size_splits=9, axis=1)
        normalized_var_3 = tf.keras.layers.BatchNormalization()(var_3)
        normalized_var_4 = tf.keras.layers.BatchNormalization()(var_4)
        normalized_var_5 = tf.keras.layers.BatchNormalization()(var_5)
        normalized_var_6 = tf.keras.layers.BatchNormalization()(var_6)
        normalized_var_7 = tf.keras.layers.BatchNormalization()(var_7)
        normalized_var_8 = tf.keras.layers.BatchNormalization()(var_8)
        normalized_var_9 = tf.keras.layers.BatchNormalization()(var_9)
        normalized_inputs = tf.concat(
            [var_1, normalized_var_3, normalized_var_4, normalized_var_5, normalized_var_6, normalized_var_7,
             normalized_var_8, normalized_var_9],
            axis=1)
        last_layer = normalized_inputs

        hiddens = [256, 256, 256, 256]
        for i, size in enumerate(hiddens):
            label = "fc{}".format(i)
            last_layer = tf.keras.layers.Dense(
                units=size,
                kernel_initializer=normc_initializer(1.0),
                activation=tf.nn.tanh,
                name=label,
            )(last_layer)
            # If you want to add batch normalization layers in between hidden layers
            # last_layer = tf.keras.layers.BatchNormalization()(
            #     last_layer, training=is_training[0]
            # )

        output = tf.keras.layers.Dense(
            units=self.num_outputs,
            kernel_initializer=normc_initializer(0.01),
            activation=None,
            name="fc_out",
        )(last_layer)
        value_out = tf.keras.layers.Dense(
            units=1,
            kernel_initializer=normc_initializer(0.01),
            activation=None,
            name="value_out",
        )(last_layer)

        self.base_model = tf.keras.models.Model(
            inputs=[inputs, is_training], outputs=[output, value_out]
        )

    @override(ModelV2)
    def forward(self, input_dict, state, seq_lens):
        if isinstance(input_dict, SampleBatch):
            is_training = input_dict.is_training
        else:
            is_training = input_dict["is_training"]
        out, self._value_out = self.base_model(
            [input_dict["obs"], tf.expand_dims(is_training, 0)]
        )
        return out, []

    @override(ModelV2)
    def value_function(self):
        return tf.reshape(self._value_out, [-1])


class GameNormModel(TFModelV2):

    def __init__(self, obs_space, action_space, num_outputs, model_config, name):
        super().__init__(obs_space, action_space, num_outputs, model_config, name)
        inputs = tf.keras.layers.Input(shape=obs_space.shape, name="inputs")
        is_training = tf.keras.layers.Input(shape=(), dtype=tf.bool, batch_size=1, name="is_training")

        # 1 action
        # 2 wait time
        # 3 deposit call address
        # 4 withdraw call address
        # 5 number of deposits
        # 6 balance deposit call address
        # 7 balance withdraw call address
        # 8 balance TC contract

        var_1, var_2, var_3, var_4, var_5, var_6, var_7, var_8 = tf.split(inputs, num_or_size_splits=8, axis=1)

        normalized_var_2 = tf.keras.layers.BatchNormalization()(var_2)
        normalized_var_5 = tf.keras.layers.BatchNormalization()(var_5)
        normalized_var_6 = tf.keras.layers.BatchNormalization()(var_6)
        normalized_var_7 = tf.keras.layers.BatchNormalization()(var_7)
        normalized_var_8 = tf.keras.layers.BatchNormalization()(var_8)
        normalized_inputs = tf.concat(
            [var_1, normalized_var_2, var_3, var_4, normalized_var_5, normalized_var_6, normalized_var_7,
             normalized_var_8],
            axis=1)
        last_layer = normalized_inputs

        hiddens = [64, 64]
        for i, size in enumerate(hiddens):
            label = "fc{}".format(i)
            last_layer = tf.keras.layers.Dense(
                units=size,
                kernel_initializer=normc_initializer(1.0),
                activation=tf.nn.tanh,
                name=label,
            )(last_layer)
            # If you want to add batch normalization layers in between hidden layers
            # last_layer = tf.keras.layers.BatchNormalization()(
            #     last_layer, training=is_training[0]
            # )

        output = tf.keras.layers.Dense(
            units=self.num_outputs,
            kernel_initializer=normc_initializer(0.01),
            activation=None,
            name="fc_out",
        )(last_layer)
        value_out = tf.keras.layers.Dense(
            units=1,
            kernel_initializer=normc_initializer(0.01),
            activation=None,
            name="value_out",
        )(last_layer)

        self.base_model = tf.keras.models.Model(
            inputs=[inputs, is_training], outputs=[output, value_out]
        )

    @override(ModelV2)
    def forward(self, input_dict, state, seq_lens):
        if isinstance(input_dict, SampleBatch):
            is_training = input_dict.is_training
        else:
            is_training = input_dict["is_training"]
        out, self._value_out = self.base_model(
            [input_dict["obs"], tf.expand_dims(is_training, 0)]
        )
        return out, []

    @override(ModelV2)
    def value_function(self):
        return tf.reshape(self._value_out, [-1])


class CustomModelTFModelV2Agent1(TFModelV2):

    def __init__(self, obs_space, action_space, num_outputs, model_config, name):
        super(CustomModelTFModelV2Agent1, self).__init__(obs_space,
                                                         action_space,
                                                         num_outputs,
                                                         model_config,
                                                         name)
        model_config['fcnet_hiddens'] = [256, 256, 256, 256]
        self.model = FullyConnectedNetwork(obs_space, action_space, num_outputs, model_config, name)

    def import_from_h5(self, h5_file: str):
        pass

    def forward(self, input_dict, state, seq_lens):
        return self.model.forward(input_dict, state, seq_lens)

    def value_function(self):
        return self.model.value_function()


class CustomModelTFModelV2Agent2(TFModelV2):

    def __init__(self, obs_space, action_space, num_outputs, model_config, name):
        super(CustomModelTFModelV2Agent2, self).__init__(obs_space,
                                                         action_space,
                                                         num_outputs,
                                                         model_config,
                                                         name)

        self.model = FullyConnectedNetwork(obs_space, action_space, num_outputs, model_config, name)

    def import_from_h5(self, h5_file: str):
        pass

    def forward(self, input_dict, state, seq_lens):
        return self.model.forward(input_dict, state, seq_lens)

    def value_function(self):
        return self.model.value_function()
