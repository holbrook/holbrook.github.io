
Maven简单来说是Java世界的一种新型的build工具，比ant的最大好处是依赖的管理，以及配置文件的可读性，可复用性，可扩展性。Maven的配置文件称为POM，即Project Object Model。在Maven中，每一个插件或者模块都由groupId，artifactId，version唯一标示。还有两个可选的标示元素，一个是packaging，默认支持的选项有pom，jar，maven-plugin，ejb，war，ear，rar，par等，maven会根据packaging设置的不同为模块执行不同的目标（goal）；另一个是classifier，一般用不上。
