#---------------------------------------------------------------------------------------
# data
# read player / enemy / boss / boss_map / skill / skill_map
#---------------------------------------------------------------------------------------
import gspread

# character offset
C_NAME = 1
C_HP = 2
C_SP = 3
C_MP = 4
C_ATK = 5
C_SKILL_1 = 6
C_SKILL_2 = 7
C_SKILL_3 = 8
C_SKILL_4 = 9
C_SKILL_5 = 10
C_SKILL_6 = 11
C_SKILL_7 = 12
C_PROPERTY = 13

# property
PROPERTY_POEM = 1
PROPERTY_SOLA = 2
PROPERTY_ORBIT = 3
PROPERTY_VOID = 4

class character:
    def __init__(self, c_id, c_data):
        self.id = c_id
        self.name = c_data[C_NAME]
        self.hp = int(c_data[C_HP])
        self.sp = int(c_data[C_SP])
        self.mp = int(c_data[C_MP])
        self.atk = int(c_data[C_ATK])

        if c_data[C_SKILL_1] != '-':
            self.skill_1 = int(c_data[C_SKILL_1])
        else:
            self.skill_1 = -1

        if c_data[C_SKILL_2] != '-':
            self.skill_2 = int(c_data[C_SKILL_2])
        else:
            self.skill_2 = -1

        if c_data[C_SKILL_3] != '-':
            self.skill_3 = int(c_data[C_SKILL_3])
        else:
            self.skill_3 = -1

        if c_data[C_SKILL_4] != '-':
            self.skill_4 = int(c_data[C_SKILL_4])
        else:
            self.skill_4 = -1

        if c_data[C_SKILL_5] != '-':
            self.skill_5 = int(c_data[C_SKILL_5])
        else:
            self.skill_5 = -1

        if c_data[C_SKILL_6] != '-':
            self.skill_6 = int(c_data[C_SKILL_6])
        else:
            self.skill_6 = -1

        if c_data[C_SKILL_7] != '-':
            self.skill_7 = int(c_data[C_SKILL_7])
        else:
            self.skill_7 = -1

        if c_data[C_PROPERTY] == '시':
            self.property = PROPERTY_POEM
        elif c_data[C_PROPERTY] == '공':
            self.property = PROPERTY_SOLA
        elif c_data[C_PROPERTY] == '원':
            self.property = PROPERTY_ORBIT
        elif c_data[C_PROPERTY] == '허':
            self.property = PROPERTY_VOID
        else:
            self.property = 0


# skill offset
S_NAME = 1
S_CMD = 2
S_PASSIVE = 3
S_COST = 4
S_SKILL_RANGE = 5
S_SKILL_EFFECT_RANGE = 6
S_SKILL_TARGET = 7
S_HEAL = 8
S_DAMAGE = 9

S_PARALYZE = 10
S_PARALYZE_REMAIN = 11
S_POISON = 12
S_POISON_REMAIN = 13
S_WEAKEN = 14
S_WEAKEN_REMAIN = 15

S_HEIST = 16
S_ENFORCE = 17
S_BROKEN = 18
S_TANK = 19
S_PROVOKE = 20
S_CROWN = 21

S_BARRIER = 22
S_KNIGHT = 23
S_EVADE = 24
S_SAVE = 25

S_PROPERTY = 26

