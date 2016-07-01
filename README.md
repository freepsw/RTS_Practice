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

#### Sample 1 :  Fetching Twitter Data
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

#### Sample 2 : NetCat Source
 * Scenario : NecCat source를 이용하여 수집된 데이터를 logger를 통해 저장하는 예제
 * Configuring Flume
  ```
  #Naming the components on the current agent
  NetcatAgent.sources = Netcat
  NetcatAgent.channels = MemChannel
  NetcatAgent.sinks = LoggerSink
  
  # Describing/Configuring the source
  NetcatAgent.sources.Netcat.type = netcat
  NetcatAgent.sources.Netcat.bind = localhost
  NetcatAgent.sources.Netcat.port = 56565
  
  # Describing/Configuring the sink
  NetcatAgent.sinks.LoggerSink.type = logger
  
  # Describing/Configuring the channel
  NetcatAgent.channels.MemChannel.type = memory
  NetcatAgent.channels.MemChannel.capacity = 1000
  NetcatAgent.channels.MemChannel.transactionCapacity = 100
  
  # Bind the source and sink to the channel
  NetcatAgent.sources.Netcat.channels = MemChannel
  NetcatAgent.sinks.LoggerSink.channel = MemChannel
  ```
 * Execute Flume

  ```
bin/flume-ng agent --conf $FLUME_HOME/conf --conf-file $FLUME_HOME/conf/netcat.conf --name NetcatAgent -Dflume.root.logger=INFO,console
  ```
  
 * Send message using Telnet

    ```
    > curl telnet://localhost:56565 
connected 
    ```
  
#### Sample 3 : Flume Interceptor [link](http://hadoopathome.logdown.com/posts/293904-apache-flume-interceptors-modifying-the-event-body)
 * Flume Event는 header + body로 구성됨  
 ![flume evtns](http://i.imgur.com/uIe8eQE.png)
 * interceptor는 body 수정(filter, extract, add information ...)
 * Secnario : Sample2에 Interceptor를 삽입하여 timestamp가 출력되도록 한다.
 * java로 interceptor class를 구현하고 jar로 생성하여, FLUME_HOME/lib 아래로 복사한다.
  * [source project](https://github.com/benwatson528/flume-timestamp-body-interceptor)
  * 아래의 함수가 실제 event를 interceptor하여 조작하는 함수
  ```
  @Override
	public Event intercept(Event event) {
		byte[] eventBody = event.getBody();
		event.setBody(appendTimestampToBody(eventBody, System.nanoTime()));
		return event;
	}
	
	protected byte[] appendTimestampToBody(byte[] startEventBody, long time) {
		try {
			this.timeBytes = Long.toString(time).getBytes();
			this.outputBodyLength 	= startEventBody.length + this.separator.length + this.timeBytes.length;
			this.outputStream 		= new ByteArrayOutputStream(this.outputBodyLength);
			this.outputStream.write(startEventBody);
			this.outputStream.write(this.separator);
			this.outputStream.write(this.timeBytes);
			return this.outputStream.toByteArray();
		} catch (IOException ex) {
			this.logger.error("Couldn't add timestamp to body", ex);
			throw new RuntimeException("Couldn't add timestamp to body", ex);
		}
	}
  ```
 * config 파일 수정 (intercepor 추가)
  ```
  > cp netcat.conf interceptorNetcat.conf
  
  # Describing/Configuring the interceptor
  InNetcatAgent.sources.Netcat.interceptors = i1
  InNetcatAgent.sources.Netcat.interceptors.i1.type = uk.co.hadoopathome.flume.timestampbodyinterceptor.TimestampBodyInterceptor$Builder
  InNetcatAgent.sources.Netcat.interceptors.i1.separator = , //구분자를 ","로 지정함.
  ```
  
 * flume 실행
   ```
bin/flume-ng agent --conf $FLUME_HOME/conf --conf-file $FLUME_HOME/conf/interceptorNetcat.conf --name InNetcatAgent -Dflume.root.logger=INFO,console
  ```
 * telnet 실행
  ```
curl telnet://localhost:56565
test
OK
  ```

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
