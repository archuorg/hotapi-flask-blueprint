layui.use('element', function () {
    var element = layui.element;

    // 监听导航点击
    element.on('nav(demo)', function (elem) {
        layer.msg(elem.text());
    });
});

// 接口地址
var api_hot = "http://127.0.0.1:5000/v1/";

function render(elem_name, limit_num) {
    layui.use('flow', function () {
        var $ = layui.jquery;
        var flow = layui.flow;

        flow.load({
            elem: "#" + elem_name, // 指定列表容器
            end: "没有更多了",
            scrollElem: "#" + elem_name + "card", // 滚动条元素
            mb: 30,
            done: function (page, next) { // 到达临界点触发下一页
                var lis = [];

                // 使用 jQuery 的 Ajax 请求数据
                $.ajax({
                    url: api_hot + elem_name +'/',
                    method: 'GET',
                    dataType: 'json',
                    success: function (res) {
                        layui.each(res.data, function (index, item) {
                        var num = index + 1;
                        // console.log(num);
                        var num2 = page - 1;
                        // console.log(num2);
                        var num3 = num + num2 * limit_num;
                        // console.log(num3);

                        var img = ""; // 初始化图片标签
                        if(num3<=3){
                          var img_1 = "<img src='static/img/no1.png' width='32' height='18'>"
                          var img_2 = "<img src='static/img/no2.png' width='32' height='18'>"
                          var img_3 = "<img src='static/img/no3.png' width='32' height='18'>"
                          var str_left = '<li>'+"<a target='_blank' href='"+item.url+"'>";
                          var str_right = "    "+item.title+'</a></li>';
                          switch(num3){
                            case 1:
                              lis.push(str_left+img_1+str_right);
                              break;
                            case 2:
                              lis.push(str_left+img_2+str_right);
                              break;
                            case 3:
                              lis.push(str_left+img_3+str_right);
                              break;
                        }
                       }else{
                        var strnum = "<font color='#009688'>"+num3+"      "+"</font>";

                        var str_all = '<li>'+"<a target='_blank' href='"+item.url+"'"+strnum+item.title+'</a></li>';
                        lis.push(str_all);
                       }
                      });

                    // 执行下一页渲染，第二参数为：满足“加载更多”的条件
                    next(lis.join(''), page < res.pages);

                    },
                });
            }
        });
    });
}