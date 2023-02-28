#---------------------------------------------------------------------------------------
# runtime
# read runtime
# write runtime
#---------------------------------------------------------------------------------------
# map data
import gspread

global raid_map
global raid_character

class cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.character_placed = 0
        self.character_num = -1

class map_data:
    def __init__(self):
        self.cell = list()

        for x in range(0, 10):
            self.cell.append(list())
            for y in range(0, 10):
                self.cell[x].append(cell(x, y))

    def print_map(self):
        print("------------------------------------------------------------------")
        print("print_map")
        print("------------------------------------------------------------------")
        for y in range(0, 10):
            for x in range(0, 10):
                cell = self.cell[x][y]
                print("(" + str(cell.character_placed) + "," + str(cell.character_num) + ")", end=' ');
            print(" ")
        print("------------------------------------------------------------------")

    def is_placed(self, location):
        x = ord(location[0]) - ord('A')
        y = ord(location[1]) - ord('0')

        if self.cell[x][y].character_placed == 1:
            return 1

        return 0

    def get_character_placed(self, location):
        x = ord(location[0]) - ord('A')
        y = ord(location[1]) - ord('0')

        if self.cell[x][y].character_placed == 1:
            return self.cell[x][y].character_num

        print("no placed location")

        return 0

    def place_character(self, character_num, location):
        x = ord(location[0]) - ord('A')
        y = ord(location[1]) - ord('0')

        if (x < 0) or (x > 9) or (y < 0) or (y > 9):
            #print("wrong location")
            return 0

        if self.cell[x][y].character_placed == 1:
            #print("already character placed")
            return 0

        self.cell[x][y].character_placed = 1
        self.cell[x][y].character_num = character_num

        return 1

    def remove_character(self, character):
        if character.is_player() or character.is_enemy():
            if character.location == '':
                return

            x = ord(character.location[0]) - ord('A')
            y = ord(character.location[1]) - ord('0')

            self.cell[x][y].character_placed = 0
            self.cell[x][y].character_num = -1

        elif character.is_boss():
            if character.location != 'BOSS':

                x = ord(character.location[0]) - ord('A')
                y = ord(character.location[1]) - ord('0')

                self.cell[x][y].character_placed = 0
                self.cell[x][y].character_num = -1

                return

            for location in character.location_boss:
                x = ord(location[0]) - ord('A')
                y = ord(location[1]) - ord('0')

                self.cell[x][y].character_placed = 0
                self.cell[x][y].character_num = -1

    def place_boss(self, character):
        if character.type != BOSS:
            print("character is not boss type")
            return 0
        
        if character.location != 'BOSS':
            return self.place_character(character.num, character.location)

        for location in character.location_boss:
            if self.is_placed(location):
                return 0

        for location in character.location_boss:
            self.place_character(character.num, location)

        return 1

#---------------------------------------------------------------------------------------
# status
ENEMY = 0
PLAYER = 1
BOSS = 2

# cost
COST_REMAIN = -1
COST_MAX = -2
COST_MAX_MP = -3

# property
PROPERTY_POEM = 1
PROPERTY_SOLA = 2
PROPERTY_ORBIT = 3
PROPERTY_VOID = 4

