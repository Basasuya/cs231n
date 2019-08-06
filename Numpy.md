# Numpy

* np.sum, np.argsort, np.argmax 等等都是　axis = 0是按列, axis = 1是按行进

* 当二维矩阵和一维矩阵相加的时候，可以通过np.expand_dims来把一维矩阵扩充为２维的数组

```python
n = 4
a = np.zeros(n)
np.expand_dims(a, axis = 0)
# 扩充为(1, n)
np.expand_dims(a, axis = 1)
# 扩充为(n, 1)
```

* 选择二维数组中的几行，或者几列可以通过数组操作完成。如果只想选择其中的一部分元素，可以直接通过a[array1, array2]的组合方式进行选择

```python
a = np.random.rand(2,3)
a[[1,2],:]
# 选择行
a[:, [1]]
# 选择列
a[[0,1], [1,0]]
# 最后会形成一个１维度的数组
```

* 如果想选择二维数组每行的不同元素，可以通过np.choose(choose, array)，默认对于array的行进行选择
* np.hstack((a,b))对于两个二维数组　进行行合并，

