#  This file is part of Pynguin.
#
#  SPDX-FileCopyrightText: 2019–2020 Pynguin Contributors
#
#  SPDX-License-Identifier: LGPL-3.0-or-later
#
import ast

import pytest

from pynguin.analyses.seeding.initialpopulationseeding import _TestTransformer
from pynguin.generation.export.exportprovider import ExportProvider
from pynguin.setup.testclustergenerator import TestClusterGenerator


# TODO(fk) this is not correct, i.e. in the second example str3 should be dict0 and var0
#  should be list0. However, this is a more complex problem in AST -> Statement
#  conversion.
@pytest.mark.parametrize(
    "testcase_seed",
    [
        (
            """    float0 = 1.1
    var0 = module0.positional_only(float0)
"""
        ),
        (
            """    float0 = 1.1
    int0 = 42
    var0 = []
    str0 = 'test'
    str1 = 'key'
    str2 = 'value'
    str3 = {str1: str2}
    var1 = module0.all_params(float0, int0, *var0, param4=str0, **str3)
"""
        ),
    ],
)
def test_parameter_mapping_roundtrip(testcase_seed, tmp_path):
    testcase_seed = (
        """# Automatically generated by Pynguin.
import tests.fixtures.grammar.parameters as module0


def test_case_0():
"""
        + testcase_seed
    )
    test_cluster = TestClusterGenerator(
        "tests.fixtures.grammar.parameters"
    ).generate_cluster()
    transformer = _TestTransformer(test_cluster)
    transformer.visit(ast.parse(testcase_seed))
    export_path = tmp_path / "export.py"
    ExportProvider.get_exporter().export_sequences(export_path, transformer.testcases)
    with open(export_path) as f:
        content = f.read()
        assert content == testcase_seed
