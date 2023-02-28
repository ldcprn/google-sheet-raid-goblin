import gspread
import time

import raid_data
import raid_runtime


# common functions
def get_dist(location1, location2):
    x1 = ord(location1[0]) - ord('A')
    y1 = ord(location1[1]) - ord('0')

    x2 = ord(location2[0]) - ord('A')
    y2 = ord(location2[1]) - ord('0')

    return abs(x2 - x1) + abs(y2 - y1)


#---------------------------------------------------------------------------------------
# Google Sheet API functions
class console:
    def __init__(self, json_path, sh_name):
        self.gc = gspread.service_account(filename=json_path)
        self.sh = self.gc.open("bus station test sheet").worksheet(sh_name)

        self.update_buffer = list()

    def connect_command(self,
                        command_0, command_1, command_2,
                        command_3, command_4, command_5):
        self.command_0 = command_0
        self.command_1 = command_1
        self.command_2 = command_2
        self.command_3 = command_3
        self.command_4 = command_4
        self.command_5 = command_5

    def update_console_0(self):
        self.update_buffer.append({'range': 'P4:P4','values': [[False]]})
        self.update_buffer.append({'range': 'O6:O6','values': [[False]]})
        self.update_buffer.append({'range': 'P6:P6','values': [[False]]})
        self.update_buffer.append({'range': 'Q6:Q6','values': [[False]]})
        self.update_buffer.append({'range': 'Q10:Q10','values': [[False]]})

    def update_console_1(self):
        self.update_buffer.append({'range': 'P21:P21','values': [[False]]})
        self.update_buffer.append({'range': 'O23:O23','values': [[False]]})
        self.update_buffer.append({'range': 'P23:P23','values': [[False]]})
        self.update_buffer.append({'range': 'Q23:Q23','values': [[False]]})
        self.update_buffer.append({'range': 'Q27:Q27','values': [[False]]})

    def update_console_2(self):
        self.update_buffer.append({'range': 'P38:P38','values': [[False]]})
        self.update_buffer.append({'range': 'O40:O40','values': [[False]]})
        self.update_buffer.append({'range': 'P40:P40','values': [[False]]})
        self.update_buffer.append({'range': 'Q40:Q40','values': [[False]]})
        self.update_buffer.append({'range': 'Q44:Q44','values': [[False]]})

    def update_console_3(self):
        self.update_buffer.append({'range': 'AI4:AI4','values': [[False]]})
        self.update_buffer.append({'range': 'AH6:AH6','values': [[False]]})
        self.update_buffer.append({'range': 'AI6:AI6','values': [[False]]})
        self.update_buffer.append({'range': 'AJ6:AJ6','values': [[False]]})
        self.update_buffer.append({'range': 'AJ10:AJ10','values': [[False]]})

    def update_console_4(self):
        self.update_buffer.append({'range': 'AI21:AI21','values': [[False]]})
        self.update_buffer.append({'range': 'AH23:AH23','values': [[False]]})
        self.update_buffer.append({'range': 'AI23:AI23','values': [[False]]})
        self.update_buffer.append({'range': 'AJ23:AJ23','values': [[False]]})
        self.update_buffer.append({'range': 'AJ27:AJ27','values': [[False]]})

    def update_console_5(self):
        self.update_buffer.append({'range': 'AI38:AI38','values': [[False]]})
        self.update_buffer.append({'range': 'AH40:AH40','values': [[False]]})
        self.update_buffer.append({'range': 'AI40:AI40','values': [[False]]})
        self.update_buffer.append({'range': 'AJ40:AJ40','values': [[False]]})
        self.update_buffer.append({'range': 'AJ44:AJ44','values': [[False]]})

    def update_console(self):
        try:
            self.update_buffer.clear()

            # console 0
            if self.command_0.need_update_console == 1:
                self.command_0.need_update_console = 0
                self.update_console_0()

            # console 1
            if self.command_1.need_update_console == 1:
                self.command_1.need_update_console = 0
                self.update_console_1()

            # console 2
            if self.command_2.need_update_console == 1:
                self.command_2.need_update_console = 0
                self.update_console_2()

            # console 3
            if self.command_3.need_update_console == 1:
                self.command_3.need_update_console = 0
                self.update_console_3()

            # console 4
            if self.command_4.need_update_console == 1:
                self.command_4.need_update_console = 0
                self.update_console_4()

            # console 5
            if self.command_5.need_update_console == 1:
                self.command_5.need_update_console = 0
                self.update_console_5()

            self.sh.batch_update(self.update_buffer)
            return 0

        except:
            return 1

#---------------------------------------------------------------------------------------
# cost
COST_REMAIN = -1
COST_MAX = -2
COST_MAX_MP = -3

# property
PROPERTY_NONE = 0
PROPERTY_POEM = 1
PROPERTY_SOLA = 2
PROPERTY_ORBIT = 3
PROPERTY_VOID = 4

#---------------------------------------------------------------------------------------
def dance(character, runtime):
    result = "[" + character.name + "]의 [대기]"

    cost = 0
    action = 1
    _property = PROPERTY_NONE

    if character.is_cost_enough(cost, _property) == False:
        result = result + "SP 부족"
        print(result)
        print("------------------------------------------------------------------")
        return result

    character.decrease_cost(cost, _property)
    character.decrease_action(action)
    character.update_location()

    print(result)
    print("------------------------------------------------------------------")
    return result

#---------------------------------------------------------------------------------------
def attack_2(character, target_location, runtime):
    result = "[" + character.name + "]의 [회심의 일격]: "

    _cost = COST_REMAIN
    _action = 1
    _property = PROPERTY_NONE

    if character.is_cost_enough(_cost, _property) == False:
        result = result + "SP 부족"
        print(result)
        print("------------------------------------------------------------------")
        return result

    x = ord(target_location[0]) - ord('A')
    y = ord(target_location[1]) - ord('0')
    if (x < 0) or (x > 9) or (y < 0) or (y > 9):
        result = result + "잘못된 위치"
        print(result)
        print("------------------------------------------------------------------")
        return result

    if runtime.map.is_placed(target_location) == 0:
        result = result + "대상 없음"
        print(result)
        print("------------------------------------------------------------------")
        return result

    target_dist = get_dist(character.location, target_location)
    if target_dist > 1:
        result = result + "사거리 바깥"
        print(result)
        print("------------------------------------------------------------------")
        return result

    _damage = character.decrease_cost(_cost, _property) * 5
    _damage = character.get_damage(_damage)

    character.decrease_cost(_cost, _property)
    character.decrease_action(_action)
    character.update_location()

    target_id = runtime.map.get_character_placed(target_location)
    target = runtime.character.get_character(target_id)
    result = result + "[" + target.name + "]에게 " + "[피해 " + str(_damage) + "]"

    target.decrease_hp(_damage)
    target.update_location()

    print(result)
    print("------------------------------------------------------------------")
    return result

#---------------------------------------------------------------------------------------
def attack(character, target_location, runtime):
    result = "[" + character.name + "]의 [공격]: "

    cost = 1
    action = 1
    _property = PROPERTY_NONE

    if character.is_cost_enough(cost, _property) == False:
        result = result + "SP 부족"
        print(result)
        print("------------------------------------------------------------------")
        return result

    x = ord(target_location[0]) - ord('A')
    y = ord(target_location[1]) - ord('0')
    if (x < 0) or (x > 9) or (y < 0) or (y > 9):
        result = result + "잘못된 위치"
        print(result)
        print("------------------------------------------------------------------")
        return result

    if runtime.map.is_placed(target_location) == 0:
        result = result + "대상 없음"
        print(result)
        print("------------------------------------------------------------------")
        return result

    target_dist = get_dist(character.location, target_location)
    if target_dist > 1:
        result = result + "사거리 바깥"
        print(result)
        print("------------------------------------------------------------------")
        return result

    character.decrease_cost(cost, _property)
    character.decrease_action(action)
    character.update_location()

    damage = character.get_damage(character.atk)

    target_id = runtime.map.get_character_placed(target_location)
    target = runtime.character.get_character(target_id)
    result = result + "[" + target.name + "]에게 " + "[피해 " + str(damage) + "]"

    target.decrease_hp(damage)
    target.update_location()

    print(result)
    print("------------------------------------------------------------------")
    return result

#---------------------------------------------------------------------------------------
def throw(character, target_location, runtime):
    result = "[" + character.name + "]의 [견제]: "

    cost = 1
    action = 1
    _property = PROPERTY_NONE

    if character.is_cost_enough(cost, _property) == False:
        result = result + "SP 부족"
        print(result)
        print("------------------------------------------------------------------")
        return result

    x = ord(target_location[0]) - ord('A')
    y = ord(target_location[1]) - ord('0')
    if (x < 0) or (x > 9) or (y < 0) or (y > 9):
        result = result + "잘못된 위치"
        print(result)
        print("------------------------------------------------------------------")
        return result

    if runtime.map.is_placed(target_location) == 0:
        result = result + "대상 없음"
        print(result)
        print("------------------------------------------------------------------")
        return result

    target_dist = get_dist(character.location, target_location)
    if target_dist > 3:
        result = result + "사거리 바깥"
        print(result)
        print("------------------------------------------------------------------")
        return result

    character.decrease_cost(cost, _property)
    character.decrease_action(action)
    character.update_location()

    damage = character.get_damage(5)

    target_id = runtime.map.get_character_placed(target_location)
    target = runtime.character.get_character(target_id)
    result = result + "[" + target.name + "]에게 " + "[피해 " + str(damage) + "]"

    target.decrease_hp(damage)
    target.update_location()

    print(result)
    print("------------------------------------------------------------------")
    return result

#---------------------------------------------------------------------------------------
def aid(character, runtime):
    result = "[" + character.name + "]의 [긴급 재생]: "

    cost = 3
    action = 1
    _property = PROPERTY_NONE

    if character.is_cost_enough(cost, _property) == False:
        result = result + "SP 부족"
        print(result)
        print("------------------------------------------------------------------")
        return result

    character.decrease_cost(cost, _property)
    character.decrease_action(action)

    result = result + "자신에게 [치유 20]"

    character.increase_hp(20)
    character.update_location()

    print(result)
    print("------------------------------------------------------------------")
    return result

