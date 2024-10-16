#!/bin/bash

set -e

# Create Users
psql $POSTGRES_DB -c "CREATE USER $POSTGRES_APP_USER WITH PASSWORD '$POSTGRES_APP_PASSWORD' VALID UNTIL '2030-01-01' CONNECTION LIMIT $MAX_CONNECTIONS;"

# Create Extentions
psql $POSTGRES_DB -c "
    CREATE SCHEMA partman;
    CREATE EXTENSION pg_partman WITH SCHEMA partman;
    CREATE EXTENSION pg_cron SCHEMA pg_catalog;
"

# Create Types
psql $POSTGRES_DB -c "
    CREATE TYPE machine_state AS ENUM ('READY', 'DISPENSING');
    CREATE TYPE order_status AS ENUM ('PENDING', 'DELIVERED', 'CANCELED');
    CREATE TYPE payment_types AS ENUM ('CASH');
"

# Create Schemas
psql $POSTGRES_DB -c "
    CREATE SCHEMA IF NOT EXISTS machines_schema;
    CREATE SCHEMA IF NOT EXISTS orders_schema;
    CREATE SCHEMA IF NOT EXISTS payments_schema;
    CREATE SCHEMA IF NOT EXISTS products_schema;
"

# Create Tables
psql $POSTGRES_DB -c "
    CREATE TABLE IF NOT EXISTS products_schema.products(
        id UUID UNIQUE NOT NULL,
        name VARCHAR(320) NOT NULL,
        unit_price INT NOT NULL,
        CONSTRAINT pk_products_id PRIMARY KEY (id)
    );

    CREATE TABLE IF NOT EXISTS machines_schema.owners(
        id UUID UNIQUE NOT NULL,
        full_name TEXT NOT NULL,
        email VARCHAR(320) UNIQUE NOT NULL,
        CONSTRAINT pk_owner_id PRIMARY KEY (id)
    );

    CREATE TABLE IF NOT EXISTS machines_schema.machines(
        id UUID NOT NULL,
        owner_id UUID NOT NULL,
        state machine_state NOT NULL,
        coin_01_qty SMALLINT NOT NULL,
        coin_05_qty SMALLINT NOT NULL,
        coin_10_qty SMALLINT NOT NULL,
        coin_25_qty SMALLINT NOT NULL,
        coin_50_qty SMALLINT NOT NULL,
        coin_100_qty SMALLINT NOT NULL,
        CONSTRAINT pk_machine_id PRIMARY KEY (id)
    );

    CREATE TABLE IF NOT EXISTS machines_schema.machine_products(
        machine_id UUID NOT NULL,
        product_id UUID NOT NULL,
        product_qty INT NOT NULL,
        code VARCHAR(2) NOT NULL,
        CONSTRAINT fk_product_id FOREIGN KEY(product_id) REFERENCES products_schema.products(id) ON UPDATE CASCADE ON DELETE CASCADE,
        CONSTRAINT fk_machine_id FOREIGN KEY(machine_id) REFERENCES machines_schema.machines(id) ON UPDATE CASCADE ON DELETE CASCADE
    ) PARTITION BY LIST (machine_id);

    CREATE TABLE IF NOT EXISTS orders_schema.orders(
        id UUID NOT NULL,
        machine_id UUID NOT NULL,
        status order_status NOT NULL,
        total_amount INT NOT NULL,
        created_at TIMESTAMP NOT NULL,
        updated_at TIMESTAMP NOT NULL,
        CONSTRAINT pk_order_id PRIMARY KEY (id, created_at)
    ) PARTITION BY RANGE (created_at);

    CREATE TABLE IF NOT EXISTS orders_schema.order_items(
        id UUID NOT NULL,
        order_id UUID NOT NULL,
        product_id UUID NOT NULL,
        price INT NOT NULL,
        qty INT NOT NULL,
        created_at TIMESTAMP NOT NULL,
        CONSTRAINT pk_order_item_id_created_at PRIMARY KEY (id, created_at),
        CONSTRAINT fk_product_id FOREIGN KEY(product_id) REFERENCES products_schema.products(id) ON UPDATE CASCADE ON DELETE CASCADE
    ) PARTITION BY RANGE (created_at);

    CREATE TABLE IF NOT EXISTS payments_schema.payments(
        id UUID NOT NULL,
        order_id UUID NOT NULL,
        amount INT NOT NULL,
        payment_type payment_types NOT NULL,
        payment_date TIMESTAMP NOT NULL,
        CONSTRAINT pk_payment_id_payment_date PRIMARY KEY (id, payment_date)
    ) PARTITION BY RANGE (payment_date);

    CREATE TABLE IF NOT EXISTS payments_schema.cash_payments(
        id UUID NOT NULL,
        payment_id UUID NOT NULL,
        cash_tendered INT NOT NULL,
        change INT NOT NULL,
        payment_date TIMESTAMP NOT NULL,
        CONSTRAINT pk_cash_payment_id_payment_date PRIMARY KEY (id, payment_date),
        CONSTRAINT fk_payment_id_payment_date FOREIGN KEY(payment_id, payment_date) REFERENCES payments_schema.payments(id, payment_date) ON UPDATE CASCADE ON DELETE CASCADE,
        CONSTRAINT check_id_equal_payment_id CHECK (id = payment_id)
    ) PARTITION BY RANGE (payment_date);
