#!/usr/bin/env python3
"""
Resume PDF Generator using ReportLab
Supports multiple styles: modern, classic, minimal
"""
import sys
import json
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm, cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, ListFlowable, ListItem
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Try to register Chinese fonts - search multiple possible paths
CHINESE_FONT = 'Helvetica'
CHINESE_FONT_BOLD = 'Helvetica-Bold'

FONT_PATHS = [
    # Linux paths
    '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',
    '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc',
    '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
    '/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc',
    '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
    # More Linux paths
    '/usr/share/fonts/truetype/arphic/uming.ttc',
    '/usr/share/fonts/truetype/arphic/ukai.ttc',
    # Noto fonts (commonly available)
    '/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc',
    '/usr/share/fonts/google-noto-cjk/NotoSansCJK-Regular.ttc',
]

for font_path in FONT_PATHS:
    if Path(font_path).exists():
        try:
            pdfmetrics.registerFont(TTFont('ChineseFont', font_path))
            CHINESE_FONT = 'ChineseFont'
            CHINESE_FONT_BOLD = 'ChineseFont'  # Same font for bold (will simulate with style)
            break
        except Exception:
            continue

# Color schemes for different styles
STYLES = {
    'modern': {
        'primary': colors.HexColor('#2563eb'),
        'secondary': colors.HexColor('#1e40af'),
        'text': colors.HexColor('#1f2937'),
        'light': colors.HexColor('#6b7280'),
        'accent': colors.HexColor('#3b82f6'),
    },
    'classic': {
        'primary': colors.HexColor('#1f2937'),
        'secondary': colors.HexColor('#374151'),
        'text': colors.HexColor('#111827'),
        'light': colors.HexColor('#6b7280'),
        'accent': colors.HexColor('#4b5563'),
    },
    'minimal': {
        'primary': colors.HexColor('#000000'),
        'secondary': colors.HexColor('#333333'),
        'text': colors.HexColor('#000000'),
        'light': colors.HexColor('#666666'),
        'accent': colors.HexColor('#999999'),
    }
}


