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

