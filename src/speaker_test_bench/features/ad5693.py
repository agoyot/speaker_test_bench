"""
Code for interface AD5693 analog device DAC
"""

from dataclasses import dataclass
from typing import SupportsIndex, Union

import numpy as np
import smbus
import time


@dataclass(init=False)
class AD5693:
    """
    Code for interface AD5693 analog device DAC
    """

    def __init__(
        self,
        device_address: Union[int, SupportsIndex, str],
        bus_number: int = 1,
        v_ref: float = 5,
    ) -> None:

        self.device_address = hex(device_address)

        self.NOP = 0x00
        """
        The input register allows the preloading of a new value for the DAC register
        """
        self.WRITE_INPUT_REGISTER_ADDR = 0x10
        """
        This command transfers the contents of the input register to the DAC register "
        "and, consequently,the Vout pin is updated,The data contained in the serial write is ignored"
        """
        self.UPDATE_REGISTER_ADDR = 0x20
        """
        This command updates the DAC output on completion of the write operation.
        The input register is refreshed automatically with the DAC register value
        """
        self.DATA_REGISTER_ADDR = 0x30
        """
        The control register is used to set the power-down and gain functions.
        It is also used to enable/disable the internal reference and perform a software reset
        """
        self.CONTROL_REGISTER_ADDR = 0x40
        """
        Define operating mode
        In normal mode, the output buffer is directly connected to the VOUT pin.
        In power-down mode, the output buffer is internally disabled and the VOUT pin output impedance can be selected
        """
        self.NORMAL_MODE = 0x00
        self.OUTPUT_1K_IMPEDANCE = 0x01
        self.OUTPUT_100K_IMPEDANCE = 0x02
        self.OUTPUT_TREE_STATE = 0x03

        """
        Default configuration
        """
        self._mode = self.NORMAL_MODE
        self._internal_ref = True
        self._gain = False

        self.v_ref = v_ref
        self.bus = smbus.SMBus(bus_number)
        try:
            self.update_control_register(
                mode=self._mode,
                internal_ref=self._internal_ref,
                gain=self._gain,
            )
        except OSError as error:
            raise OSError(f"Failed to initialize AD569x, {error}") from error

    @staticmethod
    def convert_analog_to_digital(
        voltage: Union[float, np.ndarray], v_ref: float
    ) -> Union[int, np.ndarray]:
        resolution = 16
        return (np.array(voltage / v_ref) * ((2**resolution) - 1)).astype(int)

    def send_command(self, register: int, data: int) -> None:
        """
        Send a command and data to the I2C device.

        This internal function prepares a 3-byte buffer containing the command and data,
        and writes it to the I2C device.

        :param register: The register address
        :param data: The 16-bit data to send.
        """
        try:
            high_byte = (data >> 8) & 0xFF
            low_byte = data & 0xFF
            data = bytearray([high_byte, low_byte])
            self.bus.write_i2c_block_data(self.device_address, register, data)
        except Exception as error:
            raise Exception(f"Error sending command: {error}") from error

    def update_control_register(
        self, mode: int, internal_ref: bool, gain: bool
    ) -> None:
        self.reset()
        # Prepare the high and low data bytes
        data = 0x0000
        data |= mode << 13  # Set D14 and D13 for the operating mode
        data |= not internal_ref << 12  # Set D12 for internal_ref
        data |= gain << 11  # Set D11 for the gain
        self.send_command(register=self.CONTROL_REGISTER_ADDR, data=data)

    def reset(self) -> None:
        """
        The AD5693R/AD5692R/AD5691R/AD5693 control register contains a software reset bit that resets the DAC to
        zero-scale and resets the input, DAC, and control registers to their default values.
        A software reset is initiated by setting the RESET bit in the control register to 1 (D15).
        When the software reset has completed, the reset bit is cleared to 0 automatically.
        """
        reset_command = 0x8000
        try:
            self.send_command(
                register=self.CONTROL_REGISTER_ADDR, data=reset_command
            )
        except Exception as error:
            raise Exception(f"Error during reset: {error}") from error

    def set_voltage(self, voltage: float) -> None:
        data = self.convert_analog_to_digital(voltage=voltage, v_ref=self.v_ref)
        self.send_command(register=self.DATA_REGISTER_ADDR, data=data)

    def generate_sine_wave(self, frequency: float, duration: float):
        """
        Generate a sinusoidal waveform with the specified frequency and duration.

        :param frequency: Frequency of the sine wave in Hertz.
        :param duration: Duration of the waveform generation in seconds.
        """
        try:
            num_samples = int(self.v_ref * duration * frequency)
            time_per_sample = 1.0 / (frequency * num_samples)

            for i in range(num_samples):
                angle = 2.0 * np.pi * frequency * i * time_per_sample
                voltage = 0.5 * self.v_ref * np.sin(angle) + 0.5 * self.v_ref
                self.set_voltage(voltage)
                time.sleep(time_per_sample)

        except Exception as error:
            raise Exception(f"Error during sinusoidal waveform generation: {error}") from error
