$(function () {
    var annual_yield = $('.desc-box .annual-yield');
    var retreat_rate = $('.desc-box .retreat-rate');

    // Store all chart instances for global resize
    var chartInstances = [];

    // Global resize handler for all ECharts
    $(window).on('resize', function () {
        chartInstances.forEach(function (chart) {
            if (chart && chart.resize) {
                chart.resize();
            }
        });
    });

    //日线(量霸价投，对标中证100  code_flag=0)
    dateStock('main', 0);
    //周线(量霸价投，对标中证100  code_flag=0)
    weekStock('main3', 0);
    //月线(量霸价投，对标中证100  code_flag=0)
    monthStock('main4', 0);
    //分时图(量霸价投，对标中证100  code_flag=0)
    echartsDom('main2' , 0);

    //日线(量霸超额，对标中证500 code_flag = 1)
    dateStock('main5', 1);
    //周线(量霸超额，对标中证500 code_flag = 1)
    weekStock('main7', 1);
    //月线(量霸超额，对标中证500 code_flag = 1)
    monthStock('main8', 1);
    //分时图(量霸超额，对标中证500 code_flag = 1)
    echartsDom('main6', 1);

    //日线(量霸成长，对标沪深300 code_flag = 2)
    dateStock('main9', 2);
    //周线(量霸成长，对标沪深300 code_flag = 2)
    weekStock('main11', 2);
    //月线(量霸成长，对标沪深300 code_flag = 2)
    monthStock('main12', 2);
    //分时图(量霸成长，对标沪深300 code_flag = 2)
    echartsDom('main10', 2);

    /*
        id：盒子div的id
        flag： 接口code_flag的值
    */

    function dateStock(id, flag) {
        var myChart = echarts.init(document.getElementById(id));
        chartInstances.push(myChart);
        window.onresize = function () {
            myChart.resize();
        };
        var upColor = '#ec0000';
        var upBorderColor = '#8A0000';
        var downColor = '#00da3c';
        var downBorderColor = '#008F28';
        var data0 = [];
        var control_data = [];
        var flag_info = null;
        var annual_yield = '.day-annual-yield' + flag;
        var retreat_rate = '.day-retreat-rate' + flag;

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
                text: '',
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
                axisLine: { onZero: false },
                splitLine: { show: false },
                min: 'dataMin',
                max: 'dataMax'
            },
            yAxis: [
                {
                    scale: true,
                    splitArea: {
                        show: true
                    }
                }
            ],
            dataZoom: [
                {
                    type: 'inside',
                    start: 0,
                    end: 100
                },
                {
                    show: true,
                    type: 'slider',
                    top: '90%',
                    start: 0,
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
        $.get('/api/v1/data/tensc/day/?code_flag=' + flag).done(function (response) {
            console.log(response);
            var xdata = [];
            var item = [];
            var nowDate = new Date();
            var nowMonth = nowDate.getMonth() + 1;
            var now = nowDate.getFullYear() + '-' + nowMonth + '-' + nowDate.getDate();
            xdata = response.dayk_data;
            data0 = splitData(xdata);
            flag_info = response.flag_info.slice(0, 4);
            $('.desc-box ' + annual_yield ).text((response.annual_yield*100).toFixed(2) + '%');
            $('.desc-box ' + retreat_rate).text((response.retreat_rate*100).toFixed(2) + '%');

            response.control_data.data.forEach(function (v) {
                control_data.push(v[1]);
            })
            myChart.setOption({
                title: {
                    text: flag_info
                },
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

    function echartsDom(id, flag) {
        var myChart = echarts.init(document.getElementById(id));
        chartInstances.push(myChart);
        window.onresize = function () {
            myChart.resize();
        };

        var timer = null;
        var xdata = [];
        var avg_price = [];
        var sh = [];
        var date = new Date();
        var now = date.getHours() + date.getMinutes();
        var flag_info = null;
        var annual_yield = '.minsec-annual-yield' + flag;
        var retreat_rate = '.minsec-retreat-rate' + flag;


        function getData() {
            xdata = [];
            avg_price = [];
            $.get('/api/v1/data/tensc/minsec/?code_flag=' + flag).done(function (response) {
                flag_info = response.flag_info;
                $('.desc-box ' + annual_yield ).text((response.annual_yield*100).toFixed(2) + '%');
                $('.desc-box ' + retreat_rate).text((response.retreat_rate*100).toFixed(2) + '%');
                response.last_work_data.forEach(function (v) {
                    // 时间展示形式
                    newData = v[0].split("");
                    xdata.push(newData[0] + newData[1] + ':' + newData[2] + newData[3]);
                    avg_price.push(v[1]);
                });
                response.control_data.data.forEach(function (val) {
                    sh.push(val[1]);
                })
                myChart.setOption({
                    title: {
                        text: flag_info
                    },
                    xAxis: {
                        data: xdata
                    },
                    series: [
                        {
                            name: 'avg_price',
                            data: avg_price
                        },
                        {
                            name: 'sh_data',
                            data: sh
                        }
                    ]
                });
                if (!response.is_work_time) {
                    clearInterval(timer);
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
            legend: {
                data: ['avg_price', 'sh_data'],
                right: 0
            },
            // 横坐标
            xAxis: {
                type: 'category',
                boundaryGap: false,
                data: xdata,
            },
            // 纵坐标
            yAxis: [
                {
                    name: 'avg_peice',
                    type: 'value',
                    data: avg_price,
                    max: 100,
                    min: function (value) {
                        return value.min;
                    },
                    max: function (value) {
                        return value.max;
                    }
                }, {
                    name: 'sh_data',
                    type: 'value',
                    data: sh,
                    min: function (value) {
                        return value.min;
                    },
                    max: function (value) {
                        return value.max;
                    }
                }
            ],
            // 数据
            series: [
                {
                    name: 'avg_price',
                    type: 'line',
                    symbol: 'none',
                    lineStyle: {
                        normal: {
                            color: 'green'
                        }
                    }
                },
                {
                    name: 'sh_data',
                    type: 'line',
                    symbol: 'none',
                    yAxisIndex: 1,
                    lineStyle: {
                        normal: {
                            color: 'skyblue'
                        }
                    }
                }
            ],
        };
        getData();


        timer = setInterval(function () {
            getData();
        }, 3000 * 60);



        myChart.setOption(option);
    };

    function monthStock(id, flag) {
        var myChart = echarts.init(document.getElementById(id));
        chartInstances.push(myChart);
        window.onresize = function () {
            myChart.resize();
        };
        var upColor = '#ec0000';
        var upBorderColor = '#8A0000';
        var downColor = '#00da3c';
        var downBorderColor = '#008F28';
        var data0 = [];
        var flag_info = null;
        var annual_yield = '.month-annual-yield' + flag;
        var retreat_rate = '.month-retreat-rate' + flag;

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
                text: '',
                left: 0
            },
            tooltip: {
                trigger: 'axis',
                axisPointer: {
                    type: 'cross'
                }
            },
            legend: {
                data: ['月K', 'MA5', 'MA10', 'MA20', 'MA30']
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
                axisLine: { onZero: false },
                splitLine: { show: false },
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
                    start: 0,
                    end: 100
                },
                {
                    show: true,
                    type: 'slider',
                    top: '90%',
                    start: 0,
                    end: 100
                }
            ],
            // 数据
            series: [
                {
                    name: '月K',
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
        $.get('/api/v1/data/tensc/month/?code_flag=' + flag).done(function (response) {
            console.log(response);
            var xdata = [];
            var item = [];
            var nowDate = new Date();
            var nowMonth = nowDate.getMonth() + 1;
            var now = nowDate.getFullYear() + '-' + nowMonth + '-' + nowDate.getDate();
            xdata = response.monthk_data;
            data0 = splitData(xdata);
            flag_info = response.flag_info.slice(0, 4);
            $('.desc-box ' + annual_yield ).text((response.annual_yield*100).toFixed(2) + '%');
            $('.desc-box ' + retreat_rate).text((response.retreat_rate*100).toFixed(2) + '%');
            myChart.setOption({
                title: {
                    text: flag_info
                },
                xAxis: {
                    type: 'category',
                    data: data0.categoryData
                },
                series: [
                    {
                        name: '月K',
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

    function weekStock(id, flag) {
        var myChart = echarts.init(document.getElementById(id));
        chartInstances.push(myChart);
        window.onresize = function () {
            myChart.resize();
        };
        var upColor = '#ec0000';
        var upBorderColor = '#8A0000';
        var downColor = '#00da3c';
        var downBorderColor = '#008F28';
        var data0 = [];
        var flag_info = null;
        var annual_yield = '.week-annual-yield' + flag;
        var retreat_rate = '.week-retreat-rate' + flag;

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
                text: '',
                left: 0
            },
            tooltip: {
                trigger: 'axis',
                axisPointer: {
                    type: 'cross'
                }
            },
            legend: {
                data: ['周K', 'MA5', 'MA10', 'MA20', 'MA30']
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
                axisLine: { onZero: false },
                splitLine: { show: false },
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
                    start: 0,
                    end: 100
                },
                {
                    show: true,
                    type: 'slider',
                    top: '90%',
                    start: 0,
                    end: 100
                }
            ],
            // 数据
            series: [
                {
                    name: '周K',
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
        $.get('/api/v1/data/tensc/week/?code_flag=' + flag).done(function (response) {
            console.log(response);
            var xdata = [];
            var item = [];
            var nowDate = new Date();
            var nowMonth = nowDate.getMonth() + 1;
            var now = nowDate.getFullYear() + '-' + nowMonth + '-' + nowDate.getDate();
            xdata = response.weekk_data;
            data0 = splitData(xdata);
            flag_info = response.flag_info.slice(0, 4);
            $('.desc-box ' + annual_yield ).text((response.annual_yield*100).toFixed(2) + '%');
            $('.desc-box ' + retreat_rate).text((response.retreat_rate*100).toFixed(2) + '%');
            myChart.setOption({
                title: {
                    text: flag_info
                },
                xAxis: {
                    type: 'category',
                    data: data0.categoryData
                },
                series: [
                    {
                        name: '周K',
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

});