"

# Create Indexes
psql $POSTGRES_DB -c "
    CREATE UNIQUE INDEX idx_btree_products_id ON products_schema.products USING BTREE (id);
    CREATE INDEX idx_hash_machines_id ON machines_schema.machines USING HASH (id);
    CREATE INDEX idx_hash_owners_id ON machines_schema.owners USING HASH (id);
    CREATE INDEX idx_btree_machine_products_product_id ON machines_schema.machine_products USING BTREE (product_id);
    CREATE INDEX idx_btree_orders_machine_id_id ON orders_schema.orders USING BTREE (machine_id, id);
    CREATE INDEX idx_btree_order_items_order_id_id ON orders_schema.order_items USING BTREE (order_id, id);
    CREATE INDEX idx_btree_payments_payment_date_id ON payments_schema.payments USING BTREE (payment_date, id);
    CREATE INDEX idx_btree_cash_payments_payment_date_id ON payments_schema.cash_payments USING BTREE (payment_date, id);
"

# Configure Patitioning
psql $POSTGRES_DB -c "
    SELECT partman.create_parent(
        p_parent_table := 'orders_schema.orders'
        , p_control := 'created_at'
        , p_interval := '1 month'
        , p_type := 'range'
        , p_premake := 3
        , p_start_partition := date_trunc('day', CURRENT_TIMESTAMP)::TEXT
        , p_template_table := 'orders_schema.orders'
    );

    SELECT partman.create_parent(
        p_parent_table := 'orders_schema.order_items'
        , p_control := 'created_at'
        , p_interval := '1 month'
        , p_type := 'range'
        , p_premake => 3
        , p_start_partition := date_trunc('day', CURRENT_TIMESTAMP)::TEXT
        , p_template_table := 'orders_schema.order_items'
    );

    SELECT partman.create_parent(
        p_parent_table => 'payments_schema.payments'
        , p_control => 'payment_date'
        , p_interval => '1 month'
        , p_type => 'range'
        , p_premake => 3
        , p_start_partition := date_trunc('day', CURRENT_TIMESTAMP)::TEXT
        , p_template_table := 'payments_schema.payments'
    );

    SELECT partman.create_parent(
        p_parent_table => 'payments_schema.cash_payments'
        , p_control => 'payment_date'
        , p_interval => '1 month'
        , p_type => 'range'
        , p_premake => 3
        , p_start_partition := date_trunc('day', CURRENT_TIMESTAMP)::TEXT
        , p_template_table := 'payments_schema.cash_payments'
    );

    UPDATE partman.part_config
    SET infinite_time_partitions = true,
        retention_keep_table = true
    WHERE parent_table = 'orders_schema.orders' OR
        parent_table = 'orders_schema.order_items' OR
        parent_table = 'payments_schema.payments' OR
        parent_table = 'payments_schema.cash_payments';
"

# Run Cron Jobs
psql $POSTGRES_DB -c "
    SELECT cron.schedule('orders_partition_maintainer_job', '0 0 $ * *', 'SELECT partman.run_maintenance(p_parent_table := ''orders_schema.orders'', p_analyze := false)');
    SELECT cron.schedule('order_items_partition_maintainer_job', '0 0 $ * *', 'SELECT partman.run_maintenance(p_parent_table := ''orders_schema.order_items'', p_analyze := false)');
    SELECT cron.schedule('payments_partition_maintainer_job', '0 0 $ * *', 'SELECT partman.run_maintenance(p_parent_table := ''payments_schema.payments'', p_analyze := false)');
    SELECT cron.schedule('cash_payments_partition_maintainer_job', '0 0 $ * *', 'SELECT partman.run_maintenance(p_parent_table := ''payments_schema.cash_payments'', p_analyze := false)');
    SELECT cron.schedule('clean_jobs_log_job', '0 0 * * *', 'DELETE FROM cron.job_run_details WHERE end_time < now() - interval ''7 days''');
"