class runtime_character:
    def __init__(self, num, char_type):
        self.num = num
        self.type = char_type

        self.added = 0
        self.name = ''
        self.location = ''

        self.action = 0
        self.hp = 0
        self.sp = 0
        self.mp = 0

        self.action_max = 0
        self.hp_max = 0
        self.sp_max = 0
        self.mp_max = 0

        self.atk = 0

        self.paralyze = 0
        self.paralyze_remain = 0

        self.poison = 0
        self.poison_remain = 0

        self.weaken = 0
        self.weaken_remain = 0

        self.heist = 0
        self.enforce = 0
        self.broken = 0
        self.tank = 0
        self.provoke = 0
        self.crown = 0
        self.barrier = 0
        self.knight = -1
        self.polka = 0
        self.evade = -1
        
        self.save = 0
        self.hp_save = 0
        self.sp_save = 0
        self.mp_save = 0
        self.location_save = ''

        self.location_prev = ''
        self.sp_prev = 0

        self.solist = 0
        self.property = 0
        self.ultimate = 0
        self.invincible = 0

        # for boss placement
        self.location_boss = []

    def is_added(self):
        return self.added == 1

    def is_enemy(self):
        return self.type == ENEMY

    def is_player(self):
        return self.type == PLAYER

    def is_boss(self):
        return self.type == BOSS

    def is_ally(self, character):
        return self.type == character.type

    def is_opposit(self, character):
        return self.type != character.type

    def add(self, location, character, polka_stack):
        if self.added == 1:
            #print(self.name, "is already added")
            return 0
        else:
            print("------------------------------------------------------------------")
            print("add:", character.name)

            self.added = 1
            self.location = location
            self.location_prev = location
            self.action = 2
            self.action_max = 2
            self.ultimate = 1

            self.name = character.name
            self.hp = character.hp
            self.sp = character.sp
            self.mp = character.mp
            self.hp_max = character.hp
            self.sp_max = character.sp
            self.mp_max = character.mp
            self.sp_prev = character.sp
            self.atk = character.atk
            self.property = character.property

            self.heist = self.heist + polka_stack

            # test case
            if self.name == "나무인형 A" or self.name == "벽":
                print("action = 0")
                self.action = 0
                self.action_max = 0

            # for raid
            if self.name == "아가레스":
                self.ultimate = 0
                #self.invincible = 1

            if self.name == "비프론스":
                self.ultimate = 0

            if self.name == "아토믹레이H":
                self.ultimate = 0
                self.invincible = 1

            if self.name == "아토믹레이V":
                self.ultimate = 0
                self.invincible = 1

            if self.name == "눌어붙은 땅":
                print("action = 0")
                self.action = 0
                self.action_max = 0
                self.invincible = 1

            if (self.name == "수용"
                or self.name == "용인"
                or self.name == "예측"
                or self.name == "억제"
                or self.name == "보호기제"):
                print("action = 0")
                self.action = 0
                self.action_max = 0
 

            print("------------------------------------------------------------------")
            return 1

    def add_boss(self, boss_data, polka_stack):
        return self.add("", boss_data, polka_stack)

    def set_boss(self, data1, data2, data3, data4, data5):
        print("------------------------------------------------------------------")
        print("set boss:", self.name)
            
        self.location = "BOSS"
        self.type = BOSS
        self.ultimate = 0

        print('boss location set')
        if self.name == '강철의 천사':
            self.location_boss.append('E0')
            self.location_boss.append('E1')
            self.location_boss.append('F0')
            self.location_boss.append('F1')

            #self.invincible = 1

            self.left_wing = data1
            self.right_wing = data2

            print("connect:", self.name, "->", end='')

            if self.left_wing != 0:
                print("[" + self.left_wing.name + "]", end='')
            if self.right_wing != 0:
                print("[" + self.right_wing.name + "]")

        elif self.name == '천사의 좌익':
            self.location_boss.append('C0')
            self.location_boss.append('D0')

            self.angel = data1

            print("connect:", self.name, "->", 
                  "[" + self.angel.name + "]")

        elif self.name == '천사의 우익':
            self.location_boss.append('G0')
            self.location_boss.append('H0')

            self.angel = data1

            print("connect:", self.name, "->", 
                  "[" + self.angel.name + "]")

        elif self.name == '주에즈 노엘':
            # movable boss
            self.location = 'E2'
            self.location_prev = 'E2'

            self.wall_1 = data1
            self.wall_2 = data2
            self.wall_3 = data3
            self.wall_4 = data4
            self.wall_5 = data5

            print("connect:", self.name, "->", end='')

            if self.wall_1 != 0:
                print("[" + self.wall_1.name + "]", end='')
            if self.wall_2 != 0:
                print("[" + self.wall_2.name + "]", end='')
            if self.wall_3 != 0:
                print("[" + self.wall_3.name + "]", end='')
            if self.wall_4 != 0:
                print("[" + self.wall_4.name + "]", end='')
            if self.wall_5 != 0:
                print("[" + self.wall_5.name + "]")

        elif self.name == '수용':
            self.location_boss.append('B1')
            self.location_boss.append('B2')
            self.location_boss.append('C1')

            self.robot = data1

            print("connect:", self.name, "->", 
                  "[" + self.robot.name + "]")

        elif self.name == '용인':
            self.location_boss.append('H1')
            self.location_boss.append('I1')
            self.location_boss.append('I2')

            self.robot = data1

            print("connect:", self.name, "->", 
                  "[" + self.robot.name + "]")

        elif self.name == '예측':
            self.location_boss.append('B7')
            self.location_boss.append('B8')
            self.location_boss.append('C8')

            self.robot = data1

            print("connect:", self.name, "->", 
                  "[" + self.robot.name + "]")

        elif self.name == '억제':
            self.location_boss.append('H8')
            self.location_boss.append('I7')
            self.location_boss.append('I8')

            self.robot = data1

            print("connect:", self.name, "->", 
                  "[" + self.robot.name + "]")

        elif self.name == '방어기제':
            self.location_boss.append('E4')
            self.location_boss.append('E5')
            self.location_boss.append('F4')
            self.location_boss.append('F5')

            self.robot = data1

            print("connect:", self.name, "->", 
                  "[" + self.robot.name + "]")

        print("boss location:", self.location_boss)
        print("------------------------------------------------------------------")
        return 1

    def remove(self):
        if self.added == 0:
            #print("character", str(self.num), "is already removed")
            return
        else:
            print("------------------------------------------------------------------")
            print("remove:", self.name)

            self.added = 0
            self.location = ''
            self.location_prev = ''
            self.action = 0
            self.action_max = 0

            self.name = ''
            self.hp = 0
            self.sp = 0
            self.mp = 0
            self.hp_max = 0
            self.sp_max = 0
            self.mp_max = 0
            self.sp_prev = 0
            self.atk = 0

            self.paralyze = 0
            self.poison = 0
            self.poison_remain = 0
            self.weaken = 0
            self.heist = 0
            self.enforce = 0
            self.broken = 0
            self.tank = 0
            self.provoke = 0
            self.crown = 0
            self.barrier = 0
            self.knight = -1
            self.polka = 0
            self.evade = -1

            self.save = 0
            self.hp_save = 0
            self.sp_save = 0
            self.mp_save = 0
            self.location_save = ''

            self.solist = 0
            self.property = 0
            self.ultimate = 0
            self.invincible = 0

            if self.type == BOSS:
                print("boss information reset")
                self.type = ENEMY
                self.location_boss.clear()

            print("------------------------------------------------------------------")

    def move(self, location):
        if self.added == 0:
            print(self.name, "is not added")
        else:
            self.location = location

    def set_name(self, name):
        self.name = name

    def set_hp(self, hp):
        self.hp = hp

    def set_sp(self, sp):
        self.sp = sp

    def set_mp(self, mp):
        self.mp = mp

    def decrease_hp_real(self, value):
        #value = int(value * 50 / 100)

        if self.invincible == 1:
            print(self.name, "invincible")
            return

        if self.weaken != 0:
            print(self.name, ": weaken:", self.weaken)
            modifier = 100 + 10 * (self.weaken)
            damage = int(value * modifier / 100)

        else:
            damage = value

        if self.tank == 1:
            print(self.name, ": tank:", self.tank)
            damage = int(damage * 85 / 100)

        if self.barrier != 0 and self.barrier >= damage:
            print(self.name + ": barrier:", self.barrier, "->", self.barrier - damage)
            self.barrier = self.barrier - damage
            return
        
        if self.barrier != 0 and self.barrier < damage:
            print(self.name + ": barrier:", self.barrier, "->",'0')
            damage = damage - self.barrier
            self.barrier = 0

        print(self.name + ": hp:", self.hp, "->", self.hp - damage)
        self.hp = self.hp - damage

        """
        if (self.hp <= 0):
            self.hp = 1
        """

        if (self.hp <= 0):
            print(self.name + ": hp is 0. removed.")
            raid_map.remove_character(self)
            self.remove()

    def decrease_hp(self, value):
        if self.knight != -1:
            character = raid_character.get_character(self.knight)
            if character.added == 0:
                print("dusk:", character.name, "removed")
                self.knight = 0

            else:
                print("dusk:", self.name, "to", character.name)
                character.decrease_hp_real(value)
                return

        if self.evade >= 0:
            character = raid_character.character[self.evade]
            if character.added == 0:
                print("evade:", character.name, "removed")
                self.evade = -1

            else:
                print("evade:", self.name, "to", character.name)
                character.decrease_hp_real(value)
                return

            print(self.name, ": evade:", character.evade, "->", '-2')
            character.evade = -1
            return

        if (self.name == '수용'
            or self.name == '용인'
            or self.name == '예측'
            or self.name == '억제'
            or self.name == '방어기제'):

            self.robot.decrease_hp_real(value)

        self.decrease_hp_real(value)

    def increase_hp(self, value):
        #value = int(value * 50 / 100)

        print(self.name + ": hp:", self.hp, "->", self.hp + value)

        self.hp = self.hp + value
        if (self.hp > self.hp_max):
            print(self.name + ": hp over:", self.hp, "->", self.hp_max)
            self.hp = self.hp_max

    def decrease_sp(self, sp):
        if self.sp >= sp:
            self.sp = self.sp - sp
            return False
        else:
            self.sp = 0
            print(self.name, "SP decreased under 0. Set 0")
            return True

    def increase_sp(self, sp):
        self.sp = self.sp + sp

    def decrease_mp(self, mp):
        if self.mp >= mp:
            self.mp = self.mp - mp
            return False
        else:
            self.mp = 0
            print(self.name, "MP decreased under 0. Set 0")
            return True

    def increase_mp(self, mp):
        self.mp = self.mp + mp

    def decrease_cost_without_mp(self, cost):
        if cost == COST_MAX:
            self.sp = 0
            return self.sp_max

        elif cost ==  COST_REMAIN:
            cost_used = self.sp
            self.sp = 0
            return cost_used

        elif cost >= 0:
            self.decrease_sp(cost)
            return cost

        else:
            print(self.name, "invalid cost:", cost)
            return -1

    def decrease_cost_with_mp(self, cost):
        if cost ==  COST_MAX_MP:
            self.mp = 0
            return self.mp_max

        elif cost == COST_MAX and self.mp == self.mp_max:
            self.mp = 0
            return self.mp_max

        elif cost == COST_MAX and self.sp == self.sp_max:
            self.sp = 0
            return self.sp_max

        elif cost ==  COST_REMAIN and self.mp != 0:
            cost_used = self.mp
            self.mp = 0
            return cost_used

        elif cost ==  COST_REMAIN and self.sp != 0:
            cost_used = self.sp
            self.sp = 0
            return cost_used

        elif cost >= 0 and self.mp >= cost:
            self.decrease_mp(cost)
            return cost

        elif cost >= 0 and self.mp < cost:
            self.decrease_sp(cost - self.mp)
            self.mp = 0
            return cost

        else:
            print(self.name, "invalid cost:", cost)
            return -1

    def decrease_cost(self, _cost, _property):
        if self.property == _property:
            return self.decrease_cost_with_mp(_cost)
        else:
            return self.decrease_cost_without_mp(_cost)

    def is_cost_enough_without_mp(self, cost):
        if cost ==  COST_MAX_MP:
            return False

        elif cost == COST_MAX and self.sp == self.sp_max:
            return True

        elif cost ==  COST_REMAIN and self.sp != 0:
            return True

        elif cost >= 0 and self.sp >= cost:
            return True

        elif cost >= 0:
            return False

        else:
            print(self.name, "invalid cost:", cost)
            return False

    def is_cost_enough_with_mp(self, cost):
        if cost ==  COST_MAX_MP and self.mp == self.mp_max:
            return True

        elif cost == COST_MAX and self.mp == self.mp_max:
            return True

        elif cost == COST_MAX and self.sp == self.sp_max:
            return True

        elif cost ==  COST_REMAIN and self.mp != 0:
            return True

        elif cost ==  COST_REMAIN and self.sp != 0:
            return True

        elif cost >= 0 and self.sp + self.mp >= cost:
            return True

        elif cost >= 0:
            return False

        else:
            print(self.name, "invalid cost:", cost)
            return False

    def is_cost_enough(self, _cost, _property):
        if self.property == _property:
            return self.is_cost_enough_with_mp(_cost)
        else:
            return self.is_cost_enough_without_mp(_cost)

    def is_ultimate_usable(self):
        return self.ultimate == 1

    def decrease_ultimate(self):
        self.ultimate = 0

    def decrease_action(self, action):
        if self.action >= action:
            self.action = self.action - action
            return False
        else:
            print(self.name + "action decreased under 0. ignored")
            return True

    def remove_debuff(self):

        print(self.name, "paralyze:", self.paralyze, "->", "0")
        print(self.name, "poison:", self.poison, "->", "0")
        print(self.name, "poison_remain:", self.poison_remain, "->", "0")
        print(self.name, "weaken:", self.weaken, "->", "0")
        print(self.name, "broken:", self.broken, "->", "0")

        self.paralyze = 0
        self.poison = 0
        self.poison_remain = 0
        self.weaken = 0
        self.broken = 0

    def update_location(self):
        #print("location_prev update:", self.location_prev, "->", self.location)
        self.location_prev = self.location
        self.sp_prev = self.sp

    def increase_poison(self, value):
        self.poison = self.poison + value
        self.poison_remain = 3
        if (self.poison > 10):
            self.poison = 10

    def increase_weaken(self, value):
        self.weaken = self.weaken + value
        if (self.weaken > 10):
            self.weaken = 10

    def get_damage(self, value):
        if self.enforce == 0 and self.broken == 0:
            return value

        print(self.name, ": enforce:", self.enforce, ": broken:", self.broken)
        modifier = 100 + 5 * (self.enforce - self.broken)

        return int(value * modifier / 100)

    def increase_barrier(self, value):
        #value = int(value * 50 / 100)

        self.barrier = self.barrier + value

    def get_dist_character(self, _location):
        x1 = ord(self.location[0]) - ord('A')
        y1 = ord(self.location[1]) - ord('0')

        x2 = ord(_location[0]) - ord('A')
        y2 = ord(_location[1]) - ord('0')

        return abs(x2 - x1) + abs(y2 - y1)

    def get_dist_boss(self, _location):
        if self.location != 'BOSS':
            return self.get_dist_character(_location)

        x_loc = ord(_location[0]) - ord('A')
        y_loc = ord(_location[1]) - ord('0')

        dist = 999
        for location in self.location_boss: 
            x = ord(location[0]) - ord('A')
            y = ord(location[1]) - ord('0')

            dist = min(dist, abs(x - x_loc) + abs(y - y_loc))

        return dist

    def get_dist(self, _location):
        if self.is_player() or self.is_enemy():
            return self.get_dist_character(_location)

        elif self.is_boss():
            return self.get_dist_boss(_location)

    def set_knight(self, character):
        self.knight = character.num

    def set_evade(self, character):
        self.evade = character.num

    # boss
    def is_wing_remain(self):
        return (self.left_wing != 0 or self.right_wing != 0)


