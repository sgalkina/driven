# Copyright 2015 Novo Nordisk Foundation Center for Biosustainability, DTU.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import unittest
import os
import numpy as np
from driven.data_sets.expression_profile import ExpressionProfile
from driven.flux_analysis.transcriptomics import gimme, imat


CURDIR = os.path.dirname(__file__)


class TranscriptomicsTestCase(unittest.TestCase):
    def setUp(self):
        variables = {}

        # Blazier et al toy model and mock expression set can be use to test GIMME, iMAT, MADE, E-flux and PROM
        execfile(os.path.join(CURDIR, "assets", "blazier_et_al_2012.py"), variables)
        self._blazier_model = variables["model"]
        self._blazier_expression = variables["expression_profile"]

        # Toy model from iMAT publication
        execfile(os.path.join(CURDIR, "assets", "zur_et_al_2010.py"), variables)
        self._zur_et_al_model = variables["model"]
        self._zur_et_al_expression = variables["expression_profile"]

    def test_gimme(self):
        model = self._blazier_model
        gimme_res_025 = gimme(model=model, expression_profile=self._blazier_expression,
                              cutoff=0.25, fraction_of_optimum=0.4)

        self.assertEqual(gimme_res_025.inconsistency_score, .0)
        gimme_res_050 = gimme(model=model, expression_profile=self._blazier_expression,
                              cutoff=0.5, fraction_of_optimum=0.4)

        self.assertGreater(gimme_res_050.inconsistency_score, .0)

    def test_imat(self):
        model = self._blazier_model
        imat_res_025_075 = imat(model, self._blazier_expression, low_cutoff=0.25, high_cutoff=0.75, condition="Exp#2")
        print imat_res_025_075.data_frame

        self.assertTrue(all([imat_res_025_075[r] == 0 for r in ["R1", "R2"]]))
        self.assertTrue(all([imat_res_025_075[r] != 0 for r in ["R3", "R4", "R5", "R6", "R7", "R8"]]))

        imat_res_050_075 = imat(model, self._blazier_expression, low_cutoff=0.50, high_cutoff=0.75, condition="Exp#2")
        print imat_res_050_075.data_frame
        self.assertTrue(all([imat_res_050_075[r] == 0 for r in ["R1", "R2", "R3", "R4"]]))
        self.assertTrue(all([imat_res_050_075[r] != 0 for r in ["R5", "R6", "R8"]]))

    @unittest.skip("Not implemented")
    def test_made(self):
        raise NotImplementedError

    @unittest.skip("Not implemented")
    def test_eflux(self):
        raise NotImplementedError

    @unittest.skip("Not implemented")
    def test_relatch(self):
        raise NotImplementedError

    @unittest.skip("Not implemented")
    def test_gx_fba(self):
        raise NotImplementedError

    @unittest.skip("Not implemented")
    def test_prom(self):
        raise NotImplementedError


class ThermodynamicsTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_(self):
        pass


class C13TestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_fba(self):
        pass


class ExpressionProfileTestCase(unittest.TestCase):
    def test_difference(self):
        genes = ["G1"]
        conditions = ["T1", "T2", "T3", "T4"]
        expression = np.zeros((1, 4))
        expression[0] = [10, 11, 65, 109]
        profile = ExpressionProfile(genes, conditions, expression)

        self.assertEqual(profile.differences, {"G1": [0, 1, 1]})