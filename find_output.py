"""查找特定指令的四进制编码"""

def find_instruction(target_name):
    """查找指令的编码"""
    # 简化版指令表
    instructions = {
        # 组1: 常量 (16-31)
        16: 'PUSH_0',
        17: 'PUSH_1', 
        18: 'PUSH_2',
        19: 'PUSH_5',
        20: 'PUSH_10',
        21: 'PUSH_42',
    }
    
    for opcode, name in instructions.items():
        if name == target_name:
            # 转四进制
            quat = ''
            n = opcode
            if n == 0:
                return '000'
            digits = []
            while n > 0:
                digits.append(str(n % 4))
                n //= 4
            quat = ''.join(reversed(digits))
            # 补齐到3位
            quat = quat.zfill(3)
            print(f"{name} = {opcode} (十进制) = {quat} (四进制)")
            return quat
    
    return None

# 查找PUSH_3
print("Looking for PUSH_3...")
result = find_instruction('PUSH_3')
if not result:
    print("PUSH_3 not found! Need to use PUSH_2 + PUSH_1 + ADD")
    print()
    print("Let's verify the instruction encodings:")
    find_instruction('PUSH_2')  # Should be 102
    find_instruction('PUSH_5')  # Should be 103
    find_instruction('PUSH_10') # Should be 120

print("\n--- Decode Test ---")
print("103 (quaternary) =", int('103', 4), "(decimal)")
print("120 (quaternary) =", int('120', 4), "(decimal)")
