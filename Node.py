import avango
import avango.gua
import math

# Node Class
class Node:

  def __init__(self, postition = avango.gua.Vec3(0,0,0), material = "data/materials/Blue.gmd"):
    self.position_ = postition
    self.material_ = material

    loader = avango.gua.nodes.TriMeshLoader()
    self.geometry_ = loader.create_geometry_from_file(
      "sphere",
      "data/objects/sphere.obj",
      self.material_,
      avango.gua.LoaderFlags.DEFAULTS
    )
    self.apply_position()

  def set_position(self, position = avango.gua.Vec3(0,0,0)):
    self.position_ = position
    self.apply_position()

  def apply_position(self):
    self.geometry_.Transform.value = avango.gua.make_trans_mat(self.position_)

  def set_material(self, material, temporary = True):
    if temporary:
      self.geometry_.Material.value = material
    else:
      self.material_ = material
      self.reset_material()

  def reset_material(self):
    self.geometry_.Material.value = self.material_
