import React from 'react';
import ReactECharts from 'echarts-for-react';

interface LineChartProps {
  title?: string;
  data: {
    xAxis: string[];
    series: {
      name: string;
      data: number[];
    }[];
  };
  height?: number;
}

const LineChart: React.FC<LineChartProps> = ({ title, data, height = 300 }) => {
  const option = {
    title: title
      ? {
          text: title,
          left: 'center',
          textStyle: {
            fontSize: 14,
            fontWeight: 'normal',
          },
        }
      : undefined,
    tooltip: {
      trigger: 'axis',
    },
    legend: {
      data: data.series.map((s) => s.name),
      bottom: 0,
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '10%',
      containLabel: true,
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: data.xAxis,
    },
    yAxis: {
      type: 'value',
    },
    series: data.series.map((s) => ({
      name: s.name,
      type: 'line',
      data: s.data,
      smooth: true,
      areaStyle: {
        opacity: 0.1,
      },
    })),
  };

  return <ReactECharts option={option} style={{ height }} />;
};

export default LineChart;
