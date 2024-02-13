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
    counts = [0] * 7
    for digit in s:
        counts[int(digit)-1] += 1
    return counts

def create_player_want(s: str) -> list:
    counts = [0] * 7
    for digit in s:
        counts[int(digit)-1] = 1
    return counts


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


