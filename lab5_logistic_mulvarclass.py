#lab5_logistic, multivariate classification
import tensorflow as tf 
import numpy as np
import matplotlib.pyplot as plt
from time import time

start=time()
batch_size=int(input("what batchsize? (1~10000, integer): "))
stepsize=int(input("how often do you want to check accuracy?(1~10000, int): "))

np_xy=np.loadtxt("lab5_diabetes.csv",delimiter=",",dtype=np.float32)
mat_len=len(np_xy[0,:])
n_param=mat_len-1

fq=tf.train.string_input_producer(["lab5_diabetes.csv"], name="fq")
reader=tf.TextLineReader()
key, val= reader.read(fq)

record_defaults=[[0.] for i in range(mat_len)]
xy=tf.decode_csv(val, record_defaults=record_defaults)

train_xb, train_yb= tf.train.batch([xy[0:-1],xy[-1:]], batch_size=batch_size)


X=tf.placeholder(tf.float32, shape=[None,n_param])
Y=tf.placeholder(tf.float32, shape=[None,1])
W=tf.Variable(tf.random_normal([n_param, 1]))
b=tf.Variable(tf.random_normal([1]))

hyp=tf.sigmoid(tf.matmul(X,W)+b)
cost=(-1)*tf.reduce_mean(Y*tf.log(hyp)+(1-Y)*tf.log(1-hyp))
train=tf.train.GradientDescentOptimizer(learning_rate=0.01).minimize(cost)
#this previously were two split lines with one more instance "optimizer"

#classification results analytics
pred=tf.round(hyp)
acc=tf.reduce_mean(tf.cast(tf.equal(pred,Y), dtype=tf.float32))

#run!
sess=tf.Session()
sess.run(tf.global_variables_initializer())

#coordinator for queuerunner
coord=tf.train.Coordinator()
threads=tf.train.start_queue_runners(sess=sess, coord=coord)

xc=[i for i in range(5000)]
step100=[]
yc_cost=[]
yc_acc=[]
avg_acc_list=[]

for step in range(5000):
    x_b, y_b=sess.run([train_xb, train_yb])
    h, p, a, costv, t=sess.run([hyp, pred, acc, cost,train], feed_dict={X:x_b, Y:y_b})
    yc_cost.append(costv)
    yc_acc.append(a)
    if step%stepsize==0:
        step100.append(step)
        #print("\nhypothesis= \n", h,"\nY= \n",y_b,"\nprediction= \n", p, "\n")
        avg_acc=sum(yc_acc)/len(yc_acc)
        avg_acc_list+=list(avg_acc*np.ones(stepsize))
        print("step=", step,"cost= ", costv, "avg_acc= ", avg_acc)
coord.request_stop()
coord.join(threads)

print("for batch_size= %s, stepsize=%s elapsed time is %s"%(batch_size,stepsize,(time()-start)))
print("accuracy reached=%s"%avg_acc_list[-1])

plt.plot(xc,yc_cost)
plt.show()

plt.plot(xc,avg_acc_list)
plt.show()