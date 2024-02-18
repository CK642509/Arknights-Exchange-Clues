import numpy as np
from derangement import read_derangements

NUM_CLUES = 7

DERANGE_3 = read_derangements(3)
DERANGE_4 = read_derangements(4)
DERANGE_5 = read_derangements(5)
DERANGE_6 = read_derangements(6)
DERANGE_7 = read_derangements(7)
DERANGE_8 = read_derangements(8)

def get_derangement(n: int) -> list:
    if n == 3:
        return DERANGE_3
    elif n == 4:
        return DERANGE_4
    elif n == 5:
        return DERANGE_5
    elif n == 6:
        return DERANGE_6
    elif n == 7:
        return DERANGE_7
    elif n == 8:
        return DERANGE_8
    else:
        return []

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

def show_result(players: list, best_chg: list):
    print("兌換方法：")
    for i, player_1 in enumerate(players):
        for j, player_2 in enumerate(players):
            count = 0
            for clue_no in range(NUM_CLUES):
                for change in best_chg:   # change = [clue_no, player_1, player_2]
                    if change[1] == i and change[2] == j and change[0] == clue_no:
                        if count == 0:
                            print(f"{player_1}\t →\t {player_2}\t", end='')
                            count += 1
                        print(f"{clue_no + 1}", end='')
            if count != 0:
                print()
        print("--------------------------")

class ConditionEvaluator:
    def __init__(self, all_wants: list):
        self.all_wants = all_wants
        self.nPlayers = len(all_wants)
        self.nClues = len(all_wants[0])
        self.condition_count = 0
        self.best_condition = None
        self.best_chg = None
        self.best_rank = [self.nPlayers, 0, 0, 0, 0]
        
        # count number of want = 0
        nValid = 0
        valid_spot = []
        for i in range(self.nPlayers):
            for j in range(self.nClues):
                if all_wants[i][j] == 0:
                    nValid += 1
                    valid_spot.append([i, j])
        self.nValid = nValid
        self.valid_spot = valid_spot

        # copy all_wants to temp_wants
        temp_wants = []
        for i in range(nPlayers):
            temp_wants.append(all_wants[i].copy())
        self.temp_wants = temp_wants

    def generate_conditions(self, index: int):
        x = 2 ** self.nValid
        if index == self.nValid:
            # We have generated a valid condition, print or store it
            self.condition_count += 1
            print(f"{self.condition_count} / {x}", end='\r')   # progress bar
            yield self.temp_wants.copy()   # return a copy of temp_wants
        else:
            # Set the current spot to 1 and generate the remaining conditions
            i, j = self.valid_spot[index]
            self.temp_wants[i][j] = 1
            yield from self.generate_conditions(index + 1)

            # Set the current spot to -1 and generate the remaining conditions
            self.temp_wants[i][j] = -1
            yield from self.generate_conditions(index + 1)
    
    def try_condition(self, condition: list, conf: list) -> list:
        """
        Evaluate the given condition. If it meets the criteria, return score and result, else return blank list.
        Criteria for a good condition:
        1. Minimize players exchanging 0 clues.
        2. Minimize players exchanging 1 clue.
        3. Minimize players exchanging 6 clues.
        4. Minimize exchange combinations between players.
        5. Minimize total exchanges.
        """

        tmp_how = []

        for i in range(self.nClues):
            tmp_how.append([0])
            for j in range(self.nPlayers):
                if condition[j][i] == 1:
                    tmp_how[i][0] += 1
                    tmp_how[i].append(j)
            
            # one player can only exchange with one other player
            if tmp_how[i][0] == 1:
                return []
        
        tmp_rank = [0]*5

        # 5. Minimize total exchanges.
        for i in range(self.nClues):
            tmp_rank[4] += tmp_how[i][0]

        # 1. Minimize players exchanging 0 clues.
        # 2. Minimize players exchanging 1 clue.
        # 3. Minimize players exchanging 6 clues.
        for i in range(self.nPlayers):
            total_exchange_clues = 0
            for j in range(self.nClues):
                if condition[i][j] == 1:
                    total_exchange_clues += 1

            if total_exchange_clues == 0:
                tmp_rank[0] += 1
            elif total_exchange_clues == 1:
                tmp_rank[1] += 1
            elif total_exchange_clues == 6:
                tmp_rank[2] += 1
    
        num_conf = self.nPlayers * (self.nPlayers - 1)

        def log(j: int, clue_no: int, p1: int, p2: int, tmp_vote: list, tmp_chg: list, tmp_num_chg: int):
            tmp_vote[j] += 1
            tmp_num_chg += 1
            tmp_chg.append([clue_no, p1, p2])
            return tmp_vote, tmp_chg, tmp_num_chg
        
        tmp_vote = [0] * num_conf
        tmp_chg = []   # [[線索編號, 玩家1, 玩家2], ...]
        tmp_num_chg = 0
        
        def n_way_exchange(n: int, tmp_how, tmp_vote, tmp_chg, tmp_num_chg):
            for i in range(self.nClues):
                if tmp_how[i][0] == n:
                    solutions = get_derangement(n)
                    best_solution = None
                    
                    # if tmp_vote is empty, then it's the first time to exchange
                    # just use the first solution
                    if tmp_vote == [0] * num_conf:
                        best_solution = solutions[0]
                    else:
                        # the best solution has the highest total
                        max_total = -1
                        
                        for sol in solutions:
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
            return tmp_vote, tmp_chg, tmp_num_chg


        # 2-way exchange
        for i in range(self.nClues):
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

        for i in range(3, self.nPlayers + 1):
            tmp_vote, tmp_chg, tmp_num_chg = n_way_exchange(i, tmp_how, tmp_vote, tmp_chg, tmp_num_chg)
        
        # 4. Minimize exchange combinations between players.
        tmp_rank[3] = tmp_num_chg
        
        tmp_rank.append(tmp_chg)
        return tmp_rank
    
    def evaluate(self):
        for condition in self.generate_conditions(0):
            tmp_rank = self.try_condition(condition, conf)
            if tmp_rank:
                for tmp_score, best_score in zip(tmp_rank[:-1], self.best_rank):
                    if tmp_score < best_score:
                        self.best_rank = tmp_rank
                        self.best_condition = condition
                        self.best_chg = tmp_rank[5]
                        break
    




if __name__ == '__main__':
    players = get_players()
    print(players)
    clues = get_input_clues()
    print(clues)
    nPlayers = len(players)

    # 計算完家之間的組合數
    num_conf = nPlayers * (nPlayers - 1)
    print(f"組合數 = {num_conf}")


    # 建立組合矩陣
    # conf[i][0] = 投票數
    # conf[i][1] = 玩家1 (給)
    # conf[i][2] = 玩家2 (收)
    conf = [[0, 0, 0] for _ in range(num_conf)]

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
                    print(f"玩家{i+1}自己沒有線索{j+1}，不能跟別人換")
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

    evaluator = ConditionEvaluator(all_wants)
    evaluator.evaluate()
    print("best_rank ==>", evaluator.best_rank)
    print("best_condition ==>", evaluator.best_condition)
    print("best_chg ==>", evaluator.best_chg)

    print_temp_wants(players, evaluator.best_condition)

    # show result
    show_result(players, evaluator.best_chg)
