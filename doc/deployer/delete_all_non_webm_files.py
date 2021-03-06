# This Script will delete all mp4 files if it has webm and will replace mp4 objects with webm objects
from gnowsys_ndf.ndf.models import *

video_files_cur = node_collection.find({
                                    'if_file.mime_type': {'$regex': str('video'), '$options': "i"}
                                })


if video_files_cur:
    print "\n All Video files count: ", video_files_cur.count()

    for each in video_files_cur:

        each_mid_url = each.if_file.mid.relurl
        each_original_url = each.if_file.original.relurl

        # `if_file.mid.relurl` contains converted (webm) file.
        if each_mid_url and (each_original_url != each_mid_url):

            print "\n\nUpdating " + each.name + str(each._id)
            # following will delete filehive instance as well as file from hashFS.
            Filehive.delete_file_from_filehive(each.if_file.original.id, each_original_url)
            # TODO: but one additional check needs to be added to check if this particular file is not reference anywhere else.

            each.if_file.original.relurl = each_mid_url
            each.if_file.original.id = each.if_file.mid.id 

            each.save()
