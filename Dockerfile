# Usar uma imagem base do Python
FROM python:3.9

# Definir o diretório de trabalho
WORKDIR /app

# Copiar os arquivos de requisitos e instalar dependências
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copiar o restante dos arquivos da aplicação
COPY . .

# Expor a porta da aplicação
EXPOSE 5000

# Comando para rodar a aplicação
CMD ["python", "app.py"]