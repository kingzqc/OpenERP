from django import forms
from doc.models import ContentType, ResourceMaster, JobType
from workflow.models import FlowType
from base.models import BUMaster
from crm.models import ContactMaster, CustomerMaster
from base.psmsetting import *
from captcha.fields import CaptchaField
from django.contrib.auth import get_user_model
UserProfile = get_user_model()
'''
Dummy_id规则 后三位：
    workflow： （100-199）
    contact : (200-299)
    customer: (300-399)
    Opportunity: (400-499)
    Project: (500-599)
    Document:(600-699)
    Resource:(700-799)
    Service:(800-899)
    User:(900-999)
'''
class LoginForm(forms.Form):
    '''登录验证表单'''
    username = forms.CharField(required=True,widget=forms.TextInput(attrs = {'onchange' : "changeusername(this);"}),)
    password = forms.CharField(required=True,min_length=5,widget=forms.PasswordInput(),)
    captcha = CaptchaField(error_messages={'invalid':'验证码错误'})
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs) # Call to ModelForm constructor
        self.fields['username'].widget.attrs['style'] = 'width:30%; height:40px;'
        self.fields['username'].widget.attrs['placeholder'] = '输入用户名'
        self.fields['password'].widget.attrs['style'] = 'width:30%; height:40px;'
        self.fields['password'].widget.attrs['placeholder'] = '输入密码'
        self.fields['captcha'].widget.attrs['style'] = 'width:30%; height:40px;'
#
class RegisterForm(forms.Form):
    '''注册验证表单'''
    surname = forms.CharField(label="姓氏", required=True, min_length=2,widget=forms.TextInput(),
                              max_length=20, error_messages={"required": "该字段不能为空!","min_length": "姓氏太短,长度不能少于2。",
                                                             "max_length": "姓氏太长,长度不能多于20。"})
    name = forms.CharField(label="名字",required=True,min_length=2, max_length=20,
                           widget=forms.TextInput(),
                           error_messages={"required": "该字段不能为空!",
                                                             "min_length": "名字太短,长度不能少于2。",
                                                             "max_length": "名字太长,长度不能多于20。"})
    email = forms.EmailField(label="邮件地址",required=True, widget=forms.EmailInput())
    cellphone = forms.CharField(label="电话号码", required=True, min_length=8,widget=forms.TextInput(),
                                 error_messages={"required": "该字段不能为空!",
                                                             "min_length": "数字太短,长度不能少于8。"})
    usertype = forms.ChoiceField(label="账号类型", widget = forms.Select(), choices = web_USERTYPE, initial='Partner', required=True,)
    resourcetype = forms.ChoiceField(label="资源类型", widget = forms.Select(),
                                     choices = ContentType.objects.filter(Content_shape__range=['HUMAN','SPACE'], Data_status='OK').values_list("Data_id","ContentType_brief"),
                                     initial=' ', )
    databu = forms.ChoiceField(label="所属机构", widget=forms.Select(),
                                     choices=BUMaster.objects.values_list("BU_code","BU_name"),
                                     initial='', required=False,)
    username = forms.CharField(label="用户名",required=True,min_length=5, max_length=20,
                               widget=forms.TextInput(),
                               error_messages={"required": "该字段不能为空!",
                                                            "min_length": "用户名太短,长度不能少于5。",
                                                             "max_length": "用户名太长,长度不能多于20。"},)
    password = forms.CharField(label="密码",required=True, widget=forms.PasswordInput(),)
    password2 = forms.CharField(label="确认密码",required=True, widget=forms.PasswordInput(),)
    # 验证码
    captcha = CaptchaField(error_messages={'invalid':'验证码错误'})
    #数据验证
    def clean_surname(self):
        surname = self.cleaned_data.get('surname')
        if len(surname) < 2:
            raise forms.ValidationError(u"输入长度少于2字符")
        else:
            if len(surname) > 20:
                raise forms.ValidationError(u"输入长度多于20字符")
            else:
                return surname
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) < 2:
            raise forms.ValidationError(u"输入长度少于2字符")
        else:
            if len(name) > 20:
                raise forms.ValidationError(u"输入长度多于20字符")
            else:
                return name
    def clean_email(self):
        # email
        email = self.cleaned_data.get('email')
        if UserProfile.objects.filter(email=email):
            raise forms.ValidationError(u"邮箱已被注册")
        else:
            return email
    def clean_cellphone(self):
        # cellphone
        cellphone = self.cleaned_data.get('cellphone')
        if UserProfile.objects.filter(mobile=cellphone):
            raise forms.ValidationError(u"电话已被注册")
        else:
            return cellphone
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < 5:
            raise forms.ValidationError(u"输入长度不能少于5字符")
        else:
            if len(username) > 20:
                raise forms.ValidationError(u"输入长度不能多于20字符")
            else:
                if UserProfile.objects.filter(username=username):
                    raise forms.ValidationError(u"此注册账号已经存在")
                else:
                    return username
    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password != password2:
            raise forms.ValidationError(u"两次输入的密码不一致")
        else:
            return password2
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs) # Call to ModelForm constructor
        # 自动更新选择字段的值
        self.fields['databu'].widget.choices = BUMaster.objects.all().values_list("BU_code","BU_name")
        #
        self.fields['surname'].widget.attrs['style'] = 'width:40%; height:40px;'
        self.fields['surname'].widget.attrs['placeholder'] = '姓氏输入长度介于2-20'
        self.fields['name'].widget.attrs['style']  = 'width:40%; height:40px;'
        self.fields['name'].widget.attrs['placeholder'] = '名字输入长度介于2-20'
        self.fields['email'].widget.attrs['style'] = 'width:40%; height:40px;'
        self.fields['cellphone'].widget.attrs['style'] = 'width:40%; height:40px;'
        self.fields['cellphone'].widget.attrs['placeholder'] = '输入长度>8'
        self.fields['usertype'].widget.attrs['style'] = 'width:40%; height:40px;'
        self.fields['resourcetype'].widget.attrs['style'] = 'width:40%; height:40px;'
        self.fields['databu'].widget.attrs['style'] = 'width:40%; height:40px;'
        self.fields['username'].widget.attrs['style'] = 'width:40%; height:40px;'
        self.fields['username'].widget.attrs['placeholder'] = '用户名输入长度介于5-20'
        self.fields['password'].widget.attrs['style'] = 'width:40%; height:40px;'
        self.fields['password2'].widget.attrs['style'] = 'width:40%; height:40px;'
        self.fields['captcha'].widget.attrs['style'] = 'width:30%; height:40px;'
