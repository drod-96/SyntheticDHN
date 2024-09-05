from src.graph_generator import GraphDHNGenerator
from src.demands_model_dpe import generate_substation_demands, get_json_serializable_information

import networkx as nx 
import os
import pandas as pd
import numpy as np

RECENT_BUILDING_U = 0.84 # W.K^1.m^-2
ANCIENT_BUILDING_U = 3.4
OFFICE_BUILDING_U = 2.5

class DHNTopology(object):
    """This class contains the DHN graph generated, the topology information and the heating demands of the nodes
    """
    
    def __init__(self, 
                 dhn_graph: GraphDHNGenerator = None, 
                 graph_folder_name: str = "Generated_DHN", 
                 heating_demand_model=2, 
                 dpe_model_demand_version=1, # used only if the heating demand model is DPE (version 2), more information see demands_model_dpe.py
                 max_h=4, 
                 max_d=0.5, 
                 min_d=0.05):
        """Initializes the class and creates the topology excel file directly 

        Args:
            dhn_graph (GraphDHNGenerator, optional): the DHN graph generator. Defaults to None.
            graph_folder_name (str, optional): the folder name of the graph. Defaults to "Generated_DHN".
            heating_demand_model (int, optional): the heating demand model version to use. If 1 use heating law model, else if it is 2 use the DPE based model. Defaults to 2.
            dpe_model_demand_version (int, optional): the DPE based model version to use, only used if the DPE based model is selected. Defaults to 1. Further information, refer to DPE model
            max_d (float, optional): max diameter value of the pipes (m). Defaults to 0.5.
            min_d (float, optional): min diameter value of the pipes (m). Defaults to 0.5.
            max_h (float, optional): max convective coefficient of the pipes with minimum value 0.8. Defaults to 4.
        """
        
        self._dhn_name = os.path.join('Synthetic_DHNs', graph_folder_name)
        self._dhn_graph = dhn_graph
        self._nodes_positions = [] # contains nodes sheet information [nbr, x, y, is_prod]
        self._pipes_properties = [] # contains pipes sheet information [start node, end node, Diameter, h, length] # Diameter may be changed from dimensioning
        self._outdoor_temperature = dict() # Outdoor temperatures, important only for demands so far
        self._substations_informations = dict()
        self._loads = dict() # contains loads sheet information demands of each substation over the time
        self._heating_demand_version = heating_demand_model
        self._dpe_model_version = 1
        
        self.max_convective_coefficient = max_h
        self.min_convective_coefficient = 0.8
        self.min_diameter = min_d
        self.max_diameter = max_d
        
        self._fill_dhn_information()
        self._generate_heating_demands()
        
    def _check_not_empty_graph(self):
        """Checks if the DHN graph is not empty

        Returns:
            bool: true if not empty false otherwise
        """
        return self._dhn_graph != None
    
    def _generate_nodes_positions_with_excel_sheet(self, writer_excel):
        """Generates the information about the nodes positions and which among them the sources

        Args:
            writer_excel : excel writer
        """
        node_indices = self._dhn_graph.node_indices
        node_positions = self._dhn_graph.node_positions
        producer_indices = self._dhn_graph.producer_indices
        
        indices = [int(item) for item in self._dhn_graph.node_indices]
        sorted_indices = indices.copy()
        sorted_indices.sort()
        
        nodes_data_dict = []
        for i in sorted_indices:
            is_prod = 1 if (i) in self._dhn_graph.producer_indices else 0 
            nodes_data_dict.append({
                'Node': i+1, # in Julia it is base 1
                'x': node_positions[i][0],
                'y': node_positions[i][1],
                'Is source': is_prod
            })
        
        self._nodes_positions = nodes_data_dict
        # pandas used to generate excel sheet
        # Create a Pandas Excel writer using XlsxWriter as the engine.
        df_ = pd.DataFrame.from_dict(nodes_data_dict)
        df_.to_excel(writer_excel, sheet_name='nodes', index=False, index_label=False)
        
    def _generate_pipes_properties_with_excel_sheet(self, writer_excel):
        """Generates the information about the pipes

        Args:
            writer_excel : excel writer
        """
        
        node_indices = self._dhn_graph.node_indices
        node_positions = self._dhn_graph.node_positions
        producer_indices = self._dhn_graph.producer_indices
        g = self._dhn_graph.graph
        
        pipes_metadata = []
        for pipe in g.edges():
            (start_node, end_node) = pipe
            length = np.linalg.norm(np.array(node_positions[start_node]) - np.array(node_positions[end_node]))
            h = np.random.uniform(self.min_convective_coefficient, self.max_convective_coefficient)
            diameter = np.random.uniform(self.min_diameter, self.max_diameter)
            pipes_metadata.append({
                'start node': start_node + 1,
                'end node': end_node + 1,
                'Diameter': diameter,
                'h': h,
                'length': length
            })
        
        self._pipes_properties = pipes_metadata
        df_ = pd.DataFrame.from_dict(pipes_metadata)
        df_.to_excel(writer_excel, sheet_name='pipes', index=False, index_label=False)
        
    def _generate_loads_model_dpe(self, writer_excel):
        """Generates heating demands of the nodes based on DPE distribution model

        Args:
            writer_excel : excel writer
        """
        
        # This demands model uses the DPE France distribution knowledge. Further information is detailed in "Demands models"
        labels = [int(item)+1 for item in self._dhn_graph.node_indices]
        sorted_labels = labels.copy()
        sorted_labels.sort()
        dict_substations_heating_areas = []
        dict_substations_dpe_class = []
        dict_heating_profiles = {}
        
        for node in sorted_labels:
            dict_values = generate_substation_demands(self._dpe_model_version, verbose=0, one_type_per_subsation=False) # can be changed if necessary
            substation_heating_area_distribution = {
                'node': node,
                'COM(%)': dict_values['COM']['percentage'] * 100,
                'MFH(%)': dict_values['MFH']['percentage'] * 100,
                'SFH(%)': dict_values['SFH']['percentage'] * 100,
                'APPRT(%)': dict_values['APPRT']['percentage'] * 100,
                'Total area(m2)': dict_values['COM']['percentage'] + dict_values['MFH']['heating_area'] + dict_values['SFH']['heating_area'] + dict_values['APPRT']['heating_area']
            }
            dict_substations_heating_areas.append(substation_heating_area_distribution)
            substation_dpe_class = {
                'node': node,
                'COM': dict_values['COM']['class_dpe'],
                'MFH': dict_values['MFH']['class_dpe'],
                'SFH': dict_values['SFH']['class_dpe'],
                'APPRT': dict_values['APPRT']['class_dpe'],
            }
            dict_substations_dpe_class.append(substation_dpe_class)
            
            dict_heating_profiles[node] = dict_values['total_heating_demand']
            
        df_cons = pd.DataFrame.from_dict(dict_substations_heating_areas)
        df_cons.to_excel(writer_excel, sheet_name='consumers(area)', index=False, index_label=False)
        
        df_cons = pd.DataFrame.from_dict(dict_substations_dpe_class)
        df_cons.to_excel(writer_excel, sheet_name='consumers(dpe)', index=False, index_label=False)
        
        df_loads = pd.DataFrame.from_dict(dict_heating_profiles)
        df_loads.to_excel(writer_excel, sheet_name='loads', index=True, index_label=True)
        
        self._loads = df_loads
                
    def _generate_loads_model_heating_law(self, writer_excel):
        """Generates heating demands of the nodes based on heating law model

        Args:
            writer_excel : excel writer
        """
        
        # Ce modèle utilise une loi de chauffe pour estimer la demande
        labels = [int(item)+1 for item in self._dhn_graph.node_indices]
        sorted_labels = labels.copy()
        sorted_labels.sort()
        cons_metadata = []
        df_loads = pd.DataFrame()
        df_nantes_data = pd.read_excel(os.path.join('src', 'files', 'Nantes_Power_load_data.xlsx'), sheet_name=['Data'])['Data']
        temps = np.array(df_nantes_data['T2M'], dtype=float)
        hours = np.array(df_nantes_data['HOUR_STEP'], dtype=int)
        df_loads.insert(loc=0, column='hours', value=hours)
        loads = []
        for n in sorted_labels:
            loads_n = np.ones_like(temps)
            area = 0
            u = 0
            gen_f = 0
            is_space_heating = 0
            is_industrial_heating = 0
            
            is_space_heating = 1
            id = np.random.choice([0, 1, 2])
            area = np.random.uniform(5,12) # Entre 5000-12000m2 de surface d'echange
            if id == 0: # ancient building
                u = np.random.default_rng().normal(ANCIENT_BUILDING_U, 0.1)
            elif id == 1:
                u = np.random.default_rng().normal(RECENT_BUILDING_U, 0.1)
            else:
                u = np.random.default_rng().normal(OFFICE_BUILDING_U, 0.1)
            peak = u*area*1e3*(18+6)
            for t in range(len(loads_n)):
                if temps[t] >= 18.0:
                    loads_n[t] = 0.2*peak
                else:
                    sanitary_shape = np.random.uniform(2,5)*0.1
                    loads_n[t] = u*area*1e3*np.abs(18.0-temps[t]) + sanitary_shape*peak    

            cons_metadata.append([n, area, u, gen_f, is_space_heating, is_industrial_heating])
            loads.append(loads_n * 1e-3) # we use kW for consistency reason
            
        df_cons = pd.DataFrame(cons_metadata, columns=['nbr', 'surface area', 'U factor', 'Gen-factor', 'Space heating', 'Industrial use'])
        nn_loads = pd.DataFrame(np.array(loads).T, columns=sorted_labels)
        df_loads = pd.concat([df_loads, nn_loads], axis=1)
        df_cons.to_excel(writer_excel, sheet_name='consumers', index=False, index_label=False)
        df_loads.to_excel(writer_excel, sheet_name='loads', index=False, index_label=False)
        
        self._loads = df_loads
        
    def _fill_dhn_information(self):
        """Creates the topology excel file and fills the information about the nodes and the pipes  
        """
        if self._check_not_empty_graph():
            
            folder = self._dhn_name
            if not os.path.exists(folder):
                os.mkdir(folder)
            
            excel_file = os.path.join(folder, 'topology.xlsx')

            writer = pd.ExcelWriter(excel_file, engine='openpyxl', mode='w')
            self._generate_nodes_positions_with_excel_sheet(writer)
            self._generate_pipes_properties_with_excel_sheet(writer)
            writer.close()
    
    def _generate_heating_demands(self):
        """Generates heating demands values of the nodes of the DHN generated

        Raises:
            Exception: raise exception if no graph has been created and the topology excel file is not present
        """
        if self._check_not_empty_graph(): 
            excel_file = os.path.join(self._dhn_name, 'topology.xlsx')
            if not os.path.exists(excel_file):
                raise Exception('Excel file not found! Create first excel topology!')
            
            
            writer = pd.ExcelWriter(excel_file, engine='openpyxl', mode='a', if_sheet_exists='replace')
            if self._heating_demand_version == 1:
                self._generate_loads_model_heating_law(writer)
            elif self._heating_demand_version == 2:
                self._generate_loads_model_dpe(writer)
                
            writer.close()
        
    def regenerate_heating_demands(self, model_demand_version: int = 2):
        """Regenerates the heating deùands if the heating model has been changed

        Args:
            model_demand_version (int, optional): the new heating demand model version to use. Defaults to 2.
        """
        if model_demand_version != self._heating_demand_version:
            self._heating_demand_version = model_demand_version
            self._generate_heating_demands()