#---------------------------------------------------------------------------------------
def solist(character, runtime):
    result = "[" + character.name + "]의 [모닝스타 솔리스트]: "

    cost = 3
    action = 1
    _property = PROPERTY_POEM

    if character.is_cost_enough(cost, _property) == False:
        result = result + "SP 부족"
        print(result)
        return result

    character.solist = 10

    character.decrease_cost(cost, _property)
    character.decrease_action(action)
    character.update_location()

    result = result + "성공. [관측 10]"
    print(result)
    print("------------------------------------------------------------------")
    return result

#---------------------------------------------------------------------------------------
def nocturn(character, target_location, runtime):
    result = "[" + character.name + "]의 [콘스텔라 녹턴]: "

    cost = 4
    action = 1
    _property = PROPERTY_POEM

    if character.is_cost_enough(cost, _property) == False:
        result = result + "SP 부족"
        print(result)
        print("------------------------------------------------------------------")
        return result

    x = ord(target_location[0]) - ord('A')
    y = ord(target_location[1]) - ord('0')
    if (x < 0) or (x > 9) or (y < 0) or (y > 9):
        result = result + "잘못된 위치"
        print(result)
        print("------------------------------------------------------------------")
        return result

    if runtime.map.is_placed(target_location) == 0:
        result = result + "대상 없음"
        print(result)
        print("------------------------------------------------------------------")
        return result

    target_dist = get_dist(character.location, target_location)
    if target_dist > 3:
        result = result + "사거리 바깥"
        print(result)
        print("------------------------------------------------------------------")
        return result

    character.decrease_cost(cost, _property)
    character.decrease_action(action)
    character.update_location()

    target_id = runtime.map.get_character_placed(target_location)
    target = runtime.character.get_character(target_id)
    result = result + "[" + target.name + "]에게 [약화 해제]"

    target.remove_debuff()
    target.update_location()

    print(result)
    print("------------------------------------------------------------------")
    return result

#---------------------------------------------------------------------------------------
def song(character, target_location, runtime):
    result = "[" + character.name + "]의 [솔스티스 송]: "

    cost = COST_REMAIN
    action = 1
    _property = PROPERTY_POEM

    if character.is_cost_enough(cost, _property) == False:
        result = result + "SP 부족"
        print(result)
        print("------------------------------------------------------------------")
        return result

    x = ord(target_location[0]) - ord('A')
    y = ord(target_location[1]) - ord('0')
    if (x < 0) or (x > 9) or (y < 0) or (y > 9):
        result = result + "잘못된 위치"
        print(result)
        print("------------------------------------------------------------------")
        return result

    if runtime.map.is_placed(target_location) == 0:
        result = result + "대상 없음"
        print(result)
        print("------------------------------------------------------------------")
        return result

    target_dist = get_dist(character.location, target_location)
    if target_dist > 3:
        result = result + "사거리 바깥"
        print(result)
        print("------------------------------------------------------------------")
        return result

    heal = character.decrease_cost(cost, _property) * 10

    character.decrease_action(action)
    character.update_location()

    target_id = runtime.map.get_character_placed(target_location)
    target = runtime.character.get_character(target_id)
    result = result + "[" + target.name + "]에게 " + "[치유 " + str(heal) + "]"

    target.increase_hp(heal)
    target.update_location()

    print(result)
    print("------------------------------------------------------------------")
    return result

#---------------------------------------------------------------------------------------
def sonata(character, runtime):
    result = "[" + character.name + "]의 [밀키웨이 소나타]: "

    cost = COST_REMAIN
    action = 1
    _property = PROPERTY_POEM

    if character.is_cost_enough(cost, _property) == False:
        result = result + "SP 부족"
        print(result)
        print("------------------------------------------------------------------")
        return result

    heal = character.decrease_cost(cost, _property) * 4

    character.decrease_action(action)
    character.update_location()

    if character.is_enemy():
        runtime.character.increase_enemy_hp(heal)

    elif character.is_player():
        runtime.character.increase_player_hp(heal)

    result = result + "[전원]에게 " + "[치유 " + str(heal) + "]"
    print(result)
    print("------------------------------------------------------------------")
    return result

#---------------------------------------------------------------------------------------
def protect(character, runtime):
    result = "[" + character.name + "]의 [가호]: "

    _cost = 5
    _action = 1
    _property = PROPERTY_SOLA

    if character.is_cost_enough(_cost, _property) == False:
        result = result + "SP 부족"
        print(result)
        print("------------------------------------------------------------------")
        return result

    _barrier = 20

    character.decrease_cost(_cost, _property)
    character.decrease_action(_action)
    character.update_location()

    _location = character.location
    _range = 3

    if character.is_enemy():
        runtime.character.increase_enemy_barrier_range(_barrier, _location, _range)

    elif character.is_player():
        runtime.character.increase_player_barrier_range(_barrier, _location, _range)

    result = result + "[영역]에게 " + "[보호 20]"
    print(result)
    print("------------------------------------------------------------------")
    return result

#---------------------------------------------------------------------------------------
def dim(character, runtime):
    result = "[" + character.name + "]의 [자비의 서광]: "

    _cost = 4
    _action = 1
    _property = PROPERTY_SOLA

    if character.is_cost_enough(_cost, _property) == False:
        result = result + "SP 부족"
        print(result)
        print("------------------------------------------------------------------")
        return result

    _barrier = 70

    character.decrease_cost(_cost, _property)
    character.decrease_action(_action)
    character.update_location()

    character.increase_barrier(_barrier)

    result = result + "자신에게 [보호 70]"
    print(result)
    print("------------------------------------------------------------------")
    return result

#---------------------------------------------------------------------------------------
def flash(character, target_location, runtime):
    result = "[" + character.name + "]의 [찰나의 섬광]: "

    _cost = COST_REMAIN
    _action = 1
    _property = PROPERTY_SOLA

    if character.is_cost_enough(_cost, _property) == False:
        result = result + "SP 부족"
        print(result)
        print("------------------------------------------------------------------")
        return result

    x = ord(target_location[0]) - ord('A')
    y = ord(target_location[1]) - ord('0')
    if (x < 0) or (x > 9) or (y < 0) or (y > 9):
        result = result + "잘못된 위치"
        print(result)
        print("------------------------------------------------------------------")
        return result

    if runtime.map.is_placed(target_location) == 0:
        result = result + "대상 없음"
        print(result)
        print("------------------------------------------------------------------")
        return result

    target_id = runtime.map.get_character_placed(target_location)
    target = runtime.character.get_character(target_id)

    location = character.location
    x_cur = ord(location[0]) - ord('A')
    y_cur = ord(location[1]) - ord('0')

    if ((x_cur != x) and (y_cur != y)):
        result = result + "직선 범위 바깥"
        print(result)
        print("------------------------------------------------------------------")
        return result

    if x_cur == x:
        if y_cur > y:
            for i in range(y + 1, y_cur):
                if runtime.map.cell[x][i].character_placed == 1:
                    result = result + "장애물 존재"
                    print(result)
                    print("------------------------------------------------------------------")
                    return result

            x_new = x
            y_new = y + 1

        elif y_cur < y:
            for i in range(y_cur + 1, y):
                if runtime.map.cell[x][i].character_placed == 1:
                    result = result + "장애물 존재"
                    print(result)
                    print("------------------------------------------------------------------")
                    return result

            x_new = x
            y_new = y - 1

    elif y_cur == y:
        if x_cur > x:
            for i in range(x + 1, x_cur):
                if runtime.map.cell[i][y].character_placed == 1:
                    result = result + "장애물 존재"
                    print(result)
                    print("------------------------------------------------------------------")
                    return result

            x_new = x + 1
            y_new = y

        elif x_cur < x:
            for i in range(x_cur + 1, x):
                if runtime.map.cell[i][y].character_placed == 1:
                    result = result + "장애물 존재"
                    print(result)
                    print("------------------------------------------------------------------")
                    return result

            x_new = x - 1
            y_new = y

    location_new = chr(x_new + ord('A')) + chr(y_new + ord('0'))

    runtime.map.remove_character(character)
    character.move(location_new)
    runtime.map.place_character(character.num, location_new)

    damage = character.decrease_cost(_cost, _property) * 10
    damage = character.get_damage(damage)

    character.decrease_action(_action)
    character.update_location()

    result = result + "[" + target.name + "]에게 " + "[피해 " + str(damage) + "]"

    target.decrease_hp(damage)
    target.update_location()

    print(result)
    print("------------------------------------------------------------------")
    return result

#---------------------------------------------------------------------------------------
def quatro(character, target_location, runtime):
    result = "[" + character.name + "]의 [세르피안테 콰트로]: "

    _cost = 3
    _action = 1
    _property = PROPERTY_ORBIT

    if character.is_cost_enough(_cost, _property) == False:
        result = result + "SP 부족"
        print(result)
        print("------------------------------------------------------------------")
        return result

    x = ord(target_location[0]) - ord('A')
    y = ord(target_location[1]) - ord('0')
    if (x < 0) or (x > 9) or (y < 0) or (y > 9):
        result = result + "잘못된 위치"
        print(result)
        print("------------------------------------------------------------------")
        return result

    if runtime.map.is_placed(target_location) == 0:
        result = result + "대상 없음"
        print(result)
        print("------------------------------------------------------------------")
        return result

    target_dist = get_dist(character.location, target_location)
    if target_dist > 1:
        result = result + "사거리 바깥"
        print(result)
        print("------------------------------------------------------------------")
        return result

    damage = character.get_damage(100)

    character.decrease_cost(_cost, _property)
    character.decrease_action(_action)
    character.update_location()

    target_id = runtime.map.get_character_placed(target_location)
    target = runtime.character.get_character(target_id)
    result = result + "[" + target.name + "]에게 " + "[피해 " + str(damage) + "]"

    target.decrease_hp(damage)
    target.update_location()

    print(result)
    print("------------------------------------------------------------------")
    return result

#---------------------------------------------------------------------------------------
def raven(character, target_location, runtime):
    result = "[" + character.name + "]의 [레이븐 나인]: "

    _cost = 4
    _action = 1
    _property = PROPERTY_ORBIT

    if character.is_cost_enough(_cost, _property) == False:
        result = result + "SP 부족"
        print(result)
        print("------------------------------------------------------------------")
        return result

    x = ord(target_location[0]) - ord('A')
    y = ord(target_location[1]) - ord('0')
    if (x < 0) or (x > 9) or (y < 0) or (y > 9):
        result = result + "잘못된 위치"
        print(result)
        print("------------------------------------------------------------------")
        return result

    if runtime.map.is_placed(target_location) == 0:
        result = result + "대상 없음"
        print(result)
        print("------------------------------------------------------------------")
        return result

    target_dist = get_dist(character.location, target_location)
    if target_dist > 3:
        result = result + "사거리 바깥"
        print(result)
        print("------------------------------------------------------------------")
        return result

    damage = character.get_damage(60)

    character.decrease_cost(_cost, _property)
    character.decrease_action(_action)
    character.update_location()

    target_id = runtime.map.get_character_placed(target_location)
    target = runtime.character.get_character(target_id)

    result = result + "[" + target.name + "]에게 " + "[피해 " + str(damage) + "]"
    result = result + "[독 6]"

    target.decrease_hp(damage)
    target.increase_poison(6)
    target.update_location()

    print(result)
    print("------------------------------------------------------------------")
    return result

#---------------------------------------------------------------------------------------
def stardust(character, target_location, runtime):
    result = "[" + character.name + "]의 [스타더스트 폴]: "

    _cost = 4
    _action = 1
    _property = PROPERTY_ORBIT

    if character.is_cost_enough(_cost, _property) == False:
        result = result + "SP 부족"
        print(result)
        print("------------------------------------------------------------------")
        return result

    x = ord(target_location[0]) - ord('A')
    y = ord(target_location[1]) - ord('0')
    if (x < 0) or (x > 9) or (y < 0) or (y > 9):
        result = result + "잘못된 위치"
        print(result)
        print("------------------------------------------------------------------")
        return result

    target_dist = get_dist(character.location, target_location)
    if target_dist > 3:
        result = result + "사거리 바깥"
        print(result)
        print("------------------------------------------------------------------")
        return result

    _damage = character.get_damage(40)

    character.decrease_cost(_cost, _property)
    character.decrease_action(_action)
    character.update_location()

    _range = 3

    if character.is_enemy():
        runtime.character.decrease_player_hp_range(_damage, target_location, _range)

    elif character.is_player():
        runtime.character.decrease_enemy_hp_range(_damage, target_location, _range)


    result = result + "[영역]에게 " + "[피해 " + str(_damage) + "]"
    print(result)
    print("------------------------------------------------------------------")
    return result

#---------------------------------------------------------------------------------------
def dusk(character, target_location, runtime):
    result = "[" + character.name + "]의 [여명을 거두는 빛]: "

    _cost = 4
    _action = 1
    _property = PROPERTY_SOLA

    if character.is_cost_enough(_cost, _property) == False:
        result = result + "SP 부족"
        print(result)
        print("------------------------------------------------------------------")
        return result

    x = ord(target_location[0]) - ord('A')
    y = ord(target_location[1]) - ord('0')
    if (x < 0) or (x > 9) or (y < 0) or (y > 9):
        result = result + "잘못된 위치"
        print(result)
        print("------------------------------------------------------------------")
        return result

    if runtime.map.is_placed(target_location) == 0:
        result = result + "대상 없음"
        print(result)
        print("------------------------------------------------------------------")
        return result

    target_dist = get_dist(character.location, target_location)
    if target_dist > 3:
        result = result + "사거리 바깥"
        print(result)
        print("------------------------------------------------------------------")
        return result

    target_id = runtime.map.get_character_placed(target_location)
    target = runtime.character.get_character(target_id)
    if target.is_opposit(character):
        result = result + "잘못된 대상"
        print(result)
        print("------------------------------------------------------------------")
        return result

    character.decrease_cost(_cost, _property)
    character.decrease_action(_action)
    character.update_location()

    result = result + "[" + target.name + "]을 [방어]"

    target.set_knight(character)
    target.update_location()

    print(result)
    print("------------------------------------------------------------------")
    return result

#---------------------------------------------------------------------------------------
def define(character, target_location, runtime):
    result = "[" + character.name + "]의 [허의 존재 증명]: "

    _cost = 2
    _action = 1
    _property = PROPERTY_VOID

    if character.is_cost_enough(_cost, _property) == False:
        result = result + "SP 부족"
        print(result)
        print("------------------------------------------------------------------")
        return result

    x = ord(target_location[0]) - ord('A')
    y = ord(target_location[1]) - ord('0')
    if (x < 0) or (x > 9) or (y < 0) or (y > 9):
        result = result + "잘못된 위치"
        print(result)
        print("------------------------------------------------------------------")
        return result

    if runtime.map.is_placed(target_location) == 0:
        result = result + "대상 없음"
        print(result)
        print("------------------------------------------------------------------")
        return result

    target_dist = get_dist(character.location, target_location)
    if target_dist > 3:
        result = result + "사거리 바깥"
        print(result)
        print("------------------------------------------------------------------")
        return result

    _damage = character.get_damage(20)
    _weaken = 2

    character.decrease_cost(_cost, _property)
    character.decrease_action(_action)
    character.update_location()

    target_id = runtime.map.get_character_placed(target_location)
    target = runtime.character.get_character(target_id)

    result = result + "[" + target.name + "]에게 "
    result = result + "[피해 " + str(_damage) + "]"
    result = result + "[약화 " + str(_weaken) + "]"

    target.decrease_hp(_damage)
    target.increase_weaken(_weaken)
    target.update_location()

    print(result)
    print("------------------------------------------------------------------")
    return result

#---------------------------------------------------------------------------------------
def evade(character, target_location, runtime):
    result = "[" + character.name + "]의 [모순 논파]: "

    _cost = 4
    _action = 1
    _property = PROPERTY_VOID

    if character.is_cost_enough(_cost, _property) == False:
        result = result + "SP 부족"
        print(result)
        print("------------------------------------------------------------------")
        return result

    x = ord(target_location[0]) - ord('A')
    y = ord(target_location[1]) - ord('0')
    if (x < 0) or (x > 9) or (y < 0) or (y > 9):
        result = result + "잘못된 위치"
        print(result)
        print("------------------------------------------------------------------")
        return result

    if runtime.map.is_placed(target_location) == 0:
        result = result + "대상 없음"
        print(result)
        print("------------------------------------------------------------------")
        return result

    target_id = runtime.map.get_character_placed(target_location)
    target = runtime.character.get_character(target_id)
    if target.is_ally(character):
        result = result + "잘못된 대상"
        print(result)
        print("------------------------------------------------------------------")
        return result

    character.decrease_cost(_cost, _property)
    character.decrease_action(_action)
    character.update_location()

    result = result + "[" + target.name + "]에게 " + "[다음 피해 전가]"

    character.set_evade(target)
    target.update_location()

    print(result)
    print("------------------------------------------------------------------")
    return result

#---------------------------------------------------------------------------------------
def swap(character, target_location, runtime):
    result = "[" + character.name + "]의 [역설의 시작]: "

    _cost = 5
    _action = 1
    _property = PROPERTY_VOID

    if character.is_cost_enough(_cost, _property) == False:
        result = result + "SP 부족"
        print(result)
        print("------------------------------------------------------------------")
        return result

    x = ord(target_location[0]) - ord('A')
    y = ord(target_location[1]) - ord('0')
    if (x < 0) or (x > 9) or (y < 0) or (y > 9):
        result = result + "잘못된 위치"
        print(result)
        print("------------------------------------------------------------------")
        return result

    if runtime.map.is_placed(target_location) == 0:
        result = result + "대상 없음"
        print(result)
        print("------------------------------------------------------------------")
        return result

    target_id = runtime.map.get_character_placed(target_location)
    target = runtime.character.get_character(target_id)
    if target.is_opposit(character):
        result = result + "잘못된 대상"
        print(result)
        print("------------------------------------------------------------------")
        return result

    character.decrease_cost(_cost, _property)
    character.decrease_action(_action)

    location = character.location

    # remove character & target
    runtime.map.remove_character(character)
    runtime.map.remove_character(target)

    # move character & target
    character.move(target_location)
    target.move(location)

    result = result + "[" + target.name + "]과 " + "[위치 교환]"

    # place character & target
    runtime.map.place_character(character.num, target_location)
    runtime.map.place_character(target.num, location)

    character.update_location()
    target.update_location()

    print(result)
    print("------------------------------------------------------------------")
    return result

#---------------------------------------------------------------------------------------
def save(character, runtime):
    result = "[" + character.name + "]의 [바니타스 베리타스]: "

    _cost = COST_REMAIN
    _action = 1
    _property = PROPERTY_VOID

    if character.is_cost_enough(_cost, _property) == False:
        result = result + "SP 부족"
        print(result)
        print("------------------------------------------------------------------")
        return result

    if character.save == 2:
        result = result + "소진됨"
        print(result)
        print("------------------------------------------------------------------")
        return result

    elif character.save == 1:
        print("save:", character.name, ": load status:",
              "hp:", character.hp, "->", character.hp_save,
              "sp:", character.sp, "->", character.sp_save,
              "mp:", character.sp, "->", character.mp_save,
              "location:", character.location, "->", character.location_save)

        result = result + "[복원]"

        character.hp = character.hp_save
        character.sp = character.sp_save
        character.mp = character.mp_save
        character.location = character.location_save

        character.action = character.action - 1
        character.update_location()

        character.hp_save = 0
        character.sp_save = 0
        character.mp_save = 0
        character.location_save = ''
        character.save = 2

        print(result)
        print("------------------------------------------------------------------")
        return result

    result = result + "[기록]"

    character.hp_save = character.hp
    character.sp_save = character.sp
    character.mp_save = character.mp
    character.location_save = character.location
    character.save = 1

    character.decrease_cost(_cost, _property)
    character.decrease_action(_action)
    character.update_location()

    print(result)
    print("------------------------------------------------------------------")
    return result

