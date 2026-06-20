'''
冒泡排序
'''
if __name__ == '__main__':
    num = [10, 88, 5, 70, 99, 3]
    for i in range(len(num)-1):
        for j in range(len(num)-i-1):
            if num[j] > num[j+1]:
                num[j], num[j+1] = num[j+1], num[j]
    print(num)
