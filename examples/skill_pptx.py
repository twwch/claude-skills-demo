"""
示例：使用 Claude API 调用官方 PowerPoint (pptx) Skill
创建一个简单的演示文稿
"""
from dotenv import load_dotenv
from anthropic import Anthropic

# 从 .env 文件加载环境变量
load_dotenv()

client = Anthropic()

BETAS = [
    "code-execution-2025-08-25",
    "skills-2025-10-02",
    "files-api-2025-04-14",
]


def create_presentation():
    """使用 pptx skill 创建 PowerPoint 演示文稿"""

    response = client.beta.messages.create(
        model="claude-3-7-sonnet-20250219",
        max_tokens=16000,
        betas=BETAS,
        container={
            "skills": [
                {"type": "anthropic", "skill_id": "pptx", "version": "latest"}
            ]
        },
        tools=[
            {"type": "code_execution_20250825", "name": "code_execution"}
        ],
        messages=[
            {
                "role": "user",
                "content": """创建一个关于 "测试的 ppt" 的 PowerPoint 演示文稿：

                幻灯片 1: 标题页
                - 标题: 测试的 ppt
                - 副标题: 测试的 ppt
                """
            }
        ],
    )

    # 提取 file_id 并下载文件
    for block in response.content:
        if block.type == "text":
            print(f"Claude: {block.text}")

        # 从 bash_code_execution_tool_result 中提取 file_id
        if hasattr(block, "content") and hasattr(block.content, "content"):
            inner_content = block.content.content
            if isinstance(inner_content, list):
                for item in inner_content:
                    if hasattr(item, "file_id") and item.file_id:
                        file_id = item.file_id
                        file_content = client.beta.files.download(
                            file_id=file_id,
                            betas=["files-api-2025-04-14"]
                        )
                        file_content.write_to_file("output.pptx")
                        print(f"✅ 文件已保存: output.pptx")

    return response


if __name__ == "__main__":
    print("🚀 调用 Claude pptx Skill 创建演示文稿...")
    create_presentation()
