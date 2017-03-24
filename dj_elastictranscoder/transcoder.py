import boto3

from django.contrib.contenttypes.models import ContentType

from .models import EncodeJob


class Transcoder(object):

    def __init__(self, pipeline_id, region=None, access_key_id=None, secret_access_key=None):
        self.pipeline_id = pipeline_id

        self.client = boto3.client('elastictranscoder', aws_access_key_id=access_key_id,
                                   aws_secret_access_key=secret_access_key, region_name=region)

    def encode(self, input_name, outputs, **kwargs):
        self.message = self.client.create_job(
            PipelineId=self.pipeline_id,
            Input=input_name,
            Outputs=outputs,
            **kwargs
        )

    def create_job_for_object(self, obj):
        content_type = ContentType.objects.get_for_model(obj)

        job = EncodeJob()
        job.id = self.message['Job']['Id']
        job.content_type = content_type
        job.object_id = obj.pk
        job.save()
