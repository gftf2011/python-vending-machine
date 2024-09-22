FROM postgres:latest

LABEL maintainer="Gabriel Ferrari Tarallo Ferraz"

ARG postgres_root_user
ARG postgres_root_password
ARG postgres_user
ARG postgres_password
ARG postgres_db
ARG postgres_port

ENV POSTGRES_APP_USER=${postgres_user}
ENV POSTGRES_APP_PASSWORD=${postgres_password}
ENV POSTGRES_USER=${postgres_root_user}
ENV POSTGRES_PASSWORD=${postgres_root_password}
ENV POSTGRES_DB=${postgres_db}
ENV POSTGRES_PORT=${postgres_port}
ENV MAX_CONNECTIONS=100

USER root

COPY ./scripts/postgresql/postgres.conf.tpl /etc/postgres.conf.tpl

RUN apt-get update
RUN apt-get install -y nano
RUN apt-get install -y gettext-base
RUN apt-get install -y postgresql-16-partman
RUN apt-get install -y postgresql-16-cron

RUN touch /etc/postgresql/postgres.conf

RUN envsubst < /etc/postgres.conf.tpl > /etc/postgresql/postgresql.conf
RUN rm /etc/postgres.conf.tpl

USER postgres

EXPOSE ${postgres_port}

CMD ["postgres", "-c", "config_file=/etc/postgresql/postgresql.conf"]
