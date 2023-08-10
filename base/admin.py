"""
***  系统说明： ***
base 模块是一些基础数据的维护，这些数据被业务数据所使用：
1. BUMaster -- 定义公司实体，基本信息，使用系统的有效期，所购买的账户数目等
2. AccountMaster -- 定义系统的使用账号，隶属于哪个BU, 只能访问哪个BU的数据;账号必须提前定义为系统用户，其权限也是以来与系统层面的。
3. BUParameter -- 定义系统业务中使用的一些参数
"""
import xadmin
from base.models import *
from crm.models import *
from xadmin.layout import *
from django.forms.widgets import *
from django.contrib.admin.widgets import *
from django.utils.html import format_html
from django.http import HttpResponse
from django.core.validators import *
from django.core.validators import ValidationError
from django.contrib import messages
from django.shortcuts import render,redirect
from xadmin.views.base import get_account_bu  # psm add for get BU
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side, Field
# Register your models here.

class BUMasterAdmin(object):
    model = BUMaster
    model_icon = 'fa fa-jpy'
    actions_on_top = True
    actions_selection_counter = None

    # fields 定义此功能可以使用 model 中已经存在的哪些个字段，不能超出
    #fields = ['BU_code', 'BU_name', 'BU_type', 'BU_taxcode', 'BU_accounts', 'BU_datetime', 'BU_startdate', 'BU_expirydate','BU_status', 'BU_evidence',]
    fields = [f.name for f in BUMaster._meta.fields]
    # list_display 指定列表页中显示的字段， 除了model中定义的字段，也可以使用"自定义“字段
    list_display = ('BU_code', 'BU_name', 'BU_accounts', 'colored_BU_status', 'bu_accounts', 'bu_customers',)
    exclude = []
    list_display_links = ('BU_code',)
    list_export_fields = ('BU_code', 'BU_name', 'BU_status')
    search_fields = ('BU_code', 'BU_name')
    save_as = False
    show_bookmarks = False
    use_related_menu = False
    # 详细页面的页面布局的定义
    form_layout = (
        Main(
            Fieldset('基本信息',
                     'BU_code', 'BU_name', 'BU_type', 'BU_taxcode', 'BU_datetime',
                     ),
            Fieldset('协议信息',
                     'BU_startdate', 'BU_expirydate', 'BU_evidence', 'BU_accounts',
                     ),
        ),
        Side(
            Fieldset('附加信息',
                      'BU_status',
                     ),
            Fieldset('操 作 栏',
                     Row('actions_column1',),
                     ),
        ),
    )
