东方财富网报表采用json文件保存表格数据，抓取时，文本数字用编码代替，如下：<br>
```
{"scode":"002323","sname":"*ST百特","securitytype":"A股","trademarket":"深交所风险警示板","latestnoticedate":"2018-08-31T00:00:00","reportdate":"2018-06-30T00:00:00","publishname":"工程建设","securitytypecode":"058001001","trademarketcode":"069001002005","firstnoticedate":"2018-08-31T00:00:00","basiceps":"&#xEA5D;.&#xEA5D;&#xEA5D;&#xF2F8;&#xF137;","cutbasiceps":"-","totaloperatereve":"&#xE80C;&#xE712;&#xF275;&#xE268;&#xF137;&#xEA5D;&#xF2F8;&#xE73F;&#xE712;.&#xE712;&#xF137;","ystz":"-&#xE268;&#xEA5D;.&#xF137;&#xE73F;&#xF275;&#xF137;","yshz":"-&#xE80C;&#xECE9;.&#xF275;&#xF2F8;&#xE712;&#xE80C;","parentnetprofit":"&#xE268;&#xE73F;&#xE268;&#xF137;&#xEA5D;&#xF2F8;&#xEA5D;.&#xE891;","sjltz":"-&#xE891;&#xE712;.&#xF275;&#xE73F;&#xE73F;","sjlhz":"-&#xE80C;&#xECE9;.&#xF2F8;&#xF275;&#xECE9;&#xE73F;","roeweighted":"&#xEA5D;.&#xF275;&#xF137;","bps":"&#xE73F;.&#xE73F;&#xE80C;&#xEA5D;&#xE80C;&#xE73F;&#xE712;&#xE712;&#xE73F;","mgjyxjje":"&#xEA5D;.&#xEA5D;&#xF275;&#xF137;&#xEA5D;&#xE73F;&#xECE9;","xsmll":"&#xE80C;&#xE712;.&#xF137;&#xE712;&#xF137;&#xF137;","assigndscrpt":"不分配不转增","gxl":"-"},
```

在json数据的最后，有对应的字体编码字典，如下：<br>
```
"FontMapping":[{"code":"&#xE73F;","value":1},{"code":"&#xE80C;","value":2},{"code":"&#xF137;","value":3},{"code":"&#xE712;","value":4},{"code":"&#xECE9;","value":5},{"code":"&#xE268;","value":6},{"code":"&#xF275;","value":7},{"code":"&#xF2F8;","value":8},{"code":"&#xE891;","value":9},{"code":"&#xEA5D;","value":0}]}}
```

因此用正则提取出fontmapping，然后再替换成数字，最后保存到表格
