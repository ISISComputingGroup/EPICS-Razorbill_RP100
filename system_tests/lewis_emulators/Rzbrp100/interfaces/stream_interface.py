from lewis.adapters.stream import StreamInterface, Cmd
from lewis.utils.command_builder import CmdBuilder
from lewis.core.logging import has_log
from lewis.utils.replies import conditional_reply


@has_log
class Rzbrp100StreamInterface(StreamInterface):

    in_terminator = "\r\n"
    out_terminator = "\r\n"

    commands = {
        # CmdBuilder(self.catch_all).arg("^#9.*$").eos().build(),  # Catch-all command for debugging
        CmdBuilder("get_id").escape("*IDN?").eos().build(),

        CmdBuilder("get_voltage").escape("SOUR").int().escape(":VOLT:NOW?").eos().build(),
        CmdBuilder("set_voltage").escape("SOUR").int().escape(":VOLT ").float().eos().build(),

        # Commands for output on and off (not currently required)
        # CmdBuilder("get_channel_output").escape("OUTP%1?").eos().build(),
        # CmdBuilder("set_channel_output").escape("OUTP%1%1").eos().build(),
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

    @conditional_reply("connected")
    def get_id(self):
        """
            Gets the device Identification string

        :return:  Device ID string
        """

        return "{}".format(self._device.id)


    @conditional_reply("connected")
    def get_voltage(self, channel):
        """
            Gets the voltage of a channel

            Args:
                channel: channel number
        """

        return "{}".format(float(self._device.voltages[channel-1]))

    @conditional_reply("connected")
    def set_voltage(self, channel, output):
        """
            Sets the voltage of a channel

            Args:
                channel: channel number
                output: desired output voltage
        """

        self._device.voltages[channel-1] = output
