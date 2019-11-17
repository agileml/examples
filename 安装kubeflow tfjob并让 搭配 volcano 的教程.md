## 安装kubeflow tfjob并让 搭配 volcano 的教程

参考网址：
https://www.kubeflow.org/docs/started/k8s/overview/
https://www.jianshu.com/p/afe262304fd6
https://yylin1.github.io/2019/01/22/kubeflow-job-scheduling/
https://www.kubeflow.org/docs/use-cases/job-scheduling/


（1）准备工作，安装好 k8s集群，安装好kfctl
（2）确认你是否有一个默认StorageClass且也配置好了动态pv，确认方法如下:

kubectl get sc
输出：

NAME            PROVISIONER            AGE
nfs (default)   fuseim.pri/ifs         147m
slow            kubernetes.io/gce-pd   5d
default表示这个storageclass是默认的。

修改一个storageclass为默认：

    kubectl patch storageclass <your-class-name> -p '{"metadata": {"annotations":{"storageclass.kubernetes.io/is-default-class":"true"}}}'


​	
	我这里用的是：
	    kubectl patch storageclass alicloud-disk-ssd -p '{"metadata": {"annotations":{"storageclass.kubernetes.io/is-default-class":"true"}}}'

（3）安装kfctl

(4)安装 istio 和 kubeflow的一些组件

```
export PATH=$PATH:"/usr/bin/kfctl"
export KF_NAME="my-kubeflow"
export BASE_DIR="/opt"
export KF_DIR=${BASE_DIR}/${KF_NAME}
export CONFIG_URI="https://raw.githubusercontent.com/kubeflow/manifests/v0.7-branch/kfdef/kfctl_k8s_istio.0.7.0.yaml"


kfctl init ${KF_DIR} --config=${CONFIG_URI} -V

cd ${KF_DIR}
kfctl generate all -V
```

这一步后会生成 app.yaml 和 kustomize文件夹

注意要 提前创建namespace kubeflow-anonymous
kubectl create namespace kubeflow-anonymous

然后就可以
kfctl apply all -V

但是我直接使用apply的时候seldon-core-operator这个组件装不上，所有我修改了app.yaml并且从kustomize文件夹删除了seldon-core-operator。然后执行apply命令。


（5）安装valcano

（6）修改 volcano scheduler.的 clustterrole
kubectl -n kubeflow edit clusterrole  volcano-scheduler
添加

```markdown
  - apiGroups:
    - '*'
    resources:
    - '*'
    verbs:
    - '*'
```

 （7）修改tf-operator的cluster role

```
$ kubectl -n kubeflow edit clusterrole  tf-job-operator
...
...
- apiGroups:
  - scheduling.incubator.k8s.io
  resources:
  - podgroups
  verbs:
  - '*'
```

(8) 修改tf-operator，让其能使用gang-scheduling
Take tf-operator for example, enable gang-scheduling in tf-operator by setting true to --enable-gang-scheduling flag.

```
  $ kubectl -n kubeflow edit deployment tf-job-operator
...
spec:
      containers:
      - command:
        - /opt/kubeflow/tf-operator.v1beta2
        - --alsologtostderr
        - -v=1
        - --enable-gang-scheduling=true
```

