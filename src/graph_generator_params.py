import sys
sys.path.insert(0, r'D:\PhD DATA\Codes & Works\SyntheticDHN\SyntheticDHN\src')


class GraphGeneratorParameters():
    """Class containing the control parameters of the DHN generator. It englobes all the necessary control parameters of the graph generator.
    We note that all defined parameters are publicly settable and gettable within this class.


    Attributes:
        E_cp (float): Probability value of having center producer of the overall DHN (default = 0.5)
        E_rp (float): Probability value of having producer(s) within a generated region (default = 0.2)
        E_ee (float): Probability value of edges between generated regions. It controls the connectivity between the regions (default = 0.1)
        nb_nodes_per_region (int): Number of nodes (or size) of each generated region (default = 100)
        nb_regions (int): Number of regions to generate (default = 4)
        max_diameter (int): Maximal diameter of the DHN, measured in hop-distances (default = 12)
        min_cycle_length (int): Minimum size of acceptable cycles (default = 3). Any cycle with number of edges below this threshold will be broken.
        target_ratio (float): Targeted ratio of #Edges/#Nodes
        min_distance_bt_producers (int): Minimum distance between two distributed heat producers within the DHN, measured in hop-distance (default = 3)
        nb_producers_to_reach (int): Number of heat producers to reach wihin the DHN, we note that it can be not achieved (default = 3)
        edge_weight_mean (float): Mean of the normal distribution used to generate the edges' weights (default = 1.5)
        edge_weight_std (flaot): Standard deviation of the normal distribution used to generate the edges' weights (default = 0.2)


    """
    def __init__(self, 
                 E_cp = 0.5, # Probability of having central producer
                 E_rp = 0.2, # Probability of having producer per region
                 E_ee = 0.1, # Probability of having edges between regions
                 nb_nodes_per_region = 100,
                 nb_regions = 4,
                 max_diameter = 12,
                 min_cycle_length = 3,
                 target_ratio = 1.01,
                 min_distance_bt_producers = 3,
                 nb_producers_to_reach = 3,
                 edge_weight_mean = 1.5,
                 edge_weight_std = 0.2):
        """ Initializes the GraphGeneratorParameters
        
        Args:
            E_cp (float): Probability value of having center producer of the overall DHN (default = 0.5)
            E_rp (float): Probability value of having producer(s) within a generated region (default = 0.2)
            E_ee (float): Probability value of edges between generated regions. It controls the connectivity between the regions (default = 0.1)
            nb_nodes_per_region (int): Number of nodes (or size) of each generated region (default = 100)
            nb_regions (int): Number of regions to generate (default = 4)
            max_diameter (int): Maximal diameter of the DHN, measured in hop-distances (default = 12)
            min_cycle_length (int): Minimum size of acceptable cycles (default = 3). Any cycle with number of edges below this threshold will be broken.
            target_ratio (float): Targeted ratio of #Edges/#Nodes
            min_distance_bt_producers (int): Minimum distance between two distributed heat producers within the DHN, measured in hop-distance (default = 3)
            nb_producers_to_reach (int): Number of heat producers to reach wihin the DHN, we note that it can be not achieved (default = 3)
            edge_weight_mean (float): Mean of the normal distribution used to generate the edges' weights (default = 1.5)
            edge_weight_std (flaot): Standard deviation of the normal distribution used to generate the edges' weights (default = 0.2)s
        """
        
        self.E_central_producer = E_cp
        self.E_region_produce = E_rp
        self.E_bt_regions_pipes = E_ee
        self.max_degree = 3
        self.jump_node_numm = 1
        self.max_diameter = max_diameter
        self.start_node_num = 0
        self.min_cycle_length = min_cycle_length
        self.nb_nodes_per_region = nb_nodes_per_region
        self.nb_regions = nb_regions
        self.target_ratio = target_ratio
        self.min_distance_bt_producers = min_distance_bt_producers
        self.edge_weight_mean = edge_weight_mean
        self.edge_weight_std = edge_weight_std
        self.number_producers = nb_producers_to_reach
