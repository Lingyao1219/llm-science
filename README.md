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
pip3 install pandas matplotlib ast uuid openai google-generativeai networkx networkit powerlaw
```

3. Install required R packages:
```
install.packages(c("ggraph", "igraph", "ggforce", "concaveman", "RColorBrewer", "ggrepel", "tidygraph", "ggplot2", "patchwork", "CausalImpact", "car", "scales", "reshape2", "forecast"))
```

### Python Dependencies
```
import datetime
import pandas as pd
from ast import literal_eval
import matplotlib.pyplot as plt
import os
import ast
import uuid
import string
import json
import time
from openai import OpenAI
import google.generativeai as genai
import networkx as nx
import networkit as nk
import powerlaw
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
```

## Instructions for Use

### Python Scripts
- [batch.py](https://github.com/Lingyao1219/llm-science/blob/main/batch.py): This code applies GPT4o batch method. 
- [generate_json.py](https://github.com/Lingyao1219/llm-science/blob/main/generate_json.py): This code generates json files for implementaing the GPT4o batch method. 
- [model.py](https://github.com/Lingyao1219/llm-science/blob/main/model.py): This code implements several popular LLMs, including GPT4, GPT3.5, and Gemini.
- [prompt.py](https://github.com/Lingyao1219/llm-science/blob/main/prompt.py): This code lists the prompt design for running GPT4o batch method.
- [Data_prepare_BSTS.py](https://github.com/Lingyao1219/llm-science/blob/main/Data_prepare_BSTS.py): This code prepares the data for BSTS analysis.

### Jupyter Notebooks
- [batch_check_paper.ipynb](https://github.com/Lingyao1219/llm-science/blob/main/batch_check_paper.ipynb): This code uses GPT4o batch method to check whether a paper is relevant to the topic of LLMs.
- [batch_extract_authorinfo.ipynb](https://github.com/Lingyao1219/llm-science/blob/main/batch_extract_authorinfo.ipynb): This code uses GPT4o batch method to extract the authors' department information based on their affiliated information. 
- [collaboration_analysis.ipynb](https://github.com/Lingyao1219/llm-science/blob/main/collaboration_analysis.ipynb): this notebook aims to evaluate and analyze the authors' collaboration. The authors' collaboration diversity is calculated based on Shannon Entropy. 
- [data_cleaning.ipynb](https://github.com/Lingyao1219/llm-science/blob/main/data_cleaning.ipynb): This notebook is used to clean the papers collected from OpenAlex and ensure that the cleaned papers are relevant to the topics of LLMs.
- [network_projection_and_metrics.ipynb](https://github.com/Lingyao1219/llm-science/blob/main/network_projection_and_metrics.ipynb): this code is used for bipartite projection of networks and calculation of network metrics (overall cohesion, topology, community structure, and centrality measures).

### R Scripts
- [network_visualization.R](https://github.com/Lingyao1219/llm-science/blob/main/network_visualization.R): this code visualizes networks based on Fruchterman-reingold layout. Louvain modularity is used to cluster the networks into subgroups. The top degree centrality filters nodes and edges.
- [BSTS.R](https://github.com/Lingyao1219/llm-science/blob/main/BSTS.R): This code runs the BSTS model.


## Data Files
- [data](https://github.com/Lingyao1219/llm-science/tree/main/data): This directory contains three edgelists which are used for network analysis and visualization.
- The original and cleaned data files are published in https://doi.org/10.5281/zenodo.13118978.


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
