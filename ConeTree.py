import avango
import avango.gua
import math

import avango.script
from avango.script import field_has_changed

from Cone import *
from Text import TextField


# ConeTree Class
class ConeTree(avango.script.Script):
  COLORMODE = "NODETYPE"
  OutMatrix = avango.gua.SFMatrix4()
  EyeTransform = avango.gua.SFMatrix4()

  ## Initialized with the scenegraph that is visualized
  def __init__(self):
    self.super(ConeTree).__init__()

  def myConstructor(self, graph, screen, eye):
    self.Input_graph_ = graph
    self.RootCone_ = Cone(graph.Root.value, None)
    self.FocusCone_ = self.RootCone_
    avango.gua.load_materials_from("data/materials")
    avango.gua.load_materials_from("data/materials/font")
    self.FocusEdge_ = -1

    self.EyeTransform.connect_from(eye.Transform)
    self.Screen = screen

    self.CT_graph_  = avango.gua.nodes.SceneGraph(
      Name = "ConeTree_Graph"
    )
    self.layout()

    #initialize camera pos
    self.CT_graph_.update_cache()
    self.set_camera_on_Focus()

    #initialize label
    self.ShowLabel_ = True
    self.Label_ = TextField()
    self.Label_.my_constructor(self.Screen)
    self.Label_.sf_transform.value = ( avango.gua.make_trans_mat(- self.Screen.Width.value/2 , (-self.Screen.Height.value/2) + 0.07, 0)
                                      * avango.gua.make_scale_mat(self.Screen.Height.value*0.07) )
    self.update_label()


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
    if not self.FocusCone_.is_leaf():
      bb = self.FocusCone_.outNode_.geometry_.BoundingBox.value
      nodePosition = self.FocusCone_.outNode_.geometry_.WorldTransform.value.get_translate()

      diff_x_left = nodePosition.x - bb.Min.value.x
      diff_x_right = bb.Max.value.x - nodePosition.x

      diff_y_left = nodePosition.y - bb.Min.value.y
      diff_y_right = bb.Max.value.y - nodePosition.y

      size_x = max(diff_x_left,diff_x_right) * 2
      size_y = bb.Max.value.y - bb.Min.value.y
      size_z = bb.Max.value.z - bb.Min.value.z

      eye_from_screen = self.EyeTransform.value.get_translate().length()

      distance_x = ((eye_from_screen*size_x)/self.Screen.Width.value) - eye_from_screen
      distance_y = ((eye_from_screen*size_y)/self.Screen.Height.value) - eye_from_screen

      distance = max(distance_x,distance_y) + 0.5 * size_z

      depth = - size_y / 2
      self.OutMatrix.value = avango.gua.make_trans_mat( nodePosition  + avango.gua.Vec3(0,depth,distance) )

  def flip_showlabel(self):
    self.ShowLabel_ = not self.ShowLabel_
    self.update_label()


  def update_label(self):
    if self.ShowLabel_:
      if self.FocusEdge_ == -1:
        self.Label_.sf_text.value = self.FocusCone_.Input_node_.Name.value
      else:
        self.Label_.sf_text.value = self.FocusCone_.ChildrenCones_[self.FocusEdge_].Input_node_.Name.value
    else:
      self.Label_.sf_text.value = ""

  # rotate
  def rotate_by_id(self, id, angle):
    cones = []
    cones.append(self.RootCone_)
    # search for the id
    while (not len(cones) == 0):
      current = cones.pop()
      # when found set highlighted
      if current.id_ == id :
        current.rotate(angle)
        print "Rotate: " + str(current.id_) + " : " + str(angle)
        self.layout()
        return True
      for child in current.ChildrenCones_:
        cones.append(child)
    return False

  # highlighting
  def highlight(self, selector, highlight = True):
    cones = []
    cones.append(self.RootCone_)
    # search for the selector
    while (not len(cones) == 0):
      current = cones.pop()
      # when found set highlighted
      if current.id_ == selector or current.Input_node_ == selector or current.outNode_.geometry_ == selector:
        current.highlight(highlight)
        print "Highlight: " + str(current.id_) + " : " + str(highlight)

      for child in current.ChildrenCones_:
        cones.append(child)

  def highlight_path(self, selector, highlight = True):
    cones = []
    cones.append(self.RootCone_)
    # search for the selector
    while (not len(cones) == 0):
      current = cones.pop()
      # when found set highlighted
      if current.id_ == selector or current.Input_node_ == selector or current.outNode_.geometry_ == selector:
        # always hold a reference to the parent and current cone
        parent = current.Parent_
        while (not parent == None): # go up the ConeTree
          current.highlight(highlight) # highlight the Nodes

          for edge in parent.Edges_:
            if edge.To_ == current.outNode_:  # look for the edge linking parent and current
              edge.highlight(highlight) # highlight it

          current = current.Parent_
          parent = current.Parent_

        current.highlight(highlight) # highlight also root
        return True

      for child in current.ChildrenCones_:
        cones.append(child)

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

  def collapse(self, selector, collapse = True):
    cones = []
    cones.append(self.RootCone_)
    # search for the selector
    while (not len(cones) == 0):
      current = cones.pop()
      # when found set highlighted
      if current.id_ == selector or current.Input_node_ == selector or current.outNode_.geometry_ == selector:
        current.collapse(collapse)
        print "Collapsed: " + str(current.id_) + " : " + str(collapse)

      for child in current.ChildrenCones_:
        cones.append(child)


  # deal with focus
  def focus_next_edge(self):
    if not self.FocusCone_.is_leaf():
      if not self.FocusEdge_ == -1:
        self.FocusCone_.highlight_edge(self.FocusEdge_,0)
      self.FocusEdge_ += 1
      if self.FocusEdge_ == len(self.FocusCone_.Edges_):
        self.FocusEdge_ = 0
      self.FocusCone_.highlight_edge(self.FocusEdge_,1)
      self.update_label()

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
      self.update_label()

  def go_deep_at_focus(self):
    if not (self.FocusCone_.is_leaf() or self.FocusEdge_ == -1):
      # reset focusi
      self.FocusCone_.highlight(0)
      self.FocusCone_.highlight_edge(self.FocusEdge_,0)
      # set new focus
      self.FocusCone_ = self.FocusCone_.ChildrenCones_[self.FocusEdge_]
      self.FocusCone_.highlight(1)
      self.FocusEdge_ = -1
      self.update_label()

  def level_up(self):
    if not self.FocusCone_.Parent_ == None:
      self.FocusCone_.highlight(0)
      if not self.FocusEdge_ == -1:
        self.FocusCone_.highlight_edge(self.FocusEdge_,0)
      self.FocusEdge_ = -1
      self.FocusCone_ = self.FocusCone_.Parent_
      self.FocusCone_.highlight(1)
      self.update_label()





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