# player
class characters:
    def __init__(self):
        self.character = list()
        self.enemy_offset = 0
        self.player_offset = 12

        self.polka_enemy = 0
        self.polka_player = 0

        for i in range (0, 12):
            self.character.append(runtime_character(i, ENEMY))

        for i in range (12, 24):
            self.character.append(runtime_character(i, PLAYER))

    def get_character(self, char_id):
        return self.character[char_id]

    def get_empty_enemy(self):
        for character in self.character:
            if character.is_added():
                continue

            if character.is_enemy():
                return character

        return 0

    def run_characters(self):
        for character in self.character:
            if character.added == 0:
                continue

            if character.solist > 0:
                character.solist = character.solist - 1

    def increase_player_polka(self):
        self.polka_player = self.polka_player + 1

        for character in self.character:
            if character.is_added() == False:
                continue

            elif character.is_player() == False:
                continue

            else:
                character.heist = character.heist + 1
                print(character.name + ": heist:", character.heist)

    def increase_enemy_polka(self):
        self.polka_enemy = self.polka_enemy + 1

        for character in self.character:
            if character.is_added() == False:
                continue

            elif character.is_enemy() == False and character.is_boss() == False:
                continue

            else:
                character.heist = character.heist + 1
                print(character.name + ": heist:", character.heist)

    def decrease_player_polka(self):
        self.polka_player = self.polka_player - 1

        for character in self.character:
            if character.is_added() == False:
                continue

            elif character.is_player() == False:
                continue

            else:
                character.heist = character.heist - 1
                print(character.name + ": heist:", character.heist)

    def decrease_enemy_polka(self):
        self.polka_enemy = self.polka_enemy - 1

        for character in self.character:
            if character.is_added() == False:
                continue

            elif character.is_enemy() == False and character.is_boss() == False:
                continue

            else:
                character.heist = character.heist - 1
                print(character.name + ": heist:", character.heist)

    def increase_player_hp(self, value):
        for character in self.character:
            if character.is_added() == False:
                continue

            elif character.is_player() == False:
                continue

            else:
                character.increase_hp(value)
                print(character.name + ": hp:", character.hp)

    def decrease_player_hp(self, _value):
        for character in self.character:
            if character.is_added() == False:
                continue

            elif character.is_player() == False:
                continue

            else:
                character.decrease_hp(_value)
                print(character.name + ": hp:", character.hp)

    def increase_player_weaken(self, _value):
        for character in self.character:
            if character.is_added() == False:
                continue

            elif character.is_player() == False:
                continue

            else:
                character.increase_weaken(_value)
                print(character.name + ": weaken:", character.weaken)

    def increase_enemy_hp(self, value):
        for character in self.character:
            if character.is_added() == False:
                continue

            elif character.is_enemy() == False and character.is_boss() == False:
                continue

            else:
                character.increase_hp(value)
                print(character.name + ": hp:", character.hp)

    def increase_player_barrier_range(self, _value, _location, _range):
        for character in self.character:
            if character.is_added() == False:
                continue

            elif character.is_player() == False:
                continue

            elif character.get_dist(_location) > _range:
                continue

            else:
                character.increase_barrier(_value)
                character.update_location()

    def increase_enemy_barrier_range(self, _value, _location, _range):
        for character in self.character:
            if character.is_added() == False:
                continue

            elif character.is_enemy() == False and character.is_boss() == False:
                continue

            elif character.get_dist(_location) > _range:
                continue

            else:
                character.increase_barrier(_value)
                character.update_location()

    def decrease_player_hp_range(self, _value, _location, _range):
        for character in self.character:
            if character.is_added() == False:
                continue

            elif character.is_player() == False:
                continue

            elif character.get_dist(_location) > _range:
                continue

            else:
                character.decrease_hp(_value)
                character.update_location()

    def decrease_player_hp_range_share(self, _value, _location, _range):
        total = 0
        for character in self.character:
            if character.is_added() == False:
                continue

            elif character.is_player() == False:
                continue

            elif character.get_dist(_location) > _range:
                continue

            else:
                total = total + 1

        if total != 0:
            _value = int(_value / total)
            self.decrease_player_hp_range(_value, _location, _range)

    def increase_player_broken_range(self, _value, _location, _range):
        for character in self.character:
            if character.is_added() == False:
                continue

            elif character.is_player() == False:
                continue

            elif character.get_dist(_location) > _range:
                continue

            else:
                character.broken = character.broken + _value
                character.update_location()

    def decrease_enemy_hp_range(self, _value, _location, _range):
        for character in self.character:
            if character.is_added() == False:
                continue

            elif character.is_enemy() == False and character.is_boss() == False:
                continue

            elif character.get_dist(_location) > _range:
                continue

            else:
                character.decrease_hp(_value)
                character.update_location()

    def end_turn(self):
        for character in self.character:
            if character.added == 0:
                continue

        # end of player turn. remove attack buff/debuff
            if character.is_player():
                character.action = 0
                character.enforce = 0
                character.broken = 0
                character.location_prev = character.location

        # player crown
                if character.crown == 1:
                    print(character.name, "sp remained:", character.sp)
                    print(character.name, "get enforce by crown")
                    character.enforce = character.sp

        # start of enemy turn. refresh sp & action
            elif character.is_enemy() or character.is_boss():
                #character.weaken = 0
                character.barrier = 0
                character.knight = -1
                character.solist = 0
                character.invincible = 0

                character.action = character.action_max
                character.sp = character.sp_max + character.heist
                character.sp_prev = character.sp_max + character.heist
                character.mp = character.mp_max

        # raid specialized
                if character.name == '아가레스':
                    character.invincible = 1

                if character.name == '아토믹레이H':
                    character.invincible = 1

                if character.name == '아토믹레이V':
                    character.invincible = 1

                if character.name == '강철의 천사':
                    if character.is_wing_remain():
                       character.invincible = 1

                if character.name == '눌어붙은 땅':
                    character.invincible = 1

    def end_round(self):
        for character in self.character:
            if character.added == 0:
                continue

        # poison
            if character.poison_remain != 0:
                poison_damage = character.poison * 5
                character.decrease_hp(poison_damage)

                print(character.name, "get poison damage:", poison_damage)
                print(character.name, "poison_remain:",
                      character.poison_remain, '->', character.poison_remain - 1)

                character.poison_remain = character.poison_remain - 1
                if character.poison_remain <= 0:
                    character.poison = 0
                    character.poison_remain = 0

        # end of enemy turn. remove attack buff/debuff
            if character.is_enemy() or character.is_boss():
                character.action = 0
                #character.enforce = 0
                character.broken = 0
                character.location_prev = character.location

                if character.name == '앰버':
                    character.enforce = character.enforce + 1
                else:
                    character.enforce = 0

        # player crown
                if character.crown == 1:
                    print(character.name, "sp remained:", character.sp)
                    print(character.name, "get enforce by crown")
                    character.enforce = character.sp

        # start of player turn. refresh sp & action
            elif character.is_player():
                #character.weaken = 0
                character.barrier = 0
                character.knight = -1
                character.solist = 0
                character.invincible = 0

                character.action = character.action_max
                character.sp = character.sp_max + character.heist
                character.sp_prev = character.sp_max + character.heist
                character.mp = character.mp_max

    def start_round(self):
        for character in self.character:
            if character.added == 0:
                continue

        # remove attack buff/debuff (after reset)
            character.action = 0
            character.enforce = 0
            character.broken = 0
            character.location_prev = character.location

        # start of player turn. refresh sp & action
            if character.is_player():
                character.weaken = 0
                character.barrier = 0
                character.knight = -1
                character.solist = 0
                character.invincible = 0

                character.action = character.action_max
                character.sp = character.sp_max + character.heist
                character.sp_prev = character.sp_max + character.heist
                character.mp = character.mp_max


