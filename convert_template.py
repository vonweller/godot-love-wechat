#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import shutil
import zipfile
import json
import argparse
from pathlib import Path


def create_wechat_template(source_dir, template_name, output_dir="./templates"):
    """
    将自定义的Godot Web导出模板转换为微信小游戏模板
    
    Args:
        source_dir (str): 包含自定义Godot Web导出文件的目录
        template_name (str): 生成的模板文件名（不含扩展名）
        output_dir (str): 输出目录，默认为./templates
    """
    
    # 确保输出目录存在
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # 创建临时目录结构
    temp_dir = Path("temp_template")
    if temp_dir.exists():
        shutil.rmtree(temp_dir, ignore_errors=True)
        # 等待一段时间确保目录被删除
        import time
        time.sleep(0.1)
    temp_dir.mkdir(exist_ok=True)
    
    # 使用 d:\Do\Githubs\godot-minigame-template 作为模板基础
    template_source = Path(r"d:\Do\Githubs\godot-minigame-template")
    print(f"使用 {template_source} 作为模板基础，复制所有文件...")
    
    # 检查模板源目录是否存在
    if not template_source.exists():
        print(f"错误: 模板源目录 {template_source} 不存在")
        return None
    
    # 复制模板源目录中的所有文件和目录
    for item in template_source.iterdir():
        # 跳过临时目录和输出目录
        if item.name in ["temp_template", "templates", "__pycache__", ".git"]:
            continue
            
        # 跳过Python字节码文件
        if item.name.endswith(".pyc"):
            continue
            
        dest_item = temp_dir / item.name
        try:
            if item.is_dir():
                shutil.copytree(item, dest_item, dirs_exist_ok=True)
                print(f"已复制目录: {item.name}")
            elif item.is_file():
                shutil.copy2(item, dest_item)
                print(f"已复制文件: {item.name}")
        except Exception as e:
            print(f"复制 {item.name} 时出错: {e}")
    
    # 替换engine目录中的核心文件
    engine_dir = temp_dir / "engine"
    if not engine_dir.exists():
        engine_dir.mkdir(exist_ok=True)
    
    # 复制Godot核心文件（从正确的源目录）
    source_path = Path(source_dir)
    core_files = ["godot.js", "godot.wasm", "godot.worker.js"]
    copied_files = 0
    for file in core_files:
        src_file = source_path / file
        dest_file = engine_dir / file
        if src_file.exists():
            try:
                shutil.copy2(src_file, dest_file)
                print(f"已复制核心文件: {file}")
                copied_files += 1
            except Exception as e:
                print(f"复制核心文件 {file} 时出错: {e}")
        else:
            print(f"警告: 核心文件 {file} 未在源目录中找到")
    
    # 如果没有复制任何核心文件，且engine目录为空，创建占位文件
    if copied_files == 0 and not any(engine_dir.iterdir()):
        print("未找到核心文件，创建占位文件...")
        try:
            (engine_dir / "godot.js").touch()
            (engine_dir / "godot.wasm").touch()
        except Exception as e:
            print(f"创建占位文件时出错: {e}")
    
    # 更新配置文件
    update_config_files(temp_dir, template_name)
    
    # 打包为ZIP文件
    template_filename = f"{template_name}.zip"
    template_path = Path(output_dir) / template_filename
    
    try:
        with zipfile.ZipFile(template_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    file_path = Path(root) / file
                    arc_path = file_path.relative_to(temp_dir)
                    zipf.write(file_path, arc_path)
    except Exception as e:
        print(f"打包ZIP文件时出错: {e}")
        return None
    
    # 清理临时目录
    try:
        shutil.rmtree(temp_dir, ignore_errors=True)
    except Exception as e:
        print(f"清理临时目录时出错: {e}")
    
    print(f"模板已创建: {template_path}")
    
    # 更新template.json
    update_template_json(template_name, template_filename, output_dir)
    
    return template_path


def update_config_files(template_dir, template_name):
    """更新配置文件以匹配新模板"""
    
    # 更新game.json
    game_json_path = template_dir / "game.json"
    if game_json_path.exists():
        try:
            with open(game_json_path, "r", encoding="utf-8") as f:
                game_json = json.load(f)
        except (json.JSONDecodeError, UnicodeDecodeError):
            game_json = {
                "deviceOrientation": "portrait"
            }
    else:
        game_json = {
            "deviceOrientation": "portrait"
        }
    
    # 更新项目属性
    game_json["deviceOrientation"] = "portrait"
    with open(game_json_path, "w", encoding="utf-8") as f:
        json.dump(game_json, f, ensure_ascii=False, indent=2)
    
    # 更新project.config.json
    project_config_path = template_dir / "project.config.json"
    if project_config_path.exists():
        try:
            with open(project_config_path, "r", encoding="utf-8") as f:
                project_config = json.load(f)
        except (json.JSONDecodeError, UnicodeDecodeError):
            project_config = {
                "appid": "touristappid",
                "projectname": "godot-wechat-template"
            }
    else:
        project_config = {
            "appid": "touristappid",
            "projectname": "godot-wechat-template"
        }
    
    project_config["projectname"] = f"godot-{template_name}"
    with open(project_config_path, "w", encoding="utf-8") as f:
        json.dump(project_config, f, ensure_ascii=False, indent=2)
    
    # 更新project.private.config.json
    private_config_path = template_dir / "project.private.config.json"
    if private_config_path.exists():
        try:
            with open(private_config_path, "r", encoding="utf-8") as f:
                private_config = json.load(f)
        except (json.JSONDecodeError, UnicodeDecodeError):
            private_config = {
                "projectname": "godot-wechat-template"
            }
    else:
        private_config = {
            "projectname": "godot-wechat-template"
        }
    
    private_config["projectname"] = f"godot-{template_name}"
    with open(private_config_path, "w", encoding="utf-8") as f:
        json.dump(private_config, f, ensure_ascii=False, indent=2)


def update_template_json(template_name, template_filename, output_dir="./templates"):
    """更新templates/template.json文件"""
    
    template_json_path = Path(output_dir) / "template.json"
    
    # 如果template.json不存在，创建一个新的
    if not template_json_path.exists():
        templates = []
    else:
        try:
            with open(template_json_path, "r", encoding="utf-8") as f:
                templates = json.load(f)
        except (json.JSONDecodeError, UnicodeDecodeError):
            templates = []
    
    # 检查是否已存在同名模板
    existing_template = None
    for i, template in enumerate(templates):
        if template.get("filename") == template_filename:
            existing_template = i
            break
    
    # 创建新的模板条目
    new_template = {
        "name": f"自定义 {template_name}",
        "filename": template_filename
    }
    
    # 更新或添加模板条目
    if existing_template is not None:
        templates[existing_template] = new_template
        print(f"已更新模板条目: {template_name}")
    else:
        templates.append(new_template)
        print(f"已添加新模板条目: {template_name}")
    
    # 写回文件
    with open(template_json_path, "w", encoding="utf-8") as f:
        json.dump(templates, f, ensure_ascii=False, indent=2)


def main():
    # 硬编码路径配置（一键启动）
    SOURCE_DIR = r"D:\Do\Githubs\godot\bin\web_4.6_full"  # Godot bin文件目录
    TEMPLATE_NAME = "4.6latest"  # 模板名称
    OUTPUT_DIR = r"D:\Do\Githubs\godot-love-wechat\templates"  # 输出目录
    
    print("使用硬编码路径配置:")
    print(f"源目录: {SOURCE_DIR}")
    print(f"模板名称: {TEMPLATE_NAME}")
    print(f"输出目录: {OUTPUT_DIR}")
    print("")
    
    # 检查源目录是否存在
    if not Path(SOURCE_DIR).exists():
        print(f"错误: 源目录 {SOURCE_DIR} 不存在")
        input("按回车键退出...")
        sys.exit(1)
    
    # 创建模板
    template_path = create_wechat_template(SOURCE_DIR, TEMPLATE_NAME, OUTPUT_DIR)
    
    if template_path:
        print(f"\n模板创建完成: {template_path}")
        print("现在可以在 @godot-minigame-template 工具中使用这个自定义模板了!")
    else:
        print("\n模板创建失败!")
    
    input("按回车键退出...")


if __name__ == "__main__":
    main()