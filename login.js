const puppeteer = require('puppeteer');

// 定义用户和密码列表
const users = [
  { username: '13438186526', password: '19821124' },
  { username: '13678154062', password: '19821124' },
  { username: '15928968862', password: '19821124' }
];

(async () => {
  for (let i = 0; i < users.length; i++) {
    const { username, password } = users[i];

    // 为每个用户创建一个新的浏览器实例
    const browser = await puppeteer.launch({ headless: false });
    const page = await browser.newPage();

    let retryCount = 0;
    let success = false;

    while (retryCount < 3 && !success) {
      try {
        await page.goto('http://wwww.cq17.com:12345/index/Index/Userlogins.html');

        // 等待页面加载完成
        await page.waitForSelector('#content_name');
        await page.waitForSelector('#content_password');
        await page.waitForSelector('.content_button button');

        // 输入用户名和密码
        await page.type('#content_name', username);
        await page.type('#content_password', password);

        // 提交登录表单
        await page.click('.content_button button');

        // 等待登录成功
        await page.waitForNavigation();

        // 转到用户中心页面
        await page.goto('http://wwww.cq17.com:12345/index/User/index.html');

        // 等待页面加载完成
        await page.waitForSelector('.signinqd');

        // 点击红包领取
        await page.click('.signinqd');

        // 在领取红包后执行其他操作...

        // 点击安全退出
        await page.click('.quit a');

        // 等待安全退出完成
        await page.waitForNavigation();

        success = true;
      } catch (error) {
        console.error(`登录时出现错误: ${error}`);
        retryCount++;
      }
    }

    // 在处理完每个用户后关闭页面和浏览器
    await page.close();
    await browser.close();

    // 用户之间添加随机延时
    const delay = Math.floor(Math.random() * 5000) + 1000; // 随机延时1秒到6秒之间
    await delayTime(delay);
  }
})();

// 自定义延时函数
function delayTime(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}
