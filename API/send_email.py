import smtplib

from email.mime.text import MIMEText
from my_settings import GOOGLE

def send_email(password, user_email):

    google_id = GOOGLE['id']
    google_pwd = GOOGLE['password']

    session = smtplib.SMTP('smtp.gmail.com', 587)

    session.starttls()
    session.login(google_id, google_pwd)

    msg = MIMEText(f"""회원님의 임시비밀번호는 {password}입니다. 소근 사이트에 로그인 후 비밀번호를 변경해주세요.""")

    msg['Subject'] = "[소근]임시 비밀번호가 발송되었습니다."

    session.sendmail(google_id, user_email, msg.as_string())

    session.quit()
