# Time-Series-Forecasitng-Using-Neural-Networks
This is a time series forecasting project using Neural Networks. <br>In this project, I try to make a forecast of criminal activities within the City of london. <br>Two Neural Networks algorithms will be utilized i.e `N-BEATS` and `DeepAR`

<h2>Deep AR</h2>
<p>The DeepAR model is a cutting-edge time-series forecasting method that creates a probability distribution across the target variable at each time step, enabling it to be used for probabilistic forecasting. The model is trained to maximize the log-likelihood of the observed data given the input time series and categorical variables. This is accomplished through the training process, which aims to make the negative log-likelihood loss function as little as possible. The model uses various gradient descent techniques, such as stochastic gradient descent (SGD) or the Adam optimizer, to optimize the parameters of the DeepAR model. The predicted parameters computed in the model training process are used to obtain the mean and variance of the Gaussian distribution, which can be used for probabilistic forecasting.</p>

