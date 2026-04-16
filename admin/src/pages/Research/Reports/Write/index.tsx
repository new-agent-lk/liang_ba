import React, { useState } from "react";
import {
  Alert,
  Button,
  Card,
  Form,
  Input,
  Modal,
  Select,
  Space,
  Tabs,
  Typography,
  message,
} from "antd";
import { CopyOutlined } from "@ant-design/icons";
import MDEditor from "@uiw/react-md-editor";
import PageHeader from "@/components/Common/PageHeader";
import { MarkdownFormItem } from "@/components/Common/MarkdownEditor";
import { createReport } from "@/api/reports";
import { RESEARCH_STRATEGY_TYPES } from "@/types";
import writingGuideMarkdown from "../writing-guide.md?raw";
import exampleReportMarkdown from "../example-report.md?raw";

const { TextArea } = Input;
const { Option } = Select;
const { Paragraph, Text } = Typography;

const ReportsWrite: React.FC = () => {
  const [form] = Form.useForm();
  const [guideModalVisible, setGuideModalVisible] = useState(false);
  const [submitLoading, setSubmitLoading] = useState(false);

  const handleOpenGuide = () => {
    setGuideModalVisible(true);
  };

  const copyMarkdown = async (content: string, successText: string) => {
    try {
      await navigator.clipboard.writeText(content);
      message.success(successText);
    } catch {
      message.error("复制失败，请手动复制");
    }
  };

  const applyTemplateToForm = () => {
    form.setFieldsValue({
      title: "请替换为你的研究标题",
      summary: "请用 2-3 句话概括研究结论、适用场景与主要风险。",
      strategy_name: "请替换策略名称",
      strategy_type: "multi_factor",
      market: "A股",
      content: exampleReportMarkdown,
    });
    setGuideModalVisible(false);
    message.success("已套用范文");
  };

  const handleClear = () => {
    form.resetFields();
  };

  const handleSubmit = async () => {
    try {
      const values = await form.validateFields();
      setSubmitLoading(true);
      await createReport({
        ...values,
        status: "draft",
      });
      message.success("草稿已保存");
      form.resetFields();
    } catch (error) {
      if (!(error instanceof Error) || !("errorFields" in error)) {
        message.error("保存草稿失败");
      }
    } finally {
      setSubmitLoading(false);
    }
  };

  return (
    <>
      <PageHeader
        title="报告撰写"
        description="这里专门用于起草研究报告，保存后进入草稿，后续可在管理页继续编辑、提审和发布。"
        actions={[
          <Button key="guide" onClick={handleOpenGuide}>
            查看范文
          </Button>,
          <Button key="template" onClick={applyTemplateToForm}>
            套用范文
          </Button>,
          <Button key="clear" onClick={handleClear}>
            清空
          </Button>,
          <Button
            key="save"
            type="primary"
            loading={submitLoading}
            onClick={handleSubmit}
          >
            保存草稿
          </Button>,
        ]}
      />

      <Card title="报告撰写区">
        <Alert
          type="info"
          showIcon
          style={{ marginBottom: 16 }}
          message="推荐按“研究背景 / 核心观点 / 策略逻辑 / 回测表现 / 风险提示 / 结论建议”组织正文。"
        />
        <Form form={form} layout="vertical">
          <Form.Item
            name="title"
            label="报告标题"
            rules={[{ required: true, message: "请输入报告标题" }]}
          >
            <Input placeholder="例如：高股息红利策略在震荡市场中的表现复盘" />
          </Form.Item>

          <Form.Item name="summary" label="摘要">
            <TextArea
              rows={3}
              placeholder="概括研究目标、核心发现、适用场景与主要风险"
            />
          </Form.Item>

          <div
            style={{
              display: "grid",
              gridTemplateColumns: "1fr 1fr 1fr",
              gap: 16,
            }}
          >
            <Form.Item name="strategy_name" label="策略名称">
              <Input placeholder="如：红利低波组合" />
            </Form.Item>
            <Form.Item name="strategy_type" label="策略类型">
              <Select placeholder="请选择策略类型" allowClear>
                {RESEARCH_STRATEGY_TYPES.map((item) => (
                  <Option key={item.value} value={item.value}>
                    {item.label}
                  </Option>
                ))}
              </Select>
            </Form.Item>
            <Form.Item name="market" label="适用市场">
              <Input placeholder="如：A股、港股、期货" />
            </Form.Item>
          </div>

          <MarkdownFormItem
            name="content"
            label="报告正文 (Markdown)"
            required
            height={520}
            placeholder="直接在这里写报告正文。"
          />
        </Form>
      </Card>

      <Modal
        title="研究报告写作范文与规范"
        open={guideModalVisible}
        onCancel={() => setGuideModalVisible(false)}
        footer={null}
        width={980}
      >
        <Alert
          type="info"
          showIcon
          style={{ marginBottom: 16 }}
          message="这里提供研究报告写作规范、Markdown 范文和完整示例，方便研究员学习并直接套用。"
        />
        <Tabs
          items={[
            {
              key: "guide",
              label: "写作规范",
              children: (
                <div data-color-mode="light">
                  <Paragraph type="secondary">
                    推荐先阅读规范，再决定使用完整范文或直接套用示例。
                  </Paragraph>
                  <Space style={{ marginBottom: 16 }}>
                    <Button
                      icon={<CopyOutlined />}
                      onClick={() =>
                        copyMarkdown(writingGuideMarkdown, "写作规范已复制")
                      }
                    >
                      复制规范
                    </Button>
                  </Space>
                  <MDEditor.Markdown
                    source={writingGuideMarkdown}
                    style={{
                      backgroundColor: "#fff",
                      padding: 16,
                      border: "1px solid #f0f0f0",
                      borderRadius: 8,
                      maxHeight: 560,
                      overflow: "auto",
                    }}
                  />
                </div>
              ),
            },
            {
              key: "example",
              label: "Markdown 范文",
              children: (
                <div data-color-mode="light">
                  <Paragraph>
                    <Text strong>用途：</Text>
                    适合直接套用结构，再按自己的研究主题替换内容。
                  </Paragraph>
                  <Space style={{ marginBottom: 16 }}>
                    <Button
                      icon={<CopyOutlined />}
                      onClick={() =>
                        copyMarkdown(
                          exampleReportMarkdown,
                          "Markdown 范文已复制",
                        )
                      }
                    >
                      复制范文
                    </Button>
                    <Button type="primary" onClick={applyTemplateToForm}>
                      套用到写作区
                    </Button>
                  </Space>
                  <MDEditor.Markdown
                    source={exampleReportMarkdown}
                    style={{
                      backgroundColor: "#fff",
                      padding: 16,
                      border: "1px solid #f0f0f0",
                      borderRadius: 8,
                      maxHeight: 560,
                      overflow: "auto",
                    }}
                  />
                </div>
              ),
            },
          ]}
        />
      </Modal>
    </>
  );
};

export default ReportsWrite;
