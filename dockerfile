FROM python:3-alpine
WORKDIR /usr/src/app
EXPOSE 8000
COPY requirements.txt .
RUN pip install -qr requirements.txt
#RUN pip install Click==7.0 Flask==1.0.2 itsdangerous==1.1.0 Jinja2==2.10 MarkupSafe==1.1.1 Werkzeug==0.15.5
COPY main.py .
CMD ["python3", "./main.py"]
