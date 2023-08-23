##trails -yadhu
chitrial = read.csv("C:/Users/Gazal V/Documents/Chisq - Data.csv",header=TRUE)
chitrial
Chitrial1 <- na.omit(chitrial)
Chitrial1
Img1 = data.frame(Chitrial1$ideal.product.E.,Chitrial1$O1)
Img1
chi_testImg1 = chisq.test(Img1)
print(chi_testImg1)
Img2 = data.frame(Chitrial1$ideal.product.E.,Chitrial1$O2)
Img2
chi_testImg2 = chisq.test(Img2)
print(chi_testImg2)
Img3 =data.frame(Chitrial1$ideal.product.E.,Chitrial1$O4)
Img3
chi_testImg3 = chisq.test(Img3)
print(chi_testImg3)
#03
Img4 =data.frame(Chitrial1$ideal.product.E.,Chitrial1$O3)
Img4
chi_testImg4 = chisq.test(Img4)
print(chi_testImg4)
#05
Img5 =data.frame(Chitrial1$ideal.product.E.,Chitrial1$O5)
Img5
chi_testImg5 = chisq.test(Img5)
print(chi_testImg5)
#06
Img6 =data.frame(Chitrial1$ideal.product.E.,Chitrial1$O6)
Img6
chi_testImg6 = chisq.test(Img6)
print(chi_testImg6)
#07
Img7 =data.frame(Chitrial1$ideal.product.E.,Chitrial1$O7)
Img7
chi_testImg7 = chisq.test(Img7)
print(chi_testImg7)
#08
Img8 =data.frame(Chitrial1$ideal.product.E.,Chitrial1$O8)
Img8
chi_testImg8 = chisq.test(Img8)
print(chi_testImg8)
#fisher.test(chi_testImg8)
#09
Img9 =data.frame(Chitrial1$O9,Chitrial1$ideal.product.E.)
Img9
ct <- table(Chitrial1$O9,Chitrial1$ideal.product.E.)
chi_testImg9 = chisq.test(ct)
print(chi_testImg9)
chi_testImg09 = chisq.test(Img9)
print(chi_testImg09)
 #010

Img10 =data.frame(Chitrial1$ideal.product.E.,Chitrial1$O10)
Img10
chi_testImg10 = chisq.test(Img10)
print(chi_testImg10)

