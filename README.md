This project developed during Ph.D work contains synthetic District Heating Networks generator models referred to as **SyntheticDHN**. More precisely, it contains a graph generator model and a heating demands profiles model.

# SyntheticDHN

SyntheticDHN is a complete synthetic DHN generator which we believe can be important for users and researchers and we believe may be first step to generate benchmarks DHN as in IEEE for electrical grid. This software uses Graph theory approach combined to the node method to generate plausible DHN's layouts incoroporating some expertise based constraints. The nodes are then randomly selected to be substations or junction nodes. Substation nodes are assigned synthetic but realistic heating demands profiles (for one year) using France's ADEME [open access data](https://data-transitions2050.ademe.fr/).

## **Graph generator model**

The graph generator is a *constrained* random graph generator model. The whole concept of this model is to generate a random graph mimicking the topology of the real-world District Heating Network's topology in terms of nodes degrees distribution, maximal nodes degree and connectivity.

For more control purpose, this model does not use established random generator model but generates graph from scratch using a *recursive nodes adding approach*. Based on the target number of nodes and maximal degree, at each step, a new node is created and randomly connected to previously created nodes.

Once the graph is created, the display on a 2D space necessites an optimization approach in order to disperse effectively the nodes on the 2D grid. We rely on improved version of the *Kamada-Kawai* cost-function graph layout [[link](https://arxiv.org/pdf/1508.05312)].

### Expertise based constraints

Contraints applied on the DHN's layouts are based on expertise point of view. For instance, a maximal degree of 4 is applied to all nodes with tree-like layout. Loops are added in post-processing to mimic thermal network's looping pipes using statistical assumptions. Also, loop of 3 nodes (*i.e.*, triangle cliques) are discarded as they are physically unlikely. We note that the proposed software allows the user to change all of these parameters.

Additionally, expertise knowledge suggests that the DHN are subdivied into internal regions or subregions which we capture by generating the overall network as ensemble of sub-DHNs. Connections between these subregions are randomly applied. These constitute hyperparameters that the users can adapt as desired.

### Recursie nodes adding approach

This approach has been considered to give high flexibility about the generation of the layouts of the DHN instead of using some established random graph generator approaches. Indeed, our proposed approach generates the DHN as graph by recursively adding nodes and connecting the new nodes to previously added nodes. Doing, limiting connections and number of formed nodes become more effectively.

## **Heating demands model**

Two heating demands models have been developed during this thesis. 

#### Heating law

First model uses a modified heating law approach. In this case, a substation node heating demand is directly proportional to outdoor temperature with a scaling factor provided by the heating area and the efficiency coefficient of the substation heat exchanger. *Nantes* real outdoor temperatures of the year 2022 are used in our experiment.

Conceptually, we generate the heating demands using the following steps:

- Randomly select heating area and heat exchanger efficiency coefficient [*minArea*, *maxArea*]
- Retrieve outdoor temperatures of Nantes 
- Creates the heating demands profile for the year using the simple formula of D = U x (T - Tref) where Tref is a threshold temperature fixed at 18°C

*minArea*, *maxArea* and *U* factors are users inputs.

#### DPE data based

In the second model, we try to mimic further the distribution of buildings consumption in France during the year 2022. Real *DPE* data provided by the French goverment and made publicly avaiable are used to evaluate the distribution of DPE classes within 4 types of buildings which are commercial use (COM), multi-family house (MFH), single-family house (SFH) and appartments (APPRT). 

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

This project only uses publicly available packages which makes the replication and contribution easier. To install all required packages, enter the following line commands at the project source folder

```bash
python -m pip install -r requirements.txt
``` 

# License

The replication and use of codes, images, files, and data in this project are protected under the [European Union Public Licence (EUPL) v1.2](https://joinup.ec.europa.eu/page/eupl-text-11-12).
For more information see [LICENSE](LICENSE).


# Contributions

This project humbly tries to propose a synthetic DHN generator using expertise-knowledge and graph theories. We recognise that many parts can be improved and we welcome all interested contributors from the community. 

Please contact us at dubon.rodrigue@imt-atlantique.fr.
