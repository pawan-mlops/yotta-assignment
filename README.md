
1. Architecture Overview
Multi-tenancy: Each website is deployed in its own Kubernetes namespace (user1, user2, user3)
Dynamic Domains: Host-based routing using Ingress (userX.yotta.local)
Workload Isolation:
ResourceQuota per namespace
NetworkPolicies for ingress/egress control
Autoscaling: Horizontal Pod Autoscaler (HPA) based on CPU utilization
Observability: Prometheus + Grafana
CI/CD: GitHub Actions with Helm-based deployment and rollback
Event-driven: Kafka publishes deployment events

2. Repository Structure
   .
├── Chart.yaml
├── Dockerfile
├── app.py
├── docker-compose.yaml
├── load-test.yaml
├── templates
│   ├── _helpers.tpl
│   ├── deployment.yaml
│   ├── hpa.yaml
│   ├── ingress.yaml
│   ├── networkpolicy.yaml
│   ├── pdb.yaml
│   ├── resourcequota.yaml
│   └── service.yaml
├── user1.yotta.local+2-key.pem
├── user1.yotta.local+2.pem
├── values.yaml
└── yotta-kind-cluster.yaml

3. Multi-Tenant Deployment & Dynamic Domain Mapping
A single Helm chart is reused for all tenants.
Each tenant is deployed into its own namespace.
Ingress uses host-based routing to map domains dynamically.
Example Mapping
user1.yotta.local → user1 namespace
user2.yotta.local → user2 namespace
user3.yotta.local → user3 namespace
Ingress-nginx routes traffic based on the HTTP Host header.

4. Scaling & Resource Optimization
Horizontal Pod Autoscaler (HPA)
Configured per tenant
Scales pods from 1 → 5 replicas
Triggered when CPU utilization exceeds 50%
Resource Quotas
Enforced per namespace
Prevents noisy-neighbor issues
Load-test pods must explicitly define CPU and memory requests/limits
Pod Disruption Budget (PDB)
Ensures at least one pod is always available during:
Rolling updates
Node disruptions
Load Simulation
Load is generated using a dedicated load-test pod
HPA scaling is verified using:
kubectl get hpa -n user1kubectl get pods -n user1

5. Observability (Prometheus & Grafana)
Installed using kube-prometheus-stack
Runs on the system node group
Metrics collected:
Pod CPU and memory usage
Node resource utilization
HPA replica count
Grafana dashboards used:
Kubernetes / Compute Resources / Pod
Kubernetes / Compute Resources / Node

6. CI/CD Pipeline with Rollback
Pipeline Trigger
Runs on every push to the main branch
Also supports manual trigger (workflow_dispatch)
Pipeline Steps
Build Docker image
Deploy application using Helm
Verify rollout
Automatically rollback on failure
Rollback is handled via:
helm rollback <release-name>

# Local Environment Limitation

The CI/CD pipeline is defined using GitHub Actions, but the Kubernetes cluster is running locally using kind.
Since GitHub Actions runners cannot directly access a locally running kind cluster, the deployment, rollback, and Kafka event-trigger steps cannot be fully executed from GitHub Actions in this setup its failed when pushed the commit and it executed.
The pipeline YAML reflects a production-ready workflow, and the same pipeline would work successfully when:
The cluster is running in a cloud environment (e.g., AWS EKS) via pushing it to cloud registery and deploy to cloud managed k8s clusters 
Or when a self-hosted GitHub Actions runner is configured with access to the cluster


7. Event-Driven Pipeline (Kafka)
Kafka and Zookeeper run via Docker Compose
Application publishes WebsiteCreated events on deployment
Events are consumed to verify successful publishing

