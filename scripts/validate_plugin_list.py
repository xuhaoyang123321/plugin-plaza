import json
from pathlib import Path
from typing import Dict, Union

from pydantic import BaseModel, ValidationError, RootModel


class PluginInfo(BaseModel):
    name: str
    description: str
    version: str
    plugin_ver: int
    author: str
    url: str
    branch: str
    update_date: str
    tag: str


class PluginRegistry(RootModel):
    root: Dict[str, PluginInfo]


def validate_plugin_list(file_path: str) -> bool:
    """验证插件列表文件

    Args:
        file_path: 要验证的 JSON 文件路径

    Returns:
        bool: 验证结果（True=通过，False=失败）
    """
    try:
        # 解析文件路径
        path = Path(file_path)

        # 检查文件是否存在
        if not path.exists():
            print(f"❌ 错误：文件 {path.resolve()} 不存在")
            return False

        # 读取并解析 JSON
        with open(path, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)

        # 执行 Pydantic 验证
        PluginRegistry.model_validate(raw_data)

        print(f"✅ 文件 {path.name} 验证通过")
        return True

    except json.JSONDecodeError as e:
        print(f"❌ JSON 格式错误：{e}")
        return False

    except ValidationError as e:
        print(f"❌ 数据验证失败：")
        print(e.json(indent=2))
        return False

    except Exception as e:
        print(f"❌ 发生意外错误：{str(e)}")
        return False


if __name__ == "__main__":
    # 要验证的文件路径（根据实际情况修改）
    target_file = "Plugins/plugin_list.json"

    # 执行验证
    validation_result = validate_plugin_list(target_file)

    # 根据验证结果返回系统退出码
    exit(0 if validation_result else 1)
