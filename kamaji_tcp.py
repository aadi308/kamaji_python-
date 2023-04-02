import subprocess
import yaml


# cert = "kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.11.0/cert-manager.yaml"
# subprocess.run(cert, shell=True, check=True)
# # Add Clastix Helm repository
# add_repo_command = ['helm', 'repo', 'add', 'clastix', 'https://clastix.github.io/charts']
# subprocess.run(add_repo_command, check=True)

# # Update Helm repositories
# update_repo_command = ['helm', 'repo', 'update']
# subprocess.run(update_repo_command, check=True)

# # Install Kamaji via Helm
# install_command = ['helm', 'install', 'kamaji', 'clastix/kamaji', '-n', 'kamaji-system', '--create-namespace']
# subprocess.run(install_command, check=True)
cluster_name = "tenant1"
secret_name = f"{cluster_name}-admin-kubeconfig"
config = f"/tmp/kubeconfig3"
tenant = {
    'apiVersion': 'kamaji.clastix.io/v1alpha1',
    'kind': 'TenantControlPlane',
    'metadata': {
        'name': cluster_name
    },
    'spec': {
        'controlPlane': {
            'deployment': {
                'replicas': 2,
                'additionalMetadata': {
                    'annotations': {
                        'environment.clastix.io': 'tenant1',
                        'tier.clastix.io': '0'
                    },
                    'labels': {
                        'tenant.clastix.io': 'tenant1',
                        'kind.clastix.io': 'deployment'
                    }
                }
            },
            'service': {
                'additionalMetadata': {
                    'annotations': {
                        'environment.clastix.io': 'tenant1',
                        'tier.clastix.io': '0'
                    },
                    'labels': {
                        'tenant.clastix.io': 'tenant1',
                        'kind.clastix.io': 'service'
                    }
                },
                'serviceType': 'NodePort'
            }
        },
        'kubernetes': {
            'version': 'v1.23.4',
            'kubelet': {
                'cgroupfs': 'cgroupfs'
            },
            'admissionControllers': [
                'LimitRanger',
                'ResourceQuota'
            ]
        },
        'networkProfile': {
            'address': '172.19.0.2',
            'port': 31443,
            'certSANs': [
                'test.clastixlabs.io'
            ],
            'serviceCidr': '10.96.0.0/16',
            'podCidr': '10.244.0.0/16',
            'dnsServiceIPs': [
                '10.96.0.10'
            ]
        },
        'addons': {
            'coreDNS': {},
            'kubeProxy': {}
        }
    }
}
tenant_yaml = yaml.dump(tenant)

# Use kubectl to create the CRD

subprocess.run(["kubectl", "apply", "-f", "-"], input=tenant_yaml.encode())
command = f'kubectl get secrets {secret_name} -o json | jq -r \'.data["admin.conf"]\' | base64 -d > {config}'
subprocess.run(command, shell=True, check=True)

config_cmd = f'kubectl --kubeconfig={config} config view'
subprocess.run(config_cmd, shell=True, check=True)
# subprocess.run(["kubectl", "--kubeconfig={config}", "config", "view"])