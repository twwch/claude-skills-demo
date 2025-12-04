"""
示例：使用 Claude API 调用官方 PDF Skill
创建一个格式化的 PDF 报告
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


def create_pdf_report():
    """使用 pdf skill 创建 PDF 报告"""

    messages = [
        {
            "role": "user",
            "content": """创建一份 PDF 格式的月度报告：

            标题: 2025年11月运营报告

            1. 执行摘要
               - 本月核心指标概览
               - 关键成就

            2. 业务数据
               - 用户增长: 15%
               - 收入增长: 22%
               - 客户满意度: 4.5/5

            3. 重点项目进展
               - 项目A: 已完成 80%
               - 项目B: 已完成 60%
               - 项目C: 规划中

            4. 下月计划
               - 完成项目A
               - 推进项目B
               - 启动项目C

            5. 风险与挑战
               - 人员招聘进度
               - 技术债务处理

            请使用专业的 PDF 格式，包含页眉页脚。
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
                    {"type": "anthropic", "skill_id": "pdf", "version": "latest"}
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
                            file_content.write_to_file("monthly_report.pdf")
                            print(f"✅ PDF 文件已保存: monthly_report.pdf")

        # 检查是否需要继续
        if response.stop_reason == "end_turn":
            break

        # 将 assistant 响应加入消息历史，继续对话
        messages.append({"role": "assistant", "content": response.content})
        messages.append({"role": "user", "content": [{"type": "text", "text": "继续"}]})

    return response


if __name__ == "__main__":
    print("🚀 调用 Claude pdf Skill 创建 PDF 报告...")
    create_pdf_report()
