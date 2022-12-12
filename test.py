from kubernetes import client, config
from kubernetes.stream import stream
import ssl
from flask import jsonify

ssl._create_default_https_context = ssl._create_unverified_context
config = client.Configuration()

config.api_key['authorization'] = "eyJhbGciOiJSUzI1NiIsImtpZCI6IlZXRi0yc3VQa1Fjc3RHT3NUcFFIamN3ejlCQmpZclNqc21tTmtreWJhdUkifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJkZWZhdWx0Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZWNyZXQubmFtZSI6ImRlZmF1bHQtdG9rZW4tdzc3ZngiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoiZGVmYXVsdCIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6IjFjMDRkMjYwLTY4ZmYtNDVkMi05OGQ2LTQwYTc0NDU2MDc4YSIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDpkZWZhdWx0OmRlZmF1bHQifQ.PJNIDkzgHMq9Pf-1bCCRfWnPvFO-FSJ9VdzmL7rAk3ZDWb2OYxBFc3u6H78VJW6SgOILWygaWKW-12jwZVgArZlHxtJ8TXVGlc7HA1Q5g7l8ukohxqY69QAV8w-DQUC7kv6NFM4YQh355cP3LNkCihfK3Rv2UeD2DImhticb-p7t0TEElbWPVzFNpFl5wRcDfGiWMdb0IlNjySwtkwhV7XL4zPyQ5JQkNKU1YLCycwfLg23o-vQn84nc4Adg60HD7piNmw3dyDZhQJKafBL-yTtYEUQ0CFvS2ZO-AFhq2AvyU8WragVfgjk5C6SySRDKVtX-5wZAcPEGxinh0jgt2w"
config.api_key_prefix['authorization'] = 'Bearer'
config.host = 'https://192.168.50.21:6443'
config.verify_ssl=False

# api_client는 "2. 연결 정보 설정하기" 항목을 참고한다

kube = client.AutoscalingV1Api()

def create_hpa_object(name, namespace ,max_replicas, min_replicas, target_name,
                      target_cpu_utilization_percentage):
    hpa_body = client.V1HorizontalPodAutoscaler(
        metadata=client.V1ObjectMeta(
            name=name,
            namespace=namespace
        ),
        spec=client.V1HorizontalPodAutoscalerSpec(
            max_replicas=max_replicas,
            min_replicas=min_replicas,
            scale_target_ref=client.V1CrossVersionObjectReference(
                kind="Deployment",
                name=target_name
            ),
        target_cpu_utilization_percentage=target_cpu_utilization_percentage
        )
    )
    return hpa_body

def create_hpa(namespace, body):
    resp = kube.create_namespaced_horizontal_pod_autoscaler(namespace=namespace, body=body)
    return jsonify(str(resp.metadata.name))



hpa_body = create_hpa_object("nginx-deployment", 'default', 11, 3, 'nginx-deployment', 50)
create_hpa('default', hpa_body)


