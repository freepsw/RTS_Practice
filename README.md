# Technical Guide for processing realtime data
## 1. Collection(Apache Flume)
- Flume Quick Glance
http://www.slideshare.net/madvirus/flume-29149433

- Why Flume?
  - 단순히 log를 수집하는것이 아니라 분산환경에서 다양한 유스케이스를 실행하는데 최적화 됨.
  - 예를 들면,
    1. sensor들의 정보를 수집해서 분석
    2. newwork device들의 성능을 모니터링
    3. 신뢰성, 안정정, 확장성을 지원하는 다양한 기능

## 2. Collection(Apache Kafka)
- Why Kafka?
  - kafka는 기존 message queue에서 사용하는 용도(messaging, website activity tracking, log aggregation, operational metrics, stream processing)로 주로 활용되고 있다.  
  - 그럼 왜 kafka를 써야하는 걸까?
  - 대부분의 message queue의 한계(fault tolerance, memory 용량에 따른 throughtput)를 극복할 수 있는 용도
  - disk기반으로 message 유실을 없애고, broker-partition을 활용하여 100K+/sec 성능을 충분히 보장


## 3. scala & java project 생성하기
- java와 scala를 동시에 compile하고 테스트할 수 있도록 build path 및 maven dependency를 설정한다.
- inetlliJ IDE를 활용한 사례 참고
- https://github.com/freepsw/java_scala

## 4. Realtime Processing (Apache Spark - Streaming)
- Why spark?
 - 유사한 straming sw(storm, flink, samza 등)들과 실시간 분산처리 성능은 유사하고,
 - 또한 데이터의 유실을 방지하는 exactly once도 유사하게 지원한다.
 - Apache spark의 장점은 실시간 처리와 함께 다양한 plugin(Graphx, SQL, MLlib)을 제공하여
 - 원하는 제품을 쉽게 확장할 수 있는데 그 장점이 있다. (Apache Flink도 일부 유사함)
 - 또한 수많은 commiter & contrubuter들의 참여 및 기업에서의 적용/투자를 통하여 제품의 안정성 및 성능이 지속적으로 검증 및 개선된다는 장점도 있다
 - 이는 Open source sw를 도입하고자 하는 기업의 관점에서는 가장 중요한 항목중에 하나이다.

- How to use?
 - 설치
  * Apache spark를 cluster로 구성하여 여러대로 분산처리가 가능하고,
  * 1대의 서버에서 thread를 여러개 생성하여 분산처리도 가능하다.
  * (이번 실습에서는 별도의 spark을 설치하지 않고, intelliJ Ide에서 직접 실행하여 spark streaming을 실행할 예정)

- 설치 가이드 (standalone cluster)
 * http://nberserk.github.io/2015/06/16/spark.html
 > - master가 될 컴퓨터에 spark 2.0.0 버전을 다운받아서 압축을 푼다
 > - conf/spark-env.sh 에
 > - SPARK_MASTER_IP 에 master ip 기입
 > - conf/slaves 에 slave ip 혹은 호스트 명을 기입 - 한줄에 하나씩
 > - spark 폴더 전체를 다른 slave에 복사. 앞서 설명한 bash script를 사용하면 쉽다.
 > - master에서 .sbin/start-all.sh 실행
 > - http://master_ip:8080/ 에 접속하면 spark web ui를 볼 수 있다.
- 설치 가이드 (yarn, mesos)
 * http://spark.apache.org/docs/latest/spark-standalone.html#installing-spark-standalone-to-a-cluster






# mark down examples
https://guides.github.com/features/mastering-markdown/
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
