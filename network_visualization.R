setwd("\\Users\\lydinh\\Desktop")

# Load necessary libraries
#install.packages("ggraph")
library(ggraph)
#install.packages("igraph")
library(igraph)
#install.packages("ggforce")
library(ggforce)
#install.packages("concaveman")
library(concaveman)
#install.packages("RColorBrewer")
library(RColorBrewer)
#install.packages("ggrepel")
library(ggrepel)
#install.packages("tidygraph")
library(tidygraph)
#install.packages("ggplot2")
library(ggplot2)
#install.packages("patchwork")
library(patchwork)
#install.packages("Cairo")
library(Cairo)

disciplines = read.csv("disciplines_projected_edgelist.csv")
institutions = read.csv("institutions_projected_edgelist.csv")
#countries = read.csv("countries_projected_edgelist.csv")

## Create function for plotting network and communities
plot_disciplines <- function(net, title, max_clusters = 5, label_percentage = 0.7) {
  # Cluster the network using Louvain algorithm
  louvain_clusters <- cluster_louvain(net)
  
  # Calculate cluster sizes
  cluster_sizes <- sort(table(membership(louvain_clusters)), decreasing = TRUE)
  
  # If more than max_clusters exist, merge smaller clusters
  if (length(cluster_sizes) > max_clusters) {
    top_clusters <- as.numeric(names(cluster_sizes)[1:max_clusters])
    
    cluster_mapping <- membership(louvain_clusters)
    
    # Reassign smaller clusters to the nearest top cluster using spatial proximity
    coords <- layout_with_fr(net)
    
    for (i in which(!cluster_mapping %in% top_clusters)) {
      distances <- sapply(top_clusters, function(cluster) {
        cluster_coords <- coords[cluster_mapping == cluster, ]
        min(dist(rbind(coords[i, ], cluster_coords)))
      })
      
      cluster_mapping[i] <- top_clusters[which.min(distances)]
    }
    
    cluster_membership <- factor(cluster_mapping, levels = top_clusters)
  } else {
    cluster_membership <- factor(membership(louvain_clusters))
  }
  
  # Create layout
  layout <- create_layout(net, layout = "fr")
  layout$x <- layout$x * 70
  layout$y <- layout$y * 70
  
  # Calculate degree centrality
  degree_centrality <- degree(net)
  
  # Prepare layout data
  layout$degree_centrality <- degree_centrality
  layout$cluster <- cluster_membership
  layout$name <- V(net)$name
  
  # Label a higher percentage of nodes by degree centrality in each cluster
  top_nodes <- layout %>% 
    group_by(cluster) %>% 
    mutate(rank = rank(-degree_centrality)) %>% 
    filter(rank <= label_percentage * n()) %>% 
    pull(name)
  
  layout$label <- ifelse(layout$name %in% top_nodes, layout$name, NA)
  
  # Plot the network
  set.seed(4343)
  ggraph(layout) + 
    geom_edge_link(width = 0.2, alpha = 0.05) + 
    geom_node_point(aes(fill = cluster), shape = 21, size = 5, alpha = 0.75) + 
    geom_mark_hull(aes(x = x, y = y, group = cluster, fill = cluster), 
                   concavity = 4, 
                   expand = unit(2, "mm"), 
                   alpha = 0.25) + 
    geom_text_repel(aes(x = x, y = y, label = label), 
                    size = 4, 
                    fontface = "bold", 
                    family = "Garamond", 
                    box.padding = 0.3, 
                    point.padding = 0.3, 
                    na.rm = TRUE) + 
    scale_fill_brewer(palette = "Set2") + 
    theme_graph() + 
    ggtitle(title) + 
    theme(
      legend.position = "none",
      text = element_text(family = "Garamond", size = 16),
      plot.title = element_text(size = 14, face = "bold", family = "Garamond")
    )
}

