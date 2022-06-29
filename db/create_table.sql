CREATE TABLE invoice_audit (
id                          BIGSERIAL   NOT NULL PRIMARY KEY,
created_at                  TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
updated_at                  TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
invoice_id                  TEXT        NOT NULL,
payment_hash                TEXT        NOT NULL,
sender                      TEXT        NOT NULL,
recipient                   TEXT        NOT NULL,
action                      TEXT        NOT NULL,
amount                      BIGINT      NOT NULL,
status                      TEXT        NOT NULL,
UNIQUE(sender, payment_hash, invoice_id)
);
