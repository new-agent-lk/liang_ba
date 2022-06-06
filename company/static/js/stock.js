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
        var upColor = '#ec0000';
        var upBorderColor = '#8A0000';
        var downColor = '#00da3c';
        var downBorderColor = '#008F28';
        var data0 = [];

        function calculateMA(dayCount) {
            var result = [];
            for (var i = 0, len = data0.values.length; i < len; i++) {
                if (i < dayCount) {
                    result.push('-');
                    continue;
                }
                var sum = 0;
                for (var j = 0; j < dayCount; j++) {
                    sum += +data0.values[i - j][1];
                }
                result.push(sum / dayCount);
            }
            return result;
        }

        function splitData(rawData) {
            var categoryData = [];
            var values = [];
            for (var i = 0; i < rawData.length; i++) {
                categoryData.push(rawData[i].splice(0, 1)[0]);
                values.push(rawData[i]);
            }
            return {
                categoryData: categoryData,
                values: values
            };
        }


        var option = {
            // 标题
            title: {
                text: '深证指数',
                left: 0
            },
            tooltip: {
                trigger: 'axis',
                axisPointer: {
                    type: 'cross'
                }
            },
            legend: {
                data: ['日K', 'MA5', 'MA10', 'MA20', 'MA30']
            },
            grid: {
                left: '10%',
                right: '10%',
                bottom: '15%'
            },
            xAxis: {
                type: 'category',
                data: [],
                boundaryGap: false,
                axisLine: {onZero: false},
                splitLine: {show: false},
                min: 'dataMin',
                max: 'dataMax'
            },
            yAxis: {
                scale: true,
                splitArea: {
                    show: true
                }
            },
            dataZoom: [
                {
                    type: 'inside',
                    start: 50,
                    end: 100
                },
                {
                    show: true,
                    type: 'slider',
                    top: '90%',
                    start: 50,
                    end: 100
                }
            ],
        // 数据
            series: [
                {
                    name: '日K',
                    type: 'candlestick',
                    data: [],
                    itemStyle: {
                        color: upColor,
                        color0: downColor,
                        borderColor: upBorderColor,
                        borderColor0: downBorderColor
                    },
                    markPoint: {
                        label: {
                            formatter: function (param) {
                                return param != null ? Math.round(param.value) + '' : '';
                            }
                        },
                        data: [
                            {
                                name: 'Mark',
                                coord: ['2013/5/31', 2300],
                                value: 2300,
                                itemStyle: {
                                    color: 'rgb(41,60,85)'
                                }
                            },
                            {
                                name: 'highest value',
                                type: 'max',
                                valueDim: 'highest'
                            },
                            {
                                name: 'lowest value',
                                type: 'min',
                                valueDim: 'lowest'
                            },
                            {
                                name: 'average value on close',
                                type: 'average',
                                valueDim: 'close'
                            }
                        ],
                        tooltip: {
                            formatter: function (param) {
                                return param.name + '<br>' + (param.data.coord || '');
                            }
                        }
                    },
                    markLine: {
                        symbol: ['none', 'none'],
                        data: [
                            [
                                {
                                    name: 'from lowest to highest',
                                    type: 'min',
                                    valueDim: 'lowest',
                                    symbol: 'circle',
                                    symbolSize: 10,
                                    label: {
                                        show: false
                                    },
                                    emphasis: {
                                        label: {
                                            show: false
                                        }
                                    }
                                },
                                {
                                    type: 'max',
                                    valueDim: 'highest',
                                    symbol: 'circle',
                                    symbolSize: 10,
                                    label: {
                                        show: false
                                    },
                                    emphasis: {
                                        label: {
                                            show: false
                                        }
                                    }
                                }
                            ],
                            {
                                name: 'min line on close',
                                type: 'min',
                                valueDim: 'close'
                            },
                            {
                                name: 'max line on close',
                                type: 'max',
                                valueDim: 'close'
                            }
                        ]
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
            var item = [];
            var nowDate = new Date();
            var nowMonth = nowDate.getMonth()+1;
            // if (nowMonth < 10) {
            //     nowMonth = '0' + nowMonth;
            // }
            var now = nowDate.getFullYear() + '-' + nowMonth + '-' + nowDate.getDate();
            console.log(now);
            $.each(response.sz399001, function (k, v) {
                // if (v.day.slice(0, 10) == now) {
                //     xdata.push(v.day);
                //     high.push(v.high);
                //     low.push(v.low);
                //     open.push(v.open);
                //     close.push(v.close)
                // }
                    item = [v.day, v.open, v.close, v.low, v.high];
                    xdata.push(item);


            });
            data0 = splitData(xdata);
            myChart.setOption({
                xAxis: {
                    type: 'category',
                    data: data0.categoryData
                },
                series: [
                    {
                        name: '日K',
                        data: data0.values
                    },
                    {
                        name: 'MA5',
                        type: 'line',
                        data: calculateMA(5),
                        smooth: true,
                        lineStyle: {
                            opacity: 0.5
                        }
                    },
                    {
                        name: 'MA10',
                        type: 'line',
                        data: calculateMA(10),
                        smooth: true,
                        lineStyle: {
                            opacity: 0.5
                        }
                    },
                    {
                        name: 'MA20',
                        type: 'line',
                        data: calculateMA(20),
                        smooth: true,
                        lineStyle: {
                            opacity: 0.5
                        }
                    },
                    {
                        name: 'MA30',
                        type: 'line',
                        data: calculateMA(30),
                        smooth: true,
                        lineStyle: {
                            opacity: 0.5
                        }
                    }
                ],
            })
        })
};

    function echartsDom() {
        var myChart = echarts.init(document.getElementById('main2'));
        window.onresize = function () {
            myChart.resize();
        };

        var isActive = true;
        var xdata = [];
        var avg_price = [];
        var date = new Date();
        var now = date.getHours() + date.getMinutes();


        function getData(shift) {
            $.get('http://www.liangbax.com/api/v1/data/tensc/').done(function (response) {
                xdata.push(now);
                avg_price.push(response.avg_price);
                if (shift) {
                    xdata.shift();
                    avg_price.shift();
                }
            });
        }


        var option = {
            // 标题
            title: {
                text: '分时图'
            },
            tooltip: {
                trigger: 'axis'
            },
            // 图例声明
            // legend: {
            //     data: ['成交'],
            //     right: 150
            // },
            // 横坐标
            xAxis: {
                type: 'category',
                boundaryGap: false,
                data: xdata,
                axisTick: {
                    show: false//不显示坐标轴刻度线
                },
                axisLabel: {
                    show: false,//不显示坐标轴上的文字
                }
            },
            // 纵坐标
            yAxis: {
                axisTick: {
                    show: false//不显示坐标轴刻度线
                },
                axisLabel: {
                    show: false,//不显示坐标轴上的文字
                },
                type: 'value',
                data: avg_price,
                min: function (value) {
                    return value.min;
                },
                max: function (value) {
                    return value.max;
                }
            },
            // 数据
            series: [
                {
                    name: 'avg_price',
                    type: 'line',
                    symbol: 'none'
                }
            ],
        };

        $.get('http://www.liangbax.com/api/v1/data/tensc/').done(function (response) {
            console.log(response);
            response.last_work_data.forEach(function (v) {
                xdata.push(v[0]);
                avg_price.push(v[1]);
            })
            myChart.setOption({
                xAxis: {
                    data: xdata
                },
                series: [
                    {
                        name: 'avg_price',
                        data: avg_price
                    }
                ]
            });
        });

        setInterval(function () {
            getData(true);
            myChart.setOption({
                xAxis: {
                    data: xdata
                },
                series: [
                    {
                        name: 'avg_price',
                        data: avg_price
                    }
                ]
            });
        }, 3000 * 60);


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
        // legend: {
        //   data:['open', 'high', 'low', 'close'],
        //     right: 100
        // },
        // 横坐标
        xAxis: {
            axisTick: {
                show: false//不显示坐标轴刻度线
            },
            axisLabel: {
                show: false,//不显示坐标轴上的文字
            },
            data: []
        },
        // 纵坐标
        yAxis: [
            {
                type: 'value',
                // boundaryGap: [0, '50%'],
                position: 'left',
                axisTick: {
                    show: false//不显示坐标轴刻度线
                },
                axisLabel: {
                    show: false,//不显示坐标轴上的文字
                }
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
        // legend: {
        //   data:['open', 'high', 'low', 'close'],
        //     right: 100
        // },
        // 横坐标
        xAxis: {
            data: [],
                        axisTick: {
                show: false//不显示坐标轴刻度线
            },
            axisLabel: {
                show: false,//不显示坐标轴上的文字
            }
        },
        // 纵坐标
        yAxis: [
            {
                type: 'value',
                // boundaryGap: [0, '50%']
                position: 'left',
                axisTick: {
                    show: false//不显示坐标轴刻度线
                },
                axisLabel: {
                    show: false,//不显示坐标轴上的文字
                }
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