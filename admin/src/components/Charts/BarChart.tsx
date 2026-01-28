import React from 'react';
import ReactECharts from 'echarts-for-react';

interface BarChartProps {
  title?: string;
  data: {
    xAxis: string[];
    series: {
      name: string;
      data: number[];
    }[];
  };
  height?: number;
  horizontal?: boolean;
}

const BarChart: React.FC<BarChartProps> = ({
  title,
  data,
  height = 300,
  horizontal = false,
}) => {
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
    xAxis: horizontal
      ? {
          type: 'value',
        }
      : {
          type: 'category',
          data: data.xAxis,
        },
    yAxis: horizontal
      ? {
          type: 'category',
          data: data.xAxis,
        }
      : {
          type: 'value',
        },
    series: data.series.map((s) => ({
      name: s.name,
      type: 'bar',
      data: s.data,
      itemStyle: {
        borderRadius: [4, 4, 0, 0],
      },
    })),
  };

  return <ReactECharts option={option} style={{ height }} />;
};

export default BarChart;
