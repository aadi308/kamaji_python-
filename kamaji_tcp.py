import subprocess
import yaml
import time
import os

def create_cluster(cluster_name, yaml_file_path):
    secret_name = f"{cluster_name}-admin-kubeconfig"
    config = f"/tmp/kubeconfig"
    yaml_file_path= "kamaji-tenant.yaml"

    with open(yaml_file_path) as f:
        tenant_yaml = f.read().replace('<cluster_name>', cluster_name)


    # Use kubectl to create the CRD
    subprocess.run(["kubectl", "apply", "-f", "-"], input=tenant_yaml.encode())

    time.sleep(40)
    # retrieve kubeconfig and store in /tmp/kubeconfig
    config_detail = f'kubectl get secrets {secret_name} -o json | jq -r \'.data["admin.conf"]\' | base64 -d'
    subprocess.run(config_detail, shell=True, check=True)
  
    
    command = f'kubectl get secrets {secret_name} -o json | jq -r \'.data["admin.conf"]\' | base64 -d > {config}'
    subprocess.run(command, shell=True, check=True)

    print(f"Cluster '{cluster_name}' created successfully.")

#list resources created
    list_resources = f'kubectl get tcp,deploy,pods,svc'
    subprocess.run(list_resources, shell=True, check=True)
    
    # return config

#created cluster-info
    created_cluster_info = f'kubectl --kubeconfig={config} cluster-info'
    subprocess.run(created_cluster_info, shell=True, check=True)

    created_cluster_svc = f'kubectl --kubeconfig={config} get svc'
    subprocess.run(created_cluster_svc, shell=True, check=True)



def delete_cluster(cluster_name):
    delete_command = f"kubectl delete tenantcontrolplane {cluster_name}"
    subprocess.run(delete_command, shell=True, check=True)

    print(f"Cluster '{cluster_name}' deleted successfully.")

def create_node():

    os.environ['KUBECONFIG'] = '/tmp/kubeconfig'
 
    subprocess.run("./join-node.bash", shell=True)
    subprocess.run(["kubectl", "get", "nodes"])

if __name__ == "__main__":
    operation = input("Enter operation (create, addnode, delete): ")
    cluster_name = input("Enter cluster name: ")
    



    if operation == "create":
        create_cluster(cluster_name, yaml_file_path= "kamaji-tenant.yaml")
        # list_cluster()
        # cluster_name = input("Enter cluster name: ")
    elif operation == "addnode":
        create_node()
    # elif operation == "update":
    #     update_cluster(cluster_name)
    elif operation == "delete":
        delete_cluster(cluster_name)
    else:
        print("Invalid operation.")

