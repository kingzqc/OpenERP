资源详情
@login_required()
def service_detail_edit(request):
    """用户资料维护"""
    job_id = request.GET.get('data_id', '')  # 用户 data id
    #
    if request.method == "GET":
        job_profile = JobMaster.objects.filter(Data_id=job_id)
        if job_profile:
            image = settings.MEDIA_URL + str(job_profile[0].Job_image)
            nickname = job_profile[0].Job_nickname
            contactinfo = job_profile[0].Job_contactinfo
            jobtype = job_profile[0].Job_type_id
            basecity = job_profile[0].Job_basecity
            #
            brief = job_profile[0].Job_brief
            feature = job_profile[0].Job_feature
            value = job_profile[0].Job_value
            summary = job_profile[0].Job_summary
            owner = job_profile[0].Data_owner_id
            jobcode = job_profile[0].Job_code_id
            # 获取已有的数据，返回给前端页面
            servicedetail_form ={
                'mode': 'view',
                'job_id': job_id,
                'imageurl': image,
                'nickname': nickname,
                'contactinfo': contactinfo,
                'jobtype': jobtype,
                'basecity': basecity,
                'brief': brief,
                'feature': feature,
                'value': value,
                'summary': summary,
                'owner': owner,
                'jobcode': jobcode,
            }
            #
            servicedetail_form = forms.JobForm(servicedetail_form) # 没有这句话不体现form定义的格式
            return render(request, 'servicedetail.html', {'msg': servicedetail_form.errors, 'servicedetail_form': servicedetail_form, 'job_id': job_id, 'imageurl': image})
        else:
            servicedetail_form = {
                'mode': 'edit',
                'job_id': '',
                'imageurl': '',
                'nickname': '',
                'contactinfo': '',
                'jobtype': '',
                'basecity': '',
                'brief': '',
                'feature': '',
                'value': '',
                'summary': '',
                'owner': request.user.id,
                'jobcode': '',
            }
            servicedetail_form = forms.JobForm(servicedetail_form)
            return render(request,'servicedetail.html',{'msg':'请输入新增资源的内容','servicedetail_form': servicedetail_form, 'job_id': job_id})
    else:
        servicedetail_form = forms.JobForm(request.POST, request.FILES)
        if servicedetail_form.is_valid():# form验证通过
            # 获取页面数据保存到数据库
            imageurl = ''
            image = request.FILES.get('image', None)
            if image:
                # image upload path
                currentYM = str(datetime.now().strftime('%Y%m'))
                upload_to = 'static/base/static/website/image/' + currentYM
                media_root = settings.MEDIA_ROOT
                full_path = media_root + '/' + upload_to
                if not os.path.exists(full_path):  # 判断路径是否存在
                    os.makedirs(full_path)  # 创建此路径
                # 上传图片文件
                with open(full_path + '/' + image.name, 'wb') as f:
                    for c in image.chunks():  # 相当于切片
                        f.write(c)
                #
                imageurl = upload_to + '/' + image.name
            #
            #print(imageurl)
            nickname = request.POST.get('nickname', None)
            contactinfo = request.POST.get('contactinfo', None)
            jobtype = int(request.POST.get('jobtype', None))
            basecity = request.POST.get('basecity', None)
            brief = request.POST.get('brief', None)
            feature = request.POST.get('feature', None)
            value = request.POST.get('value', None)
            summary = request.POST.get('summary', None)
            owner = int(request.POST.get('owner', None))
            jobcode = int(request.POST.get('jobcode', None))
            #
            if JobMaster.objects.filter(Data_id=job_id):
                if image:
                    JobMaster.objects.filter(Data_id=job_id).update(Job_image=imageurl, Job_nickname=nickname,
                                                                            Job_contactinfo=contactinfo, Job_type_id=jobtype, Job_basecity=basecity,
                                                                            Job_brief=brief, Job_feature=feature, Job_value=value, Job_summary=summary, Data_owner_id=owner, Job_code_id=jobcode)
                else:
                    JobMaster.objects.filter(Data_id=job_id).update(Job_nickname=nickname,
                                                                                    Job_contactinfo=contactinfo,
                                                                                    Job_type_id=jobtype,
                                                                                    Job_basecity=basecity,
                                                                                    Job_brief=brief,
                                                                                    Job_feature=feature,
                                                                                    Job_value=value,
                                                                                    Job_summary=summary, Data_owner_id=owner, Job_code_id=jobcode)
            else:
                JobMaster.objects.create(Job_image=imageurl,
                                                                                Job_nickname=nickname,
                                                                                Job_contactinfo=contactinfo,
                                                                                Job_type_id=jobtype,
                                                                                Job_basecity=basecity,
                                                                                Job_brief=brief,
                                                                                Job_feature=feature,
                                                                                Job_value=value,
                                                                                Job_summary=summary, Data_owner_id=owner, Job_code_id=jobcode)
            #messages.info(request, '保存 sucess!')
            return redirect('/servicelist/?userid='+ str(request.user.id))
        else:
            return render(request, 'servicedetail.html', {'msg': servicedetail_form.errors,'servicedetail_form': servicedetail_form, 'job_id': job_id,})
#