class ResumeGenerator:
    def __init__(self, data: dict, style: str = 'modern'):
        self.data = data
        self.style_name = style
        self.colors = STYLES.get(style, STYLES['modern'])
        self.elements = []
        self._setup_styles()

    def _setup_styles(self):
        """Setup paragraph styles with Chinese font support"""
        self.styles = getSampleStyleSheet()

        # Name style
        self.styles.add(ParagraphStyle(
            'Name',
            parent=self.styles['Heading1'],
            fontName=CHINESE_FONT,
            fontSize=24,
            textColor=self.colors['primary'],
            spaceAfter=2*mm,
            alignment=TA_CENTER if self.style_name == 'modern' else TA_LEFT,
        ))

        # Title style
        self.styles.add(ParagraphStyle(
            'Title2',
            parent=self.styles['Normal'],
            fontName=CHINESE_FONT,
            fontSize=12,
            textColor=self.colors['light'],
            spaceAfter=3*mm,
            alignment=TA_CENTER if self.style_name == 'modern' else TA_LEFT,
        ))

        # Section header
        self.styles.add(ParagraphStyle(
            'SectionHeader',
            parent=self.styles['Heading2'],
            fontName=CHINESE_FONT,
            fontSize=14,
            textColor=self.colors['primary'],
            spaceBefore=5*mm,
            spaceAfter=3*mm,
            borderPadding=(0, 0, 2, 0),
        ))

        # Company/Institution
        self.styles.add(ParagraphStyle(
            'Company',
            parent=self.styles['Normal'],
            fontName=CHINESE_FONT,
            fontSize=11,
            textColor=self.colors['text'],
        ))

        # Job title
        self.styles.add(ParagraphStyle(
            'JobTitle',
            parent=self.styles['Normal'],
            fontName=CHINESE_FONT,
            fontSize=10,
            textColor=self.colors['secondary'],
        ))

        # Date style
        self.styles.add(ParagraphStyle(
            'Date',
            parent=self.styles['Normal'],
            fontName=CHINESE_FONT,
            fontSize=9,
            textColor=self.colors['light'],
            alignment=TA_RIGHT,
        ))

        # Bullet point
        self.styles.add(ParagraphStyle(
            'Bullet',
            parent=self.styles['Normal'],
            fontName=CHINESE_FONT,
            fontSize=10,
            textColor=self.colors['text'],
            leftIndent=5*mm,
            spaceBefore=1*mm,
        ))

        # Contact info
        self.styles.add(ParagraphStyle(
            'Contact',
            parent=self.styles['Normal'],
            fontName=CHINESE_FONT,
            fontSize=9,
            textColor=self.colors['light'],
            alignment=TA_CENTER if self.style_name == 'modern' else TA_LEFT,
        ))

        # Summary
        self.styles.add(ParagraphStyle(
            'Summary',
            parent=self.styles['Normal'],
            fontName=CHINESE_FONT,
            fontSize=10,
            textColor=self.colors['text'],
            spaceAfter=3*mm,
            leading=14,
        ))

    def _add_header(self):
        """Add name and contact info"""
        header = self.data.get('header', {})

        # Name
        if header.get('name'):
            self.elements.append(Paragraph(header['name'], self.styles['Name']))

        # Title
        if header.get('title'):
            self.elements.append(Paragraph(header['title'], self.styles['Title2']))

        # Contact info line
        contact_parts = []
        if header.get('email'):
            contact_parts.append(header['email'])
        if header.get('phone'):
            contact_parts.append(header['phone'])
        if header.get('location'):
            contact_parts.append(header['location'])

        if contact_parts:
            self.elements.append(Paragraph(' | '.join(contact_parts), self.styles['Contact']))

        # Links line
        link_parts = []
        if header.get('linkedin'):
            link_parts.append(header['linkedin'])
        if header.get('github'):
            link_parts.append(header['github'])

        if link_parts:
            self.elements.append(Paragraph(' | '.join(link_parts), self.styles['Contact']))

        self.elements.append(Spacer(1, 5*mm))

        # Divider line
        if self.style_name != 'minimal':
            self.elements.append(HRFlowable(
                width="100%",
                thickness=1,
                color=self.colors['accent'],
                spaceAfter=3*mm
            ))

    def _add_section_header(self, title: str):
        """Add section header with optional underline"""
        self.elements.append(Paragraph(title, self.styles['SectionHeader']))
        if self.style_name == 'classic':
            self.elements.append(HRFlowable(
                width="100%",
                thickness=0.5,
                color=self.colors['light'],
                spaceAfter=2*mm
            ))

    def _add_summary(self):
        """Add professional summary"""
        if self.data.get('summary'):
            self._add_section_header('专业概述' if self._is_chinese() else 'Summary')
            self.elements.append(Paragraph(self.data['summary'], self.styles['Summary']))

    def _add_experience(self):
        """Add work experience section"""
        experience = self.data.get('experience', [])
        if not experience:
            return

        self._add_section_header('工作经历' if self._is_chinese() else 'Experience')

        for job in experience:
            # Company and dates on same line
            company_text = f"<b>{job.get('company', '')}</b>"
            if job.get('location'):
                company_text += f" - {job['location']}"

            date_text = f"{job.get('start_date', '')} - {job.get('end_date', '')}"

            # Use table for company/date alignment
            data = [[
                Paragraph(company_text, self.styles['Company']),
                Paragraph(date_text, self.styles['Date'])
            ]]
            t = Table(data, colWidths=['70%', '30%'])
            t.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (0, 0), (-1, -1), 0),
                ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ]))
            self.elements.append(t)

            # Job title
            if job.get('title'):
                self.elements.append(Paragraph(job['title'], self.styles['JobTitle']))

            # Highlights
            for highlight in job.get('highlights', []):
                self.elements.append(Paragraph(f"• {highlight}", self.styles['Bullet']))

            self.elements.append(Spacer(1, 3*mm))

    def _add_education(self):
        """Add education section"""
        education = self.data.get('education', [])
        if not education:
            return

        self._add_section_header('教育背景' if self._is_chinese() else 'Education')

        for edu in education:
            # Institution and dates
            data = [[
                Paragraph(f"<b>{edu.get('institution', '')}</b>", self.styles['Company']),
                Paragraph(f"{edu.get('start_date', '')} - {edu.get('end_date', '')}", self.styles['Date'])
            ]]
            t = Table(data, colWidths=['70%', '30%'])
            t.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (0, 0), (-1, -1), 0),
                ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ]))
            self.elements.append(t)

            # Degree
            degree_text = edu.get('degree', '')
            if edu.get('gpa'):
                degree_text += f" | GPA: {edu['gpa']}"
            self.elements.append(Paragraph(degree_text, self.styles['JobTitle']))

            self.elements.append(Spacer(1, 2*mm))

    def _add_skills(self):
        """Add skills section"""
        skills = self.data.get('skills', {})
        if not skills:
            return

        self._add_section_header('专业技能' if self._is_chinese() else 'Skills')

        if isinstance(skills, dict):
            for category, skill_list in skills.items():
                skill_text = f"<b>{category}:</b> {', '.join(skill_list)}"
                self.elements.append(Paragraph(skill_text, self.styles['Bullet']))
        elif isinstance(skills, list):
            self.elements.append(Paragraph(', '.join(skills), self.styles['Summary']))

        self.elements.append(Spacer(1, 2*mm))

    def _add_projects(self):
        """Add projects section"""
        projects = self.data.get('projects', [])
        if not projects:
            return

        self._add_section_header('项目经验' if self._is_chinese() else 'Projects')

        for project in projects:
            self.elements.append(Paragraph(f"<b>{project.get('name', '')}</b>", self.styles['Company']))
            if project.get('description'):
                self.elements.append(Paragraph(project['description'], self.styles['JobTitle']))
            for highlight in project.get('highlights', []):
                self.elements.append(Paragraph(f"• {highlight}", self.styles['Bullet']))
            self.elements.append(Spacer(1, 2*mm))

    def _add_certifications(self):
        """Add certifications section"""
        certs = self.data.get('certifications', [])
        if not certs:
            return

        self._add_section_header('专业认证' if self._is_chinese() else 'Certifications')

        for cert in certs:
            cert_text = f"• <b>{cert.get('name', '')}</b>"
            if cert.get('date'):
                cert_text += f" ({cert['date']})"
            self.elements.append(Paragraph(cert_text, self.styles['Bullet']))

    def _add_languages(self):
        """Add languages section"""
        languages = self.data.get('languages', [])
        if not languages:
            return

        self._add_section_header('语言能力' if self._is_chinese() else 'Languages')

        lang_parts = [f"{l.get('language', '')}: {l.get('proficiency', '')}" for l in languages]
        self.elements.append(Paragraph(' | '.join(lang_parts), self.styles['Summary']))

    def _is_chinese(self) -> bool:
        """Check if resume content is primarily Chinese"""
        header = self.data.get('header', {})
        name = header.get('name', '')
        return any('\u4e00' <= c <= '\u9fff' for c in name)

    def generate(self, output_path: str):
        """Generate the PDF resume"""
        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=1.5*cm,
            bottomMargin=1.5*cm
        )

        # Build content
        self._add_header()
        self._add_summary()
        self._add_experience()
        self._add_education()
        self._add_skills()
        self._add_projects()
        self._add_certifications()
        self._add_languages()

        # Generate PDF
        doc.build(self.elements)
        return output_path


def main():
    if len(sys.argv) < 3:
        print("Error: Usage: python generate_resume.py <data.json> <output.pdf>")
        sys.exit(1)

    data_path = sys.argv[1]
    output_path = sys.argv[2]

    try:
        with open(data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        style = data.get('style', 'modern')
        generator = ResumeGenerator(data, style)
        generator.generate(output_path)
        print(f"Resume generated: {output_path}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
