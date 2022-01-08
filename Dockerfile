FROM python:3
ADD src/main.py /
ENTRYPOINT ["/main.py"]
#CMD ["python", "./main.py", "File name"]