# Insert Products
psql $POSTGRES_DB -c "
    INSERT INTO products_schema.products (id, name, unit_price) VALUES ('223e4567-e89b-12d3-a456-426614174003', 'Pepsi', 150);
    INSERT INTO products_schema.products (id, name, unit_price) VALUES ('223e4567-e89b-12d3-a456-426614174004', 'Butterfinger', 50);
    INSERT INTO products_schema.products (id, name, unit_price) VALUES ('223e4567-e89b-12d3-a456-426614174005', 'Hershey''s', 75);
    INSERT INTO products_schema.products (id, name, unit_price) VALUES ('223e4567-e89b-12d3-a456-426614174006', 'Twix Candy Bars', 95);
"

# Super User Functions
psql $POSTGRES_DB -c "
    CREATE TYPE product_type AS (
        id UUID,
        name VARCHAR(320),
        unit_price INT,
        qty INT
    );

    CREATE TYPE owner_type AS (
        id UUID,
        full_name TEXT,
        email VARCHAR(320)
    );

    CREATE TYPE machine_type AS (
        id UUID,
        state machine_state,
        coin_01_qty SMALLINT,
        coin_05_qty SMALLINT,
        coin_10_qty SMALLINT,
        coin_25_qty SMALLINT,
        coin_50_qty SMALLINT,
        coin_100_qty SMALLINT
    );

    CREATE OR REPLACE FUNCTION fn_create_machine_partition(machine machine_type, owner owner_type, products product_type[])
    RETURNS VOID AS \$\$
    DECLARE
        i INT;
        owner_row machines_schema.owners;
        machine_row machines_schema.machines;
        schema_name TEXT;
        table_name TEXT;
        partition_name TEXT;
        new_partition_name TEXT;
    BEGIN
        IF array_length(products, 1) IS NULL THEN
            RAISE EXCEPTION 'no products to insert';
        END IF;

        IF array_length(products, 1) > 99 THEN
            RAISE EXCEPTION 'too many products to register';
        END IF;

        IF owner IS NULL THEN
            RAISE EXCEPTION 'no owner specified';
        END IF;

        IF machine IS NULL THEN
            RAISE EXCEPTION 'no machine specified';
        END IF;

        SELECT * INTO owner_row FROM machines_schema.owners WHERE id = owner.id LIMIT 1;

        SELECT * INTO machine_row FROM machines_schema.machines WHERE id = machine.id LIMIT 1;

        CASE
            WHEN machine_row.id IS NOT NULL THEN
                RAISE EXCEPTION 'machine with id: % - already exists', machine.id;
            ELSE
                SELECT * INTO owner_row FROM machines_schema.owners WHERE id = owner.id LIMIT 1;

                IF owner_row.id IS NULL THEN
                    INSERT INTO machines_schema.owners (id, full_name, email) VALUES (owner.id, owner.full_name, owner.email);
                END IF;

                INSERT INTO machines_schema.machines (
                    id,
                    owner_id,
                    state,
                    coin_01_qty,
                    coin_05_qty,
                    coin_10_qty,
                    coin_25_qty,
                    coin_50_qty,
                    coin_100_qty
                ) VALUES (
                    machine.id,
                    owner.id,
                    machine.state,
                    machine.coin_01_qty,
                    machine.coin_05_qty,
                    machine.coin_10_qty,
                    machine.coin_25_qty,
                    machine.coin_50_qty,
                    machine.coin_100_qty
                );

                schema_name := 'machines_schema';
                table_name := 'machine_products';
                partition_name := schema_name || '.' || table_name;
                new_partition_name := schema_name || '.' || table_name || '_' || REPLACE(machine.id::TEXT, '-', '');

                EXECUTE format(
                    'CREATE TABLE %s PARTITION OF %s FOR VALUES IN (''%s'')',
                    new_partition_name, partition_name, machine.id
                );

                FOR i IN 1..array_length(products, 1) LOOP
                    INSERT INTO machines_schema.machine_products (
                        machine_id,
                        product_id,
                        product_qty,
                        code
                    ) VALUES (
                        machine.id,
                        products[i].id,
                        products[i].qty,
                        LPAD(CAST(i AS VARCHAR), 2, '0')
                    );
                END LOOP;
        END CASE;
    END;
    \$\$ LANGUAGE plpgsql;
"

# Grant Permissions
psql $POSTGRES_DB -c "
    GRANT CONNECT ON DATABASE $POSTGRES_DB TO $POSTGRES_APP_USER;

    GRANT USAGE ON SCHEMA machines_schema TO $POSTGRES_APP_USER;
    GRANT USAGE ON SCHEMA orders_schema TO $POSTGRES_APP_USER;
    GRANT USAGE ON SCHEMA payments_schema TO $POSTGRES_APP_USER;
    GRANT USAGE ON SCHEMA products_schema TO $POSTGRES_APP_USER;

    GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA machines_schema TO $POSTGRES_APP_USER;
    GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA orders_schema TO $POSTGRES_APP_USER;
    GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA payments_schema TO $POSTGRES_APP_USER;
    GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA products_schema TO $POSTGRES_APP_USER;
"
