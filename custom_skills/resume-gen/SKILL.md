---
name: resume-gen
description: |
  Use this skill to generate professional resume/CV PDFs based on user information.
  Triggers: user asks to "create a resume", "generate CV", "make a resume",
  "help me with my resume", or provides personal/professional information for a resume.
  Capabilities: Creates beautifully formatted PDF resumes with sections for
  contact info, summary, work experience, education, skills, projects, and more.
  Supports multiple styles: modern, classic, minimal.
---

# Resume Generator Skill

## Overview

This skill generates professional PDF resumes using ReportLab. It creates well-formatted,
ATS-friendly resumes that can be customized based on user preferences.

## Available Styles

1. **modern** - Clean design with accent colors, icons, and modern typography
2. **classic** - Traditional format, formal and conservative
3. **minimal** - Simple, lots of white space, focuses on content

## Resume Sections

The resume can include any of these sections:
- **Header**: Name, title, contact info (email, phone, location, LinkedIn, GitHub)
- **Summary**: Professional summary or objective (2-3 sentences)
- **Experience**: Work history with company, title, dates, and bullet points
- **Education**: Degrees, institutions, dates, GPA (optional)
- **Skills**: Technical and soft skills, can be grouped by category
- **Projects**: Personal or professional projects with descriptions
- **Certifications**: Professional certifications with dates
- **Languages**: Language proficiencies
- **Awards**: Honors and achievements

## How to Use

### Step 1: Gather Information

Ask the user for their resume information. At minimum, you need:
- Full name
- Contact information (email, phone)
- Work experience OR education

### Step 2: Generate the Resume

Use the provided Python script to generate the PDF:

```python
python /skills/resume-gen/generate_resume.py
```

The script reads resume data from a JSON file and outputs a PDF.

### Step 3: Create the Data File

Before running the script, create a JSON file with the resume data:

```python
import json

resume_data = {
    "style": "modern",  # modern, classic, or minimal
    "header": {
        "name": "张三",
        "title": "高级软件工程师",
        "email": "zhangsan@example.com",
        "phone": "+86 138-0000-0000",
        "location": "北京市",
        "linkedin": "linkedin.com/in/zhangsan",
        "github": "github.com/zhangsan"
    },
    "summary": "拥有8年软件开发经验的全栈工程师...",
    "experience": [
        {
            "company": "某科技公司",
            "title": "高级软件工程师",
            "location": "北京",
            "start_date": "2020-01",
            "end_date": "至今",
            "highlights": [
                "主导开发了公司核心交易系统，日处理交易量超过100万笔",
                "优化系统性能，响应时间降低60%",
                "带领5人团队完成微服务架构改造"
            ]
        }
    ],
    "education": [
        {
            "institution": "北京大学",
            "degree": "计算机科学与技术 学士",
            "start_date": "2012-09",
            "end_date": "2016-06",
            "gpa": "3.8/4.0"
        }
    ],
    "skills": {
        "编程语言": ["Python", "Java", "JavaScript", "Go"],
        "框架": ["Django", "Spring Boot", "React", "Vue.js"],
        "数据库": ["MySQL", "PostgreSQL", "MongoDB", "Redis"],
        "工具": ["Docker", "Kubernetes", "Git", "Jenkins"]
    },
    "projects": [
        {
            "name": "智能推荐系统",
            "description": "基于机器学习的个性化推荐引擎",
            "highlights": ["使用协同过滤算法", "日活用户超过50万"]
        }
    ],
    "certifications": [
        {"name": "AWS Solutions Architect", "date": "2023-05"}
    ],
    "languages": [
        {"language": "中文", "proficiency": "母语"},
        {"language": "英语", "proficiency": "流利"}
    ]
}

with open('/tmp/resume_data.json', 'w', encoding='utf-8') as f:
    json.dump(resume_data, f, ensure_ascii=False, indent=2)
```

Then run:
```bash
python /skills/resume-gen/generate_resume.py /tmp/resume_data.json /files/output/resume.pdf
```

## Output

The script outputs a PDF file. On success:
```
Resume generated: /files/output/resume.pdf
```

On error:
```
Error: <error message>
```

## Best Practices

1. **Keep it concise**: Aim for 1-2 pages maximum
2. **Quantify achievements**: Use numbers and metrics where possible
3. **Tailor to the job**: Highlight relevant experience
4. **Use action verbs**: Start bullet points with strong verbs
5. **Proofread**: Check for spelling and grammar errors
6. **Consistent formatting**: Dates, bullet styles should be uniform

## Limitations

- Maximum 2 pages recommended
- Images/photos not supported
- Limited to PDF output format
