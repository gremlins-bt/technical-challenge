-- Schema initialization for DevOps Technical Challenge
CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    item VARCHAR(200) NOT NULL,
    amount NUMERIC(10, 2) NOT NULL,
    status VARCHAR(50) DEFAULT 'PENDING',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Seed initial test orders
INSERT INTO orders (customer_name, item, amount, status) VALUES
('Alex Tech', 'Kubernetes Cluster (3 nodes)', 299.00, 'COMPLETED'),
('DevOps Corp', 'Enterprise CI/CD Runner', 129.50, 'PROCESSING'),
('SRE Solutions', 'Prometheus Monitoring Pack', 79.99, 'PENDING');
