import multiprocessing as mp
import os
from unittest import skipIf

from hexrd import config
from .common import YmlTestCase


reference_data = \
"""
analysis_name: analysis_1
---
analysis_name: analysis_2
working_dir: %s
multiprocessing: -1
---
working_dir: an_unlikely_name_for_a_directory
multiprocessing: all
---
multiprocessing: half
---
multiprocessing: 2
---
multiprocessing: 1000
---
multiprocessing: -1000
---
multiprocessing: foo
""" % os.path.abspath('..')

print os.path.abspath('..')


class TestConfig(YmlTestCase):

    @classmethod
    def get_reference_data(cls):
        return reference_data

    def test_analysis_name(self):
        self.assertEqual(self.cfg.analysis_name, 'analysis_1')
        self.assertEqual(self.cfgs[1].analysis_name, 'analysis_2')

    def test_section_inheritance(self):
        self.assertEqual(self.cfg.analysis_name, 'analysis_1')
        self.assertEqual(self.cfgs[1].analysis_name, 'analysis_2')
        # the third section does not specify the working dir
        # should inherit the value from the first section, *not* the second
        self.assertEqual(self.cfgs[2].analysis_name, 'analysis_1')


    def test_working_dir(self):
        self.assertEqual(self.cfg.working_dir, os.getcwd())
        self.assertEqual(self.cfgs[1].working_dir, os.path.abspath('..'))
        def get_wd(cfg):
            return cfg.working_dir
        self.assertRaises(IOError, get_wd, self.cfgs[2])

    @skipIf(mp.cpu_count() < 2, 'test requires at least two cores')
    def test_multiprocessing(self):
        ncpus = mp.cpu_count()
        self.assertEqual(self.cfg.multiprocessing, ncpus - 1)
        self.assertEqual(self.cfgs[1].multiprocessing, ncpus - 1)
        self.assertEqual(self.cfgs[2].multiprocessing, ncpus)
        self.assertEqual(self.cfgs[3].multiprocessing, ncpus/2)
        self.assertEqual(self.cfgs[4].multiprocessing, 2)
        self.assertEqual(self.cfgs[5].multiprocessing, ncpus)
        self.assertEqual(self.cfgs[6].multiprocessing, 1)
        self.assertEqual(self.cfgs[7].multiprocessing, ncpus-1)
