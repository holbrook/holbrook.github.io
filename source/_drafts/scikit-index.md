---
title: scikit-index
date: 
category: 
tags: 
---

# 深入MLPClassifier


.neural_network中MLPClassifier各个参数 
例如:mlp = MLPClassifier(solver=’sgd’, activation=’relu’,alpha=1e-4,hidden_layer_sizes=(50,50), random_state=1,max_iter=10,verbose=10,learning_rate_init=.1)

参数说明: 
1. hidden_layer_sizes :例如hidden_layer_sizes=(50, 50)，表示有两层隐藏层，第一层隐藏层有50个神经元，第二层也有50个神经元。 
2. activation :激活函数,{‘identity’, ‘logistic’, ‘tanh’, ‘relu’}, 默认relu 
- identity：f(x) = x 
- logistic：其实就是sigmod,f(x) = 1 / (1 + exp(-x)). 
- tanh：f(x) = tanh(x). 
- relu：f(x) = max(0, x) 
3. solver： {‘lbfgs’, ‘sgd’, ‘adam’}, 默认adam，用来优化权重 
- lbfgs：quasi-Newton方法的优化器 
- sgd：随机梯度下降 
- adam： Kingma, Diederik, and Jimmy Ba提出的机遇随机梯度的优化器 
注意：默认solver ‘adam’在相对较大的数据集上效果比较好（几千个样本或者更多），对小数据集来说，lbfgs收敛更快效果也更好。 
4. alpha :float,可选的，默认0.0001,正则化项参数 
5. batch_size : int , 可选的，默认’auto’,随机优化的minibatches的大小batch_size=min(200,n_samples)，如果solver是’lbfgs’，分类器将不使用minibatch 
6. learning_rate :学习率,用于权重更新,只有当solver为’sgd’时使用，{‘constant’，’invscaling’, ‘adaptive’},默认constant 
- ‘constant’: 有’learning_rate_init’给定的恒定学习率 
- ‘incscaling’：随着时间t使用’power_t’的逆标度指数不断降低学习率learning_rate_ ，effective_learning_rate = learning_rate_init / pow(t, power_t) 
- ‘adaptive’：只要训练损耗在下降，就保持学习率为’learning_rate_init’不变，当连续两次不能降低训练损耗或验证分数停止升高至少tol时，将当前学习率除以5. 
7. power_t: double, 可选, default 0.5，只有solver=’sgd’时使用，是逆扩展学习率的指数.当learning_rate=’invscaling’，用来更新有效学习率。 
8. max_iter: int，可选，默认200，最大迭代次数。 
9. random_state:int 或RandomState，可选，默认None，随机数生成器的状态或种子。 
10. shuffle: bool，可选，默认True,只有当solver=’sgd’或者‘adam’时使用，判断是否在每次迭代时对样本进行清洗。 
11. tol：float, 可选，默认1e-4，优化的容忍度 
12. learning_rate_int:double,可选，默认0.001，初始学习率，控制更新权重的补偿，只有当solver=’sgd’ 或’adam’时使用。 
14. verbose : bool, 可选, 默认False,是否将过程打印到stdout 
15. warm_start : bool, 可选, 默认False,当设置成True，使用之前的解决方法作为初始拟合，否则释放之前的解决方法。 
16. momentum : float, 默认 0.9,动量梯度下降更新，设置的范围应该0.0-1.0. 只有solver=’sgd’时使用. 
17. nesterovs_momentum : boolean, 默认True, Whether to use Nesterov’s momentum. 只有solver=’sgd’并且momentum > 0使用. 
18. early_stopping : bool, 默认False,只有solver=’sgd’或者’adam’时有效,判断当验证效果不再改善的时候是否终止训练，当为True时，自动选出10%的训练数据用于验证并在两步连续迭代改善，低于tol时终止训练。 
19. validation_fraction : float, 可选, 默认 0.1,用作早期停止验证的预留训练数据集的比例，早0-1之间，只当early_stopping=True有用 
20. beta_1 : float, 可选, 默认0.9，只有solver=’adam’时使用，估计一阶矩向量的指数衰减速率，[0,1)之间 
21. beta_2 : float, 可选, 默认0.999,只有solver=’adam’时使用估计二阶矩向量的指数衰减速率[0,1)之间 
22. epsilon : float, 可选, 默认1e-8,只有solver=’adam’时使用数值稳定值。 
属性说明： 
- classes_:每个输出的类标签 
- loss_:损失函数计算出来的当前损失值 
- coefs_:列表中的第i个元素表示i层的权重矩阵 
- intercepts_:列表中第i个元素代表i+1层的偏差向量 
- n_iter_ ：迭代次数 
- n_layers_:层数 
- n_outputs_:输出的个数 
- out_activation_:输出激活函数的名称。


