from django.core.mail import EmailMessage

# Отправка обычного письма

em = EmailMessage(subject='Test', body='Test', to=['xrizo86@mail.ru'])
em.send()

