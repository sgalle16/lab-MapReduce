# Curso ST0263 Tópicos Especiales en Telemática
# Laboratorio: Map/Reduce en Python con MRJOB.

* Despliegue un cluster EMR en su cuenta de AWS Academy, teniendo en cuenta la guia para esto. En este enlace, encuentra la documentación de AWS EMR (https://docs.aws.amazon.com/emr/index.html)
    * Reto: Consulte como realizar la implementación del cluster via AWS CLI. En el informe debe enviar la evidencia de los diferentes comandos que tuvo que ejecutar para poder instanciar el cluster EMR. Adjunte el paso a paso con los diferentes pantallazos de evidencia.

* Ejecutar la versión serial/secuencial de la aplicación de wordcount-local.py. Esto lo puede ejecutar en el main node del clúster EMR. Para esto clone este repositorio desde el main node del cluster y asuma todos los datos locales. Una vez clonado el repositorio, ejecute los siguientes comandos:
```sh
     user@master$ cd wordcount
     user@master$ python wordcount-local.py /datasets/gutenberg-small/*.txt > salida-serial.txt
     user@master$ more salida-serial.txt
```
* Ahora, vamos a proceder a ejecutar el programa escrito en python de word count que emplea el paradigma de programación Map/Reduce. Hay varias librerias de python para acceder a servicios MapReduce en Hadoop. Para efectos de este laboratorio vamos a utilzar MRJOB (https://mrjob.readthedocs.io/en/stable/). Esta es la libreria que nos permite escribir programas en python que empleen el paradigma de Map/Reduce. De igual forma, esta libreria, permite la ejecución del programa de manera local o sobre un clúster Hadoop. En este laboratorio, vamos a ejecutarlo de manera local y en el clúster EMR.

* Se puede emplear una version de python 2.x o 3.x, del sistema (como root) o con un manejador de versiones de node (pyenv o virtualenv).

* Como parte del sistema, se instalará mrjob así:

```sh
	user@master$ sudo yum install python3-pip
	user@master$ sudo pip3 install mrjob
````

* Probar mrjob python local:

```sh
	user@master$ cd wordcount
	user@master$ python wordcount-mr.py ./datasets/gutenberg-small/*.txt
````

* Ejecutar mrjob python en Hadoop con datos en hdfs o s3:

    * Reto: Se debe consultar en la documentación de mrjob para ejecutar en clusters AWS EMR. Se ejecutará algo similar a esto:

```sh
	user@master$ python wordcount-mr.py hdfs:///datasets/gutenberg-small/*.txt -r hadoop --output-dir hdfs:///user/<login>/result3 --hadoop-streaming-jar $HADOOP_STREAMING_HOME/hadoop-streaming.jar
```

Tenga en cuenta que el directorio 'result*' no puede existir. 

* Nota: "-D mapred.reduce.tasks=10" para especificar el nro de reducers en MRJOB

Debe entregar en el informe la evidencia de la ejecución de la aplicación así como el resultado. 

# Reto de Programación en Map/Reduce

A continuación se listan diferentes ejercicios básicos de MapReduce con MRJOB en python. Los puede verificar en su máquina local, sin embargo, debe envíar la evidencia de que se ejecutan en un cluster EMR.

1. Se tiene un conjunto de datos, que representan el salario anual de los empleados formales en Colombia por sector económico, según la DIAN. [datasets de ejemplo](../datasets/otros)

    *  La estructura del archivo es: (sececon: sector económico) (archivo: dataempleados.csv)

        idemp,sececon,salary,year

        3233,1234,35000,1960
        3233,5434,36000,1961
        1115,3432,34000,1980
        3233,1234,40000,1965
        1115,1212,77000,1980
        1115,1412,76000,1981
        1116,1412,76000,1982

    *  Realizar un programa en Map/Reduce, con hadoop en Python, que permita calcular:

        1. El salario promedio por Sector Económico (SE)
        2. El salario promedio por Empleado
        3. Número de SE por Empleado que ha tenido a lo largo de la estadística

2. Se tiene un conjunto de acciones de la bolsa, en la cual se reporta a diario el valor promedio por acción, la estructura de los datos es (archivo: dataempresas.csv):

    company,price,date

    exito,77.5,2015-01-01
    EPM,23,2015-01-01
    exito,80,2015-01-02
    EPM,22,2015-01-02
    …

    * Realizar un programa en Map/Reduce, con hadoop en Python, que permita calcular:

        1. Por acción, dia-menor-valor, día-mayor-valor
        2. Listado de acciones que siempre han subido o se mantienen estables.
        3. DIA NEGRO: Saque el día en el que la mayor cantidad de acciones tienen el menor valor de acción (DESPLOME), suponga una inflación independiente del tiempo.

3. Sistema de evaluación de películas (archivo: datapeliculas.csv): Se tiene un conjunto de datos en el cual se evalúan las películas con un rating, con la siguiente estructura:

    User,Movie,Rating,Genre,Date

    166,346,1,accion,2014-03-20
    298,474,4,accion,2014-03-20
    115,265,2,accion,2014-03-20
    253,465,5,accion,2014-03-20
    305,451,3,accion,2014-03-20
    …
    …

    * Realizar un programa en Map/Reduce, con hadoop en Python, que permita calcular:

        1. Número de películas vista por un usuario, valor promedio de calificación
        2. Día en que más películas se han visto
        3. Día en que menos películas se han visto
        4. Número de usuarios que ven una misma película y el rating promedio
        5. Día en que peor evaluación en promedio han dado los usuarios
        6. Día en que mejor evaluación han dado los usuarios
        7. La mejor y peor película evaluada por genero

* Fecha de entrega del informe: Viernes 31 de Mayo a las 6:00 pm por el buzón de interactiva virtual. La sustentación de los códigos y las actividades realizadas en este laboratorio/reto se programarán posterior a la entrega. Este trabajo es de carácter individual.
* Debe realizar un video de entrega explicando detalladamente TODOS los aspectos que le permitieron realizar el laboratorio.código 




