vrayMtlConverter.exe放到到根目录下，使用V-Ray Standalone渲染器渲染。

1，将准备转换测试对比的vrscene放入scene文件夹，有rename函数统一重新命名

origin文件存放mtl渲染结果（1.png  2.png  3.png）
transformed存放osl渲染结果（1.png  2.png  3.png）
统一按照其对应的vrscene序号命名。

2，运行main函数，autoTest函数会自动执行 场景转换-分别渲染-ssim测试-html生成



vrayMtlConverter.exe "d:/origin.vrscene" "d:/transformed.vrscene"
表示将origin.vrscene中的vrayMtl转换成krayMtl并存储为transformed.vrscene
