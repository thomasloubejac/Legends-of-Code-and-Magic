# Legends-of-Code-and-Magic
Our solution to this game on the platform Codingame.com

Faire tourner le projet en local :
```
git clone https://github.com/CodinGame/codingame-game-engine
git clone https://github.com/CodinGame/LegendsOfCodeAndMagic

cp -r codingame-game-engine/runner/src/main/java/com/codingame/gameengine LegendsOfCodeAndMagic/src/main/java/com/codingame/

vi LegendsOfCodeAndMagic/pom.xml
```
ajouter ces lignes (venant du codingame-gameengine pom.xml) dans le groupe <dependencies>
```
                <dependency>
                        <groupId>io.undertow</groupId>
                        <artifactId>undertow-core</artifactId>
                        <version>2.0.25.Final</version>
                </dependency>
                <dependency>
                        <groupId>commons-io</groupId>
                        <artifactId>commons-io</artifactId>
                        <version>2.4</version>
                </dependency>
                <dependency>
                        <groupId>org.javassist</groupId>
                        <artifactId>javassist</artifactId>
                        <version>3.22.0-GA</version>
                </dependency>
                <dependency>
                        <groupId>org.apache.commons</groupId>
                        <artifactId>commons-lang3</artifactId>
                        <version>3.5</version>
                </dependency>
                <dependency>
                        <groupId>org.yaml</groupId>
                        <artifactId>snakeyaml</artifactId>
                        <version>1.24</version>
                </dependency>
```
Pour build le projet : `mvn install` ou `mvn package`

Pour savoir quoi mettre dans le classpath : `mvn dependency:build-classpath`

mettre ça dans `export CLASSPATH=le truc qu’on vient de sortir`


script test :
```
#!/bin/bash

cd LegendsOfCodeAndMagic/target/test-classes/
java -cp $CLASSPATH Main
```

on execute le script et ça fait un jeu de PlayerEmpty pas très intéressant

pour faire jouer un script python :
```
vi LegendsOfCodeAndMagic/src/test/java/Main.java
```

remplacer 
```
gameRunner.addAgent(PlayerEmpty.class);
gameRunner.addAgent(PlayerEmpty.class);
```
par
```
gameRunner.addAgent("python3 -u player1.py");
gameRunner.addAgent("python3 -u player2.py");
```

Et voilà !!
