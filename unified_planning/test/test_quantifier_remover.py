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


import os
import unified_planning
from unified_planning.environment import get_env
from unified_planning.shortcuts import *
from unified_planning.model.problem_kind import classical_kind, full_classical_kind, basic_temporal_kind, full_numeric_kind, hierarchical_kind
from unified_planning.test import TestCase, skipIfNoPlanValidatorForProblemKind, skipIfNoOneshotPlannerForProblemKind
from unified_planning.test.examples import get_example_problems
from unified_planning.transformers import QuantifiersRemover



class TestQuantifiersRemover(TestCase):
    def setUp(self):
        TestCase.setUp(self)
        self.problems = get_example_problems()

    @skipIfNoOneshotPlannerForProblemKind(classical_kind)
    @skipIfNoPlanValidatorForProblemKind(full_classical_kind)
    def test_basic_exists(self):
        problem = self.problems['basic_exists'].problem
        qr = QuantifiersRemover(problem)
        uq_problem = qr.get_rewritten_problem()
        uq_problem_2 = qr.get_rewritten_problem()
        self.assertEqual(uq_problem, uq_problem_2)
        self.assertTrue(problem.kind.has_existential_conditions())
        self.assertFalse(uq_problem.kind.has_existential_conditions())
        self.assertEqual(len(problem.actions), len(uq_problem.actions))

        with OneshotPlanner(problem_kind=uq_problem.kind) as planner:
            self.assertNotEqual(planner, None)
            uq_plan = planner.solve(uq_problem).plan
            new_plan = qr.rewrite_back_plan(uq_plan)
            with PlanValidator(problem_kind=problem.kind) as pv:
                self.assertTrue(pv.validate(problem, new_plan))

    @skipIfNoOneshotPlannerForProblemKind(classical_kind)
    @skipIfNoPlanValidatorForProblemKind(full_classical_kind)
    def test_basic_forall(self):
        problem = self.problems['basic_forall'].problem
        qr = QuantifiersRemover(problem)
        uq_problem = qr.get_rewritten_problem()
        self.assertTrue(problem.kind.has_universal_conditions())
        self.assertFalse(uq_problem.kind.has_universal_conditions())
        self.assertEqual(len(problem.actions), len(uq_problem.actions))

        with OneshotPlanner(problem_kind=uq_problem.kind) as planner:
            self.assertNotEqual(planner, None)
            uq_plan = planner.solve(uq_problem).plan
            new_plan = qr.rewrite_back_plan(uq_plan)
            with PlanValidator(problem_kind=problem.kind) as pv:
                self.assertTrue(pv.validate(problem, new_plan))

    @skipIfNoOneshotPlannerForProblemKind(classical_kind.union(full_numeric_kind))
    @skipIfNoPlanValidatorForProblemKind(full_classical_kind.union(full_numeric_kind))
    def test_robot_locations_connected(self):
        problem = self.problems['robot_locations_connected'].problem
        qr = QuantifiersRemover(problem)
        uq_problem = qr.get_rewritten_problem()
        self.assertTrue(problem.kind.has_existential_conditions())
        self.assertFalse(uq_problem.kind.has_existential_conditions())
        self.assertEqual(len(problem.actions), len(uq_problem.actions))

        with OneshotPlanner(problem_kind=uq_problem.kind) as planner:
            self.assertNotEqual(planner, None)
            uq_plan = planner.solve(uq_problem).plan
            new_plan = qr.rewrite_back_plan(uq_plan)
            with PlanValidator(problem_kind=problem.kind) as pv:
                self.assertTrue(pv.validate(problem, new_plan))

    @skipIfNoOneshotPlannerForProblemKind(classical_kind.union(full_numeric_kind))
    @skipIfNoPlanValidatorForProblemKind(full_classical_kind.union(full_numeric_kind))
    def test_robot_locations_visited(self):
        problem = self.problems['robot_locations_visited'].problem
        qr = QuantifiersRemover(problem)
        uq_problem = qr.get_rewritten_problem()
        self.assertTrue(problem.kind.has_existential_conditions())
        self.assertFalse(uq_problem.kind.has_existential_conditions())
        self.assertTrue(problem.kind.has_universal_conditions())
        self.assertFalse(uq_problem.kind.has_universal_conditions())
        self.assertEqual(len(problem.actions), len(uq_problem.actions))

        with OneshotPlanner(problem_kind=uq_problem.kind) as planner:
            self.assertNotEqual(planner, None)
            uq_plan = planner.solve(uq_problem).plan
            new_plan = qr.rewrite_back_plan(uq_plan)
            with PlanValidator(problem_kind=problem.kind) as pv:
                self.assertTrue(pv.validate(problem, new_plan))


    def test_hierarchical_blocks_world_exists(self):
        problem = self.problems['hierarchical_blocks_world_exists'].problem
        qr = QuantifiersRemover(problem)
        uq_problem = qr.get_rewritten_problem()
        self.assertTrue(problem.kind.has_existential_conditions())
        self.assertFalse(uq_problem.kind.has_existential_conditions())
        self.assertTrue(uq_problem.kind.has_disjunctive_conditions())
        self.assertFalse(problem.kind.has_disjunctive_conditions())
        self.assertIn('(on(block_1, block_1) or on(block_2, block_1) or on(block_3, block_1))', str(uq_problem.goals))

    @skipIfNoOneshotPlannerForProblemKind(classical_kind.union(basic_temporal_kind))
    def test_timed_connected_locations(self):
        problem = self.problems['timed_connected_locations'].problem
        qr = QuantifiersRemover(problem)
        uq_problem = qr.get_rewritten_problem()
        self.assertTrue(problem.kind.has_existential_conditions())
        self.assertFalse(uq_problem.kind.has_existential_conditions())
        self.assertEqual(len(problem.actions), len(uq_problem.actions))

        with OneshotPlanner(problem_kind=uq_problem.kind) as planner:
            self.assertNotEqual(planner, None)
            uq_plan = planner.solve(uq_problem).plan
            new_plan = qr.rewrite_back_plan(uq_plan)
            for (s, a, d), (s_1, a_1, d_1) in zip(new_plan.actions, uq_plan.actions):
                self.assertEqual(s, s_1)
                self.assertEqual(d, d_1)
                self.assertIn(a.action, problem.actions)

    def test_ad_hoc_1(self):
        Obj = UserType('Obj')
        x = Fluent('x')
        y = Fluent('y', BoolType(), obj=Obj)
        o = Variable('o', Obj)
        a = InstantaneousAction('a')
        o1 = Object('o1', Obj)
        o2 = Object('o2', Obj)
        o3 = Object('o3', Obj)
        a.add_effect(x, True, Exists(FluentExp(y, [o]), o))
        da = DurativeAction('da')
        da.add_effect(StartTiming(), x, True, Forall(FluentExp(y, [o]), o))
        problem = Problem('ad_hoc')
        problem.add_fluent(x)
        problem.add_fluent(y)
        problem.add_action(a)
        problem.add_action(da)
        problem.add_object(o1)
        problem.add_object(o2)
        problem.add_object(o3)
        problem.add_timed_effect(GlobalStartTiming(4), x, Forall(FluentExp(y, [o]), o), Exists(FluentExp(y, [o]), o))
        problem.add_timed_goal(GlobalStartTiming(6), x)
        problem.add_timed_goal(OpenTimeInterval(GlobalStartTiming(8), GlobalStartTiming(10)), x)
        problem.set_initial_value(x, False)
        problem.set_initial_value(y(o1), True)
        problem.set_initial_value(y(o2), False)
        problem.set_initial_value(y(o3), True)
        problem.add_goal(x)
        qr = QuantifiersRemover(problem)
        unq_problem = qr.get_rewritten_problem()
        self.assertTrue(problem.kind.has_existential_conditions())
        self.assertTrue(problem.kind.has_universal_conditions())
        self.assertFalse(unq_problem.kind.has_existential_conditions())
        self.assertFalse(unq_problem.kind.has_universal_conditions())
        unq_as = qr.get_transformed_actions(a)
        self.assertEqual(len(unq_as), 1)
        unq_a = unq_as[0]
        self.assertTrue(unq_a.effects[0].condition.is_or())
        unq_das = qr.get_transformed_actions(da)
        self.assertEqual(len(unq_das), 1)
        unq_da = unq_das[0]
        self.assertTrue((unq_da.effects[StartTiming()])[0].condition.is_and())