model = MLPClassifier(activation='relu', solver='adam', alpha=0.0001)
"""参数
---
    hidden_layer_sizes: 元祖
    activation：激活函数
    solver ：优化算法{‘lbfgs’, ‘sgd’, ‘adam’}
    alpha：L2惩罚(正则化项)参数。
"""


solver:

- lbfgs，准确率较高，比较适合小(少于几千)数据集来说，且使用的是全训练集训练，比较消耗内存
- adam, 在这里准确率较低
- sgd，在这里准确最高，且每次训练都会分batch，消耗更小的内存


fit和partial_fit进行训练的区别 
可以看出即使训练的顺序和迭代的次数一样但准确率仍然有区别。

```

# 训练模型
# mlp.fit(x_training_data_final, y_training_data_final) 


# 将数据切割成batch
x_training_data_final1 = x_training_data_final[:30000]
y_training_data_final1 = y_training_data_final[:30000]
x_training_data_final2 = x_training_data_final[30000:]
y_training_data_final2 = y_training_data_final[30000:]

# #partial_fit只会进行一次迭代，需要循环进行迭代max_iter=10
# for i in range(10):
#     #第一次调用需要加classes
#     mlp.partial_fit(x_training_data_final1,y_training_data_final1,classes)
#     mlp.partial_fit(x_training_data_final2,y_training_data_final2)

```

对于神经网络的输出层（即mlp.out_activation_,且mlp.out_activation_不可设置），激活函数的选取还是有一定的原则的： 
1) 如果是两类判别，输出层只有一个神经元，那么选logistic，即实例1mlp.out_activation_输出； 
2) 如果是n类判别，输出层有n个神经元，那么选softmax即实例2，输出0-9多分类； 
3) 如果是回归，那么选线性。 
这些选择并不是为了提高性能，而只是让输出的范围合理。 
对于判别问题，输出是概率，所以必须在0到1之间，多类判别时还需要加起来等于1； 
对于回归问题，一般没有理由要求输出在0到1之间。 





## 交叉验证



from sklearn.model_selection import cross_val_score
cross_val_score(model, X, y=None, scoring=None, cv=None, n_jobs=1)
"""参数
---
    model：拟合数据的模型
    cv ： k-fold
    scoring: 打分参数-‘accuracy’、‘f1’、‘precision’、‘recall’ 、‘roc_auc’、'neg_log_loss'等等
"""

使用检验曲线，我们可以更加方便的改变模型参数，获取模型表现。

复制代码
from sklearn.model_selection import validation_curve
train_score, test_score = validation_curve(model, X, y, param_name, param_range, cv=None, scoring=None, n_jobs=1)
"""参数
---
    model:用于fit和predict的对象
    X, y: 训练集的特征和标签
    param_name：将被改变的参数的名字
    param_range： 参数的改变范围
    cv：k-fold
   
返回值
---
   train_score: 训练集得分（array）
    test_score: 验证集得分（array）
"""


交叉验证是经常用到的验证方法
使用sklearn可以很大程度上简化交叉验证的过程
使用过程见下方：

from sklearn import cross_validation
gbdt=GradientBoostingRegressor()
score = cross_validation.cross_val_score(gbdt, train_set, 
    label_set, cv=10, scoring='accuracy')

这里以gbdt模型为例
train_set：训练集
label_set：标签
cv: 交叉验证的倍数
scoring: 返回结果的类型，可以自定义，也有很多默认选项
         例如‘accuracy’, 就是返回准确率
         [‘accuracy‘, ‘adjusted_rand_score‘, 
         ‘average_precision‘, ‘f1‘, ‘f1_macro‘, 
         ‘f1_micro‘, ‘f1_samples‘, ‘f1_weighted‘, 
         ‘log_loss‘, ‘mean_absolute_error‘, 
         ‘mean_squared_error‘, ‘median_absolute_error‘,
          ‘precision‘, ‘precision_macro‘, 
          ‘precision_micro‘, ‘precision_samples‘, 
          ‘precision_weighted‘, ‘r2‘, ‘recall‘, 
          ‘recall_macro‘, ‘recall_micro‘, 
          ‘recall_samples‘, ‘recall_weighted‘, 
          ‘roc_auc‘]   都是可以的
         
这就是简单的用法，只有scoring比较复杂，其他都比较简单


绘图：
http://scikit-learn.org/stable/auto_examples/model_selection/plot_validation_curve.html#sphx-glr-auto-examples-model-selection-plot-validation-curve-py