#---------------------------------------------------------------------------------------
def finale(character, target_location, runtime):
    result = "[" + character.name + "]의 [스타라이트 피날레]: "

    _cost = COST_MAX_MP
    _action = 1
    _property = PROPERTY_POEM

    if character.is_cost_enough(_cost, _property) == False:
        result = result + "SP 부족"
        print(result)
        print("------------------------------------------------------------------")
        return result

    x = ord(target_location[0]) - ord('A')
    y = ord(target_location[1]) - ord('0')
    if (x < 0) or (x > 9) or (y < 0) or (y > 9):
        result = result + "잘못된 위치"
        print(result)
        print("------------------------------------------------------------------")
        return result

    if runtime.map.is_placed(target_location) == 1:
        result = result + "잘못된 위치"
        print(result)
        print("------------------------------------------------------------------")
        return result

    if character.is_ultimate_usable == False:
        result = result + "소진됨"
        print(result)
        print("------------------------------------------------------------------")
        return result

    character.decrease_ultimate()

    character.decrease_cost(_cost, _property)
    character.decrease_action(_action)
    character.update_location()

    result = result + "성공. [위치 "+ target_location + "]"

    print(result)
    print("------------------------------------------------------------------")
    return result

#---------------------------------------------------------------------------------------
def sola(character, runtime):
    result = "[" + character.name + "]의 [솔라 디비니티]: "

    _cost = COST_MAX_MP
    _action = 1
    _property = PROPERTY_SOLA

    if character.is_cost_enough(_cost, _property) == False:
        result = result + "SP 부족"
        print(result)
        print("------------------------------------------------------------------")
        return result

    if character.is_ultimate_usable == False:
        result = result + "소진됨"
        print(result)
        print("------------------------------------------------------------------")
        return result

    character.decrease_ultimate()

    character.invincible = 1

    character.decrease_cost(_cost, _property)
    character.decrease_action(_action)
    character.update_location()

    result = result + "자신에게 [불멸]"

    print(result)
    print("------------------------------------------------------------------")
    return result

#---------------------------------------------------------------------------------------
def badmagic(character, target_location, runtime):
    result = "[" + character.name + "]의 [최흉의 마법]: "

    _cost = COST_MAX_MP
    _action = 1
    _property = PROPERTY_ORBIT

    if character.is_cost_enough(_cost, _property) == False:
        result = result + "SP 부족"
        print(result)
        print("------------------------------------------------------------------")
        return result

    if character.is_ultimate_usable == False:
        result = result + "소진됨"
        print(result)
        print("------------------------------------------------------------------")
        return result

    x = ord(target_location[0]) - ord('A')
    y = ord(target_location[1]) - ord('0')
    if (x < 0) or (x > 9) or (y < 0) or (y > 9):
        result = result + "잘못된 위치"
        print(result)
        print("------------------------------------------------------------------")
        return result

    if runtime.map.is_placed(target_location) == 0:
        result = result + "대상 없음"
        print(result)
        print("------------------------------------------------------------------")
        return result

    _damage = character.get_damage(333)

    character.decrease_ultimate()

    character.decrease_cost(_cost, _property)
    character.decrease_action(_action)
    character.update_location()

    target_id = runtime.map.get_character_placed(target_location)
    target = runtime.character.get_character(target_id)

    result = result + "[" + target.name + "]에게 " + "[피해 " + str(_damage) + "]"

    target.decrease_hp(_damage)
    target.update_location()

    print(result)
    print("------------------------------------------------------------------")
    return result

#---------------------------------------------------------------------------------------
def makeidiot(character, target_location, runtime):
    result = "[" + character.name + "]의 [종언선고의 최종증언]: "

    _cost = COST_MAX_MP
    _action = 1
    _property = PROPERTY_VOID

    if character.is_cost_enough(_cost, _property) == False:
        result = result + "SP 부족"
        print(result)
        print("------------------------------------------------------------------")
        return result

    if character.is_ultimate_usable == False:
        result = result + "소진됨"
        print(result)
        print("------------------------------------------------------------------")
        return result

    x = ord(target_location[0]) - ord('A')
    y = ord(target_location[1]) - ord('0')
    if (x < 0) or (x > 9) or (y < 0) or (y > 9):
        result = result + "잘못된 위치"
        print(result)
        print("------------------------------------------------------------------")
        return result

    if runtime.map.is_placed(target_location) == 0:
        result = result + "대상 없음"
        print(result)
        print("------------------------------------------------------------------")
        return result

    character.decrease_ultimate()

    character.decrease_cost(_cost, _property)
    character.decrease_action(_action)
    character.update_location()

    target_id = runtime.map.get_character_placed(target_location)
    target = runtime.character.get_character(target_id)
    target.update_location()

    result = result + "[" + target.name + "]에게 [선언]"

    print(result)
    print("------------------------------------------------------------------")
    return result

#---------------------------------------------------------------------------------------
def swip_up(character, runtime):
    result = "[" + character.name + "]의 [꼬리 휩쓸기]: "

    character.action = character.action - 1
    character.update_location()

    damage = 20

    for x_new in range(0,10):
        for y_new in range(0,5):
            cell = runtime.map.cell[x_new][y_new]
            if cell.character_placed == 1:
                if cell.character_num == character.num:
                    continue

                new_target = runtime.character.character[cell.character_num]
                new_target.decrease_hp(damage)
                new_target.update_location()

    result = result + "[영역]에게 " + "[피해 " + str(damage) + "]"
    print(result)
    print("------------------------------------------------------------------")
    return result

#---------------------------------------------------------------------------------------
def swip_down(character, runtime):
    result = "[" + character.name + "]의 [머리 휩쓸기]: "

    character.action = character.action - 1
    character.update_location()

    damage = 20

    for x_new in range(0,10):
        for y_new in range(5,10):
            cell = runtime.map.cell[x_new][y_new]
            if cell.character_placed == 1:
                if cell.character_num == character.num:
                    continue

                new_target = runtime.character.character[cell.character_num]
                new_target.decrease_hp(damage)
                new_target.update_location()

    result = result + "[영역]에게 " + "[피해 " + str(damage) + "]"
    print(result)
    print("------------------------------------------------------------------")
    return result

#---------------------------------------------------------------------------------------
def explode(character, runtime):
    location = character.location
    x = ord(location[0]) - ord('A')
    y = ord(location[1]) - ord('0')

    if character.name == '아가레스':
        _damage = 50
        _broken = 2
        _range = 2

        runtime.character.decrease_player_hp_range(_damage, location, _range)
        runtime.character.increase_player_broken_range(_broken, location, _range)

        result = "[아가레스]의 [폭발]: "
        result = result + "[영역]에게 " + "[피해 50][무너짐 2]"

    elif character.name == '비프론스':
        _damage = 50
        _weaken = 1

        runtime.character.decrease_player_hp(_damage)
        runtime.character.increase_player_weaken(_weaken)

        result = "[비프론스]의 [폭발]: "
        result = result + "[전원]에게 " + "[피해 50][약화 1]"

    elif character.name == '안티키테라':
        _damage = 50
        _weaken = 2

        runtime.character.decrease_player_hp(_damage)
        runtime.character.increase_player_weaken(_weaken)

        result = "[안티키테라 메커니즘]: "
        result = result + "[전원]에게 " + "[피해 50][약화 2]"

    runtime.map.remove_character(character)
    character.remove()

    print(result)
    print("------------------------------------------------------------------")
    return result

#---------------------------------------------------------------------------------------
def crystal_fall(character, target_location, runtime):
    result = "[" + character.name + "]의 [결정 낙하]: "

    x = ord(target_location[0]) - ord('A')
    y = ord(target_location[1]) - ord('0')
    if (x < 0) or (x > 9) or (y < 0) or (y > 9):
        result = result + "잘못된 위치"
        print(result)
        print("------------------------------------------------------------------")
        return result

    for x_new in range(0,10):
        for y_new in range(0,10):
            new_dist = abs(x - x_new) + abs(y - y_new)
            if new_dist <= 2:
                cell = runtime.map.cell[x_new][y_new]
                if cell.character_placed == 1:
                    if cell.character_num == character.num:
                        continue

                    new_target = runtime.character.character[cell.character_num]
                    if new_target.type == character.type:
                        continue

                    new_target.decrease_hp(15)
                    new_target.update_location()

    result = result + "[영역]에게 " + "[피해 15]"
    print(result)
    print("------------------------------------------------------------------")
    return result

#---------------------------------------------------------------------------------------
def poison_bite(character, target_location, runtime):
    result = "[" + character.name + "]의 [독니]: "

    damage = 30

    x = ord(target_location[0]) - ord('A')
    y = ord(target_location[1]) - ord('0')
    if (x < 0) or (x > 9) or (y < 0) or (y > 9):
        result = result + "잘못된 위치"
        print(result)
        print("------------------------------------------------------------------")
        return result

    if runtime.map.is_placed(target_location) == 0:
        result = result + "대상 없음"
        print(result)
        print("------------------------------------------------------------------")
        return result

    target_id = runtime.map.get_character_placed(target_location)
    target = runtime.character.get_character(target_id)
    result = result + "[" + target.name + "]에게 " + "[피해 " + str(damage) + "]"
    result = result + "[독 6]"

    target.decrease_hp(damage)
    target.increase_poison(6)
    target.update_location()

    print(result)
    print("------------------------------------------------------------------")
    return result

