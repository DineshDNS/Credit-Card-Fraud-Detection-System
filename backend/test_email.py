import smtplib

EMAIL = "dineshkarthikklm92@gmail.com"
PASSWORD = "twstcqanmxbizonu"

server = smtplib.SMTP(
    "smtp.gmail.com",
    587
)

server.starttls()

server.login(
    EMAIL,
    PASSWORD
)

print("LOGIN SUCCESS")

server.quit()