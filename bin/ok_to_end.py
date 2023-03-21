from kubernetes import client, config

# We want to check that all pods other than the sidecar have terminated, because of completion.
def container_state(container_status):
    if container_status.state.terminated is None:
        return 'running'
    else:
        return 'terminated'


if __name__ == "__main__":
    config.load_incluster_config()
    v1 = client.CoreV1Api()

    # Get the pod name
    # cat /etc/hostname
    with open('/etc/hostname', 'r') as file:
        podname = file.read().replace('\n', '')

    # Get the namespace
    # cat /var/run/secrets/kubernetes.io/serviceaccount/namespace

    with open('/var/run/secrets/kubernetes.io/serviceaccount/namespace', 'r') as file:
        namespace = file.read().replace('\n', '')

    statuses = v1.read_namespaced_pod(podname, namespace).status.container_statuses

    running_state = [container_state(container_status) for container_status in statuses if container_status.name != 'gateway-sidecar']

    # This will return true, if no containers are running.
    # all([]) returns True
    all_ended = all([state == 'terminated' for state in running_state])

    print(all_ended)
