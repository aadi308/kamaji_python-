from kubernetes import client, config

# Load Kubernetes configuration from default location
config.load_kube_config()

# Define API group, version, and kind for the TenantControlPlane CRD
api_group = "kamaji.io"
api_version = "v1"
resource_plural = "tenantcontrolplanes"
kind = "TenantControlPlane"

# Create a Kubernetes API client
crd_client = client.CustomObjectsApi()

def create_cluster():
    # Get user input for cluster name, namespace, and number of replicas
    cluster_name = input("Enter a name for the new cluster: ")
    namespace = input("Enter a namespace for the new cluster: ")
    replicas = int(input("Enter the number of replicas for the new cluster: "))

    # Define the TenantControlPlane CRD schema
    schema = {
        "apiVersion": f"{api_group}/{api_version}",
        "kind": kind,
        "metadata": {
            "name": cluster_name,
            "namespace": namespace,
            "labels": {
                "app": "kamaji"
            }
        },
        "spec": {
            "replicas": replicas
        }
    }

    # Create the TenantControlPlane CRD
    crd_client.create_namespaced_custom_object(api_group, api_version, namespace, resource_plural, schema)
    
    print(f"Cluster {cluster_name} created in namespace {namespace} with {replicas} replicas.")

def list_clusters():
    # Get user input for namespace to list clusters from
    namespace = input("Enter a namespace to list clusters from (leave blank for all namespaces): ")

    # Retrieve the list of TenantControlPlane CRDs
    if namespace:
        crd_list = crd_client.list_namespaced_custom_object(api_group, api_version, namespace, resource_plural)
    else:
        crd_list = crd_client.list_cluster_custom_object(api_group, api_version, resource_plural)

    # Print out the details for each cluster
    for crd in crd_list['items']:
        cluster_name = crd['metadata']['name']
        namespace = crd['metadata']['namespace']
        replicas = crd['spec']['replicas']
        print(f"Cluster {cluster_name} in namespace {namespace} has {replicas} replicas.")

def update_cluster():
    # Get user input for cluster name and namespace
    cluster_name = input("Enter the name of the cluster to update: ")
    namespace = input("Enter the namespace of the cluster to update: ")

    # Retrieve the current state of the TenantControlPlane CRD
    crd = crd_client.get_namespaced_custom_object(api_group, api_version, namespace, resource_plural, cluster_name)

    # Get user input for number of replicas to update to
    new_replicas = int(input("Enter the new number of replicas for the cluster: "))

    # Update the number of replicas in the CRD schema
    crd['spec']['replicas'] = new_replicas

    # Update the TenantControlPlane CRD
    crd_client.replace_namespaced_custom_object(api_group, api_version, namespace, resource_plural, cluster_name, crd)

    print(f"Cluster {cluster_name} in namespace {namespace} updated with {new_replicas} replicas.")

def delete_cluster():
    # Get user input for cluster name and namespace
    cluster_name = input("Enter the name of the cluster to delete: ")
    namespace = input("Enter the namespace of the cluster to delete: ")

    # Delete the Tenant