class skill:
    def __init__(self, s_id, s_data):
        self.id = s_id
        self.name = s_data[S_NAME]
        self.passive = int(s_data[S_PASSIVE])
        self.cmd = s_data[S_CMD]

        # check cost
        cost = s_data[S_COST]
        if cost == "-" or cost == "" or cost == "패시브":
            self.cost = -1
        elif cost == "잔여 기력":
            self.cost = -2
        elif cost == "최대 기력":
            self.cost = -3
        elif cost == "최대 마력":
            self.cost = -4
        else:
            self.cost = int(cost)

        # skill_range
        skill_range = s_data[S_SKILL_RANGE]
        if skill_range == "-" or skill_range == "":
            self.skill_range = -1
        elif skill_range == "근거리":
            self.skill_range = 1
        elif skill_range == "원거리":
            self.skill_range = 3
        elif skill_range == "전체":
            self.skill_range = -2
        elif skill_range == "십자":
            self.skill_range = -3
        else:
            self.skill_range = int(skill_range)

        # skill_effect_range
        skill_effect_range = s_data[S_SKILL_EFFECT_RANGE]
        if skill_effect_range == "-":
            self.skill_effect_range = -1
        elif skill_effect_range == "전체":
            self.skill_effect_range = -2
        else:
            self.skill_effect_range = int(skill_effect_range)

        # skill target
        skill_target = s_data[S_SKILL_TARGET]
        if skill_target == "자신":
            self.skill_target = 0
        elif skill_target == "아군 단일":
            self.skill_target = 1
        elif skill_target == "아군 전원":
            self.skill_target = 2
        elif skill_target == "적 단일":
            self.skill_target = 3
        elif skill_target == "적 전원":
            self.skill_target = 4
        else:
            self.skill_target = -1

        # heal modifier
        modifier = s_data[S_HEAL].split('*')
        if modifier[0] == '':
            self.heal_base = 0
            self.heal_modifier = 0
        elif modifier[0] == 'remain':
            self.heal_base = 0
            self.heal_modifier = int(modifier[1])
        else:
            self.heal_base = int(modifier[0])
            self.heal_modifier = 0

        # damage modifier
        modifier = s_data[S_DAMAGE].split('*')
        if modifier[0] == '':
            self.damage_base = 0
            self.damage_modifier = 0
        elif modifier[0] == 'remain':
            self.damage_base = 0
            self.damage_modifier = int(modifier[1])
        else:
            self.damage_base = int(modifier[0])
            self.damage_modifier = 0

        # additional effect
        self.paralyze = int(s_data[S_PARALYZE])
        self.paralyze_remain = int(s_data[S_PARALYZE_REMAIN])

        self.poison = int(s_data[S_POISON])
        self.poison_remain = int(s_data[S_POISON_REMAIN])

        self.weaken = int(s_data[S_WEAKEN])
        self.weaken_remain = int(s_data[S_WEAKEN_REMAIN])

        self.heist = int(s_data[S_HEIST])
        self.enforce = int(s_data[S_ENFORCE])
        self.broken = int(s_data[S_BROKEN])
        self.tank = int(s_data[S_TANK])
        self.provoke = int(s_data[S_PROVOKE])

        self.barrier = int(s_data[S_BARRIER])
        self.knight = int(s_data[S_KNIGHT])
        self.evade = int(s_data[S_EVADE])
        self.save = int(s_data[S_SAVE])


class boss_map:
    def __init__(self, boss_map):
        self.map = []

        for i in range(10):
            line = []
            for j in range(10):
                line.append(int(boss_map[i][j]))
            self.map.append(line)

