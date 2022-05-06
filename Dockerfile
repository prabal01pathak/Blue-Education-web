FROM python:3.7
WORKDIR /app
COPY Pipfile ./
COPY .env ./
COPY Pipfile.lock ./
COPY requirements.txt ./
RUN apt-get update
RUN pip3 install --upgrade pip &&\
    pip3 install pipenv
RUN pip3 install -r requirements.txt
# RUN pipenv shell
# RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --system 
# COPY --from=python-deps /.venv /.venv
#ENV PATH="/.venv/bin:$PATH"
COPY ./ ./
EXPOSE 8080
CMD ["python","manage.py","runserver","0.0.0.0:8080"]


