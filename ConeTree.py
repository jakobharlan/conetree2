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
  FocusCTNode = avango.gua.SFNode()
  FocusSceneNode = avango.gua.SFNode()

  def __init__(self):
    self.super(ConeTree).__init__()

  # Constructor, start_node is the input node from wich one the ConeTree Representation starts
  def myConstructor(self, start_node):
    self.Start_node = start_node
    self.RootNode_ = avango.gua.nodes.TransformNode(
      Name = "ConeTreeRoot",
    )
    self.ScaleNode_ = avango.gua.nodes.TransformNode(
      Name = "ConeTreeScale",
    )
    self.TransformNode_ = avango.gua.nodes.TransformNode(
      Name = "ConeTreeTransform",
    )
    self.RootCone_ = Cone(self.Start_node, None)
    self.FocusCone_ = self.RootCone_
    avango.gua.load_materials_from("data/materials")

    self.FocusEdge_ = -1

    self.layout()

  def update_focus_nodes(self):
    if self.FocusEdge_ == -1:
      self.FocusCTNode.value = self.FocusCone_.outNode_.geometry_
      self.FocusSceneNode.value = self.FocusCone_.Input_node_
    else:
      self.FocusCTNode.value = self.FocusCone_.ChildrenCones_[self.FocusEdge_].outNode_.geometry_
      self.FocusSceneNode.value = self.FocusCone_.ChildrenCones_[self.FocusEdge_].Input_node_

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

  def create_scenegraph_structure(self):
    node = self.RootCone_.get_scenegraph()
    self.RootNode_.Children.value = [self.ScaleNode_]
    self.ScaleNode_.Children.value = [self.TransformNode_]
    self.TransformNode_.Children.value = [node]
    return self.RootNode_

  def get_root(self):
    return self.RootNode_

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

  def scale(self):
    if self.FocusCone_.is_leaf():
      used_Cone = self.FocusCone_.Parent_
    else:
      used_Cone = self.FocusCone_
    
    bb = used_Cone.outNode_.geometry_.BoundingBox.value

    bb_sides = (bb.Max.value.x - bb.Min.value.x
               ,bb.Max.value.y - bb.Min.value.y
               ,bb.Max.value.z - bb.Min.value.z)

    # scale = 0.5 / max(bb_sides)
    scale = 1.0 / max(bb_sides)
    # scale = 1.5 / max(bb_sides)

    self.ScaleNode_.Transform.value *= avango.gua.make_scale_mat(scale)

  def reposition(self):
    if self.FocusCone_.is_leaf():
      used_Cone = self.FocusCone_.Parent_
    else:
      used_Cone = self.FocusCone_

    if not used_Cone.Parent_ == None:
      current = used_Cone
      parent  = current.Parent_
      matrix  = current.outNode_.geometry_.Transform.value
      while not parent == self.RootCone_:
        current = parent
        parent = current.Parent_
        matrix *= current.outNode_.geometry_.Transform.value
      self.TransformNode_.Transform.value = avango.gua.make_inverse_mat(matrix)
    else:
      self.TransformNode_.Transform.value = avango.gua.make_identity_mat()


  def set_camera_on_Focus(self):
    return
    # if not self.FocusCone_.is_leaf():
    #   bb = self.FocusCone_.outNode_.geometry_.BoundingBox.value
    #   nodePosition = self.FocusCone_.outNode_.geometry_.WorldTransform.value.get_translate()

    #   diff_x_left = nodePosition.x - bb.Min.value.x
    #   diff_x_right = bb.Max.value.x - nodePosition.x

    #   diff_y_left = nodePosition.y - bb.Min.value.y
    #   diff_y_right = bb.Max.value.y - nodePosition.y

    #   size_x = max(diff_x_left,diff_x_right) * 2
    #   size_y = bb.Max.value.y - bb.Min.value.y
    #   size_z = bb.Max.value.z - bb.Min.value.z

    #   eye_from_screen = self.EyeTransform.value.get_translate().length()

    #   distance_x = ((eye_from_screen*size_x)/self.Screen.Width.value) - eye_from_screen
    #   distance_y = ((eye_from_screen*size_y)/self.Screen.Height.value) - eye_from_screen

    #   distance = max(distance_x,distance_y) + 0.5 * size_z

    #   depth = - size_y / 2
    #   self.OutMatrix.value = avango.gua.make_trans_mat( nodePosition  + avango.gua.Vec3(0,depth,distance) )

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
  def highlight(self, selector, highlight = True, path = False):
    cones = []
    cones.append(self.RootCone_)
    # search for the selector
    while (not len(cones) == 0):
      current = cones.pop()
      # when found set highlighted
      if current.id_ == selector or current.Input_node_ == selector or current.outNode_.geometry_ == selector:
        if path:
          current.highlight_path(highlight)
          print "Highlight path: " + str(current.id_) + " : " + str(highlight)
        else:
          current.highlight(highlight)
          print "Highlight: " + str(current.id_) + " : " + str(highlight)

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
  def focus(self, selector):

    cones = []
    cones.append(self.RootCone_)
    # search for the selector in whole COneTree
    while (not len(cones) == 0):
      current = cones.pop()
      # when found set highlighted
      if current.id_ == selector or current.Input_node_ == selector or current.outNode_.geometry_ == selector:
        # set new focus
        self.FocusCone_.highlight_path(0)
        self.FocusCone_ = current
        self.FocusCone_.highlight_path(1)
        self.FocusEdge_ = -1
        self.update_focus_nodes()
        return True

      for child in current.ChildrenCones_:
        cones.append(child)

    return False

  def rotate_by_ray(self, ray, ray_scale):
    ray_start = ray.WorldTransform.value.get_translate()

    matrix = ray.WorldTransform.value * avango.gua.make_scale_mat(1.0/ray_scale.x , 1.0/ray_scale.y , 1.0/ray_scale.z)
    ray_direction = avango.gua.make_rot_mat(matrix.get_rotate()) * avango.gua.Vec3(0,0,-1)
    ray_direction = avango.gua.Vec3(ray_direction.x, ray_direction.y, ray_direction.z)

    ray_direction.normalize()

    if abs(ray_direction.x) > 0.5:
      if ray_direction.x > 0:
        self.FocusCone_.rotate((ray_direction.x - 0.5) / 10)
      else:
        self.FocusCone_.rotate((ray_direction.x + 0.5) / 10)

      # self.RootCone_.apply_layout(root = True)
      self.layout()


  def highlight_closest_edge(self, ray, ray_scale):
    ray_start = ray.WorldTransform.value.get_translate()

    matrix = ray.WorldTransform.value * avango.gua.make_scale_mat(1.0/ray_scale.x , 1.0/ray_scale.y , 1.0/ray_scale.z)
    ray_direction = avango.gua.make_rot_mat(matrix.get_rotate()) * avango.gua.Vec3(0,0,-1)
    ray_direction = avango.gua.Vec3(ray_direction.x, ray_direction.y, ray_direction.z)

    ray_direction_length = ray_direction.length()

    # calculate distance to Focus Node
    point = self.FocusCone_.outNode_.geometry_.WorldTransform.value.get_translate()
    tmp = ray_direction.cross((point - ray_start))
    closest_distance = tmp.length() / ray_direction_length
    result = -1
    # and calculate distance to all Children
    for i in range(len(self.FocusCone_.ChildrenCones_)):
      point = self.FocusCone_.ChildrenCones_[i].outNode_.geometry_.WorldTransform.value.get_translate()
      tmp = ray_direction.cross((point - ray_start))
      tmp_distance = tmp.length() / ray_direction_length
      # closer ?
      if tmp_distance < closest_distance:
        closest_distance = tmp_distance
        result = i

    # the closest one ist highlighted
    if not result == -1:
      self.FocusCone_.weak_highlight_edge(self.FocusEdge_,0)
      self.FocusEdge_ = result
      self.FocusCone_.weak_highlight_edge(self.FocusEdge_,1)

    self.update_focus_nodes()


  def focus_in_focuscone(self, selector):
    # look for the selector in the edges of the Focus Cone
    for i in range(len(self.FocusCone_.Edges_)):
      if self.FocusCone_.Edges_[i].geometry_ == selector:
        self.FocusCone_.highlight_edge(self.FocusEdge_,0)
        self.FocusEdge_ = i
        self.FocusCone_.highlight_edge(self.FocusEdge_,1)
        return True

    cones = []
    if self.FocusCone_.Parent_ == None:
      cones.append(self.FocusCone_)
    else:
      cones.append(self.FocusCone_.Parent_)
    
    for child in self.FocusCone_.ChildrenCones_:
        cones.append(child)

    # search for the selector in whole FocusCone
    while (not len(cones) == 0):
      current = cones.pop()
      # when found set highlighted
      if current.id_ == selector or current.Input_node_ == selector or current.outNode_.geometry_ == selector:
        # set new focus
        # self.FocusCone_.highlight_edge(self.FocusEdge_,0)
        self.FocusCone_.highlight_path(0)
        self.FocusCone_ = current
        self.FocusCone_.highlight_path(1)
        self.FocusEdge_ = -1
        self.update_focus_nodes()
        return True

    return False

  def focus_next_edge(self):
    if not self.FocusCone_.is_leaf():
      if not self.FocusEdge_ == -1:
        self.FocusCone_.highlight_edge(self.FocusEdge_,0)
      self.FocusEdge_ += 1
      if self.FocusEdge_ == len(self.FocusCone_.Edges_):
        self.FocusEdge_ = 0
      self.FocusCone_.highlight_edge(self.FocusEdge_,1)
      # self.update_label()

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
      # self.update_label()

  def go_deep_at_focus(self):
    if not (self.FocusCone_.is_leaf() or self.FocusEdge_ == -1):
      # reset focusi
      self.FocusCone_.highlight_path(0)
      self.FocusCone_.highlight_edge(self.FocusEdge_,0)
      # set new focus
      self.FocusCone_ = self.FocusCone_.ChildrenCones_[self.FocusEdge_]
      self.FocusCone_.highlight_path(1)
      self.FocusEdge_ = -1
      self.update_focus_nodes()
      # self.update_label()

  def level_up(self):
    if not self.FocusCone_.Parent_ == None:
      self.FocusCone_.highlight_path(0)
      if not self.FocusEdge_ == -1:
        self.FocusCone_.highlight_edge(self.FocusEdge_,0)
      self.FocusEdge_ = -1
      self.FocusCone_ = self.FocusCone_.Parent_
      self.FocusCone_.highlight_path(1)
      self.update_focus_nodes()
      # self.update_label()





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

