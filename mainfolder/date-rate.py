def bit_length(n: int) -> int:
    if n <= 0:
        raise ValueError("正の整数を入力してください")
    return n.bit_length()

# 使用例
x = int(input())
print(bit_length(x))
