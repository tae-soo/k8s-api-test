import requests
from requests.structures import CaseInsensitiveDict
import json
from collections import defaultdict

def create_deployment_bluegreen():
    cluster_url = "https://192.168.50.21:6443/apis/apps/v1/namespaces/test1234/deployments"
    cluster_token ="eyJhbGciOiJSUzI1NiIsImtpZCI6InJ4Q05BRlZvbzJpeTlVSDFpaTVZdjN1UnRvc2xTZmliSlN4Vmp6cWhtYk0ifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJkZWZhdWx0Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZWNyZXQubmFtZSI6ImRlZmF1bHQtdG9rZW4tdjd6OHciLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoiZGVmYXVsdCIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6IjljZjU3NmZhLTYxZTgtNDlhMi05MDkzLTRiZjU1NmQ3MjI2NyIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDpkZWZhdWx0OmRlZmF1bHQifQ.aD7E_V3SBfiyKo8TbrCg8y8y4qfjxvk7eYF11ybApjuQMJBtrGNmPpz8R3rSC2ION5rKYQQLO7cmSlfUOrplBFFYfFWGTgdkeC3IKhpuTcI-YpCpQYz-ktafrbBLvZQkbkJ7_IBJ3bZHegehBHXrl2F2pgmu6ft1tjszFMctbFxgDlk4VrdG7BXHIPuWPY0ZXDfe0V5AuYq4D5WvNCjLZlPYDTifjM3bll5Tq79M6frti57My59dXfbQ-VUfgRHcJAA37ZLY3IDIpfRc5O2IjZg4XznceKPw0v2tEWVD1yez-lgMhqwxE-fIttLKsFZvO3RKfcN0R-JKctU3nJFVLQ"
    deploy_name = "test-green"
    namespace = "test1234"
    image = "nginx:1.13"
    replicas = 5
 

    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Authorization"] = f"Bearer {cluster_token}"    
    data = {
        "kind": "Deployment",
        "apiVersion": "apps/v1",
        "metadata": {
            "name": deploy_name,
            "namespace": namespace,
            "labels": {
            "app": deploy_name,
            "color": "green",
            "canary": "stable"
        }
        },
        "spec": {
            "replicas": replicas,
            "selector": {
                "matchLabels": {
                    "app": deploy_name,
                    "color": "green",
                    "canary": "stable"
                }
           },
            "template": {
            "metadata": {
                "labels": {
                    "app": deploy_name,
                    "color": "green",
                    "canary": "stable"
                }
            },
            "spec": {
                "containers": [
                    {
                        "name": deploy_name,
                        "image": image,
                        "imagePullPolicy": "IfNotPresent"
                    }
                ]
            }
        },
        "revisionHistoryLimit": 10
        }
    }
    resp = requests.post(cluster_url, headers=headers, data=json.dumps(data), verify=False)
    print(resp.text)
    print(resp.status_code)






def getInfo_deployment_bluegreen():
    cluster_url = "https://192.168.50.21:6443/apis/apps/v1/namespaces/test1234/deployments/test-green"
    cluster_token ="eyJhbGciOiJSUzI1NiIsImtpZCI6InJ4Q05BRlZvbzJpeTlVSDFpaTVZdjN1UnRvc2xTZmliSlN4Vmp6cWhtYk0ifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJkZWZhdWx0Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZWNyZXQubmFtZSI6ImRlZmF1bHQtdG9rZW4tdjd6OHciLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoiZGVmYXVsdCIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6IjljZjU3NmZhLTYxZTgtNDlhMi05MDkzLTRiZjU1NmQ3MjI2NyIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDpkZWZhdWx0OmRlZmF1bHQifQ.aD7E_V3SBfiyKo8TbrCg8y8y4qfjxvk7eYF11ybApjuQMJBtrGNmPpz8R3rSC2ION5rKYQQLO7cmSlfUOrplBFFYfFWGTgdkeC3IKhpuTcI-YpCpQYz-ktafrbBLvZQkbkJ7_IBJ3bZHegehBHXrl2F2pgmu6ft1tjszFMctbFxgDlk4VrdG7BXHIPuWPY0ZXDfe0V5AuYq4D5WvNCjLZlPYDTifjM3bll5Tq79M6frti57My59dXfbQ-VUfgRHcJAA37ZLY3IDIpfRc5O2IjZg4XznceKPw0v2tEWVD1yez-lgMhqwxE-fIttLKsFZvO3RKfcN0R-JKctU3nJFVLQ"


    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Authorization"] = f"Bearer {cluster_token}"    
 
    resp = requests.get(cluster_url, headers=headers,verify=False)
    print(resp.text)
    print(resp.status_code)


