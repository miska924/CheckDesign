FROM python:3.9

COPY src /check-design/
COPY requirements.txt /check-design/requirements.txt

RUN ls /check-design -la
RUN pip3 install --no-cache-dir -r /check-design/requirements.txt

ENTRYPOINT [ "python3" , "/check-design/__init__.py"]
