# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 15:46:25 2024

@author: kimsj
"""

import math

# proton
gived_energy_eV = 0.01e6

charge = 1.602*1e-19 #C
J_energy = gived_energy_eV*charge


proton_mass = 1.67*1e-27 #kg

electron_mass= 9.1093837*1e-31

proton_velocity = math.sqrt(J_energy/proton_mass)
electron_velocity = math.sqrt(J_energy/electron_mass)


electron_momentum = math.sqrt(2*electron_mass*J_energy)
electron_m = electron_mass*electron_velocity

light_velocity = 3*1e8
# lorentz_factor = 1 / (math.sqrt(1 - (electron_velocity ** 2) / (light_velocity ** 2)))
# electron_re = lorentz_factor*electron_mass*electron_velocity

proton_velocity = math.sqrt(J_energy/proton_mass) # unit : m/s

proton_momentum = math.sqrt(2*proton_mass*J_energy)
proton_m = proton_mass*proton_velocity

magnetic_field = 0.2 #kg/(s*C) - T

# electron_gyro_radius = electron_momentum / (charge*magnetic_field)  # unit : m

proton_gyro_radius1 = proton_momentum / (charge*magnetic_field)  # unit : m
proton_gyro_radius2 = proton_m / (charge*magnetic_field)  # unit : m

electron_gyro_radius1 = electron_momentum / (charge*magnetic_field)  # unit : m
electron_gyro_radius2 = electron_m / (charge*magnetic_field)  # unit : m
# electron_gyro_radius3 = electron_re / (charge*magnetic_field)  # unit : m


print(proton_gyro_radius1)
print(proton_gyro_radius2)
print(electron_gyro_radius1)
print(electron_gyro_radius2)
# print(electron_gyro_radius3)