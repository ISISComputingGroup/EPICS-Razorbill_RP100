from lewis.adapters.stream import StreamInterface
from lewis.core.logging import has_log
from lewis.utils.command_builder import CmdBuilder
from lewis.utils.replies import conditional_reply


@has_log
class Rzbrp100StreamInterface(StreamInterface):
    in_terminator = "\r\n"
    out_terminator = "\r\n"

    commands = {
        # Command to return ID string
        CmdBuilder("get_id").escape("*IDN?").eos().build(),
        # Commands for output
        CmdBuilder("get_output").escape("OUTP").int().escape("?").eos().build(),
        CmdBuilder("set_output").escape("OUTP").int().escape(" ").int().eos().build(),
        # Commands for voltage
        CmdBuilder("get_voltage").escape("SOUR").int().escape(":VOLT:NOW?").eos().build(),
        CmdBuilder("set_voltage").escape("SOUR").int().escape(":VOLT ").float().eos().build(),
        # Commands for voltage slew rate
        CmdBuilder("get_voltage_slewrate").escape("SOUR").int().escape(":VOLT:SLEW?").eos().build(),
        CmdBuilder("set_voltage_slewrate")
        .escape("SOUR")
        .int()
        .escape(":VOLT:SLEW ")
        .float()
        .eos()
        .build(),
    }

    def handle_error(self, request, error):
        """
        If command is not recognised print and error

        Args:
            request: requested string
            error: problem

        """
        self.log.error("An error occurred at request " + repr(request) + ": " + repr(error))

    def catch_all(self, command):
        """
        Catch-all command for debugging
        """
        pass

    def reset(self):
        self.device.reset()
        return self.out_terminator

    @conditional_reply("connected")
    def get_id(self):
        """
            Gets the device Identification string

        :return:  Device ID string
        """
        return "{}".format(self._device.id)

    @conditional_reply("connected")
    def get_output(self, channel):
        """
        Sets the specified channel's output status
            Args:
            channel: channel number
        """
        return "{}".format(int(self._device.outputs[channel - 1]))

    @conditional_reply("connected")
    def set_output(self, channel, output):
        """
        Sets the specified channel's output status
            Args:
            channel: channel number
            output: desired output status (0, 1)
        """
        self._device.outputs[channel - 1] = output

    @conditional_reply("connected")
    def get_voltage(self, channel):
        """
        Gets the voltage of a channel

        Args:
            channel: channel number
        """
        return "{}".format(float(self._device.voltages[channel - 1]))

    @conditional_reply("connected")
    def set_voltage(self, channel, voltage):
        """
        Sets the voltage of a channel

        Args:
            channel: channel number
            voltage: desired output voltage
        """
        self._device.voltages[channel - 1] = voltage

    @conditional_reply("connected")
    def get_voltage_slewrate(self, channel):
        """
        Gets the voltage slew rate of a channel

        Args:
            channel: channel number
        """
        return "{}".format(float(self._device.voltage_slewrates[channel - 1]))

    @conditional_reply("connected")
    def set_voltage_slewrate(self, channel, voltage_slewrate):
        """
        Sets the voltage slew rate of a channel

        Args:
            channel: channel number
            voltage_slewrate: desired voltage slew rate
        """
        self._device.voltage_slewrates[channel - 1] = voltage_slewrate
