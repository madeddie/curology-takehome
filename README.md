# Curology takehome exercise

This project consists of:

- an exceedingly simple web app written in Python using the Flask framework and the Gunicorn WSGI server
- Dockerfile to build Python container with the web app
- Helm chart with a Deployment, Service and Ingress

## How to deploy

To deploy this service to a local kubernetes cluster (like minikube or the Docker Desktop built-in kubernetes service) follow the following steps.

- build the container
```bash
docker build -t curology-takehome:latest .
```

- deploy Helm chart
```bash
helm upgrade --install --create-namespace --namespace curology-takehome curology-takehome helm-chart
```

The deployment should automagically create the required kubernetes namespace `curology-takehome` (please check this doesn't conflict with existing usage).
It will also use the docker image that was built and stored in the local docker daemon.

If this is to be run on a remote cluster the container should be pushed to a registry that's available to the cluster and the `values.yaml` file updated accordingly.

## Usage of webservice

If the service was deployed on a local cluster the Ingress most likely won't be functional, but the service can be reached by executing:

```bash
kubectl port-forward service/curology-takehome-web 8000:8000 -n curology-takehome
```

this will forward localhost port 8000 to the service port 8000.
Browse to http://localhost:8000/ to see the service

The endpoints are:
- / (root) - return Hello, <perceived remote IP address>!
- /headers -  returns the HTTP headers of the request

Press CTRL-c to stop forwarding the port.

## Clean up

To clean up the resources:

```bash
helm uninstall curology-takehome -n curology-takehome
kubectl delete namespace curology-takehome
docker rmi curology-takehome:latest
```
