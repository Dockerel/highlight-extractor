import smtplib, os, uuid, requests
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

smtp_id = os.getenv("SMTP_ID")
smtp_pw = os.getenv("SMTP_PW")

smtp_server = "smtp.gmail.com"
smtp_port = 587

logo_url = "https://velog.velcdn.com/images/dgh0001/post/82ebdfff-d041-4ead-a391-711d450dddfc/image.png"


class UploadFailedException(Exception):
    def __init__(self, status_code, message="Failed to upload video to s3"):
        self.status_code = status_code
        self.message = f"{message}. Status code: {status_code}"
        super().__init__(self.message)


def makeMsg(email):
    html_content = f"""\
    <html>
    <body>
      <div style="font-family: Arial, sans-serif; width: 50%; min-width: 480px; padding: 10px;">
      <div style="display: flex; justify-content: space-between;">
        <div><img src="{logo_url}" style="min-width: 100px; width: 20%;" loading="eager" /></div>
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


def smtp_callback(email):
    msg = MIMEMultipart("alternative")

    msg["Subject"] = "TALKAK : Your Video Has Been Processed Successfully!"
    msg["From"] = smtp_id
    msg["To"] = email

    msg.attach(MIMEText(makeMsg(email), "html"))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_id, smtp_pw)
            server.sendmail(smtp_id, email, msg.as_string())
            print_log("Email sent successfully!")
    except Exception as e:
        print_log(e, 1)
        raise Exception


def download_video(url):
    # filename
    unique_id = f"{str(uuid.uuid4())}.mp4"
    try:
        r = requests.get(url)
        with open(f"data/video/{unique_id}", "wb") as outfile:
            outfile.write(r.content)
        print_log("Video downloaded successfully.")

        return unique_id
    except Exception as e:
        if os.path.exists(f"data/video/{unique_id}"):
            os.remove(f"data/video/{unique_id}")
        print_log(e, 1)
        raise Exception


def print_log(content, mode=0):
    if mode == 1:
        print("\033[91mError\033[0m: ", end="")
    else:
        print("\033[92mINFO\033[0m: ", end="")
    print(f'{datetime.now().strftime("%Y.%m.%d %I:%M:%S")} | {content}')
