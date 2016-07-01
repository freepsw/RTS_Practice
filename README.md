# Technical Guide for processing realtime data
## 1. Collection(Apache Flume)

- Flume Quick Glance
http://www.slideshare.net/madvirus/flume-29149433
### Let's install
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
