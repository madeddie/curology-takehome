# Curology take-home

## Infrastructure

To deploy the take-home web service I would deploy in AWS since I’m most well-versed in using it.

Assuming we’ll be hosting more applications and we’re really starting from scratch I’d use Terraform to create a VPC with internal and external IP subnet and NAT gateways in at least 3 AZs.

In this VPC we’ll also use Terraform to create an EKS cluster, container registry and an autoscaler  (Karpnenter) to manage deployment of worker nodes. Worker nodes will be spun up in all 3 AZs within the internal IP subnets.
Access to the services is managed by the AWS Load Balancer Controller with ALBs running in the external IP subnets.

Terraform source is kept in git and deployed using Terraform Cloud.

(In case this is the only application or we’re only planning on installing a minimal amount of services, I’d be using eksctl to create most of the infrastructure instead of Terraform.)

Developers get a large set of RBAC permissions to execute get/describe/logs on the cluster, but only the automated deployment system and a small subset of SREs will get full permissions on the cluster to deploy and fix issues.

Metric collection will happen using a standard Prometheus stack and log collection will use Grafana Loki.

For a smaller setup I’d like to host dev, staging and prod on the same cluster in their own specific namespaces, if the amount of hosted applications (and probably teams working on them) grows, a separate cluster per environment could be considered. 

## Continuous delivery

The size of our application stack defines if we’ll have a true staging environment or just feature branch envs and production. A larger stack usually needs more continuous integration testing and possibly also some manual QA work, which means a longer-lived staging env is useful. Smaller setups can benefit from merging and deploying directly to a production env using a combination of canary and blue/green deployment strategies.

ArgoCD monitors the docker registry and git repo for changes and deploys new versions of the application containers, Kubernetes manifests or Helm charts. While I don’t think Helm is necessary for deploying applications that will only be used internally, I also don’t think it’s a hindrance, especially if we want to use a uniform pattern of application deployment. I’m also a fan of Kustomize, especially if there’s no real attachment to Helm yet.

Developers commit changes to a feature branch which gets built and tested using Github Actions. If the size of the test suite is on the big side only unit tests are automatically run at this stage, otherwise integration tests are also run. If possible I’d like to deploy the application to a user and branch-specific namespace within the cluster so the developer can manually test things on a running environment while developing.

Once a PR has been created to merge the feature branch to the staging branch a new namespace is created and the code deployed for a full suite of integration tests, which after running update the PR of their results. After the tests successfully finish a merge is allowed. A merge causes the tested container to be tagged with a staging version tag which is monitored by ArgoCD and deployed to our staging env.

After optional more testing, soaking and manual QA steps on staging a PR will be created to merge the latest state of staging into production, preferably with a short period of freezing of the staging branch.
A merge to production will cause retagging of the current staging containers with a production version tag and deployed to the production environment.
