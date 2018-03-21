
## Maven2快速入门教程
http://www.blogjava.net/wanghaikuo/archive/2006/12/02/84985.html

现在maven似乎很火，但网上的中文资料大部分都是maven1的，对maven2的入门介绍比较少。

本文演示maven2的安装，配置和初步体验，不涉及深入的原理。

本文内容主要参考

http://maven.apache.org/guides/getting-started/maven-in-five-minutes.html

1.安装

下载Maven.目前的版本是2.0.4

http://www.apache.org/dyn/closer.cgi/maven/binaries/maven-2.0.4-bin.zip

解压缩后，设置环境变量M2_HOME到maven目录；在环境变量path中增加maven的bin目录。

在命令行输入

Mvn -version

显示

Maven version: 2.0.4

则安装成功。

2. 网络设置

maven运行时需要网络环境。如果你的网络需要代理，则要在maven目录的conf/settings.xml中设置。

找到<proxies>节点，按照例子，根据自己实际环境设置。

3.体验maven

在命令行中，进入你常用的项目文件夹，输入

mvn archetype:create -DgroupId=com.mycompany.app -DartifactId=my-app

如果网络配置正确，maven就会下载需要的文件，执行任务，最终显示“BUILD SUCCESSFUL”，并生成my-app目录。

让我们看一下mvn对项目目录的组织：

My-app

├─pom.xml

└─src

├─main

│ └─java

│ └─com

│ └─mycompany

│ └─app

│ └─App.java

└─test

└─java

└─com

└─mycompany

└─app

└─AppTest.java

可以看出，代码和测试代码分别放在main及test文件夹下。

Pom.xml描述项目对象模型（Project Object Model）。其模式文件为http://maven.apache.org/xsd/maven-4.0.0.xsd

详细的POM说明请参考相关资料。

4.maven命令

在命令行下输入mvn -h ， 显示mvn帮助，其中usage: mvn [options] [<goal(s)>] [<phase(s)>]表明了mvn命令的构成。

Options：可选的参数。比如前面提到的-version , -h等。

Goal(s): 表示maven构建的“目标”。比如前面的

mvn archetype:create -DgroupId=com.mycompany.app -DartifactId=my-app

其中archetype:create表示archetype插件下的create目标。这里，插件是为了某种目的构建的目标的集合，maven通过插件扩展其功能。

还可以为目标传递一些参数，比如上面的“-DgroupId=com.mycompany.app -DartifactId=my-app”。

Phase(s):阶段。表示maven构建生命周期 中的一个步骤。使用相位命令时，maven会执行生命周期中该阶段之前的所有命令，使项目处于指定的“状态”。

比如在刚才创建的项目路径下输入mvn compile，会创建target文件夹，并编译class，使项目处于“已编译”状态。

maven定义的生命周期中主要的相位如下：
validate: 验证项目是否正确以及相关信息是否可用。
compile: 编译。
test: 通过junit进行单元测试。
package: 根据事先指定的格式（比如jar），进行打包。
integration-test: 部署到运行环境中，准备进行集成测试。
verify: 对包进行有效性性和质量检查。
install: 安装到本地代码库。
deploy: 在集成或发布环境，将包发布到远程代码库。
在“默认”的生命周期之外，还有两个“阶段”：

clean: 清除以前的构建物。
site: 生成项目文档。
阶段实际上是通过目标的组合实现的。

5.组合命令

可以通过对目标及相位的组合使得一个命令完成多个功能，比如：

mvn clean dependency:copy-dependencies package

相当于按顺序执行

mvn clean

mvn dependency:copy-dependencies

mvn package

到这里，对maven应该有一个初步的印象并能上手使用了吧？更多的内容可以查阅相关的文档。