#---------------------------------------------------------------------------------------
# progress
class progress:
    def __init__(self):
        self.rnd = 0
        self.turn = 0 # 0 = player 1 = enemy
        self.time = 0
        self.interval = 300
        self.run = 0

    def set_progress(self, rnd, turn, interval):
        self.rnd = rnd
        self.turn = turn
        self.interval = interval

    def update_progress(self):
        sh.set_status_map(0, self.rnd, self.turn,
                          self.time, self.interval, self.run)

    def is_player_turn(self):
        if (self.rnd == 0 or self.turn == 0):
            return 1

        return 0

    def is_enemy_turn(self):
        if (self.rnd == 0 or self.turn == 1):
            return 1

        return 0

    def start_progress(self):
        if self.run == 1:
            print("progress already started")

        self.run = 1

    def stop_progress(self):
        if self.run == 0:
            print("progress already stopped")

        self.run = 0

    def reset_progress(self):
        self.rnd = 0
        self.turn = 0
        self.time = 0
        self.run = 0

    def step_progress(self):
        if self.run == 1:
            return 0

        # skip init round
        if self.rnd == 0:
            self.rnd = 1

            print("------------------------------------------------------------------")
            print("Round:", self.rnd, "Turn:", self.turn)
            print("------------------------------------------------------------------")

            return 1

        # change turn
        self.time = 0
        if self.turn == 0:
            self.turn = 1

            print("------------------------------------------------------------------")
            print("Round:", self.rnd, "Turn:", self.turn)
            print("------------------------------------------------------------------")

            return 2

        # change round
        self.turn = 0
        self.rnd = self.rnd + 1

        print("------------------------------------------------------------------")
        print("Round:", self.rnd, "Turn:", self.turn)
        print("------------------------------------------------------------------")

        return 3

    def run_progress(self, enemy_remain, player_remain):
        if self.run == 0:
            return 0

        # skip init round
        if self.rnd == 0:
            self.rnd = 1

            print("------------------------------------------------------------------")
            print("Round:", self.rnd, "Turn:", self.turn)
            print("------------------------------------------------------------------")

            return 1

        self.time = self.time + 1

        # check player turn end
        if self.turn == 0:
            if player_remain != 0 and self.time <= self.interval:
                return 0

        elif self.turn == 1:
            if enemy_remain != 0 and self.time <= self.interval:
                return 0

        # change turn
        self.time = 0
        if self.turn == 0:
            self.turn = 1

            print("------------------------------------------------------------------")
            print("Round:", self.rnd, "Turn:", self.turn)
            print("------------------------------------------------------------------")

            return 2

        # change round
        self.turn = 0
        self.rnd = self.rnd + 1

        print("------------------------------------------------------------------")
        print("Round:", self.rnd, "Turn:", self.turn)
        print("------------------------------------------------------------------")

        return 3

