def analyze_phases(phase_loads):
    result = {}
    for phase, loads in phase_loads.items():
        result[phase] = sum(loads)
    return result
def detect_imbalance(phase_loads, max_diff=15.0):
    averages = {}
    for phase, loads in phase_loads.items():
        averages[phase] = sum(loads) / len(loads)
    max_avg = max(averages.values())
    min_avg = min(averages.values())
    actual_diff = max_avg - min_avg
    is_imbalanced = actual_diff > max_diff

    return (is_imbalanced, round(actual_diff, 2))
def get_last_n_samples(phase_loads, n=5):

    result = {}
    for phase, loads in phase_loads.items():
        result[phase] = loads[-n:]
    return result