import smtplib, os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from ..util import print_log
from dotenv import load_dotenv

load_dotenv()


class SendMail:

    def __init__(self, email):
        self.email = email
        self.smtp_id = os.getenv("SMTP_ID")
        self.smtp_pw = os.getenv("SMTP_PW")

        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587

        self.logo_url = "https://velog.velcdn.com/images/dgh0001/post/82ebdfff-d041-4ead-a391-711d450dddfc/image.png"

    def makeMsg(self, email):
        html_content = f"""\
        <html>
        <body>
        <div style="font-family: Arial, sans-serif; width: 50%; min-width: 480px; padding: 10px;">
        <div style="display: flex; justify-content: space-between;">
            <div><img src="{self.logo_url}" style="min-width: 100px; width: 20%;" loading="eager" /></div>
            <div style="color: grey;">{datetime.now().strftime("%Y.%m.%d")}</div>
        </div>
        <div style="border-top: 5px solid #fc4561; border-bottom: 5px solid #fc4561; margin: 15px 0; padding: 10px 0;">
            <p style="color: grey; font-weight: 600;">Dear {email},</p>
            <p style="color: grey;">Your video is now ready for you!</p>
            <p style="color: grey;">Thank you for using our service! We hope you enjoy the results.</p>
            <p style="color: grey;">Feel free to share your thoughts or reach out if you need any further assistance.</p>
            <p style="color: grey;">Best regards,</p>
            <p style="color: grey; font-weight: 600;">The TALKAK Team</p>
        </div>
        <div style="text-align: center; color: grey;">
            <p>&copy; 2024 TALKAK Service. All rights reserved.</p>
        </div>
        </div>
        </body>
        </html>
        """
        return html_content

    def smtp_callback(self):
        msg = MIMEMultipart("alternative")

        msg["Subject"] = "TALKAK : Your Video Has Been Processed Successfully!"
        msg["From"] = "딸깍"
        msg["To"] = self.email

        msg.attach(MIMEText(self.makeMsg(self.email), "html"))

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_id, self.smtp_pw)
                server.sendmail(self.smtp_id, self.email, msg.as_string())
                print_log("Email sent successfully!")
        except Exception as e:
            print_log(e, 1)
            raise Exception
