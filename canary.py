import requests
from requests.structures import CaseInsensitiveDict
import json
from collections import defaultdict

def create_deployment_canary():
    cluster_url = "https://192.168.50.21:6443/apis/apps/v1/namespaces/test1234/deployments"
    cluster_token ="eyJhbGciOiJSUzI1NiIsImtpZCI6InJ4Q05BRlZvbzJpeTlVSDFpaTVZdjN1UnRvc2xTZmliSlN4Vmp6cWhtYk0ifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJkZWZhdWx0Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZWNyZXQubmFtZSI6ImRlZmF1bHQtdG9rZW4tdjd6OHciLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoiZGVmYXVsdCIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6IjljZjU3NmZhLTYxZTgtNDlhMi05MDkzLTRiZjU1NmQ3MjI2NyIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDpkZWZhdWx0OmRlZmF1bHQifQ.aD7E_V3SBfiyKo8TbrCg8y8y4qfjxvk7eYF11ybApjuQMJBtrGNmPpz8R3rSC2ION5rKYQQLO7cmSlfUOrplBFFYfFWGTgdkeC3IKhpuTcI-YpCpQYz-ktafrbBLvZQkbkJ7_IBJ3bZHegehBHXrl2F2pgmu6ft1tjszFMctbFxgDlk4VrdG7BXHIPuWPY0ZXDfe0V5AuYq4D5WvNCjLZlPYDTifjM3bll5Tq79M6frti57My59dXfbQ-VUfgRHcJAA37ZLY3IDIpfRc5O2IjZg4XznceKPw0v2tEWVD1yez-lgMhqwxE-fIttLKsFZvO3RKfcN0R-JKctU3nJFVLQ"
    deploy_name = "test-canary"
    namespace = "test1234"
    image = "nginx:1.15"
    color = "green"
    replicas = 1
 

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
            "color": color,
            "canary": "canary"
        }
        },
        "spec": {
            "replicas": replicas,
            "selector": {
                "matchLabels": {
                    "app": deploy_name,
                    "color": color,
                    "canary": "canary"
                }
           },
            "template": {
            "metadata": {
                "labels": {
                    "app": deploy_name,
                    "color": color,
                    "canary": "canary"
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

if __name__ == '__main__':
    cluster_url = "https://192.168.50.21:6443"
    cluster_token ="eyJhbGciOiJSUzI1NiIsImtpZCI6InJ4Q05BRlZvbzJpeTlVSDFpaTVZdjN1UnRvc2xTZmliSlN4Vmp6cWhtYk0ifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJkZWZhdWx0Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZWNyZXQubmFtZSI6ImRlZmF1bHQtdG9rZW4tdjd6OHciLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoiZGVmYXVsdCIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6IjljZjU3NmZhLTYxZTgtNDlhMi05MDkzLTRiZjU1NmQ3MjI2NyIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDpkZWZhdWx0OmRlZmF1bHQifQ.aD7E_V3SBfiyKo8TbrCg8y8y4qfjxvk7eYF11ybApjuQMJBtrGNmPpz8R3rSC2ION5rKYQQLO7cmSlfUOrplBFFYfFWGTgdkeC3IKhpuTcI-YpCpQYz-ktafrbBLvZQkbkJ7_IBJ3bZHegehBHXrl2F2pgmu6ft1tjszFMctbFxgDlk4VrdG7BXHIPuWPY0ZXDfe0V5AuYq4D5WvNCjLZlPYDTifjM3bll5Tq79M6frti57My59dXfbQ-VUfgRHcJAA37ZLY3IDIpfRc5O2IjZg4XznceKPw0v2tEWVD1yez-lgMhqwxE-fIttLKsFZvO3RKfcN0R-JKctU3nJFVLQ"
    create_deployment_canary()