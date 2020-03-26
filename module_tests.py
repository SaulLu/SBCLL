from cpp.target_module.target_module_v1 import _target_module


def module_test():
    units_list = [[2, 2, 1, 2], [3, 3, 1, 2], [4, 4, 2, 2], [5, 3, 2, 2]]
    player_int = 2
    all_attributions = _target_module.targetsAttribution(units_list, len(units_list), player_int)
    for attacks, merges in all_attributions:
        print('\nattacks:')
        for x_start, y_start, x_target, y_target, number in attacks:
            print(f"\tstart:({x_start}, {y_start}), target:({x_target}, {y_target}), number: {number}")
        print('merges:')
        for x_start, y_start, x_target, y_target, number in merges:
            print(f"\tstart:({x_start}, {y_start}), target:({x_target}, {y_target}), number: {number}")
    print('end')

if __name__ == "__main__":
    module_test()
