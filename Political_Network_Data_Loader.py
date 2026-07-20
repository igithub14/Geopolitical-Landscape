# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "5"
# ///
# DBTITLE 1,Create Catalog and Schema
# MAGIC %sql
# MAGIC -- Create catalog and schema for geopolitical data
# MAGIC CREATE CATALOG IF NOT EXISTS geopolitics_data_catalog;
# MAGIC
# MAGIC CREATE SCHEMA IF NOT EXISTS geopolitics_data_catalog.processed
# MAGIC COMMENT 'Processed data for political power structure and network analysis';
# MAGIC
# MAGIC -- Verify creation
# MAGIC SHOW SCHEMAS IN geopolitics_data_catalog;

# COMMAND ----------

# DBTITLE 1,Create Institutional Hierarchy Table
# MAGIC %sql
# MAGIC -- Italian institutional hierarchy: President → Government → Ministries → Agencies
# MAGIC CREATE OR REPLACE TABLE geopolitics_data_catalog.processed.institutional_hierarchy (
# MAGIC   institution_id STRING NOT NULL,
# MAGIC   institution_name STRING NOT NULL,
# MAGIC   parent_id STRING COMMENT 'NULL for root (President of Republic)',
# MAGIC   institution_type STRING NOT NULL COMMENT 'executive, legislative, judicial, agency',
# MAGIC   level INT NOT NULL COMMENT '1=top level, 2=second tier, etc.',
# MAGIC   description STRING
# MAGIC )
# MAGIC USING DELTA
# MAGIC COMMENT 'Italian institutional command chain and organizational structure';
# MAGIC
# MAGIC -- Verify table structure
# MAGIC DESCRIBE EXTENDED geopolitics_data_catalog.processed.institutional_hierarchy;

# COMMAND ----------

# DBTITLE 1,Create Leader Relationships Table
# MAGIC %sql
# MAGIC -- Political relationships: leaders, ministers, advisors, coalition partners
# MAGIC CREATE OR REPLACE TABLE geopolitics_data_catalog.processed.leader_relationships (
# MAGIC   from_leader STRING NOT NULL,
# MAGIC   to_leader STRING NOT NULL,
# MAGIC   relationship_type STRING NOT NULL COMMENT 'advisor, minister, coalition_partner, successor, deputy',
# MAGIC   strength INT NOT NULL COMMENT '1-10 scale for edge thickness in visualization',
# MAGIC   start_date DATE NOT NULL,
# MAGIC   end_date DATE COMMENT 'NULL for current relationships'
# MAGIC )
# MAGIC USING DELTA
# MAGIC COMMENT 'Network of political relationships in Italian government';
# MAGIC
# MAGIC -- Verify table structure
# MAGIC DESCRIBE EXTENDED geopolitics_data_catalog.processed.leader_relationships;

# COMMAND ----------

