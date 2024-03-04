![Soccer Image](https://images.unsplash.com/photo-1522778119026-d647f0596c20?q=40&w=1070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D)

# RAMP : Soccer Winning Teams Classification

This is the starting kit for the RAMP on predicting soccer winning teams. The goal is to predict the outcome of a soccer match, given some information about the statistics of the teams such as possession, shots, key passes, etc. The data is provided by the [StatsBomb](https://statsbomb.com/) company, which is a data provider for football (soccer) statistics.

## Getting Started

### Prerequisites

To get started, you need to install the necessary dependencies. You can do this by running the following command in your terminal:

```bash
pip install -r requirements.txt
```

### Data
If you want to download the original data from [Statbomb]("https://github.com/statsbomb/open-data"), you can run the following command:

```bash
python download_data.py
```

After running this command, you will find the data in the `data/statbomb` folder.

Then, to prepare the data for the challenge, you can run the following command:

```bash
python prepare_data.py
```

### Example

You can see an example in the `starting_kit.ipynb` notebook. This notebook will guide you through the process of loading the data, training a model, and making predictions.

## Test a submission

The submissions need to be located in the submissions folder. For instance for `starting_kit`, it should be located in `submissions/starting_kit`.

Then you can run the following command to test the submission:

```bash
ramp-test --submission starting_kit
```

You can get more information regarding this command line:

```bash
ramp-test --help
```

## Authors

This challenge was created by: [Thomas Sinapi](https://github.com/tomasnp), [Ilyes Tebourski](https://github.com/ilyes-tebourski), [Julien Maille-Paez](https://github.com/julienMP06), [Mohamed Hamdouni](https://github.com/Mohamed-Hamdouni) and [Manitas Bahri](https://github.com/b-manitas)