def update_deployment_bluegreen():
    cluster_url = "https://192.168.50.21:6443/apis/apps/v1/namespaces/test1234/deployments/test-green"
    cluster_token ="eyJhbGciOiJSUzI1NiIsImtpZCI6InJ4Q05BRlZvbzJpeTlVSDFpaTVZdjN1UnRvc2xTZmliSlN4Vmp6cWhtYk0ifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJkZWZhdWx0Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZWNyZXQubmFtZSI6ImRlZmF1bHQtdG9rZW4tdjd6OHciLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoiZGVmYXVsdCIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6IjljZjU3NmZhLTYxZTgtNDlhMi05MDkzLTRiZjU1NmQ3MjI2NyIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDpkZWZhdWx0OmRlZmF1bHQifQ.aD7E_V3SBfiyKo8TbrCg8y8y4qfjxvk7eYF11ybApjuQMJBtrGNmPpz8R3rSC2ION5rKYQQLO7cmSlfUOrplBFFYfFWGTgdkeC3IKhpuTcI-YpCpQYz-ktafrbBLvZQkbkJ7_IBJ3bZHegehBHXrl2F2pgmu6ft1tjszFMctbFxgDlk4VrdG7BXHIPuWPY0ZXDfe0V5AuYq4D5WvNCjLZlPYDTifjM3bll5Tq79M6frti57My59dXfbQ-VUfgRHcJAA37ZLY3IDIpfRc5O2IjZg4XznceKPw0v2tEWVD1yez-lgMhqwxE-fIttLKsFZvO3RKfcN0R-JKctU3nJFVLQ"
    deploy_name = "test-green"
    namespace = "test1234"
    image = "nginx:1.16"
    replicas = 2
 

    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Authorization"] = f"Bearer {cluster_token}"    
    data = {
        "kind": "Deployment",
        "apiVersion": "apps/v1",
        "metadata": {
            "name": deploy_name,
            "namespace": namespace,
            "labels": {
            "app": deploy_name,
            "color": "green",
            "canary": "stable"
        }
        },
        "spec": {
            "replicas": replicas,
            "selector": {
                "matchLabels": {
                    "app": deploy_name,
                    "color": "green",
                    "canary": "stable"
                }
           },
            "template": {
            "metadata": {
                "labels": {
                    "app": deploy_name,
                    "color": "green",
                    "canary": "stable"
                }
            },
            "spec": {
                "containers": [
                    {
                        "name": deploy_name,
                        "image": image,
                        "imagePullPolicy": "IfNotPresent"
                    }
                ]
            }
        },
        "revisionHistoryLimit": 10
        }
    }
    resp = requests.put(cluster_url, headers=headers, data=json.dumps(data), verify=False)
    print(resp.text)
    print(resp.status_code)

def update_service_bluegreen():
    cluster_url = "https://192.168.50.21:6443/apis/apps/v1/namespaces/test1234/services/svc-nginx"
    cluster_token ="eyJhbGciOiJSUzI1NiIsImtpZCI6InJ4Q05BRlZvbzJpeTlVSDFpaTVZdjN1UnRvc2xTZmliSlN4Vmp6cWhtYk0ifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJkZWZhdWx0Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZWNyZXQubmFtZSI6ImRlZmF1bHQtdG9rZW4tdjd6OHciLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoiZGVmYXVsdCIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6IjljZjU3NmZhLTYxZTgtNDlhMi05MDkzLTRiZjU1NmQ3MjI2NyIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDpkZWZhdWx0OmRlZmF1bHQifQ.aD7E_V3SBfiyKo8TbrCg8y8y4qfjxvk7eYF11ybApjuQMJBtrGNmPpz8R3rSC2ION5rKYQQLO7cmSlfUOrplBFFYfFWGTgdkeC3IKhpuTcI-YpCpQYz-ktafrbBLvZQkbkJ7_IBJ3bZHegehBHXrl2F2pgmu6ft1tjszFMctbFxgDlk4VrdG7BXHIPuWPY0ZXDfe0V5AuYq4D5WvNCjLZlPYDTifjM3bll5Tq79M6frti57My59dXfbQ-VUfgRHcJAA37ZLY3IDIpfRc5O2IjZg4XznceKPw0v2tEWVD1yez-lgMhqwxE-fIttLKsFZvO3RKfcN0R-JKctU3nJFVLQ"
    svc_name = "svc-nginx"
    namespace = "test1234"
 

    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Authorization"] = f"Bearer {cluster_token}"    
    data = {
        "kind": "Service",
        "apiVersion": "v1",
        "metadata": {
            "name": svc_name,
            "namespace": namespace,
            "resourceVersion": "2068892",
            "labels": {
                "app": svc_name,
                "app.kubernetes.io/instance": "testapp",
                "bluegreen": "blue"
            }
        },
        "spec": {
            "ports": [
                {
                    "name": svc_name,
                    "protocol": "TCP",
                    "port": 80,
                    "targetPort": 80,
                    "nodePort": 30270
                }
            ],
            "selector": {
                "app": svc_name,
                "bluegreen": "blue"
            },
            "clusterIP": "10.233.37.110",
            "clusterIPs": [
                "10.233.37.110"
            ],
            "type": "LoadBalancer",
            "sessionAffinity": "None",
            "externalTrafficPolicy": "Cluster",
            "ipFamilies": [
                "IPv4"
            ],
            "ipFamilyPolicy": "SingleStack",
            "allocateLoadBalancerNodePorts": true,
            "internalTrafficPolicy": "Cluster"
        },
        "status": {
            "loadBalancer": {
                "ingress": [
                    {
                        "ip": "192.168.50.107"
                    }
                ]
            }
        }
    }
    resp = requests.put(cluster_url, headers=headers, data=json.dumps(data), verify=False)
    print(resp.text)
    print(resp.status_code)

