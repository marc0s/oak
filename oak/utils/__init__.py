# -*- coding: utf-8 -*-
"Helper functions for oak"

def copytree_(src, dst):
    names = os.listdir(src)
    if not os.path.exists(dst):
        os.mkdir(dst)
    for name in names:
        srcname = os.path.join(src, name)
        dstname = os.path.join(dst, name)
        try:
            if os.path.isdir(srcname):
                copytree_(srcname, dstname)
            else:
                shutil.copy2(srcname, dstname)
        except (IOError, os.error), why:
            raise Exception(why)
    try:
        shutil.copystat(src, dst)
    except OSError, why:
        raise Exception(why)