# remove some auth  ---------
    def ResetAuth(self):
       # 重新定义此函数，限制普通用户的增删改权限
        if self.user.is_superuser:
            self.remove_permissions = ()
        else:
            self.remove_permissions = ('delete', 'add',)
        return self.remove_permissions
    #    remove_permissions = ('delete', 'add', 'change'，'view')
    # PSM set readonly fields
    def get_readonly_fields(self):
        readonly_fields = []
        if not self.org_obj:  #新建时
            readonly_fields = []
            return readonly_fields
        else:
            readonly_fields = ['BU_code', 'actions_column1', 'BU_datetime']  # 修改时
            return readonly_fields

    # PSM add for selected BU expiry validation
    def instance_forms(self):
        super().instance_forms()
        # 判断是否为新建操作
        if not self.org_obj: # 新建功能
            # PSM add for BU check
            self.form_obj.initial['BU_taxcode'] = '输入税号'
            self.form_obj.initial['BU_name'] = '输入实体名称'
        else:  # 修改功能
            pass
    # PSM add for save model customization
    def save_models(self):
        obj = self.new_obj
        if obj.BU_name == '输入实体名称':
            obj.BU_name = ''
        if obj.BU_taxcode == '输入税号':
            obj.BU_taxcode = ''
        super(BUMasterAdmin, self).save_models()

    # show BU evidence
    """def show_evidence(self,obj):
        if not obj.BU_evidence:
            return mark_safe('<img src="/%s" height="30" width="60" />' % (obj.BU_evidence))  #'(obj.BU_evidence.url)
        else:
            return mark_safe('<img src="/%s" height="30" width="60" />' % '-')
            pass
    show_evidence.short_description = ''"""
    # 状态字段 - 自定义屏幕列表字段
    def colored_BU_status(self,obj):
        if 'OK' in obj.BU_status:
            color_code = 'green'
        else:
            color_code = 'red'
        return format_html(
            '<span style="color: {};">{}</span>',
            color_code,
            obj.BU_status,
        )
    colored_BU_status.short_description = u'状态'
    # 编辑页面的操作按钮定义
    def actions_column1(self,obj):
        #
        parameter_str1 = 'BU_code={}'.format(str(obj.BU_code))
        btn_str1 = '<a class="btn btn-primary btn-sm" href="{}" rel="external nofollow" >' \
                  '<input name="通过审核"' \
                  'type="button" id="passButton" ' \
                  'title="审核按钮" value="初始化">' \
                  '</a>'
        return format_html(btn_str1, '/base/make_bu_enable/?{}'.format(parameter_str1))
    actions_column1.short_description = ''
    # 临时统计并显示 账号数目
    def bu_accounts(self,obj):
        #
        app_name = UserProfile._meta.app_label
        model_name = UserProfile._meta.model_name
        self.choice = '?' + "_q_=%s" % (obj.BU_code)

        admin_url = self.get_admin_url(
            '%s_%s_changelist' % (app_name, model_name))
        account_count = UserProfile.objects.filter(Data_bu_id=obj.BU_code).count()
        #
        if account_count > 0:
            return mark_safe("<a href='%s'>%s</a>" % (admin_url + self.choice, account_count))
        else:
            return format_html(
                '<span style="color: {};">{}</span>',
                'blue',
                account_count, )
    bu_accounts.short_description = '已用账户数'
    # 临时统计并显示 客户数目
    def bu_customers(self,obj):
        #
        app_name = CustomerMaster._meta.app_label
        model_name = CustomerMaster._meta.model_name
        self.choice = '?' + "_q_=%s" % (obj.BU_code)

        admin_url = self.get_admin_url(
                '%s_%s_changelist' % (app_name, model_name))
        customer_count = CustomerMaster.objects.filter(Data_bu_id=obj.BU_code).count()
        #
        if customer_count >0 :
            return mark_safe("<a href='%s'>%s</a>" % (admin_url + self.choice, customer_count))
        else:
            return format_html(
            '<span style="color: {};">{}</span>',
            'blue',
            customer_count, )
    bu_customers.short_description = '客户数目'

xadmin.site.register(BUMaster, BUMasterAdmin)
#
class AccountMasterForm(forms.models.BaseModelForm):
    # 页面字段内容的校验
    def clean(self):
        # PSM add for 'check expiry'
        bm = BUMaster.objects.filter(BU_code=self.Data_bu_id)
        if bm:
            bue = bm[0].BU_expirydate
        else:
            bue = timezone.now().strftime("%Y-%m-%d")
        if str(self.Account_expiry) > str(bue):
            raise ValidationError({'Account_expiry': '账号有效期超过BU有效期 %s，请更正！' % str(bue)})
        if str(self.Account_expiry) < timezone.now().strftime("%Y-%m-%d") and self.Account_status != 'XX':
            raise ValidationError({'Account_status': '账号已经过期，状态有误！'})
