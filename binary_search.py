#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
二分查找算法实现
Binary Search Algorithm Implementation

作者: AI Assistant
日期: 2025-11-19
"""


def binary_search(arr, target):
    """
    二分查找算法 - 在有序数组中查找目标值
    
    参数:
        arr (list): 已排序的数组（升序）
        target: 要查找的目标值
    
    返回:
        int: 如果找到目标值，返回其索引；否则返回-1
    
    时间复杂度: O(log n)
    空间复杂度: O(1)
    """
    if not arr:
        return -1
    
    left = 0
    right = len(arr) - 1
    
    while left <= right:
        # 计算中间位置，防止整数溢出
        mid = left + (right - left) // 2
        
        if arr[mid] == target:
            return mid  # 找到目标值，返回索引
        elif arr[mid] < target:
            left = mid + 1  # 目标值在右半部分
        else:
            right = mid - 1  # 目标值在左半部分
    
    return -1  # 未找到目标值


def binary_search_recursive(arr, target, left=0, right=None):
    """
    二分查找算法 - 递归实现版本
    
    参数:
        arr (list): 已排序的数组（升序）
        target: 要查找的目标值
        left (int): 搜索范围的左边界
        right (int): 搜索范围的右边界
    
    返回:
        int: 如果找到目标值，返回其索引；否则返回-1
    """
    if not arr:
        return -1
    
    if right is None:
        right = len(arr) - 1
    
    if left > right:
        return -1  # 搜索范围无效，未找到
    
    mid = left + (right - left) // 2
    
    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        return binary_search_recursive(arr, target, mid + 1, right)
    else:
        return binary_search_recursive(arr, target, left, mid - 1)


def binary_search_leftmost(arr, target):
    """
    查找目标值的最左边位置（适用于有重复元素的数组）
    
    参数:
        arr (list): 已排序的数组（升序）
        target: 要查找的目标值
    
    返回:
        int: 目标值的最左边索引，如果不存在返回-1
    """
    if not arr:
        return -1
    
    left, right = 0, len(arr) - 1
    result = -1
    
    while left <= right:
        mid = left + (right - left) // 2
        
        if arr[mid] == target:
            result = mid  # 记录找到的位置
            right = mid - 1  # 继续在左半部分查找
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return result


def binary_search_rightmost(arr, target):
    """
    查找目标值的最右边位置（适用于有重复元素的数组）
    
    参数:
        arr (list): 已排序的数组（升序）
        target: 要查找的目标值
    
    返回:
        int: 目标值的最右边索引，如果不存在返回-1
    """
    if not arr:
        return -1
    
    left, right = 0, len(arr) - 1
    result = -1
    
    while left <= right:
        mid = left + (right - left) // 2
        
        if arr[mid] == target:
            result = mid  # 记录找到的位置
            left = mid + 1  # 继续在右半部分查找
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return result


def test_binary_search():
    """
    测试二分查找算法的各种情况
    """
    print("=" * 50)
    print("二分查找算法测试")
    print("=" * 50)
    
    # 测试用例1: 基本功能测试
    arr1 = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
    print(f"测试数组: {arr1}")
    
    test_cases = [7, 1, 19, 10, 0, 20]
    for target in test_cases:
        result = binary_search(arr1, target)
        if result != -1:
            print(f"查找 {target}: 找到，索引为 {result}")
        else:
            print(f"查找 {target}: 未找到")
    
    print("\n" + "-" * 30)
    
    # 测试用例2: 递归版本测试
    print("递归版本测试:")
    for target in [5, 15, 8]:
        result = binary_search_recursive(arr1, target)
        if result != -1:
            print(f"递归查找 {target}: 找到，索引为 {result}")
        else:
            print(f"递归查找 {target}: 未找到")
    
    print("\n" + "-" * 30)
    
    # 测试用例3: 重复元素测试
    arr2 = [1, 2, 2, 2, 3, 4, 4, 5, 5, 5, 5, 6]
    print(f"重复元素数组: {arr2}")
    
    target = 5
    leftmost = binary_search_leftmost(arr2, target)
    rightmost = binary_search_rightmost(arr2, target)
    print(f"查找 {target}: 最左位置 {leftmost}, 最右位置 {rightmost}")
    
    target = 2
    leftmost = binary_search_leftmost(arr2, target)
    rightmost = binary_search_rightmost(arr2, target)
    print(f"查找 {target}: 最左位置 {leftmost}, 最右位置 {rightmost}")
    
    print("\n" + "-" * 30)
    
    # 测试用例4: 边界情况测试
    print("边界情况测试:")
    
    # 空数组
    empty_arr = []
    result = binary_search(empty_arr, 5)
    print(f"空数组查找: {result}")
    
    # 单元素数组
    single_arr = [42]
    result1 = binary_search(single_arr, 42)
    result2 = binary_search(single_arr, 10)
    print(f"单元素数组查找 42: {result1}")
    print(f"单元素数组查找 10: {result2}")
    
    print("=" * 50)


if __name__ == "__main__":
    # 运行测试
    test_binary_search()
    
    print("\n使用示例:")
    print("from binary_search import binary_search")
    print("arr = [1, 3, 5, 7, 9, 11, 13, 15]")
    print("result = binary_search(arr, 7)")
    print("print(f'找到元素7的索引: {result}')")