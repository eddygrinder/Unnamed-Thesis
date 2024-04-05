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
import store_ps_dmm

# Caminho para o diretório ctrl_hardware
ctrl_hardware_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ctrl_hardware'))
# Adiciona o diretório ao sys.path
sys.path.append(ctrl_hardware_path)

from pyvirtualbench import PyVirtualBench, PyVirtualBenchException, DmmFunction

# You will probably need to replace "myVirtualBench" with the name of your device.
# By default, the device name is the model number and serial number separated by a hyphen; e.g., "VB8012-309738A".
# You can see the device's name in the VirtualBench Application under File->About

def test_parameters(Vcc:int, R:int, measure_parameter:str, configOK:bool, configSTOP:bool):
    virtualbench = PyVirtualBench('VB8012-30A210F')

    '''
    São passados vários parâmetros do ficheiro views.py para este script/função.
    De entre eles, são feitas quatro possíveis combinações que correspondem a quatro situações diferentes:
    1 - Vcc, Resistance, measure_parameter, configOK, configSTOP = 0, 0, None, True, None - Botão OK premido
        Sistema adquire a fonte de alimentação e o multímetro e pronto para realizar medição
    2 - Vcc, Resistance, measure_parameter, configOK, configSTOP = 0, 0, None, None, True - Botão STOP premido
        Sistema "desliga" a fonte de alimentação e o multímetro, e os relés são desligados (configuração inicial)
    3/4 - Vcc, Resistance, measure_parameter, configOK, configSTOP = !=0, !=0, V or I, None, None
        Sistema realiza medição de tensão ou corrente, conforme os parâmetros passados
    '''
    if (Vcc == 0 and R == 0 and measure_parameter is None and configOK is True and configSTOP is None):
        print("OKPSDMM")
        #Chama a função que adquire a fonte de alimentação e o multímetro
        ps = virtualbench.acquire_power_supply()
        dmm = virtualbench.acquire_digital_multimeter()
        store_ps_dmm.set_values(ps, dmm)
        print(ps, dmm )
    if (Vcc == 0 and R == 0 and measure_parameter is None and configOK is None and configSTOP is True):
        print("STOP")
        #Chama a função que desliga fonte de alimentação e multímetro
        ps, dmm = store_ps_dmm.get_values()       
        ps.release()
        dmm.release()
        virtualbench.release()
        store_ps_dmm.clear_values()
    
    if (Vcc != 0 and R != 0 and measure_parameter is not None and configOK is None and configSTOP is None):
        print("Medição")
        #Chama a função que realiza a medição de tensão ou corrente
        try:
            #############################
            # Power Supply Configuration
            #############################
            channel = "ps/+25V"
            voltage_level = Vcc
            current_limit = 0.5 
            ps, dmm = store_ps_dmm.get_values()       
            ps.configure_voltage_output(channel, voltage_level, current_limit)
            ps.enable_all_outputs(True)
            print("Adquiriu a fonte de alimentação")
        # ... use ps for configuration ...    ps.configure_voltage_output(channel, voltage_level, current_limit)
            #dmm = virtualbench.acquire_digital_multimeter()
            print("Adquiriu o multímetro")
            # ... use dmm for configuration ...

            if measure_parameter == "voltage":
                dmm.configure_measurement(DmmFunction.DC_VOLTS, True, 10)
            elif measure_parameter == "current":
                dmm.configure_measurement(DmmFunction.DC_CURRENT, True, 1) # Verificar Manual Range = 10.0
        
            measurement_result = dmm.read()        
            print("MeasurementCONFIG: %f V" % (measurement_result))

        except PyVirtualBenchException as e:
            print("Error/Warning %d occurred\n%s" % (e.status, e))
        finally:
            return measurement_result