# model userprofile用户资料
class MyProfileForm(forms.Form):
    '''注册验证表单'''
    username = forms.CharField(label="用户账号",required=False,
                           widget=forms.HiddenInput())
    userid = forms.CharField(label="用户ID", required=False,
                           widget=forms.HiddenInput())
    first_name = forms.CharField(label="名字", required=True, min_length=1,widget=forms.TextInput(),
                              max_length=20, error_messages={"required": "该字段不能为空!","min_length": "昵称太短,长度不能少于2",
                                                             "max_length": "昵称太长,长度不能多于20"})
    last_name = forms.CharField(label="姓氏",required=True,min_length=1, max_length=20,
                           widget=forms.TextInput(),
                           error_messages={"required": "该字段不能为空!",
                                                             "min_length": "太短,长度不能少于2",
                                                             "max_length": "太长,长度不能多于20"})
    nick_name = forms.CharField(label="昵称",required=True, min_length=4, max_length=20,
                           widget=forms.TextInput(),
                           error_messages={"required": "该字段不能为空!",
                                                             "min_length": "太短,长度不能少于5",
                                                             "max_length": "太长,长度不能多于20"})
    birthday = forms.DateTimeField(label="出生日期", required=True, widget=forms.DateInput(format='%Y-%m-%d', attrs={'type':'date'}),)
    email = forms.EmailField(label="邮件地址", required=True, widget=forms.EmailInput())
    cellphone = forms.CharField(label="电话号码", required=True, min_length=8, max_length=11, widget=forms.TextInput(),
                                error_messages={"required": "该字段不能为空!",
                                                "min_length": "数字太短,长度不能少于8","max_length": "太长,长度不能多于11"})
    image = forms.FileField(label="图片", required=False,)
    password1 = forms.CharField(label="密码",required=False, widget=forms.PasswordInput(), initial='')
    password2 = forms.CharField(label="确认密码",required=False, widget=forms.PasswordInput(), initial='')
    # 数据校验
    def clean_first_name(self):
        # first_name
        first_name = self.cleaned_data.get('first_name')
        if len(first_name) < 1:
            raise forms.ValidationError(u"名字太短，不能少于1字符")
        else:
            if len(first_name) > 20:
                raise forms.ValidationError(u"名字太长，不能多于20字符")
            else:
                return first_name

    def clean_last_name(self):
        # last_name
        last_name = self.cleaned_data.get('last_name')
        if len(last_name) < 1:
            raise forms.ValidationError(u"姓氏太短，不能少于2字符")
        else:
            if len(last_name) > 20:
                raise forms.ValidationError(u"姓氏太长，不能多于20字符")
            else:
                return last_name
    def clean_nick_name(self):
        # nick_name
        nick_name = self.cleaned_data.get('nick_name')
        if len(nick_name) < 4:
            raise forms.ValidationError(u"昵称太短，不能少于4字符")
        else:
            if len(nick_name) > 20:
                raise forms.ValidationError(u"昵称太长，不能多于20字符")
            else:
                return nick_name
    def clean_email(self):
        # email
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if UserProfile.objects.filter(email=email).exclude(username=username):
            raise forms.ValidationError(u"邮箱已被注册")
        else:
            return email
    def clean_cellphone(self):
        # cellphone
        cellphone = self.cleaned_data.get('cellphone')
        username = self.cleaned_data.get('username')
        if len(cellphone) < 8:
            raise forms.ValidationError(u"输入长度少于8")
        else:
            if len(cellphone) > 11:
                raise forms.ValidationError(u"输入长度不能多于11")
            else:
                if UserProfile.objects.filter(mobile=cellphone).exclude(username=username):
                    raise forms.ValidationError(u"电话已被注册")
                else:
                    return cellphone
    def clean_password2(self):
        # password
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError(u"两次输入的密码不一致")
        else:
            return password2
    #
    def __init__(self, *args, **kwargs):
        super(MyProfileForm, self).__init__(*args, **kwargs) # Call to ModelForm constructor
        self.fields['username'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['first_name'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['first_name'].widget.attrs['placeholder'] = '输入长度介于1-20'
        self.fields['last_name'].widget.attrs['style']  = 'width:100%; height:40px;'
        self.fields['last_name'].widget.attrs['placeholder'] = '输入长度介于1-20'
        self.fields['nick_name'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['nick_name'].widget.attrs['placeholder'] = '输入长度介于4-20'
        self.fields['email'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['cellphone'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['cellphone'].widget.attrs['placeholder'] = '输入长度介于8-11'
        self.fields['birthday'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['image'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['password1'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['password2'].widget.attrs['style'] = 'width:100%; height:40px;'
#MODEL resourcemaster 资源资料
class ResourceForm(forms.Form):
    '''注册验证表单'''
    mode = forms.CharField(label="mode", required=False,
                           widget=forms.HiddenInput())
    nowuser = forms.CharField(label="user", required=False,
                           widget=forms.HiddenInput())
    nickname = forms.CharField(label="昵称", required=True, min_length=5,widget=forms.TextInput(),
                              max_length=20, error_messages={"required": "该字段不能为空!","min_length": "昵称太短,长度不能少于5。",
                                                             "max_length": "昵称太长,长度不能多于20。"})
    contactinfo = forms.CharField(label="联系信息",required=True,min_length=2, max_length=100,
                           widget=forms.TextInput(),
                           error_messages={"required": "该字段不能为空!",
                                                             "min_length": "太短,长度不能少于2。",
                                                             "max_length": "太长,长度不能多于100。"})
    resourcetype = forms.ChoiceField(label="类型", widget = forms.Select(),
                                     choices = ContentType.objects.filter(Content_shape__range=['HUMAN','SPACE'], Data_status='OK').values_list("Data_id","ContentType_brief"),
                                     initial=' ', )
    basecity = forms.CharField(label="所在城市",required=True,min_length=2, max_length=20,
                               widget=forms.TextInput(),
                               error_messages={"required": "该字段不能为空!",
                                                            "min_length": "城市名太短,长度不能少于5。",
                                                             "max_length": "城市名太长,长度不能多于20。"},)
    brief = forms.CharField(label="简介", required=True, widget=forms.Textarea)
    feature = forms.CharField(label="特点", required=True, widget=forms.Textarea)
    value = forms.CharField(label="价值", required=True, widget=forms.Textarea)
    summary = forms.CharField(label="摘要", required=True, widget=forms.Textarea)
    owner = forms.ChoiceField(label="Owner", required=False, widget = forms.Select(),
                              choices=UserProfile.objects.values_list("id","username"),
                              )
    resourcecode = forms.ChoiceField(label="RElResource", widget = forms.Select(),
                                     choices=UserProfile.objects.values_list("id","username"),
                                     initial=' ', )
    image = forms.FileField(label="图片", required=False,)
    onwebpage = forms.BooleanField(label='网页展示', widget=forms.CheckboxInput, initial=False, required=False)
    # 数据校验
    def clean_nickname(self):
        # nickname
        nickname = self.cleaned_data.get('nickname')
        if len(nickname)< 5:
            raise forms.ValidationError(u"昵称太短，不能少于5字符")
        else:
            if len(nickname)>20:
                raise forms.ValidationError(u"昵称太长，不能多于20字符")
            else:
                return nickname

    def clean_contactinfo(self):
        # contactinfo
        contactinfo = self.cleaned_data.get('contactinfo')
        if len(contactinfo) < 2:
            raise forms.ValidationError(u"昵称太短，不能少于2字符")
        else:
            if len(contactinfo) > 100:
                raise forms.ValidationError(u"昵称太长，不能多于100字符")
            else:
                return contactinfo

    def clean_resourcetype(self):
        # resourcetype
        resourcetype = self.cleaned_data.get('resourcetype')
        return resourcetype
    def clean_basecity(self):
        # basecity
        basecity = self.cleaned_data.get('basecity')
        if len(basecity) < 2:
            raise forms.ValidationError(u"太短，不能少于2字符")
        else:
            if len(basecity) > 20:
                raise forms.ValidationError(u"太长，不能多于20字符")
            else:
                return basecity
    #
    def __init__(self, *args, **kwargs):
        super(ResourceForm, self).__init__(*args, **kwargs) # Call to ModelForm constructor
        # 自动更新选择字段的值
        self.fields['resourcetype'].widget.choices = ContentType.objects.filter(Content_shape__range=['HUMAN','SPACE'], Data_status='OK').values_list("Data_id","ContentType_brief")
        up = UserProfile.objects.get(id=int(args[0]['nowuser']))
        self.fields['owner'].widget.choices = UserProfile.objects.filter(Data_bu_id=up.Data_bu_id).values_list("id","username")
        self.fields['resourcecode'].widget.choices = UserProfile.objects.filter(Data_bu_id=up.Data_bu_id).values_list("id", "username")
        #
        if args[0]['mode'] == 'edit':
            pass
        else:
            if args[0]['nowuser'] == args[0]['owner']:
                pass
            else:
                self.fields['nickname'].widget.attrs['readonly'] = 'readonly'
                self.fields['contactinfo'].widget.attrs['readonly'] = 'readonly'
                self.fields['resourcetype'].widget.attrs['readonly'] = 'readonly'
                self.fields['basecity'].widget.attrs['readonly'] = 'readonly'
                self.fields['brief'].widget.attrs['readonly'] = 'readonly'
                #
                self.fields['feature'].widget.attrs['readonly'] = 'readonly'
                self.fields['value'].widget.attrs['readonly'] = 'readonly'
                self.fields['owner'].widget.attrs['readonly'] = 'readonly'
                self.fields['summary'].widget.attrs['readonly'] = 'readonly'
                self.fields['resourcecode'].widget.attrs['readonly'] = 'readonly'

        #
        self.fields['nickname'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['nickname'].widget.attrs['placeholder'] = '输入长度介于5-20'
        self.fields['contactinfo'].widget.attrs['style']  = 'width:100%; height:40px;'
        self.fields['contactinfo'].widget.attrs['placeholder'] = '输入长度介于2-100'
        self.fields['resourcetype'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['basecity'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['basecity'].widget.attrs['placeholder'] = '输入长度介于2-20'
        self.fields['brief'].widget.attrs['style'] = 'width:100%; height:70px;'
        self.fields['feature'].widget.attrs['style'] = 'width:100%; height:100px;'
        self.fields['value'].widget.attrs['style'] = 'width:100%; height:100px;'
        self.fields['summary'].widget.attrs['style'] = 'width:100%; height:70px;'
        self.fields['owner'].widget.attrs['style'] = 'width:40%; height:40px;'
        self.fields['resourcecode'].widget.attrs['style'] = 'width:40%; height:40px;'
        self.fields['image'].widget.attrs['style'] = 'width:50%; height:30px;'
        self.fields['onwebpage'].widget.attrs['style'] = 'width:50%; height:20px;'
class ServiceForm(forms.Form):
    '''注册验证表单'''
    mode = forms.CharField(label="mode", required=False,
                           widget=forms.HiddenInput())
    nowuser = forms.CharField(label="user", required=False,
                           widget=forms.HiddenInput())
    job_code = forms.CharField(label="code", required=True, min_length=5,widget=forms.TextInput(),max_length=20,
                               error_messages={"required": "该字段不能为空!","min_length": "简称太短,长度不能少于5。",
                                                             "max_length": "简称太长,长度不能多于20。"})
    job_target = forms.CharField(label="target", required=True, widget=forms.Textarea)
    job_price = forms.DecimalField(label="联系信息", required=True, max_digits=10, decimal_places=2, widget=forms.NumberInput())
    job_brief = forms.CharField(label="brief",required=True,min_length=5, max_length=200,
                               widget=forms.TextInput(),
                               error_messages={"required": "该字段不能为空!",
                                                            "min_length": "摘要太短,长度不能少于5。",
                                                             "max_length": "摘要太长,长度不能多于200。"},)
    job_feature = forms.CharField(label="feature", required=True, widget=forms.Textarea)
    job_detail = forms.CharField(label="detail", required=True, widget=forms.Textarea)
    #
    job_type = forms.ChoiceField(label="type", required=False, widget=forms.Select(),
                                 choices=JobType.objects.values_list("Data_id","JobType_content")
                                 )
    job_contenttype = forms.ChoiceField(label="contenttype", required=False, widget=forms.Select(),
                                        choices=ContentType.objects.filter(ContentType_class='TOPIC', is_pagetop=0, Data_status='OK').values_list("Data_id","ContentType_brief"),
                                        initial=' ',)
    owner = forms.ChoiceField(label="Owner", required=False, widget = forms.Select(),
                              choices=UserProfile.objects.values_list("id","username"),
                              )
    job_resource = forms.ChoiceField(label="RElResource", widget = forms.Select(),
                                     choices=ResourceMaster.objects.values_list("Data_id","Resource_nickname"),
                                     initial=' ', )
    image = forms.FileField(label="图片", required=False,)
    on_webpage = forms.BooleanField(label='网页展示', initial=False, required=False)
    # 数据校验
    def clean_job_code(self):
        # code
        code = self.cleaned_data.get('job_code')
        if len(code)< 5:
            raise forms.ValidationError(u"简称太短，不能少于5字符")
        else:
            if len(code)>20:
                raise forms.ValidationError(u"简称太长，不能多于20字符")
            else:
                return code

    def clean_job_brief(self):
        # job brief
        jobbrief = self.cleaned_data.get('job_brief')
        if len(jobbrief) < 5:
            raise forms.ValidationError(u"摘要太短，不能少于5字符")
        else:
            if len(jobbrief) > 200:
                raise forms.ValidationError(u"摘要太长，不能多于200字符")
            else:
                return jobbrief

    def __init__(self, *args, **kwargs):
        super(ServiceForm, self).__init__(*args, **kwargs) # Call to ModelForm constructor
        # 获取下拉框的值
        up = UserProfile.objects.get(id=int(args[0]['nowuser']))
        self.fields['owner'].widget.choices = UserProfile.objects.filter(Data_bu_id=up.Data_bu_id).values_list("id",
                                                                                                               "username")
        self.fields['job_resource'].widget.choices = ResourceMaster.objects.filter(Data_owner_id=int(args[0]['nowuser'])).values_list(
            "Data_id", "Resource_nickname")
        self.fields['job_type'].widget.choices = JobType.objects.values_list("Data_id", "JobType_content")
        self.fields['job_contenttype'].widget.choices = ContentType.objects.filter(ContentType_class='TOPIC', is_pagetop=0, Data_status='OK').values_list("Data_id",
                                                                                                          "ContentType_brief")
        #
        if args[0]['mode'] == 'edit':
            pass
        else:
            if args[0]['nowuser'] == args[0]['owner']:
                pass
            else:
                self.fields['mode'].widget.attrs['readonly'] = 'readonly'
                self.fields['job_code'].widget.attrs['readonly'] = 'readonly'
                self.fields['job_price'].widget.attrs['readonly'] = 'readonly'
                self.fields['job_brief'].widget.attrs['readonly'] = 'readonly'
                self.fields['job_feature'].widget.attrs['readonly'] = 'readonly'
                self.fields['job_detail'].widget.attrs['readonly'] = 'readonly'
                self.fields['job_target'].widget.attrs['readonly'] = 'readonly'
                #
                self.fields['job_type'].widget.attrs['readonly'] = 'readonly'
                self.fields['job_contenttype'].widget.attrs['readonly'] = 'readonly'
                self.fields['owner'].widget.attrs['readonly'] = 'readonly'
                self.fields['job_resource'].widget.attrs['readonly'] = 'readonly'

        #
        self.fields['mode'].widget.attrs['style'] = 'width:50px; height:20px;'
        self.fields['job_code'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['job_code'].widget.attrs['placeholder'] = '输入长度介于5-20'
        self.fields['job_price'].widget.attrs['style']  = 'width:100%; height:40px;'
        self.fields['job_brief'].widget.attrs['style'] = 'width:100%; height:80px;'
        self.fields['job_brief'].widget.attrs['placeholder'] = '输入长度介于5-200'
        self.fields['job_feature'].widget.attrs['style'] = 'width:100%; height:170px;'
        self.fields['job_detail'].widget.attrs['style'] = 'width:100%; height:220px;'
        self.fields['job_target'].widget.attrs['style'] = 'width:100%; height:80px;'
        self.fields['job_type'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['job_contenttype'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['owner'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['job_resource'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['image'].widget.attrs['style'] = 'width:50%; height:30px;'
        self.fields['on_webpage'].widget.attrs['style'] = 'width:50%; height:20px;'
#MODEL requestmaster workflow资料
class RequestForm(forms.Form):
    '''注册验证表单'''
    Data_id = forms.CharField(label="ID", required=False,
                               widget=forms.TextInput(attrs={'class': 'disabled', 'readonly': 'readonly'}))
    Dummy_id = forms.CharField(label="DummyID", required=False,
                             widget=forms.TextInput(attrs={'class': 'disabled', 'readonly': 'readonly'}))
    Request_desc = forms.CharField(label="Desc", required=False,
                               widget=forms.TextInput(attrs={'class': 'disabled', 'readonly': 'readonly'}))
    Request_date = forms.DateTimeField(label="日期", required=False,
                                   widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date','class': 'disabled', 'readonly': 'readonly'}), )
    Request_initdate = forms.DateTimeField(label="init日期", required=False,
                                       widget=forms.DateInput(format='%Y-%m-%d',
                                                              attrs={'type': 'date', 'class': 'disabled',
                                                                     'readonly': 'readonly'}), )
    Request_inittime = forms.CharField(label="inittime", required=False,
                                           widget=forms.TimeInput(
                                                                  attrs={'class': 'disabled',
                                                                         'readonly': 'readonly'}), )
    Request_enddate = forms.DateTimeField(label="end日期", required=False,
                                       widget=forms.DateInput(format='%Y-%m-%d',
                                                              attrs={'type': 'date', 'class': 'disabled',
                                                                     'readonly': 'readonly'}), )
    Request_endtime = forms.CharField(label="endtime", required=False,
                                           widget=forms.TextInput(attrs={'class': 'disabled',
                                                                         'readonly': 'readonly'}), )
    Request_comments = forms.CharField(label="comments", required=False,
                               widget=forms.Textarea())
    Request_status = forms.CharField(label="status", required=False,
                                       widget=forms.TextInput(attrs={'class': 'disabled', 'readonly': 'readonly'}))
    #
    Data_owner = forms.CharField(label="Owner", required=False,
                              widget=forms.TextInput(attrs={'class': 'disabled', 'readonly': 'readonly'}))
    Data_creator = forms.CharField(label="Creator", required=False,
                                 widget=forms.TextInput(attrs={'class': 'disabled', 'readonly': 'readonly'}))
    Data_approver = forms.CharField(label="Approver", required=False,
                                 widget=forms.TextInput(attrs={'class': 'disabled', 'readonly': 'readonly'}))
    Data_processor = forms.CharField(label="Processor", required=False,
                                 widget=forms.TextInput(attrs={'class': 'disabled', 'readonly': 'readonly'}))
    Data_realizer = forms.CharField(label="Realizer", required=False,
                                 widget=forms.TextInput(attrs={'class': 'disabled', 'readonly': 'readonly'}))
    #
    Request_mainresource = forms.CharField(label="Mainresource", required=False,
                                 widget=forms.TextInput(attrs={'class': 'disabled', 'readonly': 'readonly'}))
    Request_contact = forms.CharField(label="Contact", required=False,
                                           widget=forms.TextInput(attrs={'class': 'disabled', 'readonly': 'readonly'}))
    Request_customer = forms.CharField(label="Customer", required=False,
                                           widget=forms.TextInput(attrs={'class': 'disabled', 'readonly': 'readonly'}))
    Request_opportunity = forms.CharField(label="Opportunity", required=False,
                                           widget=forms.TextInput(attrs={'class': 'disabled', 'readonly': 'readonly'}))
    #

    # 数据校验
    def __init__(self, *args, **kwargs):
        super(RequestForm, self).__init__(*args, **kwargs) # Call to ModelForm constructor
        self.fields['Data_id'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['Dummy_id'].widget.attrs['style']  = 'width:100%; height:40px;'
        self.fields['Request_desc'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['Request_date'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['Request_initdate'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['Request_inittime'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['Request_enddate'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['Request_endtime'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['Request_comments'].widget.attrs['style'] = 'width:100%; height:90px;'
        self.fields['Request_status'].widget.attrs['style'] = 'width:50%; height:40px;'
        #
        self.fields['Data_owner'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['Data_creator'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['Data_approver'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['Data_processor'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['Data_realizer'].widget.attrs['style'] = 'width:100%; height:40px;'
        #
        self.fields['Request_mainresource'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['Request_contact'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['Request_customer'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['Request_opportunity'].widget.attrs['style'] = 'width:100%; height:40px;'
#
#MODEL contactmaster 联系人资料
class ContactForm(forms.Form):
    '''注册验证表单'''
    mode = forms.CharField(label="mode", required=False,
                               widget=forms.HiddenInput())
    nowuser = forms.CharField(label="user", required=False,
                           widget=forms.HiddenInput())
    Data_id = forms.CharField(label="ID", required=False,
                               widget=forms.TextInput(attrs={'class': 'disabled', 'readonly': 'readonly'}))
    Contact_code = forms.CharField(label="Code", required=False,
                             widget=forms.TextInput())
    Contact_name = forms.CharField(label="Name", required=False,
                               widget=forms.TextInput())
    Contact_source = forms.ChoiceField(label="Source", widget=forms.Select(),
                                     choices=crm_SOURCE, initial='SELF',
                                     required=True, )
    Contact_method = forms.ChoiceField(label="Method", widget=forms.Select(),
                                     choices=crm_METHOD, initial='CALL',
                                     required=True, )
    Contact_content = forms.CharField(label="Content", required=False,
                               widget=forms.TextInput())
    Contact_card = forms.FileField(label="Card", required=False, )
    Contact_scanflag = forms.CharField(label="Flag", required=False,
                                   widget=forms.TextInput())
    Data_owner = forms.ChoiceField(label="Owner", widget=forms.Select(),
                                     choices=UserProfile.objects.values_list("id","username"),
                                     initial='', required=False,)
    Data_creator = forms.ChoiceField(label="Creator", widget=forms.Select(),
                                   choices=UserProfile.objects.values_list("id", "username"),
                                   initial='', required=False, )
    Contact_status = forms.CharField(label="Status", required=False,
                               widget=forms.TextInput())
    # 数据校验
    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs) # Call to ModelForm constructor
        # 获取下拉框的值
        up = UserProfile.objects.get(id=int(args[0]['nowuser']))
        self.fields['Data_owner'].widget.choices = UserProfile.objects.filter(Data_bu_id=up.Data_bu_id).values_list("id",
                                                                                                               "username")
        self.fields['Data_creator'].widget.choices = UserProfile.objects.filter(Data_bu_id=up.Data_bu_id).values_list(
            "id", "username")
        #
        if args[0]['mode'] == 'edit':
            pass
        else:
            if args[0]['nowuser'] == args[0]['Data_owner']:
                pass
            else:
                self.fields['Contact_code'].widget.attrs['readonly'] = 'readonly'
                self.fields['Contact_name'].widget.attrs['readonly'] = 'readonly'
                self.fields['Contact_source'].widget.attrs['readonly'] = 'readonly'
                self.fields['Contact_method'].widget.attrs['readonly'] = 'readonly'
                self.fields['Contact_content'].widget.attrs['readonly'] = 'readonly'
                #
                self.fields['Contact_card'].widget.attrs['readonly'] = 'readonly'
                self.fields['Contact_scanflag'].widget.attrs['readonly'] = 'readonly'
                self.fields['Data_owner'].widget.attrs['readonly'] = 'readonly'
                self.fields['Data_creator'].widget.attrs['readonly'] = 'readonly'
                self.fields['Contact_status'].widget.attrs['readonly'] = 'readonly'
        #
        self.fields['Data_id'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['Contact_code'].widget.attrs['style']  = 'width:100%; height:40px;'
        self.fields['Contact_name'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['Contact_source'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['Contact_method'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['Contact_content'].widget.attrs['style'] = 'width:100%; height:90px;'
        #
        self.fields['Contact_card'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['Contact_scanflag'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['Data_owner'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['Data_creator'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['Contact_status'].widget.attrs['style'] = 'width:100%; height:40px;'
#
#MODEL customermaster 客户资料
class CustomerForm(forms.Form):
    '''注册验证表单'''
    mode = forms.CharField(label="mode", required=False,
                           widget=forms.HiddenInput())
    nowuser = forms.CharField(label="user", required=False,
                           widget=forms.HiddenInput())
    Data_id = forms.CharField(label="ID", required=False,
                               widget=forms.TextInput())
    Customer_code = forms.CharField(label="Code", required=False,
                             widget=forms.TextInput())
    Customer_name = forms.CharField(label="Name", required=False,
                               widget=forms.TextInput())
    Customer_address = forms.CharField(label="Address", required=False,
                               widget=forms.TextInput())
    Customer_source = forms.ChoiceField(label="Source", widget=forms.Select(),
                                     choices=crm_SOURCE, initial='',
                                     required=False, )
    Customer_contact1 = forms.ChoiceField(label="Contact1", widget=forms.Select(),
                                     choices=ContactMaster.objects.values_list("Data_id", "Contact_code"),
                                          initial='',
                                     required=False, )
    Customer_contact2 = forms.ChoiceField(label="Contact2", widget=forms.Select(),
                                     choices=ContactMaster.objects.values_list("Data_id", "Contact_code"),
                                    initial='',
                                     required=False, )
    Data_owner = forms.ChoiceField(label="Owner", widget=forms.Select(),
                                     choices=UserProfile.objects.values_list("id","username"),
                                     initial='', required=False,)
    Data_creator = forms.ChoiceField(label="Creator", widget=forms.Select(),
                                   choices=UserProfile.objects.values_list("id", "username"),
                                   initial='', required=False, )
    Customer_status = forms.CharField(label="Status", required=False,
                               widget=forms.TextInput(attrs={'class': 'disabled', 'readonly': 'readonly'}))
    # 数据校验
    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs) # Call to ModelForm constructor
        # 获取下拉框的值
        up = UserProfile.objects.get(id=int(args[0]['nowuser']))
        self.fields['Data_owner'].widget.choices = UserProfile.objects.filter(Data_bu_id=up.Data_bu_id).values_list(
            "id","username")
        self.fields['Data_creator'].widget.choices = UserProfile.objects.filter(Data_bu_id=up.Data_bu_id).values_list(
            "id", "username")
        self.fields['Customer_contact1'].widget.choices = ContactMaster.objects.filter(Data_bu_id=up.Data_bu_id).values_list("Data_id", "Contact_code")
        self.fields['Customer_contact2'].widget.choices = ContactMaster.objects.filter(
            Data_bu_id=up.Data_bu_id).values_list("Data_id", "Contact_code")
        #
        if args[0]['mode'] == 'edit':
            pass
        else:
            if args[0]['nowuser'] == args[0]['Data_owner']:
                pass
            else:
                self.fields['Customer_code'].widget.attrs['readonly'] = 'readonly'
                self.fields['Customer_name'].widget.attrs['readonly'] = 'readonly'
                self.fields['Customer_source'].widget.attrs['readonly'] = 'readonly'
                self.fields['Customer_address'].widget.attrs['readonly'] = 'readonly'
                self.fields['Customer_contact1'].widget.attrs['readonly'] = 'readonly'
                self.fields['Customer_contact2'].widget.attrs['readonly'] = 'readonly'
                #
                self.fields['Data_owner'].widget.attrs['readonly'] = 'readonly'
                self.fields['Data_creator'].widget.attrs['readonly'] = 'readonly'
                self.fields['Customer_status'].widget.attrs['readonly'] = 'readonly'

        self.fields['Data_id'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['Customer_code'].widget.attrs['style']  = 'width:100%; height:40px;'
        self.fields['Customer_code'].widget.attrs['placeholder'] = 'customer placeholder'
        self.fields['Customer_name'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['Customer_source'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['Customer_address'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['Customer_contact1'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['Customer_contact2'].widget.attrs['style'] = 'width:100%; height:40px;'
        #
        self.fields['Data_owner'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['Data_creator'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['Customer_status'].widget.attrs['style'] = 'width:100%; height:40px;'
#
#MODEL opportunitymaster 客户资料
class OpportunityForm(forms.Form):
    '''注册验证表单'''
    mode = forms.CharField(label="mode", required=False,
                           widget=forms.HiddenInput())
    nowuser = forms.CharField(label="user", required=False,
                           widget=forms.HiddenInput())
    Data_id = forms.CharField(label="ID", required=False,
                               widget=forms.TextInput())
    Opportunity_code = forms.CharField(label="Code", required=False,
                             widget=forms.TextInput())
    Opportunity_name = forms.CharField(label="Name", required=False,
                               widget=forms.TextInput())
    Opportunity_source = forms.ChoiceField(label="Source", widget=forms.Select(),
                                     choices=crm_SOURCE, initial='',
                                     required=False, )
    Opportunity_flowcycle = forms.ChoiceField(label="flowcycle", widget=forms.Select(),
                                     choices=FlowType.objects.values_list("Data_id", "Flowtype_desc"),
                                              initial='',
                                     required=False, )
    Opportunity_initialamount = forms.CharField(label="initamt", required=False,
                                       widget=forms.TextInput())
    Opportunity_currentamount = forms.CharField(label="nowamt", required=False,
                                       widget=forms.TextInput())
    Opportunity_finalamount = forms.CharField(label="finalamt", required=False,
                                       widget=forms.TextInput())
    Opportunity_nowstage = forms.CharField(label="nowstage", required=False,
                                       widget=forms.TextInput())
    Opportunity_nextstage = forms.CharField(label="nextstage", required=False,
                                       widget=forms.TextInput())
    Opportunity_date = forms.CharField(label="date", required=False,
                                       widget=forms.TextInput())
    Opportunity_comments = forms.CharField(label="comments", required=False,
                                       widget=forms.TextInput())

    Opportunity_contact = forms.ChoiceField(label="Contact", widget=forms.Select(),
                                     choices=ContactMaster.objects.values_list("Data_id", "Contact_code"),
                                            initial='',
                                     required=False, )
    Opportunity_customer = forms.ChoiceField(label="Contact2", widget=forms.Select(),
                                     choices=CustomerMaster.objects.values_list("Data_id", "Customer_code"),
                                             initial='',
                                     required=False, )
    Data_owner = forms.ChoiceField(label="Owner", widget=forms.Select(),
                                     choices=UserProfile.objects.values_list("id","username"),
                                     initial=['---','---'], required=False,)
    Data_creator = forms.ChoiceField(label="Creator", widget=forms.Select(),
                                   choices=UserProfile.objects.values_list("id", "username"),
                                   initial=['---','---'], required=False, )
    Data_approver = forms.ChoiceField(label="Approver", widget=forms.Select(),
                                   choices=UserProfile.objects.values_list("id", "username"),
                                   initial=['---','---'], required=False, )
    Opportunity_status = forms.CharField(label="Status", required=False,
                               widget=forms.TextInput(attrs={'class': 'disabled', 'readonly': 'readonly'}))
    # 数据校验
    def __init__(self, *args, **kwargs):
        super(OpportunityForm, self).__init__(*args, **kwargs) # Call to ModelForm constructor
        # 获取下拉框的值
        up = UserProfile.objects.get(id=int(args[0]['nowuser']))
        self.fields['Data_owner'].widget.choices = UserProfile.objects.filter(Data_bu_id=up.Data_bu_id).values_list(
            "id", "username")
        self.fields['Data_creator'].widget.choices = UserProfile.objects.filter(Data_bu_id=up.Data_bu_id).values_list(
            "id", "username")
        self.fields['Data_approver'].widget.choices = UserProfile.objects.filter(Data_bu_id=up.Data_bu_id).values_list(
            "id", "username")
        self.fields['Opportunity_contact'].widget.choices = ContactMaster.objects.filter(
            Data_bu_id=up.Data_bu_id).values_list("Data_id", "Contact_code")
        self.fields['Opportunity_customer'].widget.choices = CustomerMaster.objects.filter(
            Data_bu_id=up.Data_bu_id).values_list("Data_id", "Customer_code")
        self.fields['Opportunity_flowcycle'].widget.choices = FlowType.objects.filter(
            Data_bu_id=up.Data_bu_id).values_list("Data_id", "Flowtype_desc")
        #
        if args[0]['mode'] == 'edit':
            self.fields['Opportunity_nowstage'].widget.attrs['readonly'] = 'readonly'
            self.fields['Opportunity_nextstage'].widget.attrs['readonly'] = 'readonly'
            self.fields['Opportunity_currentamount'].widget.attrs['readonly'] = 'readonly'
            self.fields['Opportunity_finalamount'].widget.attrs['readonly'] = 'readonly'
            #pass
        else:
            self.fields['Opportunity_code'].widget.attrs['readonly'] = 'readonly'
            self.fields['Opportunity_name'].widget.attrs['readonly'] = 'readonly'
            self.fields['Opportunity_source'].widget.attrs['readonly'] = 'readonly'
            self.fields['Opportunity_flowcycle'].widget.attrs['readonly'] = 'readonly'
            self.fields['Opportunity_initialamount'].widget.attrs['readonly'] = 'readonly'
            self.fields['Opportunity_currentamount'].widget.attrs['readonly'] = 'readonly'
            self.fields['Opportunity_finalamount'].widget.attrs['readonly'] = 'readonly'
            self.fields['Opportunity_nowstage'].widget.attrs['readonly'] = 'readonly'
            self.fields['Opportunity_nextstage'].widget.attrs['readonly'] = 'readonly'
            self.fields['Opportunity_date'].widget.attrs['readonly'] = 'readonly'
            self.fields['Opportunity_contact'].widget.attrs['readonly'] = 'readonly'
            self.fields['Opportunity_customer'].widget.attrs['readonly'] = 'readonly'
            #
            self.fields['Data_owner'].widget.attrs['readonly'] = 'readonly'
            self.fields['Data_creator'].widget.attrs['readonly'] = 'readonly'
            self.fields['Data_approver'].widget.attrs['readonly'] = 'readonly'
            self.fields['Opportunity_status'].widget.attrs['readonly'] = 'readonly'

        self.fields['Data_id'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['Opportunity_code'].widget.attrs['style']  = 'width:100%; height:40px;'
        self.fields['Opportunity_name'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['Opportunity_source'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['Opportunity_flowcycle'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['Opportunity_initialamount'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['Opportunity_currentamount'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['Opportunity_finalamount'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['Opportunity_nowstage'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['Opportunity_nextstage'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['Opportunity_date'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['Opportunity_comments'].widget.attrs['style'] = 'width:100%; height:70px;'
        self.fields['Opportunity_contact'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['Opportunity_customer'].widget.attrs['style'] = 'width:100%; height:40px;'
        #
        self.fields['Data_owner'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['Data_creator'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['Data_approver'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['Opportunity_status'].widget.attrs['style'] = 'width:100%; height:40px;'
#
class ForgotPasswordForm(forms.Form):
    '''忘记密码'''
    username = forms.CharField(label="用户名",required=True,min_length=5, max_length=20,
                               widget=forms.TextInput(),
                               error_messages={"required": "该字段不能为空!",
                                                            "min_length": "用户名太短,长度不能少于5。",
                                                             "max_length": "用户名太长,长度不能多于20。"},)
    email = forms.EmailField(required=True)
    cellphone = forms.CharField(label="电话号码", required=True, min_length=8, widget=forms.TextInput(),
                                error_messages={"required": "该字段不能为空!",
                                                "min_length": "数字太短,长度不能少于8。"})
    password = forms.CharField(label="新密码",required=True, widget=forms.PasswordInput(),)
    password2 = forms.CharField(label="确认密码",required=True, widget=forms.PasswordInput(),)
    captcha = CaptchaField(error_messages={'invalid': '验证码错误'})

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if UserProfile.objects.filter(username=username):
            return username
        else:
            raise forms.ValidationError(u"此账号不存在")
    def clean_email(self):
        # email
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if UserProfile.objects.filter(email=email,username=username):
            return email
        else:
            raise forms.ValidationError(u"邮箱与用户不匹配")
    def clean_cellphone(self):
        # cellphone
        username = self.cleaned_data.get('username')
        cellphone = self.cleaned_data.get('cellphone')
        if UserProfile.objects.filter(mobile=cellphone,username=username):
            return cellphone
        else:
            raise forms.ValidationError(u"手机号码与用户不匹配")
    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password != password2:
            raise forms.ValidationError(u"两次输入的密码不一致")
        else:
            return password2
    #def __init__(self, *args, **kwargs):
     #   super(ForgotPasswordForm, self).__init__(*args, **kwargs) # Call to ModelForm constructor
      #  self.fields['email'].widget.attrs['style'] = 'width:30%; height:40px;'
      #  self.fields['cellphone'].widget.attrs['style'] = 'width:30%; height:40px;'
      #  self.fields['username'].widget.attrs['style'] = 'width:30%; height:40px;'
class ResetPasswordForm(forms.Form):
    '''注册验证表单'''
    email = forms.EmailField(required=True)
    password = forms.CharField(label="密码",required=True, widget=forms.PasswordInput(),)
    password2 = forms.CharField(label="确认密码",required=True, widget=forms.PasswordInput(),)
    # 验证码
    captcha = CaptchaField(error_messages={'invalid':'验证码错误'})

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password != password2:
            raise forms.ValidationError(u"两次输入的密码不一致")
        else:
            return password2

class ModifyPwdForm(forms.Form):
    '''重置密码'''
    password1 = forms.CharField(required=True, min_length=5)
    password2 = forms.CharField(required=True, min_length=5)