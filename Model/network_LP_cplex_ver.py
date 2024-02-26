import numpy as np
import cplex


def solve(all_arcs, number_of_YT, number_of_Job):
    solver = cplex.Cplex()

    # Decision Variables
    x = [f'x[{i}]' for i in range(len(all_arcs))]
    solver.variables.add(names=x, types=['B'] * len(all_arcs))

    # Constraints 1 : 한 YT에서 활성화되는 아크들의 합은 1
    for l in range(number_of_YT):
        list_for_const1 = [i for i, a in enumerate(all_arcs) if a.i == ['YT', l]]
        solver.linear_constraints.add(
            lin_expr=[[x[j] for j in list_for_const1], [1.0] * len(list_for_const1)],
            senses=['E'],
            rhs=[1.0]
        )

    # Constraint 2 : sink node로 들어오는 아크들의 합은 YT의 수
    list_for_const2 = [i for i, a in enumerate(all_arcs) if a.j[0] == 'Sink']
    solver.linear_constraints.add(
        lin_expr=[[x[j] for j in list_for_const2], [1.0] * len(list_for_const2)],
        senses=['E'],
        rhs=[number_of_YT]
    )

    # Constraint 3 : Pick 노드와 Drop노드 대상으로, 각 노드에 들어오는 아크와 나가는 아크의 수의 합이 같아야함
    for l in range(number_of_Job):
        list_for_const3_from_Pick = [i for i, a in enumerate(all_arcs) if a.i == ['Pick', l]]
        list_for_const3_to_Pick = [i for i, a in enumerate(all_arcs) if a.j == ['Pick', l]]
        list_for_const3_from_Drop = [i for i, a in enumerate(all_arcs) if a.i == ['Drop', l]]
        list_for_const3_to_Drop = [i for i, a in enumerate(all_arcs) if a.j == ['Drop', l]]

        solver.linear_constraints.add(
            lin_expr=[[x[j] for j in list_for_const3_from_Pick] + [x[j] for j in list_for_const3_to_Pick],
                      [1.0] * (len(list_for_const3_from_Pick) + len(list_for_const3_to_Pick))],
            senses=['E'],
            rhs=[2.0]
        )

        solver.linear_constraints.add(
            lin_expr=[[x[j] for j in list_for_const3_from_Drop] + [x[j] for j in list_for_const3_to_Drop],
                      [1.0] * (len(list_for_const3_from_Drop) + len(list_for_const3_to_Drop))],
            senses=['E'],
            rhs=[2.0]
        )

    # Constraint 4 : Drop노드 대상으로, 각 Drop노드에 들어오는 아크의 합이 1
    for l in range(number_of_Job):
        list_for_const4 = [i for i, a in enumerate(all_arcs) if a.j == ['Drop', l]]
        solver.linear_constraints.add(
            lin_expr=[[x[j] for j in list_for_const4], [1.0] * len(list_for_const4)],
            senses=['E'],
            rhs=[1.0]
        )

    # Objective Function
    for i, arc in enumerate(all_arcs):
        solver.objective.set_linear([(x[i], arc.cost)])

    solver.objective.set_sense(solver.objective.sense.minimize)

    solver.solve()

    # Retrieve solution
    solution_values = solver.solution.get_values()
    activated_arcs = [all_arcs[i] for i, val in enumerate(solution_values) if val > 0.5]
    objective_value = solver.solution.get_objective_value()

    return objective_value, activated_arcs
