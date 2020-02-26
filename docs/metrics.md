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

Role          |        System/Host |           Taskobra | Description
--------------|--------------------|--------------------|-------------
Administrator | :heavy_check_mark: | :heavy_check_mark: | System/Host Administrators are System Observers and Reporters, and can also insert and update data in the System and Component tables for systems they own.<br/>Taskobra Administrators can affect any data in the data model, which means they can add/remove Users, Systems, Components, and read or write Snapshot data.
Observer      | :heavy_check_mark: | :heavy_check_mark: | Taskobra Observers can read data from any tables.<br/>System/Host Observers can read data from the System, Component, and Snapshot tables.
Reporter      | :heavy_check_mark: |                :x: | Reporters can insert data into the System, Component, and Snapshot tables.

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

For each component type, there are defined metrics with specific formats.
These metrics are each associated with a snapshot ID and Concrete Component ID.

---

### Snapshots

Snapshots are a collection of metrics representing the host System's
state at a specific time.  Each Snapshot contains a System ID and
timestamp, and is associated with a set of records in the Metrics
tables for each Component type.  Because we periodically prune the
backend database, snapshots need to be aware of the period of time
they cover, which is represented as a base and an exponent.  These
are used during pruning to figure out how many data points to prune.

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

## Pruning

When analyzing performance or debugging problems, down to the second data is
important to have.  On the other hand, looking at system and pool performance
trends requires data to persist for long periods of time, but doesn't need
frequent samples.  Rather than store a linear set of samples, taskobra can
be configured to automatically compress aging data.

We use a logarithmic scale to calculate averages, combining multiple snapshots
into one.  This time period can be represented by a base and an exponent.  Raw
snapshot data generally is reported with an exponent of 0 and a Reporter
configurable base. For example, the following snapshots are 1 second apart,
with base 3 pruning.

| Snapshot |  User | System | Time | Base | Exponent |
|----------|-------|--------|------|------|----------|
|        0 |    42 |    314 | 1000 |    3 |        0 |
|        1 |    42 |    314 | 1001 |    3 |        0 |
|        2 |    42 |    314 | 1002 |    3 |        0 |

After applying the pruning algorithm, the snapshot table would look
something like this:

| Snapshot |  User | System | Time | Base | Exponent |
|----------|-------|--------|------|------|----------|
|        3 |    42 |    314 | 1001 |    3 |        1 |

Pruned snapshots cover <code>Base<sup>Exponent</sup></code> seconds,
with a Timestamp in the center of that range, and contain an average
of all the snapshots they were generated from.

---

## Metrics Monitoring

### Using [psutil](https://psutil.readthedocs.io/en/latest/)

Python's `psutil` is a mature, well supported, cross-platform library that
provides system information and statistics.  Statistic availability is
not the same across all platforms, for instance temperatures are only
available in Linux and FreeBSD, and fan speeds only in Linux and MacOS.
Our ORM is resilient to missing data, since snapshots are composed of
entries from many snapshot type tables.  A missing entry simply means
the query returns no items, and presentation of that fact can be made
clear to users on the front end with a message like "No Data."

In the future, extensions can be implemented to cover statistics across
more platforms by having fallback routines, or contributing back to
`psutil`.

### Using [Open Hardware Monitor](https://openhardwaremonitor.org/)

Using the [`pythonnet`](https://pythonnet.github.io/) module and the
API provided by Open Hardware Monitor statistics such as temperatures
and fan speeds can be retreived.  It supports Windows 7/8/10 and all
x86 Linux installations.  Support for these statistics represents
additional development effort and user setup time due to external
dependencies.
