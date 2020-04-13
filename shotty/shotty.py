import boto3
import click
session = boto3.Session(profile_name='shotty')
ec2 = session.resource('ec2')
def filter_instances(project):
 instances = []
 if project:
  filters = [{'Name':'tag:Project','Values':[project]}]
  instances = ec2.instances.filter(Filters=filters)
 else:
  instances = ec2.instances.all()
 return instances
 


@click.group()
def instances():
    """Commands of Instanaces"""
@instances.command('list')
@click.option('--project',default=None,help="only instance for Project (tag Project:<name>)")
def list_instances(project):
 instances = filter_instances(project)
 for i in instances:
  tags = {t['Key']:t['Value'] for t in i.tags or []}
  print( ','.join((i.id,i.instance_type, i.state['Name'],tags.get('Project','No Project'))))
 return
        
        
@instances.command('stop')
@click.option('--project',default=None,help="only instance for Project (tag Project:<name>)")
def stop_instances(project):
 instances = filter_instances(project)
 for i in instances:
  print("Stopping the instances....{0}".format(i.id))
  i.stop()
 return
 
@instances.command('start')
@click.option('--project',default=None,help="only instance for Project (tag Project:<name>)")
def start_instances(project):
 instances = filter_instances(project)
 for i in instances:
  print("Starting the instances....{0}".format(i.id))
  i.start()
 return
    
if __name__ == '__main__':
 instances()