#---------------------------------------------------------------------------------------
def lift_wall(character, target_location, runtime):
    result = "[" + character.name + "]의 [흑점]: "

    _cost = 4
    _action = 1
    _property = PROPERTY_SOLA

    if character.is_cost_enough(_cost, _property) == False:
        result = result + "SP 부족"
        print(result)
        print("------------------------------------------------------------------")
        return result

    x = ord(target_location[0]) - ord('A')
    y = ord(target_location[1]) - ord('0')
    if (x < 0) or (x > 9) or (y < 0) or (y > 9):
        result = result + "잘못된 위치"
        print(result)
        print("------------------------------------------------------------------")
        return result

    if runtime.map.is_placed(target_location):
        result = result + "대상 존재"
        print(result)
        print("------------------------------------------------------------------")
        return result

    wall_data = data.get_enemy(40)
    wall = runtime.character.get_empty_enemy()
    if wall == 0:
        result = result + "벽 슬롯 부족"
        print(result)
        print("------------------------------------------------------------------")
        return result

    elif wall.add(target_location, wall_data, 0) == 0:
        result = result + "벽 추가 실패"
        print(result)
        print("------------------------------------------------------------------")
        return result

    character.decrease_cost(_cost, _property)
    character.decrease_action(_action)
    character.update_location()

    _damage = character.get_damage(40)
    _range = 1

    runtime.character.decrease_player_hp_range(_damage, target_location, _range)

    result = result + "[영역]에게 " + "[피해 " + str(_damage) + "]"
    result = result + "[벽 생성]"
    print(result)
    print("------------------------------------------------------------------")
    return result

#---------------------------------------------------------------------------------------
def flash_2(character, target_location, runtime):
    result = "[" + character.name + "]의 [크샤나]: "

    _cost = 4
    _action = 1
    _property = PROPERTY_SOLA

    if character.is_cost_enough(_cost, _property) == False:
        result = result + "SP 부족"
        print(result)
        print("------------------------------------------------------------------")
        return result

    x = ord(target_location[0]) - ord('A')
    y = ord(target_location[1]) - ord('0')
    if (x < 0) or (x > 9) or (y < 0) or (y > 9):
        result = result + "잘못된 위치"
        print(result)
        print("------------------------------------------------------------------")
        return result

    if runtime.map.is_placed(target_location) == 0:
        result = result + "대상 없음"
        print(result)
        print("------------------------------------------------------------------")
        return result

    target_id = runtime.map.get_character_placed(target_location)
    target = runtime.character.get_character(target_id)

    location = character.location
    x_cur = ord(location[0]) - ord('A')
    y_cur = ord(location[1]) - ord('0')

    if ((x_cur != x) and (y_cur != y)):
        result = result + "직선 범위 바깥"
        print(result)
        print("------------------------------------------------------------------")
        return result

    if x_cur == x:
        if y_cur > y:
            for i in range(y + 1, y_cur):
                if runtime.map.cell[x][i].character_placed == 1:
                    result = result + "장애물 존재"
                    print(result)
                    print("------------------------------------------------------------------")
                    return result

            x_new = x
            y_new = y + 1

        elif y_cur < y:
            for i in range(y_cur + 1, y):
                if runtime.map.cell[x][i].character_placed == 1:
                    result = result + "장애물 존재"
                    print(result)
                    print("------------------------------------------------------------------")
                    return result

            x_new = x
            y_new = y - 1

    elif y_cur == y:
        if x_cur > x:
            for i in range(x + 1, x_cur):
                if runtime.map.cell[i][y].character_placed == 1:
                    result = result + "장애물 존재"
                    print(result)
                    print("------------------------------------------------------------------")
                    return result

            x_new = x + 1
            y_new = y

        elif x_cur < x:
            for i in range(x_cur + 1, x):
                if runtime.map.cell[i][y].character_placed == 1:
                    result = result + "장애물 존재"
                    print(result)
                    print("------------------------------------------------------------------")
                    return result

            x_new = x - 1
            y_new = y

    location_new = chr(x_new + ord('A')) + chr(y_new + ord('0'))

    runtime.map.remove_character(character)
    character.move(location_new)
    runtime.map.place_character(character.num, location_new)

    character.decrease_cost(_cost, _property)
    character.decrease_action(_action)
    character.update_location()

    _damage = character.get_damage(60)

    result = result + "[" + target.name + "]에게 " + "[피해 " + str(_damage) + "]"

    target.decrease_hp(_damage)
    target.update_location()

    print(result)
    print("------------------------------------------------------------------")
    return result

#---------------------------------------------------------------------------------------
def knockback(character, target_location, runtime):
    result = "[" + character.name + "]의 [플레어]: "

    _cost = 4
    _action = 1
    _property = PROPERTY_SOLA

    if character.is_cost_enough(_cost, _property) == False:
        result = result + "SP 부족"
        print(result)
        print("------------------------------------------------------------------")
        return result

    x = ord(target_location[0]) - ord('A')
    y = ord(target_location[1]) - ord('0')
    if (x < 0) or (x > 9) or (y < 0) or (y > 9):
        result = result + "잘못된 위치"
        print(result)
        print("------------------------------------------------------------------")
        return result

    if runtime.map.is_placed(target_location) == 0:
        result = result + "대상 없음"
        print(result)
        print("------------------------------------------------------------------")
        return result

    target_dist = get_dist(character.location, target_location)
    if target_dist != 1:
        result = result + "사거리 바깥"
        print(result)
        print("------------------------------------------------------------------")
        return result

    _damage = character.get_damage(60)

    character.decrease_cost(_cost, _property)
    character.decrease_action(_action)
    character.update_location()

    location = character.location
    x_cur = ord(location[0]) - ord('A')
    y_cur = ord(location[1]) - ord('0')

    x_new = x
    y_new = y

    # up
    if x_cur == x and y_cur == y + 1:
        while y_new > 0:
            if runtime.map.cell[x_new][y_new - 1].character_placed == 1:
                break
            y_new = y_new - 1

    # down
    elif x_cur == x and y_cur == y - 1:
        while y_new < 9:
            if runtime.map.cell[x_new][y_new + 1].character_placed == 1:
                break
            y_new = y_new + 1

    # left
    elif x_cur == x + 1 and y_cur == y:
        while x_new > 0:
            if runtime.map.cell[x_new - 1][y_new].character_placed == 1:
                break
            x_new = x_new - 1

    # left
    elif x_cur == x - 1 and y_cur == y:
        while x_new < 9:
            if runtime.map.cell[x_new + 1][y_new].character_placed == 1:
                break
            x_new = x_new + 1

    location_new = chr(x_new + ord('A')) + chr(y_new + ord('0'))

    target_id = runtime.map.get_character_placed(target_location)
    target = runtime.character.get_character(target_id)
    result = result + "[" + target.name + "]에게 " + "[피해 " + str(_damage) + "][밀치기]"

    runtime.map.remove_character(target)
    target.move(location_new)
    runtime.map.place_character(target.num, location_new)

    target.decrease_hp(_damage)
    target.update_location()

    print(result)
    print("------------------------------------------------------------------")
    return result

#---------------------------------------------------------------------------------------
def breakdown(character, runtime):
    result = "[" + character.name + "]의 [프로미넌스]: "

    _cost = 4
    _action = 1
    _property = PROPERTY_SOLA

    if character.is_cost_enough(_cost, _property) == False:
        result = result + "SP 부족"
        print(result)
        print("------------------------------------------------------------------")
        return result

    _damage = character.get_damage(40)
    _broken = 1

    character.decrease_cost(_cost, _property)
    character.decrease_action(_action)
    character.update_location()

    _location = character.location
    _range = 2

    runtime.character.decrease_player_hp_range(_damage, _location, _range)
    runtime.character.increase_player_broken_range(_broken, _location, _range)

    result = result + "[주위]에게 " + "[피해 " + str(_damage) + "][무너짐 1]"
    print(result)
    print("------------------------------------------------------------------")
    return result

#---------------------------------------------------------------------------------------
def attack_call(character, target_location, runtime):
    #result = "[" + character.name + "]의 [오리아스 콜]: "
    result = "[" + character.name + "]의 [바알베크 헬리오폴리스]: "

    _damage = 100

    x = ord(target_location[0]) - ord('A')
    y = ord(target_location[1]) - ord('0')
    if (x < 0) or (x > 9) or (y < 0) or (y > 9):
        result = result + "잘못된 위치"
        print(result)
        print("------------------------------------------------------------------")
        return result

    if runtime.map.is_placed(target_location) == 0:
        result = result + "대상 없음"
        print(result)
        print("------------------------------------------------------------------")
        return result

    target_id = runtime.map.get_character_placed(target_location)
    target = runtime.character.get_character(target_id)
    result = result + "[" + target.name + "]에게 " + "[피해 " + str(_damage) + "]"

    target.decrease_hp(_damage)
    target.update_location()

    print(result)
    print("------------------------------------------------------------------")
    return result

#---------------------------------------------------------------------------------------
def punch_vertical(character, runtime):
    #result = "[" + character.name + "]의 [엘리고스 레이]: "
    result = "[" + character.name + "]의 [네브라스카이 디스크]: "
    print(result)

    _damage = 60
    #_broken = 1
    _broken = 2

    location = character.location

    x = ord(location[0]) - ord('A')
    y = ord(location[1]) - ord('0')

    if x != 0:
        x_new = x - 1
        for y_new in range(0,10):
            cell = runtime.map.cell[x_new][y_new]
            if cell.character_placed == 0:
                continue

            target = runtime.character.character[cell.character_num]
            if target.is_player() == False:
                continue

            target.decrease_hp(_damage)
            target.broken = target.broken + _broken
            target.update_location()

    x_new = x
    for y_new in range(0,10):
        cell = runtime.map.cell[x_new][y_new]
        if cell.character_placed == 0:
            continue

        target = runtime.character.character[cell.character_num]
        if target.is_player() == False:
            continue

        target.decrease_hp(_damage)
        target.broken = target.broken + _broken
        target.update_location()

    if x != 9:
        x_new = x + 1
        for y_new in range(0,10):
            cell = runtime.map.cell[x_new][y_new]
            if cell.character_placed == 0:
                continue

            target = runtime.character.character[cell.character_num]
            if target.is_player() == False:
                continue

            target.decrease_hp(_damage)
            target.broken = target.broken + _broken
            target.update_location()

    runtime.map.remove_character(character)
    character.remove()

    result = result + "[영역]에게 " + "[피해 60][무너짐 2]"
    print(result)
    print("------------------------------------------------------------------")
    return result

