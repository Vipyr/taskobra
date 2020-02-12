# Metrics

## Data Model

![Data Model](images/ORM.svg)

## Sampling Methodology

Taskobra's data model both simple and robust.  There are five
main parts:
1. Users
1. Roles
1. Systems
1. Components
1. Snapshots
1. Metrics

---

### Users

User representation is kept simple, with a username and [OAuth](./auth.md) token.
Users can be assigned Roles at the site level or the system level.

---

### Roles

There are two types of Role available to Users in taskobra.  The first is Site
Roles, which apply to the entire data model.  The second is System Roles, which
apply to the data for a particular System.  There are four Roles different:
Administrator, Observer, Reporter, and Owner.

Role          |       System       |        Site        | Description
--------------|--------------------|--------------------|-------------
Administrator |         :x:        | :heavy_check_mark: | Administrators can affect any data in the data model, which means they can add/remove Users, Systems, Components, and read or write Snapshot data.
Observer      | :heavy_check_mark: | :heavy_check_mark: | Site Observers can read data from any tables.  System Observers can read data from the System, Component, and Snapshot tables.
Reporter      | :heavy_check_mark: |         :x:        | Reporters can insert data into the System, Component, and Snapshot tables.
Owner         | :heavy_check_mark: |         :x:        |Owners are System Observers and Reporters, and can also insert and update data in the System and Component tables for systems they own.

---

### Systems

Individual Systems, or Hosts, in taskobra are represented by a couple of tables.
The root is the System table which contains an ID, the owner's ID, and a system
name.  Other information about the System is determined compositionally by querying
through the associative SystemComponent table.  The SystemComponent table represents
a many to many relationship between System IDs and Component IDs.

---

### Components



---

### Snapshots

---

### Metrics

The foundation of the data model is the snapshot.  Each snapshot
is a collection of metrics, measured at the same time.  Metrics
are simple data points which contain a type, value, and are
associated with component.  The type and component can be used
to determine how the value is interpreted.

---

## Pruning?

---

## Metrics Monitoring Lib (PSUTIL)

