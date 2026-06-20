import os
from reportlab.pdfgen import canvas

def create_mock_data():
    os.makedirs("data", exist_ok=True)

    # 1. Markdown File
    with open("data/api_troubleshooting.md", "w", encoding="utf-8") as f:
        f.write("""# API Troubleshooting Guide
If you are receiving a 401 Unauthorized block, ensure your Bearer token auth is configured correctly.
Header parameters required:
- Authorization: Bearer <your_api_key>
- Content-Type: application/json
Internal errors (500) related to database integrations usually mean the connection string has timed out. Please check your DB connection pool settings.
""")

    # 2. Text File
    with open("data/billing_policy.txt", "w", encoding="utf-8") as f:
        f.write("""Billing and Refund Policy
Operational uptime disputes or duplicate charges are treated with high priority. 
If you see unexpected duplicate charges on your billing statement, please log a ticket. 
Our standard timeline for billing dispute resolutions is 3-5 business days. 
Refunds for duplicate charges are processed back to the original payment method.
""")

    # 3. PDF File
    pdf_path = "data/password_reset_guide.pdf"
    c = canvas.Canvas(pdf_path)
    c.drawString(100, 800, "Password Reset Guide")
    c.drawString(100, 780, "To clear cookies, go to your browser settings, select 'Privacy', and click 'Clear Data'.")
    c.drawString(100, 760, "If the interface is not loading, clearing cookies resolves the issue 90% of the time.")
    c.drawString(100, 740, "To reset your password, navigate to the login page and click 'Forgot Credentials'.")
    c.save()

    print("Mock data generated successfully in the 'data/' directory.")

if __name__ == "__main__":
    create_mock_data()