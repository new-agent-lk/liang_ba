
const args = process.argv.slice(2);

const input_path = args[0];
const out_path = args[1];
if (!input_path) {
  console.error('请提供 input_path 参数');
  process.exit(1);
}
if (!out_path) {
  console.error('请提供 out_path 参数');
  process.exit(1);
}

const puppeteer = require('puppeteer');

(async () => {
  // 启动 Chrome 浏览器
  const browser = await puppeteer.launch({
    headless: 'new'
  });

  // 打开一个新的页面
  const page = await browser.newPage();

  // 导航到要截图的网页
  const fileURL = 'file://' + input_path; // 将 URL 替换为您要截图的网页 URL
  await page.goto(fileURL);

  // 等待页面加载完成
  await page.waitForSelector('body');
  await page.setViewport({ width: 800, height: 500 });
  await page.waitForTimeout(5000);

  // 截取整个页面的截图
  const screenshot = await page.screenshot({ dpi: 300 });

  // 保存截图为图片文件
  const fs = require('fs');
  fs.writeFileSync(out_path, screenshot);

  // 关闭浏览器
  await browser.close();
})();
