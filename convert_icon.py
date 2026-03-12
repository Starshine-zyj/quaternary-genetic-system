#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图标转换工具 - 将 PNG 转换为 ICO 格式
"""

import os
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("❌ 错误: 未安装 Pillow 库")
    print("请运行: pip install pillow")
    sys.exit(1)


def convert_png_to_ico(png_path, ico_path, sizes=None):
    """
    将 PNG 图片转换为 ICO 格式
    
    Args:
        png_path: PNG 文件路径
        ico_path: ICO 输出路径
        sizes: 图标尺寸列表，默认 [256, 128, 64, 48, 32, 16]
    """
    if sizes is None:
        sizes = [256, 128, 64, 48, 32, 16]
    
    try:
        # 打开 PNG 图片
        img = Image.open(png_path)
        
        # 确保是 RGBA 模式
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # 生成多个尺寸的图标
        icon_sizes = []
        for size in sizes:
            resized = img.resize((size, size), Image.Resampling.LANCZOS)
            icon_sizes.append(resized)
        
        # 保存为 ICO 格式
        icon_sizes[0].save(
            ico_path,
            format='ICO',
            sizes=[(size, size) for size in sizes]
        )
        
        print(f"✓ 成功: {png_path} -> {ico_path}")
        print(f"  包含尺寸: {sizes}")
        return True
        
    except Exception as e:
        print(f"❌ 转换失败: {e}")
        return False


def find_dna_icon():
    """查找 DNA 图标文件"""
    current_dir = Path(__file__).parent
    
    # 查找所有可能的 DNA 图标文件
    patterns = [
        "A_DNA_double_helix_icon*.png",
        "dna_icon.png",
        "dna*.png"
    ]
    
    for pattern in patterns:
        matches = list(current_dir.glob(pattern))
        if matches:
            # 返回最新的文件
            return max(matches, key=lambda p: p.stat().st_mtime)
    
    return None


def main():
    """主函数"""
    print("=" * 60)
    print("DNA 图标转换工具")
    print("=" * 60)
    
    # 查找 DNA 图标
    png_path = find_dna_icon()
    
    if not png_path:
        print("❌ 错误: 未找到 DNA 图标文件")
        print("请确保目录中存在 DNA 图标 PNG 文件")
        sys.exit(1)
    
    print(f"✓ 找到图标: {png_path.name}")
    
    # 转换为 ICO
    ico_path = Path(__file__).parent / "dna_icon.ico"
    
    if convert_png_to_ico(str(png_path), str(ico_path)):
        print(f"✓ 图标已生成: {ico_path}")
        print(f"  文件大小: {ico_path.stat().st_size:,} 字节")
    else:
        sys.exit(1)


if __name__ == '__main__':
    main()
