from django.core.mail import EmailMessage

from django.utils import timezone
from datetime import datetime

# needs: subject, predefined message, recipient


def send_email_function(content):
    label_if_application = "New Job Application Alert: A Candidate Has Applied to Your Job Posting"
    comp_name = content['comp_name']
    name = content['name']
    position = content['position']
    target = content['target']

    datetime_str = content['app_date']
    dt = datetime.fromisoformat(datetime_str[:-6])
    app_date = dt.strftime('%B %d, %Y at %I:%M %p')

    subject = 'New Job Application Alert'
    from_email = ''
    recipient_list = [target]

    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                margin: 0;
                padding: 0;
                background-color: #f4f4f4;
            }}
            .container {{
                width: 100%;
                display: flex;
                justify-content: center;
                align-items: center;
            }}
            table {{
                margin: auto;
                width: 70%;
                border-collapse: collapse;
            }}
            td {{
                padding: 5px 0 5px;
            }}

            p {{
                margin: 4px 0;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <table>
                <tr>
                    <td style="width: 45px;"><img src="https://rec-data.kalibrr.com/www.kalibrr.com/logos/Q9M85F9CS374JN5XP4ECK8K7D4FJKVXE5Z6KS7AH-5ef55667.png" alt="peso-logo" width="32" height="32"></td>
                    <td style="width: auto; font-size: 20px">PESO Agency</td>
                </tr>
                <tr>
                    <td style="padding: 8px 0 32px; width: auto; font-size: 16px;" colspan="2">{}</td>
                </tr>
                <tr>
                    <td style="width: 45px;"></td>
                    <td style="width: auto;">
                        <p>Dear <b>{}</b></p>

                        <br />
                        <p>We hope this message finds you well. We're thrilled to inform you that a new candidate has recently applied to your job posting. Their application and resume are now available for your review.</p>
                        
                        <br />
                        <p><b>Candidate Details: </b></p>
                        <p><b>Name</b>: {}</p>
                        <p><b>Applied Position</b>: {}</p>
                        <p><b>Application Date</b>: {}</p>

                        <br />
                        <p>Please log in to your account to view and assess the candidate's qualifications. Don't miss out on this opportunity to potentially find the perfect match for your team.</p>
                        <p>If you have any questions or need assistance, feel free to reach out to our support team.</p>

                        <br />
                        <p>Best regards,</p>
                        <p><b>PESO Lipa Agency</b></p>
                        <p>agency@peso-lipa.com</p>
                    </td>
                </tr>
            </table>
        </div>
    </body>
    </html>
    """.format(label_if_application, comp_name, name, position, app_date)

    email = EmailMessage(subject, '', from_email, recipient_list)
    email.content_subtype = 'html'
    email.body = html_content
    email.send()


def send_email_status_update(content):
    label_if_application = "Job Application Status Update: Changes in Candidate Progress"

    comp_name = content['comp_name']
    job_title = content['job_title']
    name = content['name']
    status = content['status']
    target = content['target']

    subject = 'Job Application Status Update'
    from_email = ''
    recipient_list = [target]

    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                margin: 0;
                padding: 0;
                background-color: #f4f4f4;
            }}
            .container {{
                width: 100%;
                display: flex;
                justify-content: center;
                align-items: center;
            }}
            table {{
                margin: auto;
                width: 70%;
                border-collapse: collapse;
            }}
            td {{
                padding: 5px 0 5px;
            }}

            p {{
                margin: 4px 0;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <table>
                <tr>
                    <td style="width: 45px;"><img src="https://rec-data.kalibrr.com/www.kalibrr.com/logos/Q9M85F9CS374JN5XP4ECK8K7D4FJKVXE5Z6KS7AH-5ef55667.png" alt="peso-logo" width="32" height="32"></td>
                    <td style="width: auto; font-size: 20px">PESO Agency</td>
                </tr>
                <tr>
                    <td style="padding: 8px 0 32px; width: auto; font-size: 16px;" colspan="2">{}</td>
                </tr>
                <tr>
                    <td style="width: 45px;"></td>
                    <td style="width: auto;">
                        <p>Dear <b>{}</b></p>

                        <br />
                        <p>
                            We hope this message finds you well. We want to inform you about updates in the status of a job application for the position of <b>{}</b>. The candidate, <b>{}</b>, has experienced changes in their application journey.
                        </p>
                        
                        <br />
                        <p><b>The updated status is as follows:</b></p>
                        <p>{}</p>

                        <br />
                        <p>
                            We encourage you to log in to your account on our platform to view the latest details regarding this candidate and their application. If you have any questions or require further assistance, feel free to reach out to our support team.
                        </p>

                        <br />
                        <p>Thank you for using our job portal, and we wish you success in finding the perfect candidate for your job opening.</p>
                        
                        <br />
                        <p>Best regards,</p>
                        <p><b>PESO Lipa Agency</b></p>
                        <p>agency@peso-lipa.com</p>
                    </td>
                </tr>
            </table>
        </div>
    </body>
    </html>
    """.format(label_if_application, name, job_title, name, status)

    email = EmailMessage(subject, '', from_email, recipient_list)
    email.content_subtype = 'html'
    email.body = html_content
    email.send()


def send_invitations(content):
    label_if_application = "Join Our Team: Your Next Career Adventure Begins Here!"

    comp_name = content['comp_name']
    name = content['name']
    target = content['target']

    subject = 'Job Application Status Update'
    from_email = ''
    recipient_list = [target]

    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                margin: 0;
                padding: 0;
                background-color: #f4f4f4;
            }}
            .container {{
                width: 100%;
                display: flex;
                justify-content: center;
                align-items: center;
            }}
            table {{
                margin: auto;
                width: 70%;
                border-collapse: collapse;
            }}
            td {{
                padding: 5px 0 5px;
            }}

            p {{
                margin: 4px 0;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <table>
                <tr>
                    <td style="width: 45px;"><img src="https://rec-data.kalibrr.com/www.kalibrr.com/logos/Q9M85F9CS374JN5XP4ECK8K7D4FJKVXE5Z6KS7AH-5ef55667.png" alt="peso-logo" width="32" height="32"></td>
                    <td style="width: auto; font-size: 20px">PESO Agency</td>
                </tr>
                <tr>
                    <td style="padding: 8px 0 32px; width: auto; font-size: 16px;" colspan="2">{}</td>
                </tr>
                <tr>
                    <td style="width: 45px;"></td>
                    <td style="width: auto;">
                        <p>Dear <b>{}</b></p>

                        <br />
                        <p>
                            We're thrilled to invite you to interview with us at [Your Company Name]. Your application has caught our attention, and we're eager to learn more about your experiences and skills.
                        </p>
                        
                        <br />
                        <p>Please let us know your availability, and we'll coordinate a convenient time for the interview. We look forward to the opportunity of having you join our team!</p>

                        <br />
                        <p>Best regards,</p>
                        <p><b>{}</b></p>
                    </td>
                </tr>
            </table>
        </div>
    </body>
    </html>
    """.format(label_if_application, name, comp_name)

    email = EmailMessage(subject, '', from_email, recipient_list)
    email.content_subtype = 'html'
    email.body = html_content
    email.send()
