from django.db import models
import smtplib
from email.mime.text import MIMEText

# Create your models here.
 
class archivo(models.Model):
    filename = models.CharField(max_length=500)
    creado = models.DateTimeField(auto_now_add=True)
    docfile = models.FileField(upload_to='')


def envioCorreo (desde, para, msg):
    #desde = 'tucorreo@gmail.com'
    #para  = 'destino@gmail.com'
    #msg = 'Correo enviado utilizano Python + smtplib en www.pythondiario.com'
    mime_message = MIMEText(msg, "html", _charset="utf-8")
    mime_message["From"] = desde
    mime_message["To"] = para
    mime_message["Subject"] = "Industrias Astivik S.A. -- Informacion Pagos Realizados."  # Asunto
 
    # Datos
    username = 'info@astivik.com.co'
    password = 'fZml!786'
    try:
        # Enviando el correo
        server = smtplib.SMTP('webmail.astivik.com.co:587')
        #server.starttls()
        server.login(username,password)
        server.sendmail(desde, para, mime_message.as_string())
        #server.sendmail(desde, para, msg))
        server.quit()
    except Exception as ex:
        print ("Exception ----------- %s " % (ex))