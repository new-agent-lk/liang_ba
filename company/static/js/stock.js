$(function () {
    // 日k线
    dateStock();

    //周k线
    weekStock();

    //月k线
    monthStock();

    //动态数据
    echartsDom();

    checkDate();


    function dateStock() {
    var myChart = echarts.init(document.getElementById('main'));
    window.onresize = function () {
        myChart.resize();
    };
        var option = {
        // 标题
        title: {
            text: '今日K线'
        },
        // 工具箱 保存图片
        // toolbox: {
        //   show: true,
        //   feature: {
        //       saveAsImage: {
        //           show: true
        //       }
        //   }
        // },
        tooltip: {
            trigger: 'axis'
        },
        // 图例声明
        legend: {
          data:['open', 'high', 'low', 'close'],
            right: 100
        },
        // 横坐标
        xAxis: {
            data: []
        },
        // 纵坐标
        yAxis: [
            {
                type: 'value',
                // boundaryGap: [0, '50%'],
                position: 'left'
            }
        ],
        // 数据
        series: [
            {   name: 'open',
                type: 'line',
                symbol: 'none',
                data: [],
                lineStyle: {
                    normal: {
                        color: 'skyblue'
                    }
                },
                itemStyle: {
                    color: 'skyblue'
                }
            },
            {   name: 'high',
                type: 'line',
                symbol: 'none',
                data: [],
                lineStyle: {
                    normal: {
                        color: '#c26611'
                    }
                },
                itemStyle: {
                    color: '#c26611'
                }
            },
            {   name: 'low',
                type: 'line',
                symbol: 'none',
                data: [],
                lineStyle: {
                    normal: {
                        color: '#d33392'
                    }
                },
                itemStyle: {
                    color: '#d33392'
                }
            },
            {
                name: 'close',
                type: 'line',
                symbol: 'none',
                data: [],
                lineStyle: {
                    normal: {
                        color: '#0fd342'
                    }
                },
                itemStyle: {
                    color: '#0fd342'
                }
            }
        ]
    };
        myChart.setOption(option);
        myChart.on('click', function (params) {
            alert(params.data);
        });

        $.get('/api/v1/data/history?stock_codes=sz399001').done(function (response) {
            console.log(response);
            var xdata = [];
            var high = [];
            var low = [];
            var open = [];
            var close = [];
            var min =  10000;
            var max =  15000;
            var nowDate = new Date();
            var nowMonth = nowDate.getMonth()+1;
            if (nowMonth < 10) {
                nowMonth = '0' + nowMonth;
            }
            var now = nowDate.getFullYear() + '-' + nowMonth + '-' + nowDate.getDate();
            console.log(now);
            $.each(response.sz399001, function (k, v) {
                if (v.day.slice(0, 10) == now) {
                    xdata.push(v.day);
                    high.push(v.high);
                    low.push(v.low);
                    open.push(v.open);
                    close.push(v.close)
                }

            });
            for (var i=0;i<high.length;i++) {
                if (i>i+1) {
                    max = high[i];
                } else {
                    max = high[i+1];
                }
            }
            for (var i = 0; i < low.length; i++) {
                if (i < i + 1) {
                    min = low[i] -300;
                } else {
                    min = low[i+1] -300;
                }
            }
            myChart.setOption({
                xAxis: {
                    data: xdata
                },
                series: [
                    {
                        name: 'open',
                        data: open
                    },
                    {
                        name: 'high',
                        data: high
                    },
                    {
                        name: 'low',
                        data: low
                    },
                    {
                        name: 'close',
                        data: close
                    }
                ],
                yAxis: {
                    min: min,
                    max: max
                }
            })
        })
};

    function echartsDom() {
    var myChart = echarts.init(document.getElementById('main2'));
    window.onresize = function () {
        myChart.resize();
    };

    // var base = +new Date(2014, 9, 3);
    // var oneDay = 24 * 3600 * 1000;
    // var date = [];
    // var data = [Math.random() * 10000];
    var now = new Date();
        var xdata = [];
        var now_price = [];

        function getData(shift) {
            // now = now.getFullYear()+'-'+(now.getMonth()+1)+'-'+now.getDate()+'T'+now.getHours()+':'+now.getMinutes()+':'+now.getSeconds();
            $.get('http://liangbax.com/api/v1/data/current/sz399001/').done(function (response) {
                xdata.push(response.data.current_time);
                now_price.push(response.data.now_price);
                if (shift) {
                    xdata.shift();
                    now_price.shift();
                }
            });
        }


    var option = {
        // 标题
        title: {
            text: '定时数据'
        },
        tooltip: {
            trigger: 'axis'
        },
        // 图例声明
        legend: {
            data: ['成交'],
            right: 150
        },
        // 横坐标
        xAxis: {
            type: 'category',
            boundaryGap: false,
            data: xdata
        },
        // 纵坐标
        yAxis: {
            min: 12000,
            max: 12500,
            type: 'value',
            data: now_price
        },
        // 数据
        series: [
            {
                name: 'now_price',
                type: 'line',
                smooth: true,
                symbol: 'none',
                stack: 'a'
            }
        ],
    };
        $.get('http://liangbax.com/api/v1/data/current/sz399001/').done(function (response) {
            console.log(response);

            $.each(response.today_data, function (k, v) {
                if (v.now_price != 0) {
                    xdata.push(v.current_time);
                    now_price.push(v.now_price);
                }
            });
            myChart.setOption({
                xAxis: {
                    data: xdata
                },
                series: [
                    {
                        name: 'now_price',
                        data: now_price
                    }
                ]
            })
        });

    setInterval(function () {
        getData(true);
        myChart.setOption({
            xAxis: {
                data: xdata
            },
            series: [
                {
                    name: 'now_price',
                    data: now_price
                }
            ]
        });
    }, 1000*60);

    myChart.setOption(option);
};

    function monthStock() {
    var myChart = echarts.init(document.getElementById('main4'));
    window.onresize = function () {
        myChart.resize();
    };
        var option = {
        // 标题
        title: {
            text: '本月K线'
        },
        tooltip: {
            trigger: 'axis'
        },
        // 图例声明
        legend: {
          data:['open', 'high', 'low', 'close'],
            right: 100
        },
        // 横坐标
        xAxis: {
            data: []
        },
        // 纵坐标
        yAxis: [
            {
                type: 'value',
                // boundaryGap: [0, '50%'],
                position: 'left'
            }
        ],
        // 数据
        series: [
            {   name: 'open',
                type: 'line',
                symbol: 'none',
                data: [],
                lineStyle: {
                    normal: {
                        color: 'skyblue'
                    }
                },
                itemStyle: {
                    color: 'skyblue'
                }
            },
            {   name: 'high',
                type: 'line',
                symbol: 'none',
                data: [],
                lineStyle: {
                    normal: {
                        color: '#c26611'
                    }
                },
                itemStyle: {
                    color: '#c26611'
                }
            },
            {   name: 'low',
                type: 'line',
                symbol: 'none',
                data: [],
                lineStyle: {
                    normal: {
                        color: '#d33392'
                    }
                },
                itemStyle: {
                    color: '#d33392'
                }
            },
            {
                name: 'close',
                type: 'line',
                symbol: 'none',
                data: [],
                lineStyle: {
                    normal: {
                        color: '#0fd342'
                    }
                },
                itemStyle: {
                    color: '#0fd342'
                }
            }
        ]
    };
        myChart.setOption(option);
        myChart.on('click', function (params) {
            alert(params.data);
        });

        $.get('/api/v1/data/history?stock_codes=sz399001').done(function (response) {
            var xdata = [];
            var high = [];
            var low = [];
            var open = [];
            var close = [];
            var min =  10000;
            var max =  15000;
            var nowDate = new Date();
            var nowMonth = nowDate.getMonth()+1;
            if (nowMonth < 10) {
                nowMonth = '0' + nowMonth;
            }
            var now = nowDate.getFullYear() + '-' + nowMonth + '-' + nowDate.getDate();
            $.each(response.sz399001, function (k, v) {
                    xdata.push(v.day.slice(0, 10));
                    high.push(v.high);
                    low.push(v.low);
                    open.push(v.open);
                    close.push(v.close)
            });
            for (var i=0;i<high.length;i++) {
                if (i>i+1) {
                    max = high[i];
                } else {
                    max = high[i+1];
                }
            }
            for (var i = 0; i < low.length; i++) {
                if (i < i + 1) {
                    min = low[i] -1000;
                } else {
                    min = low[i+1] -1000;
                }
            }
            myChart.setOption({
                xAxis: {
                    data: xdata
                },
                series: [
                    {
                        name: 'open',
                        data: open
                    },
                    {
                        name: 'high',
                        data: high
                    },
                    {
                        name: 'low',
                        data: low
                    },
                    {
                        name: 'close',
                        data: close
                    }
                ],
                yAxis: {
                    min: min,
                    max: max
                }
            })
        })
};

    function weekStock() {
    var myChart = echarts.init(document.getElementById('main3'));
    window.onresize = function () {
        myChart.resize();
    };
        var option = {
        // 标题
        title: {
            text: '周K线'
        },
        tooltip: {
            trigger: 'axis'
        },
        // 图例声明
        legend: {
          data:['open', 'high', 'low', 'close'],
            right: 100
        },
        // 横坐标
        xAxis: {
            data: []
        },
        // 纵坐标
        yAxis: [
            {
                type: 'value',
                // boundaryGap: [0, '50%'],
                position: 'left'
            }
        ],
        // 数据
        series: [
            {   name: 'open',
                type: 'line',
                symbol: 'none',
                data: [],
                lineStyle: {
                    normal: {
                        color: 'skyblue'
                    }
                },
                itemStyle: {
                    color: 'skyblue'
                }
            },
            {   name: 'high',
                type: 'line',
                symbol: 'none',
                data: [],
                lineStyle: {
                    normal: {
                        color: '#c26611'
                    }
                },
                itemStyle: {
                    color: '#c26611'
                }
            },
            {   name: 'low',
                type: 'line',
                symbol: 'none',
                data: [],
                lineStyle: {
                    normal: {
                        color: '#d33392'
                    }
                },
                itemStyle: {
                    color: '#d33392'
                }
            },
            {
                name: 'close',
                type: 'line',
                symbol: 'none',
                data: [],
                lineStyle: {
                    normal: {
                        color: '#0fd342'
                    }
                },
                itemStyle: {
                    color: '#0fd342'
                }
            }
        ]
    };
        myChart.setOption(option);
        myChart.on('click', function (params) {
            alert(params.data);
        });

        $.get('/api/v1/data/history?stock_codes=sz399001').done(function (response) {
            var xdata = [];
            var high = [];
            var low = [];
            var open = [];
            var close = [];
            var min =  10000;
            var max =  15000;

            $.each(response.sz399001, function (k, v) {
                if (checkDate(v.day.slice(0, 10))) {
                    xdata.push(v.day.slice(0, 10));
                    high.push(v.high);
                    low.push(v.low);
                    open.push(v.open);
                    close.push(v.close);
                }

            });
            for (var i=0;i<high.length;i++) {
                if (i>i+1) {
                    max = high[i];
                } else {
                    max = high[i+1];
                }
            }
            for (var i = 0; i < low.length; i++) {
                if (i < i + 1) {
                    min = low[i] -500;
                } else {
                    min = low[i+1] -500;
                }
            }
            myChart.setOption({
                xAxis: {
                    data: xdata
                },
                series: [
                    {
                        name: 'open',
                        data: open
                    },
                    {
                        name: 'high',
                        data: high
                    },
                    {
                        name: 'low',
                        data: low
                    },
                    {
                        name: 'close',
                        data: close
                    }
                ],
                yAxis: {
                    min: min,
                    max: max
                }
            })
        })
};

    //判断是否为前7天内的日期(参数格式'YYYY-MM-dd')
    function checkDate(date) {
        var myDate = new Date();
        myDate.setDate(myDate.getDate()-7);
        var dateArray = [];
        var currentDate = '';
        var isPass = false;
        for (var i = 0; i < 7; i++) {
            var month = (myDate.getMonth()+1)<10?'0'+(myDate.getMonth()+1):(myDate.getMonth()+1)
            currentDate = myDate.getFullYear() +'-'+ month +'-'+ myDate.getDate();
            if (date === currentDate) {
                isPass = true;
            }
            myDate.setDate(myDate.getDate()+1);
        }
        if (isPass) {
            return true;
        } else {
            return false;
        }
    }

});