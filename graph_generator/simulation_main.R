library('igraph')

#E(net)       # The edges of the "net" object
#V(net)       # The vertices of the "net" object
#E(net)$type  # Edge attribute "type"
#V(net)$media # Vertex attribute "media"


nodes <- read.csv("networks/NodeTest.csv", header=T, as.is=T)
links <- read.csv("networks/EdgeTest.csv", header=T, as.is=T)

head(nodes)
head(links)

net <- graph_from_data_frame(d=links, vertices=nodes, directed=T) 

net <- simplify(net, remove.multiple = F, remove.loops = T) 

tkid <- tkplot(net) #tkid is the id of the tkplot that will open
l <- tkplot.getcoords(tkid) # grab the coordinates from tkplot
#plot(net, layout=l)

#plot(net, edge.arrow.size=.4,vertex.label=NA)