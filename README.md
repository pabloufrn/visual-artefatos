## Antes de iniciar
Tenha certeza que o neo4j está instalado e sendo executado em sua máquina.  
Caso ainda não tenha, baixe o Neo4j Community Server no link: [Baixar](https://neo4j.com/download-center/#community).  
Em seguida, extraia, vá até a pasta `bin` do Neo4j e execute `./neo4j start`. É necessário ter o Oracle(R) Java(TM) 8, 
OpenJDK(TM) ou IBM J9 instalado.  

Também é necessário que o python3 e o pip estejam instalados, consulte como instalar na documentação da sua distribuição.  

É recomendável utilizar o vitualenv, use `sudo pip3 install virtualenv` para instalar.

## Como iniciar
Caso esteja usando virtualenv, crie seu ambiente python com:
`virtualenv env`, depois use `source env/bin/activate`.  

Instale as dependencias com `pip3 install -r requirements.txt`.  

Execute o programa com `python3 main.py`

## Consultas
Obter todos os issues criados por um usuário:  
MATCH p=(u:user)-[c:CRIOU]->(i:issue) RETURN p LIMIT  
![Issues e criadores](img/quserissuecriou.png?raw=true "Issues e criadores")  
Obter todos o issues que um usuário participou ou criou:  
MATCH p=(u:user)-[]->(i:issue) RETURN p LIMIT 80  
![Participante/Criador de issue](img/quserissueparticipa.png?raw=true "Participante/Criador de issue")  
Obter o login de todos os pares de usuário tal que um criou uma issue que o outro participou, ou seja, as relações de usuário por meio das issues:  
MATCH (criador:user)-[:CRIOU]->(i:issue)<-[:PARTICIPA_DE]-(participante:user) where not criador.id = participante.id RETURN criador.login, participante.login  
![Issues e criadores](img/qcriadorparticipante.png?raw=true "Issues e criadores")  


