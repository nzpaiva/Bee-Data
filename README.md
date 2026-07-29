# 🐝 BeeData – Precision Beekeeping Database

BeeData is a relational database project developed to support **precision beekeeping** by integrating operational, environmental, and production data into a single information system.

The project was developed as part of the **Database Systems** course at the University of São Paulo (USP) and covers the complete database design process, from requirements analysis to the relational schema.

---

## Project Overview

The objective of BeeData is to provide a robust database capable of managing information related to:

- Apiaries
- Beehives
- Environmental sensors
- Meteorological data
- Beekeeping interventions
- Honey production batches
- Inventory and supplies
- Quality control
- Technical reports
- Employees and auditors

The system emphasizes **traceability**, allowing users to follow the complete production chain from raw materials to final honey batches.

## Features

- Entity-Relationship (ER) Modeling
- Relational Database Design
- Weak Entities
- Generalization / Specialization
- Business Rules
- Referential Integrity
- Historical Data Storage
- Production Traceability

## Database Design

The project was developed following a structured database design methodology:

1. Requirements Analysis
2. Conceptual Modeling (ER Diagram)
3. Logical Modeling
4. Relational Schema
5. Mapping Justifications
6. Business Rules
7. SQL Implementation

## Main Entities

Some of the principal entities include:

- Apiary
- Beehive
- Sensor
- Sensor Data
- Meteorological Data
- Product
- Supply
- Production Batch
- Intervention
- Report
- Employee
- Auditor

The database also models multiple inheritance hierarchies and weak entities to preserve semantic consistency and reduce redundancy.

---

## Technologies

- Oracle SQL
- Relational Database Modeling
- Draw.io (ER diagrams)
- SQL Developer

---

## Project Structure

```
BeeData/
│
├── Documentation/
│   ├── BeeData___Apicultura_de_Precisão_entrega_parte_3.pdf
│   ├── projeto_lógico.drawio
│   
├── SQL/
│   ├── esquema.sql
│   ├── consultas.sql
│   ├── dados.sql
│   
├── Python/
│   ├── main.py
│   ├── application.py
│   ├── validador.py
│   
└── README.md
```

---

## Highlights

The database incorporates several advanced modeling concepts, including:

- Weak entities
- Composite keys
- Artificial keys
- Generalization and specialization
- Derived attributes
- Optional and mandatory participation
- N:M relationship mapping
- Referential integrity constraints
- Traceability of production batches
- Historical sensor data

Special attention was given to preserving data consistency through appropriate relational modeling, integrity constraints, and a design that supports future system expansion.

---

## Learning Outcomes

Through this project, I gained practical experience with:

- Relational database design
- Oracle SQL
- Entity-Relationship modeling
- Business rule translation into relational schemas
- Data integrity constraints
- Database documentation

---

## Authors

**Nicolas Zafred Paiva**, 
**Álvaro Minto Ramos**, 
**Leonardo Mendes De Souza Maciel**,
**Vinicius Henrique Pereira Giroto**
