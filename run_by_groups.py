#!/usr/bin/env python3
"""
按组运行股票分析脚本：
- 读取 config_groups.yaml
- 对每个 group，将 global 参数与 group.params 合并（group 覆盖 global）
- 将 tickers 传给现有的分析函数

说明：请把 run_analysis_for_tickers 替换为你仓库中实际的分析入口函数。
"""

import yaml
import copy
import sys
from pathlib import Path

# TODO: 修改下面导入为你仓库中真正的分析入口
# 例如：from analysis.main import run_analysis
def run_analysis_for_tickers(config):
    """
    占位函数：把 config 中的信息传给你现有的分析流程。
    请替换为实际调用，例如：
      from mypkg.analysis import analyze
      analyze(config)
    """
    print(f"Running analysis for group={{config.get('group_name')}} tickers={{config.get('tickers')}}")
    # 在这里调用真实分析函数
    # analyze(config)
    return

def deep_merge(a, b):
    """简单的深度合并：b 覆盖 a 的值（用于合并 global 与 group.params）"""
    if not isinstance(a, dict) or not isinstance(b, dict):
        return copy.deepcopy(b)
    out = copy.deepcopy(a)
    for k, v in b.items():
        if k in out and isinstance(out[k], dict) and isinstance(v, dict):
            out[k] = deep_merge(out[k], v)
        else:
            out[k] = copy.deepcopy(v)
    return out


def main(cfg_path):
    with open(cfg_path, 'r', encoding='utf-8') as f:
        cfg = yaml.safe_load(f)

    global_cfg = cfg.get('global', {})
    groups = cfg.get('groups', [])
    if not groups:
        print("config has no groups; nothing to do.")
        return

    for group in groups:
        name = group.get('name')
        tickers = group.get('tickers', [])
        group_params = group.get('params', {}) or {}

        # 合并参数：group 覆盖 global
        merged = deep_merge(global_cfg, group_params)
        merged['group_name'] = name
        merged['tickers'] = tickers

        # 调用现有的分析流程（替换为你自己的函数）
        run_analysis_for_tickers(merged)

if __name__ == "__main__":
    cfg = sys.argv[1] if len(sys.argv) > 1 else "config_groups.yaml"
    if not Path(cfg).exists():
        print(f"配置文件 {{cfg}} 不存在。")
        sys.exit(1)
    main(cfg)
