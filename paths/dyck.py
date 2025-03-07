NAME = 'Dyck'
SAFE_NAME = 'dyck'

import path_properties as pp

steps = {
    'U': pp.Step(1, 1, 'U','red'),
    'D': pp.Step(1, -1, 'D','blue'),
}


def generate(n, return_type='str'):
    """Generate paths of length n."""
    
    stack = [(0, 0, 0, "")]  # (length, height, up count, path)
    
    while stack:
        length, height, up, path = stack.pop()

        if length == 2 * n:
            yield list(path) if return_type=='list' else path
            continue

        if height>0:
            stack.append((length+1, height-1, up, path + "D"))

        if up < n:
            stack.append((length + 1, height+1, up+1, path + "U"))


properties = {
    'Height': lambda path: pp.get_height(steps, path),
    'Height_Sum': lambda path: pp.get_height_sum(steps, path),
    'Weight': lambda path: pp.get_weight(steps, 'U', path),
    'n_Runs': pp.count_runs,
    'n_Peaks': pp.count_peaks,
    'A': lambda path: pp.count_start_run('U', path),
    'B': lambda path: pp.count_end_run('D', path),

}