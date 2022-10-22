import pandas as pd

def convertToHtml(result,title):
    #将数据转换为html的table
    #result是list[list1,list2]这样的结构
    #title是list结构；和result一一对应。titleList[0]对应resultList[0]这样的一条数据对应html表格中的一列
    d = {}
    index = 0
    for t in title:
        d[t] = result[index]
        index = index+1
    df = pd.DataFrame(d)
    df = df[title]
    h = df.to_html(index=False)
    #pandas只能导出数据表格html，所以这里插入<img />标签，后期把&gt转义回来。。
    h = h.replace('&lt;', '<')
    h = h.replace('&gt;', '>')
    print(h)
    with open('1.html', 'w') as f:
        f.write(h)
        print("html文件已经生成！")

def sortTable():
    #没找到什么实现表格排序的好方法，替换法用js简单粗暴排序。。  生成的 2.html是排序过的，点击表头排序
    f = open("1.html", "r")
    f_new = open("2.html", "w")
    find_th = "<th>"
    find_td = "<td>"
    modif_th = '''<th id="th{num}" onclick="SortTable(this)" class="as">'''
    modif_td = '''<td name="td{num}">'''
    count1 = 0
    count2 = 0
    for line in f:
        if find_th in line:
            line = line.replace(find_th, modif_th.format(num=count1))
            count1 += 1
        if find_td in line:
            line = line.replace(find_td, modif_td.format(num=count2))
            count2 += 1
            if count2 == 5:
                count2 = 0
        f_new.write(line)
    f.close()
    js = '''<script type="text/javascript">
        var tag=1;
        function SortTable(obj){
            var td0s=document.getElementsByName("td0");//得到id为td0的一串列表，下相同
            var td1s=document.getElementsByName("td1");
            var td2s=document.getElementsByName("td2");
            var td3s=document.getElementsByName("td3");
            var td4s=document.getElementsByName("td4");
            var tdArray0=[];
            var tdArray1=[];
            var tdArray2=[];
            var tdArray3=[];
            var tdArray4=[];
            for(var i=0;i<td0s.length;i++){
                tdArray0.push(td0s[i].innerHTML);
            }//每串都写到数组中
            for(var i=0;i<td1s.length;i++){
                tdArray1.push(td1s[i].innerHTML);
            }
            for(var i=0;i<td2s.length;i++){
                tdArray2.push(td2s[i].innerHTML);
            }
            for(var i=0;i<td3s.length;i++){
                tdArray3.push(td3s[i].innerHTML);
            }
            for(var i=0;i<td4s.length;i++){
                tdArray4.push(td4s[i].innerHTML);
            }
            var tds = document.getElementsByName("td" + obj.id.substr(2, 1));
            //得到当前传入对象的那一列
            var columnArray=[];
            for(var i=0;i<tds.length;i++){
                columnArray.push(tds[i].innerHTML);
            }//当前那一列都写入column这个栈，是逆序的
            var orginArray=[];
            for(var i=0;i<columnArray.length;i++){
                orginArray.push(columnArray[i]);
            }//将这一列的内容再存储一遍，一会原来列表修改以后，
            //通过比对值的方式对应到当前行的内容，实现同行内容一起修改
            columnArray.sort();   //排序后的新值，只排序了当前列
            for(var i=0;i<columnArray.length;i++){
                for(var j=0;j<orginArray.length;j++){
                    if(orginArray[j]==columnArray[i]){
                        document.getElementsByName("td0")[i].innerHTML=tdArray0[j];
                        document.getElementsByName("td1")[i].innerHTML=tdArray1[j];
                        document.getElementsByName("td2")[i].innerHTML=tdArray2[j];
                        document.getElementsByName("td3")[i].innerHTML=tdArray3[j];
                        document.getElementsByName("td4")[i].innerHTML=tdArray4[j];
                        orginArray[j]=null;
                        break;
                    }
                }
            }
        }
    </script>'''
    f_new.write(js)
    f_new.close()

    #
    # result = [['2016-08-25', '2016-08-26', '2016-08-27'], [u'张三', u'李四', u'王二'],[u'111<br> <img src="1-mtl-1m4s.png" />', u'222<br> <img src="1-osl-1m10s.png" />',' ']]
    # title = [u'日期',u'姓名',u'图片']

