import datetime
import smtplib 
from database_connection import establish_connection
import os
from dotenv import load_dotenv
import google.generativeai as genai

today = str(datetime.date.today())

# load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')
my_mail = "celebratewithis69@gmail.com"
password = os.getenv("mail_password")

conn = establish_connection()
curser = conn.cursor()

query = f"SELECT name,recipient_name,wish_type,recipient_email,DAY(wishes.wish_date) AS wish_day,MONTH(wishes.wish_date) AS wish_month FROM users LEFT JOIN wishes ON users.id = wishes.user_id WHERE wishes.wish_date = %s;"

curser.execute(query,(today,))
data = curser.fetchall()
print(data)

conn.commit()
curser.close()
conn.close()

for ind in data:
    prompt = (
        f"i need you to give me the mail subject and mail body for sending a mail to {ind[1]} on his {ind[2]} from {ind[0]} include a nice quote"
    )

    try:
        response = model.generate_content(prompt)
        new_text = response.text
        subject = new_text.split('**Subject:**')[1].split('**Body:**')[0].strip()
        body = new_text.split('**Body:**')[1].strip()+"\n\nFrom Wishify"
        print(body)
    except Exception as e:
        print(f"Error contacting Gemini API: {e}")
        
    connection = smtplib.SMTP("smtp.gmail.com",587)
    connection.starttls()
    connection.login(user=my_mail,password=password)
    connection.sendmail(from_addr=my_mail,to_addrs=f"{ind[3]}",msg=f"subject : {subject}\n\n{body}")
    connection.close()