#---------------------------------------------------------------------------------------
# command
class command:
    def __init__(self):
        self.cmd = ''
        self.count = 0
        self.result = ''

        self.move = ''
        self.action = ''
        self.target = ''
        self.event = ''

        self.need_update = 0
        self.need_update_console = 0

    def set_cmd(self, cmd, move, action, target, event):
        self.cmd = cmd
        self.move = move
        self.action = action
        self.target = target
        self.event = event

    def update_cmd(self, result):
        self.result = result
        self.count = self.count + 1
        self.need_update = 1

    def update_cmd_console(self, result):
        self.result = result
        self.count = self.count + 1
        self.need_update = 1
        self.need_update_console = 1

    def print_cmd(self):
        print("cmd:", self.cmd, "move:", self.move, "action:", self.action,
              "target:", self.target, "event:", self.event)

    def get_cmd(self):
        return self.cmd

    def get_count(self):
        return self.count

    def get_result(self):
        return self.result

    def get_move(self):
        return self.move

    def get_action(self):
        return self.action

    def get_target(self):
        return self.target

    def get_event(self):
        return self.event


class command_list:
    def __init__(self):
        self.commands = list()

        for i in range (0, 32):
            self.commands.append(command())

        self.map_offset = 0
        self.char_offset = 1

    def set_map_cmd(self, cmd):
        self.commands[self.map_offset].set_cmd(cmd, '', '', '', '')

    def set_character_cmd(self, char_id, cmd, move, action, target, event):
        self.commands[self.char_offset + char_id].set_cmd(cmd, move, action, target, event)

    def print_all_cmd(self):
        print("map")
        self.commands[self.map_offset].print_cmd()
        print("character")
        for i in range (0, 24):
            self.commands[self.char_offset + i].print_cmd()

# map
    def get_map_command(self):
        return self.commands[self.map_offset]

# character
    def get_character_command(self, char_id):
        return self.commands[self.char_offset + char_id]


