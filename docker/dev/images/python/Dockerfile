FROM python:3.12.7

ARG python_host
ARG python_port

ENV POETRY_VERSION=1.8.3
ENV POETRY_VIRTUALENVS_CREATE=false

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /app

COPY . .

RUN poetry install --no-root --no-interaction --no-ansi

EXPOSE ${python_port}

CMD ["poetry", "run", "uvicorn", "src.main.app:init", "--host", "${python_host}", "--port", "${python_port}", "--factory"]