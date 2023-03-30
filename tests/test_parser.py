from game_of_life_demo import init
from game_of_life_demo.game_of_life import init_grid, grid_update, RUN_VERSION

def test_variant():
    print("RUNNING test_variant()")
    variant_str = "numpy"
    args = init.parse_args(["--variant", variant_str])
    assert args.variant == variant_str
    assert RUN_VERSION == variant_str
    print(init_grid.__module__)