#---------------------------------------------------------------------------------------
def punch_horizon(character, runtime):
    #result = "[" + character.name + "]의 [엘리고스 레이]: "
    result = "[" + character.name + "]의 [네브라스카이 디스크]: "
    print(result)

    _damage = 60
    #_broken = 1
    _broken = 2

    location = character.location

    x = ord(location[0]) - ord('A')
    y = ord(location[1]) - ord('0')

    if y != 0:
        y_new = y - 1
        for x_new in range(0,10):
            cell = runtime.map.cell[x_new][y_new]
            if cell.character_placed == 0:
                continue

            target = runtime.character.character[cell.character_num]
            if target.is_player() == False:
                continue

            target.decrease_hp(_damage)
            target.broken = target.broken + _broken
            target.update_location()

    y_new = y
    for x_new in range(0,10):
        cell = runtime.map.cell[x_new][y_new]
        if cell.character_placed == 0:
            continue

        target = runtime.character.character[cell.character_num]
        if target.is_player() == False:
            continue

        target.decrease_hp(_damage)
        target.broken = target.broken + _broken
        target.update_location()

    if y != 9:
        y_new = y + 1
        for x_new in range(0,10):
            cell = runtime.map.cell[x_new][y_new]
            if cell.character_placed == 0:
                continue

            target = runtime.character.character[cell.character_num]
            if target.is_player() == False:
                continue

            target.decrease_hp(_damage)
            target.broken = target.broken + _broken
            target.update_location()

    runtime.map.remove_character(character)
    character.remove()

    result = result + "[영역]에게 " + "[피해 60][무너짐 2]"
    print(result)
    print("------------------------------------------------------------------")
    return result

#---------------------------------------------------------------------------------------
def rage(character, runtime):
    result = "[" + character.name + "]의 [마르바스 레이지]: "

    _damage = 40

    runtime.character.decrease_player_hp(_damage)

    result = result + "[영역]에게 " + "[피해 40]"
    print(result)
    print("------------------------------------------------------------------")
    return result

#---------------------------------------------------------------------------------------
def knockback_all(character, direction, runtime):
    #result = "[" + character.name + "]의 [솔라 윈드]: "
    result = "[" + character.name + "]의 [파에스토스 디스크]: "

    _cost = 4
    _action = 1
    _property = PROPERTY_SOLA
    #_damage = 20
    _damage = 40

    if character.is_cost_enough(_cost, _property) == False:
        result = result + "SP 부족"
        print(result)
        print("------------------------------------------------------------------")
        return result

    for __ in range (0, 12):
        if direction == 'UP':
            for target in runtime.character.character:
                if not target.is_added() or not target.is_player():
                    continue

                x = ord(target.location[0]) - ord('A')
                y = ord(target.location[1]) - ord('0')

                while y > 0:
                    if runtime.map.cell[x][y - 1].character_placed == 1:
                        break
                    y = y - 1

                location_new = chr(x + ord('A')) + chr(y + ord('0'))

                runtime.map.remove_character(target)
                target.move(location_new)
                runtime.map.place_character(target.num, location_new)

                target.update_location()

        elif direction == 'DOWN':
            for target in runtime.character.character:
                if not target.is_added() or not target.is_player():
                    continue

                x = ord(target.location[0]) - ord('A')
                y = ord(target.location[1]) - ord('0')

                while y < 9:
                    if runtime.map.cell[x][y + 1].character_placed == 1:
                        break
                    y = y + 1

                location_new = chr(x + ord('A')) + chr(y + ord('0'))

                runtime.map.remove_character(target)
                target.move(location_new)
                runtime.map.place_character(target.num, location_new)

                target.update_location()

        elif direction == 'LEFT':
            for target in runtime.character.character:
                if not target.is_added() or not target.is_player():
                    continue

                x = ord(target.location[0]) - ord('A')
                y = ord(target.location[1]) - ord('0')

                while x > 0:
                    if runtime.map.cell[x - 1][y].character_placed == 1:
                        break
                    x = x - 1

                location_new = chr(x + ord('A')) + chr(y + ord('0'))

                runtime.map.remove_character(target)
                target.move(location_new)
                runtime.map.place_character(target.num, location_new)

                target.update_location()

        elif direction == 'RIGHT':
            for target in runtime.character.character:
                if not target.is_added() or not target.is_player():
                    continue

                x = ord(target.location[0]) - ord('A')
                y = ord(target.location[1]) - ord('0')

                while x < 9:
                    if runtime.map.cell[x + 1][y].character_placed == 1:
                        break
                    x = x + 1

                location_new = chr(x + ord('A')) + chr(y + ord('0'))

                runtime.map.remove_character(target)
                target.move(location_new)
                runtime.map.place_character(target.num, location_new)

                target.update_location()

        else:
            result = result + "잘못된 방향:"
            print(result, direction)
            print("------------------------------------------------------------------")
            return result

    character.decrease_cost(_cost, _property)
    character.decrease_action(_action)
    character.update_location()

    damage = character.get_damage(_damage)
    runtime.character.decrease_player_hp(_damage)

    result = result + "[전원]에게 " + "[피해 " + str(_damage) + "][밀치기]"
    print(result)
    print("------------------------------------------------------------------")
    return result

#---------------------------------------------------------------------------------------
def share(character, target_location, runtime):
    #result = "[" + character.name + "]의 [카타스트로피]: "
    result = "[" + character.name + "]의 [나즈카 지오글리프]: "

    _cost = 10
    _action = 1
    _property = PROPERTY_SOLA

    if character.is_cost_enough(_cost, _property) == False:
        result = result + "SP 부족"
        print(result)
        print("------------------------------------------------------------------")
        return result

    x = ord(target_location[0]) - ord('A')
    y = ord(target_location[1]) - ord('0')
    if (x < 0) or (x > 9) or (y < 0) or (y > 9):
        result = result + "잘못된 위치"
        print(result)
        print("------------------------------------------------------------------")
        return result

    _damage = character.get_damage(300)

    character.decrease_cost(_cost, _property)
    character.decrease_action(_action)
    character.update_location()

    _range = 2
    runtime.character.decrease_player_hp_range_share(_damage, target_location, _range)

    result = result + "[영역]에게 " + "[분산 피해 " + str(_damage) + "]"
    print(result)
    print("------------------------------------------------------------------")
    return result

#---------------------------------------------------------------------------------------
def run_move(character, direction, runtime):
    #result = "[" + character.name + "]의 [이동]: "
    result = "[이동]: "

    # new location check
    location = character.location

    if direction == 'up':
        x = ord(location[0]) - ord('A')
        y = ord(location[1]) - ord('0') - 1
        location_new = location[0] + chr(y + ord('0'))

    elif direction == 'down':
        x = ord(location[0]) - ord('A')
        y = ord(location[1]) - ord('0') + 1
        location_new = location[0] + chr(y + ord('0'))

    elif direction == 'left':
        x = ord(location[0]) - ord('A') - 1
        y = ord(location[1]) - ord('0')
        location_new = chr(x + ord('A')) + location[1]

    elif direction == 'right':
        x = ord(location[0]) - ord('A') + 1
        y = ord(location[1]) - ord('0')
        location_new = chr(x + ord('A')) + location[1]

    else:
        result = result + "잘못된 방향"
        print(result)
        print("------------------------------------------------------------------")
        return result

    if (x < 0) or (x > 9) or (y < 0) or (y > 9):
        result = result + "잘못된 위치"
        print(result)
        print("------------------------------------------------------------------")
        return result

    if runtime.map.cell[x][y].character_placed == 1:
        result = result + "충돌"
        print(result)
        print("------------------------------------------------------------------")
        return result

    # distance check
    location_dist = get_dist(location_new, character.location_prev)
    #print("location_dist:", location_dist, character.location_prev, "->", location_new)

    if location_dist > character.sp_prev:
        result = result + "SP 부족"
        print(result)
        print("------------------------------------------------------------------")
        return result

    runtime.map.remove_character(character)
    character.move(location_new)
    runtime.map.place_character(character.num, location_new)

    character.sp = character.sp_prev - location_dist

    result = result + location_new
    print(character.name, ":", result)
    print("------------------------------------------------------------------")
    return result

