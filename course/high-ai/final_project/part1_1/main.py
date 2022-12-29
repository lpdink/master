from utils import get_dataset, logging
from sklearn.neighbors import KNeighborsClassifier as KNN
from sklearn.neural_network import MLPClassifier


train_src, train_dst, test_src, test_dst = get_dataset(
    "/home/lpdink/github/master/course/high-ai/final_project/part1/resources/mnist"
)

def knn_sklearn(n_neighbors):
    model = KNN(n_neighbors=n_neighbors)
    logging.warning(f"KNN模型，K={n_neighbors}")
    model.fit(train_src.reshape(train_src.shape[0], -1), train_dst)
    ret = model.predict(test_src.reshape(test_src.shape[0], -1))
    acc = (ret==test_dst).sum()/len(ret)*100
    logging.warning(f"测试集上预测准确率：{acc}% K={n_neighbors}")

def mlp_sklearn(hidden_nodes, learning_rate):
    model = MLPClassifier(hidden_layer_sizes=(hidden_nodes,),learning_rate_init=learning_rate)
    logging.warning(f"sklearn中的全连接模型，hidden_nodes={hidden_nodes}, learning_rate={learning_rate}")
    model.fit(train_src.reshape(train_src.shape[0], -1), train_dst)
    ret = model.predict(test_src.reshape(test_src.shape[0], -1))
    acc = (ret==test_dst).sum()/len(ret)*100
    logging.warning(f"测试集上预测准确率：{acc}%")
    


if __name__ == "__main__":

    # KNN
    # for k in range(1, 8, 2):
    #     knn_sklearn(k)

    # mlp in sklearn, 隐层节点数影响
    # for hidden_nodes in [500, 1000, 1500, 2000]:
    #     mlp_sklearn(hidden_nodes, 0.01)

    # mlp in sklearn, 学习率影响
    # for learning_rate in [0.1, 0.01, 0.001, 0.0001]:
    #     mlp_sklearn(1000, learning_rate)
    

    breakpoint()
