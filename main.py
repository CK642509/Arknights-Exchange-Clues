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
