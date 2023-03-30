from game_of_life_demo import init
from game_of_life_demo.game_of_life import RUN_VERSION, grid_update, init_grid


def test_variant():
    print("RUNNING test_variant()")
    variant_str = "numpy"
    args = init.parse_args(["--variant", variant_str])
    assert args.variant == variant_str
    assert RUN_VERSION == variant_str
    print(init_grid.__module__)
