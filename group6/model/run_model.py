#!/usr/bin/env python3
"""Reproduce your result by your saved model.

This is a script that helps reproduce your prediction results using your saved
model. This script is unfinished and you need to fill in to make this script
work. If you are using R, please use the R script template instead.

The script needs to work by typing the following commandline (file names can be
different):

python3 run_model.py -i unlabelled_sample.txt -m model.pkl -o output.txt

python run_model.py -i data/Validation_call.txt -m models/model.pkl -o output.txt
"""

# author: Chao (Cico) Zhang
# date: 31 Mar 2017

import argparse
import sys

# Start your coding

# import the library you need here
import pickle
import pandas as pd
import csv
# End your coding



def main():
    """Main function."""
    parser = argparse.ArgumentParser(description='Reproduce the prediction')
    parser.add_argument('-i', '--input', required=True, dest='input_file',
                        metavar='unlabelled_sample.txt', type=str,
                        help='Path of the input file')
    parser.add_argument('-m', '--model', required=True, dest='model_file',
                        metavar='model.pkl', type=str,
                        help='Path of the model file')
    parser.add_argument('-o', '--output', required=True,
                        dest='output_file', metavar='output.txt', type=str,
                        help='Path of the output file')
    # Parse options
    args = parser.parse_args()

    if args.input_file is None:
        sys.exit('Input is missing!')

    if args.model_file is None:
        sys.exit('Model file is missing!')

    if args.output_file is None:
        sys.exit('Output is not designated!')

    # Start your coding

    # suggested steps
    # Step 1: load the model from the model file
    # Step 2: apply the model to the input file to do the prediction
    # Step 3: write the prediction into the desinated output file
    names = ['HER2+', 'HR+', 'Triple Neg']
    
    # Lasso reduction
    l_features = [177, 192, 230, 486, 576, 621, 623, 669, 765, 818, 1009, 1079, 1191, 1206, 1243, 1352, 1558, 1559, 1656, 1838, 1869, 1871, 1881, 1900, 1902, 1906, 1998, 2017, 2026, 2068, 2077, 2078, 2180, 2184, 2188, 2210, 2218, 2501, 2750, 2828]
    
    d_args = vars(args)
    
    df_valid = pd.read_csv(d_args['input_file'], sep='\t', header=0)
    df_valid = df_valid.drop(['Chromosome', 'Start', 'End', 'Nclone'], axis=1)

    df_valid = df_valid.transpose()
    df_valid = df_valid.reset_index()
    df_valid = df_valid.rename(columns={"index": "Sample"})

    print('nr of patients: ', len(df_valid))
    
    # Simple Preprocessing
    X_valid = df_valid[df_valid.columns[1:]]
    samples = df_valid[df_valid.columns[0]]

    # Select same features
    X_valid = X_valid[X_valid.columns[l_features]]
    
    # remove negative values
    X_valid = X_valid.replace(2, 3)
    X_valid = X_valid.replace(1, 2)
    X_valid = X_valid.replace(0, 1)
    X_valid = X_valid.replace(-1, 0)

    best_model = pickle.load(open(d_args['model_file'], 'rb'))
    
    y_pred =  best_model.predict(X_valid)
    
    d = {'"Sample"' : samples, '"Subgroup"': y_pred}
    df = pd.DataFrame(data=d)
    
    # Change to desired Format 
    df['"Sample"'] = df['"Sample"'].apply(lambda x: '"'+ x+ '"')
    df['"Subgroup"'] = df['"Subgroup"'].apply(lambda x: '"'+ names[x]+ '"')

    #df.head()
    
    df.to_csv(d_args['output_file'], quoting=csv.QUOTE_NONE, sep='\t', index=False)
    print(df.head())
    # End your coding


if __name__ == '__main__':
    main()
