# ProGit

通过本文了解不那么常用的git命令（尤其像git rebase，git merge和cherry pick）的使用吧，不用再总被diss是麻瓜了！

> 本文参考progit

## 修补最后一次提交

常见的情况是，手快git commit后，执行git status，发现有几个文件漏交了，或者最后一次git commit的log写错了，如果在以前，我会：

```sh
git reset last_commit_hash
# do right git command
git commit -m "right log"
```

但更好的解决方案是：

```sh
# do right git command, like git add forget_file
git commit --amend -m "new log"
# 你也可以不加-m，这将使用之前的log，如果log没有错误的话。
```

## 远程操作

```sh
# 远程操作
git remote --help

# 查看远程配置
git remote -v --verbose

# 添加远程, 添加多个远程是很有用的，push和pull默认用origin，你可以给origin配置ssh，另起一个名字（如origin_http)，用于http方式
# 或者，可以推到多个远程仓库
git remote add remote_name remote_url/ssh
# 其他的rename和remove等可以在help里看到

# 推送tag到远程
git push remote_name(origin) tag_name
# 全部tag
git push remote_name --tags
# 删除tag
git push remote_name --delete tagname/branch_name
```

## checkout到历史提交

我之前这样做：

```sh
git branch new_branch
git checkout new_branch
git reset commit_hash --hard
```

但是最好：

```sh
git checkout -b new_branch tag_name/commit_hash
# 如果不添加commit_hash/tag_name，会用当前的最后一次提交，建议用这种方法替代git branch和git checkout 两句命令

```

建议常用这一命令，这帮助我们更好地模块开发，或探索模块的作用。

## git别名

你可以设置git的命令别名：

```sh
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.st status

```

这样就可以用git ci替代git commit了，不过我不这么设置。

## git branch

### merge

```sh
# 如果branch_name分支是当前分支(head指向)的直接后继，head会直接移动到branch_name分支
git merge branch_name
# 如果你merge了，不需要临时分支，可以删除它了
git branch -d branch_name

# 如果commit冲突了，git merge会帮你生成冲突处理相关的代码，等待你解决冲突。
# 出现冲突时的工作流：
git merge branch_name
# fix conflict
git add conflict.file
git commit -m "merge: fix conflict"
# 解决冲突需要一次额外的git add和git commit，解决冲突后，冲突的两个commit log都会保留，且以你解决冲突的commit作为head指向
```

### 展示信息

```sh
git branch -v # 展示分支们的最后一次提交
git branch --merged # 查看已经合并到当前分支的分支
git branch --no-merged # 查看没合并的
```

### rebase

rebase的直接作用是将某一分支的更改 **应用** 到当前分支，最常用的情况是，如果分支new_feat希望合并到master，但是check到new_feat后的这段时间，master有更新，如果直接在master上merge new_feat分支，就会出现两个分支并行的情况（好处是commit严格按照时间排序了，但这可能是坏处）。  
因此，先在new_feat分支上，git rebase master，将master这段时间的更改应用到本分支。这会将master的更改放在new_feat的任何更改之前，之后再追加new_feat的提交。（这会打乱commit的时间顺序）

总之，rebase的作用主要是避免commit历史上出现复杂的多线并进的情况，保证git commit history是一条直线。  

工作流：

```sh
# new_feat 要进入master:
git checkout new_feat
git rebase master
git checkout master
git merge new_feat

```

关于rebase存在一个警告：不要对已经推送到远程仓库的提交rebase，即，不要调整他们的提交线，这会破坏其他开发者的base。  

### cherry-pick

cherry-pick是将其他分支的某个提交直接拿过来，十分方便。  
这是某种拷贝，也就是说，cherry-pick过来的commit是一个新的commit，如果new分支与master分支只有最新一次提交不同，你cherry-pick了这个提交，那么再merge new到master时，会发现出现了两次最后一次提交。  

```sh
git cherry-pick commit_hash
# cherry-pick来的commit的hash是新的hash
```