#---------------------------------------------------------------------------------------
def run_action_2(character, action, target, runtime, data):
    skill = data.get_skill(action)
    if skill == 0:
        print("no skill cmd is found in data")
        return

    result = "[" + character.name + "]의 " + "[" + skill.name + "]: "
    print(result, end='')

    # cost check
    sp_usage = 0
    if skill.cost == -1:
        result = result + "패시브"
        print("패시브")
        print("------------------------------------------------------------------")
        return result

    elif skill.cost == -2:
        if character.sp <= 0:
            result = result + "SP 부족"
            print("잔여 기력: SP 부족")
            print("------------------------------------------------------------------")
            return result

        sp_usage = character.sp

    elif skill.cost == -3:
        if character.sp <= character.sp_max:
            result = result + "SP 부족"
            print("최대 기력: SP 부족")
            print("------------------------------------------------------------------")
            return result

        sp_usage = character.sp

    elif character.sp < skill.cost:
        result = result + "SP 부족"
        print("코스트", skill.cost, ": SP 부족")
        print("------------------------------------------------------------------")
        return result

    elif character.sp >= skill.cost:
        sp_usage = skill.cost

    # target check 
    if skill.skill_range != -1 and target == '':
        result = result + "타겟 없음"
        print("타겟 없음")
        print("------------------------------------------------------------------")
        return result

    elif target != '':
        x = ord(target[0]) - ord('A')
        y = ord(target[1]) - ord('0')
        if (x < 0) or (x > 9) or (y < 0) or (y > 9):
            result = result + "잘못된 위치"
            print(result)
            print("------------------------------------------------------------------")
            return result

        if (skill.skill_target == 1 or skill.skill_target == 3):
            if runtime.map.is_placed(target) == 0:
                result = result + "대상 없음"
                print(result)
                print("------------------------------------------------------------------")
                return result

            target_id = runtime.map.get_character_placed(target)
            target_character = runtime.character.get_character(target_id)
            if ((skill.skill_target == 1 and target_character.type != character.type) or
                (skill.skill_target == 3 and target_character.type == character.type)):
                result = result + "잘못된 대상"
                print(result)
                print("------------------------------------------------------------------")
                return result

        # distance check 
        target_dist = get_dist(character.location, target)
        if skill.skill_range > 0 and target_dist > skill.skill_range:
            result = result + "사거리 바깥"
            print(result)
            print("------------------------------------------------------------------")
            return result

        elif skill.skill_range == -3:
            location = character.location
            x_cur = ord(location[0]) - ord('A')
            y_cur = ord(location[1]) - ord('0')
            if ((x_cur != x) and (y_cur != y)):
                result = result + "직선 범위 바깥"
                print(result)
                print("------------------------------------------------------------------")
                return result

    # calculate skill effects
    heal_value = skill.heal_base + skill.heal_base * sp_usage
    damage_value = skill.damage_base + skill.damage_base * sp_usage

    # apply skill effect to 1 target
    if skill.skill_target == 1 or skill.skill_target == 3:
        if heal_value != 0:
            target_character.increase_hp(heal_value)

        if damage_value != 0:
            damage = character.get_damage(damage_value)
            target_character.decrease_hp(damage)

        #if skill.paralyze != 0:
        if skill.poison != 0:
            target_character.increase_poison(skill.poison)

        if skill.weaken != 0:
            target_character.increase_weaken(skill.weaken)

        target.update_location()

    character.sp = character.sp - sp_usage
    character.action = character.action - 1
    character.update_location()

    return result

#---------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------
def run_action(character, action, target, runtime):

    if action == 'dance':
        return dance(character, runtime)

    elif action == 'aid':
        return aid(character, runtime)

    elif action == 'solist':
        return solist(character, runtime)

    elif action == 'sonata':
        return sonata(character, runtime)

    elif action == 'dim':
        return dim(character, runtime)

    elif action == 'save':
        return save(character, runtime)

    elif action == 'protect':
        return protect(character, runtime)

    elif action == 'swip_up':
        return swip_up(character, runtime)

    elif action == 'swip_down':
        return swip_down(character, runtime)

    elif action == 'explode':
        return explode(character, runtime)

    elif action == 'breakdown':
        return breakdown(character, runtime)

    elif action == 'sola':
        return sola(character, runtime)

    elif action == 'rage':
        return rage(character, runtime)

    elif action == 'punch_vertical':
        return punch_vertical(character, runtime)

    elif action == 'punch_horizon':
        return punch_horizon(character, runtime)

    elif target == '':
        return 'failed: no target'

    # direction
    elif target == 'UP' or target == 'DOWN' or target == 'LEFT' or target == 'RIGHT':
        if action == 'knockback_all':
            return knockback_all(character, target, runtime)

        else:
            return 'failed: not defined command'

    elif len(target) != 2:
        return 'failed: wrong target'

    elif action == 'attack':
        return attack(character, target, runtime)

    elif action == 'attack_2':
        return attack_2(character, target, runtime)

    elif action == 'throw':
        return throw(character, target, runtime)

    elif action == 'nocturn':
        return nocturn(character, target, runtime)

    elif action == 'song':
        return song(character, target, runtime)

    elif action == 'flash':
        return flash(character, target, runtime)

    elif action == 'quatro':
        return quatro(character, target, runtime)

    elif action == 'raven':
        return raven(character, target, runtime)

    elif action == 'stardust':
        return stardust(character, target, runtime)

    elif action == 'define':
        return define(character, target, runtime)

    elif action == 'dusk':
        return dusk(character, target, runtime)

    elif action == 'evade':
        return evade(character, target, runtime)

    elif action == 'swap':
        return swap(character, target, runtime)

    elif action == 'crystal_fall':
        return crystal_fall(character, target, runtime)

    elif action == 'poison_bite':
        return poison_bite(character, target, runtime)

    elif action == 'lift_wall':
        return lift_wall(character, target, runtime)

    elif action == 'flash_2':
        return flash_2(character, target, runtime)

    elif action == 'knockback':
        return knockback(character, target, runtime)

    elif action == 'finale':
        return finale(character, target, runtime)

    elif action == 'badmagic':
        return badmagic(character, target, runtime)

    elif action == 'makeidiot':
        return makeidiot(character, target, runtime)

    elif action == 'attack_call':
        return attack_call(character, target, runtime)

    elif action == 'share':
        return share(character, target, runtime)

    else:
        return 'failed: not defined command'


#---------------------------------------------------------------------------------------
# run
#---------------------------------------------------------------------------------------
def run_map_cmd(cmd, runtime, data):
    command = cmd.split()
    print("map:", command)

    if command[0] == 'start':
        if len(command) != 1:
            return "failed:input error"

        runtime.progress.start_progress()
        return "success: map start"

    elif command[0] == 'stop':
        if len(command) != 1:
            return "failed: input error"

        runtime.progress.stop_progress()
        return "success: map stop"

    elif command[0] == 'reset':
        if len(command) != 1:
            return "failed: input error"

        runtime.progress.reset_progress()

        data.reset_player()
        data.reset_enemy()
        data.reset_boss()
        data.reset_skill()
        data.print_data()

        return "success: map reset"

    elif command[0] == 'step':
        if len(command) != 1:
            return "failed: input error"

        result = runtime.progress.step_progress()
        if result == 1:
            runtime.character.start_round()

        elif result == 2:
            runtime.character.end_turn()

        elif result == 3:
            runtime.character.end_round()

        return "success: map step"

    return "failed: not defined command"


def run_apply_passive(character, cmd, name, runtime):
    if cmd == "hp_boost":
        print("[" + name + "]:",
              "hp:", character.hp, "->", character.hp + 30,
              "hp_max:", character.hp_max, "->", character.hp_max + 30)

        character.hp = character.hp + 30
        character.hp_max = character.hp_max + 30

    elif cmd == "sp_boost":
        print("[" + name + "]:",
              "sp:", character.sp, "->", character.sp + 2,
              "sp_max:", character.sp_max, "->", character.sp_max + 2,
              "sp_prev:", character.sp_prev, "->", character.sp_prev + 2)

        character.sp = character.sp + 2
        character.sp_max = character.sp_max + 2
        character.sp_prev = character.sp_prev + 2

    elif cmd == "mp_boost":
        print("[" + name + "]:",
              "mp:", character.mp, "->", character.mp + 2,
              "mp_max:", character.mp_max, "->", character.mp_max + 2)

        character.mp = character.mp + 2
        character.mp_max = character.mp_max + 2

    elif cmd == "polka":
        if character.is_enemy():
            print("[" + name + "]: enemy polka:",
                  runtime.character.polka_enemy, "->", runtime.character.polka_enemy + 1)

            runtime.character.increase_enemy_polka()

        elif character.is_player():
            print("[" + name + "]: player polka:",
                  runtime.character.polka_player, "->", runtime.character.polka_player + 1)

            runtime.character.increase_player_polka()

        character.polka = 1

    elif cmd == "dawn":
        print("[" + name + "]:",
              "hp:", character.hp, "->", character.hp + 70,
              "hp_max:", character.hp_max, "->", character.hp_max + 70,
              "tank:", character.tank, "->", 1,
              "provoke:", character.provoke, "->", 1)

        character.hp = character.hp + 70
        character.hp_max = character.hp_max + 70
        character.tank = 1
        character.provoke = 1

    elif cmd == "cast":
        print("[" + name + "]:",
              "action:", character.action, "->", character.action + 1,
              "action_max:", character.action_max, "->", character.action_max + 1)

        character.action = character.action + 1
        character.action_max = character.action_max + 1

    elif cmd == "crown":
        print("[" + name + "]:",
              "crown:", character.crown, "->", 1)

        character.crown = 1

    elif cmd == "bookmark":
        print("[" + name + "]: do nothing")

    else:
        print("invalid passive")


def run_character_add(character_id, data_id, location, runtime, data):
    character = runtime.character.get_character(character_id)

    if character.is_enemy():
        character_data = data.get_enemy(data_id)
        polka_stack = runtime.character.polka_enemy

    elif character.is_player():
        character_data = data.get_player(data_id)
        polka_stack = runtime.character.polka_player

    elif character.is_boss():
        return "failed: tried to add boss slot"

    if character.add(location, character_data, polka_stack) == 0:
        return "failed: character already added"

    if runtime.map.place_character(character_id, location) == 0:
        character.remove()
        return "failed: character already placed"

    skill = data.skill[character_data.skill_1]
    if skill.passive == 1:
        run_apply_passive(character, skill.cmd, skill.name, runtime)

    skill = data.skill[character_data.skill_2]
    if skill.passive == 1:
        run_apply_passive(character, skill.cmd, skill.name, runtime)

    skill = data.skill[character_data.skill_3]
    if skill.passive == 1:
        run_apply_passive(character, skill.cmd, skill.name, runtime)

    skill = data.skill[character_data.skill_4]
    if skill.passive == 1:
        run_apply_passive(character, skill.cmd, skill.name, runtime)

    skill = data.skill[character_data.skill_5]
    if skill.passive == 1:
        run_apply_passive(character, skill.cmd, skill.name, runtime)

    skill = data.skill[character_data.skill_6]
    if skill.passive == 1:
        run_apply_passive(character, skill.cmd, skill.name, runtime)

    skill = data.skill[character_data.skill_7]
    if skill.passive == 1:
        run_apply_passive(character, skill.cmd, skill.name, runtime)

    return "success: character added to " + location


