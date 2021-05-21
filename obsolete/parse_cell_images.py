import matplotlib.pyplot as plt
from skimage import io
import numpy as np
import os

# directory = "./images/"
# for filename in os.listdir(directory):
#    print("\"" + filename + "\", ", end="")

img_names = ["AICS-10_48_4.ome.tif", "AICS-10_40_1.ome.tif", "AICS-10_63_6.ome.tif", "AICS-10_33_7.ome.tif",
             "AICS-10_3_7.ome.tif", "AICS-10_34_5.ome.tif", "AICS-10_42_6.ome.tif", "AICS-10_70_4.ome.tif",
             "AICS-10_55_2.ome.tif", "AICS-10_46_1.ome.tif", "AICS-10_28_1.ome.tif", "AICS-10_52_1.ome.tif",
             "AICS-10_82_1.ome.tif", "AICS-10_47_2.ome.tif", "AICS-10_31_1.ome.tif", "AICS-10_32_5.ome.tif",
             "AICS-10_59_9.ome.tif", "AICS-10_34_6.ome.tif", "AICS-10_68_4.ome.tif", "AICS-10_37_2.ome.tif",
             "AICS-10_54_2.ome.tif", "AICS-10_36_1.ome.tif", "AICS-10_29_1.ome.tif", "AICS-10_47_1.ome.tif",
             "AICS-10_46_2.ome.tif", "AICS-10_64_6.ome.tif", "AICS-10_73_2.ome.tif", "AICS-10_37_3.ome.tif",
             "AICS-10_58_9.ome.tif", "AICS-10_70_3.ome.tif", "AICS-10_64_3.ome.tif", "AICS-10_51_3.ome.tif",
             "AICS-10_35_1.ome.tif", "AICS-10_58_5.ome.tif", "AICS-10_63_8.ome.tif", "AICS-10_44_10.ome.tif",
             "AICS-10_43_3.ome.tif", "AICS-10_64_2.ome.tif", "AICS-10_33_1.ome.tif", "AICS-10_27_1.ome.tif",
             "AICS-10_39_1.ome.tif", "AICS-10_71_3.ome.tif", "AICS-10_31_4.ome.tif", "AICS-10_53_7.ome.tif",
             "AICS-10_56_2.ome.tif", "AICS-10_0_7.ome.tif", "AICS-10_63_3.ome.tif", "AICS-10_51_1.ome.tif",
             "AICS-10_60_7.ome.tif", "AICS-10_35_3.ome.tif"]


# 5: anotirana celica
# 0: observed membrana
# 7: anotiran rob celice(membrana)

for img_name in img_names:

    img = io.imread("./images/" + img_name)



# layer = []
# for i in range(img_sk.shape[0]):
#     current_layer = img_sk[i][7][:][:]
#     layer.append(current_layer)
#
# for i in range(img_sk.shape[0]):
#     plt.imshow(layer[i])
#     plt.show()

