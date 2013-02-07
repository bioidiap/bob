#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Andre Anjos <andre.anjos@idiap.ch>
# Tue 21 Aug 2012 13:30:54 CEST 

"""Test scripts in bob.visioner
"""

import os
import unittest
from ...test import utils
from ..script import facebox, facepoints
from ... import io, ip
from ...ip import test as iptest

MOVIE = utils.datafile('test.mov', io)
IMAGE = utils.datafile('test-faces.jpg', iptest, os.path.join('data', 'faceextract'))

class VisionerScriptTest(unittest.TestCase):

  @utils.ffmpeg_found()
  def test01_face_detect(self):
   
    # sanity checks
    self.assertTrue(os.path.exists(MOVIE))

    cmdline = '%s --self-test=1' % (MOVIE)
    self.assertEqual(facebox.main(cmdline.split()), 0)

  def test02_face_detect(self):
   
    # sanity checks
    self.assertTrue(os.path.exists(IMAGE))

    cmdline = '%s --self-test=2' % (IMAGE)
    self.assertEqual(facebox.main(cmdline.split()), 0)

  @utils.ffmpeg_found()
  def test03_keypoint_localization(self):
   
    # sanity checks
    self.assertTrue(os.path.exists(MOVIE))

    cmdline = '%s --self-test=1' % (MOVIE)
    self.assertEqual(facepoints.main(cmdline.split()), 0)

  def test04_keypoint_localization(self):
   
    # sanity checks
    self.assertTrue(os.path.exists(IMAGE))

    cmdline = '%s --self-test=2' % (IMAGE)
    self.assertEqual(facepoints.main(cmdline.split()), 0)
