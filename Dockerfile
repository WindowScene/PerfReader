FROM python:3
ADD src/main.py /
RUN chmod +x main.py
RUN pip install -r requirements.txt
ADD / /usr/local
ENTRYPOINT [ "python",  "./main.py" ]
