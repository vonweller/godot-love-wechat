# 自定义Godot Web导出模板转换为微信小游戏模板指南

## 脚本功能

`convert_template.py` 脚本可以将你自己编译的Godot Web导出模板自动转换为适用于微信小游戏的模板，并集成到 `@godot-minigame-template` 项目中。

## 使用方法

### 1. 一键启动模式（推荐）

直接双击运行脚本或在命令行中执行：

```bash
python convert_template.py
```

脚本使用硬编码的路径配置，无需任何输入：
- 源目录：`D:\Do\Githubs\godot\bin`（Godot编译输出目录）
- 模板名称：`4.6latest`
- 输出目录：`D:\Do\Githubs\godot-love-wechat\templates`

### 2. 命令行参数模式

```bash
python convert_template.py <source_dir> <template_name>
```

参数说明：
- `source_dir`: 包含你自定义Godot Web导出文件的目录
- `template_name`: 生成的模板名称

### 3. 示例

假设你编译的Godot文件位于 `./my_godot_build/` 目录中：

```bash
python convert_template.py ./my_godot_build my_custom_template
```

这将会：
1. 创建一个名为 `my_custom_template.zip` 的模板文件
2. 自动放置在 `./templates/` 目录中
3. 更新 `templates/template.json` 配置文件

### 4. 高级选项

```bash
# 指定输出目录
python convert_template.py ./my_godot_build my_custom_template --output-dir ./custom_templates

# 启用brotli压缩（需要安装brotli库）
python convert_template.py ./my_godot_build my_custom_template --compress
```

## 安装依赖

如果要使用压缩功能，需要安装brotli库：

```bash
pip install brotli
```

## 脚本工作原理

1. **文件复制**：从源目录复制核心文件（godot.js, godot.wasm等）
2. **目录结构创建**：建立符合微信小游戏要求的目录结构
3. **配置文件生成**：创建必要的配置文件（game.json等）
4. **适配脚本集成**：复制微信小游戏适配所需的JS文件
5. **模板打包**：将所有文件打包为ZIP格式
6. **配置更新**：自动更新模板配置文件

## 注意事项

1. **适配文件**：确保 `js/` 目录中的适配脚本是最新的
2. **编译选项**：你的Godot编译应包含微信小游戏所需的适配选项
3. **文件同步**：脚本会保留原有的文件系统同步机制
4. **分包支持**：生成的模板支持微信小游戏的分包功能

## 压缩功能说明

根据项目RoadMap，计划支持pck文件的brotli压缩与加载。当前脚本提供了基础的brotli压缩功能，但完整集成还需要进一步开发。

## 在工具中使用自定义模板

转换完成后，在 `@godot-minigame-template` 工具中：

1. 启动工具并进入设置页面
2. 选择你的自定义模板（会显示为"自定义 4.6latest"）
3. 正常导出项目即可使用你的自定义模板