NUM_CLUES = 7

# get player list
def get_players() -> list:
    with open('players.txt', 'r') as f:
        data = f.readlines()
        players = [x.strip() for x in data]
        return players
    
def get_input_clues() -> list:
    with open('clues.txt', 'r') as f:
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

    # print want status
    print_temp_wants(players, temp_wants)



