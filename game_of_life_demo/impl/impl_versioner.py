from game_of_life_demo.impl.arg_parser import parse_args

RUN_VERSION = parse_args().variant

if RUN_VERSION == "Numba".casefold():
    from numba import config

    from game_of_life_demo.impl.impl_numba import asnumpy
    from game_of_life_demo.impl.impl_numba import grid_update
    from game_of_life_demo.impl.impl_numba import init_grid
    from game_of_life_demo.impl.impl_numba import impl_string

    config.THREADING_LAYER = parse_args().threading_layer
elif RUN_VERSION == "NumPy".casefold():
    from game_of_life_demo.impl.impl_numpy import asnumpy
    from game_of_life_demo.impl.impl_numpy import grid_update
    from game_of_life_demo.impl.impl_numpy import init_grid
    from game_of_life_demo.impl.impl_numpy import impl_string
elif RUN_VERSION == "DPNP".casefold():
    from game_of_life_demo.impl.impl_dpnp import asnumpy
    from game_of_life_demo.impl.impl_dpnp import grid_update
    from game_of_life_demo.impl.impl_dpnp import init_grid
    from game_of_life_demo.impl.impl_dpnp import impl_string
elif RUN_VERSION == "Numba-DPEX".casefold():
    from game_of_life_demo.impl.impl_numba_dpex import asnumpy
    from game_of_life_demo.impl.impl_numba_dpex import grid_update
    from game_of_life_demo.impl.impl_numba_dpex import init_grid
    from game_of_life_demo.impl.impl_numba_dpex import impl_string


def get_variant_string():
    return impl_string(parse_args)
