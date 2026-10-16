from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import Color, black, red, white
import textwrap

def draw_wrapped_text(c, text, x, y, max_width, line_height=11, font_name="Times-Roman", font_size=9.5):
    """Helper to wrap and draw paragraphs cleanly."""
    c.setFont(font_name, font_size)
    words = text.split()
    lines = []
    current_line = []
    for word in words:
        test_line = " ".join(current_line + [word])
        if c.stringWidth(test_line, font_name, font_size) <= max_width:
            current_line.append(word)
        else:
            lines.append(" ".join(current_line))
            current_line = [word]
    if current_line:
        lines.append(" ".join(current_line))
    
    for line in lines:
        c.drawString(x, y, line)
        y -= line_height
    return y

def create_fillable_directive(output_filename="Advance_Health_Care_Directive_Fillable.pdf"):
    c = canvas.Canvas(output_filename, pagesize=letter)
    width, height = letter  # 612 x 792 points
    form = c.acroForm
    field_bg = Color(0.95, 0.97, 1.0, alpha=0.3)

    # =========================================================================
    # PAGE 1 (Formerly Page 2 of original scan - Main Directive Body)
    # =========================================================================
    margin_x = 70
    content_w = 472
    top_y = 755

    # Outer border matching original card margins
    c.setLineWidth(0.75)
    c.rect(margin_x - 8, 175, content_w + 16, 595)

    # Header
    c.setFont("Times-Bold", 15)
    c.drawCentredString(width / 2, top_y - 15, "Advance Health Care Directive")
    c.setFont("Times-Roman", 8.5)
    c.drawCentredString(width / 2, top_y - 27, "(California Probate Code §§ 4600 to 4806)")

    # Item 1 & Field A: Name
    y = top_y - 50
    c.setFont("Times-Roman", 9.5)
    c.drawString(margin_x, y, "1.  I,")
    c.line(margin_x + 24, y - 2, margin_x + 315, y - 2)
    
    form.textfield(
        name="Name",
        tooltip="Full Name (Print or Type)",
        x=margin_x + 25,
        y=y - 1,
        width=288,
        height=13,
        borderStyle="underlined",
        borderWidth=0,
        fillColor=field_bg,
        textColor=black,
        fontSize=10,
        forceBorder=False
    )
    
    c.drawString(margin_x + 318, y, "(print or type full name), fill out")
    y -= 12
    c.drawString(margin_x + 14, y, "this document to set forth my treatment instructions and to appoint a health-care agent in case of my incapacity.")

    # Item 2: Refusal of Transfusions Section
    y -= 20
    c.drawString(margin_x, y, "2.")
    y = draw_wrapped_text(
        c,
        "[Insert Clause 2 Directive Text: Direction that NO TRANSFUSIONS of whole blood, red cells, white cells, "
        "platelets, or plasma be given under any circumstances, and refusal to predonate or store blood for later infusion.]",
        margin_x + 14, y, content_w - 14, line_height=11.5
    )

    # Item 3: End-of-Life Matters
    y -= 8
    c.setFont("Times-Bold", 9.5)
    c.drawString(margin_x, y, "3.  Regarding end-of-life matters:")
    c.setFont("Times-Roman", 9.5)
    c.drawString(margin_x + 148, y, "[initial one of the two choices]")
    
    y -= 16
    c.drawString(margin_x + 14, y, "(a) _______")
    y = draw_wrapped_text(
        c,
        "[Choice A: Election not to prolong life if, to a reasonable degree of medical certainty, the situation is hopeless.]",
        margin_x + 65, y, content_w - 65, line_height=11.5
    )

    y -= 6
    c.drawString(margin_x + 14, y, "(b) _______")
    y = draw_wrapped_text(
        c,
        "[Choice B: Election for life to be prolonged as long as possible within generally accepted medical standards.]",
        margin_x + 65, y, content_w - 65, line_height=11.5
    )

    # Item 4 & Field B: MedicalConditions (6 lines free-form)
    y -= 10
    c.setFont("Times-Bold", 9.5)
    c.drawString(margin_x, y, "4.  Regarding other health-care instructions")
    c.setFont("Times-Roman", 9.5)
    c.drawString(margin_x + 190, y, "(medications, allergies, medical problems, or other wishes):")
    
    y -= 18
    line_spacing = 16
    med_top_y = y + 10
    for i in range(6):
        line_y = y - (i * line_spacing)
        c.line(margin_x + 14, line_y, margin_x + content_w, line_y)
    
    med_bottom_y = y - (5 * line_spacing)
    
    # 6-line Multiline Text Field (fieldFlags=4096 enables multiline in PDF spec)
    form.textfield(
        name="MedicalConditions",
        tooltip="Other Health-Care Instructions (6 Lines Free-Form)",
        x=margin_x + 14,
        y=med_bottom_y,
        width=content_w - 14,
        height=(med_top_y - med_bottom_y),
        borderWidth=0,
        fillColor=field_bg,
        textColor=black,
        fontSize=10,
        fieldFlags=4096,  # Multiline flag (1 << 12)
        forceBorder=False
    )

    # Item 5: Authority & Non-Override
    y = med_bottom_y - 18
    c.drawString(margin_x, y, "5.")
    y = draw_wrapped_text(
        c,
        "[Insert Clause 5 Text: No authority granted to disregard or override instructions set forth herein.]",
        margin_x + 14, y, content_w - 14, line_height=11.5
    )

    # Item 6: Appointment of Health-Care Agent
    y -= 8
    c.drawString(margin_x, y, "6.")
    y = draw_wrapped_text(
        c,
        "[Insert Clause 6 Text: Appointment of health-care agent and alternate agent with full power and authority to consent "
        "to or refuse treatment, consult doctors, receive medical records, and ensure wishes are honored.]",
        margin_x + 14, y, content_w - 14, line_height=11.5
    )

    # Signature & Date Lines
    y -= 22
    c.line(margin_x + 14, y, margin_x + 250, y)
    c.line(margin_x + 270, y, margin_x + 375, y)
    c.setFont("Times-Roman", 7.5)
    c.drawString(margin_x + 18, y - 9, "(Signature*)")
    c.drawString(margin_x + 275, y - 9, "(Date)")

    # Field C: PersonalAddress
    y -= 28
    c.line(margin_x + 14, y, margin_x + 375, y)
    c.drawString(margin_x + 18, y - 9, "(Address)")
    
    form.textfield(
        name="PersonalAddress",
        tooltip="Personal Address",
        x=margin_x + 14,
        y=y + 1,
        width=361,
        height=13,
        borderWidth=0,
        fillColor=field_bg,
        textColor=black,
        fontSize=10,
        forceBorder=False
    )

    # Statement of Witnesses Header
    y -= 22
    y = draw_wrapped_text(
        c,
        "STATEMENT OF WITNESSES: [Insert California Probate Code witness attestation paragraph regarding identity, "
        "presence, sound mind, non-agent status, and non-provider status...]",
        margin_x + 14, y, content_w - 14, line_height=10.5, font_size=8.8
    )

    c.setFont("Times-Roman", 8)
    c.drawCentredString(width / 2, 182, "Page 1 of 2")
    c.showPage()

    # =========================================================================
    # PAGE 2 (Formerly Page 1 of original scan - Witnesses & Agent Cards)
    # =========================================================================
    c.setLineWidth(0.75)
    c.rect(margin_x - 8, 175, content_w + 16, 595)

    y = top_y - 12
    y = draw_wrapped_text(
        c,
        "...[Continuation of Witness Attestation from Page 1 regarding community care and residential care facilities.]",
        margin_x + 6, y, content_w - 12, line_height=11, font_size=9
    )

    # Witness Signatures
    y -= 20
    col1_x = margin_x + 6
    col2_x = margin_x + 245
    col_w = 215

    c.line(col1_x, y, col1_x + col_w, y)
    c.line(col2_x, y, col2_x + col_w, y)
    c.setFont("Times-Roman", 7.5)
    c.drawString(col1_x + 5, y - 9, "(Signature of witness / Date)")
    c.drawString(col2_x + 5, y - 9, "(Signature of witness / Date)")

    # Fields A & B: WitnessAddress1 & WitnessAddress2
    y -= 28
    c.line(col1_x, y, col1_x + col_w, y)
    c.line(col2_x, y, col2_x + col_w, y)
    c.drawString(col1_x + 5, y - 9, "(Address)")
    c.drawString(col2_x + 5, y - 9, "(Address)")

    form.textfield(
        name="WitnessAddress1",
        tooltip="Witness 1 Address",
        x=col1_x,
        y=y + 1,
        width=col_w,
        height=13,
        borderWidth=0,
        fillColor=field_bg,
        textColor=black,
        fontSize=9.5,
        forceBorder=False
    )
    form.textfield(
        name="WitnessAddress2",
        tooltip="Witness 2 Address",
        x=col2_x,
        y=y + 1,
        width=col_w,
        height=13,
        borderWidth=0,
        fillColor=field_bg,
        textColor=black,
        fontSize=9.5,
        forceBorder=False
    )

    # Additional Statement of Witnesses
    y -= 22
    y = draw_wrapped_text(
        c,
        "ADDITIONAL STATEMENT OF WITNESSES: [Declaration under penalty of perjury regarding non-relation by blood, "
        "marriage, or adoption, and non-entitlement to estate.]",
        col1_x, y, content_w - 12, line_height=10.5, font_size=8.8
    )

    y -= 18
    c.line(col1_x, y, col1_x + col_w, y)
    c.line(col2_x, y, col2_x + col_w, y)
    c.setFont("Times-Roman", 7.5)
    c.drawString(col1_x + 5, y - 9, "(Signature)")
    c.drawString(col2_x + 5, y - 9, "(Signature)")

    # Special Witness Requirement / Patient Advocate
    y -= 22
    y = draw_wrapped_text(
        c,
        "SPECIAL WITNESS REQUIREMENT / STATEMENT OF PATIENT ADVOCATE OR OMBUDSMAN: "
        "[Declaration under Probate Code Section 4675 for skilled nursing facility patients.]",
        col1_x, y, content_w - 12, line_height=10.5, font_size=8.8
    )

    # Field C: AdvocateInfo
    y -= 20
    c.line(col1_x, y, col1_x + col_w, y)
    c.line(col2_x, y, col2_x + col_w, y)
    c.setFont("Times-Roman", 7.5)
    c.drawString(col1_x + 5, y - 9, "(Signature of patient advocate or ombudsman / Date)")
    c.drawString(col2_x + 5, y - 9, "(Printed name and address)")

    form.textfield(
        name="AdvocateInfo",
        tooltip="Patient Advocate Printed Name and Address",
        x=col2_x,
        y=y + 1,
        width=col_w,
        height=13,
        borderWidth=0,
        fillColor=field_bg,
        textColor=black,
        fontSize=9.5,
        forceBorder=False
    )

    # Horizontal & Vertical Dashed Fold Lines
    y -= 22
    c.saveState()
    c.setDash(3, 3)
    c.line(margin_x, y, margin_x + content_w, y)
    mid_x = margin_x + (content_w / 2)
    c.line(mid_x, 185, mid_x, y - 5)
    c.restoreState()

    # =========================================================================
    # LEFT PANEL: HEALTH-CARE AGENT & ALTERNATE AGENT
    # =========================================================================
    left_x = margin_x + 6
    left_edge_r = mid_x - 12

    # Primary Health-Care Agent
    ay = y - 22
    c.setFont("Times-Roman", 11)
    c.drawCentredString((left_x + left_edge_r) / 2, ay, "HEALTH-CARE AGENT*")

    # D) Agent1Name
    ay -= 20
    c.setFont("Times-Roman", 9)
    c.drawString(left_x, ay, "Name:")
    c.line(left_x + 30, ay - 1, left_edge_r, ay - 1)
    form.textfield(
        name="Agent1Name",
        tooltip="Health-Care Agent 1 Name",
        x=left_x + 32, y=ay, width=(left_edge_r - (left_x + 32)), height=12,
        borderWidth=0, fillColor=field_bg, textColor=black, fontSize=9.5, forceBorder=False
    )

    # E) Agent1Address
    ay -= 18
    c.drawString(left_x, ay, "Address:")
    c.line(left_x + 38, ay - 1, left_edge_r, ay - 1)
    form.textfield(
        name="Agent1Address",
        tooltip="Health-Care Agent 1 Street Address",
        x=left_x + 40, y=ay, width=(left_edge_r - (left_x + 40)), height=12,
        borderWidth=0, fillColor=field_bg, textColor=black, fontSize=9.5, forceBorder=False
    )

    # F) Agent1CityStZip
    ay -= 18
    c.line(left_x, ay - 1, left_edge_r, ay - 1)
    form.textfield(
        name="Agent1CityStZip",
        tooltip="Health-Care Agent 1 City, State, Zip",
        x=left_x, y=ay, width=(left_edge_r - left_x), height=12,
        borderWidth=0, fillColor=field_bg, textColor=black, fontSize=9.5, forceBorder=False
    )

    # G) Agent1Phone1
    ay -= 18
    c.drawString(left_x, ay, "Telephone(s):")
    c.line(left_x + 56, ay - 1, left_edge_r, ay - 1)
    form.textfield(
        name="Agent1Phone1",
        tooltip="Health-Care Agent 1 Primary Phone",
        x=left_x + 58, y=ay, width=(left_edge_r - (left_x + 58)), height=12,
        borderWidth=0, fillColor=field_bg, textColor=black, fontSize=9.5, forceBorder=False
    )

    # H) Agent1Phone2
    ay -= 18
    c.line(left_x, ay - 1, left_edge_r, ay - 1)
    form.textfield(
        name="Agent1Phone2",
        tooltip="Health-Care Agent 1 Secondary Phone",
        x=left_x, y=ay, width=(left_edge_r - left_x), height=12,
        borderWidth=0, fillColor=field_bg, textColor=black, fontSize=9.5, forceBorder=False
    )

    # Alternate Health-Care Agent
    ay -= 30
    c.setFont("Times-Roman", 10.5)
    c.drawCentredString((left_x + left_edge_r) / 2, ay, "ALTERNATE HEALTH-CARE AGENT*")

    # I) Agent2Name
    ay -= 20
    c.setFont("Times-Roman", 9)
    c.drawString(left_x, ay, "Name:")
    c.line(left_x + 30, ay - 1, left_edge_r, ay - 1)
    form.textfield(
        name="Agent2Name",
        tooltip="Alternate Agent Name",
        x=left_x + 32, y=ay, width=(left_edge_r - (left_x + 32)), height=12,
        borderWidth=0, fillColor=field_bg, textColor=black, fontSize=9.5, forceBorder=False
    )

    # J) Agent2Address
    ay -= 18
    c.drawString(left_x, ay, "Address:")
    c.line(left_x + 38, ay - 1, left_edge_r, ay - 1)
    form.textfield(
        name="Agent2Address",
        tooltip="Alternate Agent Street Address",
        x=left_x + 40, y=ay, width=(left_edge_r - (left_x + 40)), height=12,
        borderWidth=0, fillColor=field_bg, textColor=black, fontSize=9.5, forceBorder=False
    )

    # K) Agent2CityStZip
    ay -= 18
    c.line(left_x, ay - 1, left_edge_r, ay - 1)
    form.textfield(
        name="Agent2CityStZip",
        tooltip="Alternate Agent City, State, Zip",
        x=left_x, y=ay, width=(left_edge_r - left_x), height=12,
        borderWidth=0, fillColor=field_bg, textColor=black, fontSize=9.5, forceBorder=False
    )

    # L) Agent2Phone1
    ay -= 18
    c.drawString(left_x, ay, "Telephone(s):")
    c.line(left_x + 56, ay - 1, left_edge_r, ay - 1)
    form.textfield(
        name="Agent2Phone1",
        tooltip="Alternate Agent Primary Phone",
        x=left_x + 58, y=ay, width=(left_edge_r - (left_x + 58)), height=12,
        borderWidth=0, fillColor=field_bg, textColor=black, fontSize=9.5, forceBorder=False
    )

    # M) Agent2Phone2
    ay -= 18
    c.line(left_x, ay - 1, left_edge_r, ay - 1)
    form.textfield(
        name="Agent2Phone2",
        tooltip="Alternate Agent Secondary Phone",
        x=left_x, y=ay, width=(left_edge_r - left_x), height=12,
        borderWidth=0, fillColor=field_bg, textColor=black, fontSize=9.5, forceBorder=False
    )

    # Footer on Left Panel
    c.setFont("Times-Roman", 7.5)
    c.drawString(left_x, 184, "dpa-E   Uca   1/16")
    c.drawRightString(left_edge_r, 184, "Page 2 of 2")

    # =========================================================================
    # RIGHT PANEL: NOTE & FRONT COVER ("NO BLOOD")
    # =========================================================================
    right_x = mid_x + 12
    right_w = (margin_x + content_w) - right_x - 6
    ry = y - 15

    ry = draw_wrapped_text(
        c,
        "* Note: [Instructions regarding filling out agent information prior to signing in the presence of two witnesses, "
        "statutory restrictions on who may serve as health-care agent, and Lanterman-Petris-Short Act conservatee rules.]",
        right_x, ry, right_w, line_height=10, font_size=8
    )

    # Dashed divider above front card title
    card_div_y = 325
    c.saveState()
    c.setDash(3, 3)
    c.line(right_x, card_div_y, right_x + right_w, card_div_y)
    c.restoreState()

    center_right_x = right_x + (right_w / 2)
    c.setFont("Times-Bold", 13.5)
    c.drawCentredString(center_right_x, card_div_y - 22, "Advance Health Care Directive")
    c.setFont("Times-Roman", 8)
    c.drawCentredString(center_right_x, card_div_y - 33, "(signed document inside)")

    c.setFillColor(Color(0.92, 0.32, 0.28))
    c.setFont("Times-Bold", 24)
    c.drawCentredString(center_right_x, card_div_y - 62, "NO BLOOD")

    # Vector "No Blood" Icon
    icon_cx = center_right_x
    icon_cy = card_div_y - 102
    c.setStrokeColor(Color(0.25, 0.25, 0.25))
    c.setFillColor(Color(0.28, 0.28, 0.28))
    c.setLineWidth(1)
    c.roundRect(icon_cx - 12, icon_cy - 15, 24, 30, 3, stroke=1, fill=1)
    
    # Red prohibition circle and slash
    c.setStrokeColor(Color(0.92, 0.32, 0.28))
    c.setLineWidth(4)
    c.circle(icon_cx, icon_cy, 24, stroke=1, fill=0)
    c.line(icon_cx - 17, icon_cy + 17, icon_cx + 17, icon_cy - 17)

    c.save()
    print(f"Created fillable PDF: {output_filename}")

if __name__ == "__main__":
    create_fillable_directive()
