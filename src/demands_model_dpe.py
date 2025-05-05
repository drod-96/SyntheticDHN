import sys
sys.path.insert(0, r'D:\PhD DATA\Codes & Works\SyntheticDHN\SyntheticDHN\src')

import numpy as np
import os
import json
import pandas as pd

# French DPE energetic class consumption levels
dpe_classes_conso_thresholds = {
    'A': [20.0, 70.0], # kWh/m2/an
    'B': [71.0, 110.0],
    'C': [111.0, 180.0],
    'D': [181, 250.0],
    'E': [251, 330.0],
    'F': [331, 420.0],
    'G': [421, 1000.0], # No upper limit
}

# Different building types heating area
area_building_types = {
    'COM': [100, 5000], #m2, commercial uses
    'MFH': [200, 1500], #m2, multi-family houses
    'SFH': [100, 200], #m2, single-family houses
    'APPRT': [9*70, 50*100], #m2, appartments 
}

# France park building DPE class distribution, generated from DPE data
distribution_classes_dpe = {
    "APPRT": {
        "A": 17.563412759415833,
        "B": 12.730591852421213,
        "C": 37.163720215219065,
        "D": 19.4369715603382,
        "E": 8.61837048424289,
        "F": 2.66141429669485,
        "G": 1.8255188316679476
    },
    "SFH": {
        "A": 57.84861430605762,
        "B": 5.1046116770730645,
        "C": 11.019826925183482,
        "D": 11.874246905466098,
        "E": 8.09508160806222,
        "F": 3.768211195092562,
        "G": 2.2894073830649577
    },
    "MFH": {
        "A": 17.278617710583152,
        "B": 7.559395248380129,
        "C": 34.557235421166304,
        "D": 20.950323974082075,
        "E": 11.663066954643629,
        "F": 4.751619870410368,
        "G": 3.2397408207343417
    },
    "COM": {
        "A": 11.110000000000001,
        "B": 12.25,
        "C": 24.72,
        "D": 22.62,
        "E": 13.200000000000001,
        "F": 5.88,
        "G": 10.22
    },
    "Info": "Percentage of building types DPE class within french buildings from DPE real data"
}

# Substations heating area range
min_heating_area = 500
max_heating_area = 5000

def generate_uniform_value_in_dpe(dpe_class):
    """Generates a consumption value inside the DPE class

    Args:
        dpe_class (str): the DPE class inside ['A', 'B', 'C', 'D', 'E', 'F', 'G']

    Returns:
        float: the value selected
    """
    if dpe_class not in dpe_classes_conso_thresholds:
        raise Exception('DPE Class must be inside [A, B, C, D, E, F, G]')
    
    threshold_values = dpe_classes_conso_thresholds[dpe_class]
    val_selected = np.random.uniform(low=threshold_values[0], high=threshold_values[1])
    return val_selected

def _generate_heating_demands_from_percentage_of_total_areas(min_heating_area=min_heating_area, max_heating_area=max_heating_area, verbose=0, one_type_per_subsation=False) -> dict:
    """Generates heating demand profile for a substation with a random heating area between fixed ranges. Each building type will have a percentage of this pre-selected heating area.

    Args:
        min_heating_area (float, optional): Minimum heating area. Defaults to min_heating_area.
        max_heating_area (float, optional): Maximum heating area. Defaults to max_heating_area.
        verbose (int, optional): Verbosity. Defaults to 0.
        one_type_per_subsation (bool, optional): If true only one type of building per substation, otherwise, it will be a random combinaison of all types. Defaults to False.

    Returns:
        dict: dictionary containing the percentage of each type, profile factors and heating demands of the substation
    """
    
    heating_profiles = pd.read_csv(os.path.join('src', 'files', 'heating_demands_profiles_v2.csv'))
    dict_values = {}
    
    # Here
    # We fix total heating area and each building type has its percentage selected randomly
    heating_surface_area = np.random.uniform(low=min_heating_area, high=max_heating_area) 
    percentage_by_types = np.random.random(size=4)
    if one_type_per_subsation:
        i = percentage_by_types.argmax()
        for j in range(len(percentage_by_types)):
            if j != i:
                percentage_by_types[j] = 0
                
    percentage_by_types /= np.sum(percentage_by_types)

    dict_values['COM'] = {'percentage': percentage_by_types[0]} # 100 - 5000
    dict_values['MFH'] = {'percentage': percentage_by_types[1]} # 200 - 1500
    dict_values['SFH'] = {'percentage': percentage_by_types[2]} # 100 - 200
    dict_values['APPRT'] = {'percentage': percentage_by_types[3]} # 9*70 - 50*100
    
    dpe_classes_probabilities = {}
    dpe_classes_names = {}
    
    for key in dict_values.keys():
        dpe_classes = distribution_classes_dpe[key].keys()
        dpe_classes_prob = np.array([float(val) for val in distribution_classes_dpe[key].values()])
        dpe_classes_prob /= np.sum(dpe_classes_prob)
        dpe_classes_probabilities[key] = dpe_classes_prob
        dpe_classes_names[key] = dpe_classes

    for key in dict_values.keys():
        if verbose != 0:
            print(f"{dict_values[key]['percentage'] *100:.2f} % of {key}")
        dict_values[key]['heating_area'] = dict_values[key]['percentage'] * heating_surface_area
        dpe_classes = dpe_classes_names[key]
        dpe_classes_prob = dpe_classes_probabilities[key]
        class_dpe = list(dpe_classes)[np.random.choice(range(len(dpe_classes)), p=dpe_classes_prob)]
        dict_values[key]['class_dpe'] = class_dpe
        dict_values[key]['mean_E'] = generate_uniform_value_in_dpe(class_dpe) * dict_values[key]['heating_area'] # kWh/year
        integrated_profiles = sum(heating_profiles[key]) # of the year
        
        # integral (profile x Factor) = mean energy over the year
        dict_values[key]['profile_factor'] = dict_values[key]['mean_E'] / integrated_profiles # profile factor is in fact in kW
        
        # total heating demand
        dict_values[key]['total_heating_demand'] = dict_values[key]['profile_factor'] * heating_profiles[key]
        
    dict_values['total_heating_demand'] = dict_values['COM']['total_heating_demand'] + dict_values['MFH']['total_heating_demand'] + dict_values['SFH']['total_heating_demand']
    return dict_values

