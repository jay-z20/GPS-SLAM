import os
import shutil
from pathlib import Path

# ================== 配置区 ==================
source_dir = Path("/root/office0")           # 原始文件夹
target_dir = Path("/root/office0_small")     # 生成的小数据集文件夹

num_samples = 400                      # 采样前400帧

# 文件命名规则
pattern = "{:06d}"                     # 6位数字
rgb_prefix = "frame"
depth_prefix = "depth"
rgb_ext = ".jpg"
depth_ext = ".png"
# ===========================================

def main():
    if not source_dir.exists():
        print(f"错误: 源文件夹 {source_dir} 不存在！")
        return

    target_dir.mkdir(parents=True, exist_ok=True)
    target_results = target_dir / "results"
    target_results.mkdir(exist_ok=True)

    copied = 0
    for i in range(num_samples):
        num_str = pattern.format(i)
        
        rgb_name = f"{rgb_prefix}{num_str}{rgb_ext}"
        depth_name = f"{depth_prefix}{num_str}{depth_ext}"
        
        rgb_src = source_dir / "results" / rgb_name
        depth_src = source_dir / "results" / depth_name
        
        if rgb_src.exists() and depth_src.exists():
            shutil.copy2(rgb_src, target_results / rgb_name)
            shutil.copy2(depth_src, target_results / depth_name)
            copied += 1
            
            if copied % 50 == 0:
                print(f"✅ 已复制 {copied} 帧")
        else:
            print(f"⚠️  第 {i} 帧缺失: {rgb_name} 或 {depth_name}")
            break

    # ================== 处理 traj.txt ==================
    traj_src = source_dir / "traj.txt"
    if traj_src.exists():
        with open(traj_src, 'r') as f:
            lines = f.readlines()
        
        # 取前400行
        sampled_lines = lines[:num_samples]
        
        with open(target_dir / "traj.txt", 'w') as f:
            f.writelines(sampled_lines)
        
        print(f"✅ 已采样 traj.txt 前 {len(sampled_lines)} 行")
    else:
        print("⚠️  未找到 traj.txt")

    print(f"\n🎉 采样完成！共成功复制 {copied} 帧")
    print(f"小数据集路径: {target_dir.resolve()}")
    print(f"结果保存在: {target_results.resolve()}")

if __name__ == "__main__":
    main()