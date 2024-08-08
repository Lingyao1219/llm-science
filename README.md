# Project Title

The code aims to support the analysis in the paper entitled "Academic collaboration on large language model studies increases overall but varies across disciplines."

## Files and Directories

- [data](https://github.com/Lingyao1219/llm-science/tree/main/data): This directory contains three edgelists which are used for network analysis and visualization. 

### Python Scripts
- [batch.py](https://github.com/Lingyao1219/llm-science/blob/main/batch.py): Batch method for gpt4o input
- [generate_json.py](https://github.com/Lingyao1219/llm-science/blob/main/generate_json.py): Generate JSON data
- [model.py](https://github.com/Lingyao1219/llm-science/blob/main/model.py): Contains model definitions
- [prompt.py](https://github.com/Lingyao1219/llm-science/blob/main/prompt.py): Prompt design implementation

### Jupyter Notebooks
- [batch_check_paper.ipynb](https://github.com/Lingyao1219/llm-science/blob/main/batch_check_paper.ipynb): For checking paper relevance
- [batch_extract_authorinfo.ipynb](https://github.com/Lingyao1219/llm-science/blob/main/batch_extract_authorinfo.ipynb): For extracting author information
- [collaboration_analysis.ipynb](https://github.com/Lingyao1219/llm-science/blob/main/collaboration_analysis.ipynb): Collaboration network analysis
- [data_cleaning.ipynb](https://github.com/Lingyao1219/llm-science/blob/main/data_cleaning.ipynb): this notebook is used to clean the papers collected from OpenAlex and ensure that the cleaned papers are relevant to the topics of LLMs.
- [network_projection_and_metrics.ipynb](https://github.com/Lingyao1219/llm-science/blob/main/network_projection_and_metrics.ipynb): this code is used for bipartite projection of networks and calculation of network metrics (overall cohesion, topology, community structure, and centrality measures).

### R Scripts
- [network_visualization.R](https://github.com/Lingyao1219/llm-science/blob/main/network_visualization.R): this code visualizes networks based on Fruchterman-reingold layout. Louvain modularity is used to cluster the networks into subgroups. Nodes and edges are filtered by the top degree centrality.
