import subprocess
import yaml

# Define the CRD group, version, and plural name
group = "kamaji.io"
version = "v1alpha1"
plural = "tenantcontrolplanes"

# Define the CRD definition
crd_definition = {
    "apiVersion": "apiextensions.k8s.io/v1apha1",
    "kind": "CustomResourceDefinition",
    "metadata": {
        "name": f"{plural}.{group}"
    },
    "spec": {
        "group": group,
        "version": version,
        "names": {
            "plural": plural,
            "singular": "tenantcontrolplane",
            "kind": "TenantControlPlane",
            "shortNames": ["tcp"]
        },
        "scope": "Namespaced",
        "versions": [{
            "name": version,
            "served": True,
            "storage": True,
            "schema": {
                "openAPIV3Schema": {
                    "type": "object",
                    "properties": {
                        "spec": {
                            "type": "object",
                            "properties": {
                                "size": {
                                    "type": "integer",
                                    "minimum": 1,
                                    "maximum": 10
                                },
                                "region": {
                                    "type": "string",
                                    "enum": ["us-west", "us-east", "eu-west"]
                                },
                                "nodeType": {
                                    "type": "string",
                                    "enum": ["t2.micro", "m5.large", "c5.xlarge"]
                                }
                            },
                            "required": ["size", "region", "nodeType"]
                        }
                    },
                    "required": ["spec"]
                }
            }
        }]
    }
}

# Convert the CRD definition to YAML format
crd_yaml = yaml.dump(crd_definition)

# Use kubectl to create the CRD
subprocess.run(["kubectl", "apply", "-f", "-"], input=crd_yaml.encode())
