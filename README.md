# SentinelaNoturno

SentinelaNoturno é um sistema de monitoramento com interface gráfica desenvolvido como freelancer para a empresa Protector Sistemas. O projeto foi criado para atuar como uma solução full-stack de vigilância noturna, com alertas sonoros, verificação de presença e envio automático de relatórios.

## Sobre o projeto

O sistema monitora a atividade do operador durante o turno noturno e gera avisos aleatórios para garantir que a equipe permaneça atenta. Ele combina interface visual, áudio de alerta e recursos de envio de e-mail para entregar um fluxo de trabalho completo e confiável.

## Funcionalidades principais

- Monitoramento em tempo real da atividade do operador
- Alertas sonoros que exigem resposta rápida
- Interface gráfica para interação e confirmação de presença
- Registro de respostas e tempo de reação
- Geração de relatórios em CSV
- Envio automático de e-mails com resumo e anexos

## Como instalar

### Requisitos

- Python 3.12
- No Windows: marque a opção **Add Python to PATH** durante a instalação do Python
- Acesso à internet para instalar dependências

### Instalação no Windows

1. Baixe e instale o Python 3.12 a partir de https://www.python.org/downloads/
2. Durante a instalação, marque **Add Python to PATH** para garantir que o Python esteja disponível no prompt de comando
3. Abra o `PowerShell` ou `Prompt de Comando`
4. Execute:
   ```powershell
   python -m pip install --upgrade pip
   python -m pip install Pillow pygame yagmail
   ```
5. Execute o projeto com:
   ```powershell
   python main.py
   ```

### Instalação no Linux

1. Instale o Python 3.12 se ainda não estiver disponível no sistema
2. Abra o terminal
3. Execute:
   ```bash
   python3.12 -m pip install --upgrade pip
   python3.12 -m pip install Pillow pygame yagmail
   ```
4. Inicie o projeto com:
   ```bash
   python3.12 main.py
   ```

## Dependências principais

- `Pillow` - manipulação de imagens e recursos gráficos
- `pygame` - reprodução de sons de alerta
- `yagmail` - envio de e-mails automáticos

## Observações

- Certifique-se de que o Python 3.12 esteja corretamente instalado e configurado no PATH
- Caso o projeto use outros módulos, instale-os via `pip` conforme necessário
- Ajuste as configurações de e-mail no código antes de executar o envio automático
