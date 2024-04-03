#! /usr/bin/env python3

# The MIT License (MIT)
#
# Copyright (c) 2016 Charles Armstrap <charles@armstrap.org>
# If you like this library, consider donating to: https://bit.ly/armstrap-opensource-dev
# Anything helps.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import os, sys

# Caminho para o diretório ctrl_hardware
ctrl_hardware_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ctrl_hardware'))
# Adiciona o diretório ao sys.path
sys.path.append(ctrl_hardware_path)

from pyvirtualbench import PyVirtualBench, PyVirtualBenchException, DmmFunction

# You will probably need to replace "myVirtualBench" with the name of your device.
# By default, the device name is the model number and serial number separated by a hyphen; e.g., "VB8012-309738A".
# You can see the device's name in the VirtualBench Application under File->About
virtualbench = PyVirtualBench('VB8012-30A210F')

# Variáveis globais para armazenar as instâncias dos instrumentos
power_supply_instance = None
digital_multimeter_instance = None

def acquire_power_supply():
    """
    Adquire uma instância da fonte de alimentação do VirtualBench.
    Utiliza inicialização preguiçosa para adquirir a instância apenas quando necessário.
    """
    global power_supply_instance
    if power_supply_instance is None:
        power_supply_instance = virtualbench.acquire_power_supply()
    return power_supply_instance

def acquire_digital_multimeter():
    """
    Adquire uma instância do multímetro digital do VirtualBench.
    Utiliza inicialização preguiçosa para adquirir a instância apenas quando necessário.
    """
    global digital_multimeter_instance
    if digital_multimeter_instance is None:
        digital_multimeter_instance = virtualbench.acquire_digital_multimeter()
    return digital_multimeter_instance

def release_instruments():
    """
    Libera as instâncias dos instrumentos se elas existirem.
    """
    global power_supply_instance, digital_multimeter_instance
    if power_supply_instance:
        power_supply_instance.release()
        power_supply_instance = None
    if digital_multimeter_instance:
        digital_multimeter_instance.release()
        digital_multimeter_instance = None

def config_VB_DMM (Vcc:int, configMeasure:str):
    global power_supply_instance

    try:
        #############################
        # Power Supply Configuration
        #############################

        channel = "ps/+25V"
        voltage_level = Vcc
        current_limit = 0.5
        ps = acquire_power_supply()
        # ... use ps for configuration ...    ps.configure_voltage_output(channel, voltage_level, current_limit)
        
        ps.configure_voltage_output(channel, voltage_level, current_limit)
        ps.enable_all_outputs(True)
        
        dmm = acquire_digital_multimeter()
        # ... use dmm for configuration ...
        if configMeasure == "voltage":
            dmm.configure_measurement(DmmFunction.DC_VOLTS, True, 10)
        elif configMeasure == "current":
            dmm.configure_measurement(DmmFunction.DC_CURRENT, True, 1) # Verificar Manual Range = 10.0
        
        measurement_result = dmm.read()
        print("MeasurementCONFIG: %f V" % (measurement_result))

    except PyVirtualBenchException as e:
        print("Error/Warning %d occurred\n%s" % (e.status, e))
    finally:
        release_instruments()
        return measurement_result
