FROM openjdk:23-jdk

WORKDIR /minecraft

COPY spigot-1.21.4.jar /minecraft/spigot.jar
COPY eula.txt /minecraft/eula.txt
COPY plugins /minecraft/plugins
COPY world /minecraft/world
COPY server.properties /minecraft/server.properties
COPY server-icon.png /minecraft/server-icon.png
COPY bukkit.yml /minecraft/bukkit.yml

EXPOSE 25565    

CMD ["java", "-Xmx1024M", "-Xms1024M", "-jar", "spigot.jar", "nogui"]