class data:
    def __init__(self):
        self.gc = gspread.service_account(filename="./gspread.json")

        self.sh_player = self.gc.open("bus station test sheet").worksheet("player")
        self.sh_enemy = self.gc.open("bus station test sheet").worksheet("enemy")
        self.sh_boss = self.gc.open("bus station test sheet").worksheet("boss")
        self.sh_boss_map = self.gc.open("bus station test sheet").worksheet("boss_map")
        self.sh_skill = self.gc.open("bus station test sheet").worksheet("skill")

        self.player = list()
        self.enemy = list()
        self.boss = list()
        self.boss_map = list()
        self.skill = list()

    def get_data_player(self):
        try:
            self.data_player = self.sh_player.get_all_values()
            return 0
        except:
            return 1

    def get_data_enemy(self):
        try:
            self.data_enemy = self.sh_enemy.get_all_values()
            return 0
        except:
            return 1

    def get_data_boss(self):
        try:
            self.data_boss = self.sh_boss.get_all_values()
        except:
            return 1

    def get_data_boss_map(self):
        try:
            self.data_boss_map = self.sh_boss_map.get_all_values()
        except:
            return 1

    def get_data_skill(self):
        try:
            self.data_skill = self.sh_skill.get_all_values()
        except:
            return 1

    def init_player(self):
        while self.get_data_player():
            time.sleep(1)

        player_total = len(self.data_player)

        for i in range(0, player_total - 1):
            self.player.append(character(i, self.data_player[1 + i]))

    def init_enemy(self):
        while self.get_data_enemy():
            time.sleep(1)

        enemy_total = len(self.data_enemy)

        for i in range(0, enemy_total - 1):
            self.enemy.append(character(i, self.data_enemy[1 + i]))

    def init_boss(self):
        while self.get_data_boss():
            time.sleep(1)

        boss_total = len(self.data_boss)

        for i in range(0, boss_total - 1):
            self.boss.append(character(i, self.data_boss[1 + i]))

    def init_skill(self):
        while self.get_data_skill():
            time.sleep(1)

        skill_total = len(self.data_skill)

        for i in range(0, skill_total - 1):
            self.skill.append(skill(i, self.data_skill[1 + i]))

    def print_data(self):
        print("print_data")
        print("------------------------------------------------------------------")
        for player in self.player:
            if player.name == '':
                continue

            print("player", player.id, ":", player.name, ":", end=" ")

            if player.property == PROPERTY_POEM:
                print("[시]:", end=" ")
            elif player.property == PROPERTY_SOLA:
                print("[공]:", end=" ")
            elif player.property == PROPERTY_ORBIT:
                print("[원]:", end=" ")
            elif player.property == PROPERTY_VOID:
                print("[허]:", end=" ")
            else:
                print("[-]:", end=" ")

            if player.skill_1 != -1:
                skill = self.skill[player.skill_1]
                print("[" + skill.name + "]", end=" ")

            if player.skill_2 != -1:
                skill = self.skill[player.skill_2]
                print("[" + skill.name + "]", end=" ")

            if player.skill_3 != -1:
                skill = self.skill[player.skill_3]
                print("[" + skill.name + "]", end=" ")

            if player.skill_4 != -1:
                skill = self.skill[player.skill_4]
                print("[" + skill.name + "]", end=" ")

            if player.skill_5 != -1:
                skill = self.skill[player.skill_4]
                print("[" + skill.name + "]", end=" ")

            if player.skill_6 != -1:
                skill = self.skill[player.skill_6]
                print("[" + skill.name + "]", end=" ")

            if player.skill_7 != -1:
                skill = self.skill[player.skill_7]
                print("[" + skill.name + "]", end=" ")

            print("")

        print("------------------------------------------------------------------")
        for enemy in self.enemy:
            if enemy.name == '':
                continue

            print("enemy", enemy.id, ":", enemy.name, ":", end=" ")

            if enemy.skill_1 != -1:
                skill = self.skill[enemy.skill_1]
                print("[" + skill.name + "]", end=" ")

            if enemy.skill_2 != -1:
                skill = self.skill[enemy.skill_2]
                print("[" + skill.name + "]", end=" ")

            if enemy.skill_3 != -1:
                skill = self.skill[enemy.skill_3]
                print("[" + skill.name + "]", end=" ")

            if enemy.skill_4 != -1:
                skill = self.skill[enemy.skill_4]
                print("[" + skill.name + "]", end=" ")

            if enemy.skill_5 != -1:
                skill = self.skill[enemy.skill_4]
                print("[" + skill.name + "]", end=" ")

            if enemy.skill_6 != -1:
                skill = self.skill[enemy.skill_6]
                print("[" + skill.name + "]", end=" ")

            print("")

        print("------------------------------------------------------------------")
        for boss in self.boss:
            if boss.name == '':
                continue

            print("boss", boss.id, ":", boss.name, ":", end=" ")

            if boss.skill_1 != -1:
                skill = self.skill[boss.skill_1]
                print("[" + skill.name + "]", end=" ")

            if boss.skill_2 != -1:
                skill = self.skill[boss.skill_2]
                print("[" + skill.name + "]", end=" ")

            if boss.skill_3 != -1:
                skill = self.skill[boss.skill_3]
                print("[" + skill.name + "]", end=" ")

            if boss.skill_4 != -1:
                skill = self.skill[boss.skill_4]
                print("[" + skill.name + "]", end=" ")

            if boss.skill_5 != -1:
                skill = self.skill[boss.skill_4]
                print("[" + skill.name + "]", end=" ")

            if boss.skill_6 != -1:
                skill = self.skill[boss.skill_6]
                print("[" + skill.name + "]", end=" ")

            print("")
        """
        print("------------------------------------------------------------------")
        for skill in self.skill:
            print("skill", skill.id,
                  ":", skill.name,
                  "passive:", skill.passive,
                  "cmd:", skill.cmd)

            print("cost:", skill.cost,
                  "range:", skill.skill_range,
                  "effect_range:", skill.skill_effect_range,
                  "target:", skill.skill_target)

            print("heal:", skill.heal_base, skill.heal_modifier,
                  "damage:", skill.damage_base, skill.damage_modifier)

        print("------------------------------------------------------------------")
        """

    def get_player(self, player_id):
        return self.player[player_id]

    def get_enemy(self, enemy_id):
        return self.enemy[enemy_id]

    def get_boss(self, boss_id):
        return self.boss[boss_id]

    def get_skill(self, action):
        for skill in self.skill:
            if skill.cmd == action:
                return skill
        return 0

    def reset_player(self):
        self.player.clear()
        self.init_player()

    def reset_enemy(self):
        self.enemy.clear()
        self.init_enemy()

    def reset_boss(self):
        self.boss.clear()
        self.init_boss()

    def reset_skill(self):
        self.skill.clear()
        self.init_skill()
