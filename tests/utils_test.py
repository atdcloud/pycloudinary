import pycloudinary.utils
import unittest

class TestUtils(unittest.TestCase):
  def setUp(self):
    pycloudinary.config(cloud_name = "test123", secure_distribution = None, private_cdn = False)
  
  def test_cloud_name(self):
    """should use cloud_name from config"""
    result, options = pycloudinary.utils.cloudinary_url("test")
    self.assertEqual(result, "http://res.cloudinary.com/test123/image/upload/test" )

  def test_cloud_name_options(self):
    """should allow overriding cloud_name in options"""
    options = {"cloud_name": "test321"}
    result, options = pycloudinary.utils.cloudinary_url("test", **options)
    self.assertEqual(options, {})
    self.assertEqual(result, "http://res.cloudinary.com/test321/image/upload/test" )
  
  def test_secure_distribution(self):
    """should use default secure distribution if secure=True"""    
    options = {"secure": True}
    result, options = pycloudinary.utils.cloudinary_url("test", **options)
    self.assertEqual(options, {})
    self.assertEqual(result, "https://d3jpl91pxevbkh.cloudfront.net/test123/image/upload/test" )

  def test_secure_distribution_overwrite(self):
    """should allow overwriting secure distribution if secure=True"""    
    options = {"secure": True, "secure_distribution": "something.else.com"}
    result, options = pycloudinary.utils.cloudinary_url("test", **options)
    self.assertEqual(options, {})
    self.assertEqual(result, "https://something.else.com/test123/image/upload/test" )

  def test_secure_distibution(self):
    """should take secure distribution from config if secure=True"""
    pycloudinary.config().secure_distribution = "config.secure.distribution.com"    
    options = {"secure": True}
    result, options = pycloudinary.utils.cloudinary_url("test", **options)
    self.assertEqual(options, {})
    self.assertEqual(result, "https://config.secure.distribution.com/test123/image/upload/test" )

  def test_missing_secure_distribution(self):
    """should raise exception if secure is given with private_cdn and no secure_distribution"""
    pycloudinary.config().private_cdn = True    
    with self.assertRaises(Exception):
      pycloudinary.utils.cloudinary_url("test", secure=True)

  def test_format(self):
    """should use format from options"""    
    options = {"format": "jpg"}
    result, options = pycloudinary.utils.cloudinary_url("test", **options)
    self.assertEqual(options, {})
    self.assertEqual(result, "http://res.cloudinary.com/test123/image/upload/test.jpg" )

  def test_crop(self):
    """should use width and height from options only if crop is given"""
    options = {"width": 100, "height": 100}
    result, options = pycloudinary.utils.cloudinary_url("test", **options)
    self.assertEqual(result, "http://res.cloudinary.com/test123/image/upload/test" )
    self.assertEqual(options, {"width": 100, "height": 100})
    options = {"width": 100, "height": 100, "crop": "crop"}
    result, options = pycloudinary.utils.cloudinary_url("test", **options)
    self.assertEqual(options, {"width": 100, "height": 100})
    self.assertEqual(result, "http://res.cloudinary.com/test123/image/upload/c_crop,h_100,w_100/test" )
  
  def test_various_options(self):
    """should use x, y, radius, prefix, gravity and quality from options"""    
    options = {"x": 1, "y": 2, "radius": 3, "gravity": "center", "quality": 0.4, "prefix": "a"}
    result, options = pycloudinary.utils.cloudinary_url("test", **options)
    self.assertEqual(options, {})
    self.assertEqual(result, "http://res.cloudinary.com/test123/image/upload/g_center,p_a,q_0.4,r_3,x_1,y_2/test" )
  
  def test_transformation_simple(self):
    """should support named tranformation"""    
    options = {"transformation": "blip"}
    result, options = pycloudinary.utils.cloudinary_url("test", **options)
    self.assertEqual(options, {})
    self.assertEqual(result, "http://res.cloudinary.com/test123/image/upload/t_blip/test" )

  def test_transformation_array(self):
    """should support array of named tranformations"""    
    options = {"transformation": ["blip", "blop"]}
    result, options = pycloudinary.utils.cloudinary_url("test", **options)
    self.assertEqual(options, {})
    self.assertEqual(result, "http://res.cloudinary.com/test123/image/upload/t_blip.blop/test" )

  def test_base_transformations(self):
    """should support base tranformation"""    
    options = {"transformation": {"x": 100, "y": 100, "crop": "fill"}, "crop": "crop", "width": 100}
    result, options = pycloudinary.utils.cloudinary_url("test", **options)
    self.assertEqual(options, {"width": 100})
    self.assertEqual(result, "http://res.cloudinary.com/test123/image/upload/c_fill,x_100,y_100/c_crop,w_100/test" )

  def test_base_transformation_array(self):
    """should support array of base tranformations"""    
    options = {"transformation": [{"x": 100, "y": 100, "width": 200, "crop": "fill"}, {"radius": 10}], "crop": "crop", "width": 100}
    result, options = pycloudinary.utils.cloudinary_url("test", **options)
    self.assertEqual(options, {"width": 100})
    self.assertEqual(result, "http://res.cloudinary.com/test123/image/upload/c_fill,w_200,x_100,y_100/r_10/c_crop,w_100/test" )

  def test_no_empty_transformation(self):
    """should not include empty tranformations"""    
    options = {"transformation": [{}, {"x": 100, "y": 100, "crop": "fill"}, {}]}
    result, options = pycloudinary.utils.cloudinary_url("test", **options)
    self.assertEqual(options, {})
    self.assertEqual(result, "http://res.cloudinary.com/test123/image/upload/c_fill,x_100,y_100/test" )

  def test_size(self):
    """should support size"""    
    options = {"size": "10x10", "crop": "crop"}
    result, options = pycloudinary.utils.cloudinary_url("test", **options)
    self.assertEqual(options, {"width": "10", "height": "10"})
    self.assertEqual(result, "http://res.cloudinary.com/test123/image/upload/c_crop,h_10,w_10/test" )

  def test_type(self):
    """should use type from options"""
    options = {"type": "facebook"}
    result, options = pycloudinary.utils.cloudinary_url("test", **options)
    self.assertEqual(options, {})
    self.assertEqual(result, "http://res.cloudinary.com/test123/image/facebook/test" )

  def test_resource_type(self):
    """should use resource_type from options"""
    options = {"resource_type": "raw"}
    result, options = pycloudinary.utils.cloudinary_url("test", **options)
    self.assertEqual(options, {})
    self.assertEqual(result, "http://res.cloudinary.com/test123/raw/upload/test" )

  def test_ignore_http(self):
    """should ignore http links only if type is not given or is asset"""
    options = {}
    result, options = pycloudinary.utils.cloudinary_url("http://test", **options)
    self.assertEqual(options, {})
    self.assertEqual(result, "http://test" )
    options = {"type": "asset"}
    result, options = pycloudinary.utils.cloudinary_url("http://test", **options)
    self.assertEqual(options, {})
    self.assertEqual(result, "http://test" )
    options = {"type": "fetch"}
    result, options = pycloudinary.utils.cloudinary_url("http://test", **options)
    self.assertEqual(options, {})
    self.assertEqual(result, "http://res.cloudinary.com/test123/image/fetch/http://test" )

  def test_fetch(self):
    """should escape fetch urls"""
    options = {"type": "fetch"}
    result, options = pycloudinary.utils.cloudinary_url("http://blah.com/hello?a=b", **options)
    self.assertEqual(options, {})
    self.assertEqual(result, "http://res.cloudinary.com/test123/image/fetch/http://blah.com/hello%3Fa%3Db" )

  def test_background(self):
    """should support background"""
    options = {"background": "red"}
    result, options = pycloudinary.utils.cloudinary_url("test", **options)
    self.assertEqual(options, {})
    self.assertEqual(result, "http://res.cloudinary.com/test123/image/upload/b_red/test" )
    options = {"background": "#112233"}
    result, options = pycloudinary.utils.cloudinary_url("test", **options)
    self.assertEqual(options, {})
    self.assertEqual(result, "http://res.cloudinary.com/test123/image/upload/b_rgb:112233/test" )
  
  def test_default_image(self):
    """should support default_image"""
    options = {"default_image": "default"}
    result, options = pycloudinary.utils.cloudinary_url("test", **options)
    self.assertEqual(options, {})
    self.assertEqual(result, "http://res.cloudinary.com/test123/image/upload/d_default/test" )

if __name__ == '__main__':
    unittest.main()

