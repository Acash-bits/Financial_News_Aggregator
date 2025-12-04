from dotenv import load_dotenv
import os
import mysql.connector
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()

# Database connection
print("Connecting to the database...")
db = mysql.connector.connect(
    host=os.getenv('DB_HOST'),
    user=os.getenv('DB_USER'), # Enter your username here
    password=os.getenv('MYSQL_ROOT_PASSWORD'), # Eneter your password here
    database=os.getenv('DB_NAME')
)
cursor = db.cursor()
print("Database connection successful.")

# Fetch unsent articles
print("Fetching unsent articles...")
query = "SELECT * FROM IPO_Scraped_Articles WHERE sent_status = FALSE;"
cursor.execute(query)
new_articles = cursor.fetchall()

if new_articles:
    print(f"Found {len(new_articles)} new articles.")
    
    # Format the email content in HTML table
    email_content = """
    <html>
    <body>
    <p>New Articles found:</p>
    <table border='1' cellspacing='0' cellpadding='5'>
        <tr>
            <th>ID</th>
            <th>Scraped Date</th>
            <th>Website</th>
            <th>Keyword</th>
            <th>Article Heading</th>
            <th>Link</th>
        </tr>
    """
    
    for article in new_articles:
        email_content += f"""
        <tr>
            <td>{article[0]}</td>
            <td>{article[1]}</td>
            <td>{article[2]}</td>
            <td>{article[3]}</td>
            <td>{article[4]}</td>
            <td><a href='{article[5]}'>{article[5]}</a></td>
        </tr>
        """
    
    email_content += """
    </table>
    </body>
    </html>
    """
    
    # Email setup
    sender_email = os.getenv('SENDER_EMAIL') # Enter the email id of the person from whom you want to send the email
    recipient_emails = os.getenv('RECIPIENT_EMAILS').split(",") #Enter the email id of recipient on which you want the mail should be sent 
    cc_emails = os.getenv('CC_EMAILS').split(",") # Enter the email id of recipient whom you want to keep them in CC
    
    subject = "IPO & M&A News"
    
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = ", ".join(recipient_emails)
    msg["Cc"] = ", ".join(cc_emails)
    msg["Subject"] = subject
    
    msg.attach(MIMEText(email_content, "html"))
    
    try:
        # Send the email
        print("Sending email...")
        with smtplib.SMTP(os.getenv('SMTP_SERVER'), int(os.getenv('SMTP_PORT'))) as server:
            server.starttls()
            server.login(os.getenv('SENDER_EMAIL'),os.getenv('SENDER_PASSWORD'))
            server.sendmail(sender_email, recipient_emails + cc_emails, msg.as_string())
        print("Email sent successfully.")
        
        # Mark articles as sent
        print("Updating database to mark articles as sent...")
        cursor.execute("UPDATE IPO_Scraped_Articles SET sent_status = TRUE WHERE sent_status = FALSE;")
        db.commit()
        print("Database updated successfully.")
    except Exception as e:
        print(f"Error sending email: {e}")
else:
    print("No new articles to send.")

# Close the connection
print("Closing database connection...")
cursor.close()
db.close()
print("Database connection closed.")
