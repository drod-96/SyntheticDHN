This project developed during Ph.D work contains synthetic District Heating Networks generator models. More precisely, it contains a graph generator model and a heating demands profiles model.

# DHN generator models

### **Graph generator model**

The graph generator is a *constrained* random graph generator model. The whole concept of this model is to generate a random graph mimicking the topology of the real-world District Heating Network's topology in terms of nodes degrees distribution, maximal nodes degree and connectivity.

For more control purpose, this model does not use established random generator model but generates graph from scratch using a *recursive nodes adding approach*. Based on the target number of nodes and maximal degree, at each step, a new node is created and randomly connected to previously created nodes.

Once the graph is created, the display on a 2D space necessites an optimization approach in order to disperse effectively the nodes on the 2D grid. We rely on the *Kamada-Kawai* cost-function graph layout [[link](https://arxiv.org/pdf/1508.05312)].


### **Heating demands model**

Two heating demands models have been during this thesis. 

#### Heating law

First model uses a modified heating law approach. In this case, a substation node heating demand is directly proportional to outdoor temperature with a scaling factor provided by the heating area and the efficiency coefficient of the substation heat exchanger. *Nantes* real outdoor temperatures of the year 2022 are used in our experiment.

Conceptually, we generate the heating demands using the following steps:

- Randomly select heating area and heat exchanger efficiency coefficient
- Retrieve outdoor temperatures of Nantes 
- Creates the heating demands profile for the year using the simple formula of D = U x (T - Tref) where Tref is a threshold temperature fixed at 18°C

#### DPE data based

In the second model, we try to mimic further the distribution of buildings consumption in France during the year 2022. Real *DPE* data provided by the French goverment and made publicly avaiable are used to evaluate the distribution of DPE classes within 4 types of buildings which are commercial use (COM), multi-family house (MFH), single-family house (SFH) and appartments (APPRT). 

Conceptually, we generate the heating demands using the following steps:

- Select the percentage and heating area of each building type within the substation
- Randomly select the DPE class based on know french building distributions
- Randomly select the energy consumption value based on the DPE class of each building type
- Creates the heating demands profile for the year based on know heating demands profiles

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