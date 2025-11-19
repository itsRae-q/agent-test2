def binary_search(arr, target):
    """
    简单的二分查找算法
    参数:
        arr: 已排序的数组
        target: 要查找的目标值
    返回:
        目标值的索引，如果不存在返回-1
    """
    left = 0
    right = len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1

# 测试示例
if __name__ == "__main__":
    # 测试数据
    numbers = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
    
    # 测试查找
    target = 7
    result = binary_search(numbers, target)
    
    if result != -1:
        print(f"找到了！数字 {target} 在索引 {result} 位置")
    else:
        print(f"没有找到数字 {target}")
    
    # 更多测试
    test_cases = [1, 5, 11, 20, 0]
    for num in test_cases:
        index = binary_search(numbers, num)
        if index != -1:
            print(f"数字 {num} 在索引 {index}")
        else:
            print(f"数字 {num} 不在数组中")