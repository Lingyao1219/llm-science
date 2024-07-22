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

disciplines = read.csv("disciplines_projected_edgelist.csv")
institutions = read.csv("institutions_projected_edgelist.csv")
countries = read.csv("countries_projected_edgelist.csv")

## Create function for plotting network and communities
plot_disciplines <- function(net, title) {
  cluster <- as.factor(cluster_louvain(net)$membership)
  
  # Calculate degree centrality
  degree_centrality <- degree(net)
  
  # Create a data frame for the layout and centrality 
  layout <- create_layout(net, layout = "fr") ## fix repulsion
  
  # Scale the layout to increase distances (spread nodes apart)
  layout$x <- layout$x * 70  # Adjust the multiplier to increase/decrease the spread
  layout$y <- layout$y * 70  # Adjust the multiplier to increase/decrease the spread
  
  layout$degree_centrality <- degree_centrality
  layout$cluster <- cluster
  layout$name <- V(net)$name  # Assuming the node names are in V(net)$name
  
  # Identify top 3% nodes within each cluster based on degree centrality
  top_nodes <- layout %>%
    group_by(cluster) %>%
    mutate(rank = rank(-degree_centrality)) %>%
    filter(rank <= 0.4 * n()) %>% ## adjust % here
    pull(name)
  
  # Create label column for top nodes
  layout$label <- ifelse(layout$name %in% top_nodes, layout$name, NA)
  
  set.seed(4343)
  ggraph(layout) +  # Use Fruchterman-Reingold layout for spreading nodes
    geom_edge_link(width = 0.2, alpha = 0.1) +  # Change opacity of edges
    geom_node_point(aes(fill = cluster),
                    shape = 21,
                    size = 5,
                    alpha = 0.75) +
    geom_mark_hull(
      aes(
        x = x,
        y = y,
        group = cluster,
        fill = cluster
      ),
      concavity = 4,
      expand = unit(2, "mm"),
      alpha = 0.25
    ) +
    geom_text_repel(
      aes(x = x, y = y, label = label),
      size = 5,  # Increase font size
      fontface = "bold",  # Make font bold
      family = "Garamond",  # Change to Arial or Garamond
      box.padding = 0.3,
      point.padding = 0.3,
      na.rm = TRUE  # Remove points with NA labels
    ) +  # Add node labels with repel
    scale_fill_brewer(palette = "Set2") +
    theme_graph() +
    ggtitle(title) + 
    theme(
      text = element_text(family = "Garamond"),  
      plot.title = element_text(size = 14, face = "bold", family = "Garamond"),
      plot.subtitle = element_text(size = 12, family = "Garamond"),
      legend.text = element_text(size = 10, family = "Garamond"),
      legend.title = element_text(size = 12, family = "Garamond"),
      legend.box.margin = margin(t = 5, r = 0, b = 0, l = -20)  # move legend box
    )
}


plot_institutions <- function(net, title) {
  cluster <- as.factor(cluster_louvain(net)$membership)
  
  # Calculate degree centrality
  degree_centrality <- degree(net)
  
  # Create a data frame for the layout and centrality 
  layout <- create_layout(net, layout = "fr") ## fix repulsion
  
  # Scale the layout to increase distances (spread nodes apart)
  layout$x <- layout$x * 70  # Adjust the multiplier to increase/decrease the spread
  layout$y <- layout$y * 70  # Adjust the multiplier to increase/decrease the spread
  
  layout$degree_centrality <- degree_centrality
  layout$cluster <- cluster
  layout$name <- V(net)$name  # Assuming the node names are in V(net)$name
  
  # Identify top 3% nodes within each cluster based on degree centrality
  top_nodes <- layout %>%
    group_by(cluster) %>%
    mutate(rank = rank(-degree_centrality)) %>%
    filter(rank <= 0.23 * n()) %>% ## adjust % here
    pull(name)
  
  # Create label column for top nodes
  layout$label <- ifelse(layout$name %in% top_nodes, layout$name, NA)
  
  set.seed(4343)
  ggraph(layout) +  # Use Fruchterman-Reingold layout for spreading nodes
    geom_edge_link(width = 0.2, alpha = 0.05) +  # Change opacity of edges
    geom_node_point(aes(fill = cluster),
                    shape = 21,
                    size = 5,
                    alpha = 0.75) +
    geom_mark_hull(
      aes(
        x = x,
        y = y,
        group = cluster,
        fill = cluster
      ),
      concavity = 4,
      expand = unit(2, "mm"),
      alpha = 0.25
    ) +
    geom_text_repel(
      aes(x = x, y = y, label = label),
      size = 5,  # Increase font size
      fontface = "bold",  # Make font bold
      family = "Garamond",  # Change to Arial or Garamond
      box.padding = 0.3,
      point.padding = 0.3,
      na.rm = TRUE  # Remove points with NA labels
    ) +  # Add node labels with repel
    scale_fill_brewer(palette = "Set2") +
    theme_graph() +
    ggtitle(title) +
    theme(
      text = element_text(family = "Garamond"),  # Change to Arial or Garamond
      plot.title = element_text(size = 14, face = "bold", family = "Garamond"),
      plot.subtitle = element_text(size = 12, family = "Garamond"),
      legend.text = element_text(size = 10, family = "Garamond"),
      legend.title = element_text(size = 12, family = "Garamond")
    )
}

