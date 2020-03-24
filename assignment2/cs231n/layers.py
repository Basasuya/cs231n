from builtins import range
import numpy as np


def affine_forward(x, w, b):
    """
    Computes the forward pass for an affine (fully-connected) layer.

    The input x has shape (N, d_1, ..., d_k) and contains a minibatch of N
    examples, where each example x[i] has shape (d_1, ..., d_k). We will
    reshape each input into a vector of dimension D = d_1 * ... * d_k, and
    then transform it to an output vector of dimension M.

    Inputs:
    - x: A numpy array containing input data, of shape (N, d_1, ..., d_k)
    - w: A numpy array of weights, of shape (D, M)
    - b: A numpy array of biases, of shape (M,)

    Returns a tuple of:
    - out: output, of shape (N, M)
    - cache: (x, w, b)
    """
    out = None
    ###########################################################################
    # TODO: Implement the affine forward pass. Store the result in out. You   #
    # will need to reshape the input into rows.                               #
    ###########################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    
    # flatten the dimensions of each example into 1 row
    x_flatten = np.reshape(x, (x.shape[0], -1))
    
    # linear operation
    out = np.dot(x_flatten, w) + b

    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    cache = (x, w, b)
    return out, cache


def affine_backward(dout, cache):
    """
    Computes the backward pass for an affine layer.

    Inputs:
    - dout: Upstream derivative, of shape (N, M)
    - cache: Tuple of:
      - x: Input data, of shape (N, d_1, ... d_k)
      - w: Weights, of shape (D, M)
      - b: Biases, of shape (M,)

    Returns a tuple of:
    - dx: Gradient with respect to x, of shape (N, d1, ..., d_k)
    - dw: Gradient with respect to w, of shape (D, M)
    - db: Gradient with respect to b, of shape (M,)
    """
    x, w, b = cache
    dx, dw, db = None, None, None
    ###########################################################################
    # TODO: Implement the affine backward pass.                               #
    ###########################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    
    # number of examples
    N = x.shape[0]
    
    # flatten the dimensions of each example into 1 row
    x_flatten = np.reshape(x, (x.shape[0], -1))
    
    # backward pass
    dx = np.dot(dout, w.T)
    dw = np.dot(x_flatten.T, dout)
    db = np.sum(dout, axis=0)
    
    # reshape dx (unflatten)
    dx = np.reshape(dx, x.shape)

    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return dx, dw, db


def relu_forward(x):
    """
    Computes the forward pass for a layer of rectified linear units (ReLUs).

    Input:
    - x: Inputs, of any shape

    Returns a tuple of:
    - out: Output, of the same shape as x
    - cache: x
    """
    out = None
    ###########################################################################
    # TODO: Implement the ReLU forward pass.                                  #
    ###########################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    out = np.maximum(x, 0)

    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    cache = x
    return out, cache


def relu_backward(dout, cache):
    """
    Computes the backward pass for a layer of rectified linear units (ReLUs).

    Input:
    - dout: Upstream derivatives, of any shape
    - cache: Input x, of same shape as dout

    Returns:
    - dx: Gradient with respect to x
    """
    dx, x = None, cache
    ###########################################################################
    # TODO: Implement the ReLU backward pass.                                 #
    ###########################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    dx = np.where(x >=0, dout, 0)

    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return dx


def batchnorm_forward(x, gamma, beta, bn_param):
    """
    Forward pass for batch normalization.

    During training the sample mean and (uncorrected) sample variance are
    computed from minibatch statistics and used to normalize the incoming data.
    During training we also keep an exponentially decaying running mean of the
    mean and variance of each feature, and these averages are used to normalize
    data at test-time.

    At each timestep we update the running averages for mean and variance using
    an exponential decay based on the momentum parameter:

    running_mean = momentum * running_mean + (1 - momentum) * sample_mean
    running_var = momentum * running_var + (1 - momentum) * sample_var

    Note that the batch normalization paper suggests a different test-time
    behavior: they compute sample mean and variance for each feature using a
    large number of training images rather than using a running average. For
    this implementation we have chosen to use running averages instead since
    they do not require an additional estimation step; the torch7
    implementation of batch normalization also uses running averages.

    Input:
    - x: Data of shape (N, D)
    - gamma: Scale parameter of shape (D,)
    - beta: Shift paremeter of shape (D,)
    - bn_param: Dictionary with the following keys:
      - mode: 'train' or 'test'; required
      - eps: Constant for numeric stability
      - momentum: Constant for running mean / variance.
      - running_mean: Array of shape (D,) giving running mean of features
      - running_var Array of shape (D,) giving running variance of features

    Returns a tuple of:
    - out: of shape (N, D)
    - cache: A tuple of values needed in the backward pass
    """
    mode = bn_param['mode']
    eps = bn_param.get('eps', 1e-5)
    momentum = bn_param.get('momentum', 0.9)

    N, D = x.shape
    running_mean = bn_param.get('running_mean', np.zeros(D, dtype=x.dtype))
    running_var = bn_param.get('running_var', np.zeros(D, dtype=x.dtype))

    out, cache = None, None
    if mode == 'train':
        #######################################################################
        # TODO: Implement the training-time forward pass for batch norm.      #
        # Use minibatch statistics to compute the mean and variance, use      #
        # these statistics to normalize the incoming data, and scale and      #
        # shift the normalized data using gamma and beta.                     #
        #                                                                     #
        # You should store the output in the variable out. Any intermediates  #
        # that you need for the backward pass should be stored in the cache   #
        # variable.                                                           #
        #                                                                     #
        # You should also use your computed sample mean and variance together #
        # with the momentum variable to update the running mean and running   #
        # variance, storing your result in the running_mean and running_var   #
        # variables.                                                          #
        #                                                                     #
        # Note that though you should be keeping track of the running         #
        # variance, you should normalize the data based on the standard       #
        # deviation (square root of variance) instead!                        # 
        # Referencing the original paper (https://arxiv.org/abs/1502.03167)   #
        # might prove to be helpful.                                          #
        #######################################################################
        # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

        # compute the minibatch statistics
        sample_mean = np.mean(x, axis=0)
        sample_var = np.var(x, axis=0)
        
        # normalize the incoming data
        X_normalized = (x - sample_mean)/np.sqrt(sample_var + eps)
        
        # scale and shift the normalized data
        out = gamma * X_normalized + beta
        
        # update the running averages
        running_mean = momentum * running_mean + (1 - momentum) * sample_mean
        running_var = momentum * running_var + (1 - momentum) * sample_var
        
        # cache intermediate values for the backward pass
        cache = (x, sample_mean, sample_var, eps, X_normalized, gamma, beta)

        # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
        #######################################################################
        #                           END OF YOUR CODE                          #
        #######################################################################
    elif mode == 'test':
        #######################################################################
        # TODO: Implement the test-time forward pass for batch normalization. #
        # Use the running mean and variance to normalize the incoming data,   #
        # then scale and shift the normalized data using gamma and beta.      #
        # Store the result in the out variable.                               #
        #######################################################################
        # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

        # normalize the incoming data
        X_normalized = (x - running_mean)/np.sqrt(running_var + eps)
        
        # scale and shift the normalized data
        out = gamma * X_normalized + beta
            
        # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
        #######################################################################
        #                          END OF YOUR CODE                           #
        #######################################################################
    else:
        raise ValueError('Invalid forward batchnorm mode "%s"' % mode)

    # Store the updated running means back into bn_param
    bn_param['running_mean'] = running_mean
    bn_param['running_var'] = running_var

    return out, cache


def batchnorm_backward(dout, cache):
    """
    Backward pass for batch normalization.

    For this implementation, you should write out a computation graph for
    batch normalization on paper and propagate gradients backward through
    intermediate nodes.

    Inputs:
    - dout: Upstream derivatives, of shape (N, D)
    - cache: Variable of intermediates from batchnorm_forward.

    Returns a tuple of:
    - dx: Gradient with respect to inputs x, of shape (N, D)
    - dgamma: Gradient with respect to scale parameter gamma, of shape (D,)
    - dbeta: Gradient with respect to shift parameter beta, of shape (D,)
    """
    dx, dgamma, dbeta = None, None, None
    ###########################################################################
    # TODO: Implement the backward pass for batch normalization. Store the    #
    # results in the dx, dgamma, and dbeta variables.                         #
    # Referencing the original paper (https://arxiv.org/abs/1502.03167)       #
    # might prove to be helpful.                                              #
    ###########################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    # unpack cached intermediate values from the forward pass
    (x, sample_mean, sample_var, eps, X_normalized, gamma, beta) = cache
    N = x.shape[0]

    # compute the gradients
    dgamma = np.sum(X_normalized * dout, axis=0)
    dbeta = np.sum(dout, axis=0)
    
    # intermediate gradients of the computational graph
    dX_normalized = gamma * dout
    
    dsample_var = np.sum((x-sample_mean)*dX_normalized, axis=0) * (-0.5/np.sqrt(sample_var + eps)**3)
    
    dsample_mean = -1/np.sqrt(sample_var + eps) * np.sum(dX_normalized, axis=0) + dsample_var * np.sum(-2*(x - sample_mean), axis=0)/N
    
    # final gradient
    dx = 1/np.sqrt(sample_var + eps) * dX_normalized + 1/N*dsample_mean + dsample_var * 2*(x - sample_mean)/N
        
    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################

    return dx, dgamma, dbeta


def batchnorm_backward_alt(dout, cache):
    """
    Alternative backward pass for batch normalization.

    For this implementation you should work out the derivatives for the batch
    normalizaton backward pass on paper and simplify as much as possible. You
    should be able to derive a simple expression for the backward pass. 
    See the jupyter notebook for more hints.
     
    Note: This implementation should expect to receive the same cache variable
    as batchnorm_backward, but might not use all of the values in the cache.

    Inputs / outputs: Same as batchnorm_backward
    """
    dx, dgamma, dbeta = None, None, None
    ###########################################################################
    # TODO: Implement the backward pass for batch normalization. Store the    #
    # results in the dx, dgamma, and dbeta variables.                         #
    #                                                                         #
    # After computing the gradient with respect to the centered inputs, you   #
    # should be able to compute gradients with respect to the inputs in a     #
    # single statement; our implementation fits on a single 80-character line.#
    ###########################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    # unpack cached intermediate values from the forward pass
    (x, sample_mean, sample_var, eps, X_normalized, gamma, beta) = cache
    N = x.shape[0]

    # compute the gradients
    dgamma = np.sum(X_normalized * dout, axis=0)
    dbeta = np.sum(dout, axis=0)
    
    # intermediate gradients of the computational graph
    dX_normalized = gamma * dout
    
    dsample_var = -0.5 * np.sum(X_normalized*dX_normalized, axis=0) * 1/(sample_var + eps)
    
    dsample_mean = - np.sqrt(sample_var + eps) * ( 1/(sample_var + eps) * np.sum(dX_normalized, axis=0) + 2/N * dsample_var * np.sum(X_normalized, axis=0) )
    
    # final gradient
    dx = 1/np.sqrt(sample_var + eps) * dX_normalized + 1/N*dsample_mean + dsample_var * 2*np.sqrt(sample_var + eps)*X_normalized/N
        
    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################

    return dx, dgamma, dbeta


def layernorm_forward(x, gamma, beta, ln_param):
    """
    Forward pass for layer normalization.

    During both training and test-time, the incoming data is normalized per data-point,
    before being scaled by gamma and beta parameters identical to that of batch normalization.
    
    Note that in contrast to batch normalization, the behavior during train and test-time for
    layer normalization are identical, and we do not need to keep track of running averages
    of any sort.

    Input:
    - x: Data of shape (N, D)
    - gamma: Scale parameter of shape (D,)
    - beta: Shift paremeter of shape (D,)
    - ln_param: Dictionary with the following keys:
        - eps: Constant for numeric stability

    Returns a tuple of:
    - out: of shape (N, D)
    - cache: A tuple of values needed in the backward pass
    """
    out, cache = None, None
    eps = ln_param.get('eps', 1e-5)
    ###########################################################################
    # TODO: Implement the training-time forward pass for layer norm.          #
    # Normalize the incoming data, and scale and  shift the normalized data   #
    #  using gamma and beta.                                                  #
    # HINT: this can be done by slightly modifying your training-time         #
    # implementation of  batch normalization, and inserting a line or two of  #
    # well-placed code. In particular, can you think of any matrix            #
    # transformations you could perform, that would enable you to copy over   #
    # the batch norm code and leave it almost unchanged?                      #
    ###########################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    # compute the feature statistics
    sample_mean = np.mean(x, axis=1, keepdims=True)
    sample_var = np.var(x, axis=1, keepdims=True)

    # normalize the incoming data
    X_normalized = (x - sample_mean)/np.sqrt(sample_var + eps)

    # scale and shift the normalized data
    out = gamma * X_normalized + beta

    # cache intermediate values for the backward pass
    cache = (x, sample_mean, sample_var, eps, X_normalized, gamma, beta)
    
    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return out, cache


def layernorm_backward(dout, cache):
    """
    Backward pass for layer normalization.

    For this implementation, you can heavily rely on the work you've done already
    for batch normalization.

    Inputs:
    - dout: Upstream derivatives, of shape (N, D)
    - cache: Variable of intermediates from layernorm_forward.

    Returns a tuple of:
    - dx: Gradient with respect to inputs x, of shape (N, D)
    - dgamma: Gradient with respect to scale parameter gamma, of shape (D,)
    - dbeta: Gradient with respect to shift parameter beta, of shape (D,)
    """
    dx, dgamma, dbeta = None, None, None
    ###########################################################################
    # TODO: Implement the backward pass for layer norm.                       #
    #                                                                         #
    # HINT: this can be done by slightly modifying your training-time         #
    # implementation of batch normalization. The hints to the forward pass    #
    # still apply!                                                            #
    ###########################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    # unpack cached intermediate values from the forward pass
    (x, sample_mean, sample_var, eps, X_normalized, gamma, beta) = cache
    N = x.shape[1]

    # compute the gradients
    dgamma = np.sum(X_normalized * dout, axis=0)
    dbeta = np.sum(dout, axis=0)
    
    # intermediate gradients of the computational graph
    dX_normalized = gamma * dout
    
    dsample_var = np.sum((x-sample_mean)*dX_normalized, axis=1, keepdims=True) * (-0.5/np.sqrt(sample_var + eps)**3)
    
    dsample_mean = -1/np.sqrt(sample_var + eps) * np.sum(dX_normalized, axis=1, keepdims=True) + dsample_var * np.sum(-2*(x - sample_mean), axis=1, keepdims=True)/N
    
    # final gradient
    dx = 1/np.sqrt(sample_var + eps) * dX_normalized + 1/N*dsample_mean + dsample_var * 2*(x - sample_mean)/N
        
    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return dx, dgamma, dbeta


def dropout_forward(x, dropout_param):
    """
    Performs the forward pass for (inverted) dropout.

    Inputs:
    - x: Input data, of any shape
    - dropout_param: A dictionary with the following keys:
      - p: Dropout parameter. We keep each neuron output with probability p.
      - mode: 'test' or 'train'. If the mode is train, then perform dropout;
        if the mode is test, then just return the input.
      - seed: Seed for the random number generator. Passing seed makes this
        function deterministic, which is needed for gradient checking but not
        in real networks.

    Outputs:
    - out: Array of the same shape as x.
    - cache: tuple (dropout_param, mask). In training mode, mask is the dropout
      mask that was used to multiply the input; in test mode, mask is None.

    NOTE: Please implement **inverted** dropout, not the vanilla version of dropout.
    See http://cs231n.github.io/neural-networks-2/#reg for more details.

    NOTE 2: Keep in mind that p is the probability of **keep** a neuron
    output; this might be contrary to some sources, where it is referred to
    as the probability of dropping a neuron output.
    """
    p, mode = dropout_param['p'], dropout_param['mode']
    if 'seed' in dropout_param:
        np.random.seed(dropout_param['seed'])

    mask = None
    out = None

    if mode == 'train':
        #######################################################################
        # TODO: Implement training phase forward pass for inverted dropout.   #
        # Store the dropout mask in the mask variable.                        #
        #######################################################################
        # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

        mask = np.random.rand(*x.shape) <= p
        # inverted dropout
        out = 1/p * np.where(mask, x, 0)

        # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
        #######################################################################
        #                           END OF YOUR CODE                          #
        #######################################################################
    elif mode == 'test':
        #######################################################################
        # TODO: Implement the test phase forward pass for inverted dropout.   #
        #######################################################################
        # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

        out = x

        # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
        #######################################################################
        #                            END OF YOUR CODE                         #
        #######################################################################

    cache = (dropout_param, mask)
    out = out.astype(x.dtype, copy=False)

    return out, cache


def dropout_backward(dout, cache):
    """
    Perform the backward pass for (inverted) dropout.

    Inputs:
    - dout: Upstream derivatives, of any shape
    - cache: (dropout_param, mask) from dropout_forward.
    """
    dropout_param, mask = cache
    mode = dropout_param['mode']

    dx = None
    if mode == 'train':
        #######################################################################
        # TODO: Implement training phase backward pass for inverted dropout   #
        #######################################################################
        # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
        
        p = dropout_param['p']
        
        dx = 1/p * np.where(mask, dout, 0)

        # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
        #######################################################################
        #                          END OF YOUR CODE                           #
        #######################################################################
    elif mode == 'test':
        dx = dout
    return dx


def conv_forward_naive(x, w, b, conv_param):
    """
    A naive implementation of the forward pass for a convolutional layer.

    The input consists of N data points, each with C channels, height H and
    width W. We convolve each input with F different filters, where each filter
    spans all C channels and has height HH and width WW.

    Input:
    - x: Input data of shape (N, C, H, W)
    - w: Filter weights of shape (F, C, HH, WW)
    - b: Biases, of shape (F,)
    - conv_param: A dictionary with the following keys:
      - 'stride': The number of pixels between adjacent receptive fields in the
        horizontal and vertical directions.
      - 'pad': The number of pixels that will be used to zero-pad the input. 
        

    During padding, 'pad' zeros should be placed symmetrically (i.e equally on both sides)
    along the height and width axes of the input. Be careful not to modfiy the original
    input x directly.

    Returns a tuple of:
    - out: Output data, of shape (N, F, H', W') where H' and W' are given by
      H' = 1 + (H + 2 * pad - HH) / stride
      W' = 1 + (W + 2 * pad - WW) / stride
    - cache: (x, w, b, conv_param)
    """
    out = None
    ###########################################################################
    # TODO: Implement the convolutional forward pass.                         #
    # Hint: you can use the function np.pad for padding.                      #
    ###########################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    
    # input shape
    N, C, H, W = x.shape
    F, _, HH, WW = w.shape
    
    # hyperparameters
    pad = conv_param['pad']
    stride = conv_param['stride']
    
    # pad input with zeros
    X_padded = np.zeros((N, C, H + 2*pad, W + 2*pad))
    X_padded[:,:, pad:H + pad, pad:W + pad] = x
    
    # output shape
    H_out = int((H + 2*pad - HH)/stride) + 1
    W_out = int((W + 2*pad - WW)/stride) + 1
    
    # initialize output
    out = np.zeros((N, F, H_out, W_out))
    
    # loop over output channel
    for c in range(F):
        # corresponding filter
        W_filter = w[c, :,:,:]
        
        # loop over output height
        for i in range(H_out):
            # corresponding input slice
            h_begin = stride*i
            h_end = h_begin + HH
            
            # loop over output width
            for j in range(W_out):
                # corresponding input slice
                w_begin = stride*j
                w_end = w_begin + WW
                # input slice
                X_slice = X_padded[:,:, h_begin:h_end, w_begin:w_end]
                
                # update the output
                out[:, c, i, j] = np.sum(np.reshape(X_slice * W_filter, (N,-1)), axis=1) + b[c]

    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    cache = (x, w, b, conv_param)
    return out, cache


def conv_backward_naive(dout, cache):
    """
    A naive implementation of the backward pass for a convolutional layer.

    Inputs:
    - dout: Upstream derivatives.
    - cache: A tuple of (x, w, b, conv_param) as in conv_forward_naive

    Returns a tuple of:
    - dx: Gradient with respect to x
    - dw: Gradient with respect to w
    - db: Gradient with respect to b
    """
    dx, dw, db = None, None, None
    ###########################################################################
    # TODO: Implement the convolutional backward pass.                        #
    ###########################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    # unpack cache
    x, w, b, conv_param = cache
    
    # input shape
    N, C, H, W = x.shape
    F, _, HH, WW = w.shape
    
    # hyperparameters
    pad = conv_param['pad']
    stride = conv_param['stride']
    
    # pad input with zeros
    X_padded = np.zeros((N, C, H + 2*pad, W + 2*pad))
    X_padded[:,:, pad:H + pad, pad:W + pad] = x
    
    # output shape
    _, _, H_out, W_out = dout.shape
    
    # initialize gradients
    dx = np.zeros(X_padded.shape)
    dw = np.zeros(w.shape)
    db = np.zeros(b.shape)
    
    # loop over output channel
    for c in range(F):
        # corresponding filter
        W_filter = np.expand_dims(w[c, :,:,:], axis=0)
        
        # loop over output height
        for i in range(H_out):
            # corresponding input slice
            h_begin = stride*i
            h_end = h_begin + HH
            
            # loop over output width
            for j in range(W_out):             
                # corresponding input slice
                w_begin = stride*j
                w_end = w_begin + WW
                # input slice
                X_slice = X_padded[:,:, h_begin:h_end, w_begin:w_end]

                # corresponding output gradient
                dout_current = np.reshape(dout[:, c, i, j], (-1, 1, 1, 1))
                
                # update the gradient
#                 print(dout_current.shape, W_filter.shape, X_slice.shape)
                dx[:,:, h_begin:h_end, w_begin:w_end] += dout_current * W_filter
                dw[c,:,:,:] += np.sum(dout_current * X_slice, axis=0)
                db[c] += np.sum(dout_current)
    
    # remove padded dimension
    dx = dx[:,:, pad:H + pad, pad:W + pad]
                
    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return dx, dw, db


def max_pool_forward_naive(x, pool_param):
    """
    A naive implementation of the forward pass for a max-pooling layer.

    Inputs:
    - x: Input data, of shape (N, C, H, W)
    - pool_param: dictionary with the following keys:
      - 'pool_height': The height of each pooling region
      - 'pool_width': The width of each pooling region
      - 'stride': The distance between adjacent pooling regions

    No padding is necessary here. Output size is given by 

    Returns a tuple of:
    - out: Output data, of shape (N, C, H', W') where H' and W' are given by
      H' = 1 + (H - pool_height) / stride
      W' = 1 + (W - pool_width) / stride
    - cache: (x, pool_param)
    """
    out = None
    ###########################################################################
    # TODO: Implement the max-pooling forward pass                            #
    ###########################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    # input shape
    N, C, H, W = x.shape
    
    # hyperparameters
    HH = pool_param['pool_height']
    WW = pool_param['pool_width']
    stride = pool_param['stride']
    
    # output shape
    H_out = int((H - HH)/stride) + 1
    W_out = int((W - WW)/stride) + 1
    
    # initialize output
    out = np.zeros((N, C, H_out, W_out))
    
    # loop over output channel
    for c in range(C):
        
        # loop over output height
        for i in range(H_out):
            # corresponding input slice
            h_begin = stride*i
            h_end = h_begin + HH
            
            # loop over output width
            for j in range(W_out):
                # corresponding input slice
                w_begin = stride*j
                w_end = w_begin + WW
                
                # input slice
                X_slice = x[:, c, h_begin:h_end, w_begin:w_end]
                
                # update the output
                out[:, c, i, j] = np.max(np.reshape(X_slice, (N,-1)), axis=1)
                
    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    cache = (x, pool_param)
    return out, cache


def max_pool_backward_naive(dout, cache):
    """
    A naive implementation of the backward pass for a max-pooling layer.

    Inputs:
    - dout: Upstream derivatives
    - cache: A tuple of (x, pool_param) as in the forward pass.

    Returns:
    - dx: Gradient with respect to x
    """
    dx = None
    ###########################################################################
    # TODO: Implement the max-pooling backward pass                           #
    ###########################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    
    # unpack cache
    x, pool_param = cache
    
    # input shape
    N, C, H, W = x.shape
    
    # hyperparameters
    HH = pool_param['pool_height']
    WW = pool_param['pool_width']
    stride = pool_param['stride']
    
    # output shape
    _, _, H_out, W_out = dout.shape
    
    # initialize gradient
    dx = np.zeros(x.shape)
    
    # loop over output channel
    for c in range(C):
        
        # loop over output height
        for i in range(H_out):
            # corresponding input slice
            h_begin = stride*i
            h_end = h_begin + HH
            
            # loop over output width
            for j in range(W_out):
                # corresponding input slice
                w_begin = stride*j
                w_end = w_begin + WW
                # input slice
                X_slice = x[:, c, h_begin:h_end, w_begin:w_end]
                
                # corresponding output gradient
                dout_current = np.reshape(dout[:, c, i, j], (-1, 1, 1))
                
                # maxpool output
                out_current = np.reshape(np.max(np.reshape(X_slice, (N,-1)), axis=1), (-1, 1, 1))
                                
                # update the gradient
                dx[:, c, h_begin:h_end, w_begin:w_end] += np.where(X_slice == out_current, dout_current, 0)
                
    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return dx


def spatial_batchnorm_forward(x, gamma, beta, bn_param):
    """
    Computes the forward pass for spatial batch normalization.

    Inputs:
    - x: Input data of shape (N, C, H, W)
    - gamma: Scale parameter, of shape (C,)
    - beta: Shift parameter, of shape (C,)
    - bn_param: Dictionary with the following keys:
      - mode: 'train' or 'test'; required
      - eps: Constant for numeric stability
      - momentum: Constant for running mean / variance. momentum=0 means that
        old information is discarded completely at every time step, while
        momentum=1 means that new information is never incorporated. The
        default of momentum=0.9 should work well in most situations.
      - running_mean: Array of shape (D,) giving running mean of features
      - running_var Array of shape (D,) giving running variance of features

    Returns a tuple of:
    - out: Output data, of shape (N, C, H, W)
    - cache: Values needed for the backward pass
    """
    out, cache = None, None

    ###########################################################################
    # TODO: Implement the forward pass for spatial batch normalization.       #
    #                                                                         #
    # HINT: You can implement spatial batch normalization by calling the      #
    # vanilla version of batch normalization you implemented above.           #
    # Your implementation should be very short; ours is less than five lines. #
    ###########################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    # swap dimensions
    X_swapped = np.swapaxes(x, -1, 1) # (N, W, H, C)
    # reshape to be able to use the vanilla version of batch normalization
    X_flatten = np.reshape(X_swapped, (-1, X_swapped.shape[-1])) # (N*W*H, C)
    # spatial batch normalization
    out_flatten, cache = batchnorm_forward(X_flatten, gamma, beta, bn_param)
    # reshape to match the input size
    out_swapped = np.reshape(out_flatten, X_swapped.shape) # (N, W, H, C)
    # re-swap dimensions
    out = np.swapaxes(out_swapped, -1, 1) # (N, C, H, W)

    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################

    return out, cache


def spatial_batchnorm_backward(dout, cache):
    """
    Computes the backward pass for spatial batch normalization.

    Inputs:
    - dout: Upstream derivatives, of shape (N, C, H, W)
    - cache: Values from the forward pass

    Returns a tuple of:
    - dx: Gradient with respect to inputs, of shape (N, C, H, W)
    - dgamma: Gradient with respect to scale parameter, of shape (C,)
    - dbeta: Gradient with respect to shift parameter, of shape (C,)
    """
    dx, dgamma, dbeta = None, None, None

    ###########################################################################
    # TODO: Implement the backward pass for spatial batch normalization.      #
    #                                                                         #
    # HINT: You can implement spatial batch normalization by calling the      #
    # vanilla version of batch normalization you implemented above.           #
    # Your implementation should be very short; ours is less than five lines. #
    ###########################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    # swap dimensions
    dout_swapped = np.swapaxes(dout, -1, 1) # (N, W, H, C)
    # reshape to be able to use the vanilla version of batch normalization
    dout_flatten = np.reshape(dout_swapped, (-1, dout_swapped.shape[-1])) # (N*W*H, C)
    # spatial batch normalization
    dx_flatten, dgamma, dbeta = batchnorm_backward(dout_flatten, cache)
    # reshape to match the input size
    dx_swapped = np.reshape(dx_flatten, dout_swapped.shape) # (N, W, H, C)
    # re-swap dimensions
    dx = np.swapaxes(dx_swapped, -1, 1) # (N, C, H, W)
    
    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################

    return dx, dgamma, dbeta


def spatial_groupnorm_forward(x, gamma, beta, G, gn_param):
    """
    Computes the forward pass for spatial group normalization.
    In contrast to layer normalization, group normalization splits each entry 
    in the data into G contiguous pieces, which it then normalizes independently.
    Per feature shifting and scaling are then applied to the data, in a manner identical to that of batch normalization and layer normalization.

    Inputs:
    - x: Input data of shape (N, C, H, W)
    - gamma: Scale parameter, of shape (C,)
    - beta: Shift parameter, of shape (C,)
    - G: Integer number of groups to split into, should be a divisor of C
    - gn_param: Dictionary with the following keys:
      - eps: Constant for numeric stability

    Returns a tuple of:
    - out: Output data, of shape (N, C, H, W)
    - cache: Values needed for the backward pass
    """
    out, cache = None, None
    eps = gn_param.get('eps',1e-5)
    ###########################################################################
    # TODO: Implement the forward pass for spatial group normalization.       #
    # This will be extremely similar to the layer norm implementation.        #
    # In particular, think about how you could transform the matrix so that   #
    # the bulk of the code is similar to both train-time batch normalization  #
    # and layer normalization!                                                # 
    ###########################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    
    # reshape the scale and shift factors
    gamma = np.reshape(gamma, (1, x.shape[1], 1, 1))
    beta = np.reshape(beta, (1, x.shape[1], 1, 1))

    # reshape to be able to use the vanilla version of layer normalization
    X_flatten = np.reshape(x, (x.shape[0]*G, -1)) # (N*G, C/G*H*W)
    # spatial group normalization
    out_flatten, cache = layernorm_forward(X_flatten, 1, 0, gn_param)    
    # reshape to match the input size
    out_unflatten = np.reshape(out_flatten, x.shape) # (N, C, W, H)
    # scale and shift
    out = gamma*out_unflatten + beta
    
    # store the scale and shift factors
    cache = (cache, gamma, beta, G)
    
    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return out, cache


def spatial_groupnorm_backward(dout, cache):
    """
    Computes the backward pass for spatial group normalization.

    Inputs:
    - dout: Upstream derivatives, of shape (N, C, H, W)
    - cache: Values from the forward pass

    Returns a tuple of:
    - dx: Gradient with respect to inputs, of shape (N, C, H, W)
    - dgamma: Gradient with respect to scale parameter, of shape (C,)
    - dbeta: Gradient with respect to shift parameter, of shape (C,)
    """
    dx, dgamma, dbeta = None, None, None

    ###########################################################################
    # TODO: Implement the backward pass for spatial group normalization.      #
    # This will be extremely similar to the layer norm implementation.        #
    ###########################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    
    # unpack the cache
    cache, gamma, beta, G = cache
    
    # reshape input to useful dimensions
    X_normalized_reshaped = np.reshape(cache[4], dout.shape) # (N, C, H, W)
    X_normalized_reshaped = np.reshape(np.swapaxes(X_normalized_reshaped, 0, 1), (dout.shape[1], -1)) # (C, N*H*W)
    dout_reshaped = np.reshape(np.swapaxes(dout, 0, 1), (dout.shape[1], -1)) # (C, N*H*W)
    
    # compute the scale and shift factors gradients
    dgamma = np.sum(X_normalized_reshaped * dout_reshaped, axis=1)
    dbeta = np.sum(dout_reshaped, axis=1)
    # reshape to expected dimensions
    dgamma = np.reshape(dgamma, gamma.shape)
    dbeta = np.reshape(dbeta, beta.shape)

    # intermediate gradients of the computational graph
    dout_unflatten = gamma * dout
    # reshape to be able to use the vanilla version of layer normalization
    dout_flatten = np.reshape(dout_unflatten, (dout.shape[0]*G, -1)) # (N*G, C/G*H*W)
    # spatial batch normalization
    dx_flatten, _, _ = layernorm_backward(dout_flatten, cache)
    # reshape to match the input size
    dx = np.reshape(dx_flatten, dout.shape) # (N, C, W, H)
    
    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return dx, dgamma, dbeta


def svm_loss(x, y):
    """
    Computes the loss and gradient using for multiclass SVM classification.

    Inputs:
    - x: Input data, of shape (N, C) where x[i, j] is the score for the jth
      class for the ith input.
    - y: Vector of labels, of shape (N,) where y[i] is the label for x[i] and
      0 <= y[i] < C

    Returns a tuple of:
    - loss: Scalar giving the loss
    - dx: Gradient of the loss with respect to x
    """
    N = x.shape[0]
    correct_class_scores = x[np.arange(N), y]
    margins = np.maximum(0, x - correct_class_scores[:, np.newaxis] + 1.0)
    margins[np.arange(N), y] = 0
    loss = np.sum(margins) / N
    num_pos = np.sum(margins > 0, axis=1)
    dx = np.zeros_like(x)
    dx[margins > 0] = 1
    dx[np.arange(N), y] -= num_pos
    dx /= N
    return loss, dx


def softmax_loss(x, y):
    """
    Computes the loss and gradient for softmax classification.

    Inputs:
    - x: Input data, of shape (N, C) where x[i, j] is the score for the jth
      class for the ith input.
    - y: Vector of labels, of shape (N,) where y[i] is the label for x[i] and
      0 <= y[i] < C

    Returns a tuple of:
    - loss: Scalar giving the loss
    - dx: Gradient of the loss with respect to x
    """
    shifted_logits = x - np.max(x, axis=1, keepdims=True)
    Z = np.sum(np.exp(shifted_logits), axis=1, keepdims=True)
    log_probs = shifted_logits - np.log(Z)
    probs = np.exp(log_probs)
    N = x.shape[0]
    loss = -np.sum(log_probs[np.arange(N), y]) / N
    dx = probs.copy()
    dx[np.arange(N), y] -= 1
    dx /= N
    return loss, dx