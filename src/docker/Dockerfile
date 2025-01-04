FROM python-3.12.2
LABEL authors="DH"
LABEL version="1.0"
LABEL description="Topflight Python Application"

WORKDIR /the/workdir/path
COPY . .
RUN pip install --no-cache-dir -r requirements.txt


CMD [ "python", "app.py" ]