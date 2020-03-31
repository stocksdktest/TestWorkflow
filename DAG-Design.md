# DAG-Design

1.0 版 By 欧阳鸿荣



## 1.Operartor

截止2020年3月31日，一共有如下的operator：

### Release Opeartor

- AndroidReleaseOperator：从GitHub和FTP获取待测试SDK版本runner的apk信息，传递给RunnerOperator
- IOSReleaseOperator：从GitHub和FTP获取待测试SDK版本runner的app信息，传递给RunnerOperator

### Runner Opeartor

- AndroidRunnerOperator：安装apk到测试机，通过RunnerConfig执行测试并存到数据库
- IOSRunnerOperator：接受app信息，安装app到测试机，通过RunnerConfig执行测试并存到数据库
- CrawlerRunnerOperator：通过RunnerConfig驱动竞品爬虫执行测试并存到数据库

### Data Operator

- DataCompareOperator：对来自RunnerOperator的结果进行比较
- DataSortingOperator：对来自RunnerOperator的结果进行排序的校验



## 2.DAG参数

### 运行环境

- 安卓
- iOS
- 竞品爬虫

### SDK版本

- 12月份版本
- 10月份版本
- ……

### 测试环境

- 全真
- 测试



## 3.DAG类型

- 运行环境和SDK版本通过指定不同的Release和Runner Operator提供
- 测试环境通过传入RunnerOperator的RunnerConfig指定

### 3.1 比对型DAG

#### 同SDK版本不同环境

- 安卓不同环境
- iOS不同环境
- 安卓iOS不同环境

#### 同环境不同SDK版本

- 安卓不同版本
- iOS不同版本
- 安卓iOS不同版本

#### 竞品

- TODO

### 3.2 排序性DAG

#### 任意环境任意版本

- 直接比较即可



## 4. 比对方法

目前一共有3种比对方法，分别是通常比对，行情快照比较，排序接口验证

### 4.1 通常比对

- 直接比较2个record的resultData值

### 4.2 行情快照比较

- 对某个用例，连续跑n次，然后对这n次结果组成的list进行比较
- 根据resultData中的datetime字段，取2个list中datetime相同的resultData进行**直接比较**

### 4.3 排序接口验证

- 这个方法其实不是比较，和另外2种比较方式不同，单独考虑

- 一个用例返回一个list，是按照某个字段排序的，检验list是否根据该字段排序

- paramData与待排序字段的对应关系目前是通过预先写好的dict来判断，这个中创那里会自己补充



## 5. DAG样例

### 5.1 DAG样例模板

这里提供了几个不同用途的DAG的例子

- [同一版本同一运行环境通常比对（特殊情况）](http://221.228.66.83:30690/admin/airflow/graph?dag_id=example_base)
- [不同版本不同运行环境行情快照（一般情况）](http://221.228.66.83:30690/admin/airflow/graph?dag_id=example_quote)
- [排序接口测试](http://221.228.66.83:30690/admin/airflow/graph?dag_id=example_sort)

### 5.2 设计DAG注意点

#### 选用不同版本SDK

注意Release和Runner Opeartor的`release_xcom_key`要对上，才能保证安装运行正确的版本

#### 运行行情快照的比较

Runner和DataCompare Opeartor的`run_times`要保持一致，同时DataCompareOperator中要令`quote_detail=True`

#### 运行春节前打包的安卓测试APK(未来将废弃)

在AndroidRunnerOperator中令`config_file=False`