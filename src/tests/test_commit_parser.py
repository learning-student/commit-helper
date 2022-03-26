import unittest

from src.parser import get_environment_parameter_operation, try_to_get_type_and_group_from_commit


class TestCommitParser(unittest.TestCase):
    def test_try_to_get_type_and_group_from_commit_does_not_exists(self):
        test_string = """test string --env-added=TEST_ENV--"""
        output = try_to_get_type_and_group_from_commit(test_string)
        assert output is None
    def test_try_to_get_type_and_group_from_commit_when_exists(self):
        test_string = """feat(test): test string --env-added=TEST_ENV--"""
        output = try_to_get_type_and_group_from_commit(test_string)
        assert output is not None
        assert output["group"] is not None and output['type'] is not None

    def test_get_added_environment_parameters_parsers_correctly_with_one_parameter(self):
        test_string = """feat(test): test string --env-added=TEST_ENV--"""
        output = get_environment_parameter_operation(test_string)
        assert len(output) == 1

    def test_get_added_environment_parameters_parsers_correctly_with_multiple_parameters(self):
        test_string = """feat(test): test string --env-added=TEST_ENV-- asdas test tasdsad --env-added=OUTPUT_TEST--"""
        output = get_environment_parameter_operation(test_string)
        assert len(output) == 2
        assert "TEST_ENV" in output

    def test_get_changed_environment_parameters_parsers_correctly_with_one_parameter(self):
        test_string = """feat(test): test string --env-changed=TEST_ENV--"""
        output = get_environment_parameter_operation(test_string, type="changed")
        assert len(output) == 1
        assert "TEST_ENV" in output

    def test_get_changed_environment_parameters_parsers_correctly_with_multiple_parameters(self):
        test_string = """feat(test): test string --env-changed=TEST_ENV-- asdas test tasdsad --env-changed=OUTPUT_TEST--"""
        output = get_environment_parameter_operation(test_string, type="changed")
        assert len(output) == 2
        assert "TEST_ENV" in output and "OUTPUT_TEST" in output



