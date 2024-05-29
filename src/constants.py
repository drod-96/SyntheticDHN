import numpy as np

CP = 4200 # J/Kg/K at 20°C (water)
RHO = 996 # Kg/m3
INF = 10

POWER_DEMAND_LOSS_KEY = "Power_demand_loss" # also used in the normalization and denormalization
UPPER_TEMPERATURE_KEY = "Upper_temperature"
LOWER_TEMPERATURE_KEY = "Lower_temperature"
LOSS_PER_TEMPERATURE_KEY = "Loss_per_temperature"
DELAY_TIME_KEY = "Delay_time"

NORMALIZATION_POWER_KEY = "Power_or_demand_or_loss"
NORMALIZATION_MASS_RATE_KEY = "Mass_rate"
NORMALIZATION_TEMPERATURE_KEY = "Temperature"
NORMALIZATION_SUPPLY_TEMPERATURE_KEY = "S_Temperature"
NORMALIZATION_RETURN_TEMPERATURE_KEY = "R_Temperature"
NORMALIZATION_DELTA_TEMPERATURE_KEY = "DeltaT"
NORMALIZATION_HEAT_LOSS_PER_TEMP_KEY = "Loss_per_t"
NORMALIZATION_DELAY_TIME_KEY = "Delay_time"

BASE_VALUES = {
    POWER_DEMAND_LOSS_KEY: 20e6, # in W
    UPPER_TEMPERATURE_KEY: 373.15, # in K (100°C)
    LOWER_TEMPERATURE_KEY: 298.15, # in K (40°C)
    LOSS_PER_TEMPERATURE_KEY: 1 * (0.06) * 1e3, # d * length * h
    DELAY_TIME_KEY: np.pi * (0.1*0.1) * RHO * 10e3 / 20, # in hours 
}

DEMAND_NOMINAL = 1e6
LOSS_NOMINAL = 40e3

LOWER_CONV_COEFF = 0.2
UPPER_CONV_COEFF = 1.2 # Le modele physique converge pas quand cette perte est trop grande

LOWER_DIAMETER = 0.01 # 1 cm
UPPER_DIAMETER = 0.1 # 10 cm

# Thickness not used

# Data venant de Mohamed et de NASA website
RECENT_BUILDING_U = 0.84 # W.K^1.m^-2
ANCIENT_BUILDING_U = 3.4
OFFICE_BUILDING_U = 2.5

# Temperature at around 55°C is necessary to avoid Legionella proliferation risk
# http://carbonalternatives.co.uk/wp-content/uploads/2016/11/CIBSE-Paper-Energy-efficient-DH-Martin-Crane.pdf
# Achieving low return increases the DHN efficiency
# Return temperatures are determined by consumers type (Water generation, Space heating, by-passes, DHW+Space heating with no load, Heat exchanges at building entry)
# return temperatures can be (20°C for DHW, 40°C (UKguidance CIBSE)), more than 60°C drops drastically the efficiency of the DHN 

LOWER_RETURN_TEMPERATURE = 275.13 + 40.
UPPER_RETURN_TEMPERATURE = 275.13 + 55.

# Supply temperatures, se baser sur les types de DHN suppliers
# Peut etre entre 60 - 100 
# http://carbonalternatives.co.uk/wp-content/uploads/2016/11/CIBSE-Paper-Energy-efficient-DH-Martin-Crane.pdf
# A 55 minimum to avoid Legionella proliferation risk
LOWER_SUPPLY_TEMPERATURE = 275.15 + 55.
UPPER_SUPPLY_TEMPERATURE = 275.15 + 90.

