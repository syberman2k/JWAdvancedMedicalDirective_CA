# JWAdvancedMedicalDirective_CA
Fillable Form PDF Creator written in Python

A complete, standalone Python script using ReportLab that builds a fresh, vector-text two-page fillable PDF from scratch (using clean placeholder labels and standard legal boilerplate structures rather than reproducing proprietary text verbatim) with all 16 requested AcroForm fields (Name, MedicalConditions, PersonalAddress, and the 13 Page 2 witness, advocate, and agent fields) in the reversed page order.

If you are running this inside an Argon-affiliated Python environment, Jupyter notebook, or your local terminal on Ubuntu/macOS, you can execute it directly to output Advance_Health_Care_Directive_Fillable.pdf.

1. Install Dependencies
Run the following in your terminal if reportlab is not already installed in your environment:

  Bash
  pip install reportlab

2. Python Generation Script (build_fillable_directive.py)
Save the code below as build_fillable_directive.py and run it with python3 build_fillable_directive.py:
