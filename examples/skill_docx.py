"""
示例：使用 Claude API 调用官方 Word (docx) Skill
创建一个格式化的文档
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


def create_document():
    """使用 docx skill 创建 Word 文档"""

    messages = [
        {
            "role": "user",
            "content": """创建一份项目提案文档，包含：

            1. 标题: "智能客服系统项目提案"

            2. 项目背景 (一段描述)

            3. 项目目标 (列表形式):
               - 提升客户满意度
               - 降低人工成本
               - 24小时服务覆盖

            4. 技术方案:
               - 使用大语言模型
               - 知识库检索增强
               - 多轮对话管理

            5. 项目里程碑 (表格形式):
               | 阶段 | 时间 | 交付物 |
               | 需求分析 | 2周 | 需求文档 |
               | 系统设计 | 3周 | 设计文档 |
               | 开发测试 | 8周 | 系统原型 |
               | 上线部署 | 2周 | 正式系统 |

            6. 预算概览

            请使用专业的文档格式。
            """
        }
    ]

    # Agentic loop: 持续处理直到任务完成
    while True:
        response = client.beta.messages.create(
            model="claude-3-7-sonnet-20250219",
            max_tokens=16000,
            betas=BETAS,
            container={
                "skills": [
                    {"type": "anthropic", "skill_id": "docx", "version": "latest"}
                ]
            },
            tools=[
                {"type": "code_execution_20250825", "name": "code_execution"}
            ],
            messages=messages,
        )

        # 处理响应内容
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
                            file_content.write_to_file("project_proposal.docx")
                            print(f"✅ Word 文件已保存: project_proposal.docx")

        # 检查是否需要继续
        if response.stop_reason == "end_turn":
            break

        # 将 assistant 响应加入消息历史，继续对话
        messages.append({"role": "assistant", "content": response.content})
        messages.append({"role": "user", "content": [{"type": "text", "text": "继续"}]})

    return response


if __name__ == "__main__":
    print("🚀 调用 Claude docx Skill 创建 Word 文档...")
    create_document()
