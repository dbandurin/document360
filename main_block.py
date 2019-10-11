from s3_utils import get_s3_keys, read_image_from_s3
import document_db 
from pre_process import image_process
from post_process import text_process
import ocr
import matplotlib.pyplot as plt
import time

#Read all images from S3
bucket_name = 'document360'

#Get all images from S3
image_list = get_s3_keys(bucket_name)

#Declare document_db instance
doc_db = document_db.DocumentDB('documents','texts')

#To drop existing document collection
#doc_db.collection.drop()

t0 = time.time()
n_doc = 0
for fname in image_list[:]:
    img = read_image_from_s3(bucket_name, fname)
    img_cleaned = image_process(img)
    text = ocr.extract_text(img_cleaned)
    text_cleaned = text_process(text)
    doc_db.write_to_db(bucket_name, fname, text_cleaned)
    print('{} processed'.format(fname))
    n_doc +=1

    #print('\n',fname)
    #print(text_cleaned)
    # plt.figure(0)
    # plt.imshow(img)
    # input("Press Enter to continue...")
print('Total processing time: {}s for {} documents.'.format(time.time()-t0, n_doc))
# 55.7s for 18 docs (3 sec/doc)