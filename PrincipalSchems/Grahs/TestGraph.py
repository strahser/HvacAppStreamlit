import streamlit
from streamlit_agraph import agraph, Node, Edge, Config

nodes = []
edges = []
nodes.append(Node(id="S01",shape='circle',label="S01",physics=False) )
nodes.append(Node(id="S02",shape='circle',label="S02",physics=False))
nodes.append(Node(id="room1",label="room1",area=500,shape='square',level=1,group=1,borderWidth=2,physics=False)) 
nodes.append(Node(id="room2",label="room2",area=500,shape='square',level=2,group=1,physics=False))
nodes.append(Node(id="room3",label="room3",area=500,shape='square',level=2,physics=False))
edges.append(Edge(source="room1", target="S01"))
edges.append(Edge(source="room2", target="S01"))
edges.append(Edge(source="room3", target="S01"))
edges.append(Edge(source="room1", target="S02"))
edges.append(Edge(source="room2", target="S02"))
edges.append(Edge(source="room3", target="S02"))


config = Config(width=500, 
                height=500,

                # **kwargs
                ) 

return_value = agraph(nodes=nodes, 
                      edges=edges, 
                      config=config)