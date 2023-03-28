# (danielpayten) pod-gateway: Automatic Completion Fork 

This project is a fork of k8s-at-home pod gateway here: https://github.com/k8s-at-home/pod-gateway/

This project can be deployed on kubernetes, allowing all container in a designated namespace to route their traffic via a VPN.
This is acheived through running a sidecar container alongside the workload(s).
While the initial project did work, it was unsuitable for my needs as jobs would never be marked as complete as the sidecar container remained running despite the workload container completing.

This for adds a 'heartbeat' type check, which terminates the sidecar container if it is the last remaining container running in the pod.

This is acheived through a small piece of python code [ok_to_end.py](https://github.com/danielpayten/pod-gateway/blob/main/bin/ok_to_end.py) which uses the kubernetes API to check the state of all other remaining containers in the pod.

The heartbeat [client_sidecar.sh](https://github.com/danielpayten/pod-gateway/blob/main/bin/client_sidecar.sh) shell script was modified to complete these checks.

Additionally, because we're using the Kubernetes API to check the state of other containers in the pod, we need to apply appropriate RBAC.
An example of this is contained in https://github.com/danielpayten/pod-gateway/blob/main/SetupEnv.yaml

## Usage

In order to deploy this pod gateway, follow the instructions here: https://docs.k8s-at-home.com/guides/pod-gateway/

However, when deploying the helm chart, we need to change the image using the following:
```
repository: docker.io/danielpayten/vpn-gateway
```


