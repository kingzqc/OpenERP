from django.views.generic.base import View
from .models import BaseCompetence, ContentType, ResourceMaster
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
# Create your views here.
#导入serializers
from django.core import serializers
# 二级联动View函数
#@login_required
class SelectBaseCompetenceView(View):
    def get(self, request):
        # 通过get得到父级选择项
        resource_id = request.GET.get('module', '')
        content_type = ResourceMaster.objects.filter(Data_id__exact=int(resource_id))
        if content_type:
            # 筛选出符合父级要求的所有子级，因为输出的是一个集合，需要将数据序列化 serializers.serialize（）
            basecompetences = serializers.serialize("json", BaseCompetence.objects.filter(BaseCompetence_type_id=int(content_type[0].Resource_type_id),is_active=True, Data_status="OK"))
            # 判断是否存在，输出
            #print(basecompetences)
            if basecompetences:
                return JsonResponse({'basecompetence': basecompetences})