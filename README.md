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
