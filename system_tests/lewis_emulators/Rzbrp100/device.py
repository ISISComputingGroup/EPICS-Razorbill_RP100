from collections import OrderedDict
from .states import DefaultState
from lewis.devices import StateMachineDevice


class SimulatedRzbrp100(StateMachineDevice):

    def _initialize_data(self):
        """
        Initialize all of the device's attributes.
        """
        self.connected = True
        self.id = "Razorbill RP100 strain cell PSU - EMULATOR"
        self.output1 = self.set_output(1, "0")
        self.output2 = self.set_output(2, "0")

    # TODO: discover correct syntax for following command:

    def set_output(self, channel, output):
        """
            Sets the specified channel's output status

            Args:
                channel: channel to set
                output: desired output status (1, 0)
        """

        self.output"{}".format(channel) = output

    def _get_state_handlers(self):
        return {
            'default': DefaultState(),
        }

    def _get_initial_state(self):
        return 'default'

    def _get_transition_handlers(self):
        return OrderedDict([
        ])
