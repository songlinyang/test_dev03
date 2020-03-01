function SelectInit(projectSelectIndex,moduleSelectIndex) {
    //获取项目Select元素、模块Select元素
    var cmbProject = document.querySelector("#selectProject");
    var cmbModule = document.querySelector("#selectModule");
    var dataList = [];
    console.log("初始化Select下拉框");

    //创建下拉选型值
    function addOption(cmb,obj){
        var option = document.createElement("option");
        cmb.options.add(option);
        option.innerHTML = obj.name;
        option.value = obj.id;
    }
    //创建默认选择下拉选项功能
    function setDefualtOption(obj,indexSelect){
        //console.log("选择了对象:",obj);
        //console.log("选择了索引：",indexSelect);
        for (var i=0;i<obj.options.length;i++){
            //console.log("判断索引类型",typeof i);
            if (obj.options[i].value == indexSelect){
                //console.log("对比1:",obj.options[i].value);
                //console.log("对比2:",indexSelect);
                obj.selectedIndex = i;
                return;
            }
        }
    }

    function getSelectData(){
        //调用获取Select数据列表
        $.get("/manage/case/get_select_data/",{},function (resp) {
            if(resp.code === 10200){
                dataList = resp.data;
                console.log("想要的数据列表",dataList);
                for(var data_list_index = 0; data_list_index<dataList.length;data_list_index++){
                    addOption(cmbProject,dataList[data_list_index]);

                }
                console.log("调用了1");
                setDefualtOption(cmbProject,projectSelectIndex);
                changeProjectToModule();
                cmbProject.onchange=changeProjectToModule;
            }else{
                console.log("fail");
            }
            console.log("调用了2");
            setDefualtOption(cmbProject,projectSelectIndex);
        });

    }
    function changeProjectToModule(){
        cmbModule.options.length = 0;
        var pid = cmbProject.options[cmbProject.selectedIndex].value;
        for (var i =0;i<dataList.length;i++){
            if (dataList[i].id == pid){
                var modules = dataList[pid-1].moduleList;
                for (var j=0;j<modules.length;j++){
                    addOption(cmbModule,modules[j]);
                }
            }
        }
    console.log("调用了3");
    setDefualtOption(cmbModule,moduleSelectIndex);
    }
    getSelectData();

}