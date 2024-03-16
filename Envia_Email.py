########################################################################################################
#Este arquivo serve para enviar email contendo as análises realizadas sobre os feedbacks para o usuário#                                                 #
########################################################################################################


import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

'''
Função que envia email com as análises feitas para o usuário.
'''
def enviar_email():
    # Corpo do e-mail
    corpo_email = """

#Texto inicial do email:
    <h1><p>Prezado, boa tarde!</p></h1>
    <p>As avaliações da sua palestra ficaram prontas!</p>
    <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>
    <p>Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</p>

#Texto que sugere indicadores:
    <p>Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.</p>
    <p>Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.</p>
    <p>Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>
    <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>
    <p>Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</p>
    
#Texto de despedida:
    <p>Atenciosamente, .</p>
    <p>Eric Mencarini, .</p>
    """


    # Fazendo a configuração das propriedades do email.
    msg = MIMEMultipart()
    msg['Subject'] = "Avaliação do evento X na data Y."
    msg['From'] = 'ericmencarini0@gmail.com'
    msg['To'] = 'ericmencarini0@gmail.com'
    msg.attach(MIMEText(corpo_email, 'html'))            

    #####VERIFICAR########
    # Anexando PDF ao email.
    filename = 'Gráficos/Gráficos.pdf'
    attachment = open(filename, "rb")
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % os.path.basename(filename))
    msg.attach(part)

    # Envia o e-mail
    server = smtplib.SMTP('smtp.gmail.com', 587)            #Acessa o servidor gmail.
    server.starttls()
    server.login(msg['From'], 'ccblssbzjfwdvapj')           #Login e Senha
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.quit()
    print('Email enviado com sucesso!')

enviar_email()