def run_character_remove(character_id, runtime):
    character = runtime.character.get_character(character_id)

    if character.polka == 1 and (character.is_enemy() or character.is_boss()):
        runtime.character.decrease_enemy_polka()

    if character.polka == 1 and character.is_player():
        runtime.character.decrease_player_polka()

    runtime.map.remove_character(character)
    character.remove()

    return "success: character removed"


def run_boss_add_robot(robot, runtime, data):
    polka_stack = runtime.character.polka_enemy

    robot_data = data.get_boss(4)
    if robot.add_boss(robot_data, polka_stack) == 0:
        return "failed: character already added"

    wall_1_data = data.get_boss(5)
    wall_1 = runtime.character.get_empty_enemy()
    if wall_1 == 0:
        return "failed: no enemy slot for wall 1"

    elif wall_1.add_boss(wall_1_data, polka_stack) == 0:
        return "failed: character already added"

    wall_2_data = data.get_boss(6)
    wall_2 = runtime.character.get_empty_enemy()
    if wall_2 == 0:
        return "failed: no enemy slot for wall 2"

    elif wall_2.add_boss(wall_2_data, polka_stack) == 0:
        return "failed: character already added"

    wall_3_data = data.get_boss(7)
    wall_3 = runtime.character.get_empty_enemy()
    if wall_3 == 0:
        return "failed: no enemy slot for wall 3"

    elif wall_3.add_boss(wall_3_data, polka_stack) == 0:
        return "failed: character already added"

    wall_4_data = data.get_boss(8)
    wall_4 = runtime.character.get_empty_enemy()
    if wall_4 == 0:
        return "failed: no enemy slot for wall 4"

    elif wall_4.add_boss(wall_4_data, polka_stack) == 0:
        return "failed: character already added"

    wall_5_data = data.get_boss(9)
    wall_5 = runtime.character.get_empty_enemy()
    if wall_5 == 0:
        return "failed: no enemy slot for wall 5"

    elif wall_5.add_boss(wall_5_data, polka_stack) == 0:
        return "failed: character already added"

    robot.set_boss(wall_1, wall_2, wall_3, wall_4, wall_5)

    wall_1.set_boss(robot, 0, 0, 0, 0)
    wall_2.set_boss(robot, 0, 0, 0, 0)
    wall_3.set_boss(robot, 0, 0, 0, 0)
    wall_4.set_boss(robot, 0, 0, 0, 0)
    wall_5.set_boss(robot, 0, 0, 0, 0)

    if runtime.map.place_boss(robot) == 0:
        print("failed: place robot")

    if runtime.map.place_boss(wall_1) == 0:
        print("failed: place wall_1")

    if runtime.map.place_boss(wall_2) == 0:
        print("failed: place wall_2")

    if runtime.map.place_boss(wall_3) == 0:
        print("failed: place wall_3")

    if runtime.map.place_boss(wall_4) == 0:
        print("failed: place wall_4")

    if runtime.map.place_boss(wall_5) == 0:
        print("failed: place wall_5")

    return "success: character added as boss"


def run_boss_add_angel(angel, runtime, data):
    polka_stack = runtime.character.polka_enemy

    angel_data = data.get_boss(1)
    if angel.add_boss(angel_data, polka_stack) == 0:
        return "failed: character already added"

    left_wing_data = data.get_boss(2)
    left_wing = runtime.character.get_empty_enemy()
    if left_wing == 0:
        return "failed: no enemy slot for left wing"

    elif left_wing.add_boss(left_wing_data, polka_stack) == 0:
        return "failed: character already added"

    right_wing_data = data.get_boss(3)
    right_wing = runtime.character.get_empty_enemy()
    if right_wing == 0:
        return "failed: no enemy slot for right wing"

    elif right_wing.add_boss(right_wing_data, polka_stack) == 0:
        return "failed: character already added"

    angel.set_boss(left_wing, right_wing, __, __, __)
    left_wing.set_boss(angel, __, __, __, __)
    right_wing.set_boss(angel, __, __, __, __)

    if runtime.map.place_boss(angel) == 0:
        print("failed: place angel")

    if runtime.map.place_boss(left_wing) == 0:
        print("failed: place left_wing")

    if runtime.map.place_boss(right_wing) == 0:
        print("failed: place right_wing")

    return "success: character added as boss"


def run_boss_add(character_id, data_id, runtime, data):
    character = runtime.character.get_character(character_id)
    if character.is_player():
        return "failed: boss cannot be added as player"

    if data_id == 0:
        return "failed: 사다크비아 is not supported now"

    elif data_id == 1:
        return run_boss_add_angel(character, runtime, data)

    elif data_id == 2:
        return run_boss_add_robot(character, runtime, data)

    else:
        return "failed: boss is not supported now"


def run_character_cmd(cmd, character_id, runtime, data):
    command = cmd.split()
    print("character", str(character_id), ":", command)

    if len(command) == 0:
        return "failed: input error"

    # add
    if command[0] == 'add':
        if len(command) != 3:
            return "failed: input error"

        if command[1] == 'boss':
            if command[2] == 'angel':
                return run_boss_add(character_id, 1, runtime, data)
            elif command[2] == 'robot':
                return run_boss_add(character_id, 2, runtime, data)

            return run_boss_add(character_id, int(command[2]), runtime, data)

        else:
            if command[1] == 'horizon':
                return run_character_add(character_id, 38, command[2], runtime, data)
            elif command[1] == 'vertical':
                return run_character_add(character_id, 39, command[2], runtime, data)
            elif command[1] == 'ball':
                return run_character_add(character_id, 37, command[2], runtime, data)
            elif command[1] == 'cross':
                return run_character_add(character_id, 36, command[2], runtime, data)
            elif command[1] == 'amber':
                return run_character_add(character_id, 32, command[2], runtime, data)

            else:
                return run_character_add(character_id, int(command[1]), command[2],
                                     runtime, data)

    # remove
    elif command[0] == 'remove':
        if len(command) != 1:
            return "failed: input error"

        return run_character_remove(character_id, runtime)

    return "failed: not defined command"


def run_command(runtime, data):
    #runtime.commands.print_all_cmd()

    # map command
    command = runtime.commands.get_map_command()
    cmd = command.get_cmd()
    if cmd != '':
        result = run_map_cmd(cmd, runtime, data)
        command.update_cmd(result)

    # character command
    for char_id in range(0, 24):
        character = runtime.character.get_character(char_id)
        command = runtime.commands.get_character_command(char_id)

        cmd = command.get_cmd()
        move = command.get_move()
        action = command.get_action()
        target = command.get_target()
        event = command.get_event()

        if cmd != '':
            result = run_character_cmd(cmd, char_id, runtime, data)
            runtime.map.print_map()
            command.update_cmd(result)

        # console move
        elif move != '':
            result = run_move(character, move, runtime)
            command.update_cmd_console(result)

        # console action
        elif event == 'TRUE':
            result = run_action(character, action, target, runtime)
            #result = run_action_2(character, action, target, runtime, data)
            command.update_cmd_console(result)

#---------------------------------------------------------------------------------------
# main
#---------------------------------------------------------------------------------------
if __name__ == '__main__':
    print("inititialize")

    # initialize data
    print("inititialize data")
    data = raid_data.data()
    data.init_player()
    data.init_enemy()
    data.init_boss()
    data.init_skill()
    data.print_data()

    # initialize runtime
    print("inititialize runtime")
    runtime = raid_runtime.runtime()
    runtime.get_runtime()
    runtime.sync_runtime()
    runtime.update_runtime_data()
    while runtime.update_runtime():
        time.sleep(1)

    # initialize console
    print("inititialize console admin")
    console_admin = console("./console_goblin_0.json", "console_admin")
    console_admin.connect_command(runtime.commands.get_character_command(0),
                                  runtime.commands.get_character_command(1),
                                  runtime.commands.get_character_command(2),
                                  runtime.commands.get_character_command(3),
                                  runtime.commands.get_character_command(4),
                                  runtime.commands.get_character_command(5))

    print("inititialize console admin 1")
    console_admin_1 = console("./console_goblin_1.json", "console_admin_1")
    console_admin_1.connect_command(runtime.commands.get_character_command(6),
                                    runtime.commands.get_character_command(7),
                                    runtime.commands.get_character_command(8),
                                    runtime.commands.get_character_command(9),
                                    runtime.commands.get_character_command(10),
                                    runtime.commands.get_character_command(11))

    print("inititialize console")
    console_player = console("./console_goblin_2.json", "console")
    console_player.connect_command(runtime.commands.get_character_command(12),
                                   runtime.commands.get_character_command(13),
                                   runtime.commands.get_character_command(14),
                                   runtime.commands.get_character_command(15),
                                   runtime.commands.get_character_command(16),
                                   runtime.commands.get_character_command(17))

    print("inititialize console")
    console_player_1 = console("./console_goblin_3.json", "console_1")
    console_player_1.connect_command(runtime.commands.get_character_command(18),
                                     runtime.commands.get_character_command(19),
                                     runtime.commands.get_character_command(20),
                                     runtime.commands.get_character_command(21),
                                     runtime.commands.get_character_command(22),
                                     runtime.commands.get_character_command(23))


    print("inititialize done")
    print("------------------------------------------------------------------")
    # get command
    while 1:
        runtime.get_runtime_cmd()
        runtime.parse_command()

        run_command(runtime, data)

        #raid_progress.run_progress()
        #raid_character.run_characters()
        runtime.run_runtime()

        console_admin.update_console()
        console_admin_1.update_console()
        console_player.update_console()
        console_player_1.update_console()


        runtime.update_runtime_data()
        while runtime.update_runtime():
            time.sleep(1)

        time.sleep(1)
