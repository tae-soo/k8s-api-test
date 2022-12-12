from kubernetes import client, config
from kubernetes.stream import stream
import ssl

my_metrics = []
my_metrics.append(client.V2beta2MetricSpec(type='Resource', resource= client.V2beta2ResourceMetricSource(name='memory',target=client.V2beta2MetricTarget(average_utilization= 30,type='Utilization'))))

my_conditions = []
my_conditions.append(client.V2beta2HorizontalPodAutoscalerCondition(status = "True", type = 'AbleToScale'))

status = client.V2beta2HorizontalPodAutoscalerStatus(conditions = my_conditions, current_replicas = 1, desired_replicas = 1)

body = client.V2beta2HorizontalPodAutoscaler(
              api_version='autoscaling/v2beta2',
              kind='HorizontalPodAutoscaler',
              metadata=client.V1ObjectMeta(name=self.app_name),
              spec= client.V2beta2HorizontalPodAutoscalerSpec(
                  max_replicas=self.MAX_PODS,
                  min_replicas=self.MIN_PODS,
                  metrics = my_metrics,
                  scale_target_ref = client.V2beta2CrossVersionObjectReference(kind = 'Deployment', name = self.app_name, api_version = 'apps/v1'),
              ),
              status = status)
v2 = client.AutoscalingV2beta2Api()
ret = v2.create_namespaced_horizontal_pod_autoscaler(namespace='default', body=body, pretty=True)