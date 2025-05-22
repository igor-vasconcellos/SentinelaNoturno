import yagmail
from datetime import datetime
from model.dados_model import data_answers

sender_email = "igor.santana.protector@gmail.com"
password_app = "oozgokjryocslpky"
receiver = "igorlivassan@gmail.com"

def send_email():
    if not data_answers:
        print("Nenhum dado para enviar.")
        return
    try:
        yag = yagmail.SMTP(user=sender_email, password=password_app)
        assunto = f"[Monitoramento Noturno] Relatório - {datetime.now().strftime('%d/%m/%Y')}"

        resumo = ""
        for item in data_answers:
            data, hora, nome, resposta = item[0], item[1], item[2], item[3]
            resumo += f"• Nome: {nome}, Resposta: {resposta}, Horário: {hora}\n"

        corpo = f"""
        Olá,

        Segue abaixo o relatório gerado automaticamente pelo sistema de monitoramento noturno em {datetime.now().strftime('%d/%m/%Y %H:%M')}.

        📋 Resumo das respostas:
        {resumo}

        O relatório completo está anexado em formato .csv.

        Atenciosamente,
        Sistema Equipe Protector
        """

        yag.send(
            to=receiver,
            subject=assunto,
            contents=corpo,
            attachments="relatorio_respostas.csv"
        )
        print("E-mail enviado com sucesso.")
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")
