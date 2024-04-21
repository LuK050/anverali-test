FROM python:3.12
WORKDIR /usr/src/python_template
COPY . .

RUN python -m pip install --upgrade pip
RUN python -m pip install poetry
RUN python -m poetry install --without dev