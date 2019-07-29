## Antes de iniciar
Tenha certeza que o neo4j está instalado e sendo executado em sua máquina.  
Caso ainda não tenha, baixe o Neo4j Community Server no link: [Baixar](https://neo4j.com/download-center/#community).  
Em seguida, extraia, vá até a pasta `bin` do Neo4j e execute `./neo4j start`. É necessário ter o Oracle(R) Java(TM) 8, 
OpenJDK(TM) ou IBM J9 instalado.  

Também é necessário que o python3 e o pip estejam instalado, consulte como instalar na documentação da sua distribuição.  

É recomendável utilizar o vitualenv, use `sudo pip3 install virtualenv` para instalar.

## Como iniciar
Caso esteja usando virtualenv, crie seu ambiente python com:
`virtualenv env`, depois use `source env/bin/activate`.  

Instale as dependencias com `pip3 install -r requirements.txt`.  

Execute o programa com `python3 main.py`
