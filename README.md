# OSKAR reference simulations

### 1. Dependencies
- OSKAR: [(http://oerc.ox.ac.uk/~ska/oskar2/)](http://oerc.ox.ac.uk/~ska/oskar2/)
    - tested with version 2.6.1 
- CASA [(http://casa.nrao.edu/)](http://casa.nrao.edu/)
    - tested with versions: 4.4.0-REL (r33623) 
- Install python dependencies with:
    ```pip install -r requirements.txt```

### 2. Reference simulations

#### 2.1 Time smearing tests
Test looking at analytical time smearing v.s. sum of snapshots.
###### Run with:
```bash
./run <json config file>
```
e.g.
```bash
./run sim01.json
```
