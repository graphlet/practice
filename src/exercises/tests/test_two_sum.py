import pytest
from pathlib import Path
import importlib.util

# Path to the implementation (relative to this test file)
HERE = Path(__file__).parent
impl_path = HERE.parent / "core" / "two_sum.py"

if not impl_path.exists():
    raise FileNotFoundError(f"Expected implementation at {impl_path!s}")

spec = importlib.util.spec_from_file_location("two_sum_impl", impl_path)
two_sum_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(two_sum_mod)
two_sum = getattr(two_sum_mod, "TwoSum")().twoSum

def _validate_result(nums, target, res, expected_indices):
    assert isinstance(res, (list, tuple)), "result must be list/tuple"
    assert len(res) == 2, "result must contain exactly two indices"
    i, j = res
    assert 0 <= i < len(nums) and 0 <= j < len(nums), "indices must be in-bounds"
    assert i != j, "indices must be distinct"
    assert nums[i] + nums[j] == target
    assert set(res) == set(expected_indices)

def test_examples():
    _validate_result([2, 7, 11, 15], 9, two_sum([2, 7, 11, 15], 9), [0, 1])
    _validate_result([3, 2, 4], 6, two_sum([3, 2, 4], 6), [1, 2])
    _validate_result([3, 3], 6, two_sum([3, 3], 6), [0, 1])


def test_negative_and_zero():
    _validate_result([0, -1, 2, -3], -1, two_sum([0, -1, 2, -3], -1), [0, 1])


def test_no_solution_raises_value_error():
    with pytest.raises(ValueError):
        two_sum([1, 2, 3], 7)