
class GraphGeneratorParameters():
    """Class containing the control parameters of the DHN generator
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
