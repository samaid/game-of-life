import dpnp as np


def default_dpt_device():
    import dpctl

    default_device = dpctl.SyclDevice()
    if default_device.is_gpu:
        return "gpu"
    else:
        return "cpu"


def implementation_device(parse_args):
    if parse_args.gpu:
        return "gpu"
    elif parse_args.cpu:
        return "cpu"

    return default_dpt_device()


def impl_string(parse_args):
    return f"Dpnp, device: {implementation_device(parse_args())}"


def init_grid(w, h, p, args):
    u = np.random.random(
        w * h, device=implementation_device(args)
    )  # Working around the lack of random.choice
    return np.where(u <= p, 1, 0).reshape(h, w)


def grid_update(grid):
    m, n = grid.shape

    grid_neighbor = np.zeros_like(grid, shape=(m + 2, n + 2))

    grid_neighbor[0:-2, 0:-2] = grid
    grid_neighbor[1:-1, 0:-2] += grid
    grid_neighbor[2:, 0:-2] += grid
    grid_neighbor[0:-2, 1:-1] += grid
    grid_neighbor[2:, 1:-1] += grid
    grid_neighbor[0:-2, 2:] += grid
    grid_neighbor[1:-1, 2:] += grid
    grid_neighbor[2:, 2:] += grid

    grid_neighbor[1, 1:-1] += grid_neighbor[-1, 1:-1]
    grid_neighbor[-2, 1:-1] += grid_neighbor[0, 1:-1]
    grid_neighbor[1:-1, 1] += grid_neighbor[1:-1, -1]
    grid_neighbor[1:-1, -2] += grid_neighbor[1:-1, 0]

    grid_neighbor[1, 1] += grid_neighbor[-1, -1]
    grid_neighbor[-2, -2] += grid_neighbor[0, 0]
    grid_neighbor[1, -2] += grid_neighbor[-1, 0]
    grid_neighbor[-2, 1] += grid_neighbor[0, -1]

    dead_rules = np.logical_and(grid == 0, grid_neighbor[1:-1, 1:-1] == 3)
    alive_rules = np.logical_and(
        grid == 1,
        np.logical_or(grid_neighbor[1:-1, 1:-1] == 2, grid_neighbor[1:-1, 1:-1] == 3),
    )

    grid_out = np.logical_or(alive_rules, dead_rules)

    return grid_out.astype(grid.dtype)


def asnumpy(x):
    return np.asnumpy(x)
