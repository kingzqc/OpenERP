"""
notes: app_parameter name
"""
web_CONTENTCLASS = (
    ('TOPIC', '主题'),
    ('RESOURCE', '资源'),
    ('SERVICE', '服务'),
    ('WORKFLOW', '流程'),
    ('RESULT', '成果'),
    ('ABOUT', '关于我们'),
)
web_RESOURCECLASS = (
    ('HUMAN', '人力资源'),
    ('SPACE', '空间资源'),
    ('ED', '电子数据')
)
web_USERTYPE = ([('Trainer','咨询授课'),
                     ('Partner','业务开拓'),
                     ])
#
base_BUTYPE = (
    ('P', '个人'),
    ('E', '企业'),
    ('*', '待定')
)
#
base_BUSTATUS = (
    ('00', '待办'),
    ('OK', '正常'),
    ('XX', '停止'),
)
#
base_SECURITYLEVEL = (
    ('10', '10'),
    ('30', '30'),
    ('50', '50'),
    ('100', '100'),
)
#
base_PARATYPE = (
    ('industry', '所属行业'),
    ('scale', '规模'),
    ('service', '服务类型'),
)
#======== CRM  CRM  CRM  start ===================
crm_STATUS = (
        ('OPEN', '待办'),
        ('APPROVED', '已批准'),
        ('STOPPED', '停止'),
)
#
crm_SOURCE = (
    ('CAMP', '营销活动'),
    ('AGENT', '代理推荐'),
    ('SELF', '自己发掘')
)
#
crm_METHOD = (
    ('EMAIL', '电子邮件'),
    ('CALL', '电话'),
    ('WECHAT', '微信')
)
#
crm_SCANFLAG = (
    ('99', '手工输入'),
    ('00', '待识别'),
    ('01', '已识别')
)
crm_RESOURCETYPE = (
    ('CONTACT', '联系人'),
    ('CUSTOMER', '客户'),
    ('PARTNER', '合作方')
)
#
crm_CUSTTYPE = (
    ('SUSPECT', 'Suspect潜在'),
    ('LEADS', 'Leads线索'),
    ('PROSPECT', 'Prospect意向'),
    ('CUSTOMER', 'Customer客户')
)
#
crm_ACTTYPE = (
    ('CALL', '打电话'),  # TEL= telphone
    ('VISIT', '现场拜访'),  # VST = visit
    ('PAPER', '文字工作'),  # PAP = paper work
    ('OTHERS', '其他'),  # OTH = other
    ('APPOINT', '日程')  # APT = appoint
)
#  =====  workflow workflow  workflow  start =====
wf_MAINROLE = (
    ('self', '自己'),
    ('mgr', '上级'),
    ('accmgr', '客户经理'),
    ('oppmgr', '商机经理'),
    ('prjmgr', '项目经理'),
    ('admin', '系统管理员'),
)
wf_CYCLEUSAGE = (
    ('USR', '普通日程'), # 日历显示 旗子
    ('CRM', '商机管理'), # 日历显示 礼物
    ('PRJ', '项目管理'), # 日历显示 飞机
)
wf_MAINTYPE = (
    ('CAL', '日历类型'),
    ('OPD', 'CRM类型'),
    ('PRD', '交付类型'),
)
#
wf_CYCLETYPE = (
    ('STD', '标准'),
    ('SHORT', '快捷'),
)
wf_REQSTATUS = (
    ('00', '待办'),
    ('10', '已批准'),
    ('20', '已实现'),
    ('30', '已处理'),
)
wf_ACTIONCODE = (
    ('OO', '待办'),
    ('RO', '重开'),
    ('AP', '批准'),
    ('RL', '实现'),
    ('PR', '处理'),
    ('RT', '退回'),
    ('XX', '停用'),
)
# =====  project project project start ====
prj_STATUS = (
        ('OO', '待办'),
        ('OK', '启用'),
        ('XX', '停止'),
)
prj_ROLE = (
    ('PM', '项目经理'),
    ('SM', '高级成员'),
    ('NM', '普通成员')
)
prj_RESOURCETYPE = (
    ('LB', '人工工时'),
    ('IT', '物品'),
    ('OT', '其它')
)
prj_RESOURCEUNIT = (
    ('HR', '小时'),
    ('PC', '件'),
    ('EA', '个')
)
# ====   document document  start  ====
doc_TYPE = (
    ('QT', '报价'),  # QT = Quotation
    ('CT', '合同'),  # CT = Contract
    ('DF', '初步方案'),  # DF = Draft
    ('SL', '正式方案'),  # SL = Solution
    ('OT', '其它'),  # OT  = Other
)