#---------------------------------------------------------------------------------------
#runtime
class runtime:
    def __init__(self):
        self.gc = gspread.service_account(filename="./gspread.json")
        self.sh = self.gc.open("bus station test sheet").worksheet("runtime")

    # runtime command
        self.commands = command_list()

    # runtime data
        self.map = map_data()
        self.character = characters()
        self.progress = progress()

    # data range
        self.range_cmd = 'A1:H27'
        self.range_data = 'A28:AM54'

	# offset
        self.map_offset = 1
        self.character_offset = 3

    # id
        self.id = 0

    # command
        self.cmd = 1
        self.move = 4
        self.action_cmd = 5
        self.target = 6
        self.event = 7

    # runtime - map
        self.round = 1
        self.turn = 2
        self.time = 3
        self.interval = 4
        self.run = 5
        self.polka_e = 6
        self.polka_p = 7

    # runtime - character
        self.name = 1
        self.location = 2
        self.action = 3
        self.hp = 4
        self.sp = 5
        self.mp = 6
        self.action_max = 7
        self.hp_max = 8
        self.sp_max = 9
        self.mp_max = 10
        self.atk = 11
        self.paralyze = 12
        self.paralyze_remain = 13
        self.poison = 14
        self.poison_remain = 15
        self.weaken = 16
        self.weaken_remain = 17
        self.heist = 18
        self.enforce = 19
        self.broken = 20
        self.tank = 21
        self.provoke = 22
        self.crown = 23
        self.barrier = 24
        self.knight = 25
        self.polka = 26
        self.evade = 27
        self.save = 28
        self.hp_save = 29
        self.sp_save = 30
        self.mp_save = 31
        self.location_save = 32

        self.location_prev = 33
        self.sp_prev = 34

        self.solist = 35
        self.property = 36
        self.ultimate = 37
        self.invincible = 38

        global raid_map
        raid_map = self.map

        global raid_character
        raid_character = self.character

    def get_runtime_cmd(self):
        try:
            self.runtime_cmd = self.sh.get_values(self.range_cmd)
            return 0

        except:
            return 1

    def get_runtime_data(self):
        try:
            self.data = self.sh.get_values(self.range_data)
            return 0

        except:
            return 1
            
    def get_runtime(self):
        while self.get_runtime_cmd():
            time.sleep(1)

        while self.get_runtime_data():
            time.sleep(1)

    def sync_runtime(self):
        while self.get_runtime_data():
            time.sleep(1)

        self.progress.rnd = int(self.data[self.map_offset][self.round])
        self.progress.turn = int(self.data[self.map_offset][self.turn])
        self.progress.time = int(self.data[self.map_offset][self.time])
        self.progress.interval = int(self.data[self.map_offset][self.interval])
        self.progress.run = int(self.data[self.map_offset][self.run])

        self.character.polka_enemy = int(self.data[self.map_offset][self.polka_e])
        self.character.polka_player = int(self.data[self.map_offset][self.polka_p])

        # for boss sync
        angel_exist = 0
        left_wing_char = 0
        right_wing_char = 0
        
        robot_exist = 0
        wall_1 = 0
        wall_2 = 0
        wall_3 = 0
        wall_4 = 0
        wall_5 = 0

        # sync characters
        for i in range(0, 24):
            location = self.data[self.character_offset + i][self.location]
            if location != '':
                character = self.character.get_character(i)

                character.added = 1
                character.name = self.data[self.character_offset + i][self.name]

                character.location = self.data[self.character_offset + i][self.location]
                character.action = int(self.data[self.character_offset + i][self.action])
                character.hp = int(self.data[self.character_offset + i][self.hp])
                character.sp = int(self.data[self.character_offset + i][self.sp])
                character.mp = int(self.data[self.character_offset + i][self.mp])

                character.action_max = int(self.data[self.character_offset + i][self.action_max])
                character.hp_max = int(self.data[self.character_offset + i][self.hp_max])
                character.sp_max = int(self.data[self.character_offset + i][self.sp_max])
                character.mp_max = int(self.data[self.character_offset + i][self.mp_max])
                character.atk = int(self.data[self.character_offset + i][self.atk])

                character.paralyze = int(self.data[self.character_offset + i][self.paralyze])
                character.paralyze_remain = int(self.data[self.character_offset + i][self.paralyze_remain])

                character.poison = int(self.data[self.character_offset + i][self.poison])
                character.poison_remain = int(self.data[self.character_offset + i][self.poison_remain])
                character.weaken = int(self.data[self.character_offset + i][self.weaken])
                character.heist = int(self.data[self.character_offset + i][self.heist])
                character.enforce = int(self.data[self.character_offset + i][self.enforce])
                character.broken = int(self.data[self.character_offset + i][self.broken])
                character.tank = int(self.data[self.character_offset + i][self.tank])
                character.provoke = int(self.data[self.character_offset + i][self.provoke])
                character.crown = int(self.data[self.character_offset + i][self.crown])
                character.barrier = int(self.data[self.character_offset + i][self.barrier])
                character.knight = int(self.data[self.character_offset + i][self.knight])
                character.polka = int(self.data[self.character_offset + i][self.polka])
                character.evade = int(self.data[self.character_offset + i][self.evade])

                character.save = int(self.data[self.character_offset + i][self.save])
                character.hp_save = int(self.data[self.character_offset + i][self.hp_save])
                character.sp_save = int(self.data[self.character_offset + i][self.sp_save])
                character.mp_save = int(self.data[self.character_offset + i][self.mp_save])
                character.location_save = self.data[self.character_offset + i][self.location_save]

                character.location_prev = self.data[self.character_offset + i][self.location_prev]
                character.sp_prev = int(self.data[self.character_offset + i][self.sp_prev])

                character.solist = int(self.data[self.character_offset + i][self.solist])
                character.property = int(self.data[self.character_offset + i][self.property])
                character.ultimate = int(self.data[self.character_offset + i][self.ultimate])
                character.invincible = int(self.data[self.character_offset + i][self.invincible])

                if location != 'BOSS':
                    self.map.place_character(character.num, character.location)

                if character.name == '강철의 천사':
                    angel_exist = 1
                    angel_char = character

                if character.name == '천사의 좌익':
                    left_wing_char = character

                if character.name == '천사의 우익':
                    right_wing_char = character

                if character.name == '주에즈 노엘':
                    robot_exist = 1
                    robot = character

                if character.name == '수용':
                    wall_1 = character

                if character.name == '용인':
                    wall_2 = character

                if character.name == '예측':
                    wall_3 = character

                if character.name == '억제':
                    wall_4 = character

                if character.name == '방어기제':
                    wall_5 = character

        # for angel raid
        if angel_exist == 1:
            angel_char.set_boss(left_wing_char, right_wing_char)

        if left_wing_char != 0:
            left_wing_char.set_boss(angel_char, 0)

        if right_wing_char != 0:
            right_wing_char.set_boss(angel_char, 0)

        if angel_exist == 1:
            self.map.place_boss(angel_char)

        if left_wing_char != 0:
            self.map.place_boss(left_wing_char)

        if right_wing_char != 0:
            self.map.place_boss(right_wing_char)

        # for robot raid
        if robot_exist == 1:
            robot.set_boss(wall_1, wall_2, wall_3, wall_4, wall_5)
            self.map.place_boss(robot)

            if wall_1 != 0:
                wall_1.set_boss(robot, 0, 0, 0, 0)
                self.map.place_boss(wall_1)

            if wall_2 != 0:
                wall_2.set_boss(robot, 0, 0, 0, 0)
                self.map.place_boss(wall_2)

            if wall_3 != 0:
                wall_3.set_boss(robot, 0, 0, 0, 0)
                self.map.place_boss(wall_3)

            if wall_4 != 0:
                wall_4.set_boss(robot, 0, 0, 0, 0)
                self.map.place_boss(wall_4)

            if wall_5 != 0:
                wall_5.set_boss(robot, 0, 0, 0, 0)
                self.map.place_boss(wall_5)

            
    def parse_command(self):
        commands = self.commands
        commands.set_map_cmd(self.runtime_cmd[self.map_offset][self.cmd])

        for i in range(0, 24):
            commands.set_character_cmd(i,
                                       self.runtime_cmd[self.character_offset + i][self.cmd],
                                       self.runtime_cmd[self.character_offset + i][self.move],
                                       self.runtime_cmd[self.character_offset + i][self.action_cmd],
                                       self.runtime_cmd[self.character_offset + i][self.target],
                                       self.runtime_cmd[self.character_offset + i][self.event])

    def update_runtime_data(self):
        # map
        self.data[self.map_offset][self.round] = self.progress.rnd
        self.data[self.map_offset][self.turn] = self.progress.turn
        self.data[self.map_offset][self.time] = self.progress.time
        self.data[self.map_offset][self.interval] = self.progress.interval
        self.data[self.map_offset][self.run] = self.progress.run

        self.data[self.map_offset][self.polka_e] = self.character.polka_enemy
        self.data[self.map_offset][self.polka_p] = self.character.polka_player

        for i in range(0, 24):
            character = self.character.get_character(i)

            self.data[self.character_offset + i][self.name] = character.name
            self.data[self.character_offset + i][self.location] = character.location
            self.data[self.character_offset + i][self.action] = character.action
            self.data[self.character_offset + i][self.hp] = character.hp
            self.data[self.character_offset + i][self.sp] = character.sp
            self.data[self.character_offset + i][self.mp] = character.mp

            self.data[self.character_offset + i][self.action_max] = character.action_max
            self.data[self.character_offset + i][self.hp_max] = character.hp_max
            self.data[self.character_offset + i][self.sp_max] = character.sp_max
            self.data[self.character_offset + i][self.mp_max] = character.mp_max

            self.data[self.character_offset + i][self.atk] = character.atk

            self.data[self.character_offset + i][self.paralyze] = character.paralyze
            self.data[self.character_offset + i][self.paralyze_remain] = character.paralyze_remain
            self.data[self.character_offset + i][self.poison] = character.poison
            self.data[self.character_offset + i][self.poison_remain] = character.poison_remain
            self.data[self.character_offset + i][self.weaken] = character.weaken
            self.data[self.character_offset + i][self.weaken_remain] = character.weaken_remain

            self.data[self.character_offset + i][self.heist] = character.heist
            self.data[self.character_offset + i][self.enforce] = character.enforce
            self.data[self.character_offset + i][self.broken] = character.broken
            self.data[self.character_offset + i][self.tank] = character.tank
            self.data[self.character_offset + i][self.provoke] = character.provoke
            self.data[self.character_offset + i][self.crown] = character.crown
            self.data[self.character_offset + i][self.barrier] = character.barrier
            self.data[self.character_offset + i][self.knight] = character.knight
            self.data[self.character_offset + i][self.polka] = character.polka
            self.data[self.character_offset + i][self.evade] = character.evade

            self.data[self.character_offset + i][self.save] = character.save
            self.data[self.character_offset + i][self.hp_save] = character.hp_save
            self.data[self.character_offset + i][self.sp_save] = character.sp_save
            self.data[self.character_offset + i][self.mp_save] = character.mp_save
            self.data[self.character_offset + i][self.location_save] = character.location_save

            self.data[self.character_offset + i][self.location_prev] = character.location_prev
            self.data[self.character_offset + i][self.sp_prev] = character.sp_prev

            self.data[self.character_offset + i][self.solist] = character.solist
            self.data[self.character_offset + i][self.property] = character.property
            self.data[self.character_offset + i][self.ultimate] = character.ultimate
            self.data[self.character_offset + i][self.invincible] = character.invincible

    def update_runtime(self):
        try:
            update_buffer = list()
            update_buffer.append({'range': self.range_data,'values': self.data}) 

            # cmd map
            command = self.commands.get_map_command()
            if command.need_update == 1:
                command.need_update = 0
                update_buffer.append({'range': 'B2:B2','values': [['']]})
                update_buffer.append({'range': 'C2:C2','values': [[command.get_count()]]})
                update_buffer.append({'range': 'D2:D2','values': [[command.get_result()]]})

            # cmd enemy
            command = self.commands.get_character_command(0)
            if command.need_update == 1:
                command.need_update = 0
                update_buffer.append({'range': 'B4:B4','values': [['']]})
                update_buffer.append({'range': 'C4:C4','values': [[command.get_count()]]})
                update_buffer.append({'range': 'D4:D4','values': [[command.get_result()]]})

            command = self.commands.get_character_command(1)
            if command.need_update == 1:
                command.need_update = 0
                update_buffer.append({'range': 'B5:B5','values': [['']]})
                update_buffer.append({'range': 'C5:C5','values': [[command.get_count()]]})
                update_buffer.append({'range': 'D5:D5','values': [[command.get_result()]]})

            command = self.commands.get_character_command(2)
            if command.need_update == 1:
                command.need_update = 0
                update_buffer.append({'range': 'B6:B6','values': [['']]})
                update_buffer.append({'range': 'C6:C6','values': [[command.get_count()]]})
                update_buffer.append({'range': 'D6:D6','values': [[command.get_result()]]})

            command = self.commands.get_character_command(3)
            if command.need_update == 1:
                command.need_update = 0
                update_buffer.append({'range': 'B7:B7','values': [['']]})
                update_buffer.append({'range': 'C7:C7','values': [[command.get_count()]]})
                update_buffer.append({'range': 'D7:D7','values': [[command.get_result()]]})

            command = self.commands.get_character_command(4)
            if command.need_update == 1:
                command.need_update = 0
                update_buffer.append({'range': 'B8:B8','values': [['']]})
                update_buffer.append({'range': 'C8:C8','values': [[command.get_count()]]})
                update_buffer.append({'range': 'D8:D8','values': [[command.get_result()]]})

            command = self.commands.get_character_command(5)
            if command.need_update == 1:
                command.need_update = 0
                update_buffer.append({'range': 'B9:B9','values': [['']]})
                update_buffer.append({'range': 'C9:C9','values': [[command.get_count()]]})
                update_buffer.append({'range': 'D9:D9','values': [[command.get_result()]]})

            command = self.commands.get_character_command(6)
            if command.need_update == 1:
                command.need_update = 0
                update_buffer.append({'range': 'B10:B10','values': [['']]})
                update_buffer.append({'range': 'C10:C10','values': [[command.get_count()]]})
                update_buffer.append({'range': 'D10:D10','values': [[command.get_result()]]})

            command = self.commands.get_character_command(7)
            if command.need_update == 1:
                command.need_update = 0
                update_buffer.append({'range': 'B11:B11','values': [['']]})
                update_buffer.append({'range': 'C11:C11','values': [[command.get_count()]]})
                update_buffer.append({'range': 'D11:D11','values': [[command.get_result()]]})

            command = self.commands.get_character_command(8)
            if command.need_update == 1:
                command.need_update = 0
                update_buffer.append({'range': 'B12:B12','values': [['']]})
                update_buffer.append({'range': 'C12:C12','values': [[command.get_count()]]})
                update_buffer.append({'range': 'D12:D12','values': [[command.get_result()]]})

            command = self.commands.get_character_command(9)
            if command.need_update == 1:
                command.need_update = 0
                update_buffer.append({'range': 'B13:B13','values': [['']]})
                update_buffer.append({'range': 'C13:C13','values': [[command.get_count()]]})
                update_buffer.append({'range': 'D13:D13','values': [[command.get_result()]]})

            command = self.commands.get_character_command(10)
            if command.need_update == 1:
                command.need_update = 0
                update_buffer.append({'range': 'B14:B14','values': [['']]})
                update_buffer.append({'range': 'C14:C14','values': [[command.get_count()]]})
                update_buffer.append({'range': 'D14:D14','values': [[command.get_result()]]})

            command = self.commands.get_character_command(11)
            if command.need_update == 1:
                command.need_update = 0
                update_buffer.append({'range': 'B15:B15','values': [['']]})
                update_buffer.append({'range': 'C15:C15','values': [[command.get_count()]]})
                update_buffer.append({'range': 'D15:D15','values': [[command.get_result()]]})

            command = self.commands.get_character_command(12)
            if command.need_update == 1:
                command.need_update = 0
                update_buffer.append({'range': 'B16:B16','values': [['']]})
                update_buffer.append({'range': 'C16:C16','values': [[command.get_count()]]})
                update_buffer.append({'range': 'D16:D16','values': [[command.get_result()]]})

            command = self.commands.get_character_command(13)
            if command.need_update == 1:
                command.need_update = 0
                update_buffer.append({'range': 'B17:B17','values': [['']]})
                update_buffer.append({'range': 'C17:C17','values': [[command.get_count()]]})
                update_buffer.append({'range': 'D17:D17','values': [[command.get_result()]]})

            command = self.commands.get_character_command(14)
            if command.need_update == 1:
                command.need_update = 0
                update_buffer.append({'range': 'B18:B18','values': [['']]})
                update_buffer.append({'range': 'C18:C18','values': [[command.get_count()]]})
                update_buffer.append({'range': 'D18:D18','values': [[command.get_result()]]})

            command = self.commands.get_character_command(15)
            if command.need_update == 1:
                command.need_update = 0
                update_buffer.append({'range': 'B19:B19','values': [['']]})
                update_buffer.append({'range': 'C19:C19','values': [[command.get_count()]]})
                update_buffer.append({'range': 'D19:D19','values': [[command.get_result()]]})

            command = self.commands.get_character_command(16)
            if command.need_update == 1:
                command.need_update = 0
                update_buffer.append({'range': 'B20:B20','values': [['']]})
                update_buffer.append({'range': 'C20:C20','values': [[command.get_count()]]})
                update_buffer.append({'range': 'D20:D20','values': [[command.get_result()]]})

            command = self.commands.get_character_command(17)
            if command.need_update == 1:
                command.need_update = 0
                update_buffer.append({'range': 'B21:B21','values': [['']]})
                update_buffer.append({'range': 'C21:C21','values': [[command.get_count()]]})
                update_buffer.append({'range': 'D21:D21','values': [[command.get_result()]]})

            command = self.commands.get_character_command(18)
            if command.need_update == 1:
                command.need_update = 0
                update_buffer.append({'range': 'B22:B22','values': [['']]})
                update_buffer.append({'range': 'C22:C22','values': [[command.get_count()]]})
                update_buffer.append({'range': 'D22:D22','values': [[command.get_result()]]})

            command = self.commands.get_character_command(19)
            if command.need_update == 1:
                command.need_update = 0
                update_buffer.append({'range': 'B23:B23','values': [['']]})
                update_buffer.append({'range': 'C23:C23','values': [[command.get_count()]]})
                update_buffer.append({'range': 'D23:D23','values': [[command.get_result()]]})

            command = self.commands.get_character_command(20)
            if command.need_update == 1:
                command.need_update = 0
                update_buffer.append({'range': 'B24:B24','values': [['']]})
                update_buffer.append({'range': 'C24:C24','values': [[command.get_count()]]})
                update_buffer.append({'range': 'D24:D24','values': [[command.get_result()]]})

            command = self.commands.get_character_command(21)
            if command.need_update == 1:
                command.need_update = 0
                update_buffer.append({'range': 'B25:B25','values': [['']]})
                update_buffer.append({'range': 'C25:C25','values': [[command.get_count()]]})
                update_buffer.append({'range': 'D25:D25','values': [[command.get_result()]]})

            command = self.commands.get_character_command(22)
            if command.need_update == 1:
                command.need_update = 0
                update_buffer.append({'range': 'B26:B26','values': [['']]})
                update_buffer.append({'range': 'C26:C26','values': [[command.get_count()]]})
                update_buffer.append({'range': 'D26:D26','values': [[command.get_result()]]})

            command = self.commands.get_character_command(23)
            if command.need_update == 1:
                command.need_update = 0
                update_buffer.append({'range': 'B27:B27','values': [['']]})
                update_buffer.append({'range': 'C27:C27','values': [[command.get_count()]]})
                update_buffer.append({'range': 'D27:D27','values': [[command.get_result()]]})

            self.sh.batch_update(update_buffer)
            return 0

        except:
            return 1

    def run_runtime(self):
        self.character.run_characters()

        enemy_remain = 0
        for enemy_num in range(0, 12):
            enemy = self.character.get_character(enemy_num)
            if enemy.action != 0:
                enemy_remain = 1

        player_remain = 0
        for player_num in range(12, 24):
            player = self.character.get_character(player_num)
            if player.action != 0:
                player_remain = 1

        result = self.progress.run_progress(enemy_remain, player_remain)
        if result == 1:
            self.character.start_round()

        elif result == 2:
            self.character.end_turn()

        elif result == 3:
            self.character.end_round()
