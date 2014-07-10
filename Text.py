
import avango
import avango.gua
import avango.script
from avango.script import field_has_changed

class TextField(avango.script.Script):

  sf_text = avango.SFString()
  sf_text.value = ""

  sf_transform = avango.gua.SFMatrix4()
  sf_transform.value = avango.gua.make_identity_mat()

  sf_char_width = avango.SFFloat()
  sf_char_width.value = 0.8

  sf_two_sided = avango.SFBool()
  sf_two_sided.value = False


  def __init__(self):
    self.super(TextField).__init__()


  def my_constructor(self, PARENT_NODE):
    # create group node for this text and append it to the given parent
    self.group_node = avango.gua.nodes.TransformNode(Name = "TextField")
    self.group_node.Transform.connect_from(self.sf_transform)
    PARENT_NODE.Children.value.append(self.group_node)


  def get_only_printables(self, text):
    return ''.join([char for char in text if ord(char) > 31 and ord(char) < 126])


  @field_has_changed(sf_text)
  def text_updated(self):
    self.group_node.Name.value = self.get_only_printables(self.sf_text.value)
    self.create_quads()


  @field_has_changed(sf_char_width)
  def char_width_updated(self):
    self.create_quads()


  @field_has_changed(sf_two_sided)
  def two_sided_updated(self):
    self.create_quads()


  def create_quads(self):
    loader = avango.gua.nodes.TriMeshLoader()

    text = [self.get_only_printables(line) for line in self.sf_text.value.split('\n')]

    quads = []
    for linenum, line in enumerate(text):
      # remove everything but the printable ascii characters
      for charnum, char in enumerate(line):
        material = "data/materials/font/" + str(ord(char)) + ".gmd"

        trans_vec = avango.gua.Vec3(0.5 + charnum * self.sf_char_width.value, -0.5 -linenum, 0.0)

        quad_front = loader.create_geometry_from_file("char" + str(charnum), "data/objects/quad.obj", material, avango.gua.LoaderFlags.DEFAULTS)
        quad_front.Transform.value = avango.gua.make_trans_mat(trans_vec)
        quads.append(quad_front)

        if self.sf_two_sided.value:
          back_trans_vec = avango.gua.Vec3(0.5 + len(line) * self.sf_char_width.value - trans_vec.x, trans_vec.y, trans_vec.z)
          quad_back = loader.create_geometry_from_file("char" + str(charnum), "data/objects/quad.obj", material, avango.gua.LoaderFlags.DEFAULTS)
          quad_back.Transform.value = avango.gua.make_trans_mat(0.5 + len(line) * self.sf_char_width.value, 0.0, 0.0) * avango.gua.make_rot_mat(180.0, 0.0, 1.0, 0.0) * avango.gua.make_trans_mat(trans_vec)
          quads.append(quad_back)

    self.group_node.Children.value = quads
