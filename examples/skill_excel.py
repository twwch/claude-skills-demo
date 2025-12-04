"""
示例：使用 Claude API 调用官方 Excel (xlsx) Skill
创建一个简单的销售数据表格
"""
from dotenv import load_dotenv
from anthropic import Anthropic

# 从 .env 文件加载环境变量
load_dotenv()

client = Anthropic()

# 必需的 beta headers
BETAS = [
    "code-execution-2025-08-25",
    "skills-2025-10-02",
    "files-api-2025-04-14",
]


def create_excel_report():
    """使用 xlsx skill 创建 Excel 报表"""

    messages = [
        {
            "role": "user",
            "content": """创建一个 Excel 销售报表，包含：
            1. 第一个工作表 "销售数据"：
               - 列：产品名称、数量、单价、总额
               - 5行示例数据
               - 总额列使用公式计算 (数量 * 单价)
               - 最后一行显示总计

            2. 第二个工作表 "统计"：
               - 显示总销售额
               - 显示平均单价
               - 使用公式引用第一个工作表的数据
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
                    {"type": "anthropic", "skill_id": "xlsx", "version": "latest"}
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
                            file_content.write_to_file("sales_report.xlsx")
                            print(f"✅ Excel 文件已保存: sales_report.xlsx")

        # 检查是否需要继续
        if response.stop_reason == "end_turn":
            break

        # 将 assistant 响应加入消息历史，继续对话
        messages.append({"role": "assistant", "content": response.content})
        messages.append({"role": "user", "content": [{"type": "text", "text": "继续"}]})

    return response


if __name__ == "__main__":
    print("🚀 调用 Claude xlsx Skill 创建 Excel 报表...")
    create_excel_report()
