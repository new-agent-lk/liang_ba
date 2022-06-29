$(function () {
    //日线(量霸价投，对标中证100  code_flag=0)
    dateStock();
    //周线(量霸价投，对标中证100  code_flag=0)
    weekStock();
    //月线(量霸价投，对标中证100  code_flag=0)
    monthStock();
    //分时图(量霸价投，对标中证100  code_flag=0)
    echartsDom();

    //日线(量霸超额，对标中证500 code_flag = 1)
    dateStock1();
    //周线(量霸超额，对标中证500 code_flag = 1)
    weekStock1();
    //月线(量霸超额，对标中证500 code_flag = 1)
    monthStock1();
    //分时图(量霸超额，对标中证500 code_flag = 1)
    echartsDom1();

    //日线(量霸成长，对标沪深300 code_flag = 2)
    dateStock2();
    //周线(量霸成长，对标沪深300 code_flag = 2)
    weekStock2();
    //月线(量霸成长，对标沪深300 code_flag = 2)
    monthStock2();
    //分时图(量霸成长，对标沪深300 code_flag = 2)
    echartsDom2();




    
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
        var control_data = [];

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
                },
                {
                    name: 'control_data',
                    type: 'value',
                    data: control_data,
                    min: function (value) {
                        return value.min;
                    },
                    max: function (value) {
                        return value.max;
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
                },
                {
                    name: 'control_data',
                    data: control_data,
                    type: 'line',
                    yAxisIndex: 1,
                    lineStyle: {
                        normal: {
                            color: '#fc5e33'
                        }
                    }
                }
            ]
        };
        myChart.setOption(option);
        myChart.on('click', function (params) {
            alert(params.data);
        });
        $.get('/api/v1/data/tensc/day/?code_flag=0').done(function (response) {
            console.log(response);
            var xdata = [];
            var item = [];
            var nowDate = new Date();
            var nowMonth = nowDate.getMonth() + 1;
            var now = nowDate.getFullYear() + '-' + nowMonth + '-' + nowDate.getDate();
            xdata = response.dayk_data;
            data0 = splitData(xdata);

            response.control_data.data.forEach(function (v) {
                control_data.push(v[1]);
            })
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

        var timer = null;
        var xdata = [];
        var avg_price = [];
        var sh = [];
        var date = new Date();
        var now = date.getHours() + date.getMinutes();


        function getData() {
            xdata = [];
            avg_price = [];
            $.get('/api/v1/data/tensc/minsec/?code_flag=0').done(function (response) {
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
                data: ['avg_price', 'sh_data']
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

    function monthStock() {
        var myChart = echarts.init(document.getElementById('main4'));
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
        $.get('/api/v1/data/tensc/month/?code_flag=0').done(function (response) {
            console.log(response);
            var xdata = [];
            var item = [];
            var nowDate = new Date();
            var nowMonth = nowDate.getMonth() + 1;
            var now = nowDate.getFullYear() + '-' + nowMonth + '-' + nowDate.getDate();
            xdata = response.monthk_data;
            data0 = splitData(xdata);
            myChart.setOption({
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

    function weekStock() {
        var myChart = echarts.init(document.getElementById('main3'));
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
        $.get('/api/v1/data/tensc/week/?code_flag=0').done(function (response) {
            console.log(response);
            var xdata = [];
            var item = [];
            var nowDate = new Date();
            var nowMonth = nowDate.getMonth() + 1;
            var now = nowDate.getFullYear() + '-' + nowMonth + '-' + nowDate.getDate();
            xdata = response.weekk_data;
            data0 = splitData(xdata);
            myChart.setOption({
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

    function dateStock1() {
        var myChart = echarts.init(document.getElementById('main5'));
        window.onresize = function () {
            myChart.resize();
        };
        var upColor = '#ec0000';
        var upBorderColor = '#8A0000';
        var downColor = '#00da3c';
        var downBorderColor = '#008F28';
        var data0 = [];
        var control_data = [];

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
                },
                {
                    name: 'control_data',
                    type: 'value',
                    data: control_data,
                    min: function (value) {
                        return value.min;
                    },
                    max: function (value) {
                        return value.max;
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
                },
                {
                    name: 'control_data',
                    data: control_data,
                    type: 'line',
                    yAxisIndex: 1,
                    lineStyle: {
                        normal: {
                            color: '#fc5e33'
                        }
                    }
                }
            ]
        };
        myChart.setOption(option);
        myChart.on('click', function (params) {
            alert(params.data);
        });
        $.get('/api/v1/data/tensc/day/?code_flag=1').done(function (response) {
            console.log(response);
            var xdata = [];
            var item = [];
            var nowDate = new Date();
            var nowMonth = nowDate.getMonth() + 1;
            var now = nowDate.getFullYear() + '-' + nowMonth + '-' + nowDate.getDate();
            xdata = response.dayk_data;
            data0 = splitData(xdata);

            response.control_data.data.forEach(function (v) {
                control_data.push(v[1]);
            })
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

    function echartsDom1() {
        var myChart = echarts.init(document.getElementById('main6'));
        window.onresize = function () {
            myChart.resize();
        };

        var timer = null;
        var xdata = [];
        var avg_price = [];
        var sh = [];
        var date = new Date();
        var now = date.getHours() + date.getMinutes();


        function getData() {
            xdata = [];
            avg_price = [];
            $.get('/api/v1/data/tensc/minsec/?code_flag=1').done(function (response) {
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
                data: ['avg_price', 'sh_data']
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

    function monthStock1() {
        var myChart = echarts.init(document.getElementById('main8'));
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
        $.get('/api/v1/data/tensc/month/?code_flag=1').done(function (response) {
            console.log(response);
            var xdata = [];
            var item = [];
            var nowDate = new Date();
            var nowMonth = nowDate.getMonth() + 1;
            var now = nowDate.getFullYear() + '-' + nowMonth + '-' + nowDate.getDate();
            xdata = response.monthk_data;
            data0 = splitData(xdata);
            myChart.setOption({
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

    function weekStock1() {
        var myChart = echarts.init(document.getElementById('main7'));
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
        $.get('/api/v1/data/tensc/week/?code_flag=1').done(function (response) {
            console.log(response);
            var xdata = [];
            var item = [];
            var nowDate = new Date();
            var nowMonth = nowDate.getMonth() + 1;
            var now = nowDate.getFullYear() + '-' + nowMonth + '-' + nowDate.getDate();
            xdata = response.weekk_data;
            data0 = splitData(xdata);
            myChart.setOption({
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

    function dateStock2() {
        var myChart = echarts.init(document.getElementById('main9'));
        window.onresize = function () {
            myChart.resize();
        };
        var upColor = '#ec0000';
        var upBorderColor = '#8A0000';
        var downColor = '#00da3c';
        var downBorderColor = '#008F28';
        var data0 = [];
        var control_data = [];

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
                },
                {
                    name: 'control_data',
                    type: 'value',
                    data: control_data,
                    min: function (value) {
                        return value.min;
                    },
                    max: function (value) {
                        return value.max;
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
                },
                {
                    name: 'control_data',
                    data: control_data,
                    type: 'line',
                    yAxisIndex: 1,
                    lineStyle: {
                        normal: {
                            color: '#fc5e33'
                        }
                    }
                }
            ]
        };
        myChart.setOption(option);
        myChart.on('click', function (params) {
            alert(params.data);
        });
        $.get('/api/v1/data/tensc/day/?code_flag=2').done(function (response) {
            console.log(response);
            var xdata = [];
            var item = [];
            var nowDate = new Date();
            var nowMonth = nowDate.getMonth() + 1;
            var now = nowDate.getFullYear() + '-' + nowMonth + '-' + nowDate.getDate();
            xdata = response.dayk_data;
            data0 = splitData(xdata);

            response.control_data.data.forEach(function (v) {
                control_data.push(v[1]);
            })
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

    function echartsDom2() {
        var myChart = echarts.init(document.getElementById('main10'));
        window.onresize = function () {
            myChart.resize();
        };

        var timer = null;
        var xdata = [];
        var avg_price = [];
        var sh = [];
        var date = new Date();
        var now = date.getHours() + date.getMinutes();


        function getData() {
            xdata = [];
            avg_price = [];
            $.get('/api/v1/data/tensc/minsec/?code_flag=2').done(function (response) {
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
                data: ['avg_price', 'sh_data']
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

    function monthStock2() {
        var myChart = echarts.init(document.getElementById('main12'));
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
        $.get('/api/v1/data/tensc/month/?code_flag=2').done(function (response) {
            console.log(response);
            var xdata = [];
            var item = [];
            var nowDate = new Date();
            var nowMonth = nowDate.getMonth() + 1;
            var now = nowDate.getFullYear() + '-' + nowMonth + '-' + nowDate.getDate();
            xdata = response.monthk_data;
            data0 = splitData(xdata);
            myChart.setOption({
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

    function weekStock2() {
        var myChart = echarts.init(document.getElementById('main11'));
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
        $.get('/api/v1/data/tensc/week/?code_flag=2').done(function (response) {
            console.log(response);
            var xdata = [];
            var item = [];
            var nowDate = new Date();
            var nowMonth = nowDate.getMonth() + 1;
            var now = nowDate.getFullYear() + '-' + nowMonth + '-' + nowDate.getDate();
            xdata = response.weekk_data;
            data0 = splitData(xdata);
            myChart.setOption({
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

    //判断是否为前7天内的日期(参数格式'YYYY-MM-dd')
    function checkDate(date) {
        var myDate = new Date();
        myDate.setDate(myDate.getDate() - 7);
        var dateArray = [];
        var currentDate = '';
        var isPass = false;
        for (var i = 0; i < 7; i++) {
            var month = (myDate.getMonth() + 1) < 10 ? '0' + (myDate.getMonth() + 1) : (myDate.getMonth() + 1)
            currentDate = myDate.getFullYear() + '-' + month + '-' + myDate.getDate();
            if (date === currentDate) {
                isPass = true;
            }
            myDate.setDate(myDate.getDate() + 1);
        }
        if (isPass) {
            return true;
        } else {
            return false;
        }
    }

});