from collections import defaultdict


def read_input_file(path):
    with open(path) as f:
        input_line = f.readlines()

    cases = defaultdict(list)
    for line in input_line:
        case_id, activity = line.split()
        cases[int(case_id)].append(activity)
    return cases


def get_direct_follower(W):
    direct_follower = []
    for i in W:
        for j in range(0, len(i) - 1):
            temp = [[i[j]], [i[j + 1]]]
            if temp not in direct_follower:
                direct_follower.append(temp)

    direct_follower.sort(key=lambda x: x[0])
    return direct_follower


def get_parallel_and_causality(direct_follower):
    parallel = []
    causality = list(direct_follower)

    for i in range(0, len(direct_follower)):
        for j in range(i, len(direct_follower)):
            if direct_follower[i][0] == direct_follower[j][1] and direct_follower[i][1] == direct_follower[j][0]:
                parallel.append(direct_follower[i])
                causality.remove(direct_follower[i])
                causality.remove(direct_follower[j])

    return parallel, causality


def get_Xw_and_Yw(causality, parallel):
    merged_activities = []
    X_w = list(causality)
    Y_w = list(X_w)

    for front_or_back in range(0, 2):
        for i in range(0, len(X_w)):
            temp = []
            for j in range(i, len(X_w)):
                if X_w[i][front_or_back] == X_w[j][front_or_back]:
                    temp.append(X_w[j][1 - front_or_back])
            if len(temp) > 1 and temp not in parallel:
                single_list_temp = sum(temp, [])
                if front_or_back == 0:
                    merged_activities.append([X_w[i][front_or_back], single_list_temp])
                    for j in temp:
                        to_remove = [X_w[i][front_or_back], j]
                        if to_remove in Y_w:
                            Y_w.remove(to_remove)
                else:
                    merged_activities.append([single_list_temp, X_w[i][front_or_back]])
                    for j in temp:
                        to_remove = [j, X_w[i][front_or_back]]
                        if to_remove in Y_w:
                            Y_w.remove(to_remove)

    X_w += merged_activities
    Y_w += merged_activities

    X_w.sort(key=lambda x: x[0][0][0])
    Y_w.sort(key=lambda x: x[0][0][0])

    return X_w, Y_w


def get_Pw(Y_w):
    P_w = ["I_w"]
    for i in Y_w:
        P_w.append("P" + str(i))

    P_w.append("O_w")

    return P_w


def get_Fw(Y_w, P_w, T_i, T_o):
    F_w = []
    F_w.append([P_w[0], T_i])
    place_counter = 1
    for activity in Y_w:
        for i in activity[0]:
            F_w.append([i, P_w[place_counter]])

        for i in activity[1]:
            F_w.append([P_w[place_counter], i])

        place_counter += 1

    F_w.append([T_o, P_w[-1]])
    return F_w


def main():
    log_dict = read_input_file("input.txt")
    cases = sorted(log_dict.keys())

    T_w = sorted(set([j for i in log_dict.values() for j in i]))
    print("T_w :", T_w,"\n")

    W = list(set([''.join(log_dict[i]) for i in cases]))
    print("W : ", W, "\n")

    T_i = W[0][0]
    print("T_i : ", T_i, "\n")

    T_O = W[0][-1]
    print("T_O : ", T_O, "\n")

    direct_follower = get_direct_follower(W)
    print("direct_follower : ", direct_follower, "\n")

    parallel, causality = get_parallel_and_causality(direct_follower)
    print("causality : ", causality, "\n")
    print("parallel : ", parallel, "\n")

    X_w, Y_w = get_Xw_and_Yw(causality, parallel)
    print("X_w : ", X_w, "\n")
    print("Y_w : ", Y_w, "\n")

    P_w = get_Pw(Y_w)
    print("P_w : ", P_w, "\n")

    F_w = get_Fw(Y_w, P_w, T_i, T_O)
    print("F_w : ", F_w, "\n")

main()
