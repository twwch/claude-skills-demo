"""
示例：使用自定义 Skill (resume-gen) 生成简历
上传 Skill 后，在 container.skills 中引用即可使用
"""
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

client = Anthropic()

BETAS = [
    "code-execution-2025-08-25",
    "skills-2025-10-02",
    "files-api-2025-04-14",
]

# 上传后获得的 skill_id（运行 upload_custom_skill.py 后填入）
CUSTOM_SKILL_ID = "skill_01YAhbM32hbu6grvV1MLnssA"


def generate_resume(user_info: str):
    """使用自定义 Skill 生成简历"""

    messages = [
        {
            "role": "user",
            "content": f"""请根据以下信息帮我生成一份专业的简历 PDF：

{user_info}

请使用 modern 风格，生成文件名为 my_resume.pdf
"""
        }
    ]

    # Agentic loop
    while True:
        response = client.beta.messages.create(
            model="claude-3-7-sonnet-20250219",
            max_tokens=16000,
            betas=BETAS,
            container={
                "skills": [
                    # 使用自定义 Skill
                    {"type": "custom", "skill_id": CUSTOM_SKILL_ID, "version": "latest"}
                ]
            },
            tools=[
                {"type": "code_execution_20250825", "name": "code_execution"}
            ],
            messages=messages,
        )

        # 处理响应
        for block in response.content:
            if block.type == "text":
                print(f"Claude: {block.text}")

            # 提取生成的 PDF 文件
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
                            filename = "my_resume.pdf"
                            # 尝试从 stdout 提取文件名
                            if hasattr(block.content, "stdout") and block.content.stdout:
                                import re
                                matches = re.findall(r'([\w\-_]+\.pdf)', block.content.stdout)
                                if matches:
                                    filename = matches[-1]
                            file_content.write_to_file(filename)
                            print(f"✅ 简历已保存: {filename}")

        if response.stop_reason == "end_turn":
            break

        messages.append({"role": "assistant", "content": response.content})
        messages.append({"role": "user", "content": [{"type": "text", "text": "继续"}]})

    return response


if __name__ == "__main__":
    print("📝 使用自定义 Skill 生成简历\n")

    user_info = """
姓名：张三
职位：高级前端工程师
邮箱：zhangsan@example.com
电话：138-0000-0000
地址：北京市朝阳区

工作经历：
1. 字节跳动 - 高级前端工程师 (2021-01 至今)
   - 负责抖音创作者平台前端架构设计
   - 主导性能优化项目，首屏加载时间降低 40%
   - 搭建前端监控体系，覆盖 100+ 页面

2. 阿里巴巴 - 前端工程师 (2018-07 至 2020-12)
   - 参与淘宝商家后台开发
   - 开发可视化搭建平台，提升运营效率 50%

教育背景：
北京邮电大学 - 计算机科学与技术 本科 (2014-2018)

技能：
- 前端：React, Vue, TypeScript, Webpack
- 后端：Node.js, Python
- 工具：Git, Docker, CI/CD
"""

    generate_resume(user_info)
