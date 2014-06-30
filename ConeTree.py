import avango
import avango.gua
import math

from Cone import *

# ConeTree Class
class ConeTree:

  ## Initialized with the scenegraph that is visualized
  def __init__(self, graph):
    avango.gua.load_materials_from("data/materials")
    self.Input_graph_ = graph
    self.RootCone_ = Cone(graph.Root.value)
    self.CT_graph_  = avango.gua.nodes.SceneGraph(
      Name = "ConeTree_Graph"
    )
    self.layout()

  def get_scene_node(self, CT_node):
    cones = []
    cones.append(self.RootCone_)
    # search for the node
    while (not len(cones) == 0):
      current = cones.pop()
      # when found set collapsed
      if current.outNode_.geometry_ == CT_node:
        return current.Input_node_
      for child in current.ChildrenCones_:
        cones.append(child)

  def get_CT_node(self, scene_node):
    cones = []
    cones.append(self.RootCone_)
    # search for the node
    while (not len(cones) == 0):
      current = cones.pop()
      # when found set collapsed
      if current.Input_node_ == scene_node:
        return current.outNode_.geometry_
      for child in current.ChildrenCones_:
        cones.append(child)

  def highlight_by_id(self, id, highlight):
    cones = []
    cones.append(self.RootCone_)
    # search for the id
    while (not len(cones) == 0):
      current = cones.pop()
      # when found set highlighted
      if current.id_ == id :
        #current.highlight(highlight)
        print "Highlight: " + str(current.id_) + " : " + str(highlight)
        #self.layout()
        return True
      for child in current.ChildrenCones_:
        cones.append(child)

  def get_scenegraph(self):
    node = self.RootCone_.get_scenegraph()
    self.CT_graph_.Root.value.Children.value = [node]
    return self.CT_graph_

  def get_root(self):
    return self.RootCone_.get_scenegraph()

  def print_ConeTree(self):
    self.RootCone_.print_cone(0)

  def layout(self):
    self.RootCone_.layout()
    self.RootCone_.apply_layout(root = True)

  def collapse_by_id(self, id, collapsed):
    cones = []
    cones.append(self.RootCone_)
    # search for the id
    while (not len(cones) == 0):
      current = cones.pop()
      # when found set collapsed
      if current.id_ == id :
        current.collapse(collapsed)
        print "Collapsed Node: " + str(current.id_) + " : " + str(collapsed)
        self.layout()
        return True
      for child in current.ChildrenCones_:
        cones.append(child)
  
  def collapse_by_scenenode(self, scene_node, collapsed):
    cones = []
    cones.append(self.RootCone_)
    # search for the node
    while (not len(cones) == 0):
      current = cones.pop()
      # when found set collapsed
      if current.Input_node_ == scene_node :
        current.collapse(collapsed)
        print "Collapsed Node: " + str(current.id_) + " : " + str(collapsed)
        self.layout()
        return True
      for child in current.ChildrenCones_:
        cones.append(child)

  def collapse_by_CTnode(self, CT_node, collapsed):
    cones = []
    cones.append(self.RootCone_)
    # search for the node
    while (not len(cones) == 0):
      current = cones.pop()
      # when found set collapsed
      if current.outNode_.geometry_ == CT_node :
        current.collapse(collapsed)
        print "Collapsed Node: " + str(current.id_) + " : " + str(collapsed)
        self.layout()
        return True
      for child in current.ChildrenCones_:
        cones.append(child)



def printscenegraph(scenegraph):
  for node in scenegraph.Root.value.Children.value:
    printhelper(node)

def printhelper(node):
  stack = []
  stack.append((node,0))

  while stack:
    tmp = stack.pop()
    printelement(tmp)
    for child in tmp[0].Children.value:
      stack.append((child,tmp[1]+1))
  
def printelement(nodetupel):
  for i in range(0, nodetupel[1]):
    print(" "),
  print nodetupel[0].Name.value + "   " 
  #print nodetupel[0]  
  #print nodetupel[0].Transform.value

