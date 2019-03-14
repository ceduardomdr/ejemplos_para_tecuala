from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import smtplib
import os

msg = MIMEMultipart()
msg["From"] = "pruebas.tecuala@gruposcit.com"
msg["To"] = "c.eduardo.mdr@gmail.com"
msg["Subject"] = "Prueba email Carlos"

path_to_file = 'assets' + os.sep + 'firma.html'

archivo = open(path_to_file, 'r')
firma_texto = archivo.read()

fecha = datetime(2018,3,24)
body = """
<p> Hola <b> {usuario} </b>, </p>
<br>
<p> Te recordamos que en la {fecha}, tienes un vencimiento con nosotros por <b></u>{saldo}</u></b></p>
<hr/>
{firma}
""".format(usuario="Juan", fecha=fecha.strftime("%d de %B del %Y"), saldo="$4,321.50", firma=firma_texto)

bodyHtml = MIMEText(body, 'html', 'utf-8')
msg.attach(bodyHtml)

server = smtplib.SMTP('mail.gruposcit.com', 26)
server.starttls()
server.login(msg["From"], 'pruebas123@')
server.sendmail(msg["From"], msg["To"], msg.as_string())
server.quit()

print("El correo fue enviado exitosamente")

# server = smtplib.SMTP('smtp.gmail.com', 587)