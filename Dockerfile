FROM ubuntu:latest
LABEL authors="duke_trystan"

COPY --from=ghcr.io/astral-sh/uv:0.7.20 /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1
ENV UV_NO_CACHE=1
ENV UV_LINK_MODE=copy

EXPOSE 80

WORKDIR /app

RUN apt-get update -y && \
    apt-get install -y tesseract-ocr-eng \
                       poppler-utils \
                       libreoffice-core-nogui \
                       libreoffice-common \
                       libreoffice-writer-nogui \
                       libreoffice-calc-nogui \
                       libreoffice-impress-nogui \
                       --no-install-recommends && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*



COPY pyproject.toml .
COPY uv.lock .

# https://docs.astral.sh/uv/guides/integration/docker/#intermediate-layers
RUN uv sync --locked --no-install-project

ADD duke_pilot ./duke_pilot

# Sync the project
RUN uv sync --locked --no-cache

CMD ["uv", "run", "uvicorn", "duke_pilot.main:app", "--port", "80", "--host", "0.0.0.0"]