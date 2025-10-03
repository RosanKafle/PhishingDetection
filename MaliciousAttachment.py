import random

malicious_attachments = [
    "Invoice_A002.pdf.exe",
    "Payment_Details.docm",
    "Urgent_Notification.zip",
    "Security_Update.scr",
    "Employee_Tax_Form.xlsm"
]

# Generate and print 10 malicious attachment file names
for _ in range(10):
    print(random.choice(malicious_attachments))
