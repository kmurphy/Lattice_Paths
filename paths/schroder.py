NAME = 'Schröder'
SAFE_NAME = 'schroder'

import path_properties as pp

steps = {
    'U': pp.Step(1, 1, 'U','red'),
    'L': pp.Step(2, 0, 'L','green'),
    'D': pp.Step(1, -1, 'D','blue'),
}


def generate(n, return_type='str'):
    """Generate paths of length n."""
    
    half_n = n // 2
    stack = [(0, 0, 0, "")]  # (length, height, up_count, path)
    
    while stack:
        length, height, up_count, path = stack.pop()

        if length == n:
            if height!=0: continue 
            yield list(path) if return_type=='list' else path

        if height>0:
            stack.append((length+1, height-1, up_count, path + "D"))

        if height<n-length-1:
            stack.append((length+2, height, up_count, path + "L"))
        
        if up_count < half_n:
            stack.append((length+1, height+1, up_count+1, path + "U"))




properties = {
    'Height': lambda path: pp.get_height(steps, path),
    'Height_Sum': lambda path: pp.get_height_sum(steps, path),
    'Weight': lambda path: pp.get_weight(steps, 'UL', path),
    'n_Runs': pp.count_runs,
    'n_Peaks': pp.count_peaks,
    'A': lambda path: pp.count_start_run('U', path),
    'B': lambda path: pp.count_end_run('D', path),
}