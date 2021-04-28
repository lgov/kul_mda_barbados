from pandas import Series,DataFrame
import seaborn as sns
import pandas as pd
from matplotlib import pyplot as plt
import numpy
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import numpy as np

def data_number_total_log (path,year):
    df = pd.read_excel(path)
    data = df[df["report_end_date"].dt.year == year]
    data_summary = data.groupby('cik').agg({'value': ['sum', 'count']})
    index_name = data_summary.index
    total_value = []
    number_stocks = []
    for i in range(0, len(data_summary)):
        total_value.append(data_summary.values[i, 0])
        number_stocks.append(data_summary.values[i, 1])
    data_final = {'number_stocks': number_stocks, 'total_value': total_value}
    data_final = DataFrame(data_final)
    data_final.set_axis(index_name,axis='index')
    data_final = data_final.drop(data_final[data_final['total_value']==0].index)
    data_final['number_stocks'] = numpy.log(data_final['number_stocks'])
    data_final['total_value'] = numpy.log(data_final['total_value'])
    return  data_final


def data_plot (data_afterlog):
    sns.lmplot(x="number_stocks", y="total_value", data=data_afterlog)

def optimize_kmean (data_afterlog):
    wcss = []
    n=11
    if len(data_afterlog)<11:
        n=len(data_afterlog)
    for i in range(1, n):
        kmeans = KMeans(n_clusters=i, init='k-means++', max_iter=300, n_init=10, random_state=0)
        kmeans.fit(data_afterlog)
        wcss.append(kmeans.inertia_)
    plt.figure()
    plt.plot(range(1, n), wcss)
    plt.title('Elbow Method')
    plt.xlabel('Number of clusters')
    plt.ylabel('WCSS')

def kmean_plot (data_afterlog,clusters_n):
    pca = PCA(2)
    data_cluster = pca.fit_transform(data_afterlog)
    kmeans = KMeans(n_clusters=clusters_n)
    label = kmeans.fit_predict(data_cluster)
    centroids = kmeans.cluster_centers_
    u_labels = np.unique(label)
    plt.figure()
    for i in u_labels:
        plt.scatter(data_cluster[label == i, 0], data_cluster[label == i, 1], label=i)
    plt.scatter(centroids[:, 0], centroids[:, 1], s=80, color="black")
    plt.legend()
    plt.show()


def one_step_plot_kmean(path,year,clusters_n):
    data=data_number_total_log(path,year)
    data_plot(data)
    optimize_kmean(data)
    kmean_plot(data,clusters_n)

if __name__ == '__main__':
    one_step_plot_kmean("../data/all_submission_files.xlsx",2020,4)