def _generate_heating_demands_from_fixed_areas_per_building_types(verbose=0) -> dict:
    """Generates heating demand profile for a substation. Each building type has its pre-selected own heating area.

    Args:
        verbose (int, optional): Verbosity. Defaults to 0.

    Returns:
        dict: dictionary containing the heating area of each type, profile factors and heating demands of the substation
    """
    heating_profiles = pd.read_csv(os.path.join('src', 'files', 'heating_demands_profiles.csv'))
    
    dict_values = {}
    total_area = 0
    for key in area_building_types.keys():
        values = area_building_types[key]
        dict_values[key] = {}
        dict_values[key]['heating_area'] = np.random.uniform(low=values[0], high=values[1])
        total_area += dict_values[key]['heating_area']
        
    dpe_classes_probabilities = {}
    dpe_classes_names = {}
    
    for key in dict_values.keys():
        dpe_classes = distribution_classes_dpe[key].keys()
        dpe_classes_prob = np.array([float(val) for val in distribution_classes_dpe[key].values()])
        dpe_classes_prob /= np.sum(dpe_classes_prob)
        dpe_classes_probabilities[key] = dpe_classes_prob
        dpe_classes_names[key] = dpe_classes

    for key in dict_values.keys():
        dpe_classes = dpe_classes_names[key]
        dpe_classes_prob = dpe_classes_probabilities[key]
        class_dpe = list(dpe_classes)[np.random.choice(range(len(dpe_classes)), p=dpe_classes_prob)]
        dict_values[key]['class_dpe'] = class_dpe
        dict_values[key]['mean_E'] = generate_uniform_value_in_dpe(class_dpe) * dict_values[key]['heating_area'] # kWh/year
        integrated_profiles = sum(heating_profiles[key]) # of the year
        
        # integral (profile x Factor) = mean energy over the year
        dict_values[key]['profile_factor'] = dict_values[key]['mean_E'] / integrated_profiles # profile factor is in fact in kW
        
        # total heating demand
        dict_values[key]['total_heating_demand'] = dict_values[key]['profile_factor'] * heating_profiles[key] + 5.0 # avoid 0 W demands
        
        dict_values[key]['percentage'] = (dict_values[key]['heating_area'] / total_area)
        
    dict_values['total_heating_demand'] = dict_values['COM']['total_heating_demand'] + dict_values['MFH']['total_heating_demand'] + dict_values['SFH']['total_heating_demand']
    return dict_values

def generate_substation_demands(choice_heating_area, verbose=0, one_type_per_subsation=False) -> dict:
    """Generate a substation heating demand evolution over a year

    Args:
        choice_generation (int): 0 for percentage of total fixed heating area and 1 for random heating area per building type
        verbose (int, default=0): 0 no print, 1 print different consumer categories contributions
        one_type_per_subsation(bool, default=False): If True, use only one consumption type per substation otherwise use combinaisions of 3 categories
        
    Returns:
        dict: substation heating demand including ['total_heating_demand' of COM, MFH and SFH]
    """
    
    dict_values = {}
    
    # two choices here
    if choice_heating_area == 1:
        # 1 - We fix total heating area and each building type has its percentage selected randomly
        dict_values = _generate_heating_demands_from_percentage_of_total_areas()
    else:
        # 2 - We have heating areas per building type
        dict_values = _generate_heating_demands_from_fixed_areas_per_building_types()

    return dict_values

def get_json_serializable_information(dict_values):
    """Gets only the json serializable information form the subsation dict values, other values can be obtained from these valeus

    Args:
        dict_values (dict): the substation dict values

    Returns:
        dict: dict of json serializable information
    """
    dict_ = {}
    json_serializable_keys = ['heating_area', 'class_dpe', 'percentage', 'mean_E']
    for key in ['COM', 'MFH', 'SFH']:
        dict_[key] = {}
        for key_ in json_serializable_keys:
            dict_[key][key_] = dict_values[key][key_]
    return dict_
   