# DBTITLE 1,Populate Institutional Hierarchy - Italian Government
# MAGIC %sql
# MAGIC -- Insert Italian institutional hierarchy data
# MAGIC -- Level 1: President of the Republic
# MAGIC INSERT INTO geopolitics_data_catalog.processed.institutional_hierarchy VALUES
# MAGIC ('PRES_REP', 'Presidency of the Republic', NULL, 'executive', 1, 'Head of State - Sergio Mattarella'),
# MAGIC
# MAGIC -- Level 2: Prime Minister and Parliament
# MAGIC ('PM', 'Prime Minister Office', 'PRES_REP', 'executive', 2, 'Head of Government - Giorgia Meloni'),
# MAGIC ('SENATE', 'Senate of the Republic', 'PRES_REP', 'legislative', 2, 'Upper chamber of Parliament'),
# MAGIC ('CHAMBER', 'Chamber of Deputies', 'PRES_REP', 'legislative', 2, 'Lower chamber of Parliament'),
# MAGIC
# MAGIC -- Level 3: Key Ministries
# MAGIC ('MIN_FA', 'Ministry of Foreign Affairs', 'PM', 'executive', 3, 'Antonio Tajani - Foreign policy and EU relations'),
# MAGIC ('MIN_INT', 'Ministry of Interior', 'PM', 'executive', 3, 'Matteo Piantedosi - Public security and immigration'),
# MAGIC ('MIN_ECO', 'Ministry of Economy and Finance', 'PM', 'executive', 3, 'Giancarlo Giorgetti - Economic policy and budget'),
# MAGIC ('MIN_DEF', 'Ministry of Defence', 'PM', 'executive', 3, 'Guido Crosetto - National defense and armed forces'),
# MAGIC ('MIN_JUS', 'Ministry of Justice', 'PM', 'executive', 3, 'Carlo Nordio - Justice system and penitentiary'),
# MAGIC ('MIN_EDU', 'Ministry of Education', 'PM', 'executive', 3, 'Giuseppe Valditara - Education policy'),
# MAGIC ('MIN_INF', 'Ministry of Infrastructure', 'PM', 'executive', 3, 'Matteo Salvini - Transport and infrastructure'),
# MAGIC
# MAGIC -- Level 4: Key Agencies
# MAGIC ('AISE', 'External Intelligence Agency', 'MIN_FA', 'agency', 4, 'Foreign intelligence service'),
# MAGIC ('AISI', 'Internal Intelligence Agency', 'MIN_INT', 'agency', 4, 'Domestic intelligence service'),
# MAGIC ('BANK_IT', 'Bank of Italy', 'MIN_ECO', 'agency', 4, 'Central bank and financial supervision');
# MAGIC
# MAGIC -- Verify data
# MAGIC SELECT * FROM geopolitics_data_catalog.processed.institutional_hierarchy
# MAGIC ORDER BY level, institution_id;

# COMMAND ----------

# DBTITLE 1,Populate Leader Relationships - Coalition & Cabinet
# MAGIC %sql
# MAGIC -- Insert political relationships: Meloni government + coalition
# MAGIC -- Coalition partners (Meloni leads coalition of 3 parties)
# MAGIC INSERT INTO geopolitics_data_catalog.processed.leader_relationships VALUES
# MAGIC ('Giorgia Meloni', 'Antonio Tajani', 'coalition_partner', 9, '2022-10-22', NULL),  -- Forza Italia leader
# MAGIC ('Giorgia Meloni', 'Matteo Salvini', 'coalition_partner', 8, '2022-10-22', NULL),  -- Lega leader
# MAGIC
# MAGIC -- Ministers appointed by PM
# MAGIC ('Giorgia Meloni', 'Matteo Piantedosi', 'minister', 10, '2022-10-22', NULL),
# MAGIC ('Giorgia Meloni', 'Giancarlo Giorgetti', 'minister', 10, '2022-10-22', NULL),
# MAGIC ('Giorgia Meloni', 'Guido Crosetto', 'minister', 9, '2022-10-22', NULL),
# MAGIC ('Giorgia Meloni', 'Carlo Nordio', 'minister', 8, '2022-10-22', NULL),
# MAGIC ('Giorgia Meloni', 'Giuseppe Valditara', 'minister', 7, '2022-10-22', NULL),
# MAGIC
# MAGIC -- Ministers from coalition partners
# MAGIC ('Antonio Tajani', 'Giancarlo Giorgetti', 'coalition_minister', 8, '2022-10-22', NULL),  -- Forza Italia to Economy
# MAGIC ('Matteo Salvini', 'Matteo Piantedosi', 'coalition_minister', 7, '2022-10-22', NULL),  -- Lega influence on Interior
# MAGIC
# MAGIC -- Deputy relationships
# MAGIC ('Giorgia Meloni', 'Antonio Tajani', 'deputy', 9, '2022-10-22', NULL),  -- Deputy PM
# MAGIC ('Giorgia Meloni', 'Matteo Salvini', 'deputy', 9, '2022-10-22', NULL),  -- Deputy PM
# MAGIC
# MAGIC -- Key advisors
# MAGIC ('Giorgia Meloni', 'Giovanbattista Fazzolari', 'advisor', 10, '2022-10-22', NULL),  -- Undersecretary to PM
# MAGIC ('Giorgia Meloni', 'Alfredo Mantovano', 'advisor', 9, '2022-10-22', NULL),  -- Undersecretary to PM
# MAGIC
# MAGIC -- Cross-ministry coordination
# MAGIC ('Giancarlo Giorgetti', 'Matteo Salvini', 'coordination', 6, '2022-10-22', NULL),  -- Economy-Infrastructure
# MAGIC ('Guido Crosetto', 'Matteo Piantedosi', 'coordination', 7, '2022-10-22', NULL),  -- Defense-Interior
# MAGIC
# MAGIC -- Presidential oversight (institutional, not political)
# MAGIC ('Sergio Mattarella', 'Giorgia Meloni', 'institutional_oversight', 10, '2022-10-22', NULL);
# MAGIC
# MAGIC -- Verify data
# MAGIC SELECT * FROM geopolitics_data_catalog.processed.leader_relationships
# MAGIC ORDER BY strength DESC, from_leader;

