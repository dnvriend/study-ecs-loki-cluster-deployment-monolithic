# study-ecs-loki-cluster-deployment-monolithic 
A small study project on how to deploy loki in a cluster setup with Loki and Grafana in monolithic mode, but with multiple loki instances.
This deployment mode will cluster the read path, but not the write paths. 

## Example queries

```json
# find the loki cluster instances joining the cluster
{container_name="loki", ecs_cluster="dnvriend-loki-all-cluster"} |~ "caller=(ringmanager.go|basic_lifecycler.go)" |= "instance"

# find the loki cluster instances joining the cluster
{container_name="loki"} |~ "module_service|lifecycler|recalculate|engine|roundtrip|trip|compactor"
```
