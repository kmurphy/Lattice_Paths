from collections import namedtuple

Step = namedtuple('Step', ['x', 'y', 'label', 'color'])

def get_height(steps, path):
    """Compute the height of given path."""
    
    height = max_height = 0
    for step in path:
        height += steps[step].y
        if height>=max_height: max_height = height
    return max_height


def get_height_sum(steps, path):
    """Compute the sum of the heights of a given path."""

    height = height_sum = 0
    for step in path:
        height += steps[step].y
        height_sum += height
    return height_sum


def get_weight(steps, steps_in_weight, path):
    """Compute the weight of the given path."""

    height = get_height(steps, path)
    terms = {step:[0]*(height+1) for step in steps_in_weight}

    height = 0
    for step in path:
        height += steps[step].y
        if step in steps_in_weight: 
            terms[step][height] += 1

    poly = "" 
    for step in steps_in_weight:
        for p, power in enumerate(terms[step]):
            if power==0: 
                continue 
            elif power==1:
                poly += f"{step}_{p}"
            elif power>1:
                poly += f"{step}_{p}^{power}"

    return poly


def count_runs(path):
    """Count the number of repeated steps in given path."""

    n_run = 0
    for prev_step, step in zip(path, path[1:]):
        n_run += int(prev_step==step)

    return n_run


def count_peaks(path):
    """Count the number of peak in given path."""

    return path.count("UD")


def count_start_run(step, path):
    """Count run of step at start of given path."""

    for k, s in enumerate(path):
        if s!=step: return k
    return 0


def count_end_run(step, path):
    """Count run of step at end of given path."""
    
    for k, s in enumerate(reversed(path)):
        if s!=step: return k
    return 0