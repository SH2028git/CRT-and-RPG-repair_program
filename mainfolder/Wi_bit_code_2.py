import numpy as np
import binary_to_perm_3

def wi_bit_code(number: int):#Wi->B*の変換
    """
    完全NumPy版 Wi_Bit_Code
    - 文字列操作を最小化し、最初からNumPy配列で処理
    - 入力: number（自然数）
    - 出力: NumPy配列と生成文字列
    """

    # --- number → 2進数をNumPy配列に変換 ---
    # np.binary_repr で '101' のような文字列を取得し、
    # それを即座にNumPy配列 (int8) に変換
    binary_str = np.binary_repr(number)
    binary_arr = np.fromiter(binary_str, dtype=np.int8)

    length = binary_arr.size

    # --- "0" * len(binary_str) + binary_str + "0" をNumPy配列で構成 ---
    prefix = np.zeros(length, dtype=np.int8)  # 先頭のゼロ部分
    suffix = np.array([0], dtype=np.int8)     # 最後のゼロ
    result_arr = np.concatenate([prefix, binary_arr, suffix])

    # --- 出力（確認用） ---
    """
    result_str = ''.join(map(str, result_arr))
    print("生成文字列:", result_str)
    print("NumPy配列:", result_arr)
    """
    return(result_arr)