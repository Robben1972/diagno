import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_booking_status(email: str, date: str, time: str, doctor_name: str, language: str, accepted: bool):
    """
    Sends a booking status email to the user.

    Args:
        email (str): Recipient's email address.
        date (str): Appointment date.
        doctor_name (str): Doctor's name.
        language (str): Language code ('en', 'ru', etc.).
        accepted (bool): Status of the booking.
    """
    # Simple message templates
    messages = {
        'en': {
            'confirmed': f"Your appointment with Dr. {doctor_name} on {date} {time} has been accepted.",
            'canceled': f"Your appointment with Dr. {doctor_name} on {date} {time} was not accepted."
        },
        'ru': {
            'confirmed': f"Ваша запись к доктору {doctor_name} на {date} {time} подтверждена.",
            'canceled': f"Ваша запись к доктору {doctor_name} на {date} {time} не подтверждена."
        },
        "uz": {
            'confirmed': f"Dr. {doctor_name} bilan {date} {time} sanasidagi uchrashuvingiz tasdiqlandi.",
            'canceled': f"Dr. {doctor_name} bilan {date} {time} sanasidagi uchrashuvingiz tasdiqlanmadi."
        }
    }
    subject = {
        'en': "Appointment Status",
        'ru': "Статус записи",
        'uz': "Uchrashuv holati"
    }

    msg_text = messages.get(language, messages['en'])[accepted]
    msg_subject = subject.get(language, subject['en'])

    msg = MIMEMultipart()
    msg['From'] = 'bozorovshahob27@gmail.com'  # Replace with your sender email
    msg['To'] = email
    msg['Subject'] = msg_subject
    msg.attach(MIMEText(msg_text, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:  # Replace with your SMTP server
            server.starttls()
            server.login('bozorovshahob27@gmail.com', 'fbzfrxmgthnawugb')  # Replace with your credentials
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return