from ortools.linear_solver import pywraplp
import numpy as np



def solve(all_arcs, number_of_YT, number_of_Job):
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Please check solver")

    inf = solver.infinity()

    

    # sort all_arcs by index
    all_arcs.sort(key=lambda x: x.index)


    # print('lenght of all_arcs : ', len(all_arcs))
    # for i in range(len(all_arcs)):
    #     print('i : ', all_arcs[i].i),
    #     print('j : ', all_arcs[i].j)
    #     print('k : ', all_arcs[i].k)
    #     print('path : ', all_arcs[i].path)
    #     print('cost : ', all_arcs[i].cost)
    #     print('index : ', all_arcs[i].index)
    #     print('')


    # Decision Variables
    x = np.empty(len(all_arcs), dtype=object)
    for i in range(len(all_arcs)):
        x[i] = solver.IntVar(0, 1, 'x[%i]' % i)

    # # completion time of each YT
    # C = np.empty(number_of_YT, dtype=object)
    # for i in range(number_of_YT):
    #     C[i] = solver.NumVar(0, inf, 'C[%i]' % i)


    # Constraints 0 : 각 YT의 completion time은 한 출발노드가 자기자신(YT)이면서 아크들의 출발노드 도착노드를 이어서 최종적으로 sink노드로 가는데 걸리는 시간(cost의 합)
    # for l in range(number_of_YT):
    #     list_for_const0 = []
    #     for a in all_arcs:
    #         if a.i == ['YT', l]:
    #             list_for_const0.append(a.index)

    #     solver.Add(C[l] == sum(x[j] * all_arcs[j].cost for j in list_for_const0))
    # while True:
    #     list_for_const0 = []
    #     # list_for_const0의 마지막 원소의 출발노드가 현재 아크이면서 현재 아크의 도착노드가 sink인지 확인
    #     if list_for_const0[-1].i == ['YT', l] and all_arcs[list_for_const0[-1]].j[0] == 'Sink':
    #         solver.Add(C[l] == sum(x[j] * all_arcs[j].cost for j in list_for_const0))
    #         break
    #     else:
    #         # list_for_const0의 마지막 원소의 도착노드와 같은 출발노드를 가지는 아크들 중에서, 아크의 도착노드가 sink인 아크를 list_for_const0에 추가
    #         for a in all_arcs:
    #             if a.i == all_arcs[list_for_const0[-1]].j and a.j[0] == 'Sink':
    #                 list_for_const0.append(a.index)
    #                 break

    # Constraints 1 : 한 YT에서 활성화되는 아크들의 합은 1
    # 출발지(i)가 같은 YT인 아크들의 합을 1로
    for l in range(number_of_YT):
        list_for_const1 = []
        for a in all_arcs:
            if a.i == ['YT', l]:
                list_for_const1.append(a.index)

        solver.Add(sum(x[j] for j in list_for_const1) == 1)


    # Constraint 2 : sink node로 들어오는 아크들의 합은 YT의 수
    list_for_const2 = []
    for a in all_arcs:
        if a.j[0] == 'Sink':
            list_for_const2.append(a.index)

    solver.Add(sum(x[j] for j in list_for_const2) == number_of_YT)


    # Constraint 3 : Pick 노드와 Drop노드 대상으로,각 노드에 들어오는 아크와 나가는 아크의 수의 합이 같아야함
    for l in range(number_of_Job):
        list_for_const3_from_Pick = []
        list_for_const3_to_Pick = []

        list_for_const3_from_Drop = []
        list_for_const3_to_Drop = []

        for a in all_arcs:
            if a.i == ['Pick', l]:
                list_for_const3_from_Pick.append(a.index)
            if a.j == ['Pick', l]:
                list_for_const3_to_Pick.append(a.index)
            if a.i == ['Drop', l]:
                list_for_const3_from_Drop.append(a.index)
            if a.j == ['Drop', l]:
                list_for_const3_to_Drop.append(a.index)

        # print('l : ', l)
        # print('list_for_const3_from_Pick : ', list_for_const3_from_Pick)
        # print('list_for_const3_to_Pick : ', list_for_const3_to_Pick)
        # print('list_for_const3_from_Drop : ', list_for_const3_from_Drop)
        # print('list_for_const3_to_Drop : ', list_for_const3_to_Drop)
        # print('')

        solver.Add(sum(x[j] for j in list_for_const3_from_Pick) == sum(x[j] for j in list_for_const3_to_Pick))
        solver.Add(sum(x[j] for j in list_for_const3_from_Drop) == sum(x[j] for j in list_for_const3_to_Drop))


    # Constraint 4 : Drop노드 대상으로, 각 Drop노드에 들어오는 아크의 합이 1
    for l in range(number_of_Job):
        list_for_const4 = []

        for a in all_arcs:
            if a.j == ['Drop', l]:
                list_for_const4.append(a.index)
        solver.Add(sum(x[j] for j in list_for_const4) == 1)



    # Obejctive
    objective = solver.Objective()
    for i in range(len(all_arcs)):
        # 인덱스가 i인 arc의 cost를 x[i]와 곱해서 objective에 추가
        objective.SetCoefficient(x[i], all_arcs[i].cost)
        
    objective.SetMinimization()

    status = solver.Solve()
    # print("Number of arcs : " , len(all_arcs))
    # print()

    if status == pywraplp.Solver.OPTIMAL:
        objective_value = solver.Objective().Value()
        activated_arcs = []
        # print('Objective value =', solver.Objective().Value())
        # print()

        for i in range(len(all_arcs)):
            if x[i].solution_value() > 0:
                activated_arcs.append(all_arcs[i])
                # print(x[i].name(), ' = ', x[i].solution_value())
                # index가 i인 아크의 i, j, k, path 출력
                # print(all_arcs[i].i, all_arcs[i].j, all_arcs[i].k, all_arcs[i].path, all_arcs[i].cost, all_arcs[i].index)
    else:
        print('The problem does not have an optimal solution.')


    return objective_value, activated_arcs