import requests
from requests.structures import CaseInsensitiveDict
import json
from collections import defaultdict


def get_argocd_token(url: str, username: str, password: str) -> requests.models.Response:
    url = url + "/api/v1/session"

    data = {
        "username": username,
        "password": password
    }
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    resp = requests.post(url, headers=headers, data=json.dumps(data), verify=False)

    return resp


def is_have_namespace(cluster_url: str, cluster_token: str, namespace: str) -> bool:
    url = cluster_url + "/api/v1/namespaces/" + namespace

    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Authorization"] = f"Bearer {cluster_token}"
    resp = requests.get(url, headers=headers, verify=False)
    print(resp.text)
    if resp.json()['kind'] == "Namespace":
        return True
    elif resp.json()['code'] == 404:
        return False
    else:
        print("error")
        return True

def create_namespace_in_cluster(cluster_url: str, cluster_token: str, namespace: str):
    url = cluster_url + "/api/v1/namespaces/"

    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Authorization"] = f"Bearer {cluster_token}"
    data = {
        "kind": "Namespace",
        "apiVersion": "v1",
        "metadata": {
            "name": namespace
        }
    }
    resp = requests.post(url, headers=headers, data=json.dumps(data), verify=False)
    print(resp.text)


def create_argocd_app_with_auto_create_namespace(argocd_url: str, argo_bearer_token: str, app_name: str, namespace: str,
                      repo_url: str, target_revision: str, target_path: str, cluster_url: str, cluster_token: str):
    if not is_have_namespace(cluster_url, cluster_token, namespace):
        create_namespace_in_cluster(cluster_url, cluster_token, namespace)
    return create_argocd_app(argocd_url=argocd_url, argo_bearer_token=argo_bearer_token, app_name=app_name, namespace=namespace,
                      repo_url=repo_url, target_path=target_path, target_revision=target_revision, cluster_url=cluster_url)


def create_argocd_app(argocd_url: str, argo_bearer_token: str, app_name: str, namespace: str,
                      repo_url: str, target_revision: str, target_path: str, cluster_url: str):

    url = argocd_url + "/api/v1/applications"

    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Authorization"] = f"Bearer {argo_bearer_token}"
    data = {
        "metadata": {
            "name": app_name,
            "namespace": "argocd"
        },
        "spec": {
            "project": "default",
            "source": {
                "repoURL": repo_url,
                "targetRevision": target_revision,
                "path": target_path
            },
            "destination": {
                "server": cluster_url,
                "namespace": namespace
            }
        }
    }
    resp = requests.post(url, headers=headers, data=json.dumps(data), verify=False)
    print(resp.text)

def update_argocd_app(argocd_url: str, argo_bearer_token: str, app_name: str, namespace: str,
                      repo_url: str, target_revision: str, target_path: str, cluster_url: str):

    url = argocd_url + f"/api/v1/applications/{app_name}"

    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Authorization"] = f"Bearer {argo_bearer_token}"
    data = {
        "metadata": {
            "name": app_name,
            "namespace": "argocd"
        },
        "spec": {
            "project": "default",
            "source": {
                "repoURL": repo_url,
                "targetRevision": target_revision,
                "path": target_path
            },
            "destination": {
                "server": cluster_url,
                "namespace": namespace
            }
        }
    }
    resp = requests.put(url, headers=headers, data=json.dumps(data), verify=False)
    print(resp.text)

def update_argocd_app(argocd_url: str, argo_bearer_token: str, app_name: str):
    url = argocd_url + "/api/v1/applications/" + app_name

    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Authorization"] = f"Bearer {argo_bearer_token}"
    resp = requests.delete(url, headers=headers, verify=False)
    return resp

## 신규 생성 01
def get_argo_service_deployment_name(argocd_url: str, argo_bearer_token: str, app_name: str ):
    url = argocd_url + "/api/v1/applications/" + app_name + "/resource-tree"
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Authorization"] = f"Bearer {argo_bearer_token}"
    resp = requests.get(url, headers=headers, verify=False)     
    deployment_dict = defaultdict(list)
    service_dict = defaultdict(list)
    json_resp = resp.json()
    for resource in json_resp["nodes"]:
        if resource['kind'] == 'Deployment': 
            deployment_dict[resource['namespace']].append(resource['name'])
        if resource['kind'] == 'Service': 
            service_dict[resource['namespace']].append(resource['name'])
    return deployment_dict, service_dict

## Todo



if __name__ == '__main__':
    # 환경 변수내 포함할 것
    ARGOCD_URL = "https://192.168.50.104"
    ARGOCD_USERNAME = "admin"
    ARGOCD_PASSWORD = "hHGfeDCRrCJ2pXCP"

    cluster_url = "https://192.168.50.21:6443"
    cluster_token ="eyJhbGciOiJSUzI1NiIsImtpZCI6InJ4Q05BRlZvbzJpeTlVSDFpaTVZdjN1UnRvc2xTZmliSlN4Vmp6cWhtYk0ifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJkZWZhdWx0Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZWNyZXQubmFtZSI6ImRlZmF1bHQtdG9rZW4tdjd6OHciLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoiZGVmYXVsdCIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6IjljZjU3NmZhLTYxZTgtNDlhMi05MDkzLTRiZjU1NmQ3MjI2NyIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDpkZWZhdWx0OmRlZmF1bHQifQ.aD7E_V3SBfiyKo8TbrCg8y8y4qfjxvk7eYF11ybApjuQMJBtrGNmPpz8R3rSC2ION5rKYQQLO7cmSlfUOrplBFFYfFWGTgdkeC3IKhpuTcI-YpCpQYz-ktafrbBLvZQkbkJ7_IBJ3bZHegehBHXrl2F2pgmu6ft1tjszFMctbFxgDlk4VrdG7BXHIPuWPY0ZXDfe0V5AuYq4D5WvNCjLZlPYDTifjM3bll5Tq79M6frti57My59dXfbQ-VUfgRHcJAA37ZLY3IDIpfRc5O2IjZg4XznceKPw0v2tEWVD1yez-lgMhqwxE-fIttLKsFZvO3RKfcN0R-JKctU3nJFVLQ"

    # get argocd_token
    resp = get_argocd_token(ARGOCD_URL, ARGOCD_USERNAME, ARGOCD_PASSWORD)
    argo_bearer_token = ""
    # 토큰 발급 실패면, 에러 팝업
    if resp.status_code == 200:
        print("토큰 발급 성공")
        argo_bearer_token = resp.json()['token']
        print(argo_bearer_token)
    else:
        print("토큰 발급 실패")
    
    app_name = "testapp"
    name_deploy_dict, service_dict = get_argo_service_deployment_name(ARGOCD_URL, argo_bearer_token, app_name)

    for namespace , deployment in name_deploy_dict.items():
        print(namespace , deployment)

    for namespace , service in service_dict.items():
        print(namespace , service)


