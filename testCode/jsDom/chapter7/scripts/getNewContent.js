function getNewContent() {
  //获取XMLHttpRequest
  var request = getHTTPObject();
  if (request) {
    request.open('GET', "example.txt", true);
    request.onreadystatechange = function() {
      // readState 属性值
      // 0 未初始化
      // 1 正在加载
      // 2 加载完毕
      // 3 正在交互
      // 4 表示成功
      console.log('request.readState');
      console.log(request.readyState);
      if (request.readyState == 4) {
        var para = document.createElement('p');
        //request.responseText => 文本形式数据
        var txt = document.createTextNode(request.responseText);
        console.log('txt');
        console.log(txt);
        para.appendChild(txt);
        document.getElementById('new').appendChild(para);
      }
    };
    request.send(null);
  } else {
    console.log('sorry your browser doesn\'t support XMLHttpRequest');
  }
}
