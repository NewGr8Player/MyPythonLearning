def triangles():
    """
    杨辉三角形
    :return:
    """
    result = [
        [1]
    ]
    index = 0
    while True:
        cur = []
        pre = result[index]
        yield pre
        length = len(pre)
        cur.append(1)
        for i in range(1, length):
            cur.append(pre[i - 1] + pre[i])
        cur.append(1)
        result.append(cur)
        index += 1


# main method
if __name__ == '__main__':
    n = 0
    results = []
    for t in triangles():
        results.append(t)
        n = n + 1
        if n == 10:
            break
    if results == [
        [1],
        [1, 1],
        [1, 2, 1],
        [1, 3, 3, 1],
        [1, 4, 6, 4, 1],
        [1, 5, 10, 10, 5, 1],
        [1, 6, 15, 20, 15, 6, 1],
        [1, 7, 21, 35, 35, 21, 7, 1],
        [1, 8, 28, 56, 70, 56, 28, 8, 1],
        [1, 9, 36, 84, 126, 126, 84, 36, 9, 1]
    ]:
        print('测试通过!')
    else:
        print('测试失败!')
