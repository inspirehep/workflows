### Inspire Workflows POC

This repository contains the POC for the new inspire ingestion pipeline. The pipelines ('workflows') are designed in airflow.  

#### Setup
The setup is done with docker-compose. In order to run use
```{shell}
docker-compose up -d
```

Also, for the dags there's a need to define an airflow variable `inspire_token` which is a token to inspirebeta.net.
It can be added via UI (go to Admin -> Variables).  


#### UI
To access a powerful airflow UI use the user & passwor airflow.

#### DAGs
Currently, there are 2 dags implemented:
- happy_flow_dag, that is using sensor to wait for the specific input in the db. The input for the test data can be added by executing
```{sql}
insert into workflow_approval values ('2307.13748', 'approved');
```
in the inspire-db container (the db user is `inspire`).
- process_until_breakpoint dag that is implementing another concept - if it's run with parameter `approved=True` it will go through all the steps, however if `approved=True` it skips all the tasks and starts after approval task.

