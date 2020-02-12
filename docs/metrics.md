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

Role          |             System |               Site | Description
--------------|--------------------|--------------------|-------------
Administrator |                :x: | :heavy_check_mark: | Administrators can affect any data in the data model, which means they can add/remove Users, Systems, Components, and read or write Snapshot data.
Observer      | :heavy_check_mark: | :heavy_check_mark: | Site Observers can read data from any tables.  System Observers can read data from the System, Component, and Snapshot tables.
Reporter      | :heavy_check_mark: |                :x: | Reporters can insert data into the System, Component, and Snapshot tables.
Owner         | :heavy_check_mark: |                :x: |Owners are System Observers and Reporters, and can also insert and update data in the System and Component tables for systems they own.

---

### Systems

Individual Systems, or Hosts, in taskobra are represented by multiple tables.
The root is the `System` table which contains an ID, the owner's ID, and a system
name.  Other information about the System is determined compositionally by querying
through the associative `SystemComponent` table.  The `SystemComponent` table represents
a many to many relationship between System IDs and Abstract Component IDs.

---

### Components

The gatekeeper to Component identification is the `ComponentType` table, which contains
a mapping of Abstract Component ID to Concrete Component ID and Type.  The Abstract
Component ID is a generic ID of the component without any knowledge of the type.  The
Concrete Component ID is the ID of a Component of known type.  There is a table for
each type of component that taskobra takes measurements of.  These are indexed by
Concrete Component ID.

|               CPU |          GPU |       Memory |      Network Adapter |            Storage |
|-------------------|--------------|--------------|----------------------|--------------------|
|      Manufacturer | Manufacturer | Manufacturer |         Manufacturer |       Manufacturer |
|             Model |        Model |     Capacity |                 Type |           Capacity |
|               ISA | Architecture |      Timings |          MAC Address | Maximum Write Rate |
|               TDP |          TDP |    Frequency |    Maximum Send Rate | Maximum Read Rate  |
|             Cores |        Cores |              | Maximum Receive Rate |                    |
|      Threads/Core |       Memory |              |                      |                    |
| Maximum Frequency |              |              |                      |                    |
| Minimum Frequency |              |              |                      |                    |

For each component type, there are defined metrics with specific formats.  These metrics are
each associated with a snapshot ID and Concrete Component ID.

---

### Snapshots

Snapshots are a collection of metrics representing the host System's
state at a specific time.  Each Snapshot contains a System ID and
timestamp, and is associated with a set of records in the Metrics
tables for each Component type.

---

### Metrics

Metrics are simple data points which contain a Snapshot ID,
Component ID, and some number of values, depending on their
specific format.  Metrics are the building blocks of all the
views available in the [Web Front-End](webui.md).  For example,
the total system CPU utilization can be computed by taking the
mean of the all `CpuUtilization` metrics for a given Snapshot
across each Core and Thread in a system.

#### CPU Metrics

| CPU Utilization | CPU Frequency | CPU Temperature |
|-----------------|---------------|-----------------|
|     Snapshot ID |   Snapshot ID |     Snapshot ID |
|          CPU ID |        CPU ID |          CPU ID |
|            Core |          Core |                 |
|          Thread |               |                 |
|           Value |         Value |           Value |

#### GPU Metrics

| GPU Utilization | GPU Temperature |
|-----------------|-----------------|
|     Snapshot ID |     Snapshot ID |
|          GPU ID |          GPU ID |
|           Value |           Value |

#### Memory Metrics

| Memory Used | Memory Commit | Memory Paged |
|-------------|---------------|--------------|
| Snapshot ID |   Snapshot ID |  Snapshot ID |
|   Memory ID |     Memory ID |    Memory ID |
|       Value |         Value |        Value |

#### Network Adapter Metrics

|          Send Rate |       Receive Rate |
|--------------------|--------------------|
|        Snapshot ID |        Snapshot ID |
| Network Adapter ID | Network Adapter ID |
|              Value |              Value |

#### Storage Metrics

|   Read Rate |  Write Rate |
|-------------|-------------|
| Snapshot ID | Snapshot ID |
|  Storage ID |  Storage ID |
|       Value |       Value |

---

## Pruning?

---

## Metrics Monitoring Lib (PSUTIL)
