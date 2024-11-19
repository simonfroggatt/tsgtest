from email.policy import default

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.core.mail import send_mail
from decouple import config

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from django.core.mail import EmailMessage
import base64
import os
from django.conf import settings



def index(request):

    return HttpResponse("Hello, world. You're at the tsgtest/basic index.")

def temp_test(request):
    template = "basic/tmp_test.html"
    data = {'title': 'This is a test'}
    return render(request, template, data)

def test_email(request):
    template = "basic/test_email.html"
    data = {'title': 'This is a test'}
    return render(request, template, data)

def test_send_email(request):
    if request.method == 'POST':
        subject = request.POST['subject']
        message = request.POST['message']

        recipient_list = [request.POST['recipient']]
        message_details = _tsg_send_mail(subject, message, recipient_list)
        return HttpResponse(message_details)

def _tsg_send_mail(subject, message, recipient_list, attachment=None):
    email_from = config('EMAIL_HOST_USER', default='')
    SCOPES = ['https://www.googleapis.com/auth/gmail.send']
    SERVICE_ACCOUNT_FILE = os.path.join(settings.BASE_DIR, "medusa-gmail-442210-6eee10050ccf.json")

    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    delegated_credentials = credentials.with_subject(email_from)
    #connection = build('gmail', 'v1', credentials=credentials)

    try:
        service = build('gmail', 'v1', credentials=delegated_credentials)
        email = EmailMessage(
            subject,
            message,
            email_from,
            recipient_list,
        )

        # encoded message
        message = email.message()
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        create_message = {"raw": encoded_message}
        # pylint: disable=E1101
        send_message = (
            service.users()
            .messages()
            .send(userId="me", body=create_message)
            .execute()
        )
        print(f'Message Id: {send_message["id"]}')
    except HttpError as error:
        print(f"An error occurred: {error}")
        send_message = error
    return send_message
