# 变量不是盒子，而是标签

if __name__ == "__main__":
    my_list = [1, 2, 3]
    other_list_fake = my_list
    other_list_fake.append(4)
    print(my_list)