plot_countries <- function(net, title) {
  cluster <- as.factor(cluster_louvain(net)$membership)
  
  # Calculate degree centrality
  degree_centrality <- degree(net)
  
  # Create a data frame for the layout and centrality 
  layout <- create_layout(net, layout = "fr") ## fix repulsion
  
  # Scale the layout to increase distances (spread nodes apart)
  layout$x <- layout$x * 50  # Adjust the multiplier to increase/decrease the spread
  layout$y <- layout$y * 50  # Adjust the multiplier to increase/decrease the spread
  
  layout$degree_centrality <- degree_centrality
  layout$cluster <- cluster
  layout$name <- V(net)$name  # Assuming the node names are in V(net)$name
  
  # Identify top 3% nodes within each cluster based on degree centrality
  top_nodes <- layout %>%
    group_by(cluster) %>%
    mutate(rank = rank(-degree_centrality)) %>%
    filter(rank <= 0.8 * n()) %>% ## adjust % here
    pull(name)
  
  # Create label column for top nodes
  layout$label <- ifelse(layout$name %in% top_nodes, layout$name, NA)
  
  set.seed(4343)
  ggraph(layout) +  # Use Fruchterman-Reingold layout for spreading nodes
    geom_edge_link(width = 0.2, alpha = 0.1) +  # Change opacity of edges
    geom_node_point(aes(fill = cluster),
                    shape = 21,
                    size = 5,
                    alpha = 0.75) +
    geom_mark_hull(
      aes(
        x = x,
        y = y,
        group = cluster,
        fill = cluster
      ),
      concavity = 4,
      expand = unit(2, "mm"),
      alpha = 0.25
    ) +
    geom_text_repel(
      aes(x = x, y = y, label = label),
      size = 5,  # Increase font size
      fontface = "bold",  # Make font bold
      family = "Garamond",  # Change to Arial or Garamond
      box.padding = 0.3,
      point.padding = 0.3,
      na.rm = TRUE  # Remove points with NA labels
    ) +  # Add node labels with repel
    scale_fill_brewer(palette = "Set2") +
    theme_graph() +
    ggtitle(title) + 
    theme(
      text = element_text(family = "Garamond"),  
      plot.title = element_text(size = 14, face = "bold", family = "Garamond"),
      plot.subtitle = element_text(size = 12, family = "Garamond"),
      legend.text = element_text(size = 10, family = "Garamond"),
      legend.title = element_text(size = 12, family = "Garamond")
    )
}

## Filter network to top 10% degree centrality nodes so size is manageable
filter_top_centrality_countries <- function(edges) {
  net <- graph_from_data_frame(d = edges, directed = FALSE)
  degree_cent <- degree(net, mode = "all")
  cutoff <- quantile(degree_cent, 0.8)
  top_nodes <- V(net)[degree_cent >= cutoff]
  sub_net <- induced_subgraph(net, top_nodes)
  return(sub_net)
}

filter_top_centrality_disciplines <- function(edges) {
  net <- graph_from_data_frame(d = edges, directed = FALSE)
  degree_cent <- degree(net, mode = "all")
  cutoff <- quantile(degree_cent, 0.97)
  top_nodes <- V(net)[degree_cent >= cutoff]
  sub_net <- induced_subgraph(net, top_nodes)
  return(sub_net)
}

filter_top_centrality_institutions <- function(edges) {
  net <- graph_from_data_frame(d = edges, directed = FALSE)
  degree_cent <- degree(net, mode = "all")
  cutoff <- quantile(degree_cent, 0.975)
  top_nodes <- V(net)[degree_cent >= cutoff]
  sub_net <- induced_subgraph(net, top_nodes)
  return(sub_net)
}

disciplines_filtered <- filter_top_centrality_disciplines(disciplines)
institutions_filtered <- filter_top_centrality_institutions(institutions)
countries_filtered <- filter_top_centrality_countries(countries)

countries_net = plot_countries(countries_filtered, "Countries Network")
disciplines_net = plot_disciplines(disciplines_filtered, "Disciplines Network")
institutions_net = plot_institutions(institutions_filtered, "Institutions Network")

institutions_net
disciplines_net
countries_net

# Combine plots into a single figure
#combined_plot <- countries_net + disciplines_net + institutions_net + plot_layout(ncol = 1)
#combined_plot
