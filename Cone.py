import avango
import avango.gua
import math

import Edge
import Node

# Cone Class
class Cone:
  id_counter_ = 0

  def __init__(self, inNode):
    # Radius of this cone
    self.Radius_ = 2
    # Angle this Cone has in its parent Cone
    self.Angle_ = 0
    # The Represented Scenegraph Node
    self.Input_node_ = inNode
    # The CT Node
    self.outNode_ = Node.Node()
    # List for the Children Cones
    self.ChildrenCones_ = []
    # List for the Edges
    self.Edges_ = []
    Cone.id_counter_ += 1
    # unique ID for every Cone
    self.id_ = Cone.id_counter_
    # a flag to collaps at this cone
    self.collapsed_ = False

    # build Children COnes
    for child in inNode.Children.value:
      tmp_cone = Cone(child)
      self.ChildrenCones_.append(tmp_cone)
      self.Edges_.append(Edge.Edge(self.outNode_, tmp_cone.outNode_))

  def is_leaf(self):
    if len(self.ChildrenCones_)  == 0:
      return True
    if self.collapsed_:
      return True
    return False

  def collapse(self, collapsed):
    self.collapsed_ = collapsed
    if self.collapsed_:
      self.outNode_.geometry_.Children.value = []

      loader = avango.gua.nodes.TriMeshLoader()
      box = loader.create_geometry_from_file(
        "box", 
        "data/objects/cube.obj",
        "data/materials/Blue.gmd",
        avango.gua.LoaderFlags.DEFAULTS
      ) 
      box.Transform.value = avango.gua.make_trans_mat(0,-1,0)
      self.outNode_.geometry_.Children.value.append(box)
    else:
      self.outNode_.geometry_.Children.value = []
      for child in self.ChildrenCones_:
        child_node = child.outNode_.geometry_
        self.outNode_.geometry_.Children.value.append(child_node)
      for edge in self.Edges_:
        self.outNode_.geometry_.Children.value.append(edge.geometry_)


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
      _angle_sum = 0.0
      _max_radius = 0.0
      for i in range(len(self.ChildrenCones_)):
        # first Child starts with a fixed Angle
        if i == 0:
          self.ChildrenCones_[0].Angle_ = 0
        else:
          s = self.ChildrenCones_[i-1].Radius_ + self.ChildrenCones_[i].Radius_
          part_angle = s/(self.Radius_)
        
          _angle_sum += part_angle
          self.ChildrenCones_[i].Angle_ = _angle_sum

        if self.ChildrenCones_[i].Radius_ > _max_radius:
          _max_radius = self.ChildrenCones_[i].Radius_

    # adjust the Radius
    # self.Radius_ += _max_radius

  def apply_layout(self, parent_radius = 0, root = False):
    if root:
      self.outNode_.set_position(avango.gua.Vec3(0,0,0))
    else:
      self.outNode_.set_position(avango.gua.Vec3(
        math.cos(self.Angle_) * parent_radius,
        -7,
        math.sin(self.Angle_) * parent_radius))
    for child in self.ChildrenCones_:
      child.apply_layout(parent_radius = self.Radius_)
    for edge in self.Edges_:
      edge.refresh_position()