'''
class AccountMasterAdmin(object):
    actions_on_top = True
    actions_selection_counter = None
    #
    #form = AccountMasterForm
    #
    list_display = ('Account_name', 'Account_manager', 'account_customers', 'account_opportunities',)
    list_display_links = ('Account_name',)
    search_fields = ('Data_bu__BU_code', 'Data_bu__BU_name')
    list_filter = ['Data_bu']
    readonly_fields = ('account_customers', 'account_opportunities',)
    model_icon = 'fa fa-user'
    show_bookmarks = False
    use_related_menu = False
    save_as = False

    # remove some auth  ---------
    def ResetAuth(self):
        # 重新定义此函数，限制普通用户的增删改权限
        if self.user.is_superuser:
            self.remove_permissions = ()
        else:
            self.remove_permissions = ('delete', 'add',)
        return self.remove_permissions
    # 临时统计并显示 账号数目
    def account_customers(self, obj):
        #
        app_name = CustomerMaster._meta.app_label
        model_name = CustomerMaster._meta.model_name
        self.choice = '?' + "_q_Data_owner_id__id__exact=%s" % (obj.Account_name_id)

        admin_url = self.get_admin_url(
            '%s_%s_changelist' % (app_name, model_name))
        customer_count = 0
        customer_count = CustomerMaster.objects.filter(Data_bu_id=obj.Data_bu_id,
                                                       Data_owner=obj.Account_name_id).count()
        #
        if customer_count > 0:
            return mark_safe("<a href='%s'>%s</a>" % (admin_url + self.choice, customer_count))
        else:
            return format_html(
                '<span style="color: {};">{}</span>',
                'blue',
                customer_count, )
    account_customers.short_description = '客户数目'

    # 临时统计并显示 账号数目
    def account_opportunities(self, obj):
        #
        app_name = OpportunityMaster._meta.app_label
        model_name = OpportunityMaster._meta.model_name
        self.choice = '?' + "_p_Data_owner_id__Data_id__exact=%s" % (obj.Account_name_id)

        admin_url = self.get_admin_url(
                '%s_%s_changelist' % (app_name, model_name))
        opportunity_count = 0
        opportunity_count = OpportunityMaster.objects.filter(Data_bu=obj.Data_bu_id,
                                                             Data_owner=obj.Account_name_id).count()
    #
        if opportunity_count > 0:
            return mark_safe("<a href='%s'>%s</a>" % (admin_url + self.choice, opportunity_count))
        else:
            return format_html(
                '<span style="color: {};">{}</span>',
                'blue',
                opportunity_count, )
    account_opportunities.short_description = '商机数目'
# PSM add for selected BU expiry validation
    def instance_forms(self):
        super().instance_forms()
        # 判断是否为新建操作
        if not self.org_obj:
            # PSM add for BU check
            if not self.user.is_superuser:
                userid = self.request.user.id
                am = UserProfile.objects.filter(id=userid)

                if am:
                    account_bu = am[0].Data_bu_id
                else:
                    account_bu = '---'
            else:
                account_bu = '*ALL'
            self.form_obj.initial['Data_bu_id'] = account_bu
            self.form_obj.initial['Data_bu'] = account_bu
            self.form_obj.initial['Data_owner'] = self.request.user.id
            self.form_obj.initial['Data_creator'] = self.request.user.id
        else:
            pass
xadmin.site.register(UserProfile, AccountMasterAdmin)'''
# 参数维护
class BuParameterAdmin(object):
    actions_on_top = True
    actions_selection_counter = None

    list_display = ('Bu_code', 'Bu_paratype', 'Bu_parakey')
    list_display_links = ('Bu_code',)
    search_fields = ('Bu_code_id__BU_code',)
    list_filter = ['Bu_code_id']
    model_icon = 'fa fa-key'
    show_bookmarks = False
    save_as = False
    use_related_menu = False
    # PSM add for Data filter by BU
    def queryset(self):
        qs = super(BuParameterAdmin, self).queryset()
        if self.request.user.is_superuser:
            return qs
        else:
            account_bu = get_account_bu(self)
            return qs.filter(Bu_code=account_bu)

xadmin.site.register(BuParameter, BuParameterAdmin)
# 服务内容
class ItemMasterAdmin(object):
    actions_on_top = True
    actions_selection_counter = None

    list_display = ('Data_bu', 'Item_code', 'Item_desc')
    list_display_links = ('Item_code',)
    search_fields = ('Item_code', 'Item_desc')
    list_filter = ['Data_bu_id']
    model_icon = 'fa fa-key'
    show_bookmarks = False
    save_as = False
    use_related_menu = False
    # PSM add for Data filter by BU
    def queryset(self):
        qs = super(ItemMasterAdmin, self).queryset()
        if self.request.user.is_superuser:
            return qs
        else:
            account_bu = get_account_bu(self)
            return qs.filter(Data_bu=account_bu)

xadmin.site.register(ItemMaster, ItemMasterAdmin)
# 关注内容
class UserInterestAdmin(object):
    actions_on_top = True
    actions_selection_counter = None

    list_display = ('Data_id', 'User_myself', 'User_interest')
    list_display_links = ('Data_id',)
    search_fields = ('User_myself', 'User_interest')
    list_filter = ['User_myself']
    model_icon = 'fa fa-key'
    show_bookmarks = False
    save_as = False
    use_related_menu = False
    # PSM add for Data filter by BU
xadmin.site.register(UserInterest, UserInterestAdmin)
# 点赞内容
class UserThumbupAdmin(object):
    actions_on_top = True
    actions_selection_counter = None

    list_display = ('Data_id', 'User_myself', 'User_thumbup','Job_thumbup')
    list_display_links = ('Data_id',)
    search_fields = ('User_myself',)
    list_filter = ['User_myself']
    model_icon = 'fa fa-key'
    show_bookmarks = False
    save_as = False
    use_related_menu = False
    # PSM add for Data filter by BU
xadmin.site.register(UserThumbup, UserThumbupAdmin)