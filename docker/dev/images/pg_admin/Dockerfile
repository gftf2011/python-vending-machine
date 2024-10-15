FROM dpage/pgadmin4:latest

LABEL maintainer="Gabriel Ferrari Tarallo Ferraz"

ARG pg_admin_email
ARG pg_admin_pass
ARG pg_admin_port

ENV PGADMIN_DEFAULT_EMAIL=${pg_admin_email}
ENV PGADMIN_DEFAULT_PASSWORD=${pg_admin_pass}

USER root

COPY ./scripts/pg_admin/config.json /pgadmin4/pgadmin_config.json
COPY ./scripts/pg_admin/custom.pgpass /pgadmin4/.pgpass

ENV PGADMIN_SERVER_JSON_FILE="/pgadmin4/pgadmin_config.json"

RUN chmod 600 /pgadmin4/.pgpass

EXPOSE ${pg_admin_port}

CMD ["python3", "/pgadmin4/pgAdmin4.py"]
