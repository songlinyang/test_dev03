function getCaseInfo() {
    var url = window.location.href;
    var caseId = url.split("/")[5];

    $.post('/manage/case/get_case_info/',{
        "cid":caseId
    },function (resp) {
        if (resp.code === 10200){
            // 对编辑页面进行赋值操作
            console.log(resp.data);
            //URL
            document.querySelector("#urlInput").value=resp.data.url;
            //请求方式
            if (resp.data.method === 1){
                document.querySelector("#get").setAttribute("checked","");
            }else if(resp.data.method === 2){
                document.querySelector("#post").setAttribute("checked","");
            }
            //Headers
            document.querySelector("#headerInput").value = resp.data.header;
            //参数类型
            if (resp.data.param_type === 1){
                document.querySelector("#form").setAttribute("checked","")
            }else if(resp.data.param_type === 2){
                document.headerInput("#json").setAttribute("checked","")
            }
            //请求体
            document.querySelector("#paramInput").value = resp.data.paramter_body;
            //返回结果
            document.querySelector("#result").value = resp.data.result;

            //断言方法
            if (resp.data.assert_type === 1){
                document.querySelector("#include").setAttribute("checked","")
            }else if(resp.data.assert_type === 2){
                document.querySelector("#equal").setAttribute("checked","")
            }

            //断言结果
             document.querySelector("#assert").value = resp.data.assert_text;
            //项目 & 模块
            SelectInit(resp.data.project,resp.data.module);
            //名称
            document.querySelector("#caseName").value=resp.data.name;

        }
    })
}