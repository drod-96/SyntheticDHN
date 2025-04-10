This project, developed as part of a Ph.D. research, provides synthetic District Heating Network (DHN) generator models under the name **SyntheticDHN**. It includes a graph-based network generator as well as a model for generating realistic heating demand profiles.

# SyntheticDHN

SyntheticDHN is a comprehensive synthetic 3rd Generation District Heating Network (3GDHN) generator. We believe it can be a valuable tool for both users and researchers, potentially serving as a first step toward establishing standardized DHN benchmarks—similar to the IEEE benchmarks used in power systems. The software employs a graph theory-based approach combined with the node method to generate plausible DHN layouts, incorporating domain-specific constraints. Nodes are randomly designated as either substations or junction points. Substation nodes are then assigned synthetic, yet realistic, year-long heating demand profiles based on data from France's ADEME [open access data](https://data-transitions2050.ademe.fr/).

## **Graph generator model**

The graph generator is a constrained random graph model designed to emulate the topology of real-world District Heating Networks (DHNs). Its goal is to reproduce key structural properties, such as node degree distribution, maximum node degree, and overall network connectivity. To maintain greater control over the generated topology, this model does not rely on standard *random graph generators*. Instead, it builds the network from scratch using a designed **recursive nodes adding approach**. Given a target number of nodes and a maximum degree, nodes are added one by one and randomly connected to previously created nodes, while respecting the specified constraints.

Once the graph structure is complete, it must be laid out in a 2D space for visualization. This requires an optimization process to effectively distribute the nodes following a tree-like layout. For this purpose, we use an improved version of the *Kamada-Kawai* cost-function [layout algorithm](https://arxiv.org/pdf/1508.05312).

### Expertise-based constraints

The constraints applied to the DHN layouts apply domain expertises. For example, a maximum node degree of 4 is enforced to reflect the tree-like structure commonly observed in real-world networks. Loops are introduced during a post-processing step to emulate the presence of thermal looping pipes, following statistical assumptions. Triangular loops (i.e., 3-node cliques) are excluded, as they are considered physically unrealistic in this context.

Expert knowledge also indicates that DHNs are often subdivided into internal regions or sub-networks. This characteristic is captured in the model by generating the overall network as an ensemble of sub-DHNs, with interconnections between them created randomly. These inter-subregion links, as well as the number and placement of heat sources (ranging from 0 to 2 per subregion), are treated as hyperparameters.

Importantly, all of these parameters are user-configurable, allowing for flexible adaptation to different requirements.

### Recursie nodes adding approach

This approach was chosen to provide greater flexibility in generating DHN layouts, compared to using standard random graph generation methods. Instead of relying on pre-defined models, our method constructs the DHN graph by recursively adding nodes and connecting each new node to previously created ones.

This recursive process allows for finer control over the network structure—particularly in limiting the number of connections per node and managing the overall growth of the graph.

## **Heating demands model**

Two heating demands models have been developed and incorporated in this project. We note that heating demands include both space heating and hot water domestic demands.

#### Heating law

First model uses a modified heating law approach. In this case, a substation node's heating demand is directly proportional to outdoor temperature with a scaling factor provided by the heating area and the efficiency coefficient of the substation heat exchanger. *Nantes* real outdoor temperatures of the year 2022 are used in our experiment.

Conceptually, we generate the heating demands using the following steps:

- Randomly select heating area and heat exchanger efficiency coefficient [*minArea*, *maxArea*]
- Retrieve outdoor temperatures of Nantes 
- Creates the heating demands profile for the year using the following heating law formula where Tref is a threshold temperature fixed at 18°C, U the heat exchange coefficient and A the exchange area of the substaion

$$D = A . U . (T - Tref) $$

*minArea*, *maxArea* and *U* factors are users inputs.

#### DPE data based

In the second model, we aim to more accurately replicate the distribution of building energy consumption in France for the year 2022. To achieve this, we utilize real DPE (Diagnostic de Performance Énergétique) data provided by the French government, which is publicly available. This data is used to assess the distribution of *DPE* classes across four main building types: commercial buildings (COM), multi-family houses (MFH), single-family houses (SFH), and apartments (APPRT).

Conceptually, we generate the heating demands using the following steps:

- Select the percentage and heating area of each building type within the substation
- Randomly select the DPE class based on know french building distributions
- Randomly select the energy consumption value based on the DPE class of each building type
- Creates the heating demands profile for the year based on know heating demands profiles

ADEME data can be retrieved from the ADEME [website](https://data-transitions2050.ademe.fr/).

To generate the heating demands profiles, this work relies on profiles data from the work of [Ruhnau, O. and Muessel, J., When2Heat Heating Profiles. Open Power System Data, 2023](https://doi.org/10.25832/when2heat/2023-07-27)

# Usability

We propose a notebook file *main.ipynb* illustrating how to generate a random DHN and nodes heating demands. All code sources can be found in the folder *src*. We also note that this repository uses only publicly available data including Nantes outdoor temperatures, DPE classes range of consumption powers and class distribution taken from DPE data. DPE data files are not available in this repository but can be found on the ADEME [[link](https://www.ademe.fr/)] website. For more information, please refer to contact section. 

Some examples of generated DHN-like graphs:

![Sample DHN-1](https://github.com/drod-96/synthetic_dhn_model/blob/main/Images/output_dhn_test_1.png?raw=true)

![Sample DHN-2](https://github.com/drod-96/synthetic_dhn_model/blob/main/Images/output_dhn_test_3.png?raw=true)


# Python packages

This project only uses publicly available packages and data which makes the reproduction and contribution easier. To install all required packages, enter the following line commands at the project source folder

```bash
python -m pip install -r requirements.txt
``` 

# License

The replication and use of codes, images, files, and data in this project are protected under the [European Union Public Licence (EUPL) v1.2](https://joinup.ec.europa.eu/page/eupl-text-11-12).
For more information see [LICENSE](LICENSE).


# Contributions

This project humbly tries to propose a synthetic DHN generator using expertise-knowledge and graph theories. We recognize that many parts can be improved and we welcome all contributions from the community. 

Please contact us at dubon.rodrigue@imt-atlantique.fr.

# Next version ...

A future version of this approach will introduce an additional step to dimension the network pipes based on the spatial distribution of heat producers, as well as the location and heating demand levels of the substations.
