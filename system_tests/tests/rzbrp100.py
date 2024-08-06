import itertools
import unittest

from parameterized import parameterized
from utils.channel_access import ChannelAccess
from utils.ioc_launcher import get_default_ioc_dir
from utils.test_modes import TestModes
from utils.testing import get_running_lewis_and_ioc, parameterized_list, skip_if_recsim

DEVICE_NAME = "Rzbrp100"
DEVICE_PREFIX = "RZBRP100_01"


IOCS = [
    {
        "name": DEVICE_PREFIX,
        "directory": get_default_ioc_dir("RZBRP100"),
        "macros": {},
        "emulator": DEVICE_NAME,
    },
]


TEST_MODES = [TestModes.RECSIM, TestModes.DEVSIM]

CHANNELS = ["1", "2"]
TEST_FLOAT_VALUES = (-12.34, 0, 1, 99.99)
OUTPUT_STATES = ["ON", "OFF"]


class Rzbrp100Tests(unittest.TestCase):
    """
    Tests for the Razorbill RP100 Strain Cell PSU (Rzbrp100 IOC).
    """

    def setUp(self):
        self._lewis, self._ioc = get_running_lewis_and_ioc(DEVICE_NAME, DEVICE_PREFIX)
        self.ca = ChannelAccess(device_prefix=DEVICE_PREFIX)
        self._lewis.backdoor_run_function_on_device("reset")

    @skip_if_recsim("Behaviour cannot be simulated in Recsim")
    def test_WHEN_identity_requested_THEN_correct_identity_returned(self):
        expected_id_string = "EMULATED Razorbill RP100 Strain Cell PSU"[
            0:39
        ]  # 40 character PV field limit
        self.ca.assert_that_pv_is("ID", expected_id_string)

    @parameterized.expand(parameterized_list(itertools.product(CHANNELS, OUTPUT_STATES)))
    def test_WHEN_output_state_is_set_THEN_value_updates(self, _, chan, val):
        self.ca.assert_setting_setpoint_sets_readback(
            val, set_point_pv="CH{}:OUTPUT:SP".format(chan), readback_pv="CH{}:OUTPUT".format(chan)
        )

    @parameterized.expand(parameterized_list(itertools.product(CHANNELS, OUTPUT_STATES)))
    def test_WHEN_output_state_is_set_THEN_setpoint_readback_updates(self, _, chan, val):
        self.ca.assert_setting_setpoint_sets_readback(
            val,
            set_point_pv="CH{}:OUTPUT:SP".format(chan),
            readback_pv="CH{}:OUTPUT:SP:RBV".format(chan),
        )

    @parameterized.expand(parameterized_list(itertools.product(CHANNELS, TEST_FLOAT_VALUES)))
    def test_WHEN_voltage_setpoint_is_set_THEN_value_updates(self, _, chan, val):
        self.ca.assert_setting_setpoint_sets_readback(
            val, set_point_pv="CH{}:VOLT:SP".format(chan), readback_pv="CH{}:VOLT".format(chan)
        )

    @parameterized.expand(parameterized_list(itertools.product(CHANNELS, TEST_FLOAT_VALUES)))
    def test_WHEN_voltage_setpoint_is_set_THEN_setpoint_readback_updates(self, _, chan, val):
        self.ca.assert_setting_setpoint_sets_readback(
            val,
            set_point_pv="CH{}:VOLT:SP".format(chan),
            readback_pv="CH{}:VOLT:SP:RBV".format(chan),
        )

    @parameterized.expand(parameterized_list(itertools.product(CHANNELS, TEST_FLOAT_VALUES)))
    def test_WHEN_voltage_slewrate_setpoint_is_set_THEN_value_updates(self, _, chan, val):
        self.ca.assert_setting_setpoint_sets_readback(
            val,
            set_point_pv="CH{}:VOLT:SLEWRATE:SP".format(chan),
            readback_pv="CH{}:VOLT:SLEWRATE".format(chan),
        )

    @parameterized.expand(parameterized_list(itertools.product(CHANNELS, TEST_FLOAT_VALUES)))
    def test_WHEN_voltage_slewrate_setpoint_is_set_THEN_setpoint_readback_updates(
        self, _, chan, val
    ):
        self.ca.assert_setting_setpoint_sets_readback(
            val,
            set_point_pv="CH{}:VOLT:SLEWRATE:SP".format(chan),
            readback_pv="CH{}:VOLT:SLEWRATE:SP:RBV".format(chan),
        )
