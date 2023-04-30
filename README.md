# seenons-open-aws-serverless-ml
Seenons recipe for serverless Machine Learning in AWS. 

## Introduction

This repository contains the code for the Seenons recipe for serverless Machine Learning in AWS. The recipe is described in detail in the [Seenons blog](https://seenons.com/blog/2019/03/01/serverless-machine-learning-in-aws/).

## Installation

The recipe is implemented as a Pulumi program. To install the recipe, follow these steps:   

1. Install [Pulumi](https://www.pulumi.com/docs/get-started/aws/install-pulumi/).
2. Clone this repository.
3. Create a new Pulumi stack in the repository folder.
4. Update your lambda function `lambda/lambda_function.py`  accordingly to  your needs.  
5. Run `pulumi up` to deploy the stack.

## Architecture

The recipe implements the following architecture:

![Machine Learning Serverless Architecture](docs/sl-ml-arch.png?raw=true "Machine Learning Serverless Architecture")

The architecture consists of the following components:

* **S3 bucket**: The S3 bucket is used to store the training data and the training output.
* **Lambda function**: The Lambda function is used to train the model. The function is triggered by a signal sent by S3.


## Usage

To train and obtain your results, follow these steps:

1. Upload the training data to the S3 bucket. The training data must be in CSV format. The first column must contain the target variable. The remaining columns must contain the features. The first row must contain the column names. The training data must be stored in the file path configured in the `filter_prefix=<prefix>` parameter of the S3 trigger (check `create_bucket.py` file)
2. By default, output files are placed in a specific folder defined in `lambda/lambda_function.py` file.

## License

This project is licensed under the terms of the BSD-3-Clause license. See the [LICENSE](LICENSE) file.
