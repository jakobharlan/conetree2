import avango
import avango.gua
import math

import Edge
import Node
import ConeTree

# Cone Class
class Cone:
  id_counter_ = 0

  def __init__(self, inNode, parent, level = 1):
    # Radius of this cone for layout calculation, an one for the actual rendering
    self.Renderd_Radius_ = 2
    self.Radius_ = 2
    # Angle this Cone has in its parent Cone
    self.Angle_ = 0
    # Angle this Cone is turned
    self.Rotation_ = 0
    # Level and Depth
    self.Level_ = level
    self.Depth_ = 5 + (20.0 / self.Level_)
    # The Represented Scenegraph Node
    self.Input_node_ = inNode
    # The CT Node
    self.outNode_ = Node.Node(material = self.select_material())
    # Link back up to the Parent
    self.Parent_ = parent
    # List for the Children Cones
    self.ChildrenCones_ = []
    # List for the Edges
    self.Edges_ = []
    # disc for Cones with only leafs
    self.disc_ = None
    # unique ID for every Cone
    Cone.id_counter_ += 1
    self.id_ = Cone.id_counter_
    # a flag to collapse / highlight  this cone
    self.collapsed_ = False
    self.highlighted_ = False

    # build Children Cones
    for child in inNode.Children.value:
      tmp_cone = Cone(child, self, self.Level_ + 1)
      self.ChildrenCones_.append(tmp_cone)
      self.Edges_.append(Edge.Edge(self.outNode_, tmp_cone.outNode_))


  def is_leaf(self):
    if (len(self.ChildrenCones_)  == 0) or self.collapsed_:
      return True
    return False

  def is_pre_leaf(self):
    for child in self.ChildrenCones_:
      if not child.is_leaf():
        return False
    return True

  def collapse(self, collapsed):
    self.collapsed_ = collapsed
    if self.collapsed_:
      self.outNode_.geometry_.Children.value = []

      loader = avango.gua.nodes.TriMeshLoader()
      cone = loader.create_geometry_from_file(
        "cone",
        "data/objects/cone.obj",
        "data/materials/Red.gmd",
        avango.gua.LoaderFlags.DEFAULTS
      )
      cone.Transform.value = avango.gua.make_scale_mat(2)
      self.outNode_.geometry_.Children.value.append(cone)
    else:
      self.outNode_.geometry_.Children.value = []

      for child in self.ChildrenCones_:
        child_node = child.outNode_.geometry_
        self.outNode_.geometry_.Children.value.append(child_node)
      for edge in self.Edges_:
        self.outNode_.geometry_.Children.value.append(edge.geometry_)

  def rotate(self, angle):
    self.Rotation_ += angle

  def highlight(self, highlight):
    self.highlighted_ = highlight
    if self.highlighted_:
      self.outNode_.set_material("data/materials/White.gmd")
    else:
      self.outNode_.reset_material()
    self.outNode_.apply_Transform()

  def highlight_path(self, highlight):
    self.highlight(highlight)
    if not self.Parent_ == None:
      for edge in self.Parent_.Edges_:
        if edge.To_ == self.outNode_:  # look for the edge linking parent and this Cone
          edge.highlight(highlight) # highlight it
      self.Parent_.highlight_path(highlight)

  def highlight_edge(self, edge_number, highlight):
      self.Edges_[edge_number].highlight(highlight)
      
  def weak_highlight_edge(self, edge_number, highlight):
      self.Edges_[edge_number].weak_highlight(highlight)

  def get_scenegraph(self):
    if self.is_leaf():
      self.outNode_.geometry_.Children.value = []
    else:
      for child in self.ChildrenCones_:
        child_node = child.get_scenegraph()
        self.outNode_.geometry_.Children.value.append(child_node)
      for edge in self.Edges_:
        self.outNode_.geometry_.Children.value.append(edge.geometry_)

    return self.outNode_.geometry_

  def print_cone(self, depth):
    for i in range(depth):
      print " ",
    print str(self.id_) + ": ",
    if self.collapsed_:
      print "COLLAPSED ",
    print "Radius: " + str(self.Radius_) + " ",
    print "Angle: " + str(self.Angle_) + " ",
    print "Pos: " + str(self.outNode_.position_)
    for child in self.ChildrenCones_:
      child.print_cone(depth+1)

  def make_disc(self):
    loader = avango.gua.nodes.TriMeshLoader()
    self.disc_ = loader.create_geometry_from_file(
      "disc" + str(self.id_),
      "data/objects/disc.obj",
      "data/materials/DarkGrey.gmd",
      avango.gua.LoaderFlags.DEFAULTS
    )
    self.outNode_.geometry_.Children.value.append(self.disc_)
    self.update_disc()

  def update_disc(self):
    if  self.disc_== None:
      self.make_disc()
    if not (self.disc_ in self.outNode_.geometry_.Children.value):
      self.outNode_.geometry_.Children.value.append(self.disc_)
    self.disc_.Transform.value = avango.gua.make_trans_mat(0,-(self.Depth_ + 1),0) * avango.gua.make_scale_mat(self.Radius_ * 0.75)

  def layout(self):
    # if this cone has no Children, reset the Radius
    if self.is_leaf():
      self.Radius_ = 2
    else:

      # first call the function on the children, bottom up!
      for child in self.ChildrenCones_:
        child.layout()

      # then commence with layout
      _circumference = 0

      for child in self.ChildrenCones_:
        _circumference += child.Radius_
      _circumference *= 2

      self.Radius_ = _circumference / (2 * math.pi )

      # calculate the angle for the Childcones and the maximum Radius
      _angle_sum = self.Rotation_
      _max_radius = 0.0
      for i in range(len(self.ChildrenCones_)):
        # first Child starts with a fixed Angle
        if i == 0:
          self.ChildrenCones_[0].Angle_ = _angle_sum
        else:
          s = self.ChildrenCones_[i-1].Radius_ + self.ChildrenCones_[i].Radius_
          part_angle = s/(self.Radius_)

          _angle_sum += part_angle
          self.ChildrenCones_[i].Angle_ = _angle_sum

        if self.ChildrenCones_[i].Radius_ > _max_radius:
          _max_radius = self.ChildrenCones_[i].Radius_

      # adjust the Radius
      self.Renderd_Radius_ = self.Radius_
      self.Radius_ += _max_radius
      # self.Radius_ *= 3 * (_max_radius/self.Radius_) * (1.0 /len(self.ChildrenCones_))

      # check if there should be a disc
      if self.is_pre_leaf():
        self.update_disc()
      else:
        self.outNode_.geometry_.Children.value.remove(self.disc_)


  def apply_layout(self, parent_radius = 0, root = False):
    if root:
      self.outNode_.set_position(avango.gua.Vec3(0,0,0))
    elif self.Parent_.is_pre_leaf():
      self.outNode_.set_position(avango.gua.Vec3(
        math.cos(self.Angle_) * parent_radius * 0.75,
        -self.Depth_,
        math.sin(self.Angle_) * parent_radius * 0.75))
    else:
      self.outNode_.set_position(avango.gua.Vec3(
        math.cos(self.Angle_) * parent_radius,
        -self.Depth_,
        math.sin(self.Angle_) * parent_radius))

    # self.outNode_.set_rotation(self.Rotation_)

    for child in self.ChildrenCones_:
      child.apply_layout(parent_radius = self.Renderd_Radius_)
    for edge in self.Edges_:
      edge.refresh_position()

  def reapply_material(self):
    self.outNode_.set_material(self.select_material(), temporary = False)
    for child in self.ChildrenCones_:
      child.reapply_material()

  # chooses a material, based on wich node is given
  # or wich depth the node is at
  def select_material(self):
    if ConeTree.ConeTree.COLORMODE == "NODETYPE":
      if type(self.Input_node_) == avango.gua._gua.TriMeshNode :
        return "data/materials/Red.gmd"
      if type(self.Input_node_) == avango.gua._gua.TransformNode :
        return "data/materials/Blue.gmd"
      if type(self.Input_node_) == avango.gua._gua.PointLightNode :
        return "data/materials/Yellow.gmd"
      if type(self.Input_node_) == avango.gua._gua.ScreenNode :
        return "data/materials/Orange.gmd"

    elif ConeTree.ConeTree.COLORMODE == "DEPTH":
      if self.Level_ % 7 == 1 :
        return "data/materials/Red.gmd"
      if self.Level_ % 7 == 2 :
        return "data/materials/Orange.gmd"
      if self.Level_ % 7 == 3 :
        return "data/materials/Yellow.gmd"
      if self.Level_ % 7 == 4 :
        return "data/materials/Green.gmd"
      if self.Level_ % 7 == 5 :
        return "data/materials/Cyan.gmd"
      if self.Level_ % 7 == 6 :
        return "data/materials/Blue.gmd"
      if self.Level_ % 7 == 0 :
        return "data/materials/Violet.gmd"



    return "data/materials/White.gmd"
