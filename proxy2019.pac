// 直接走起的，先跑这个快，只要加常用的，加多了不如不加
var directHost = [
  '.com.cn',
  'baidu.com',
  '360.cn',
  'sina.com',
  '3zso.com',
  'huban',
  'partsbao'
];
// 要跳的
var freelist = [
  '.github.com',
  '.stackoverflow.com',
  '.softonic.com',
  '.sftcdn.net',
  '.torproject.org',
  '.youtube.com',
  '.ggpht.com',
  '.ytimg.com',
  '.google.com',
  '.google.com.hk',
  '.google-analytics.com',
  '.googleapis.com',
  '.googlecode.com',
  '.googlevideo.com',
  '.googleusercontent.com',
  '.ggpht.com',
  '.wikipedia.org',
  '.sf.net',
  '.sourceforge.net',
  'cdnjs.cloudflare.com',
  'wp.me',
  'ow.ly',
  'po.st',
  'goo.gl',
  'googlesyndication',
  'p.tanx.com',
  'a.alimama.cn',
  '.tube',
  '.pornhub.com',
  '.phncdn.com',
  '.pronhub.com',
  '.googleblog.com',
  '.box.com',
  '.mega.nz',
  '.ggpht.com',
  '.reddit.com',
  'mega.nz',
  '.sap.com'
];
var autoproxy = 'SOCKS5 127.0.0.1:1080; DIRECT';
// var blackhole = 'SOCKS5 127.0.0.1:7711; DIRECT';
var D = 'DIRECT';
//

function FindProxyForURL(url, host) {
  //
  // if (host.endsWtih('.cn')) return D;

  // 加速用
  for (var d in directHost) {
    if (dnsDomainIs(host, directHost[d])) return D;
  }

  // 非黑即白，别那麻烦
  for (var i in freelist) {
    if (dnsDomainIs(host, freelist[i])) return autoproxy;
  }
  return D;
}
