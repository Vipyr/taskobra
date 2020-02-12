# Metrics 

## Data Model 

< Insert ORM Diagram Here > 

## Sampling Methodology
Taskobra's data model both simple and robust.  There are five
main parts:
1. Users
1. Roles
1. Systems
1. Components
1. Snapshots
1. Metrics

Systems have an owning User, and are composed of Components.
Snapshots have a timestamp and system ID, and are composed of Metrics.
Metrics have a type, value, and componenent ID.

### User
Users represent an individual 

### Role
- Administrator
- Owner
- Reporter
- Observer

### System

### Component

### Snapshot

### Metric

### Associative Tables
1. UserRole
    - User
    - Role (Administrator, Observer)
1. UserSystemRole
    - User
    - System
    - Role (Owner, Reporter, Observer)

The foundation of the data model is the snapshot.  Each snapshot
is a collection of metrics, measured at the same time.  Metrics
are simple data points which contain a type, value, and are
associated with component.  The type and component can be used
to determine how the value is interpreted.

## Pruning?


## Metrics Monitoring Lib (PSUTIL) 

