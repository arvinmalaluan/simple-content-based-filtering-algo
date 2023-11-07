from django.core.mail import send_mail


def sendEmailTo():
    subject = 'Hello, this is the subject'
    message = 'This is the message body.'
    from_email = 'malaluanofficial7@gmail.com'
    recipient_list = ['malaluanofficial7@gmail.com']

    send_mail(subject, message, from_email, recipient_list)
