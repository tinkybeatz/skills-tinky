# PostgreSQL migration patterns (zero-downtime)

## 1. Adding a column with backfill

```sql
-- Step 1: Add the column (instant since PG11)
ALTER TABLE orders ADD COLUMN total_cents BIGINT DEFAULT 0 NOT NULL;

-- Step 2: Backfill in batches (if the value depends on existing data)
UPDATE orders SET total_cents = amount * 100
WHERE total_cents = 0
AND id BETWEEN 1 AND 100000;
-- Repeat in slices of 100k

-- Step 3: Add the constraint if needed
ALTER TABLE orders ADD CONSTRAINT orders_total_cents_positive
  CHECK (total_cents >= 0) NOT VALID;
ALTER TABLE orders VALIDATE CONSTRAINT orders_total_cents_positive;
```

**Why in batches:** a single UPDATE over 10M rows takes a long lock and generates a huge WAL. In batches of 100k, each transaction is short.

---

## 2. Renaming a column without downtime

Never `ALTER TABLE RENAME COLUMN` in production while the app is running — code that references the old name will break.

```sql
-- Step 1: Add the new column
ALTER TABLE users ADD COLUMN full_name TEXT;

-- Step 2: Sync trigger (temporary)
CREATE OR REPLACE FUNCTION sync_user_name() RETURNS trigger AS $$
BEGIN
  IF TG_OP = 'INSERT' OR NEW.name IS DISTINCT FROM OLD.name THEN
    NEW.full_name := NEW.name;
  END IF;
  IF TG_OP = 'INSERT' OR NEW.full_name IS DISTINCT FROM OLD.full_name THEN
    NEW.name := NEW.full_name;
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_sync_user_name
  BEFORE INSERT OR UPDATE ON users
  FOR EACH ROW EXECUTE FUNCTION sync_user_name();

-- Step 3: Backfill the old rows
UPDATE users SET full_name = name WHERE full_name IS NULL;
-- In batches if the volume is large

-- Step 4: Deploy the code that uses full_name
-- Step 5: Once the old code is no longer deployed anywhere:
DROP TRIGGER trg_sync_user_name ON users;
DROP FUNCTION sync_user_name();
ALTER TABLE users DROP COLUMN name;
```

---

## 3. Changing a column type

`ALTER TABLE ALTER COLUMN TYPE` takes an ACCESS EXCLUSIVE lock and rewrites the table if the cast is not binary-compatible.

**Binary-compatible casts (no rewrite):**
- `VARCHAR(N)` → `VARCHAR(M)` where M > N
- `VARCHAR(N)` → `TEXT`
- `INTEGER` → `BIGINT` (**warning: rewrites the table**)

**Safe pattern for incompatible changes:**

```sql
-- Same pattern as the rename: new column + trigger + backfill + switch
ALTER TABLE products ADD COLUMN price_cents BIGINT;

-- Conversion trigger
CREATE OR REPLACE FUNCTION sync_product_price() RETURNS trigger AS $$
BEGIN
  NEW.price_cents := (NEW.price * 100)::BIGINT;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_sync_product_price
  BEFORE INSERT OR UPDATE ON products
  FOR EACH ROW EXECUTE FUNCTION sync_product_price();

-- Backfill
UPDATE products SET price_cents = (price * 100)::BIGINT
WHERE price_cents IS NULL;

-- After deploying the new code:
-- DROP the old column
```

---

## 4. Adding an index on a large table

```sql
-- ALWAYS CONCURRENTLY in production
CREATE INDEX CONCURRENTLY idx_orders_customer_id
  ON orders (customer_id);

-- If the index fails (interrupted, out of disk):
-- it stays in an INVALID state
-- Check: SELECT * FROM pg_indexes WHERE indexname = 'idx_orders_customer_id';
-- If invalid: DROP INDEX idx_orders_customer_id; and recreate
```

**Estimated time:** ~1 min per million rows on SSD (varies with column size and load).

---

## 5. Adding a NOT NULL constraint on an existing column

```sql
-- Step 1: Add the CHECK constraint as NOT VALID (instant)
ALTER TABLE users ADD CONSTRAINT users_email_not_null
  CHECK (email IS NOT NULL) NOT VALID;

-- Step 2: Validate the constraint (scans the table, but without an exclusive lock)
ALTER TABLE users VALIDATE CONSTRAINT users_email_not_null;

-- Step 3 (optional): Replace with a real NOT NULL
-- Since PG12, if a CHECK (col IS NOT NULL) VALID exists,
-- ALTER TABLE ALTER COLUMN SET NOT NULL is instant
ALTER TABLE users ALTER COLUMN email SET NOT NULL;
ALTER TABLE users DROP CONSTRAINT users_email_not_null;
```

---

## 6. Partitioning an existing table

This is the heaviest migration. There is no in-place conversion.

```sql
-- 1. Create the partitioned table
CREATE TABLE orders_new (
  LIKE orders INCLUDING ALL
) PARTITION BY RANGE (created_at);

-- 2. Create the partitions
CREATE TABLE orders_2024 PARTITION OF orders_new
  FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');
CREATE TABLE orders_2025 PARTITION OF orders_new
  FOR VALUES FROM ('2025-01-01') TO ('2026-01-01');
CREATE TABLE orders_default PARTITION OF orders_new DEFAULT;

-- 3. Copy the data (in batches or in a maintenance window)
INSERT INTO orders_new SELECT * FROM orders;

-- 4. Switch (in a short maintenance window)
BEGIN;
ALTER TABLE orders RENAME TO orders_old;
ALTER TABLE orders_new RENAME TO orders;
COMMIT;

-- 5. Verify + DROP orders_old after validation
```

---

## 7. Empty migration template

```sql
-- Migration: NNN_description.sql
-- Description:
-- Author:
-- Date:

BEGIN;

-- ==================== UP ====================



-- ==================== DOWN (rollback) ====================
--

COMMIT;
```
