# Laboratorio de MapReduce con MRJOB en AWS EMR

**Realizado por: Santiago Gallego - sgalle16**

## Prerrequisitos

- Cuenta de AWS
- Cliente SSH

## Configuración de AWS CLI

1. **Instalar y Configurar AWS CLI**
    - Siga las instrucciones en la [documentación oficial de AWS CLI](https://docs.aws.amazon.com/cli/) para instalar y configurar AWS CLI.
    - Cree un archivo llamado `credentials` dentro del directorio `~/.aws`:
      ```bash
      nano ~/.aws/credentials
      ```
    - Copie y pegue el bloque de texto con sus credenciales de acceso temporal proporcionadas por AWS Academy.
    - Verifique los permisos del archivo `credentials`:
      ```bash
      chmod 600 ~/.aws/credentials
      ```
    - Pruebe la configuración de AWS CLI:
      ```bash
      aws sts get-caller-identity
      ```
    - Añada la región:
      ```bash
      nano ~/.aws/config
      region: us-east-1
      ```
    - Verifique la conexión a AWS:
      ```bash
      aws s3 ls
      ```

## Creación de Bucket y Directorios en S3

1. **Crear el Bucket S3**:
    ```bash
    aws s3 mb s3://sgalle16-lab6-emr
    ```
2. **Preparar el Bucket S3**:
    - Crear una carpeta de logs:
      ```bash
      aws s3api put-object --bucket sgalle16-lab6-emr --key logs/
      ```
## Creación de Cluster EMR via AWS CLI

1. **Crear el Cluster EMR**:
    ```bash
    aws emr create-cluster \
    --name "emr-MyClusterEMR" \
    --log-uri "s3://sgalle16-lab6-emr/logs" \
    --release-label "emr-6.14.0" \
    --service-role "arn:aws:iam::065700887692:role/EMR_DefaultRole" \
    --unhealthy-node-replacement \
    --ec2-attributes '{"InstanceProfile":"EMR_EC2_DefaultRole","EmrManagedMasterSecurityGroup":"sg-05080db9603f1d3e8","EmrManagedSlaveSecurityGroup":"sg-0feb5d1697c33f02c","KeyName":"emr-key","SubnetId":"subnet-00a285a8f1c0a75c3"}' \
    --applications Name=Flink Name=HCatalog Name=Hadoop Name=Hive Name=Hue Name=JupyterEnterpriseGateway Name=JupyterHub Name=Livy Name=Oozie Name=Pig Name=Spark Name=Sqoop Name=Tez Name=Zeppelin Name=ZooKeeper \
    --configurations '[{"Classification":"hive-site","Properties":{"hive.metastore.client.factory.class":"com.amazonaws.glue.catalog.metastore.AWSGlueDataCatalogHiveClientFactory"}},{"Classification":"spark-hive-site","Properties":{"hive.metastore.client.factory.class":"com.amazonaws.glue.catalog.metastore.AWSGlueDataCatalogHiveClientFactory"}}]' \
    --instance-groups '[{"InstanceCount":1,"InstanceGroupType":"MASTER","Name":"Principal","InstanceType":"m5.xlarge","EbsConfiguration":{"EbsBlockDeviceConfigs":[{"VolumeSpecification":{"VolumeType":"gp2","SizeInGB":32},"VolumesPerInstance":2}]}},{"InstanceCount":1,"InstanceGroupType":"CORE","Name":"Central","InstanceType":"m5.xlarge","EbsConfiguration":{"EbsBlockDeviceConfigs":[{"VolumeSpecification":{"VolumeType":"gp2","SizeInGB":32},"VolumesPerInstance":2}]}},{"InstanceCount":1,"InstanceGroupType":"TASK","Name":"Tarea - 1","InstanceType":"m5.xlarge","EbsConfiguration":{"EbsBlockDeviceConfigs":[{"VolumeSpecification":{"VolumeType":"gp2","SizeInGB":32},"VolumesPerInstance":2}]}}]' \
    --scale-down-behavior "TERMINATE_AT_TASK_COMPLETION" \
    --region "us-east-1"
    ```
2. **Verificar la Creación del Cluster**:
    - Verifica que el clúster se haya creado correctamente:
      ```bash
      aws emr describe-cluster --cluster-id j-T93J9CTIWOLW
      ```
    - Obtenga el DNS público del nodo maestro:
      ```bash
      aws emr describe-cluster --cluster-id j-5Z2G0RU0BYVC --query "Cluster.MasterPublicDnsName"
      ```

## Conexión al Nodo Maestro

1. **Conectarse al Master node**:
    ```bash
    ssh -i ~/lab_mapreduce/emr-key.pem hadoop@ec2-3-227-20-175.compute-1.amazonaws.com
    ```

## Acceso a Hue y Gestión de HDFS

1. **Acceso a Hue desde Master Node**:
    ```bash
    ssh -i ~/emr-key.pem -N -L 8888:ec2-3-227-20-175.compute-1.amazonaws.com:8888 hadoop@ec2-3-227-20-175.compute-1.amazonaws.com
    ```
    ```bash
    sudo sed -i 's/.ec2.internal:14000/.ec2.internal:9870/' /etc/hue/conf/hue.ini
    sudo systemctl restart hue
    ```
2. **Configuración de HDFS**:
    
    ```bash
    sudo hdfs dfs -ls /user
    sudo -u hdfs hdfs dfs -mkdir /user/hadoop
    sudo -u hdfs hdfs dfs -chown hadoop:hadoop /user/hadoop
    sudo -u hdfs hdfs dfs -chown hadoop:hdfsadmingroup /user/hadoop
    sudo -u hdfs hdfs dfs -chmod 755 /user/hadoop
    sudo systemctl restart hue
    ```

## Instalación de Git en el Master Node

1. **Instalar Git**:
    ```bash
    sudo yum install git
    ```
2. **Clonar el Repositorio y Ejecutar Scripts**:
    - Clonar el repositorio:
      ```bash
      cd wordcount
      ```
    - Ejecutar el script localmente:
      ```bash
      python wordcount-local.py /datasets/gutenberg-small/*.txt > salida-serial.txt
      more salida-serial.txt
      ```

## Configuración y Pruebas de MRJOB

1. **Instalar MRJOB**:
    ```bash
    sudo yum install python3-pip -y
    sudo pip3 install mrjob
    ```
2. **Probar MRJOB Localmente**:
    ```bash
    python wordcount-mr.py ../datasets/gutenberg-small/*.txt
    ```

## Subir Archivos y Dataset a HDFS

1. **Subir Archivos a HDFS**:
    ```bash
    hdfs dfs -mkdir -p /user/hadoop/input/datasets
    hdfs dfs -put datasets/* /user/hadoop/input/datasets/
    hdfs dfs -mkdir -p /user/hadoop/output
    ```
2. **Verificar los Archivos en HDFS**:
    ```bash
    hdfs dfs -ls /user/hadoop/input
    hdfs dfs -ls /user/hadoop/input/datasets
    ```

## Ejecución de WordCount MapReduce en Cluster EMR

1. **Ejecutar WordCount dentro de wordcount**:
    ```bash
    python wordcount-mr.py hdfs:///user/hadoop/input/datasets/gutenberg-small/*.txt -r hadoop --output-dir hdfs:///user/hadoop/output -D mapred.reduce.tasks=10
    ```

## Verificación de la Salida

1. **Descargar y Verificar la Salida**:
    ```bash
    hdfs dfs -get /user/hadoop/output /home/hadoop/output
    cat /home/hadoop/output/part-00000
    ```

## Retos de MapReduce con MRJOB en Python

1. **Análisis de datos**:
    ```bash
    python <script>-mr.py hdfs:///user/hadoop/input/datasets/otros/<data>
    ```

### Referencias:

- Repositorio del curso
- [How to create and run an EMR cluster using AWS CLI](https://towardsdatascience.com/how-to-create-and-run-an-emr-cluster-using-aws-cli-3a78977dc7f0#9e7d)
- [Create AWS EMR Cluster Using AWS CLI and Submit job](https://www.youtube.com/watch?v=XsWnW7-8IGQ)
- [Authenticate with short-term credentials](https://docs.aws.amazon.com/cli/latest/userguide/cli-authentication-short-term.html)
