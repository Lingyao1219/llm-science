# Academic Collaboration on Large Language Model (LLM) Research

## Table of Contents

- [Overview](#overview)
- [System Requirements](#System-Requirements)
- [Installation Guide](#Installation-Guide)
- [Instructions for Use](#Instructions-for-Use)
- [Data Files](#Data-Files)
- [License](#License)
- [Reference](#Reference)

## Overview
This repository contains code to support the analysis presented in the paper "Academic collaboration on large language model studies increases overall but varies across disciplines." The project aims to examine collaboration patterns in LLM research across different academic fields.

## System Requirements
- Python 3.7+
- R

## Installation Guide
1. Clone this repository:
```bash
git clone https://github.com/Lingyao1219/llm-science.git
cd llm-science
```

2. Install required Python packages:
```
pip3 install pandas numpy matplotlib ast argparse tqdm typing json uuid openai networkx networkit powerlaw pathlib
```

3. Install required R packages:
```
install.packages(c("ggraph", "igraph", "ggforce", "concaveman", "RColorBrewer", "ggrepel", "tidygraph", "ggplot2", "patchwork", "CausalImpact", "car", "scales", "reshape2", "forecast", "Cairo"))
```

### Python Dependencies
```
import os
import ast
import uuid
import string
import json
import tqdm
import time
import argparse
import random
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import networkit as nk
import powerlaw
from ast import literal_eval
from openai import OpenAI
from typing import List, Optional, Set, Tuple, Any
from pathlib import Path
from tqdm import tqdm
```

### R Dependencies
```
library(ggraph)
library(igraph)
library(ggforce)
library(concaveman)
library(RColorBrewer)
library(ggrepel)
library(tidygraph)
library(ggplot2)
library(patchwork)
library(CausalImpact)
library(car)
library(scales)
library(reshape2)
library(forecast)
library(Cairo)
```

## Instructions for Use

### Python Scripts
- [affiliation_matcher.py](https://github.com/Lingyao1219/llm-science/blob/main/data_preparation/affiliation_matcher.py): This code aims to match each piece of academic data based on the extracted affiliation information.
- [affiliation_processor.py](https://github.com/Lingyao1219/llm-science/blob/main/data_preparation/affiliation_processor.py): This code aims to process academic affiliations data. 
- [entropy_calculator.py](https://github.com/Lingyao1219/llm-science/blob/main/data_preparation/entropy_calculator.py): This code calculates the Shannon entropy based on authors' institutional and departmental affiliations.
- [paper_processor.py](https://github.com/Lingyao1219/llm-science/blob/main/data_preparation/paper_processor.py): This code processes paper cleaning through several steps: paper type filtering, date filtering, and duplicate handling.
- [relevance_checker.py](https://github.com/Lingyao1219/llm-science/blob/main/data_preparation/relevance_checker.py): This code checks the paper relevance to the topic of large language models.
- [config_utils.py](https://github.com/Lingyao1219/llm-science/blob/main/data_preparation/config_utils.py): This code lists configuration utility functions, including prompt design and gpt model to process paper information.  

### Jupyter Notebooks
- [batch_check_paper.ipynb](https://github.com/Lingyao1219/llm-science/blob/main/batch_check_paper.ipynb): This code uses GPT4o batch method to check whether a paper is relevant to the topic of LLMs.
- [batch_extract_authorinfo.ipynb](https://github.com/Lingyao1219/llm-science/blob/main/batch_extract_authorinfo.ipynb): This code uses GPT4o batch method to extract the authors' department information based on their affiliated information. 
- [collaboration_analysis.ipynb](https://github.com/Lingyao1219/llm-science/blob/main/collaboration_analysis.ipynb): this notebook aims to evaluate and analyze the authors' collaboration. The authors' collaboration diversity is calculated based on Shannon Entropy. 
- [data_cleaning.ipynb](https://github.com/Lingyao1219/llm-science/blob/main/data_cleaning.ipynb): This notebook is used to clean the papers collected from OpenAlex and ensure that the cleaned papers are relevant to the topics of LLMs.
- [network_projections_and_metrics.ipynb](https://github.com/Lingyao1219/llm-science/blob/main/network_projections_and_metrics.ipynb): this code is used for bipartite projection of networks and calculation of network metrics (overall cohesion, topology, community structure, and centrality measures).

### R Scripts
- [network_visualization.R](https://github.com/Lingyao1219/llm-science/blob/main/network_visualization.R): this code visualizes networks based on Fruchterman-reingold layout. Louvain modularity is used to cluster the networks into subgroups. The top degree centrality filters nodes and edges.
- [BSTS.R](https://github.com/Lingyao1219/llm-science/blob/main/BSTS.R): This code runs the BSTS model.


## Data Files
- [Network data](https://github.com/Lingyao1219/llm-science/tree/main/Network%20data): This directory contains three edgelists which are used for network analysis and visualization.
- The original and cleaned data files are published in (https://doi.org/10.5281/zenodo.14574920).


## License
This project is covered under the Apache 2.0 License.

## Reference
```
@article{@article{li2024academic,
  title={Academic collaboration on large language model studies increases overall but varies across disciplines},
  author={Li, Lingyao and Dinh, Ly and Hu, Songhua and Hemphill, Libby},
  journal={arXiv preprint arXiv:2408.04163},
  year={2024}
}
```
