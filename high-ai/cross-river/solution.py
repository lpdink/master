import json
import copy


class LocalState:
    def __init__(self, wild_num, miss_num) -> None:
        self.wild_num = wild_num
        self.miss_num = miss_num

    def __str__(self) -> str:
        return " ".join([str(self.wild_num), str(self.miss_num)])

    @property
    def num(self):
        return self.wild_num+self.miss_num


class GlobalState:
    def __init__(self) -> None:
        self.origin = LocalState(3, 3)
        self.boot = LocalState(0, 0)
        self.end = LocalState(0, 0)
        self.child_state_id = set()

    def __str__(self) -> str:
        return " ".join([str(self.origin), str(self.boot), str(self.end)])

    def __eq__(self, __o: object) -> bool:
        return str(self) == str(__o)

    @property
    def id(self):
        return str(self)

    def is_valid(self):
        # 野人大于传教士
        if self.origin.wild_num > self.origin.miss_num and self.origin.miss_num > 0:
            return False
        if self.end.wild_num > self.end.miss_num and self.end.miss_num > 0:
            return False
        if self.origin.wild_num+self.boot.wild_num > self.origin.miss_num+self.boot.miss_num and (self.origin.miss_num > 0 or self.boot.miss_num > 0):
            return False
        if self.end.wild_num+self.boot.wild_num > self.end.miss_num+self.boot.miss_num and (self.end.miss_num > 0 or self.boot.miss_num > 0):
            return False
        # 没有人开船，且不到达终止状态
        if self.origin.num != 0 and self.boot.num == 0:
            return False
        return True

    def is_end(self):
        return self.end.miss_num == 3 and self.end.wild_num == 3

    def transfer(self):
        def side_transfer(self: GlobalState, attr):
            rst = []
            tmp_state = copy.deepcopy(self)
            # 让船上的人先都下来
            getattr(tmp_state, attr).wild_num += tmp_state.boot.wild_num
            getattr(tmp_state, attr).miss_num += tmp_state.boot.miss_num
            tmp_state.boot.wild_num = 0
            tmp_state.boot.miss_num = 0
            new_state = copy.deepcopy(tmp_state)
            rst.append(new_state)
            # 上一个野人
            if getattr(tmp_state, attr).wild_num > 0:
                new_state = copy.deepcopy(tmp_state)
                getattr(new_state, attr).wild_num -= 1
                new_state.boot.wild_num += 1
                rst.append(new_state)
            # 上两个野人
            if getattr(tmp_state, attr).wild_num > 1:
                new_state = copy.deepcopy(tmp_state)
                getattr(new_state, attr).wild_num -= 2
                new_state.boot.wild_num += 2
                rst.append(new_state)
            # 上一个传教士
            if getattr(tmp_state, attr).miss_num > 0:
                new_state = copy.deepcopy(tmp_state)
                getattr(new_state, attr).miss_num -= 1
                new_state.boot.miss_num += 1
                rst.append(new_state)
            # 上两个传教士
            if getattr(tmp_state, attr).miss_num > 1:
                new_state = copy.deepcopy(tmp_state)
                getattr(new_state, attr).miss_num -= 2
                new_state.boot.miss_num += 2
                rst.append(new_state)
            # 上一个野人和一个传教士
            if getattr(tmp_state, attr).wild_num > 0 and getattr(tmp_state, attr).miss_num > 0:
                new_state = copy.deepcopy(tmp_state)
                getattr(new_state, attr).wild_num -= 1
                getattr(new_state, attr).miss_num -= 1
                new_state.boot.wild_num += 1
                new_state.boot.miss_num += 1
                rst.append(new_state)
            return rst
        rst = side_transfer(self, "origin") + side_transfer(self, "end")
        return [state for state in rst if state.is_valid()]


def main():
    visited_state = []
    start = GlobalState()
    to_visit_state = [start]
    father2child = dict()
    while len(to_visit_state) != 0:
        now_state: GlobalState = to_visit_state.pop()
        childs = now_state.transfer()
        father2child[str(now_state)] = list({str(child) for child in childs})
        for state in childs:
            if state not in visited_state and state not in to_visit_state and state != str(now_state):
                to_visit_state.append(state)
        visited_state.append(now_state)
    # 回溯法

    def trackback(now_state, path, rst):
        if "0 0 0 0 3 3" in father2child[now_state]:
            path.append("0 0 0 0 3 3")
            rst.append(copy.deepcopy(path))
            return
        for sub_state in father2child[now_state]:
            if sub_state not in path:
                path.append(copy.deepcopy(sub_state))
                trackback(sub_state, copy.deepcopy(path), rst)
                path.pop()
    rst = []
    begin_state = "3 3 0 0 0 0"
    path = [begin_state]
    trackback(begin_state, path, rst)

    # 取最短
    min_length = 1e9
    for path in rst:
        min_length = min(min_length, len(path))
    print("min length solutions: ")
    print("origin_wild origin_miss boat_wild boat_miss end_wild end_miss")
    min_length_answers = []
    for path in rst:
        if len(path) == min_length:
            min_length_answers.append(path)
            print("\n".join(path))
            print("="*10)

    # 组织答案
    answer = {"min_length_answers": min_length_answers,
              "transfer_space": father2child, "all_no_repeat_path_answers": rst}
    with open("./space.json", "w", encoding="utf-8") as file:
        json.dump(answer, file, indent=4)


if __name__ == "__main__":
    main()
