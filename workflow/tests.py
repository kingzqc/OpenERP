from django.test import TestCase

# Create your tests here.

def role_to_user(self, databu='', rolecode='', wfresource='', wfcustomer='', wfopportunity=' ', wfproject=''):
    print(wfresource)
    if rolecode == 'self':
        relatedata = int(wfresource)
        playerid = relatedata

    if rolecode == 'mgr':
        relatedata = int(wfresource)
        am = '1'
        # am = AccountMaster.objects.filter(Account_bu_id=databu, Account_name_id=relatedata).first()
        if am:
            # playerid = str(am.Account_manager_id)
            playerid = 1
    if rolecode == 'accmgr':
        relatedata = int(wfcustomer)
        cm = CustomerMaster.objects.filter(Data_bu_id=databu, Data_id=relatedata).first()
        if cm:
            playerid = cm.Data_owner_id
    if rolecode == 'oppmgr':
        relatedata = int(wfopportunity)
        om = OpportunityMaster.objects.filter(Data_bu_id=databu, Data_id=relatedata).first()
        if om:
            playerid = om.Data_owner_id
    if rolecode == 'prjmgr':
        relatedata = int(wfproject)
        pm = ProjectMaster.objects.filter(Data_bu_id=databu, Data_id=relatedata).first()
        if pm:
            playerid = pm.Project_manager_id
    return str(playerid)