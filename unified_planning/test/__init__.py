# Copyright 2021 AIPlan4EU project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest
import unified_planning as up
from functools import wraps
from unified_planning.environment import get_env
from unified_planning.model import ProblemKind
from unified_planning.test.pddl import enhsp


skipIf = unittest.skipIf
SkipTest = unittest.SkipTest


class skipIfSolverNotAvailable(object):
    """Skip a test if the given solver is not available."""

    def __init__(self, solver):
        self.solver = solver

    def __call__(self, test_fun):
        msg = "%s not available" % self.solver
        cond = self.solver not in get_env().factory.solvers
        @unittest.skipIf(cond, msg)
        @wraps(test_fun)
        def wrapper(*args, **kwargs):
            return test_fun(*args, **kwargs)
        return wrapper


class skipIfNoOneshotPlannerForProblemKind(object):
    """Skip a test if there are no oneshot planner for the given problem kind."""

    def __init__(self, kind: ProblemKind):
        self.kind = kind

    def __call__(self, test_fun):
        msg = "no oneshot planner available for the given problem kind"
        cond = False
        try:
            get_env().factory._get_solver_class('oneshot_planner', problem_kind=self.kind)
        except:
            cond = True
        @unittest.skipIf(cond, msg)
        @wraps(test_fun)
        def wrapper(*args, **kwargs):
            return test_fun(*args, **kwargs)
        return wrapper


class skipIfNoOneshotPlannerSatisfiesOptimalityGuarantee(object):
    """Skip a test if there are no oneshot planner satisfies optimality guarantee."""

    def __init__(self, optimality_guarantee: up.solvers.results.PlanGenerationResultStatus):
        self.optimality_guarantee = optimality_guarantee

    def __call__(self, test_fun):
        msg = "no oneshot planner available for the given optimality guarantee"
        cond = False
        try:
            get_env().factory._get_solver_class('oneshot_planner',
                                                optimality_guarantee=self.optimality_guarantee)
        except:
            cond = True
        @unittest.skipIf(cond, msg)
        @wraps(test_fun)
        def wrapper(*args, **kwargs):
            return test_fun(*args, **kwargs)
        return wrapper


class skipIfNoPlanValidatorForProblemKind(object):
    """Skip a test if there are no plan validator for the given problem kind."""

    def __init__(self, kind: ProblemKind):
        self.kind = kind

    def __call__(self, test_fun):
        msg = "no plan validator available for the given problem kind"
        cond = False
        try:
            get_env().factory._get_solver_class('plan_validator', problem_kind=self.kind)
        except:
            cond = True
        @unittest.skipIf(cond, msg)
        @wraps(test_fun)
        def wrapper(*args, **kwargs):
            return test_fun(*args, **kwargs)
        return wrapper

TestCase = unittest.TestCase
main = unittest.main
