import matplotlib.pyplot as plt
from random import random
import networkx as nx
import numpy as np
from itertools import product
import pandas as pd
import os
from src.constants import *
from src.graph_generator_params import GraphGeneratorParameters
 
class GraphDHNGenerator(object):
    """Random DHN graph generator object
    """
    
    def __init__(self, control_params: GraphGeneratorParameters = None, verbose=1):
        if control_params == None:
            control_params = GraphGeneratorParameters()
        self.params = control_params
        self.graph = nx.DiGraph()
        self.producer_indices = []
        self.node_colors = []
        self.node_indices = []
        self.node_positions = []
        self.verbose = verbose
        
    def _generate_random_weight(self):
        mean = self.params.edge_weight_mean
        std = self.params.edge_weight_std
        weight = np.random.default_rng().normal(mean, std)
        if weight <= 0:
            weight = self.params.edge_weight_mean / 2.0
        return weight
    
    def _check_for_short_cycles(self, G:nx.Graph):
        G_to_use = G.copy()
        short_cycles = self._get_short_cycles(G_to_use)
        print(f"Found cycles = {short_cycles}")
        for cycle in short_cycles:
            # cycle is a tuple of pair nodes (ex: [(69, 68), (68, 70), (70, 69)])
            if self.verbose == 1:
                print(f"Treating the cycle {cycle}")
            for (u, v) in cycle:
                g = G_to_use.copy()
                try:
                    g.remove_edge(u, v) # edge (u,v) may have been deleted previously from an other loop
                    if nx.is_connected(g):
                        G_to_use = g.copy()
                        if self.verbose == 1:
                            print(f"Edge ({u},{v}) removed")
                        break
                except Exception as ex:
                    pass
                
        return G_to_use
    
    def _get_short_cycles(self, G:nx.Graph):
        short_cycles = []
        try:
            cycles = {}
            for n in list(G.nodes()):
                cl = nx.find_cycle(G, source=n)
                key = f'{cl[0][0]}_{cl[0][1]}'
                cycles[key] = cl
                
            for cl in cycles:
                cycle_tuple_list = list(cycles[cl])
                if len(cycle_tuple_list) <= self.params.min_cycle_length:
                    short_cycles.append(cycle_tuple_list)
                    print(f"cycle found {cycle_tuple_list}")
        except Exception:
            pass
        
        return short_cycles

    def _remove_self_loop(self, G: nx.Graph()):
        for (u, v) in iter(nx.selfloop_edges(G)):
            G.remove_edge(u, v)
        return G

    def _generate_random_graph(self, G, remaining_nodes, jump_node_num, max_degree, node_num):
        if not remaining_nodes:
            return G
        current_node = node_num
        for _ in range(np.random.randint(1, max_degree)):
            try:
                neighbor = np.random.choice(remaining_nodes)
                G.add_edge(current_node, neighbor, weight=self._generate_random_weight())
                remaining_nodes.remove(neighbor)
            except Exception:
                break
        
        n = node_num + jump_node_num
        self._generate_random_graph(G, remaining_nodes, jump_node_num, max_degree, n)

    def _generate_region_graph(self, center, n):
        max_degree = self.params.max_degree
        jump_nd = self.params.jump_node_numm
        max_diameter = self.params.max_diameter
        
        G = nx.Graph()
        remaining_nodes = list(range(n))
        # Generate the random graph
        self._generate_random_graph(G, remaining_nodes, jump_nd, max_degree, 0)
        
        while not nx.is_connected(G):
            node1 = np.random.choice(list(G.nodes()))
            node2 = np.random.choice(list(G.nodes()))
            if G.degree(node1) >= max_degree or G.degree(node2) >= max_degree or node1 == node2:
                continue
            else:
                G.add_edge(node1, node2)

        for e in iter(nx.selfloop_edges(G)):
            G.remove_edge(e[0], e[1])

        # Ensure that the graph has the desired diameter
        it = 0
        # while nx.diameter(G) < max_diameter and it < 100:
        #     node1 = np.random.choice(list(G.nodes()))
        #     node2 = np.random.choice(list(G.nodes()))
        #     G.add_edge(node1, node2)
        #     it+=1
        
        pos = nx.kamada_kawai_layout(G, center=center)
        return G, pos

    def generate_random_region_with_target(self, center):
        params = self.params
        nb = params.nb_nodes_per_region
        ratio = 100
        G = nx.Graph()
        # if nb < 60:
        #     print('Minimumn number of nodes is 60')
        #     nb = 60
        
        G, pos = self._generate_region_graph(center, nb)
        ratio = G.number_of_edges() / (G.number_of_nodes() - 1)
        iterr = 0
        while np.abs(ratio - params.target_ratio) > 1e-1 and iterr <= 100:
            G, pos = self._generate_region_graph(center, nb)
            # if ratio > params.target_ratio:
            #     # recreer un autre graph
            #     # TODO: Remove some edges
            #     G, pos = self._generate_region_graph(center, nb)
            # else:
            #     node1 = np.random.choice(list(G.nodes()))
            #     node2 = np.random.choice([item for item in list(G.nodes()) if item != node1])
            #     G.add_edge(node1, node2)
            G = self._remove_self_loop(G)
            ratio = G.number_of_edges() / (G.number_of_nodes() -1)
            iterr += 1
        # print(f'Ratio (E/V) = {ratio}')
        return G
    
    def generate_random_dhn(self):
        params = self.params
        center_coordinates_of_trees = [[-1, -1], [1, 1], [-1, 1],[2, 1],[1,2]]
        
        ## OUTPUT Varibales
        node_colors = [] # Color of nodes
        labels = {} # Label of nodes
        positions = [] # Spatial coordinates of nodes
        producers = [] # Producer units indices
        
        initial_pos = 0
        labels_per_graphs = {}    
        
        ## GENERATION PROCESS
        if len(node_colors) != 0:
            node_colors = [] # Color of nodes
            labels = {} # Label of nodes
            positions = [] # Spatial coordinates of nodes
            producers = [] # Producer units indices
            labels_per_graphs = {}

        add_central_chp_producer = random() < params.E_central_producer # Un producteur central

        # Main graph for DHN
        u_graph = nx.Graph()

        if add_central_chp_producer:
            labels[0] = str(0)
            u_graph.add_node(0)
            positions.append(np.array([np.random.uniform(-1,2), np.random.uniform(-1,2)], dtype=float))
            node_colors.append('tab:red')
            producers.append(0)
            
        count_graph = 0
        ii = 0
        print('Generating each region ...')
        while count_graph < params.nb_regions:
            print(f'\tRegion {count_graph+1} ...')
            if count_graph == len(center_coordinates_of_trees):
                ii = 0
            center_position_of_tree = center_coordinates_of_trees[ii]
            ii+=1
            last_nd = u_graph.number_of_nodes()
            div_coordinate = np.array(center_position_of_tree, dtype=float)

            G = self.generate_random_region_with_target(div_coordinate)
            pos = nx.kamada_kawai_layout(G, center=2*div_coordinate, scale=2)
            
            starting_label = last_nd
            # print(f'Starting label = {starting_label}')
            # We add distributed source even with central big CHP
            if count_graph != 0 and np.random.uniform(0, 1) < params.E_region_produce and len(producers) < self.params.number_producers:
                producer_idx = np.random.randint(starting_label, starting_label + G.number_of_nodes()) # Chose one to be supplier
                producers.append(producer_idx)
            
            # Probability of having producer
            # if not add_central_chp_producer and count_graph == 0:
            #     e_rb = 1
            # else:
            #     e_rb = params.E_region_produce
            
            for n in pos:
                positions.append(pos[n])
                node_lab = n + starting_label
                labels[node_lab] = str(node_lab)
                if count_graph not in labels_per_graphs:
                    labels_per_graphs[count_graph] = []
                labels_per_graphs[count_graph].append(node_lab)
                
                if node_lab in producers:
                    node_colors.append('tab:red')
                else:
                    node_colors.append('tab:blue')
            
            u_graph = nx.disjoint_union(u_graph, G)
            if add_central_chp_producer:
                ts = np.random.choice(list(G.nodes()))
                u_graph.add_edge(0, int(ts)+starting_label, weight=self._generate_random_weight())
            else:
                if count_graph != 0:
                    id_othr_graph = np.random.choice(labels_per_graphs[count_graph])
                    if count_graph == 1:
                        id_prev_graph = np.random.choice(labels_per_graphs[0])
                    else:
                        id_prev_graph = np.random.choice(labels_per_graphs[np.random.randint(0,count_graph-1)])
                    u_graph.add_edge(id_othr_graph, id_prev_graph, weight=self._generate_random_weight())  
            
            count_graph += 1  
        
        # Verify the number of sources
        while len(producers) <= self.params.number_producers:
            producer_idx = np.random.randint(0, len(labels)-1) # Select a number of source
            if producer_idx not in producers:
                producers.append(producer_idx)
        
        it = 0
        looping = False
        print('Loop --> adding edges between regions')
        while not looping and it < 10:
            # Random edges connections
            for gi in range(count_graph-1): # Count - 1 = number total
                for gj in range(gi+1, count_graph-1):
                    if np.random.uniform() <= params.E_bt_regions_pipes:
                        u = np.random.choice(labels_per_graphs[gi])
                        v = np.random.choice(labels_per_graphs[gj])
                        if u != v and not u_graph.has_edge(u, v):
                            u_graph.add_edge(u, v)
            looping = nx.is_connected(u_graph)
            it+=1

        print('\t --> finished')
        poss = nx.kamada_kawai_layout(u_graph, scale=10, dim=2, weight='weight')
        if nx.is_connected(u_graph):
            close_producers = []
            for i in range(len(producers)):
                prd = producers[i]
                for j in range(i+1, len(producers)):
                    prdx = producers[j]
                    if nx.shortest_path_length(u_graph, prd, prdx) < params.min_distance_bt_producers:
                        if [prd, prdx] in close_producers or [prdx, prd] in close_producers:
                            continue
                        close_producers.append([prd, prdx])
            
            for [id1, id2] in close_producers:
                node_colors[id2] = 'tab:blue'
                if id2 in producers:
                    producers.remove(id2)
                    
            # print('Close producers = ',close_producers)
            # print('Diameter = ',nx.diameter(u_graph))
            # print('Ratio (E/V) total =',u_graph.number_of_edges() / (u_graph.number_of_nodes() -1))
            u_graph = self._check_for_short_cycles(u_graph)
            self.graph = u_graph
            self.node_colors = node_colors
            self.node_indices = labels
            self.node_positions = poss
            self.producer_indices = producers
            print('DHN-based graph generated !')
            self.plot_district_heating_network()
            return True
        else:
            print('WARNING!!!! NOT CONNECTED GRAPH !! GENERATE AGAIN')
            return False
    
    def read_generated_graph(self, excel_file_topology: str, plot_graph=True):
        # utiliser "expand graph" pour visualiser graph
        excel_data = pd.read_excel(excel_file_topology, sheet_name=['nodes', 'pipes'])
        df_nodes = excel_data['nodes']
        df_pipes = excel_data['pipes']
        n_nodes = len(df_nodes)
        n_pipes = len(df_pipes)
        node_colors = []
        labels = {}
        producer_indices = []
        positions = np.zeros(shape=(n_nodes, 2), dtype=float)
        adjacency_matrix = np.zeros(shape=(n_nodes, n_nodes), dtype=int)
        for n in range(n_nodes):
            positions[n] = np.array([df_nodes.iloc[n]['x'],df_nodes.iloc[n]['y']])
            labels[n] = n
            if df_nodes.iloc[n]['Is source'] == 1:
                node_colors.append('tab:red')
                producer_indices.append(n)
            else:
                node_colors.append('tab:blue')
            
        for indx, row in df_pipes.iterrows():
            st = int(row['start node']) - 1
            ed = int(row['end node']) - 1
            adjacency_matrix[st, ed] = 1
            adjacency_matrix[ed, st] = 1

        self.graph = nx.from_numpy_array(adjacency_matrix)
        self.producer_indices = producer_indices
        self.node_colors = node_colors
        self.node_indices = labels
        self.node_positions = positions
        
        if plot_graph:
            self.plot_district_heating_network()
    
    def plot_district_heating_network(self):
        plt.figure(figsize=(42,40))
        nx.draw(self.graph, pos=self.node_positions, labels=self.node_indices, node_color=self.node_colors, node_size=200, font_size=12, font_color="black")
        plt.show()
    
    def generate_random_connected_dhn(self):
        is_generated = False
        while not is_generated:
            is_generated = self.generate_random_dhn()