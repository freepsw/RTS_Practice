# Technical Guide for processing realtime data
## 1. Collection(Apache Flume)

- Flume Quick Glance
http://www.slideshare.net/madvirus/flume-29149433 

### 1-1. Let's install
 * Step 1: Download latest Flume release from Apache [Website](http://archive.apache.org/dist/flume/)
```
> cd ~
> mkdir apps
> cd apps
> wget http://archive.apache.org/dist/flume/stable/apache-flume-1.6.0-bin.tar.gz
> sudo tar -xzvf apache-flume-1.6.0-bin.tar.gz
```
 * Step 2: Configure Environment Setting
```
> vi ~/.bash_profile  //아래의 내용을 파일 끝에 추가한다.
export FLUME_HOME=/home/rts/apps/apache-flume-1.6.0-bin
export FLUME_CONF_DIR=$FLUME_HOME/conf
export FLUME_CLASSPATH=$FLUME_CONF_DIR
export PATH=$PATH:$FLUME_HOME/bin
> source ~/.bash_profile //변경된 내용을 shell에 적용
``` 
 * Step 3: Flume Config Setting
```
> cd /home/rts/apps/apache-flume-1.6.0-bin/conf
> cp flume-env.sh.template flume-env.sh
> vi flume-env.sh  // 아래의 내용을 추가한다. java의 경우는 JAVA_HOME 설정을 그래도 활용
$JAVA_OPTS="-Xms500m -Xmx1000m -Dcom.sun.management.jmxremote"
export JAVA_HOME=/opt/jdk1.8.0_91
```
> flume-ng --help //명령어가 정상적으로 동작하는지 확인

### 1-2. Flume Tutorial [link] (http://www.tutorialspoint.com/apache_flume/)
 * Why Flume?
  - 단순히 log를 수집하는것이 아니라 분산환경에서 다양한 유스케이스를 실행하는데 최적화 됨.
  - 예를 들면, 
    1. sensor들의 정보를 수집해서 분석
    2. newwork device들의 성능을 모니터링
    3. 신뢰성, 안정정, 확장성을 지원하는 다양한 기능
 * Fetching Twitter Data
  - sink를 logggerSink로 변경
```
# Naming the components on the current agent.
TwitterAgent.sources = Twitter
TwitterAgent.channels = MemChannel
TwitterAgent.sinks = loggerSink  //hadoop를 설치하지 않았기 때문에 logger로 변경함. 

# Describing/Configuring the source
TwitterAgent.sources.Twitter.type = org.apache.flume.source.twitter.TwitterSource
TwitterAgent.sources.Twitter.consumerKey = consumerKey
TwitterAgent.sources.Twitter.consumerSecret = consumerSecret
TwitterAgent.sources.Twitter.accessToken = accessToken
TwitterAgent.sources.Twitter.accessTokenSecret = accessTokenSecret
TwitterAgent.sources.Twitter.keywords = tutorials point,java, bigdata, mapreduce, mahout, hbase, nosql

# Describing/Configuring the sink
TwitterAgent.sinks.loggerSink.type = logger

# Describing/Configuring the channel TwitterAgent.channels.MemChannel.type = memory
TwitterAgent.channels.MemChannel.type                   = memory
TwitterAgent.channels.MemChannel.capacity               = 10000
TwitterAgent.channels.MemChannel.transactionCapacity    = 100

# Binding the source and sink to the channel
TwitterAgent.sources.Twitter.channels = MemChannel
TwitterAgent.sinks.loggerSink.channel = MemChannel
```
  - 실행 

  ```
  > bin/flume-ng agent --conf ./conf/ -f conf/twitter.conf Dflume.root.logger=DEBUG,console -n TwitterAgent
  ```
  - 
  - 추가 설정
    * twitter에서 조회한 데이터는 FLUME_HOME/logs/flume.log에 저장됨.
    * 이 flume.log를 열어보면 "body: 4F 62 6A 01 02 16 61 76 72 6F 2E 73 63 68 65 6D"와 같은 문자열만 출력됨.
    * 해결방안 
      * conf/log4j.properties 파일에서 "flume.root.logger=ALL,LOGFILE"로 변경
      * twitter
  - 결과 확인
   * TwitterAgent.sources.Twitter.keywords = tutorials point,java, bigdata, mapreduce, mahout, hbase, nosql에서 설정한 keyword에 대항하는 내용만 추출하고 있음.

# mark down examples
As Kanye West said:

> We're living the future so
> the present is our past.

I think you should use an
`<addr>` element here instead.

```javascript
function fancyAlert(arg) {
  if(arg) {
    $.facebox({div:'#foo'})
  }
}
```

    function fancyAlert(arg) {
      if(arg) {
        $.facebox({div:'#foo'})
      }
    }


- [x] @mentions, #refs, [links](), **formatting**, and <del>tags</del> supported
- [x] list syntax required (any unordered or ordered list supported)
- [x] this is a complete item
- [ ] this is an incomplete item

First Header | Second Header
------------ | -------------
Content from cell 1 | Content from cell 2
Content in the first column | Content in the second column

#1
mojombo#1
mojombo/github-flavored-markdown#1

# Structured documents

Sometimes it's useful to have different levels of headings to structure your documents. Start lines with a `#` to create headings. Multiple `##` in a row denote smaller heading sizes.

### This is a third-tier heading

You can use one `#` all the way up to `######` six for different heading sizes.

If you'd like to quote someone, use the > character before the line:

> Coffee. The finest organic suspension ever devised... I beat the Borg with it.
> - Captain Janeway