def delete_deployment_bluegreen():
    cluster_url = "https://192.168.50.21:6443/apis/apps/v1/namespaces/test1234/deployments/rollout-nginx"
    cluster_token ="eyJhbGciOiJSUzI1NiIsImtpZCI6InJ4Q05BRlZvbzJpeTlVSDFpaTVZdjN1UnRvc2xTZmliSlN4Vmp6cWhtYk0ifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJkZWZhdWx0Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZWNyZXQubmFtZSI6ImRlZmF1bHQtdG9rZW4tdjd6OHciLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoiZGVmYXVsdCIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6IjljZjU3NmZhLTYxZTgtNDlhMi05MDkzLTRiZjU1NmQ3MjI2NyIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDpkZWZhdWx0OmRlZmF1bHQifQ.aD7E_V3SBfiyKo8TbrCg8y8y4qfjxvk7eYF11ybApjuQMJBtrGNmPpz8R3rSC2ION5rKYQQLO7cmSlfUOrplBFFYfFWGTgdkeC3IKhpuTcI-YpCpQYz-ktafrbBLvZQkbkJ7_IBJ3bZHegehBHXrl2F2pgmu6ft1tjszFMctbFxgDlk4VrdG7BXHIPuWPY0ZXDfe0V5AuYq4D5WvNCjLZlPYDTifjM3bll5Tq79M6frti57My59dXfbQ-VUfgRHcJAA37ZLY3IDIpfRc5O2IjZg4XznceKPw0v2tEWVD1yez-lgMhqwxE-fIttLKsFZvO3RKfcN0R-JKctU3nJFVLQ"
 

    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Authorization"] = f"Bearer {cluster_token}"    
    resp = requests.delete(cluster_url, headers=headers, verify=False)
    print(resp.text)
    print(resp.status_code)














if __name__ == '__main__':
    cluster_url = "https://192.168.50.21:6443"
    cluster_token ="eyJhbGciOiJSUzI1NiIsImtpZCI6InJ4Q05BRlZvbzJpeTlVSDFpaTVZdjN1UnRvc2xTZmliSlN4Vmp6cWhtYk0ifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJkZWZhdWx0Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZWNyZXQubmFtZSI6ImRlZmF1bHQtdG9rZW4tdjd6OHciLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoiZGVmYXVsdCIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6IjljZjU3NmZhLTYxZTgtNDlhMi05MDkzLTRiZjU1NmQ3MjI2NyIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDpkZWZhdWx0OmRlZmF1bHQifQ.aD7E_V3SBfiyKo8TbrCg8y8y4qfjxvk7eYF11ybApjuQMJBtrGNmPpz8R3rSC2ION5rKYQQLO7cmSlfUOrplBFFYfFWGTgdkeC3IKhpuTcI-YpCpQYz-ktafrbBLvZQkbkJ7_IBJ3bZHegehBHXrl2F2pgmu6ft1tjszFMctbFxgDlk4VrdG7BXHIPuWPY0ZXDfe0V5AuYq4D5WvNCjLZlPYDTifjM3bll5Tq79M6frti57My59dXfbQ-VUfgRHcJAA37ZLY3IDIpfRc5O2IjZg4XznceKPw0v2tEWVD1yez-lgMhqwxE-fIttLKsFZvO3RKfcN0R-JKctU3nJFVLQ"
    delete_deployment_bluegreen()