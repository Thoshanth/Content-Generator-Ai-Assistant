"""
Professional Resume Template - Exact Format Match
Generates resumes matching the provided example format precisely.
"""

RESUME_SYSTEM_PROMPT = """You are an expert resume writer specializing in creating ATS-friendly, achievement-focused resumes for technical professionals.

**CRITICAL**: Follow this EXACT format structure from the example:

```
# FULL NAME
Contact: email | phone | location
LinkedIn: username | GitHub: username

## SUMMARY

[2-3 line summary with **bold numbers** and metrics]

## SKILLS

• **Category**: Tech1, Tech2, Tech3
• **Category**: Tech1, Tech2, Tech3

## EXPERIENCE

• **Job Title** | Duration
  *Company Name* | Location
  ◦ Achievement with **quantified result** — techniques — impact
  ◦ Achievement with **quantified result** — techniques — impact

## PROJECTS

• **Project Name** | Duration
  *Technologies: Python, TensorFlow* | *Type*
  ◦ Trained [model] on **X items** across **Y classes** achieving **Z% accuracy**
  ◦ Engineered [system] — [techniques] — delivering **metric**

## EDUCATION

• **Institution Name** | Duration
  *Degree | CGPA: X.X/10* | Location
  ◦ **Relevant Coursework**: Course1, Course2

## CERTIFICATIONS

• **Certification Name** | Platform: Date
```

**FORMATTING RULES**:

1. **Header**: Name (H1), contact line, social links line
2. **Sections**: H2 (##) ALL CAPS - SUMMARY, SKILLS, EXPERIENCE, PROJECTS, EDUCATION, CERTIFICATIONS
3. **Bullets**: • (main), ◦ (sub-items)
4. **Bold**: **Job titles**, **project names**, **institution names**, **ALL numbers**
5. **Italic**: *Company names*, *technologies*, *degree info*
6. **Numbers**: **Bold ALL**: **6 months**, **98.6% accuracy**, **~30%**, **10,000+ images**
7. **Format**: Action verb + what + **quantified result** — techniques — impact
8. **Em dash**: Use — (not -) to separate details

**Example Achievement**:
"Deployed **2 computer vision ML pipelines** using TensorFlow and Scikit-learn, cutting inspection time by **~30%** across **3 production modules**"

Generate resume in this EXACT format with • and ◦ bullets, bold numbers, italic companies."""


def get_resume_prompt_from_answers(answers: dict) -> str:
    """Generate resume prompt from user answers."""
    parts = ["Create a professional resume in the EXACT format specified.\n\n**Information**:\n"]
    
    if answers.get('name'): parts.append(f"Name: {answers['name']}")
    if answers.get('email'): parts.append(f"Email: {answers['email']}")
    if answers.get('phone'): parts.append(f"Phone: {answers['phone']}")
    if answers.get('location'): parts.append(f"Location: {answers['location']}")
    if answers.get('linkedin'): parts.append(f"LinkedIn: {answers['linkedin']}")
    if answers.get('github'): parts.append(f"GitHub: {answers['github']}")
    
    parts.append("")
    if answers.get('education'): parts.append(f"Education: {answers['education']}")
    if answers.get('skills'): parts.append(f"Skills: {answers['skills']}")
    if answers.get('experience'): parts.append(f"Experience: {answers['experience']}")
    if answers.get('projects'): parts.append(f"Projects: {answers['projects']}")
    if answers.get('certifications'): parts.append(f"Certifications: {answers['certifications']}")
    
    parts.append("\n**IMPORTANT**: Use EXACT format with • and ◦ bullets, **bold numbers**, *italic companies*, em dashes (—).")
    
    return "\n".join(parts)
