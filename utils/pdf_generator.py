import io
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from typing import Dict, List, Any

def generate_pdf_report(
    candidate_name: str,
    contact_info: Dict[str, Any],
    ats_results: Dict[str, Any],
    recommender_results: Dict[str, Any]
) -> bytes:
    """
    Generate a highly professional, well-styled PDF report containing ATS analysis and job recommendations.
    Returns bytes to be downloaded directly.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )
    
    story = []
    
    # ----------------------------------------------------
    # Styles
    # ----------------------------------------------------
    styles = getSampleStyleSheet()
    
    # Define corporate color palette
    primary_color = colors.HexColor("#4F46E5") # Royal Indigo
    secondary_color = colors.HexColor("#0F172A") # Slate Dark
    text_color = colors.HexColor("#334155") # Muted Charcoal
    light_bg = colors.HexColor("#F8FAFC") # Soft grey
    border_color = colors.HexColor("#E2E8F0") # Light grey border
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=primary_color,
        spaceAfter=6
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#64748B"),
        spaceAfter=15
    )
    
    section_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=secondary_color,
        spaceBefore=12,
        spaceAfter=8,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=text_color,
        spaceAfter=6
    )
    
    bold_body_style = ParagraphStyle(
        'BoldBody',
        parent=body_style,
        fontName='Helvetica-Bold'
    )
    
    bullet_style = ParagraphStyle(
        'Bullet',
        parent=body_style,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=4
    )
    
    score_title_style = ParagraphStyle(
        'ScoreTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=32,
        leading=36,
        textColor=primary_color,
        alignment=1 # Centered
    )
    
    score_desc_style = ParagraphStyle(
        'ScoreDesc',
        parent=body_style,
        alignment=1 # Centered
    )
    
    # ----------------------------------------------------
    # Header Section
    # ----------------------------------------------------
    story.append(Paragraph(f"AI-Powered Resume Analysis Report", title_style))
    
    # Contact metadata line
    phone = contact_info.get('phone') or 'N/A'
    email = contact_info.get('email') or 'N/A'
    linkedin = 'LinkedIn: Yes' if contact_info.get('linkedin') else 'LinkedIn: No'
    github = 'GitHub: Yes' if contact_info.get('github') else 'GitHub: No'
    
    meta_str = f"<b>Candidate:</b> {candidate_name} &nbsp;|&nbsp; <b>Email:</b> {email} &nbsp;|&nbsp; <b>Phone:</b> {phone} &nbsp;|&nbsp; {linkedin} &nbsp;|&nbsp; {github}"
    story.append(Paragraph(meta_str, subtitle_style))
    story.append(Spacer(1, 10))
    
    # ----------------------------------------------------
    # Overall ATS Score Summary Card (Using a single-row Table)
    # ----------------------------------------------------
    overall_score = ats_results.get("overall_score", 0)
    
    score_card_data = [
        [
            Paragraph(f"{overall_score}/100", score_title_style),
            [
                Paragraph("<b>ATS COMPATIBILITY SCORE</b>", bold_body_style),
                Paragraph(f"Your resume matches <b>{overall_score}%</b> of standard enterprise application tracking parameters.", body_style),
                Paragraph("Category Prediction: <b>" + recommender_results.get("predicted_category", "N/A") + "</b>", body_style)
            ]
        ]
    ]
    
    score_table = Table(score_card_data, colWidths=[2.2*inch, 4.8*inch])
    score_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), light_bg),
        ('BOX', (0, 0), (-1, -1), 1, primary_color),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('LEFTPADDING', (0, 0), (0, 0), 8),
        ('RIGHTPADDING', (0, 0), (0, 0), 8),
        ('LEFTPADDING', (1, 0), (1, 0), 12),
        ('RIGHTPADDING', (1, 0), (1, 0), 15),
    ]))
    
    story.append(score_table)
    story.append(Spacer(1, 15))
    
    # ----------------------------------------------------
    # Section 1: Score Breakdown
    # ----------------------------------------------------
    story.append(Paragraph("ATS Scoring Breakdown", section_heading))
    
    # Build breakdown table rows
    breakdown_data = [
        [Paragraph("<b>Category</b>", bold_body_style), Paragraph("<b>Score</b>", bold_body_style), Paragraph("<b>Status</b>", bold_body_style)]
    ]
    
    for category_name, content in ats_results.get("breakdown", {}).items():
        cat_score = content.get("score", 0)
        cat_max = content.get("max", 0)
        
        # Format custom status details based on content details
        details = content.get("details", {})
        status_str = ""
        if category_name == "Section Completeness":
            found = [k for k, v in details.items() if v]
            status_str = f"Found {len(found)}/5 key sections."
        elif category_name == "Skill Density":
            status_str = f"Extracted {details.get('count', 0)} skills ({details.get('status', '')})."
        elif category_name == "Resume Length":
            status_str = f"Length: {details.get('word_count', 0)} words ({details.get('status', '')})."
        elif category_name == "Formatting & Verbs":
            status_str = f"Verbs: {details.get('Action Verbs Found', 0)} strong verbs."
            
        breakdown_data.append([
            Paragraph(category_name, body_style),
            Paragraph(f"{cat_score} / {cat_max}", body_style),
            Paragraph(status_str, body_style)
        ])
        
    breakdown_table = Table(breakdown_data, colWidths=[2.2*inch, 1.3*inch, 3.5*inch])
    breakdown_table.setStyle(TableStyle([
        ('LINEBELOW', (0, 0), (-1, 0), 1.5, secondary_color),
        ('LINEBELOW', (0, 1), (-1, -1), 0.5, border_color),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(breakdown_table)
    story.append(Spacer(1, 15))
    
    # ----------------------------------------------------
    # Section 2: Actionable Improvements (Keep Together)
    # ----------------------------------------------------
    improvements = []
    improvements.append(Paragraph("ATS Actionable Recommendations", section_heading))
    for rec in ats_results.get("recommendations", []):
        # Strip markdown bolding inside paragraph for clean printing
        clean_rec = rec.replace("**", "")
        improvements.append(Paragraph(f"&bull; {clean_rec}", bullet_style))
        
    story.append(KeepTogether(improvements))
    story.append(Spacer(1, 15))
    
    # ----------------------------------------------------
    # Section 3: Recommended Roles & Career Pathways (Keep Together)
    # ----------------------------------------------------
    roles_story = []
    roles_story.append(Paragraph("Job Recommendations & Skill Gap Analysis", section_heading))
    
    top_recs = recommender_results.get("top_recommendations", [])[:2] # Print top 2 recommendations
    for idx, rec in enumerate(top_recs):
        role_title = rec.get("role")
        match_pct = rec.get("match_percentage")
        missing_skills = rec.get("missing_skills", [])
        matching_skills = rec.get("matching_skills", [])
        
        roles_story.append(Paragraph(f"<b>{idx+1}. {role_title}</b> (Compatibility Match: <b>{match_pct}%</b>)", bold_body_style))
        roles_story.append(Paragraph(rec.get("description", ""), body_style))
        
        # Render matching and missing skills
        matched_str = ", ".join(matching_skills) if matching_skills else "None"
        missing_str = ", ".join(missing_skills[:10]) if missing_skills else "None" # Limit to 10 for print
        
        roles_story.append(Paragraph(f"<b>Extracted Matching Skills:</b> <font color='#10B981'>{matched_str}</font>", bullet_style))
        roles_story.append(Paragraph(f"<b>Skill Gaps (Missing):</b> <font color='#EF4444'>{missing_str}</font>", bullet_style))
        
        # Add recommended learning path summary
        paths = recommender_results.get("learning_paths", {}).get(role_title, [])
        if paths:
            roles_story.append(Paragraph("<b>Recommended Next Steps / Roadmap:</b>", bold_body_style))
            for path in paths[:3]: # Show top 3 learning steps
                clean_path = path.replace("**", "") # Remove markdown formatting
                roles_story.append(Paragraph(f"&nbsp;&nbsp;&bull;&nbsp;{clean_path}", bullet_style))
                
        roles_story.append(Spacer(1, 10))
        
    story.append(KeepTogether(roles_story))
    
    # Build Document
    doc.build(story)
    
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes
