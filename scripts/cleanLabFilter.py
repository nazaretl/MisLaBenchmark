import cleanlab
import pandas as pd
import numpy as np
from utils import confusionMatrixScikit
from cleanlab.classification import LearningWithNoisyLabels
from cleanlab.noise_generation import generate_noisy_labels
from cleanlab.util import value_counts
from cleanlab.latent_algebra import compute_inv_noise_matrix
from sklearn.linear_model import LogisticRegression


# based on https://github.com/cgnorthcutt/cleanlab/blob/master/examples/simplifying_confident_learning_tutorial.ipynb

def CleanLab(X,y,noisyLabels):
 
    X = X.reset_index(drop = True).to_numpy()
    s = noisyLabels.copy().to_numpy()
    
    psx = cleanlab.latent_estimation.estimate_cv_predicted_probabilities(
        X, s, clf=LogisticRegression(max_iter=1000, multi_class='auto', solver='lbfgs'))

    s = np.asarray(s)
    psx = np.asarray(psx)
    K = len(np.unique(s)) # Find the number of unique classes if K is not given

    thresholds = [np.mean(psx[:,k][s == k]) for k in range(K)] # P(s^=k|s=k)
    thresholds = np.asarray(thresholds)

    # Compute confident joint
    confident_joint = np.zeros((K, K), dtype = int)
    for i, row in enumerate(psx):
        s_label = s[i]
        # Find out how many classes each example is confidently labeled as
        confident_bins = row >= thresholds - 1e-6
        num_confident_bins = sum(confident_bins)
        # If more than one conf class, inc the count of the max prob class
        if num_confident_bins == 1:
            confident_joint[s_label][np.argmax(confident_bins)] += 1
        elif num_confident_bins > 1:
            confident_joint[s_label][np.argmax(row)] += 1

    # Normalize confident joint (use cleanlab, trust me on this)
    confident_joint = cleanlab.latent_estimation.calibrate_confident_joint(
        confident_joint, s)
    MIN_NUM_PER_CLASS = 5
    # Leave at least MIN_NUM_PER_CLASS examples per class.
    # NOTE prune_count_matrix is transposed (relative to confident_joint)
    prune_count_matrix = cleanlab.pruning.keep_at_least_n_per_class(
        prune_count_matrix=confident_joint.T,
        n=MIN_NUM_PER_CLASS,
    )

    s_counts = np.bincount(s)
    noise_masks_per_class = []
    # For each row in the transposed confident joint
    for k in range(K):
        noise_mask = np.zeros(len(psx), dtype=bool)
        psx_k = psx[:, k]
        if s_counts[k] > MIN_NUM_PER_CLASS:  # Don't prune if not MIN_NUM_PER_CLASS
            for j in range(K):  # noisy label index (k is the true label index)
                if k != j:  # Only prune for noise rates, not diagonal entries
                    num2prune = prune_count_matrix[k][j]
                    if num2prune > 0:
                        # num2prune'th largest p(classk) - p(class j)
                        # for x with noisy label j
                        margin = psx_k - psx[:, j]
                        s_filter = s == j
                        threshold = -np.partition(
                            -margin[s_filter], num2prune - 1
                        )[num2prune - 1]
                        noise_mask = noise_mask | (s_filter & (margin >= threshold))
            noise_masks_per_class.append(noise_mask)
        else:
            noise_masks_per_class.append(np.zeros(len(s), dtype=bool))

    # Boolean label error mask
    label_errors_bool = np.stack(noise_masks_per_class).any(axis=0)

     # Remove label errors if given label == model prediction
    for i, pred_label in enumerate(psx.argmax(axis=1)):
        # np.all let's this work for multi_label and single label
        if label_errors_bool[i] and np.all(pred_label == s[i]):
            label_errors_bool[i] = False

    # Convert boolean mask to an ordered list of indices for label errors
    label_errors_idx = np.arange(len(s))[label_errors_bool]
    # self confidence is the holdout probability that an example
    # belongs to its given class label
    self_confidence = np.array(
        [np.mean(psx[i][s[i]]) for i in label_errors_idx]
    )
    margin = self_confidence - psx[label_errors_bool].max(axis=1)
    label_errors_idx = label_errors_idx[np.argsort(margin)]
    
   # actual_label_errors = y[y!=s].index
    actual_label_errors = y[s != y].index

#    ma.index.name = 't = {}, nEr = {}, N = {}'.format(str(t),len(df)*n, len(df) ) 
    return pd.Series(label_errors_idx)
    
 