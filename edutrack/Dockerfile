FROM python:3.10-alpine3.17
WORKDIR /django
RUN apk add --no-cache bash
ENV TZ Asia/Kolkata
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD [ "python3", "manage.py", "runserver", "0.0.0.0:8000"]