# COMMAND ----------

# DBTITLE 1,Validation Queries - Data Quality Check
# MAGIC %sql
# MAGIC -- Validation query 1: Institutional hierarchy levels and counts
# MAGIC SELECT 
# MAGIC   level,
# MAGIC   institution_type,
# MAGIC   COUNT(*) as institution_count
# MAGIC FROM geopolitics_data_catalog.processed.institutional_hierarchy
# MAGIC GROUP BY level, institution_type
# MAGIC ORDER BY level;
# MAGIC
# MAGIC -- Validation query 2: Relationship types and strength distribution
# MAGIC SELECT 
# MAGIC   relationship_type,
# MAGIC   COUNT(*) as relationship_count,
# MAGIC   AVG(strength) as avg_strength,
# MAGIC   MIN(strength) as min_strength,
# MAGIC   MAX(strength) as max_strength
# MAGIC FROM geopolitics_data_catalog.processed.leader_relationships
# MAGIC GROUP BY relationship_type
# MAGIC ORDER BY relationship_count DESC;
# MAGIC
# MAGIC -- Validation query 3: Top 5 most connected leaders (for network centrality)
# MAGIC SELECT 
# MAGIC   from_leader,
# MAGIC   COUNT(*) as outgoing_connections,
# MAGIC   AVG(strength) as avg_relationship_strength
# MAGIC FROM geopolitics_data_catalog.processed.leader_relationships
# MAGIC GROUP BY from_leader
# MAGIC ORDER BY outgoing_connections DESC
# MAGIC LIMIT 5;

# COMMAND ----------

# DBTITLE 1,Preview Data for Dashboard
# MAGIC %sql
# MAGIC -- Preview institutional hierarchy (for tree layout)
# MAGIC SELECT 
# MAGIC   institution_id,
# MAGIC   institution_name,
# MAGIC   parent_id,
# MAGIC   institution_type,
# MAGIC   level,
# MAGIC   description
# MAGIC FROM geopolitics_data_catalog.processed.institutional_hierarchy
# MAGIC ORDER BY level, institution_name;
# MAGIC
# MAGIC -- Preview leader relationships (for force-directed network)
# MAGIC SELECT 
# MAGIC   from_leader,
# MAGIC   to_leader,
# MAGIC   relationship_type,
# MAGIC   strength,
# MAGIC   start_date
# MAGIC FROM geopolitics_data_catalog.processed.leader_relationships
# MAGIC WHERE end_date IS NULL  -- Only current relationships
# MAGIC ORDER BY strength DESC, from_leader;