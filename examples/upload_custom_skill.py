"""
上传/更新自定义 Skill 到 Anthropic API
"""
import os
import sys
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get("ANTHROPIC_API_KEY")
BASE_URL = "https://api.anthropic.com/v1/skills"


def upload_skill(skill_dir: str, display_title: str) -> dict:
    """上传新的自定义 Skill"""
    skill_path = Path(skill_dir)

    files_to_upload = []
    for file_path in skill_path.rglob("*"):
        if file_path.is_file():
            relative_path = file_path.relative_to(skill_path.parent)
            files_to_upload.append(
                ("files[]", (str(relative_path), open(file_path, "rb")))
            )

    headers = {
        "x-api-key": API_KEY,
        "anthropic-version": "2023-06-01",
        "anthropic-beta": "skills-2025-10-02",
    }

    response = requests.post(
        BASE_URL,
        headers=headers,
        data={"display_title": display_title},
        files=files_to_upload,
    )

    for _, (_, f) in files_to_upload:
        f.close()

    response.raise_for_status()
    return response.json()


def update_skill(skill_id: str, skill_dir: str) -> dict:
    """更新已有的自定义 Skill（创建新版本）"""
    skill_path = Path(skill_dir)

    files_to_upload = []
    for file_path in skill_path.rglob("*"):
        if file_path.is_file():
            relative_path = file_path.relative_to(skill_path.parent)
            files_to_upload.append(
                ("files[]", (str(relative_path), open(file_path, "rb")))
            )

    headers = {
        "x-api-key": API_KEY,
        "anthropic-version": "2023-06-01",
        "anthropic-beta": "skills-2025-10-02",
    }

    # POST to /v1/skills/{skill_id}/versions 创建新版本
    response = requests.post(
        f"{BASE_URL}/{skill_id}/versions",
        headers=headers,
        files=files_to_upload,
    )

    for _, (_, f) in files_to_upload:
        f.close()

    response.raise_for_status()
    return response.json()


def list_skills() -> dict:
    """列出所有 Skills"""
    headers = {
        "x-api-key": API_KEY,
        "anthropic-version": "2023-06-01",
        "anthropic-beta": "skills-2025-10-02",
    }
    response = requests.get(BASE_URL, headers=headers)
    response.raise_for_status()
    return response.json()


def get_skill(skill_id: str) -> dict:
    """获取 Skill 详情"""
    headers = {
        "x-api-key": API_KEY,
        "anthropic-version": "2023-06-01",
        "anthropic-beta": "skills-2025-10-02",
    }
    response = requests.get(f"{BASE_URL}/{skill_id}", headers=headers)
    response.raise_for_status()
    return response.json()


def main():
    skill_dir = Path(__file__).parent.parent / "custom_skills" / "resume-gen"
    skill_id = "skill_01YAhbM32hbu6grvV1MLnssA"  # 已上传的 skill_id

    # 检查命令行参数
    if len(sys.argv) > 1 and sys.argv[1] == "update":
        # 更新模式
        print(f"🔄 更新 Skill: {skill_id}")
        print(f"   目录: {skill_dir}")
        print()

        try:
            result = update_skill(skill_id, str(skill_dir))
            print("✅ 更新成功!")
            print(f"   新版本: {result.get('version')}")
        except requests.exceptions.HTTPError as e:
            print(f"❌ 更新失败: {e}")
            if e.response:
                print(f"   响应: {e.response.text}")
            return
    else:
        # 上传新 Skill 模式
        print("📤 上传自定义 Skill: resume-gen")
        print(f"   目录: {skill_dir}")
        print()

        try:
            result = upload_skill(str(skill_dir), "Resume Generator")
            print("✅ 上传成功!")
            print(f"   ID: {result.get('id')}")
            print(f"   Version: {result.get('latest_version')}")
            print()
            print(f"📝 在 use_custom_skill.py 中使用这个 ID: {result.get('id')}")
        except requests.exceptions.HTTPError as e:
            print(f"❌ 上传失败: {e}")
            if e.response:
                print(f"   响应: {e.response.text}")
            return

    # 列出所有 skills
    print("\n📋 当前所有 Skills:")
    try:
        skills = list_skills()
        for skill in skills.get("data", []):
            source = "官方" if skill.get('source') == 'anthropic' else "自定义"
            print(f"   - {skill.get('id')} ({source})")
    except Exception as e:
        print(f"   获取列表失败: {e}")


if __name__ == "__main__":
    main()