plot_institutions <- function(net, title, max_clusters = 5, label_percentage = 0.7) {
  # Cluster the network using Louvain algorithm
  louvain_clusters <- cluster_louvain(net)
  
  # Calculate cluster sizes
  cluster_sizes <- sort(table(membership(louvain_clusters)), decreasing = TRUE)
  
  # If more than max_clusters exist, merge smaller clusters
  if (length(cluster_sizes) > max_clusters) {
    top_clusters <- as.numeric(names(cluster_sizes)[1:max_clusters])
    
    cluster_mapping <- membership(louvain_clusters)
    
    # Reassign smaller clusters to the nearest top cluster using spatial proximity
    coords <- layout_with_fr(net)
    
    for (i in which(!cluster_mapping %in% top_clusters)) {
      distances <- sapply(top_clusters, function(cluster) {
        cluster_coords <- coords[cluster_mapping == cluster, ]
        min(dist(rbind(coords[i, ], cluster_coords)))
      })
      
      cluster_mapping[i] <- top_clusters[which.min(distances)]
    }
    
    cluster_membership <- factor(cluster_mapping, levels = top_clusters)
  } else {
    cluster_membership <- factor(membership(louvain_clusters))
  }
  
  # Create layout
  layout <- create_layout(net, layout = "fr")
  layout$x <- layout$x * 70
  layout$y <- layout$y * 70
  
  # Calculate degree centrality
  degree_centrality <- degree(net)
  
  # Prepare layout data
  layout$degree_centrality <- degree_centrality
  layout$cluster <- cluster_membership
  layout$name <- V(net)$name
  
  # Label a higher percentage of nodes by degree centrality in each cluster
  top_nodes <- layout %>% 
    group_by(cluster) %>% 
    mutate(rank = rank(-degree_centrality)) %>% 
    filter(rank <= label_percentage * n()) %>% 
    pull(name)
  
  layout$label <- ifelse(layout$name %in% top_nodes, layout$name, NA)
  
  # Plot the network
  set.seed(4343)
  ggraph(layout) + 
    geom_edge_link(width = 0.2, alpha = 0.05) + 
    geom_node_point(aes(fill = cluster), shape = 21, size = 5, alpha = 0.75) + 
    geom_mark_hull(aes(x = x, y = y, group = cluster, fill = cluster), 
                   concavity = 4, 
                   expand = unit(2, "mm"), 
                   alpha = 0.25) + 
    geom_text_repel(aes(x = x, y = y, label = label), 
                    size = 4, 
                    fontface = "bold", 
                    family = "Garamond", 
                    box.padding = 0.3, 
                    point.padding = 0.3, 
                    na.rm = TRUE) + 
    scale_fill_brewer(palette = "Set2") + 
    theme_graph() + 
    ggtitle(title) + 
    theme(
      legend.position = "none",
      text = element_text(family = "Garamond", size = 16),
      plot.title = element_text(size = 14, face = "bold", family = "Garamond")
    )
}

# Read the data for LLM, ML, and Non-LLM
llm_institutions <- read.csv("LLM_institutions_projected_edgelist.csv")
ml_institutions <- read.csv("ML_institutions_projected_edgelist.csv")
non_llm_institutions <- read.csv("Non-LLM_institutions_projected_edgelist.csv")

# Filter top centrality for each dataset
filter_top_centrality_institutions <- function(edges, cutoff_percent = 0.985) {
  net <- graph_from_data_frame(d = edges, directed = FALSE)
  degree_cent <- degree(net, mode = "all")
  cutoff <- quantile(degree_cent, cutoff_percent)
  top_nodes <- V(net)[degree_cent >= cutoff]
  sub_net <- induced_subgraph(net, top_nodes)
  return(sub_net)
}

llm_filtered <- filter_top_centrality_institutions(llm_institutions)
ml_filtered <- filter_top_centrality_institutions(ml_institutions)
non_llm_filtered <- filter_top_centrality_institutions(non_llm_institutions)

# Plot each network
llm_plot <- plot_institutions(llm_filtered, "LLM")
ml_plot <- plot_institutions(ml_filtered, "ML")
non_llm_plot <- plot_institutions(non_llm_filtered, "Non-LLM")

combined_plot <- llm_plot / (ml_plot | non_llm_plot)
print(combined_plot)

# Save with Cairo device for better rendering
CairoPDF("combined_institutions_network_plot.pdf", width = 20, height = 16)
print(combined_plot)
dev.off()


### For disciplines
# Read the data for LLM, ML, and Non-LLM disciplines
llm_disciplines <- read.csv("LLM_disciplines_projected_edgelist.csv")
ml_disciplines <- read.csv("ML_disciplines_projected_edgelist.csv")
non_llm_disciplines <- read.csv("Non-LLM_disciplines_projected_edgelist.csv")

# Filter top centrality for each dataset
filter_top_centrality_disciplines <- function(edges, cutoff_percent = 0.985) {
  net <- graph_from_data_frame(d = edges, directed = FALSE)
  degree_cent <- degree(net, mode = "all")
  cutoff <- quantile(degree_cent, cutoff_percent)
  top_nodes <- V(net)[degree_cent >= cutoff]
  sub_net <- induced_subgraph(net, top_nodes)
  return(sub_net)
}

llm_filtered <- filter_top_centrality_disciplines(llm_disciplines)
ml_filtered <- filter_top_centrality_disciplines(ml_disciplines)
non_llm_filtered <- filter_top_centrality_disciplines(non_llm_disciplines)

# Plot each network
llm_plot <- plot_disciplines(llm_filtered, "LLM")
ml_plot <- plot_disciplines(ml_filtered, "ML")
non_llm_plot <- plot_disciplines(non_llm_filtered, "Non-LLM")

combined_plot <- llm_plot / (ml_plot | non_llm_plot)
print(combined_plot)

# Save with Cairo device for better rendering
CairoPDF("combined_disciplines_network_plot.pdf", width = 20, height = 16)
print(combined_plot)
dev.off()
