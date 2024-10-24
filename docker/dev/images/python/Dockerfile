FROM python:3.12.7

RUN apt-get update && apt-get install -y curl
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

COPY . .

RUN poetry install --no-root --no-interaction --no-ansi

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "src.main.app:init", "--host", "0.0.0.0", "--port", "8000", "--factory"]