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
        $.get('/api/v1/data/tensc/day/').done(function (response) {
            console.log(response);
            var xdata = [];
            var item = [];
            var nowDate = new Date();
            var nowMonth = nowDate.getMonth() + 1;
            var now = nowDate.getFullYear() + '-' + nowMonth + '-' + nowDate.getDate();
            console.log(now);
            xdata = response.dayk_data;
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

        var timer = null;
        var xdata = [];
        var avg_price = [];
        var sh = [];
        var date = new Date();
        var now = date.getHours() + date.getMinutes();


        function getData() {
            $.get('/api/v1/data/tensc/minsec').done(function (response) {
                console.log(response);
                response.last_work_data.forEach(function (v) {
                    // 时间展示形式
                    newData = v[0].split("");
                    xdata.push(newData[0]+newData[1]+ ':'+newData[2]+newData[3]);
                    avg_price.push(v[1]);
                });
                response.custom_data.data.forEach(function (val) {
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
                    min: function(value) {
                        return value.min;
                    },
                    max: function(value) {
                        return value.max;
                    }
                }, {
                    name: 'sh_data',
                    type: 'value',
                    data: sh,
                    min: function(value) {
                        return value.min;
                    },
                    max: function(value) {
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


        timer = setInterval(function () {
            avg_price = [];
            sh = [];
            getData();
        }, 3000 * 60);

        getData();


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
        $.get('/api/v1/data/tensc/month/').done(function (response) {
            console.log(response);
            var xdata = [];
            var item = [];
            var nowDate = new Date();
            var nowMonth = nowDate.getMonth() + 1;
            var now = nowDate.getFullYear() + '-' + nowMonth + '-' + nowDate.getDate();
            console.log(now);
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
        $.get('/api/v1/data/tensc/week/').done(function (response) {
            console.log(response);
            var xdata = [];
            var item = [];
            var nowDate = new Date();
            var nowMonth = nowDate.getMonth() + 1;
            var now = nowDate.getFullYear() + '-' + nowMonth + '-' + nowDate.getDate();
            console.log(now);
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