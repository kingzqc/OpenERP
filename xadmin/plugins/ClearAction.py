import xadmin
from xadmin.plugins.actions import BaseActionView

class ClearAction(BaseActionView):
    action_name = "ClearAction"  # 动作名
    description = "Clear Action"  # 要显示的名字
    model_perm = "change"  # 该动作所需权限
    model_icon = 'fa fa-book'

    def do_action(self, queryset):  # 重载do_action()方法
        try:
            for i in queryset:
                ...
            self.message_user(message="Done", level="success")  # level的值必须小写
        except Exception as e:
            self.message_user(e, "error")
