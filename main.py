from derangement import read_derangements

NUM_CLUES = 7

DERANGE_3 = read_derangements(3)
DERANGE_4 = read_derangements(4)
DERANGE_5 = read_derangements(5)
DERANGE_6 = read_derangements(6)
DERANGE_7 = read_derangements(7)
DERANGE_8 = read_derangements(8)

# get player list
def get_players() -> list:
    with open('settings/players.txt', 'r') as f:
        data = f.readlines()
        players = [x.strip() for x in data]
        return players
    
def get_input_clues() -> list:
    with open('settings/clues.txt', 'r') as f:
        data = f.readlines()
        clues = [x.strip() for x in data]
        return clues

def create_player_store(s: str) -> list:
    counts = [0] * NUM_CLUES
    for digit in s:
        counts[int(digit)-1] += 1
    return counts

def create_player_want(s: str) -> list:
    counts = [0] * NUM_CLUES
    if s == "0":
        return counts

    for digit in s:
        counts[int(digit)-1] = 1
    return counts

def print_temp_wants(players: list, tmp_wants: list):
    nPlayers = len(players)

    print("\n號碼\t", end='')
    for j in range(1, NUM_CLUES + 1):
        print(f"{j}\t", end='')
    print("\n【需求狀況】")
    print("--------------------------------------------------------------")
    for i in range(nPlayers):
        print(f"{players[i]}\t", end='')
        for j in range(NUM_CLUES):
            if tmp_wants[i][j] == 1:
                print("O\t", end='')
            elif tmp_wants[i][j] == 0:
                print(".\t", end='')
            else:
                print(" \t", end='')
        print("\n")
    print("\n")

condition_count = 0
def generate_conditions(index, valid_spot, temp_wants):
    global condition_count
    nValid = len(valid_spot)
    x = 2 ** nValid
    if index == nValid:
        # We have generated a valid condition, print or store it
        condition_count += 1
        print(f"{condition_count} / {x}", end='\r')   # progress bar
        if condition_count == 1000:
            yield temp_wants.copy()   # return a copy of temp_wants
    else:
        # Set the current spot to 1 and generate the remaining conditions
        i, j = valid_spot[index]
        temp_wants[i][j] = 1
        yield from generate_conditions(index + 1, valid_spot, temp_wants)

        # Set the current spot to -1 and generate the remaining conditions
        temp_wants[i][j] = -1
        yield from generate_conditions(index + 1, valid_spot, temp_wants)
    
