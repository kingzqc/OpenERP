$('#id_Resource_code').change(function () {
        var module = $('#id_Resource_code').find('option:selected').val(); //获取父级选中值
        $('#id_Resource_basecompetence')[0].selectize.clearOptions();// 清空子级
        $.ajax({
            type: 'get',
            url: '/select/resource_basecompetence/?module=' + module,
            data: '',
            async: true,
            beforeSend: function (xhr, settings) {
                xhr.setRequestHeader('X-CSRFToken', '{{ csrf_token }}')
            },
            success: function (data) {
                data = JSON.parse(data.basecompetence)//将JSON转换
                for (var i = 0; i < data.length; i++) {

                    var test = {text: '['+ (i+1) +']' + data[i].fields.BaseCompetence_timestart +'--'+ data[i].fields.BaseCompetence_timeend, value: data[i].pk,  $order: i + 1}; //遍历数据,拼凑出selectize需要的格式
                    console.log(test)
                    $('#id_Resource_basecompetence')[0].selectize.addOption(test); //添加数据
                }
            },
            error: function (xhr, textStatus) {
                console.log('error')
            }
        })
    })