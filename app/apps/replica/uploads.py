import datetime

def upload_css(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (instance.slug, ext)
    path = 'css/%s/%s' % (instance.id, filename)
    return path

def upload_media(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (instance.slug, ext)
    date = instance.date_created
    datepath_path = datetime.date.today().strftime("%Y/%m/%d")
    path = 'media/%s/%s/%s' % (datepath_path, instance.id, filename)
    #overwrite_existing(path)
    return path

def upload_media_md(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s_md.%s" % (instance.slug, ext)
    date = instance.date_created
    datepath_path = datetime.date.today().strftime("%Y/%m/%d")
    path = 'media/%s/%s/%s' % (datepath_path, instance.id, filename)
    #overwrite_existing(path)
    return path

def upload_media_sm(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s_sm.%s" % (instance.slug, ext)
    date = instance.date_created
    datepath_path = datetime.date.today().strftime("%Y/%m/%d")
    path = 'media/%s/%s/%s' % (datepath_path, instance.id, filename)
    #overwrite_existing(path)
    return path