def try_condition(condition: list, nPlayers: int, conf: list):
    """
    Evaluate the given condition. If it meets the criteria, return score and result, else return False.
    Criteria for a good condition:
    1. Minimize players exchanging 0 clues.
    2. Minimize players exchanging 1 clue.
    3. Minimize players exchanging 6 clues.
    4. Minimize exchange combinations between players.
    5. Minimize total exchanges.
    """

    tmp_how = []
    

    for i in range(NUM_CLUES):
        tmp_how.append([0])
        for j in range(nPlayers):
            if condition[j][i] == 1:
                tmp_how[i][0] += 1
                tmp_how[i].append(j)
        
        # one player can only exchange with one other player
        if tmp_how[i][0] == 1:
            return False
    print("tmp_how ==>")
    print(tmp_how)

    
    tmp_rank = [0]*5

    # 5. Minimize total exchanges.
    for i in range(NUM_CLUES):
        tmp_rank[4] += tmp_how[i][0]

    # 1. Minimize players exchanging 0 clues.
    # 2. Minimize players exchanging 1 clue.
    # 3. Minimize players exchanging 6 clues.
    for i in range(nPlayers):
        total_exchange_clues = 0
        for j in range(NUM_CLUES):
            if condition[i][j] == 1:
                total_exchange_clues += 1

        if total_exchange_clues == 0:
            tmp_rank[0] += 1
        elif total_exchange_clues == 1:
            tmp_rank[1] += 1
        elif total_exchange_clues == 6:
            tmp_rank[2] += 1
        
        # TODO: 處理 $ 

    print("tmp_rank ==>")
    print(tmp_rank)
    num_conf = nPlayers * (nPlayers - 1)
    

    # # 建立組合矩陣
    # # conf[i][0] = 投票數
    # # conf[i][1] = 玩家1 (給)
    # # conf[i][2] = 玩家2 (收)
    # conf = [[0, 0, 0] for _ in range(num_conf)]

    # count = 0
    # for i in range(nPlayers):
    #     for j in range(nPlayers):
    #         if i != j:
    #             conf[count][1] = i
    #             conf[count][2] = j
    #             count += 1
    # print(conf)
    def log(j: int, clue_no: int, p1: int, p2: int, tmp_vote: list, tmp_chg: list, tmp_num_chg: int):
        tmp_vote[j] += 1
        tmp_num_chg += 1
        tmp_chg.append([clue_no, p1, p2])
        return tmp_vote, tmp_chg, tmp_num_chg

    tmp_vote = [0] * num_conf
    tmp_chg = []   # [[線索編號, 玩家1, 玩家2], ...]
    tmp_num_chg = 0

    # 2-way exchange
    for i in range(NUM_CLUES):
        if tmp_how[i][0] == 2:
            for j in range(num_conf):
                # there is only one possible solution
                best_solution = [2, 1]
                for idx, target in enumerate(best_solution):
                    if conf[j][1] == tmp_how[i][idx + 1] and conf[j][2] == tmp_how[i][target]:
                        tmp_vote, tmp_chg, tmp_num_chg = log(j, i, conf[j][1], conf[j][2], tmp_vote, tmp_chg, tmp_num_chg)
                # # tmp_how[i][1] 簡稱玩家1，tmp_how[i][2] 簡稱玩家2
                # # 玩家1 -> 玩家2
                # if conf[j][1] == tmp_how[i][1] and conf[j][2] == tmp_how[i][2]:
                #     tmp_vote, tmp_chg, tmp_num_chg = log(j, i, conf[j][1], conf[j][2], tmp_vote, tmp_chg, tmp_num_chg)
                # # 玩家2 -> 玩家1
                # elif conf[j][1] == tmp_how[i][2] and conf[j][2] == tmp_how[i][1]:
                #     tmp_vote, tmp_chg, tmp_num_chg = log(j, i, conf[j][1], conf[j][2], tmp_vote, tmp_chg, tmp_num_chg)
    print("tmp_vote ==>", tmp_vote)
    print("tmp_chg ==>", tmp_chg)
    print("tmp_num_chg ==>", tmp_num_chg)

    # 3-way exchange
    for i in range(NUM_CLUES):
        if tmp_how[i][0] == 3:
            # there are 2 possible solutions
            # 1 -> 2，2 -> 3，3 -> 1
            # 1 -> 3，2 -> 1，3 -> 2
            comb3_solutions = DERANGE_3
            max_total = -1   # the best solution has the highest total
            best_solution = None
            for sol in comb3_solutions:
                total = 0
                for j in range(num_conf):
                    for idx, target in enumerate(sol):
                        if conf[j][1] == tmp_how[i][idx + 1] and conf[j][2] == tmp_how[i][target]:
                            total += tmp_vote[j]
                # update current best solution
                if total > max_total:
                    max_total = total
                    best_solution = sol

            # update tmp_vote, tmp_chg, tmp_num_chg
            for j in range(num_conf):
                for idx, target in enumerate(best_solution):
                    if conf[j][1] == tmp_how[i][idx + 1] and conf[j][2] == tmp_how[i][target]:
                        tmp_vote, tmp_chg, tmp_num_chg = log(j, i, conf[j][1], conf[j][2], tmp_vote, tmp_chg, tmp_num_chg)
    
    print("tmp_vote ==>", tmp_vote)
    print("tmp_chg ==>", tmp_chg)
    print("tmp_num_chg ==>", tmp_num_chg)

    # 4-way exchange
    for i in range(NUM_CLUES):
        if tmp_how[i][0] == 4:
            max_total = -1   # the best solution has the highest total
            best_solution = None
            comb4_solutions = DERANGE_4
            for sol in comb4_solutions:
                total = 0
                for j in range(num_conf):
                    for idx, target in enumerate(sol):
                        if conf[j][1] == tmp_how[i][idx + 1] and conf[j][2] == tmp_how[i][target]:
                            total += tmp_vote[j]
                # update current best solution
                if total > max_total:
                    max_total = total
                    best_solution = sol

            # update tmp_vote, tmp_chg, tmp_num_chg
            for j in range(num_conf):
                for idx, target in enumerate(best_solution):
                    if conf[j][1] == tmp_how[i][idx + 1] and conf[j][2] == tmp_how[i][target]:
                        tmp_vote, tmp_chg, tmp_num_chg = log(j, i, conf[j][1], conf[j][2], tmp_vote, tmp_chg, tmp_num_chg)
    
    print("tmp_vote ==>", tmp_vote)
    print("tmp_chg ==>", tmp_chg)
    print("tmp_num_chg ==>", tmp_num_chg)









