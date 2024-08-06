from collections import OrderedDict

from lewis.devices import StateMachineDevice

from .states import DefaultState


class SimulatedRzbrp100(StateMachineDevice):
    def _initialize_data(self):
        """
        Initialize all of the device's attributes.
        """
        self.connected = True
        self.id = "EMULATED Razorbill RP100 Strain Cell PSU"
        self.outputs = [0, 0]
        self.voltages = [0.0, 0.0]
        self.voltage_slewrates = [0.0, 0.0]

    def _get_state_handlers(self):
        return {
            "default": DefaultState(),
        }

    def _get_initial_state(self):
        return "default"

    def _get_transition_handlers(self):
        return OrderedDict([])

    def reset(self):
        self._initialize_data()
