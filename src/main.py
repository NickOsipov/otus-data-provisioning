"""
Module: main.py
"""

import argparse
import sys
from pyspark.sql import SparkSession
from pyspark.ml import PipelineModel
from pyspark.sql.functions import *


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Credit Card Customers churn prediction",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
        Examples:
            python main.py  # Uses default paths
            python main.py -m models/pipelineModel -i data/BankChurners.csv -o results/predictions
            python main.py -i data/custom_data.csv -o results/custom_predictions
        """
    )
    
    parser.add_argument(
        "-m", "--model",
        default="models/pipelineModel",
        help="Path to the trained model directory (default: models/pipelineModel)"
    )
    
    parser.add_argument(
        "-i", "--input",
        default="data/BankChurners.csv",
        help="Path to the input CSV file (default: data/BankChurners.csv)"
    )
    
    parser.add_argument(
        "-o", "--output",
        default="data/predictions",
        help="Path to the output directory for predictions (default: data/predictions.csv)"
    )
    
    parser.add_argument(
        "--master",
        default="local[*]",
        help="Spark master URL (default: local[*])"
    )
    
    parser.add_argument(
        "--app-name",
        default="CreditCardCustomers",
        help="Spark application name (default: CreditCardCustomers)"
    )
    
    return parser.parse_args()


def main():
    """Main function."""
    args = parse_args()
    
    # Create Spark session
    spark = (SparkSession
        .builder
        .master(args.master)
        .appName(args.app_name)
        .getOrCreate()
    )

    try:
        # Load the trained model
        print(f"Loading model from: {args.model}")
        model = PipelineModel.load(args.model)

        # Read input data
        print(f"Reading data from: {args.input}")
        data = (spark
            .read
            .option("header", "true")
            .option("inferSchema", "true")
            .csv(args.input))

        # Make predictions
        print("Making predictions...")
        predicted = model.transform(data)

        # Filter and save predictions
        print(f"Saving predictions to: {args.output}")
        (predicted
            .filter(col("prediction") == 1)
            .select("CLIENTNUM")
            .repartition(1)
            .write
            .mode("overwrite")
            .csv(args.output))
        
        print("Prediction completed successfully!")
        
    except Exception as e:
        print(f"Error: {e}")
        spark.stop()
        sys.exit(1)
    
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