if __name__ == '__main__':
    players = get_players()
    print(players)
    clues = get_input_clues()
    print(clues)
    nPlayers = len(players)

    # 計算組合數
    num_conf = nPlayers * (nPlayers - 1)
    print(f"組合數 = {num_conf}")


    # 建立組合矩陣
    # conf[i][0] = 投票數
    # conf[i][1] = 玩家1 (給)
    # conf[i][2] = 玩家2 (收)
    conf = [[0, 0, 0] for _ in range(num_conf)]
    # print(conf)

    count = 0
    for i in range(nPlayers):
        for j in range(nPlayers):
            if i != j:
                conf[count][1] = i
                conf[count][2] = j
                count += 1
    # print(conf)

    all_stores = []
    all_wants = []
    for clue in clues:
        store = clue.split(" ")[0]
        want = clue.split(" ")[1]
        all_stores.append(create_player_store(store))
        all_wants.append(create_player_want(want))
    print(all_stores)
    print(all_wants)

    # check store and want
    for i in range(nPlayers):
        for j in range(NUM_CLUES):
            # change want to 1 if store >= 3
            if all_stores[i][j] >= 3:
                all_wants[i][j] = 1

            # change want to -1 if store is 0
            if all_stores[i][j] == 0:
                if all_wants[i][j] == 1:
                    print(f"玩家{i+1}自己沒有線索{j+1}，不能跟別人換")   # 但也有可能是因為輸入 0 造成的
                all_wants[i][j] = -1
    
    for i in range(NUM_CLUES):
        total_players_with_clue = 0
        for j in range(nPlayers):
            if all_stores[j][i] > 0:
                total_players_with_clue += 1
        
        if total_players_with_clue < 2:
            print(f"線索{i+1}的玩家數量不足")
            for j in range(nPlayers):
                all_wants[j][i] = -1
    print("===")
    print(all_stores)
    print(all_wants)

    # count number of want = 0
    nValid = 0
    valid_spot = []
    for i in range(nPlayers):
        for j in range(NUM_CLUES):
            if all_wants[i][j] == 0:
                nValid += 1
                valid_spot.append([i, j])
    print(nValid)
    print(valid_spot)

    # TODO: if nValid is too large, try to add more constraints to make it smaller

    # copy all_wants to temp_wants
    temp_wants = []
    for i in range(nPlayers):
        temp_wants.append(all_wants[i].copy())

    # print(temp_wants)

    # print want status
    # print_temp_wants(players, temp_wants)

    for condition in generate_conditions(0, valid_spot, temp_wants):
        print(condition)
        print_temp_wants(players, condition)
        try_condition(condition, nPlayers, conf)


