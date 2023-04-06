def adj_nums(num):
    res = 0
    nums = []
    while res < num:
        ok = 1

        str_res = str(res)
        prev = str_res[0]
        if len(str_res) < 2:
            nums.append(res)
            ok = 0
        else:
            for i in range(1, len(str_res)):
                if int(prev) - 1 != int(str_res[i]) and int(prev) + 1 != int(str_res[i]):
                    ok = 0
                prev = str_res[i]
        if ok:
            nums.append(res)

        res += 1
    print(nums)

adj_nums(9999)