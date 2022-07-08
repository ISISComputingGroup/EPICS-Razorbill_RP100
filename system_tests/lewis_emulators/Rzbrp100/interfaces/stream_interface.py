from lewis.adapters.stream import StreamInterface, Cmd
from lewis.utils.command_builder import CmdBuilder
from lewis.core.logging import has_log
from lewis.utils.replies import conditional_reply


@has_log
class Rzbrp100StreamInterface(StreamInterface):

    def __init__(self):
        super(Rzbrp100StreamInterface, self).__init__()
        # Commands that we expect via serial during normal operation
        self.commands = {
            CmdBuilder(self.catch_all).arg("^#9.*$").eos().build(),  # Catch-all command for debugging
            CmdBuilder("get_id").escape("*IDN?").eos().build(),
            # TODO: discover correct syntax for input parameters
            CmdBuilder("get_channel_output").escape("OUTP%1?").eos().build(),
            CmdBuilder("set_channel_output").escape("OUTP%1%1").eos().build(),
        }

        in_terminator = "\r\n"
        out_terminator = "\r\n"

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

    # TODO: finish implementation in 'device.py'

    @conditional_reply("connected")
    def get_channel_output(self, channel):
        """
            Gets the output status of a channel

            Args:
                channel: channel number
        """

        return "{}".format(self._device.output(channel))

    @conditional_reply("connected")
    def set_channel_output(self, channel, output):
        """
            Sets the output status of a channel

            Args:
                channel: channel number
                output: desired output status (ON, OFF)
        """

        self._device.set_output(channel, output)
