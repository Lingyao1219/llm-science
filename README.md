# Project Title

The code aims to support the analysis in the paper entitled "Academic collaboration on large language model studies increases overall but varies across disciplines."

## Files and Directories

### Data Files
- [data](https://github.com/Lingyao1219/llm-science/tree/main/data): This directory contains three edgelists which are used for network analysis and visualization.
- The original and cleaned data files are published in https://doi.org/10.5281/zenodo.13118978.

### Python Scripts
- [batch.py](https://github.com/Lingyao1219/llm-science/blob/main/batch.py): This code applies GPT4o batch method. 
- [generate_json.py](https://github.com/Lingyao1219/llm-science/blob/main/generate_json.py): This code generates json files for implementaing the GPT4o batch method. 
- [model.py](https://github.com/Lingyao1219/llm-science/blob/main/model.py): This code implements several popular LLMs, including GPT4, GPT3.5, and Gemini.
- [prompt.py](https://github.com/Lingyao1219/llm-science/blob/main/prompt.py): This code lists the prompt design for running GPT4o batch method. 

### Jupyter Notebooks
- [batch_check_paper.ipynb](https://github.com/Lingyao1219/llm-science/blob/main/batch_check_paper.ipynb): This code uses GPT4o batch method to check whether a paper is relevant to the topic of LLMs.
- [batch_extract_authorinfo.ipynb](https://github.com/Lingyao1219/llm-science/blob/main/batch_extract_authorinfo.ipynb): This code uses GPT4o batch method to extract the authors' department information based on their affiliated information. 
- [collaboration_analysis.ipynb](https://github.com/Lingyao1219/llm-science/blob/main/collaboration_analysis.ipynb): this notebook aims to evaluate and analyze the authors' collaboration. The authors' collaboration diversity is calcuated based on Shannon Entropy. 
- [data_cleaning.ipynb](https://github.com/Lingyao1219/llm-science/blob/main/data_cleaning.ipynb): this notebook is used to clean the papers collected from OpenAlex and ensure that the cleaned papers are relevant to the topics of LLMs.
- [network_projection_and_metrics.ipynb](https://github.com/Lingyao1219/llm-science/blob/main/network_projection_and_metrics.ipynb): this code is used for bipartite projection of networks and calculation of network metrics (overall cohesion, topology, community structure, and centrality measures).

### R Scripts
- [network_visualization.R](https://github.com/Lingyao1219/llm-science/blob/main/network_visualization.R): this code visualizes networks based on Fruchterman-reingold layout. Louvain modularity is used to cluster the networks into subgroups. Nodes and edges are filtered by the top degree centrality.
