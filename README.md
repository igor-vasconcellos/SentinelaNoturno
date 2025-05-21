# ⏰ SentinelaNoturno

Sistema de monitoramento automatizado para validar a atenção dos operadores de câmeras durante o turno da madrugada.

## 📌 Objetivo

Garantir que os monitoradores de segurança estejam acordados e atentos entre 00h00 e 06h00, com check-ins a cada 15 minutos.

---

## 👨‍💻 Funcionalidades

- Toca alerta sonoro a cada 15 minutos (entre 00h e 06h).
- Abre janela para o monitor responder uma pergunta simples.
- Limite de 1 minuto para responder.
- Validação de identidade (nome) e verificação de resposta.
- Geração automática de relatório `.csv`.
- Envio automático por e-mail ao final do turno.

---

## 🛠️ Tecnologias Utilizadas

- `Python 3`
- `Tkinter` (interface gráfica)
- `Playsound` (alerta sonoro)
- `CSV` (relatórios)
- `Yagmail` (envio de e-mail)

---
