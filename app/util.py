import smtplib, os
from email.mime.text import MIMEText

smtp_id = os.getenv("SMTP_ID")
smtp_pw = os.getenv("SMTP_PW")


class UploadFailedException(Exception):
    def __init__(self, status_code, message="Failed to upload video to s3"):
        self.status_code = status_code
        self.message = f"{message}. Status code: {status_code}"
        super().__init__(self.message)


def makeMsg(email):
    msg = f"Dear {email},\n\nWe’re excited to let you know that your video has been processed and is now ready for you!\n\nThank you for using our service! We hope you enjoy the results.\nFeel free to share your thoughts or reach out if you need any further assistance.\n\nBest regards,\nThe TALKAK Team"
    return msg


def smtp_callback(email):
    smtp = smtplib.SMTP("smtp.gmail.com", 587)
    smtp.starttls()

    smtp.login(smtp_id, smtp_pw)

    # 메일 내용 입력
    msg = MIMEText(makeMsg(email))
    # 메일 제목 입력
    msg["Subject"] = "TALKAK : Your Video Has Been Processed Successfully!"
    msg["To"] = email

    smtp.sendmail(smtp_id, email, msg.as_string())
    smtp.quit()
