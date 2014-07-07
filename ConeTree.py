import avango
import avango.gua
import math

import avango.script
from avango.script import field_has_changed

from Cone import *

# ConeTree Class
class ConeTree(avango.script.Script):
  COLORMODE = "NODETYPE"
  OutMatrix = avango.gua.SFMatrix4()

  ## Initialized with the scenegraph that is visualized
  def __init__(self):
    self.super(ConeTree).__init__()

  def myConstructor(self, graph):
    self.Input_graph_ = graph
    self.RootCone_ = Cone(graph.Root.value, "ROOT")
    self.FocusCone_ = self.RootCone_
    avango.gua.load_materials_from("data/materials")
    self.FocusEdge_ = -1
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
    self.FocusCone_.highlight(True)

  def set_colormode(self, colormode = "NODETYPE", flip = False):
    if flip:
      if ConeTree.COLORMODE == "NODETYPE":
        ConeTree.COLORMODE = "DEPTH"
      else:
        ConeTree.COLORMODE = "NODETYPE"
    else:
      ConeTree.COLORMODE = colormode

  def reapply_materials(self):
    self.RootCone_.reapply_material()
    self.FocusCone_.highlight(True)

  def set_camera_on_Focus(self):
    nodePosition = self.FocusCone_.outNode_.geometry_.WorldTransform.value.get_translate()
    distance = (self.FocusCone_.Renderd_Radius_ * 2 ) / (1.6/4) - 2
    depth = - self.FocusCone_.Depth_ / 2
    self.OutMatrix.value = avango.gua.make_trans_mat( nodePosition  + avango.gua.Vec3(0,depth,distance) )

  # highlighting
  def highlight_by_level(self, level, highlight):
    cones = []
    cones.append(self.RootCone_)
    # search for the id
    while (not len(cones) == 0):
      current = cones.pop()
      # when found set highlighted
      if current.Level_ == level :
        current.highlight(highlight)
        print "Highlight: " + str(current.id_) + " : " + str(highlight)
        #self.layout()
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
        current.highlight(highlight)
        print "Highlight: " + str(current.id_) + " : " + str(highlight)
        #self.layout()
        return True
      for child in current.ChildrenCones_:
        cones.append(child)
    return False

  def highlight_by_scenenode(self, scenenode, highlight):
    cones = []
    cones.append(self.RootCone_)
    # search for the id
    while (not len(cones) == 0):
      current = cones.pop()
      # when found set highlighted
      if current.Input_node_ == scenenode :
        current.highlight(highlight)
        print "Highlight: " + str(current.id_) + " : " + str(highlight)
        #self.layout()
        return True
      for child in current.ChildrenCones_:
        cones.append(child)
    return False

  def highlight_by_CT_node(self, CT_node, highlight):
    cones = []
    cones.append(self.RootCone_)
    # search for the id
    while (not len(cones) == 0):
      current = cones.pop()
      # when found set highlighted
      if current.outNode_.geometry_ == CT_node :
        current.highlight(highlight)
        print "Highlight: " + str(current.id_) + " : " + str(highlight)
        #self.layout()
        return True
      for child in current.ChildrenCones_:
        cones.append(child)
    return False

  # collapsing

  def flip_collapse_at_focus(self):
    if self.FocusCone_.collapsed_:
      self.FocusCone_.collapse(False)
    else:
      self.FocusCone_.collapse(True)
    self.layout()

  def collapse_by_level(self, level, collapse):
    cones = []
    cones.append(self.RootCone_)
    # search for the level
    while (not len(cones) == 0):
      current = cones.pop()
      # when found set highlighted
      if current.Level_ == level :
        current.collapse(collapse)
        self.layout()
      for child in current.ChildrenCones_:
        cones.append(child)

  def collapse_by_id(self, id, collapsed):
    cones = []
    cones.append(self.RootCone_)
    # search for the id
    while (not len(cones) == 0):
      current = cones.pop()
      # when found set collapsed
      if current.id_ == id :
        current.collapse(collapsed)
        self.layout()
        return True
      for child in current.ChildrenCones_:
        cones.append(child)
    return False

  def collapse_by_scenenode(self, scenenode, collapsed):
    cones = []
    cones.append(self.RootCone_)
    # search for the node
    while (not len(cones) == 0):
      current = cones.pop()
      # when found set collapsed
      if current.Input_node_ == scenenode :
        current.collapse(collapsed)
        self.layout()
        return True
      for child in current.ChildrenCones_:
        cones.append(child)
    return False

  def collapse_by_CT_node(self, CT_node, collapsed):
    cones = []
    cones.append(self.RootCone_)
    # search for the node
    while (not len(cones) == 0):
      current = cones.pop()
      # when found set collapsed
      if current.outNode_.geometry_ == CT_node :
        current.collapse(collapsed)
        self.layout()
        return True
      for child in current.ChildrenCones_:
        cones.append(child)
    return False

  # deal with focus
  def focus_next_edge(self):
    if not self.FocusCone_.is_leaf():
      if not self.FocusEdge_ == -1:
        self.FocusCone_.highlight_edge(self.FocusEdge_,0)
      self.FocusEdge_ += 1
      if self.FocusEdge_ == len(self.FocusCone_.Edges_):
        self.FocusEdge_ = 0
      self.FocusCone_.highlight_edge(self.FocusEdge_,1)

  def focus_prev_edge(self):
    if not self.FocusCone_.is_leaf():
      if self.FocusEdge_ == -1:
        self.FocusEdge_ = len(self.FocusCone_.Edges_) - 1
      else:
        self.FocusCone_.highlight_edge(self.FocusEdge_,0)
        self.FocusEdge_ -= 1
        if self.FocusEdge_ == -1:
          self.FocusEdge_ = len(self.FocusCone_.Edges_) - 1
      self.FocusCone_.highlight_edge(self.FocusEdge_,1)

  def go_deep_at_focus(self):
    if not (self.FocusCone_.is_leaf() or self.FocusEdge_ == -1):
      # reset focusi
      self.FocusCone_.highlight(0)
      self.FocusCone_.highlight_edge(self.FocusEdge_,0)
      # set new focus
      self.FocusCone_ = self.FocusCone_.ChildrenCones_[self.FocusEdge_]
      self.FocusCone_.highlight(1)
      self.FocusEdge_ = -1

  def level_up(self):
    if not self.FocusCone_.Parent_ == "ROOT":
      self.FocusCone_.highlight(0)
      if not self.FocusEdge_ == -1:
        self.FocusCone_.highlight_edge(self.FocusEdge_,0)
      self.FocusEdge_ = -1
      self.FocusCone_ = self.FocusCone_.Parent_
      self.FocusCone_.highlight(1)





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

