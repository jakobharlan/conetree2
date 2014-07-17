import avango
import avango.gua
import math

# Edge Class
class Edge:

  def __init__(self, first, to):
    self.From_ = first
    self.To_ = to
    loader = avango.gua.nodes.TriMeshLoader()
    self.geometry_ = loader.create_geometry_from_file(
      "cube",
      "data/objects/cube.obj",
      "data/materials/Grey.gmd",
      avango.gua.LoaderFlags.DEFAULTS
    )
    self.refresh_position()

  def refresh_position(self):
    self.geometry_.Transform.value = calc_transform_connection(avango.gua.Vec3(0,0,0) , self.To_.position_)

  def highlight(self, highlight):
    if highlight:
      self.geometry_.Material.value = "data/materials/White.gmd"
    else:
      self.geometry_.Material.value = "data/materials/Grey.gmd"


def get_rotation_between_vectors(VEC1, VEC2):

  VEC1.normalize()
  VEC2.normalize()

  _angle = math.degrees(math.acos(VEC1.dot(VEC2)))
  _axis = VEC1.cross(VEC2)

  return avango.gua.make_rot_mat(_angle, _axis)

def calc_transform_connection(START_VEC, END_VEC):

  # calc the vector in between the two points, the resulting center of the line segment and the scaling needed to connect both points
  _vec = avango.gua.Vec3( END_VEC.x - START_VEC.x, END_VEC.y - START_VEC.y, END_VEC.z - START_VEC.z)
  _center = START_VEC + (_vec * 0.5)
  _scale  = _vec.length()

  # calc the rotation according negative z-axis
  _rotation_mat = get_rotation_between_vectors(avango.gua.Vec3(0, 0, -1), _vec)

  # build the complete matrix
  return avango.gua.make_trans_mat(_center) * _rotation_mat * avango.gua.make_scale_mat(0.1, 0.1, _scale)
