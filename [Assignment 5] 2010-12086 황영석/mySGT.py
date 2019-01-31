from sklearn.datasets import fetch_mldata
import mySGT_k_pp
import numpy as np
import scipy.spatial.distance as dis

# perform clustering using kmeans
def kmeans_prediction(X):

    runlabels = kmeans_prediction_for_votes(X)
    init_labels = runlabels
    init_votes = votes(init_labels)
    totalvotes = countvote(X, init_votes, 20)
    final_labels = find_max_vote(totalvotes)

    print '========================terminate!'
    # return runlabels
    return final_labels

# initialize k centers
def init_centers(X, k):
    # centers = random.sample(X, k)
    centers = mySGT_k_pp._k_init(X, k, mySGT_k_pp.x_squared_norms(X), np.random)
    return centers

# calculate distance between center and instance
def distance(x, center):
    dist = np.linalg.norm(x-center, 1)
    #ord = 1 : sum abs(x), 2 : largest 2-norm
  #   weight = [ 0.07075733,  0.06003508,  0.41087461,  0.09631327,  0.07616281,  0.04391302,
  # 0.06964736,  0.09919746,  0.14532772]  ### Variation of each attribute
    weight = [ 0.07075733,  0.06003508,  0.82216,  0.31327,  0.07616281,  0.04391302,
  0.06964736,  0.6011782,  0.14532772]
    # print x
    # print center.shape
    # print x. shape
    xnc = []
    xnc.append(x)
    xnc.append(center)
    # print "XNC"
    # print xnc
    # print len([x,center])
    dist2 = dis.pdist([x,center], 'wminkowski', p=1, w = weight)
    # glass = fetch_mldata('glass')
    # X = glass.data
    #
    # def attr_var(X):
    #     numpy_array = []
    #     for x in X :
    #         numpy_array.append(x)
    #     return np.var(numpy_array, axis=0)
    # var = attr_var(X)
    #
    # print "x-center"
    # print len(x-center)
    # print "shape"
    # print (x-center).shape
    # print x-center
    # xnc = [x,center]
    #  dist = dis.pdist(xnc,'cosine')   # cosine distance
    # dist = dis.pdist(xnc,'mahalanobis', VI=None)   #mahalanobis distance
    # dist = dis.pdist(xnc,'correlation')
    # dist = dis.seuclidean(x, center, var)

    # one_norm = []
    # for i in range(9):
    #     one_norm.append(abs(np.subtract(x(i), center(i)))/var(i))
    # dist2 = np.linalg.norm(one_norm,1)
    # uclidean -> association coeffi. : matching coeffi.
    return dist2


# cluster points
def cluster_points(X, centers):

    # initialize
    k = len(centers)
    labels = []

    # for each instance
    for x in X:
        dists = []

        # for each class
        for i in range(k):
            dist = distance(x, centers[i])
            dists.append(dist)

        # find index of class with the minimum distance
        label = dists.index(min(dists))+1
        labels.append(label)
    return labels

# evaluate centers
def evaluate_centers(X, labels, k):
    centers = []

    for value in range(k):
        # find indices of instances whose labels equal to the given value
        index = [j for j in range(len(labels)) if labels[j] == value+1]
        # calculate center as the value of their mean
        center = np.mean([X[idx] for idx in index], axis=0)
        # center = np.median([X[idx] for idx in index], axis=0)
        centers.append(center)
    return centers

# check termination condition
def terminate(centers_old, centers, max_iter, iteration):
    # flag = iteration > max_iter#
    if iteration > max_iter : return  True
    # print np.array(centers)-np.array(centers_old)
    # print np.linalg.norm(np.array(centers)-np.array(centers_old))
    # return distance(np.array(centers),np.array(centers_old))< 0.000000001
    # return  flag

################################################################################################

def kmeans_prediction_for_votes(X):
        # parameters
        k = 7
        max_iter = 100
        iteration = 1
        # Initialize k centers
        centers = init_centers(X, k)
        while 1:
            # Initialize
            centers_old = centers
            # print 'iteration', iteration
            iteration += 1
            # Assign all points in X to centers
            labels = cluster_points(X, centers_old)
            # Evaluate centers
            centers = evaluate_centers(X, labels, k)

            # Check if terminate ## converge old-center center deviation < e
            if terminate(centers_old, centers, max_iter, iteration):
                print '========================vote terminated!'
                return labels

### Transform an label to a vote
def votes(labels):
    vote=[]
    k=7
    for i in range(len(labels)):
        eachvote = [0,0,0,0,0,0,0]
        for j in range(k):
            if labels[i] == j+1:
                eachvote[j] += 1
        vote.append(eachvote)
    return vote

### Count all the votes, collected during iterations
def countvote(X, init_votes, max_iter):
    totalvotes = init_votes
    for i in range(max_iter):
        ith_labels = kmeans_prediction_for_votes(X)
        ith_votes = votes(ith_labels)
        totalvotes = np.array(totalvotes) + np.array(ith_votes)
    return totalvotes

### For each data, find the best label that received the most vote.
def find_max_vote(totalvotes):
    max_label = []
    for i in range(214):
        max_label.append((np.array(totalvotes).argmax(axis=1)[i]) + 1)
    return max_label